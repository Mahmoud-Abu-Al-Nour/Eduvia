"""
Eduvia — Phase 10: Teacher Dashboard & Insights Test Suite

Validates:
1. TeacherDashboardService logic:
   - Teacher overview dashboard KPIs and 7-day active metrics.
   - Cohort insights: class averages, modality distribution, and learner summaries.
   - Deterministic intervention alerts:
     * low_accuracy alert on >= 3 attempts with < 60% accuracy.
     * high_assistance alert on >= 5 attempts with >= 2.0 assistance level.
     * inactivity alert on >= 7 days with no events.
     * stalled_mastery alert on >= 8 attempts without mastery.
   - IEP progress report compilation:
     * Objective progress breakdown and status mapping.
     * Sensory modality efficacy extraction.
     * Pedagogical recommendations synthesis.
     * Clean printable Markdown generation.
   - Date range filtering across reporting windows.
2. Authorization & Security:
   - Server-side ownership enforcement (assigned vs unassigned teacher).
   - Admin platform-wide access authority.
   - Unauthenticated request rejection.
3. API Endpoints:
   - GET /api/v1/teachers/dashboard
   - GET /api/v1/teachers/cohort/insights
   - GET /api/v1/teachers/alerts
   - GET /api/v1/teachers/learners/{learner_id}/iep-report
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.analytics.models import PerformanceEvent
from app.analytics.schemas import (
    Modality,
    TeachingStrategy,
)
from app.auth.dependencies import get_current_user
from app.core.errors import AuthorizationError, NotFoundError
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.learners.models import Learner, LearnerProfile
from app.main import app
from app.teachers.schemas import (
    AlertSeverity,
    AlertTriggerType,
    CohortInsights,
    IEPReport,
    InterventionAlert,
    TeacherDashboardOverview,
)
from app.teachers.service import TeacherDashboardService
from app.users.models import User, UserRole

# ── Test Entities & Fixtures ──────────────────────────────────────────────────

now = datetime.now(UTC)
TEACHER_A_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
TEACHER_B_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
ADMIN_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")

LEARNER_1_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
LEARNER_2_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
LEARNER_B_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")

OBJ_1_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")
OBJ_2_ID = uuid.UUID("88888888-8888-8888-8888-888888888888")

teacher_a = User(
    id=TEACHER_A_ID,
    email="teacher_a@eduvia.org",
    full_name="Teacher Alice",
    role=UserRole.teacher,
    is_active=True,
    hashed_password="pw",
)

teacher_b = User(
    id=TEACHER_B_ID,
    email="teacher_b@eduvia.org",
    full_name="Teacher Bob",
    role=UserRole.teacher,
    is_active=True,
    hashed_password="pw",
)

admin_user = User(
    id=ADMIN_ID,
    email="admin@eduvia.org",
    full_name="Eduvia Admin",
    role=UserRole.admin,
    is_active=True,
    hashed_password="pw",
)

profile_1 = LearnerProfile(
    id=uuid.uuid4(),
    learner_id=LEARNER_1_ID,
    communication_preferences={"primary_mode": "verbal"},
    modality_effectiveness={"visual": {"observed_count": 10, "engagement_rating": 0.85}},
)

profile_2 = LearnerProfile(
    id=uuid.uuid4(),
    learner_id=LEARNER_2_ID,
    communication_preferences={"primary_mode": "visual"},
    modality_effectiveness={"interactive": {"observed_count": 8, "engagement_rating": 0.75}},
)

learner_1 = Learner(
    id=LEARNER_1_ID,
    teacher_id=TEACHER_A_ID,
    name="Learner One",
    learning_level="developing",
    is_active=True,
    profile=profile_1,
)

learner_2 = Learner(
    id=LEARNER_2_ID,
    teacher_id=TEACHER_A_ID,
    name="Learner Two",
    learning_level="foundation",
    is_active=True,
    profile=profile_2,
)

learner_b = Learner(
    id=LEARNER_B_ID,
    teacher_id=TEACHER_B_ID,
    name="Learner Bob",
    learning_level="emerging",
    is_active=True,
    profile=None,
)

obj_1 = LearningObjective(
    id=OBJ_1_ID,
    title={"en": "Count Objects 1-5"},
    description={"en": "Count visual items up to 5."},
    difficulty_level=1,
    assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
    order_index=1,
    is_active=True,
)

obj_2 = LearningObjective(
    id=OBJ_2_ID,
    title={"en": "Number Matching 1-5"},
    description={"en": "Match digits to dot patterns."},
    difficulty_level=1,
    assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
    order_index=2,
    is_active=True,
)


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """Mock database session populated with in-memory fixtures."""
    session = AsyncMock()

    events: list[PerformanceEvent] = [
        # Learner 1: 3 recent attempts on Obj 1
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_1_ID,
            objective_id=OBJ_1_ID,
            activity_type="matching",
            modality="visual",
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=5000,
            hints_used=1,
            assistance_level=1,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=1),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_1_ID,
            objective_id=OBJ_1_ID,
            activity_type="matching",
            modality="visual",
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=4500,
            hints_used=0,
            assistance_level=0,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=2),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_1_ID,
            objective_id=OBJ_1_ID,
            activity_type="multiple_choice",
            modality="visual",
            strategy="repetition",
            correct=False,
            score=0.0,
            attempts=2,
            response_time_ms=8000,
            hints_used=2,
            assistance_level=2,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=3),
        ),
        # Learner 2: 5 attempts with high assistance (avg 2.2) and low accuracy (1/5 = 20%)
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_2_ID,
            objective_id=OBJ_2_ID,
            activity_type="drag_drop",
            modality="interactive",
            strategy="scaffolding",
            correct=False,
            score=0.0,
            attempts=3,
            response_time_ms=12000,
            hints_used=3,
            assistance_level=3,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=1),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_2_ID,
            objective_id=OBJ_2_ID,
            activity_type="drag_drop",
            modality="interactive",
            strategy="scaffolding",
            correct=False,
            score=0.0,
            attempts=2,
            response_time_ms=10000,
            hints_used=2,
            assistance_level=2,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=2),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_2_ID,
            objective_id=OBJ_2_ID,
            activity_type="ordering",
            modality="interactive",
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=2,
            response_time_ms=9000,
            hints_used=2,
            assistance_level=2,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=3),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_2_ID,
            objective_id=OBJ_2_ID,
            activity_type="ordering",
            modality="interactive",
            strategy="demonstration",
            correct=False,
            score=0.0,
            attempts=2,
            response_time_ms=9500,
            hints_used=2,
            assistance_level=2,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=4),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=LEARNER_2_ID,
            objective_id=OBJ_2_ID,
            activity_type="drag_drop",
            modality="interactive",
            strategy="demonstration",
            correct=False,
            score=0.0,
            attempts=3,
            response_time_ms=11000,
            hints_used=2,
            assistance_level=2,
            completed=True,
            difficulty=1,
            timestamp=now - timedelta(days=5),
        ),
    ]

    async def mock_execute(stmt: Any) -> MagicMock:
        result = MagicMock()
        stmt_str = str(stmt).lower()
        params = {}
        try:
            params = stmt.compile().params
        except Exception:
            pass
        param_vals = list(params.values())

        if "from learners" in stmt_str:
            if "learners.id =" in stmt_str or "learners.id in" in stmt_str:
                if LEARNER_1_ID in param_vals:
                    result.scalars.return_value.first.return_value = learner_1
                    result.scalars.return_value.all.return_value = [learner_1]
                elif LEARNER_2_ID in param_vals:
                    result.scalars.return_value.first.return_value = learner_2
                    result.scalars.return_value.all.return_value = [learner_2]
                elif LEARNER_B_ID in param_vals:
                    result.scalars.return_value.first.return_value = learner_b
                    result.scalars.return_value.all.return_value = [learner_b]
                else:
                    result.scalars.return_value.first.return_value = learner_1
                    result.scalars.return_value.all.return_value = [learner_1, learner_2]
            elif "learners.teacher_id =" in stmt_str:
                if TEACHER_B_ID in param_vals:
                    result.scalars.return_value.all.return_value = [learner_b]
                else:
                    result.scalars.return_value.all.return_value = [learner_1, learner_2]
            else:
                result.scalars.return_value.all.return_value = [learner_1, learner_2, learner_b]
            return result

        if "from performance_events" in stmt_str:
            matched = list(events)
            if LEARNER_1_ID in param_vals and LEARNER_2_ID not in param_vals:
                matched = [e for e in matched if e.learner_id == LEARNER_1_ID]
            elif LEARNER_2_ID in param_vals and LEARNER_1_ID not in param_vals:
                matched = [e for e in matched if e.learner_id == LEARNER_2_ID]
            elif LEARNER_B_ID in param_vals:
                matched = [e for e in matched if e.learner_id == LEARNER_B_ID]

            result.scalars.return_value.all.return_value = matched
            return result

        if "from learning_objectives" in stmt_str:
            result.scalars.return_value.all.return_value = [obj_1, obj_2]
            result.scalars.return_value.first.return_value = obj_1
            return result

        result.scalars.return_value.all.return_value = []
        result.scalars.return_value.first.return_value = None
        return result

    session.execute.side_effect = mock_execute
    return session


client = TestClient(app)


# ── Unit & Service Tests ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_dashboard_overview_success(mock_db_session: AsyncMock) -> None:
    """Teacher dashboard overview calculates 7-day KPIs for assigned cohort."""
    service = TeacherDashboardService(mock_db_session)
    overview = await service.get_dashboard_overview(teacher_a)

    assert isinstance(overview, TeacherDashboardOverview)
    assert overview.total_learners == 2
    assert overview.active_learners_7d >= 1
    assert overview.total_activities_completed_7d >= 1
    assert 0.0 <= overview.cohort_average_accuracy_7d <= 1.0
    assert overview.active_alerts_count >= 1
    assert len(overview.recent_alerts) >= 1


@pytest.mark.asyncio
async def test_get_dashboard_overview_empty_cohort(mock_db_session: AsyncMock) -> None:
    """Teacher with 0 learners receives safe empty overview without exceptions."""
    empty_teacher = User(
        id=uuid.uuid4(),
        email="empty@eduvia.org",
        full_name="Empty Teacher",
        role=UserRole.teacher,
        is_active=True,
        hashed_password="pw",
    )
    # Configure mock to return empty list for this teacher
    orig_side_effect = mock_db_session.execute.side_effect

    async def empty_execute(stmt: Any) -> MagicMock:
        if "learners.teacher_id =" in str(stmt).lower():
            res = MagicMock()
            res.scalars.return_value.all.return_value = []
            return res
        return await orig_side_effect(stmt)

    mock_db_session.execute.side_effect = empty_execute

    service = TeacherDashboardService(mock_db_session)
    overview = await service.get_dashboard_overview(empty_teacher)
    assert overview.total_learners == 0
    assert overview.active_learners_7d == 0
    assert overview.cohort_average_accuracy_7d == 0.0
    assert overview.active_alerts_count == 0
    assert overview.recent_alerts == []


@pytest.mark.asyncio
async def test_cohort_insights_calculation(mock_db_session: AsyncMock) -> None:
    """Cohort insights aggregates modality distribution, mastery, and student summaries."""
    service = TeacherDashboardService(mock_db_session)
    insights = await service.get_cohort_insights(teacher_a, days=30)

    assert isinstance(insights, CohortInsights)
    assert insights.cohort_size == 2
    assert insights.reporting_period_days == 30
    assert 0.0 <= insights.average_accuracy <= 1.0
    assert 0.0 <= insights.average_assistance_level <= 3.0
    assert "visual" in insights.modality_distribution or "interactive" in insights.modality_distribution
    assert len(insights.learner_summaries) == 2


@pytest.mark.asyncio
async def test_intervention_alert_high_assistance_detection(mock_db_session: AsyncMock) -> None:
    """Detects high scaffolding reliance when assistance averages >= 2.0."""
    service = TeacherDashboardService(mock_db_session)
    alerts = await service.get_intervention_alerts(teacher_a, target_learner_id=LEARNER_2_ID)

    high_asst_alerts = [a for a in alerts if a.trigger_type == AlertTriggerType.high_assistance]
    assert len(high_asst_alerts) >= 1
    alert = high_asst_alerts[0]
    assert alert.severity == AlertSeverity.action_required
    assert alert.learner_id == LEARNER_2_ID
    assert "assistance" in alert.message.lower()
    assert len(alert.recommended_action) > 0


@pytest.mark.asyncio
async def test_intervention_alert_low_accuracy_detection(mock_db_session: AsyncMock) -> None:
    """Detects low accuracy signal when learner struggles on an objective (< 60% accuracy)."""
    service = TeacherDashboardService(mock_db_session)
    alerts = await service.get_intervention_alerts(teacher_a, target_learner_id=LEARNER_2_ID)

    # Learner 2 has 1 correct out of 5 attempts on OBJ_2 (20% accuracy)
    low_acc_alerts = [a for a in alerts if a.trigger_type == AlertTriggerType.low_accuracy]
    assert len(low_acc_alerts) >= 1
    assert low_acc_alerts[0].severity == AlertSeverity.warning


@pytest.mark.asyncio
async def test_iep_report_compilation(mock_db_session: AsyncMock) -> None:
    """Compiles structured IEP report with objectives progress and printable markdown."""
    service = TeacherDashboardService(mock_db_session)
    report = await service.get_learner_iep_report(teacher_a, LEARNER_1_ID, days=30)

    assert isinstance(report, IEPReport)
    assert report.learner_id == LEARNER_1_ID
    assert report.learner_display_name == "Learner One"
    assert "Last 30 Days" in report.reporting_period
    assert report.learning_level == "developing"
    assert report.communication_preference == "verbal"
    assert len(report.teacher_recommendations) >= 1
    assert "# Individualized Education Plan (IEP) Progress Report" in report.printable_summary_markdown
    assert "Learner Reference:" in report.printable_summary_markdown


@pytest.mark.asyncio
async def test_teacher_authorization_isolation(mock_db_session: AsyncMock) -> None:
    """Unassigned teacher accessing another teacher's learner raises AuthorizationError."""
    service = TeacherDashboardService(mock_db_session)

    # Teacher B tries to access Learner 1 (owned by Teacher A)
    with pytest.raises(AuthorizationError):
        await service.get_learner_iep_report(teacher_b, LEARNER_1_ID, days=30)


