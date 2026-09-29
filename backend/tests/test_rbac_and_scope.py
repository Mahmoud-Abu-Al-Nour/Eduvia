"""
Eduvia — RBAC, Scope Resolution, and IDOR Protection Test Suite

Comprehensive automated verification for:
1. Role-Based Access Control matrix (Admin vs Teacher vs Learner).
2. Resource scope and isolation (Teacher A vs Teacher B).
3. Learner self-scope isolation and teacher private notes redaction.
4. IDOR defense on /learners/{id}, /users/{id}, /instructional-content/{id}, /teachers/dashboard.
5. Privilege escalation defenses (self-promotion, admin creation).
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from app.auth.dependencies import get_current_user, get_current_user_optional
from app.auth.permissions import (
    Permission,
    ROLE_PERMISSIONS,
    check_resource_scope,
    get_user_role,
    has_permission,
)
from app.core.errors import AuthorizationError, NotFoundError
from app.database.session import get_db_session
from app.instructional.schemas import (
    ExplanationMethod,
    InstructionalContentRead,
    InstructionalStatus,
)
from app.instructional.service import InstructionalService
from app.learners.models import Learner, LearnerProfile
from app.learners.service import LearnerService
from app.main import app
from app.users.models import User, UserRole
from app.users.service import UserService

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_dependencies():
    """Ensure database session is mocked for API tests so engine initialization is bypassed."""
    mock_session = AsyncMock()
    app.dependency_overrides[get_db_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


# ── Fixture UUIDs ────────────────────────────────────────────────────────────
ADMIN_ID = uuid.uuid4()
TEACHER_A_ID = uuid.uuid4()
TEACHER_B_ID = uuid.uuid4()
LEARNER_USER_1_ID = uuid.uuid4()
LEARNER_USER_2_ID = uuid.uuid4()

LEARNER_1_ID = uuid.uuid4()
LEARNER_2_ID = uuid.uuid4()
PROFILE_1_ID = uuid.uuid4()
PROFILE_2_ID = uuid.uuid4()

# ── Domain Mock Entities ─────────────────────────────────────────────────────
admin_user = User(
    id=ADMIN_ID,
    email="admin@eduvia.app",
    full_name="Platform Admin",
    role=UserRole.admin,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)

teacher_a = User(
    id=TEACHER_A_ID,
    email="teacher_a@eduvia.app",
    full_name="Teacher A",
    role=UserRole.teacher,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)

teacher_b = User(
    id=TEACHER_B_ID,
    email="teacher_b@eduvia.app",
    full_name="Teacher B",
    role=UserRole.teacher,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)

learner_user_1 = User(
    id=LEARNER_USER_1_ID,
    email="learner1@eduvia.app",
    full_name="Tariq Learner",
    role=UserRole.learner,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)

learner_user_2 = User(
    id=LEARNER_USER_2_ID,
    email="learner2@eduvia.app",
    full_name="Laila Learner",
    role=UserRole.learner,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)

inactive_user = User(
    id=uuid.uuid4(),
    email="inactive@eduvia.app",
    full_name="Inactive User",
    role=UserRole.teacher,
    is_active=False,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)


def make_mock_learner(
    learner_id: uuid.UUID,
    user_id: uuid.UUID,
    teacher_id: uuid.UUID,
    name: str,
    teacher_notes: str | None = None,
    accommodations: list[str] | None = None,
) -> Learner:
    profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=learner_id,
        communication_preferences={
            "primary_mode": "verbal",
            "receptive_preference": ["verbal"],
            "expressive_preference": ["verbal"],
            "notes": "",
        },
        current_skill_level={
            "literacy_stage": "emerging",
            "numeracy_stage": "emerging",
            "attention_span_minutes": 10,
            "strengths": [],
            "focus_areas": [],
        },
        support_requirements={
            "sensory_accommodations": accommodations or ["low_distraction"],
            "pacing": "standard",
            "guidance_level": "moderate",
            "frequent_breaks": False,
        },
        teacher_constraints={
            "max_session_duration_minutes": 20,
            "excluded_modalities": [],
            "required_modalities": [],
            "custom_guidelines": "",
        },
        teacher_notes=teacher_notes,
        teacher_overrides={
            "lock_difficulty_level": None,
            "enforce_strategy": None,
            "manual_adjustments_active": False,
        },
        modality_effectiveness={"visual": {"observed_count": 0, "engagement_rating": None}},
        strategy_effectiveness={"Step-by-Step": {"observed_count": 0, "success_rate": None}},
        activity_type_effectiveness={"Matching": {"observed_count": 0, "accuracy_average": None}},
        difficulty_tolerance={
            "comfortable_difficulty_level": 1,
            "highest_successful_level": 1,
            "frustration_threshold_observed": "moderate",
        },
        assistance_requirements={
            "prompt_dependence": "moderate",
            "most_effective_prompt_type": "visual",
        },
        response_behavior={
            "average_response_latency_seconds": None,
            "consistency_pattern": "stable",
        },
        observations=[],
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    learner = Learner(
        id=learner_id,
        user_id=user_id,
        teacher_id=teacher_id,
        name=name,
        age_group="primary",
        learning_level="beginner",
        is_active=True,
        profile=profile,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    profile.learner = learner
    return learner


learner_1 = make_mock_learner(
    LEARNER_1_ID,
    LEARNER_USER_1_ID,
    TEACHER_A_ID,
    "Tariq Al-Mansoor",
    teacher_notes="Private observations: Tariq requires quiet testing room.",
    accommodations=["low_distraction"],
)

learner_2 = make_mock_learner(
    LEARNER_2_ID,
    LEARNER_USER_2_ID,
    TEACHER_B_ID,
    "Laila Hassan",
    teacher_notes="Private notes: Laila excels with visual diagrams.",
    accommodations=["visual_cues"],
)


# ── 1. Matrix & Policy Unit Tests ───────────────────────────────────────────


def test_permission_matrix_admin_possesses_all() -> None:
    """Admin possesses all permissions."""
    assert has_permission(admin_user, Permission.USERS_READ_GLOBAL)
    assert has_permission(admin_user, Permission.ADMIN_DASHBOARD)
    assert has_permission(admin_user, Permission.TEACHERS_DASHBOARD)
    assert has_permission(admin_user, Permission.ACTIVITIES_GENERATE)
    assert has_permission(admin_user, Permission.CONTENT_GENERATE)


def test_permission_matrix_teacher_restrictions() -> None:
    """Teachers possess educational permissions but cannot access admin global operations."""
    assert has_permission(teacher_a, Permission.TEACHERS_DASHBOARD)
    assert has_permission(teacher_a, Permission.ACTIVITIES_GENERATE)
    assert has_permission(teacher_a, Permission.CONTENT_GENERATE)
    assert has_permission(teacher_a, Permission.LEARNERS_READ_ASSIGNED)

    # Must NOT have administrative capabilities
    assert not has_permission(teacher_a, Permission.USERS_READ_GLOBAL)
    assert not has_permission(teacher_a, Permission.USERS_MANAGE)
    assert not has_permission(teacher_a, Permission.ROLES_MANAGE)
    assert not has_permission(teacher_a, Permission.ADMIN_DASHBOARD)


def test_permission_matrix_learner_restrictions() -> None:
    """Learners possess self-learning permissions but no teacher or admin tools."""
    assert has_permission(learner_user_1, Permission.LEARNERS_READ_SELF)
    assert has_permission(learner_user_1, Permission.ACTIVITIES_READ_SELF)
    assert has_permission(learner_user_1, Permission.PROFILE_READ_SELF)

    # Must NOT have teacher tools or admin powers
    assert not has_permission(learner_user_1, Permission.TEACHERS_DASHBOARD)
    assert not has_permission(learner_user_1, Permission.ACTIVITIES_GENERATE)
    assert not has_permission(learner_user_1, Permission.CONTENT_GENERATE)
    assert not has_permission(learner_user_1, Permission.CONTENT_APPROVE)
    assert not has_permission(learner_user_1, Permission.LEARNERS_CREATE)
    assert not has_permission(learner_user_1, Permission.ADMIN_DASHBOARD)


def test_inactive_user_has_no_permissions() -> None:
    """Inactive users are denied all permissions unconditionally."""
    assert not has_permission(inactive_user, Permission.PROFILE_READ_SELF)
    assert not has_permission(inactive_user, Permission.TEACHERS_DASHBOARD)


def test_resource_scope_resolution() -> None:
    """Validate check_resource_scope for Admin, Teacher, and Learner."""
    # Admin is always authorized
    assert check_resource_scope(admin_user, owner_teacher_id=TEACHER_B_ID)

    # Teacher A authorized for own resource, denied for Teacher B resource
    assert check_resource_scope(teacher_a, owner_teacher_id=TEACHER_A_ID)
    assert not check_resource_scope(teacher_a, owner_teacher_id=TEACHER_B_ID)

    # Learner 1 authorized for own resource, denied for Learner 2
    assert check_resource_scope(learner_user_1, owner_user_id=LEARNER_USER_1_ID)
    assert not check_resource_scope(learner_user_1, owner_user_id=LEARNER_USER_2_ID)


# ── 2. Admin Platform Access & Boundaries ────────────────────────────────────


def test_admin_dashboard_stats_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """Admin can retrieve platform stats (200 OK), non-admin is rejected (403 Forbidden)."""
    app.dependency_overrides[get_current_user] = lambda: admin_user

    async def mock_get_platform_stats(self: UserService) -> dict:
        return {
            "total_users": 15,
            "total_admins": 2,
            "total_teachers": 5,
            "total_learners": 8,
            "total_curricula": 3,
            "total_activities_completed": 42,
        }

    monkeypatch.setattr(UserService, "get_platform_stats", mock_get_platform_stats)

    try:
        # Admin gets 200
        res = client.get("/api/v1/users/platform/stats")
        assert res.status_code == 200
        data = res.json()
        assert data["total_users"] == 15
        assert data["total_activities_completed"] == 42

        # Teacher gets 403
        app.dependency_overrides[get_current_user] = lambda: teacher_a
        res_teacher = client.get("/api/v1/users/platform/stats")
        assert res_teacher.status_code == 403

        # Learner gets 403
        app.dependency_overrides[get_current_user] = lambda: learner_user_1
        res_learner = client.get("/api/v1/users/platform/stats")
        assert res_learner.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_admin_list_users_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """Admin can list all users; Teacher and Learner receive 403 Forbidden."""
    async def mock_get_multi(self: UserService, skip: int = 0, limit: int = 100, role: UserRole | None = None) -> list[User]:
        return [admin_user, teacher_a, learner_user_1]

    monkeypatch.setattr(UserService, "get_multi", mock_get_multi)

    try:
        # Admin gets 200
        app.dependency_overrides[get_current_user] = lambda: admin_user
        res = client.get("/api/v1/users/")
        assert res.status_code == 200
        assert len(res.json()) == 3

        # Teacher gets 403
        app.dependency_overrides[get_current_user] = lambda: teacher_a
        assert client.get("/api/v1/users/").status_code == 403

        # Learner gets 403
        app.dependency_overrides[get_current_user] = lambda: learner_user_1
        assert client.get("/api/v1/users/").status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ── 3. Teacher Scope & IDOR Protection ──────────────────────────────────────


def test_teacher_scope_learner_isolation(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Teacher A cannot access Teacher B's learner profile (returns None/404).
    Teacher A can access Teacher A's assigned learner (returns 200 with teacher_notes intact).
    """
    async def mock_get_by_id(self: LearnerService, learner_id: uuid.UUID, current_user: User | None = None) -> Learner | None:
        if current_user and current_user.role == UserRole.teacher:
            if learner_id == LEARNER_1_ID and current_user.id == TEACHER_A_ID:
                return learner_1
            if learner_id == LEARNER_2_ID and current_user.id == TEACHER_B_ID:
                return learner_2
            return None
        return None

    monkeypatch.setattr(LearnerService, "get_by_id", mock_get_by_id)

    app.dependency_overrides[get_current_user] = lambda: teacher_a

    try:
        # Teacher A accesses assigned Learner 1 -> 200
        res_assigned = client.get(f"/api/v1/learners/{LEARNER_1_ID}")
        assert res_assigned.status_code == 200
        data = res_assigned.json()
        assert data["name"] == "Tariq Al-Mansoor"
        # Teacher notes MUST be visible to the teacher
        assert data["profile"]["teacher_notes"] == "Private observations: Tariq requires quiet testing room."

        # Teacher A accesses unassigned Learner 2 -> 404 (IDOR blocked)
        res_unassigned = client.get(f"/api/v1/learners/{LEARNER_2_ID}")
        assert res_unassigned.status_code == 404
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ── 4. Learner Self-Scope & Teacher Notes Redaction ──────────────────────────


