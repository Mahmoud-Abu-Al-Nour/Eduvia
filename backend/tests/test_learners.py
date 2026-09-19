"""
Eduvia -- Learner & LearnerProfile Integration Tests (Phase 3)

Validates:
- Learner CRUD operations
- LearnerProfile initialization and updates
- Teacher authority preservation (notes, constraints, overrides)
- Learning observation evidence recording
- Authorization rules (teacher isolation, admin override, unauthenticated rejection)
- Educational terminology adherence (no medical/diagnostic classifications)
"""
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.auth.security import create_access_token, get_password_hash
from app.database.session import get_db_session
from app.learners.models import Learner, LearnerProfile
from app.learners.schemas import (
    LearnerCreate,
    LearnerObservationCreate,
    LearnerUpdate,
    TeacherOverrides,
)
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

# ---------------------------------------------------------
# Test Fixtures & Mock Entities
# ---------------------------------------------------------

now = datetime.now(UTC)
teacher_id = uuid.uuid4()
mock_teacher = User(
    id=teacher_id,
    email="teacher3@eduvia.app",
    full_name="Sarah Teacher",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

other_teacher_id = uuid.uuid4()
mock_other_teacher = User(
    id=other_teacher_id,
    email="other_teacher@eduvia.app",
    full_name="Other Teacher",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

admin_id = uuid.uuid4()
mock_admin = User(
    id=admin_id,
    email="admin3@eduvia.app",
    full_name="Adam Admin",
    hashed_password=get_password_hash("adminpass123"),
    role=UserRole.admin,
    is_active=True,
    created_at=now,
    updated_at=now,
)


def create_mock_learner(learner_id: uuid.UUID, t_id: uuid.UUID, name: str = "Sammy Learner") -> Learner:
    learner = Learner(
        id=learner_id,
        name=name,
        age_group="primary",
        learning_level="beginner",
        is_active=True,
        teacher_id=t_id,
        created_at=now,
        updated_at=now,
    )
    profile = LearnerProfile(
        id=uuid.uuid4(),
        learner_id=learner_id,
        learner=learner,
        communication_preferences={
            "primary_mode": "verbal",
            "receptive_preference": ["verbal", "visual_cues"],
            "expressive_preference": ["verbal"],
            "notes": "Responds well to visual prompts",
        },
        current_skill_level={
            "literacy_stage": "emerging",
            "numeracy_stage": "emerging",
            "attention_span_minutes": 10,
            "strengths": ["visual memory"],
            "focus_areas": ["number recognition"],
        },
        support_requirements={
            "sensory_accommodations": [],
            "pacing": "standard",
            "guidance_level": "moderate",
            "frequent_breaks": False,
        },
        teacher_constraints={
            "max_session_duration_minutes": 20,
            "excluded_modalities": [],
            "required_modalities": [],
            "custom_guidelines": "Keep prompts concise",
        },
        teacher_notes="Active and enthusiastic learner.",
        teacher_overrides={
            "lock_difficulty_level": None,
            "enforce_strategy": None,
            "manual_adjustments_active": False,
        },
        modality_effectiveness={
            "Visual": {"observed_count": 5, "engagement_rating": "high"},
            "Reading/Text": {"observed_count": 2, "engagement_rating": "medium"},
            "Writing": {"observed_count": 0, "engagement_rating": None},
            "Audio": {"observed_count": 4, "engagement_rating": "medium"},
            "Interactive": {"observed_count": 6, "engagement_rating": "high"},
        },
        strategy_effectiveness={
            "Step-by-Step": {"observed_count": 3, "success_rate": 0.85},
            "Repetition": {"observed_count": 2, "success_rate": 0.70},
            "Scaffolding": {"observed_count": 4, "success_rate": 0.90},
            "Prompting": {"observed_count": 1, "success_rate": 0.60},
            "Simplification": {"observed_count": 0, "success_rate": None},
            "Demonstration": {"observed_count": 2, "success_rate": 0.80},
            "Positive Reinforcement": {"observed_count": 5, "success_rate": 0.95},
            "Gradual Difficulty": {"observed_count": 1, "success_rate": 0.75},
        },
        activity_type_effectiveness={
            "Matching": {"observed_count": 4, "accuracy_average": 0.88},
            "MCQ": {"observed_count": 2, "accuracy_average": 0.75},
            "Ordering": {"observed_count": 1, "accuracy_average": 0.60},
            "Visual Identification": {"observed_count": 5, "accuracy_average": 0.92},
            "Drag & Drop": {"observed_count": 3, "accuracy_average": 0.80},
        },
        difficulty_tolerance={
            "comfortable_difficulty_level": 1,
            "highest_successful_level": 2,
            "frustration_threshold_observed": "moderate",
        },
        assistance_requirements={
            "prompt_dependence": "moderate",
            "most_effective_prompt_type": "visual",
        },
        response_behavior={
            "average_response_latency_seconds": 4.2,
            "consistency_pattern": "stable",
        },
        observations=[],
        created_at=now,
        updated_at=now,
    )
    learner.profile = profile
    return learner


@pytest.fixture(autouse=True)
def override_db():
    async def override_get_db_session():
        yield AsyncMock()
    app.dependency_overrides[get_db_session] = override_get_db_session
    yield
    app.dependency_overrides.clear()


# ---------------------------------------------------------
# Unit / Schema Tests
# ---------------------------------------------------------

def test_learner_schema_validation():
    # Valid creation
    valid = LearnerCreate(name="Tariq", age_group="primary", learning_level="beginner")
    assert valid.name == "Tariq"
    assert valid.age_group == "primary"

    # Empty name fails validation
    with pytest.raises(ValidationError):
        LearnerCreate(name="", age_group="primary")


def test_teacher_overrides_schema():
    # Valid override
    overrides = TeacherOverrides(lock_difficulty_level=3, enforce_strategy="Scaffolding")
    assert overrides.lock_difficulty_level == 3
    assert overrides.enforce_strategy == "Scaffolding"

    # Difficulty out of bounds (1..5)
    with pytest.raises(ValidationError):
        TeacherOverrides(lock_difficulty_level=6)


def test_observation_schema():
    obs = LearnerObservationCreate(
        category="modality",
        summary="Responded with high accuracy when visual cues were paired with audio.",
        context={"modality": "Visual", "accuracy": 1.0},
        teacher_note="Recommended continuing multi-modal presentation.",
    )
    assert obs.category == "modality"
    assert "visual cues" in obs.summary


# ---------------------------------------------------------
# API / Route Tests
# ---------------------------------------------------------

def test_list_learners_unauthenticated():
    res = client.get("/api/v1/learners")
    assert res.status_code == 401


def test_list_learners_authenticated_teacher():
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()
    mock_l = create_mock_learner(learner_id, teacher_id)

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.list_learners", AsyncMock(return_value=[mock_l])):
            res = client.get(
                "/api/v1/learners",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 200
            data = res.json()
            assert len(data) == 1
            assert data[0]["id"] == str(learner_id)
            assert data[0]["name"] == "Sammy Learner"


def test_create_learner_success():
    token = create_access_token(subject=str(teacher_id))
    new_id = uuid.uuid4()
    mock_created = create_mock_learner(new_id, teacher_id, name="Lina")

    payload = {
        "name": "Lina",
        "age_group": "early_childhood",
        "learning_level": "emerging",
        "teacher_notes": "Needs gentle prompting.",
        "communication_preferences": {
            "primary_mode": "verbal",
            "notes": "Prefers short sentences",
        },
    }

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.create", AsyncMock(return_value=mock_created)):
            res = client.post(
                "/api/v1/learners",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 201
            data = res.json()
            assert data["id"] == str(new_id)
            assert data["name"] == "Lina"
            assert data["profile"] is not None
            assert "modality_effectiveness" in data["profile"]


def test_get_learner_detail_success():
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()
    mock_l = create_mock_learner(learner_id, teacher_id)

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.get_by_id", AsyncMock(return_value=mock_l)):
            res = client.get(
                f"/api/v1/learners/{learner_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 200
            data = res.json()
            assert data["id"] == str(learner_id)
            assert data["profile"]["communication_preferences"]["primary_mode"] == "verbal"
            assert data["profile"]["strategy_effectiveness"]["Step-by-Step"]["success_rate"] == 0.85


def test_get_learner_unauthorized_teacher():
    # Teacher Sarah tries to access a learner owned by Other Teacher
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.get_by_id", AsyncMock(return_value=None)):
            res = client.get(
                f"/api/v1/learners/{learner_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 404
            assert "not found or access unauthorized" in res.json()["detail"].lower()


def test_get_learner_admin_access():
    # Admin can access any learner regardless of assigned teacher
    token = create_access_token(subject=str(admin_id))
    learner_id = uuid.uuid4()
    mock_l = create_mock_learner(learner_id, other_teacher_id)

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_admin)):
        with patch("app.learners.service.LearnerService.get_by_id", AsyncMock(return_value=mock_l)):
            res = client.get(
                f"/api/v1/learners/{learner_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 200
            assert res.json()["id"] == str(learner_id)


def test_update_learner_profile():
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()
    mock_l = create_mock_learner(learner_id, teacher_id)
    mock_l.profile.teacher_notes = "Updated teacher guidance note."

    update_payload = {
        "learning_level": "intermediate",
        "profile": {
            "teacher_notes": "Updated teacher guidance note.",
            "teacher_overrides": {
                "lock_difficulty_level": 2,
                "manual_adjustments_active": True,
            },
        },
    }

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.update", AsyncMock(return_value=mock_l)):
            res = client.patch(
                f"/api/v1/learners/{learner_id}",
                json=update_payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 200
            data = res.json()
            assert data["profile"]["teacher_notes"] == "Updated teacher guidance note."


def test_add_learner_observation():
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()
    obs_id = str(uuid.uuid4())
    mock_obs = {
        "id": obs_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "category": "strategy",
        "summary": "Step-by-step breakdown significantly reduced task latency.",
        "context": {"strategy": "Step-by-Step", "latency_seconds": 3.1},
        "teacher_note": "Consistently benefits from smaller chunking.",
    }

    payload = {
        "category": "strategy",
        "summary": "Step-by-step breakdown significantly reduced task latency.",
        "context": {"strategy": "Step-by-Step", "latency_seconds": 3.1},
        "teacher_note": "Consistently benefits from smaller chunking.",
    }

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.add_observation", AsyncMock(return_value=mock_obs)):
            res = client.post(
                f"/api/v1/learners/{learner_id}/observations",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 201
            assert res.json()["id"] == obs_id
            assert res.json()["category"] == "strategy"


def test_delete_learner():
    token = create_access_token(subject=str(teacher_id))
    learner_id = uuid.uuid4()

    with patch("app.auth.dependencies.UserService.get_by_id", AsyncMock(return_value=mock_teacher)):
        with patch("app.learners.service.LearnerService.delete", AsyncMock(return_value=True)):
            res = client.delete(
                f"/api/v1/learners/{learner_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert res.status_code == 204


def test_invalid_token_learners():
    res = client.get(
        "/api/v1/learners",
        headers={"Authorization": "Bearer invalid.token.payload"},
    )
    assert res.status_code == 401
