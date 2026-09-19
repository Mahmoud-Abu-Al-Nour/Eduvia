"""
Eduvia — Phase 7: Learner Analytics & Mastery Tracking Test Suite

Verifies:
1. Aggregation calculations (accuracy, average score, response latency, hints, assistance levels).
2. Modality & activity type breakdowns.
3. Deterministic objective mastery rubric:
   - Accuracy >= min_accuracy (default 0.80) AND avg_assistance <= max_assistance (default 1).
   - Denial of mastery when assistance level is excessive despite 100% accuracy.
4. Longitudinal progress timeline grouped chronologically by calendar day.
5. Teacher multi-tenant isolation and 403 Forbidden access control.
6. Administrator global access and 401 Unauthorized unauthenticated enforcement.
7. Safe zero-state responses for learners with zero activity history.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.analytics.models import PerformanceEvent
from app.analytics.schemas import (
    ActivityTypeMetrics,
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    LearnerProgressReport,
    ModalityMetrics,
    ObjectiveMasteryStatus,
    ProgressDataPoint,
)
from app.analytics.service import AnalyticsService
from app.auth.dependencies import get_current_user
from app.core.errors import AuthorizationError, NotFoundError
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.learners.models import Learner
from app.main import app
from app.users.models import User, UserRole

# ── Test Fixtures & Constants ────────────────────────────────────────────────

LEARNER_ID = uuid.uuid4()
TEACHER_ID = uuid.uuid4()
OTHER_TEACHER_ID = uuid.uuid4()
ADMIN_ID = uuid.uuid4()
OBJECTIVE_ID_1 = uuid.uuid4()
OBJECTIVE_ID_2 = uuid.uuid4()

mock_teacher = User(
    id=TEACHER_ID,
    email="assigned.teacher@eduvia.app",
    full_name="Assigned Teacher",
    role=UserRole.teacher.value,
    is_active=True,
)

mock_other_teacher = User(
    id=OTHER_TEACHER_ID,
    email="other.teacher@eduvia.app",
    full_name="Other Teacher",
    role=UserRole.teacher.value,
    is_active=True,
)

mock_admin = User(
    id=ADMIN_ID,
    email="admin@eduvia.app",
    full_name="Administrator",
    role=UserRole.admin.value,
    is_active=True,
)

mock_learner = Learner(
    id=LEARNER_ID,
    name="Test Learner",
    age_group="childhood",
    learning_level="developing",
    is_active=True,
    teacher_id=TEACHER_ID,
)

mock_obj_1 = LearningObjective(
    id=OBJECTIVE_ID_1,
    lesson_id=uuid.uuid4(),
    title="Count Objects 1–10",
    difficulty_level=1,
    is_active=True,
    assessment_criteria={
        "minimum_accuracy": 0.80,
        "maximum_assistance_level": 1,
        "required_completion": True,
    },
)

mock_obj_2 = LearningObjective(
    id=OBJECTIVE_ID_2,
    lesson_id=uuid.uuid4(),
    title="Identify Basic Shapes",
    difficulty_level=2,
    is_active=True,
    assessment_criteria={
        "minimum_accuracy": 0.75,
        "maximum_assistance_level": 1,
        "required_completion": True,
    },
)

client = TestClient(app)


@pytest.fixture
def mock_db_session() -> AsyncMock:
    session = AsyncMock()

    def mock_execute(stmt, *args, **kwargs):
        stmt_str = str(stmt)
        result = MagicMock()
        if "FROM learners" in stmt_str:
            result.scalars.return_value.first.return_value = mock_learner
            result.scalars.return_value.all.return_value = [mock_learner]
        elif "FROM learning_objectives" in stmt_str:
            result.scalars.return_value.first.return_value = mock_obj_1
            result.scalars.return_value.all.return_value = [mock_obj_1, mock_obj_2]
        elif "FROM performance_events" in stmt_str:
            result.scalars.return_value.all.return_value = []
        else:
            result.scalars.return_value.first.return_value = None
            result.scalars.return_value.all.return_value = []
        return result

    session.execute.side_effect = mock_execute
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def analytics_service(mock_db_session: AsyncMock) -> AnalyticsService:
    return AnalyticsService(mock_db_session)


@pytest.fixture(autouse=True)
def setup_dependencies(mock_db_session: AsyncMock, analytics_service: AnalyticsService):
    from app.analytics.router import get_analytics_service

    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    app.dependency_overrides[get_analytics_service] = lambda: analytics_service
    yield
    app.dependency_overrides.pop(get_db_session, None)
    app.dependency_overrides.pop(get_analytics_service, None)


# ── 1. Schema Validation Tests ───────────────────────────────────────────────


def test_modality_metrics_schema_valid():
    metric = ModalityMetrics(
        modality="visual",
        total_events=10,
        accuracy=0.9,
        avg_score=0.88,
        avg_response_time_ms=3200.0,
        avg_assistance_level=0.5,
    )
    assert metric.modality == "visual"
    assert metric.total_events == 10
    assert metric.accuracy == 0.9


def test_objective_mastery_status_schema_valid():
    status = ObjectiveMasteryStatus(
        objective_id=OBJECTIVE_ID_1,
        objective_title="Count Objects 1–10",
        difficulty_level=1,
        total_attempts=5,
        accuracy=0.85,
        avg_assistance_level=0.8,
        mastery_achieved=True,
        status="mastered",
    )
    assert status.mastery_achieved is True
    assert status.status == "mastered"


# ── 2. Summary Aggregation Unit Tests ────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_learner_summary_zero_events(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """Verifies that a learner with zero events produces safe empty-state analytics."""
    learner_result = MagicMock()
    learner_result.scalars.return_value.first.return_value = mock_learner

    events_result = MagicMock()
    events_result.scalars.return_value.all.return_value = []

    mock_db_session.execute.side_effect = [learner_result, events_result]

    summary = await analytics_service.get_learner_summary(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
    )

    assert summary.learner_id == LEARNER_ID
    assert summary.total_events == 0
    assert summary.completed_activities == 0
    assert summary.overall_accuracy == 0.0
    assert summary.avg_score == 0.0
    assert summary.avg_response_time_ms == 0.0
    assert len(summary.modality_breakdown) == 0
    assert len(summary.activity_type_breakdown) == 0


@pytest.mark.asyncio
async def test_get_learner_summary_calculated_accurately(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """Verifies aggregate accuracy, latency, and breakdown computations."""
    now = datetime.now(timezone.utc)
    ev1 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        objective_id=OBJECTIVE_ID_1,
        activity_type="multiple_choice",
        modality="visual",
        strategy="step_by_step",
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=4000,
        hints_used=1,
        assistance_level=1,
        completed=True,
        timestamp=now - timedelta(hours=2),
    )
    ev2 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        objective_id=OBJECTIVE_ID_1,
        activity_type="matching",
        modality="interactive",
        strategy="scaffolding",
        correct=False,
        score=0.5,
        attempts=2,
        response_time_ms=6000,
        hints_used=2,
        assistance_level=2,
        completed=True,
        timestamp=now - timedelta(hours=1),
    )

    learner_result = MagicMock()
    learner_result.scalars.return_value.first.return_value = mock_learner

    events_result = MagicMock()
    events_result.scalars.return_value.all.return_value = [ev1, ev2]

    mock_db_session.execute.side_effect = [learner_result, events_result]

    summary = await analytics_service.get_learner_summary(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
    )

    assert summary.total_events == 2
    assert summary.completed_activities == 2
    assert summary.overall_accuracy == 0.5  # 1 correct out of 2
    assert summary.avg_score == 0.75  # (1.0 + 0.5) / 2
    assert summary.avg_response_time_ms == 5000.0  # (4000 + 6000) / 2
    assert summary.avg_hints_per_activity == 1.5  # (1 + 2) / 2
    assert summary.avg_assistance_level == 1.5  # (1 + 2) / 2

    # Check Modality Breakdown
    assert len(summary.modality_breakdown) == 2
    visual_mod = next(m for m in summary.modality_breakdown if m.modality == "visual")
    assert visual_mod.total_events == 1
    assert visual_mod.accuracy == 1.0
    assert visual_mod.avg_response_time_ms == 4000.0

    inter_mod = next(m for m in summary.modality_breakdown if m.modality == "interactive")
    assert inter_mod.total_events == 1
    assert inter_mod.accuracy == 0.0


# ── 3. Objective Mastery Deterministic Rubric Tests ─────────────────────────


@pytest.mark.asyncio
async def test_get_learner_mastery_rubric_achieved(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """
    Test mastery achieved: Accuracy >= 80% with assistance <= Level 1.
    """
    now = datetime.now(timezone.utc)
    ev1 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        objective_id=OBJECTIVE_ID_1,
        activity_type="multiple_choice",
        modality="visual",
        strategy="step_by_step",
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=3000,
        hints_used=0,
        assistance_level=0,  # Level 0
        completed=True,
        timestamp=now - timedelta(hours=2),
    )
    ev2 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        objective_id=OBJECTIVE_ID_1,
        activity_type="multiple_choice",
        modality="visual",
        strategy="step_by_step",
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=3500,
        hints_used=1,
        assistance_level=1,  # Level 1
        completed=True,
        timestamp=now - timedelta(hours=1),
    )

    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner

    events_res = MagicMock()
    events_res.scalars.return_value.all.return_value = [ev1, ev2]

    obj_res = MagicMock()
    obj_res.scalars.return_value.all.return_value = [mock_obj_1]

    mock_db_session.execute.side_effect = [learner_res, events_res, obj_res]

    report = await analytics_service.get_learner_mastery(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
    )

    assert report.total_objectives_evaluated == 1
    assert report.mastered_count == 1
    assert report.in_progress_count == 0
    assert report.mastery_percentage == 100.0
    status_obj = report.objectives[0]
    assert status_obj.objective_id == OBJECTIVE_ID_1
    assert status_obj.accuracy == 1.0
    assert status_obj.avg_assistance_level == 0.5  # (0 + 1) / 2 <= 1.0
    assert status_obj.status == "mastered"
    assert status_obj.mastery_achieved is True


@pytest.mark.asyncio
async def test_get_learner_mastery_denied_when_assistance_excessive(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """
    CRITICAL: Verifies pedagogical rule that 100% accuracy does NOT grant mastery
    if the learner required high assistance (e.g. Level 3 full demonstration).
    """
    now = datetime.now(timezone.utc)
    ev1 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        objective_id=OBJECTIVE_ID_1,
        activity_type="multiple_choice",
        modality="visual",
        strategy="demonstration",
        correct=True,
        score=1.0,
        attempts=1,
        response_time_ms=4000,
        hints_used=3,
        assistance_level=3,  # Level 3 full demonstration
        completed=True,
        timestamp=now,
    )

    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner

    events_res = MagicMock()
    events_res.scalars.return_value.all.return_value = [ev1]

    obj_res = MagicMock()
    obj_res.scalars.return_value.all.return_value = [mock_obj_1]

    mock_db_session.execute.side_effect = [learner_res, events_res, obj_res]

    report = await analytics_service.get_learner_mastery(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
    )

    assert report.mastered_count == 0
    assert report.in_progress_count == 1
    assert report.mastery_percentage == 0.0
    status_obj = report.objectives[0]
    assert status_obj.accuracy == 1.0
    assert status_obj.avg_assistance_level == 3.0  # > max_assistance_level (1)
    assert status_obj.status == "in_progress"
    assert status_obj.mastery_achieved is False


# ── 4. Longitudinal Progress Timeline Tests ──────────────────────────────────


@pytest.mark.asyncio
async def test_get_learner_progress_timeline(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """Verifies chronological grouping of events into daily performance points."""
    day1 = datetime(2026, 9, 10, 10, 0, tzinfo=timezone.utc)
    day2 = datetime(2026, 9, 11, 14, 0, tzinfo=timezone.utc)

    ev1 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        correct=True,
        score=1.0,
        response_time_ms=2000,
        timestamp=day1,
    )
    ev2 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        correct=False,
        score=0.0,
        response_time_ms=3000,
        timestamp=day1,
    )
    ev3 = PerformanceEvent(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        activity_id=uuid.uuid4(),
        correct=True,
        score=1.0,
        response_time_ms=2500,
        timestamp=day2,
    )

    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner

    events_res = MagicMock()
    events_res.scalars.return_value.all.return_value = [ev1, ev2, ev3]

    mock_db_session.execute.side_effect = [learner_res, events_res]

    progress_report = await analytics_service.get_learner_progress(
        learner_id=LEARNER_ID,
        requesting_user=mock_teacher,
        days=30,
    )

    assert progress_report.total_days_active == 2
    assert len(progress_report.data_points) == 2

    dp1 = progress_report.data_points[0]
    assert dp1.date == "2026-09-10"
    assert dp1.events_count == 2
    assert dp1.accuracy == 0.5
    assert dp1.avg_score == 0.5

    dp2 = progress_report.data_points[1]
    assert dp2.date == "2026-09-11"
    assert dp2.events_count == 1
    assert dp2.accuracy == 1.0
    assert dp2.avg_score == 1.0


# ── 5. Authorization & Multi-Tenant Security Tests ───────────────────────────


@pytest.mark.asyncio
async def test_summary_unassigned_teacher_forbidden_403(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """Verifies that an unassigned teacher is forbidden from accessing analytics."""
    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner
    mock_db_session.execute.return_value = learner_res

    with pytest.raises(AuthorizationError) as exc:
        await analytics_service.get_learner_summary(
            learner_id=LEARNER_ID,
            requesting_user=mock_other_teacher,
        )
    assert "permission" in str(exc.value)


@pytest.mark.asyncio
async def test_mastery_unassigned_teacher_forbidden_403(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner
    mock_db_session.execute.return_value = learner_res

    with pytest.raises(AuthorizationError):
        await analytics_service.get_learner_mastery(
            learner_id=LEARNER_ID,
            requesting_user=mock_other_teacher,
        )


@pytest.mark.asyncio
async def test_admin_global_access_allowed(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    """Verifies that an admin can view any learner's analytics without restrictions."""
    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = mock_learner

    events_res = MagicMock()
    events_res.scalars.return_value.all.return_value = []

    mock_db_session.execute.side_effect = [learner_res, events_res]

    summary = await analytics_service.get_learner_summary(
        learner_id=LEARNER_ID,
        requesting_user=mock_admin,
    )
    assert summary.learner_id == LEARNER_ID


