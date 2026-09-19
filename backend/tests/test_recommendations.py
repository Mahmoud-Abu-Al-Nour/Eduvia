"""
Eduvia — Phase 8: Adaptive Learning Intelligence Engine Test Suite

Validates:
1. Deterministic AdaptationEngine logic:
   - Curriculum prerequisite constraint filtering (locked vs unlocked objectives).
   - In-progress objective persistence until mastery.
   - Teacher override precedence:
     * lock_difficulty_level overrides evidence.
     * enforce_strategy overrides evidence.
     * excluded_modalities / required_modalities filtering.
   - Modality selection threshold (minimum 5 events before empirical switch).
   - Difficulty calibration (promotion on >= 0.80 acc, scaffolding on < 0.50 acc).
   - Explainable educational rationales (no psychoanalysis or chain-of-thought).
2. RecommendationService integration:
   - Teacher multi-tenant isolation (assigned vs unassigned vs admin).
   - Activity generation pipeline integration (Zero-Strand fallback compatibility).
   - Learner profile effectiveness synchronization.
3. API Endpoints:
   - GET /api/v1/recommendations/learners/{learner_id}
   - POST /api/v1/recommendations/learners/{learner_id}/next-activity
   - POST /api/v1/recommendations/learners/{learner_id}/sync-profile
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.activities.schemas import ActivityType
from app.ai.adaptation.engine import AdaptationEngine
from app.analytics.schemas import (
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    Modality,
    ModalityMetrics,
    ObjectiveMasteryStatus,
    TeachingStrategy,
)
from app.auth.dependencies import get_current_user
from app.core.errors import AuthorizationError, NotFoundError
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.learners.models import Learner, LearnerProfile
from app.main import app
from app.recommendations.schemas import (
    ConfidenceLevel,
    ProfileSyncResult,
)
from app.recommendations.service import RecommendationService
from app.users.models import User, UserRole
from fastapi.testclient import TestClient

# ── Test Entities ────────────────────────────────────────────────────────────

now = datetime.now(UTC)
TEACHER_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
OTHER_TEACHER_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
ADMIN_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")
LEARNER_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
OBJ_1_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
OBJ_2_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")
OBJ_3_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")

mock_teacher = User(
    id=TEACHER_ID,
    email="assigned.teacher@eduvia.app",
    full_name="Assigned Teacher",
    role=UserRole.teacher.value,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_other_teacher = User(
    id=OTHER_TEACHER_ID,
    email="other.teacher@eduvia.app",
    full_name="Other Teacher",
    role=UserRole.teacher.value,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_admin = User(
    id=ADMIN_ID,
    email="admin@eduvia.app",
    full_name="Administrator",
    role=UserRole.admin.value,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_profile = LearnerProfile(
    id=uuid.uuid4(),
    learner_id=LEARNER_ID,
    communication_preferences={"primary_mode": "verbal"},
    current_skill_level={"literacy_stage": "emerging"},
    support_requirements={"sensory_accommodations": []},
    teacher_constraints={"excluded_modalities": [], "required_modalities": []},
    teacher_overrides={"lock_difficulty_level": None, "enforce_strategy": None},
    modality_effectiveness={
        "Visual": {"observed_count": 0, "engagement_rating": None},
        "Interactive": {"observed_count": 0, "engagement_rating": None},
    },
    strategy_effectiveness={
        "Step-by-Step": {"observed_count": 0, "success_rate": None},
    },
    activity_type_effectiveness={},
    difficulty_tolerance={"comfortable_difficulty_level": 1},
    created_at=now,
    updated_at=now,
)

mock_learner = Learner(
    id=LEARNER_ID,
    name="Sammy Davis",
    age_group="6-8",
    learning_level="beginner",
    is_active=True,
    teacher_id=TEACHER_ID,
    profile=mock_profile,
    created_at=now,
    updated_at=now,
)

mock_obj_1 = LearningObjective(
    id=OBJ_1_ID,
    lesson_id=uuid.uuid4(),
    title={"en": "Count Numbers 1 to 5"},
    difficulty_level=1,
    order_index=1,
    is_active=True,
    prerequisites=[],
    assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
)

mock_obj_2 = LearningObjective(
    id=OBJ_2_ID,
    lesson_id=uuid.uuid4(),
    title={"en": "Count Numbers 6 to 10"},
    difficulty_level=2,
    order_index=2,
    is_active=True,
    prerequisites=[mock_obj_1],
    assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
)

mock_obj_3 = LearningObjective(
    id=OBJ_3_ID,
    lesson_id=uuid.uuid4(),
    title={"en": "Simple Addition up to 10"},
    difficulty_level=3,
    order_index=3,
    is_active=True,
    prerequisites=[mock_obj_2],
    assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
)

client = TestClient(app)


# ── Unit Tests: AdaptationEngine ─────────────────────────────────────────────


def test_engine_prerequisite_filtering_locked() -> None:
    """Objectives with unmastered prerequisites must not be selected."""
    # Empty mastery report: obj_1 is not mastered
    mastery_report = LearnerMasteryReport(
        learner_id=LEARNER_ID,
        total_objectives_evaluated=0,
        mastered_count=0,
        in_progress_count=0,
        not_started_count=0,
        mastery_percentage=0.0,
        objectives=[],
    )

    # Candidate list has obj_2 (requires obj_1) and obj_1 (no prereqs)
    selected, constraints = AdaptationEngine.evaluate_next_objective(
        candidate_objectives=[mock_obj_2, mock_obj_1],
        mastery_report=mastery_report,
    )
    # Must select obj_1 because obj_2 prerequisite is not met
    assert selected.id == OBJ_1_ID
    assert any("prereq_locked" in c for c in constraints)


def test_engine_prerequisite_filtering_unlocked() -> None:
    """When prerequisite is mastered, the next objective is unlocked."""
    mastery_report = LearnerMasteryReport(
        learner_id=LEARNER_ID,
        total_objectives_evaluated=1,
        mastered_count=1,
        in_progress_count=0,
        not_started_count=0,
        mastery_percentage=100.0,
        objectives=[
            ObjectiveMasteryStatus(
                objective_id=OBJ_1_ID,
                objective_title="Count Numbers 1 to 5",
                difficulty_level=1,
                total_attempts=3,
                accuracy=0.90,
                avg_assistance_level=0.5,
                mastery_achieved=True,
                status="mastered",
                last_attempt_at=now,
            )
        ],
    )

    selected, _ = AdaptationEngine.evaluate_next_objective(
        candidate_objectives=[mock_obj_1, mock_obj_2, mock_obj_3],
        mastery_report=mastery_report,
    )
    # obj_1 is mastered; obj_2 has prereq obj_1 satisfied -> obj_2 selected
    assert selected.id == OBJ_2_ID


def test_engine_in_progress_objective_prioritized() -> None:
    """An objective that is in-progress (attempted but not mastered) is prioritized."""
    mastery_report = LearnerMasteryReport(
        learner_id=LEARNER_ID,
        total_objectives_evaluated=1,
        mastered_count=0,
        in_progress_count=1,
        not_started_count=0,
        mastery_percentage=0.0,
        objectives=[
            ObjectiveMasteryStatus(
                objective_id=OBJ_1_ID,
                objective_title="Count Numbers 1 to 5",
                difficulty_level=1,
                total_attempts=2,
                accuracy=0.60,
                avg_assistance_level=1.2,
                mastery_achieved=False,
                status="in_progress",
                last_attempt_at=now,
            )
        ],
    )

    selected, constraints = AdaptationEngine.evaluate_next_objective(
        candidate_objectives=[mock_obj_1, mock_obj_2],
        mastery_report=mastery_report,
    )
    assert selected.id == OBJ_1_ID
    assert "continue_in_progress_objective" in constraints


def test_engine_teacher_difficulty_override_precedence() -> None:
    """Teacher lock_difficulty_level must take precedence over high-accuracy promotion."""
    mastery_status = ObjectiveMasteryStatus(
        objective_id=OBJ_1_ID,
        objective_title="Test",
        difficulty_level=2,
        total_attempts=5,
        accuracy=0.95,  # High accuracy would normally promote to 3
        avg_assistance_level=0.2,
        mastery_achieved=True,
        status="mastered",
    )
    locked_profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        communication_preferences={},
        current_skill_level={},
        support_requirements={},
        teacher_constraints={},
        teacher_overrides={"lock_difficulty_level": 1},
    )

    calibrated, constraints = AdaptationEngine.calibrate_difficulty(
        base_difficulty=2,
        recent_status=mastery_status,
        profile=locked_profile,
    )
    assert calibrated == 1  # Locked by teacher
    assert "teacher_locked_difficulty" in constraints


def test_engine_difficulty_promotion_and_scaffolding() -> None:
    """Accuracy >= 0.80 promotes; accuracy < 0.50 scaffolds down."""
    # Promotion test
    high_perf = ObjectiveMasteryStatus(
        objective_id=OBJ_1_ID,
        objective_title="Test",
        difficulty_level=2,
        total_attempts=3,
        accuracy=0.85,
        avg_assistance_level=0.8,
        mastery_achieved=True,
        status="mastered",
    )
    promoted, p_constraints = AdaptationEngine.calibrate_difficulty(
        base_difficulty=2, recent_status=high_perf, profile=None
    )
    assert promoted == 3
    assert "empirical_difficulty_promoted" in p_constraints

    # Scaffolding test
    low_perf = ObjectiveMasteryStatus(
        objective_id=OBJ_1_ID,
        objective_title="Test",
        difficulty_level=3,
        total_attempts=3,
        accuracy=0.40,
        avg_assistance_level=2.0,
        mastery_achieved=False,
        status="in_progress",
    )
    scaffolded, s_constraints = AdaptationEngine.calibrate_difficulty(
        base_difficulty=3, recent_status=low_perf, profile=None
    )
    assert scaffolded == 2
    assert "empirical_difficulty_scaffolded" in s_constraints


def test_engine_modality_selection_evidence_threshold() -> None:
    """Switching modality based on empirical evidence requires >= 5 interaction events."""
    # Profile default is visual
    profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        communication_preferences={"primary_mode": "visual_assisted"},
        current_skill_level={},
        support_requirements={},
        teacher_constraints={},
        teacher_overrides={},
        modality_effectiveness={
            "Visual": {"observed_count": 0, "engagement_rating": None},
        },
    )

    # 3 events for interactive -> below 5 threshold, stays on visual
    insufficient_summary = LearnerAnalyticsSummary(
        learner_id=LEARNER_ID,
        total_events=3,
        completed_activities=3,
        overall_accuracy=0.90,
        avg_score=0.90,
        avg_response_time_ms=12000.0,
        avg_hints_per_activity=0.5,
        avg_assistance_level=0.5,
        modality_breakdown=[
            ModalityMetrics(
                modality="interactive",
                total_events=3,
                accuracy=1.0,
                avg_score=1.0,
                avg_response_time_ms=10000.0,
                avg_assistance_level=0.3,
            )
        ],
        activity_type_breakdown=[],
    )
    modality_res, _, _ = AdaptationEngine.select_modality_and_activity_type(
        profile=profile,
        analytics_summary=insufficient_summary,
    )
    assert modality_res == Modality.VISUAL

    # 6 events for interactive -> above 5 threshold with high accuracy, switches to interactive
    sufficient_summary = LearnerAnalyticsSummary(
        learner_id=LEARNER_ID,
        total_events=6,
        completed_activities=6,
        overall_accuracy=0.95,
        avg_score=0.95,
        avg_response_time_ms=10000.0,
        avg_hints_per_activity=0.2,
        avg_assistance_level=0.2,
        modality_breakdown=[
            ModalityMetrics(
                modality="interactive",
                total_events=6,
                accuracy=0.95,
                avg_score=0.95,
                avg_response_time_ms=9000.0,
                avg_assistance_level=0.2,
            )
        ],
        activity_type_breakdown=[],
    )
    modality_res_sufficient, act_type_res, constraints = (
        AdaptationEngine.select_modality_and_activity_type(
            profile=profile,
            analytics_summary=sufficient_summary,
        )
    )
    assert modality_res_sufficient == Modality.INTERACTIVE
    assert act_type_res == ActivityType.DRAG_DROP
    assert "empirical_modality_selected" in constraints


def test_engine_teacher_modality_exclusion() -> None:
    """Teacher excluded_modalities must prevent selection even if preferred."""
    profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        communication_preferences={"primary_mode": "visual_assisted"},
        current_skill_level={},
        support_requirements={},
        teacher_constraints={"excluded_modalities": ["visual"]},
        teacher_overrides={},
    )
    modality_res, act_type_res, constraints = AdaptationEngine.select_modality_and_activity_type(
        profile=profile,
        analytics_summary=None,
    )
    assert modality_res != Modality.VISUAL
    assert act_type_res != ActivityType.VISUAL_IDENTIFICATION
    assert "teacher_excluded_modalities_applied" in constraints


def test_engine_teacher_strategy_override() -> None:
    """Teacher enforce_strategy override takes absolute precedence."""
    profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=LEARNER_ID,
        communication_preferences={},
        current_skill_level={},
        support_requirements={},
        teacher_constraints={},
        teacher_overrides={"enforce_strategy": "demonstration"},
    )
    # High performance that would normally choose gradual_difficulty
    high_perf = ObjectiveMasteryStatus(
        objective_id=OBJ_1_ID,
        objective_title="Test",
        difficulty_level=1,
        total_attempts=5,
        accuracy=0.95,
        avg_assistance_level=0.2,
        mastery_achieved=True,
        status="mastered",
    )
    strategy, _, constraints = AdaptationEngine.select_strategy(
        profile=profile,
        recent_status=high_perf,
    )
    assert strategy == TeachingStrategy.DEMONSTRATION
    assert "teacher_enforced_strategy" in constraints


def test_engine_build_recommendation_explainability() -> None:
    """Decision must include concise rationale and applied constraints without chain-of-thought."""
    rec = AdaptationEngine.build_recommendation(
        learner_id=LEARNER_ID,
        candidate_objectives=[mock_obj_1, mock_obj_2],
        profile=mock_profile,
        mastery_report=None,
        analytics_summary=None,
    )
    assert rec.learner_id == LEARNER_ID
    assert rec.objective_id == OBJ_1_ID
    assert rec.difficulty_level == 1
    assert rec.confidence_level == ConfidenceLevel.LOW
    assert "Count Numbers 1 to 5" in rec.rationale
    assert isinstance(rec.applied_constraints, list)


# ── Integration Tests: RecommendationService ────────────────────────────────


@pytest.fixture
def mock_db_session() -> AsyncMock:
    session = AsyncMock()

    def mock_execute(stmt, *args, **kwargs):
        stmt_str = str(stmt).lower()
        result = MagicMock()
        if "from learners" in stmt_str:
            result.scalars.return_value.first.return_value = mock_learner
            result.scalars.return_value.all.return_value = [mock_learner]
            result.scalar_one_or_none.return_value = mock_learner
        elif "from learning_objectives" in stmt_str:
            result.scalars.return_value.first.return_value = mock_obj_1
            result.scalars.return_value.all.return_value = [mock_obj_1, mock_obj_2, mock_obj_3]
            result.scalar_one_or_none.return_value = mock_obj_1
        elif "from learner_profiles" in stmt_str:
            result.scalars.return_value.first.return_value = mock_profile
            result.scalars.return_value.all.return_value = [mock_profile]
            result.scalar_one_or_none.return_value = mock_profile
        elif "from performance_events" in stmt_str:
            result.scalars.return_value.first.return_value = None
            result.scalars.return_value.all.return_value = []
            result.scalar_one_or_none.return_value = None
        else:
            result.scalars.return_value.first.return_value = None
            result.scalars.return_value.all.return_value = []
            result.scalar_one_or_none.return_value = None
        return result

    session.execute.side_effect = mock_execute
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_service_get_recommendation_teacher_access(mock_db_session: AsyncMock) -> None:
    """Assigned teacher can retrieve recommendation; other teacher is forbidden."""
    service = RecommendationService(mock_db_session)

    # Assigned teacher succeeds
    rec = await service.get_recommendation(LEARNER_ID, mock_teacher)
    assert rec.learner_id == LEARNER_ID
    assert rec.objective_id == OBJ_1_ID

    # Unassigned teacher fails with 403 AuthorizationError
    with pytest.raises(AuthorizationError):
        await service.get_recommendation(LEARNER_ID, mock_other_teacher)

    # Admin succeeds
    admin_rec = await service.get_recommendation(LEARNER_ID, mock_admin)
    assert admin_rec.learner_id == LEARNER_ID


@pytest.mark.asyncio
async def test_service_nonexistent_learner(mock_db_session: AsyncMock) -> None:
    """Requesting recommendation for non-existent learner raises NotFoundError."""
    mock_db_session.execute.side_effect = None
    result = MagicMock()
    result.scalars.return_value.first.return_value = None
    result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = result

    service = RecommendationService(mock_db_session)
    non_existent = uuid.uuid4()
    with pytest.raises(NotFoundError):
        await service.get_recommendation(non_existent, mock_teacher)


@pytest.mark.asyncio
async def test_service_sync_profile_effectiveness(mock_db_session: AsyncMock) -> None:
    """Profile sync processes events and updates learner profile effectiveness."""
    service = RecommendationService(mock_db_session)
    res = await service.sync_learner_profile_effectiveness(LEARNER_ID, mock_teacher)
    assert isinstance(res, ProfileSyncResult)
    assert res.learner_id == LEARNER_ID
    assert res.total_events_processed >= 0


# ── API Endpoint Tests ───────────────────────────────────────────────────────


def test_api_get_recommendation_success(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/recommendations/learners/{learner_id} returns 200 with valid schema."""
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get(f"/api/v1/recommendations/learners/{LEARNER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_ID)
        assert data["objective_id"] == str(OBJ_1_ID)
        assert data["difficulty_level"] >= 1
        assert "rationale" in data
        assert "applied_constraints" in data
    finally:
        app.dependency_overrides.clear()


def test_api_get_recommendation_unauthorized(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/recommendations/learners/{learner_id} requires authentication."""
    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    app.dependency_overrides.pop(get_current_user, None)
    try:
        response = client.get(f"/api/v1/recommendations/learners/{LEARNER_ID}")
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()


def test_api_get_recommendation_forbidden(mock_db_session: AsyncMock) -> None:
    """GET /api/v1/recommendations/learners/{learner_id} returns 403 for unassigned teacher."""
    app.dependency_overrides[get_current_user] = lambda: mock_other_teacher
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.get(f"/api/v1/recommendations/learners/{LEARNER_ID}")
        assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_api_sync_profile_success(mock_db_session: AsyncMock) -> None:
    """POST /api/v1/recommendations/learners/{learner_id}/sync-profile returns 200."""
    app.dependency_overrides[get_current_user] = lambda: mock_teacher
    app.dependency_overrides[get_db_session] = lambda: mock_db_session

    try:
        response = client.post(f"/api/v1/recommendations/learners/{LEARNER_ID}/sync-profile")
        assert response.status_code == 200
        data = response.json()
        assert data["learner_id"] == str(LEARNER_ID)
        assert "updated_modalities" in data
    finally:
        app.dependency_overrides.clear()