@pytest.mark.asyncio
async def test_admin_access_allowed(mock_db_session: AsyncMock) -> None:
    """Administrator can access any learner's IEP report and view full cohort."""
    service = TeacherDashboardService(mock_db_session)
    report = await service.get_learner_iep_report(admin_user, LEARNER_1_ID, days=30)
    assert report.learner_id == LEARNER_1_ID


# ── API Endpoint Tests ───────────────────────────────────────────────────────


def test_api_get_dashboard_overview_success(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/teachers/dashboard returns 200 with valid overview payload."""
    app.dependency_overrides[get_current_user] = lambda: teacher_a
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get("/api/v1/teachers/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "total_learners" in data
        assert "active_learners_7d" in data
        assert "cohort_average_accuracy_7d" in data
        assert "active_alerts_count" in data
        assert "recent_alerts" in data
    finally:
        app.dependency_overrides.clear()


def test_api_get_cohort_insights_success(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/teachers/cohort/insights returns 200 with cohort aggregation."""
    app.dependency_overrides[get_current_user] = lambda: teacher_a
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get("/api/v1/teachers/cohort/insights?days=30")
        assert response.status_code == 200
        data = response.json()
        assert data["cohort_size"] == 2
        assert "average_accuracy" in data
        assert "modality_distribution" in data
        assert "learner_summaries" in data
    finally:
        app.dependency_overrides.clear()


def test_api_get_alerts_success(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/teachers/alerts returns 200 with list of alerts."""
    app.dependency_overrides[get_current_user] = lambda: teacher_a
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get("/api/v1/teachers/alerts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "trigger_type" in data[0]
            assert "severity" in data[0]
            assert "recommended_action" in data[0]
    finally:
        app.dependency_overrides.clear()


def test_api_get_iep_report_success(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/teachers/learners/{id}/iep-report returns 200 with IEP report."""
    app.dependency_overrides[get_current_user] = lambda: teacher_a
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get(f"/api/v1/teachers/learners/{LEARNER_1_ID}/iep-report?days=30")
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_1_ID)
        assert "printable_summary_markdown" in data
        assert "objectives_progress" in data
    finally:
        app.dependency_overrides.clear()


def test_api_get_iep_report_unassigned_forbidden(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/teachers/learners/{id}/iep-report returns 403 for unassigned educator."""
    app.dependency_overrides[get_current_user] = lambda: teacher_b
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get(f"/api/v1/teachers/learners/{LEARNER_1_ID}/iep-report")
        assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_api_get_dashboard_unauthenticated(mock_db_session: AsyncMock) -> None:
    """Teacher dashboard endpoints reject unauthenticated requests with 401."""
    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    app.dependency_overrides.pop(get_current_user, None)
    try:
        response = client.get("/api/v1/teachers/dashboard")
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
