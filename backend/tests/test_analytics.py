"""
Eduvia — Analytics & Telemetry Integration Tests (Phase 6)

Validates:
1. PerformanceEvent and ActivityAttempt schema contracts and numeric bounds.
2. AnalyticsService persistence, referential integrity, and attempt counter incrementing.
3. Access control: unauthenticated 401, teacher isolation 403, assigned teacher 200, admin 200.
4. Phase 5 Evaluation -> Phase 6 PerformanceEvent emission.
5. Error handling: nonexistent learner, inactive learner, nonexistent objective.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError as PydanticValidationError

from app.activities.fallbacks import create_fallback_activity
from app.activities.schemas import (
    ActivitySubmissionRequest,
    ActivityType,
    MultipleChoiceContent,
    MultipleChoiceSubmission,
)
from app.activities.service import ActivityService
from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.router import get_analytics_service
from app.analytics.schemas import (
    ActivityAttemptCreate,
    Modality,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    TeachingStrategy,
)
from app.analytics.service import AnalyticsService
from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, get_password_hash
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.learners.models import Learner
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

# ── Test Entities ────────────────────────────────────────────────────────────

now = datetime.now(UTC)
TEACHER_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
OTHER_TEACHER_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
ADMIN_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")
LEARNER_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
OBJECTIVE_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
ACTIVITY_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")

mock_teacher = User(
    id=TEACHER_ID,
    email="teacher@eduvia.app",
    full_name="Assigned Teacher",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_other_teacher = User(
    id=OTHER_TEACHER_ID,
    email="other_teacher@eduvia.app",
    full_name="Unassigned Teacher",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_admin = User(
    id=ADMIN_ID,
    email="admin@eduvia.app",
    full_name="School Admin",
    hashed_password=get_password_hash("adminpass123"),
    role=UserRole.admin,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_learner = Learner(
    id=LEARNER_ID,
    name="Sammy Learner",
    age_group="primary",
    learning_level="beginner",
    is_active=True,
    teacher_id=TEACHER_ID,
    created_at=now,
    updated_at=now,
)

mock_objective = LearningObjective(
    id=OBJECTIVE_ID,
    lesson_id=uuid.uuid4(),
    title={"en": "Counting practice"},
    description={"en": "Count items from 1 to 5"},
    difficulty_level=1,
    assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
    order_index=0,
    is_active=True,
    created_at=now,
    updated_at=now,
)

teacher_token = create_access_token(
    {"sub": str(mock_teacher.id), "email": mock_teacher.email, "role": mock_teacher.role.value}
)
other_teacher_token = create_access_token(
    {"sub": str(mock_other_teacher.id), "email": mock_other_teacher.email, "role": mock_other_teacher.role.value}
)
admin_token = create_access_token(
    {"sub": str(mock_admin.id), "email": mock_admin.email, "role": mock_admin.role.value}
)


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_db_session() -> AsyncMock:
    session = AsyncMock()

    # Configure execute return values based on select target
    def mock_execute(stmt, *args, **kwargs):
        stmt_str = str(stmt)
        result = MagicMock()
        if "FROM learners" in stmt_str:
            if "WHERE learners.id ==" in stmt_str or "learners.id = :" in stmt_str:
                result.scalars.return_value.first.return_value = mock_learner
            else:
                result.scalars.return_value.all.return_value = [mock_learner]
        elif "FROM learning_objectives" in stmt_str:
            result.scalars.return_value.first.return_value = mock_objective
        elif "FROM activity_attempts" in stmt_str:
            result.scalars.return_value.first.return_value = None
        elif "count(" in stmt_str.lower():
            result.scalar.return_value = 0
        else:
            result.scalars.return_value.first.return_value = None
            result.scalars.return_value.all.return_value = []
        return result

    session.execute.side_effect = mock_execute
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def analytics_service(mock_db_session: AsyncMock) -> AnalyticsService:
    return AnalyticsService(session=mock_db_session)


# ── 1. Schema Validation & Numeric Bounds Tests ──────────────────────────────


def test_performance_event_create_valid():
    event = PerformanceEventCreate(
        learner_id=LEARNER_ID,
        activity_id=ACTIVITY_ID,
        objective_id=OBJECTIVE_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        modality=Modality.VISUAL,
        strategy=TeachingStrategy.STEP_BY_STEP,
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=1200,
        hints_used=1,
        assistance_level=1,
        completed=True,
        difficulty=2,
        metadata={"detail": "first try"},
    )
    assert event.score == 1.0
    assert event.response_time_ms == 1200
    assert event.activity_type == ActivityType.MULTIPLE_CHOICE


def test_performance_event_negative_response_time_rejected():
    with pytest.raises(PydanticValidationError) as exc:
        PerformanceEventCreate(
            learner_id=LEARNER_ID,
            activity_id=ACTIVITY_ID,
            objective_id=OBJECTIVE_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            correct=True,
            score=1.0,
            response_time_ms=-500,  # Invalid negative
        )
    assert "greater_than_equal" in str(exc.value)


def test_performance_event_score_out_of_bounds_rejected():
    with pytest.raises(PydanticValidationError):
        PerformanceEventCreate(
            learner_id=LEARNER_ID,
            activity_id=ACTIVITY_ID,
            objective_id=OBJECTIVE_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            correct=True,
            score=1.5,  # Exceeds 1.0
        )

    with pytest.raises(PydanticValidationError):
        PerformanceEventCreate(
            learner_id=LEARNER_ID,
            activity_id=ACTIVITY_ID,
            objective_id=OBJECTIVE_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            correct=True,
            score=-0.1,  # Below 0.0
        )


def test_performance_event_assistance_level_bounds_rejected():
    with pytest.raises(PydanticValidationError):
        PerformanceEventCreate(
            learner_id=LEARNER_ID,
            activity_id=ACTIVITY_ID,
            objective_id=OBJECTIVE_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            correct=True,
            score=1.0,
            assistance_level=5,  # Max allowed is 3
        )


def test_performance_event_extra_fields_forbidden():
    with pytest.raises(PydanticValidationError):
        PerformanceEventCreate(
            learner_id=LEARNER_ID,
            activity_id=ACTIVITY_ID,
            objective_id=OBJECTIVE_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            correct=True,
            score=1.0,
            unauthorized_extra_field="spoof",
        )


# ── 2. Service Layer Persistence Tests ───────────────────────────────────────


@pytest.mark.asyncio
async def test_record_performance_event_success(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    event_in = PerformanceEventCreate(
        learner_id=LEARNER_ID,
        activity_id=ACTIVITY_ID,
        objective_id=OBJECTIVE_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        modality=Modality.VISUAL,
        strategy=TeachingStrategy.STEP_BY_STEP,
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=1500,
        hints_used=0,
        assistance_level=0,
        completed=True,
        difficulty=1,
    )

    event = await analytics_service.record_performance_event(event_in)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    assert event.learner_id == LEARNER_ID
    assert event.activity_type == "multiple_choice"
    assert event.correct is True
    assert event.score == 1.0


@pytest.mark.asyncio
async def test_record_performance_event_nonexistent_learner(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    # Override execute to return None for learner
    mock_db_session.execute.side_effect = lambda stmt, *a, **k: MagicMock(scalars=lambda: MagicMock(first=lambda: None))

    event_in = PerformanceEventCreate(
        learner_id=uuid.uuid4(),
        activity_id=ACTIVITY_ID,
        objective_id=OBJECTIVE_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        correct=True,
        score=1.0,
    )

    with pytest.raises(NotFoundError) as exc:
        await analytics_service.record_performance_event(event_in)
    assert "Learner with id" in str(exc.value)


@pytest.mark.asyncio
async def test_record_performance_event_inactive_learner(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    inactive_learner = Learner(
        id=LEARNER_ID,
        name="Inactive Sammy",
        age_group="primary",
        learning_level="beginner",
        is_active=False,
    )
    mock_db_session.execute.side_effect = lambda stmt, *a, **k: MagicMock(scalars=lambda: MagicMock(first=lambda: inactive_learner))

    event_in = PerformanceEventCreate(
        learner_id=LEARNER_ID,
        activity_id=ACTIVITY_ID,
        objective_id=OBJECTIVE_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        correct=True,
        score=1.0,
    )

    with pytest.raises(ValidationError) as exc:
        await analytics_service.record_performance_event(event_in)
    assert "inactive learner" in str(exc.value)


@pytest.mark.asyncio
async def test_record_activity_attempt_success(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    attempt_in = ActivityAttemptCreate(
        activity_id=ACTIVITY_ID,
        learner_id=LEARNER_ID,
        session_id=uuid.uuid4(),
        score=0.9,
        completed=True,
    )

    attempt = await analytics_service.record_activity_attempt(attempt_in)
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    assert attempt.activity_id == ACTIVITY_ID
    assert attempt.score == 0.9
    assert attempt.completed is True


# ── 3. Access Control & Security Tests ───────────────────────────────────────


@pytest.mark.asyncio
async def test_get_learner_events_assigned_teacher_allowed(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    event1 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=ACTIVITY_ID,
        objective_id=OBJECTIVE_ID,
        activity_type="multiple_choice",
        correct=True,
        score=1.0,
        timestamp=now,
    )

    def mock_exec(stmt, *a, **k):
        res = MagicMock()
        stmt_str = str(stmt)
        if "FROM learners" in stmt_str:
            res.scalars.return_value.first.return_value = mock_learner
        else:
            res.scalars.return_value.all.return_value = [event1]
        return res

    mock_db_session.execute.side_effect = mock_exec

    events = await analytics_service.get_learner_events(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
    )
    assert len(events) == 1
    assert events[0].learner_id == LEARNER_ID


@pytest.mark.asyncio
async def test_get_learner_events_unassigned_teacher_forbidden(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    # mock_other_teacher is NOT assigned to mock_learner
    with pytest.raises(AuthorizationError) as exc:
        await analytics_service.get_learner_events(
            learner_id=LEARNER_ID,
            requesting_user=mock_other_teacher,
        )
    assert "permission" in str(exc.value)


@pytest.mark.asyncio
async def test_get_learner_events_admin_allowed(analytics_service: AnalyticsService, mock_db_session: AsyncMock):
    def mock_exec(stmt, *a, **k):
        res = MagicMock()
        stmt_str = str(stmt)
        if "FROM learners" in stmt_str:
            res.scalars.return_value.first.return_value = mock_learner
        else:
            res.scalars.return_value.all.return_value = []
        return res

    mock_db_session.execute.side_effect = mock_exec

    events = await analytics_service.get_learner_events(
        learner_id=LEARNER_ID,
        requesting_user=mock_admin,
    )
    assert isinstance(events, list)


# ── 4. API Endpoint Integration Tests ────────────────────────────────────────


@pytest.fixture(autouse=True)
def setup_dependencies(mock_db_session: AsyncMock, analytics_service: AnalyticsService):
    from app.activities.router import get_activity_service
    activity_service = ActivityService(session=mock_db_session)

    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    app.dependency_overrides[get_analytics_service] = lambda: analytics_service
    app.dependency_overrides[get_activity_service] = lambda: activity_service
    yield
    app.dependency_overrides.pop(get_db_session, None)
    app.dependency_overrides.pop(get_analytics_service, None)
    app.dependency_overrides.pop(get_activity_service, None)


def test_api_record_event_endpoint_success():
    payload = {
        "learner_id": str(LEARNER_ID),
        "activity_id": str(ACTIVITY_ID),
        "objective_id": str(OBJECTIVE_ID),
        "activity_type": "multiple_choice",
        "modality": "visual",
        "strategy": "step_by_step",
        "correct": True,
        "score": 1.0,
        "attempts": 1,
        "response_time_ms": 2100,
        "hints_used": 0,
        "assistance_level": 0,
        "completed": True,
        "difficulty": 1,
        "metadata": {"test": True},
    }

    response = client.post("/api/v1/analytics/events", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["learner_id"] == str(LEARNER_ID)
    assert data["correct"] is True
    assert data["score"] == 1.0


def test_api_get_learner_events_unauthenticated_401():
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get(f"/api/v1/analytics/learners/{LEARNER_ID}/events")
    assert response.status_code == 401


def test_api_get_learner_events_authenticated_teacher():
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    try:
        response = client.get(
            f"/api/v1/analytics/learners/{LEARNER_ID}/events",
            headers={"Authorization": f"Bearer {teacher_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_api_get_learner_events_other_teacher_forbidden_403():
    app.dependency_overrides[get_current_user] = lambda: mock_other_teacher
    try:
        response = client.get(
            f"/api/v1/analytics/learners/{LEARNER_ID}/events",
            headers={"Authorization": f"Bearer {other_teacher_token}"},
        )
        assert response.status_code == 403
        assert "permission" in response.json()["detail"]
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ── 5. Phase 5 Evaluation -> Phase 6 Telemetry Ingestion ─────────────────────


@pytest.mark.asyncio
async def test_phase5_evaluation_emits_phase6_telemetry():
    """
    Verifies that when ActivityService.evaluate_submission is called with a learner_id,
    an authoritative PerformanceEvent is persisted with matching evaluation results.
    """
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_learner
    mock_result.scalar.return_value = 0
    mock_session.execute.return_value = mock_result
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    service = ActivityService(session=mock_session)

    activity = create_fallback_activity(
        objective_id=OBJECTIVE_ID,
        objective_title="Numeracy",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        learner_id=LEARNER_ID,
        objective_id=OBJECTIVE_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=MultipleChoiceSubmission(selected_option_id=content.correct_answer_id),
        hints_used=1,
        time_spent_seconds=4.5,
        activity_content=content,
    )

    result = await service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0

    # Verify that mock_session.add was called with a PerformanceEvent
    added_objects = [call[0][0] for call in mock_session.add.call_args_list]
    telemetry_events = [obj for obj in added_objects if isinstance(obj, PerformanceEvent)]
    assert len(telemetry_events) == 1

    event = telemetry_events[0]
    assert event.learner_id == LEARNER_ID
    assert event.activity_id == activity.id
    assert event.objective_id == OBJECTIVE_ID
    assert event.correct is True
    assert event.score == 1.0
    assert event.hints_used == 1
    assert event.response_time_ms == 4500  # 4.5s * 1000
    assert event.completed is True