@pytest.mark.asyncio
async def test_nonexistent_learner_returns_404(
    analytics_service: AnalyticsService, mock_db_session: AsyncMock
):
    learner_res = MagicMock()
    learner_res.scalars.return_value.first.return_value = None
    mock_db_session.execute.side_effect = None
    mock_db_session.execute.return_value = learner_res

    with pytest.raises(NotFoundError):
        await analytics_service.get_learner_summary(
            learner_id=uuid.uuid4(),
            requesting_user=mock_teacher,
        )


# ── 6. REST API Endpoint Integration Tests ───────────────────────────────────


def test_api_summary_unauthenticated_returns_401():
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get(f"/api/v1/analytics/learners/{LEARNER_ID}/summary")
    assert response.status_code == 401


def test_api_summary_authenticated_teacher_success():
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    try:
        response = client.get(
            f"/api/v1/analytics/learners/{LEARNER_ID}/summary",
            headers={"Authorization": "Bearer test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_ID)
        assert "overall_accuracy" in data
        assert "modality_breakdown" in data
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_api_mastery_authenticated_teacher_success():
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    try:
        response = client.get(
            f"/api/v1/analytics/learners/{LEARNER_ID}/mastery",
            headers={"Authorization": "Bearer test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_ID)
        assert "mastery_percentage" in data
        assert "objectives" in data
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_api_progress_authenticated_teacher_success():
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    try:
        response = client.get(
            f"/api/v1/analytics/learners/{LEARNER_ID}/progress?days=14",
            headers={"Authorization": "Bearer test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_ID)
        assert "data_points" in data
    finally:
        app.dependency_overrides.pop(get_current_user, None)