def test_learner_portal_me_redacts_private_notes(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Learner accessing /learners/me receives own profile with teacher private notes redacted to None.
    """
    async def mock_get_by_user_id(self: LearnerService, user_id: uuid.UUID) -> Learner | None:
        if user_id == LEARNER_USER_1_ID:
            return learner_1
        return None

    monkeypatch.setattr(LearnerService, "get_by_user_id", mock_get_by_user_id)

    app.dependency_overrides[get_current_user] = lambda: learner_user_1

    try:
        res = client.get("/api/v1/learners/me")
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "Tariq Al-Mansoor"
        assert data["profile"]["support_requirements"]["sensory_accommodations"] == ["low_distraction"]
        # Teacher notes, constraints, and overrides MUST BE REDACTED for learners
        assert data["profile"]["teacher_notes"] is None
        assert data["profile"]["teacher_constraints"] == {}
        assert data["profile"]["teacher_overrides"] == {}
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_learner_blocked_from_other_learner_idor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Learner 1 attempting to access Learner 2 via /learners/{id} is denied (404)."""
    async def mock_get_by_id(self: LearnerService, learner_id: uuid.UUID, current_user: User | None = None) -> Learner | None:
        if current_user and current_user.role == UserRole.learner:
            # Self-scope only
            if learner_id == LEARNER_1_ID and current_user.id == LEARNER_USER_1_ID:
                return learner_1
            return None
        return None

    monkeypatch.setattr(LearnerService, "get_by_id", mock_get_by_id)

    app.dependency_overrides[get_current_user] = lambda: learner_user_1

    try:
        # Accessing other learner -> 404
        res = client.get(f"/api/v1/learners/{LEARNER_2_ID}")
        assert res.status_code == 404

        # Accessing own learner -> 200 (sanitized)
        res_self = client.get(f"/api/v1/learners/{LEARNER_1_ID}")
        assert res_self.status_code == 200
        assert res_self.json()["profile"]["teacher_notes"] is None
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_learner_cannot_perform_teacher_actions() -> None:
    """Learners cannot create learners, delete learners, or access teacher dashboard."""
    app.dependency_overrides[get_current_user] = lambda: learner_user_1

    try:
        # Cannot access teacher dashboard
        assert client.get("/api/v1/teachers/dashboard").status_code == 403

        # Cannot generate activities
        assert client.post(
            "/api/v1/activities/generate",
            json={"objective_id": str(uuid.uuid4()), "learner_id": str(LEARNER_1_ID)},
        ).status_code == 403

        # Cannot generate instructional content
        assert client.post(
            "/api/v1/instructional-content/generate",
            json={"objective_id": str(uuid.uuid4())},
        ).status_code == 403

        # Cannot delete learners
        assert client.delete(f"/api/v1/learners/{LEARNER_1_ID}").status_code == 403

        # Cannot record observations
        assert client.post(
            f"/api/v1/learners/{LEARNER_1_ID}/observations",
            json={"content": "Observation", "category": "attention"},
        ).status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ── 5. Privilege Escalation & Admin Creation Defenses ───────────────────────


def test_prevent_non_admin_from_creating_admin_user() -> None:
    """Unauthenticated or regular user cannot register an admin account."""
    # Anonymous registration attempt with role='admin' -> 403 Forbidden
    res_anon = client.post(
        "/api/v1/users/",
        json={
            "email": "hacker@eduvia.app",
            "full_name": "Bad Actor",
            "password": "password123",
            "role": "admin",
        },
    )
    assert res_anon.status_code == 403

    # Teacher registration attempt with role='admin' -> 403 Forbidden
    app.dependency_overrides[get_current_user] = lambda: teacher_a
    try:
        res_teacher = client.post(
            "/api/v1/users/",
            json={
                "email": "hacker2@eduvia.app",
                "full_name": "Bad Actor 2",
                "password": "password123",
                "role": "admin",
            },
        )
        assert res_teacher.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ── 6. Instructional Content Visibility & Redaction ─────────────────────────


def test_instructional_content_learner_visibility(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Learner can view published instructional content with teacher_notes redacted.
    Learner receives 404 when accessing draft or review_required instructional content.
    """
    content_id_published = uuid.uuid4()
    content_id_draft = uuid.uuid4()

    published_item = InstructionalContentRead(
        id=content_id_published,
        objective_id=uuid.uuid4(),
        title="Counting Objects",
        explanation_method=ExplanationMethod.STEP_BY_STEP,
        difficulty_level=1,
        language="en",
        blocks=[],
        summary="Learn counting step by step",
        status=InstructionalStatus.PUBLISHED,
        teacher_notes="Confidential pedagogical strategy notes",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    draft_item = InstructionalContentRead(
        id=content_id_draft,
        objective_id=uuid.uuid4(),
        title="Draft Counting",
        explanation_method=ExplanationMethod.STEP_BY_STEP,
        difficulty_level=1,
        language="en",
        blocks=[],
        summary="Draft explanation",
        status=InstructionalStatus.DRAFT,
        teacher_notes="Draft notes",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    async def mock_get_by_id(self: InstructionalService, content_id: uuid.UUID) -> InstructionalContentRead:
        if content_id == content_id_published:
            return published_item.model_copy()
        if content_id == content_id_draft:
            return draft_item.model_copy()
        raise NotFoundError("Content not found")

    monkeypatch.setattr(InstructionalService, "get_by_id", mock_get_by_id)

    # 1. Learner accessing published content -> 200 OK, teacher_notes redacted
    app.dependency_overrides[get_current_user] = lambda: learner_user_1
    app.dependency_overrides[get_current_user_optional] = lambda: learner_user_1
    try:
        res_pub = client.get(f"/api/v1/instructional-content/{content_id_published}")
        assert res_pub.status_code == 200
        assert res_pub.json()["teacher_notes"] is None

        # 2. Learner accessing draft content -> 404 Not Found
        res_draft = client.get(f"/api/v1/instructional-content/{content_id_draft}")
        assert res_draft.status_code == 404

        # 3. Teacher accessing draft content -> 200 OK with teacher_notes intact
        app.dependency_overrides[get_current_user] = lambda: teacher_a
        app.dependency_overrides[get_current_user_optional] = lambda: teacher_a
        res_teacher_draft = client.get(f"/api/v1/instructional-content/{content_id_draft}")
        assert res_teacher_draft.status_code == 200
        assert res_teacher_draft.json()["teacher_notes"] == "Draft notes"
    finally:
        app.dependency_overrides.pop(get_current_user, None)
        app.dependency_overrides.pop(get_current_user_optional, None)
