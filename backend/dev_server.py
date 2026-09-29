"""
Eduvia — Development Live Server with In-Memory Demo Fixtures

Enables live end-to-end UI verification (frontend <-> backend <-> browser)
when running in environments without an active Docker / PostgreSQL daemon.
Provides exact demonstration entities matching seed_demo_data.py.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, patch

import uvicorn

# Ensure backend directory is in sys.path so 'app' can always be resolved
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app.activities.fallbacks import create_fallback_activity, create_fallback_lesson
from app.activities.router import get_activity_service
from app.activities.schemas import (
    Activity,
    ActivityEvaluationResponse,
    ActivityGenerateRequest,
    ActivityGenerateResponse,
    ActivityGenerationSummary,
    ActivitySubmissionRequest,
    ActivityType,
    ActivityUpdateRequest,
    EffectiveGenerationPrompt,
    LessonGenerateResponse,
    LessonPlan,
)
from app.activities.service import ActivityService
from app.ai.generation.prompts import (
    compile_generation_prompt,
    compile_lesson_prompt,
)
from app.ai.providers.base import Message, MessageRole
from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.auth.security import get_password_hash
from app.curriculum.router import get_curriculum_service
from app.database.session import get_db_session
from app.learners.models import Learner, LearnerProfile
from app.learners.router import get_learner_service
from app.learners.schemas import (
    LearnerCreate,
    LearnerObservationCreate,
    LearnerUpdate,
)
from app.main import app
from app.seeds.test_data_definitions import (
    COHORT_B_TEACHER_EMAIL,
    COHORT_B_TEACHER_ID,
    COHORT_B_TEACHER_NAME,
    generate_learner_definitions,
    get_test_uuid,
)
from app.users.models import User, UserRole

now = datetime.now(UTC)
teacher_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
admin_id = uuid.UUID("22222222-2222-2222-2222-222222222222")

demo_teacher = User(
    id=teacher_id,
    email="teacher@eduvia.app",
    full_name="Alice Teacher",
    hashed_password=get_password_hash("strongpassword123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

demo_teacher_b = User(
    id=COHORT_B_TEACHER_ID,
    email=COHORT_B_TEACHER_EMAIL,
    full_name=COHORT_B_TEACHER_NAME,
    hashed_password=get_password_hash("strongpassword123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

demo_admin = User(
    id=admin_id,
    email="admin@eduvia.app",
    full_name="Eduvia Admin",
    hashed_password=get_password_hash("adminpassword123"),
    role=UserRole.admin,
    is_active=True,
    created_at=now,
    updated_at=now,
)

learner_user_id = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
demo_learner_user = User(
    id=learner_user_id,
    email="learner@eduvia.app",
    full_name="Tariq Al-Mansoor",
    hashed_password=get_password_hash("learnerpassword123"),
    role=UserRole.learner,
    is_active=True,
    created_at=now,
    updated_at=now,
)

learner2_user_id = uuid.UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee")
demo_learner2_user = User(
    id=learner2_user_id,
    email="learner2@eduvia.app",
    full_name="Laila Hassan",
    hashed_password=get_password_hash("learnerpassword123"),
    role=UserRole.learner,
    is_active=True,
    created_at=now,
    updated_at=now,
)

researcher_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
demo_researcher = User(
    id=researcher_id,
    email="researcher@eduvia.app",
    full_name="Dr. Elena Vance (Researcher)",
    hashed_password=get_password_hash("researcherpassword123"),
    role=UserRole.researcher,
    is_active=True,
    created_at=now,
    updated_at=now,
)


from app.curriculum.curriculum_catalog import (
    CURRICULUM_DESCRIPTION,
    CURRICULUM_ID,
    CURRICULUM_TITLE,
    CURRICULUM_VERSION,
    FULL_CURRICULUM_CATALOG,
)

# Build full lookup maps from FULL_CURRICULUM_CATALOG
_SUBJECTS_MAP: dict[uuid.UUID, dict[str, Any]] = {s["id"]: s for s in FULL_CURRICULUM_CATALOG}
_UNITS_MAP: dict[uuid.UUID, dict[str, Any]] = {}
_LESSONS_MAP: dict[uuid.UUID, dict[str, Any]] = {}
_OBJECTIVES_MAP: dict[uuid.UUID, dict[str, Any]] = {}

for s in FULL_CURRICULUM_CATALOG:
    for u in s.get("units", []):
        _UNITS_MAP[u["id"]] = u
        for l in u.get("lessons", []):
            _LESSONS_MAP[l["id"]] = l
            for o in l.get("learning_objectives", []):
                _OBJECTIVES_MAP[o["id"]] = o

# Standard IDs matching catalog and legacy tests
curr_id = CURRICULUM_ID
subj_id = uuid.UUID("44444444-4444-4444-4444-444444444444")
unit_id = uuid.UUID("55555555-5555-5555-5555-555555555555")
less_id = uuid.UUID("66666666-6666-6666-6666-666666666666")
obj1_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
obj2_id = uuid.UUID("88888888-8888-8888-8888-888888888888")

curriculum_full_dict: dict[str, Any] = {
    "id": CURRICULUM_ID,
    "title": CURRICULUM_TITLE,
    "description": CURRICULUM_DESCRIPTION,
    "version": CURRICULUM_VERSION,
    "is_active": True,
    "created_by_id": admin_id,
    "subjects": FULL_CURRICULUM_CATALOG,
}

curriculum_summary_dict: dict[str, Any] = {
    "id": CURRICULUM_ID,
    "title": CURRICULUM_TITLE,
    "description": CURRICULUM_DESCRIPTION,
    "version": CURRICULUM_VERSION,
    "is_active": True,
    "created_by_id": admin_id,
}


class MockUserService:
    async def get_by_email(self, email: str) -> User | None:
        if email == "teacher@eduvia.app":
            return demo_teacher
        if email == "admin@eduvia.app":
            return demo_admin
        if email == COHORT_B_TEACHER_EMAIL:
            return demo_teacher_b
        if email == "learner@eduvia.app":
            return demo_learner_user
        if email == "learner2@eduvia.app":
            return demo_learner2_user
        if email == "researcher@eduvia.app":
            return demo_researcher
        return None

    async def get_by_id(self, uid: uuid.UUID) -> User | None:
        if uid == teacher_id:
            return demo_teacher
        if uid == admin_id:
            return demo_admin
        if uid == COHORT_B_TEACHER_ID:
            return demo_teacher_b
        if uid == learner_user_id:
            return demo_learner_user
        if uid == learner2_user_id:
            return demo_learner2_user
        if uid == researcher_id:
            return demo_researcher
        return None

    async def get_multi(self, skip: int = 0, limit: int = 100, role: UserRole | None = None) -> list[User]:
        users = [demo_admin, demo_teacher, demo_teacher_b, demo_learner_user, demo_learner2_user, demo_researcher]
        if role:
            users = [u for u in users if u.role == role]
        return users[skip:skip+limit]

    async def get_platform_stats(self) -> dict[str, int]:
        return {
            "total_users": 6,
            "total_admins": 1,
            "total_teachers": 2,
            "total_learners": 2,
            "total_researchers": 1,
            "total_curricula": 1,
            "total_activities_completed": 15,
        }



class MockCurriculumService:
    async def get_all(self) -> list[dict[str, Any]]:
        return [curriculum_summary_dict]

    async def get_by_id(self, cid: uuid.UUID) -> dict[str, Any] | None:
        if cid == CURRICULUM_ID or cid == curr_id:
            return curriculum_full_dict
        return None

    async def get_subject(self, sid: uuid.UUID) -> dict[str, Any] | None:
        return _SUBJECTS_MAP.get(sid)

    async def get_unit(self, uid: uuid.UUID) -> dict[str, Any] | None:
        return _UNITS_MAP.get(uid)

    async def get_lesson(self, lid: uuid.UUID) -> dict[str, Any] | None:
        return _LESSONS_MAP.get(lid)

    async def get_learning_objective(self, oid: uuid.UUID) -> dict[str, Any] | None:
        return _OBJECTIVES_MAP.get(oid)


# Demo Learner fixture matching seed_demo_data.py
demo_learner_id = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
demo_learner = Learner(
    id=demo_learner_id,
    name="Tariq Al-Mansoor",
    age_group="primary",
    learning_level="beginner",
    is_active=True,
    teacher_id=teacher_id,
    user_id=learner_user_id,
    created_at=now,
    updated_at=now,
)
demo_profile = LearnerProfile(
    id=uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
    learner_id=demo_learner_id,
    learner=demo_learner,
    communication_preferences={
        "primary_mode": "verbal",
        "receptive_preference": ["verbal", "visual_cues"],
        "expressive_preference": ["verbal"],
        "notes": "Responds with high engagement to visual manipulatives and calm pacing.",
    },
    current_skill_level={
        "literacy_stage": "emerging",
        "numeracy_stage": "beginner",
        "attention_span_minutes": 15,
        "strengths": ["visual memory", "enthusiastic learner"],
        "focus_areas": ["number counting", "shape sorting"],
    },
    support_requirements={
        "sensory_accommodations": ["low_distraction_lighting"],
        "pacing": "standard",
        "guidance_level": "moderate",
        "frequent_breaks": True,
    },
    teacher_constraints={
        "max_session_duration_minutes": 20,
        "excluded_modalities": [],
        "required_modalities": ["Visual"],
        "custom_guidelines": "Provide positive feedback after every completed step.",
    },
    teacher_notes="Enjoys math activities and shows steady progress in numeracy.",
    teacher_overrides={
        "lock_difficulty_level": None,
        "enforce_strategy": None,
        "manual_adjustments_active": False,
    },
    modality_effectiveness={
        "Visual": {"observed_count": 8, "engagement_rating": "high"},
        "Reading/Text": {"observed_count": 3, "engagement_rating": "medium"},
        "Writing": {"observed_count": 1, "engagement_rating": "emerging"},
        "Audio": {"observed_count": 6, "engagement_rating": "high"},
        "Interactive": {"observed_count": 9, "engagement_rating": "high"},
    },
    strategy_effectiveness={
        "Step-by-Step": {"observed_count": 6, "success_rate": 0.90},
        "Repetition": {"observed_count": 4, "success_rate": 0.75},
        "Scaffolding": {"observed_count": 5, "success_rate": 0.85},
        "Prompting": {"observed_count": 3, "success_rate": 0.70},
        "Simplification": {"observed_count": 2, "success_rate": 0.80},
        "Demonstration": {"observed_count": 4, "success_rate": 0.88},
        "Positive Reinforcement": {"observed_count": 7, "success_rate": 0.95},
        "Gradual Difficulty": {"observed_count": 3, "success_rate": 0.75},
    },
    activity_type_effectiveness={
        "Matching": {"observed_count": 7, "accuracy_average": 0.92},
        "MCQ": {"observed_count": 3, "accuracy_average": 0.78},
        "Ordering": {"observed_count": 2, "accuracy_average": 0.65},
        "Visual Identification": {"observed_count": 8, "accuracy_average": 0.95},
        "Drag & Drop": {"observed_count": 5, "accuracy_average": 0.84},
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
        "average_response_latency_seconds": 3.8,
        "consistency_pattern": "stable",
    },
    observations=[
        {
            "id": "obs-001",
            "timestamp": now.isoformat(),
            "category": "modality",
            "summary": "High engagement observed during visual matching tasks.",
            "context": {"modality": "Visual"},
            "teacher_note": "Visual cues support independent task completion.",
        }
    ],
    created_at=now,
    updated_at=now,
)
demo_learner.profile = demo_profile

demo_learner_b_id = uuid.UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
demo_learner_b = Learner(
    id=demo_learner_b_id,
    name="Laila Hassan",
    age_group="primary",
    learning_level="beginner",
    is_active=True,
    teacher_id=COHORT_B_TEACHER_ID,
    user_id=learner2_user_id,
    created_at=now,
    updated_at=now,
)
demo_profile_b = LearnerProfile(
    id=uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"),
    learner_id=demo_learner_b_id,
    learner=demo_learner_b,
    communication_preferences={
        "primary_mode": "visual_assisted",
        "receptive_preference": ["visual_cues"],
        "expressive_preference": ["verbal"],
        "notes": "Prefers visual cues.",
    },
    current_skill_level={
        "literacy_stage": "emerging",
        "numeracy_stage": "emerging",
        "attention_span_minutes": 12,
        "strengths": ["visual"],
        "focus_areas": ["phonics"],
    },
    support_requirements={
        "sensory_accommodations": ["high_contrast"],
        "pacing": "standard",
        "guidance_level": "moderate",
        "frequent_breaks": False,
    },
    teacher_constraints={
        "max_session_duration_minutes": 15,
        "excluded_modalities": [],
        "required_modalities": ["Visual"],
        "custom_guidelines": "",
    },
    teacher_notes="Cohort B learner with steady progress.",
    teacher_overrides={},
    created_at=now,
    updated_at=now,
)
demo_learner_b.profile = demo_profile_b

in_memory_learners: dict[uuid.UUID, Learner] = {
    demo_learner_id: demo_learner,
    demo_learner_b_id: demo_learner_b,
}


class MockLearnerService:
    async def list_learners(
        self,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
        current_user: User | None = None,
    ) -> list[Learner]:
        if current_user:
            role_val = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
            if role_val == "admin":
                return list(in_memory_learners.values())
            elif role_val == "teacher":
                return [l for l in in_memory_learners.values() if l.teacher_id == current_user.id]
            elif role_val == "learner":
                return [l for l in in_memory_learners.values() if l.user_id == current_user.id]
            return []
        if is_admin:
            return list(in_memory_learners.values())
        return [learner for learner in in_memory_learners.values() if learner.teacher_id == teacher_id]

    async def get_by_id(
        self,
        learner_id: uuid.UUID,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
        current_user: User | None = None,
    ) -> Learner | None:
        learner = in_memory_learners.get(learner_id)
        if not learner:
            return None
        if current_user:
            role_val = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
            if role_val == "admin":
                return learner
            elif role_val == "teacher":
                if learner.teacher_id != current_user.id:
                    return None
                return learner
            elif role_val == "learner":
                if learner.user_id != current_user.id:
                    return None
                return learner
            return None
        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
            return None
        return learner

    async def get_by_user_id(self, user_id: uuid.UUID) -> Learner | None:
        for l in in_memory_learners.values():
            if l.user_id == user_id:
                return l
        return None

    async def create(self, data: LearnerCreate, teacher_id: uuid.UUID | None) -> Learner:
        new_id = uuid.uuid4()
        learner = Learner(
            id=new_id,
            name=data.name,
            age_group=data.age_group,
            learning_level=data.learning_level,
            teacher_id=teacher_id,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        profile = LearnerProfile(
            id=uuid.uuid4(),
            learner_id=new_id,
            learner=learner,
            communication_preferences=data.communication_preferences or {
                "primary_mode": "verbal",
                "receptive_preference": ["verbal", "visual_cues"],
                "expressive_preference": ["verbal"],
                "notes": "",
            },
            current_skill_level=data.current_skill_level or {
                "literacy_stage": "emerging",
                "numeracy_stage": "emerging",
                "attention_span_minutes": 10,
                "strengths": [],
                "focus_areas": [],
            },
            support_requirements=data.support_requirements or {
                "sensory_accommodations": [],
                "pacing": "standard",
                "guidance_level": "moderate",
                "frequent_breaks": False,
            },
            teacher_constraints=data.teacher_constraints or {
                "max_session_duration_minutes": 20,
                "excluded_modalities": [],
                "required_modalities": [],
                "custom_guidelines": "",
            },
            teacher_notes=data.teacher_notes or "",
            teacher_overrides={
                "lock_difficulty_level": None,
                "enforce_strategy": None,
                "manual_adjustments_active": False,
            },
            modality_effectiveness={
                "Visual": {"observed_count": 0, "engagement_rating": None},
                "Reading/Text": {"observed_count": 0, "engagement_rating": None},
                "Writing": {"observed_count": 0, "engagement_rating": None},
                "Audio": {"observed_count": 0, "engagement_rating": None},
                "Interactive": {"observed_count": 0, "engagement_rating": None},
            },
            strategy_effectiveness={
                "Step-by-Step": {"observed_count": 0, "success_rate": None},
                "Repetition": {"observed_count": 0, "success_rate": None},
                "Scaffolding": {"observed_count": 0, "success_rate": None},
                "Prompting": {"observed_count": 0, "success_rate": None},
                "Simplification": {"observed_count": 0, "success_rate": None},
                "Demonstration": {"observed_count": 0, "success_rate": None},
                "Positive Reinforcement": {"observed_count": 0, "success_rate": None},
                "Gradual Difficulty": {"observed_count": 0, "success_rate": None},
            },
            activity_type_effectiveness={
                "Matching": {"observed_count": 0, "accuracy_average": None},
                "MCQ": {"observed_count": 0, "accuracy_average": None},
                "Ordering": {"observed_count": 0, "accuracy_average": None},
                "Visual Identification": {"observed_count": 0, "accuracy_average": None},
                "Drag & Drop": {"observed_count": 0, "accuracy_average": None},
            },
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
        learner.profile = profile
        in_memory_learners[new_id] = learner
        return learner

    async def update(
        self,
        learner_id: uuid.UUID,
        data: LearnerUpdate,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
        current_user: User | None = None,
    ) -> Learner | None:
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user)
        if not learner:
            return None
        if data.name is not None:
            learner.name = data.name
        if data.learning_level is not None:
            learner.learning_level = data.learning_level
        if data.age_group is not None:
            learner.age_group = data.age_group
        if data.profile and learner.profile:
            profile = learner.profile
            if data.profile.teacher_notes is not None:
                profile.teacher_notes = data.profile.teacher_notes
            if data.profile.support_requirements is not None:
                profile.support_requirements = data.profile.support_requirements
            if data.profile.teacher_constraints is not None:
                profile.teacher_constraints = data.profile.teacher_constraints
            if data.profile.teacher_overrides is not None:
                profile.teacher_overrides = data.profile.teacher_overrides
        learner.updated_at = datetime.now(UTC)
        return learner

    async def delete(
        self,
        learner_id: uuid.UUID,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
        current_user: User | None = None,
    ) -> bool:
        if current_user and getattr(current_user, "role", None) == UserRole.learner:
            return False
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user)
        if not learner:
            return False
        if learner_id in in_memory_learners:
            del in_memory_learners[learner_id]
        return True

    async def add_observation(
        self,
        learner_id: uuid.UUID,
        observation: LearnerObservationCreate,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
        current_user: User | None = None,
    ) -> dict[str, Any] | None:
        if current_user and getattr(current_user, "role", None) == UserRole.learner:
            return None
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user)
        if not learner or not learner.profile:
            return None
        obs_item = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "category": observation.category,
            "summary": observation.summary,
            "context": observation.context or {},
            "teacher_note": observation.teacher_note,
        }
        obs = list(learner.profile.observations)
        obs.append(obs_item)
        learner.profile.observations = obs
        return obs_item


class MockActivityService:
    def __init__(self) -> None:
        self.service = ActivityService(session=AsyncMock())
        self.activities: dict[uuid.UUID, Activity] = {}
        self.history: dict[uuid.UUID, ActivityGenerationSummary] = {}

    def _resolve_objective(self, oid: uuid.UUID | str) -> tuple[str, str, int, dict[str, Any]]:
        """Extract title, description, difficulty, criteria from curriculum catalog or known slugs."""
        obj = None
        if isinstance(oid, uuid.UUID):
            obj = _OBJECTIVES_MAP.get(oid)
        else:
            try:
                parsed_uuid = uuid.UUID(str(oid))
                obj = _OBJECTIVES_MAP.get(parsed_uuid)
            except (ValueError, TypeError):
                pass

        title = "Foundational Practice"
        desc = "Curriculum-aligned practice activity."
        diff = 1
        criteria = {}

        if obj:
            title_dict = obj.get("title")
            if isinstance(title_dict, dict):
                title = str(title_dict.get("en", "Demo Objective"))
            elif isinstance(title_dict, str):
                title = title_dict
            desc_dict = obj.get("description")
            if isinstance(desc_dict, dict):
                desc = str(desc_dict.get("en", "Practice activity"))
            elif isinstance(desc_dict, str):
                desc = desc_dict
            diff = int(obj.get("difficulty_level", 1))
            criteria = obj.get("assessment_criteria") or {}
        else:
            str_oid = str(oid)
            _KNOWN_SLUGS = {
                "math-num-01": ("Count objects from 0–10", "Count concrete everyday objects from 0 to 10 with 1-to-1 correspondence", 1),
                "math-num-02": ("Compare quantities (more, less, equal)", "Compare sets of visual objects to determine more, less, or equal", 2),
                "math-num-03": ("Addition within 10 using concrete objects", "Combine sets of objects to find sums within 10", 2),
                "math-num-04": ("Subtraction within 10 using visual models", "Remove objects from sets to find differences within 10", 3),
                "math-num-05": ("Order numbers from 0 to 20", "Arrange numbers in sequential ascending and descending order", 2),
                "lit-let-01": ("Identify uppercase and lowercase letters", "Recognize and match uppercase and lowercase letter pairs", 1),
                "lit-pho-01": ("Match beginning sounds to letters", "Identify initial phonemes and link them to letter symbols", 2),
                "lit-wor-01": ("Read basic CVC words with visual support", "Decode consonant-vowel-consonant words with picture prompts", 2),
                "daily-rou-01": ("Sequence daily morning routine tasks", "Order chronological steps in daily morning activities", 1),
                "sensory-col-01": ("Discriminate primary colors and geometric shapes", "Identify and categorize items by basic color and shape attributes", 1),
            }
            if str_oid in _KNOWN_SLUGS:
                title, desc, diff = _KNOWN_SLUGS[str_oid]

        return title, desc, diff, criteria

    async def preview_prompt(
        self,
        request: ActivityGenerateRequest,
    ) -> EffectiveGenerationPrompt:
        oid = request.objective_id
        title, desc, diff, criteria = self._resolve_objective(oid)
        if request.difficulty_level is not None:
            diff = request.difficulty_level
        act_type = request.activity_type or ActivityType.MULTIPLE_CHOICE

        grounding_chunks = []
        try:
            from app.knowledge.retrieval import get_knowledge_retrieval_service
            retrieval_service = get_knowledge_retrieval_service()
            grounding_chunks = await retrieval_service.retrieve_pedagogical_context(
                query=f"{title} {desc}".strip(),
                top_k=3,
            )
        except Exception:
            pass

        authoritative_content_payload = None
        try:
            from app.content.bank import get_content_bank
            bank = get_content_bank()
            content_item = bank.get_by_objective(oid, act_type, diff)
            if content_item:
                authoritative_content_payload = {
                    "prompt": content_item.get_prompt(request.language),
                    "correct_answer": content_item.correct_answer,
                    "content_payload": content_item.content_payload,
                }
        except Exception:
            pass

        if request.mode == "lesson":
            return compile_lesson_prompt(
                spec=request,
                objective_title=title,
                objective_description=desc,
                grounding_chunks=grounding_chunks,
                authoritative_content=authoritative_content_payload,
            )

        return compile_generation_prompt(
            spec=request,
            objective_title=title,
            objective_description=desc,
            assessment_criteria=criteria,
            grounding_chunks=grounding_chunks,
            authoritative_content=authoritative_content_payload,
        )

    async def generate_activity(
        self,
        request: ActivityGenerateRequest,
        current_user: User | None = None,
    ) -> ActivityGenerateResponse:
        oid = request.objective_id
        title, desc, diff, criteria = self._resolve_objective(oid)

        if request.difficulty_level is not None:
            diff = request.difficulty_level
        diff = max(1, min(5, diff))

        act_type = request.activity_type or ActivityType.MULTIPLE_CHOICE

        # ── Attempt REAL Gemini generation pipeline ──
        from app.ai.orchestrator.orchestrator import get_ai_orchestrator
        orchestrator = get_ai_orchestrator()

        if orchestrator.is_available:
            try:
                grounding_sources: list[dict[str, Any]] = []
                grounding_chunks: list[Any] = []

                # 1. RAG retrieval (best-effort)
                try:
                    from app.knowledge.retrieval import get_knowledge_retrieval_service
                    retrieval_service = get_knowledge_retrieval_service()
                    grounding_chunks = await retrieval_service.retrieve_pedagogical_context(
                        query=f"{title} {desc}".strip(),
                        top_k=3,
                    )
                    for c in grounding_chunks:
                        grounding_sources.append({
                            "chunk_id": c.chunk_id,
                            "title": c.document_title,
                            "source": c.source,
                            "category": c.category,
                            "score": c.score,
                            "excerpt": c.content[:200],
                        })
                except Exception:
                    pass

                # 2. Content Bank grounding (best-effort)
                authoritative_content_payload = None
                try:
                    from app.content.bank import get_content_bank
                    bank = get_content_bank()
                    content_item = bank.get_by_objective(oid, act_type, diff)
                    if content_item:
                        authoritative_content_payload = {
                            "prompt": content_item.get_prompt(request.language),
                            "correct_answer": content_item.correct_answer,
                            "content_payload": content_item.content_payload,
                        }
                except Exception:
                    pass

                # 3. Prompt compiler
                compiled = compile_generation_prompt(
                    spec=request,
                    objective_title=title,
                    objective_description=desc,
                    assessment_criteria=criteria,
                    grounding_chunks=grounding_chunks,
                    authoritative_content=authoritative_content_payload,
                )
                messages = [
                    Message(role=MessageRole.SYSTEM, content=compiled.system_prompt),
                    Message(role=MessageRole.USER, content=compiled.user_prompt),
                ]

                # 4. Gemini structured generation
                from app.activities.schemas import Activity as ActivitySchema
                output_schema = ActivitySchema.model_json_schema()
                raw_response = await orchestrator.generate_structured(
                    messages=messages,
                    output_schema=output_schema,
                )

                # 5. Patch required IDs
                if not raw_response.get("id"):
                    raw_response["id"] = str(uuid.uuid4())
                raw_response["objective_id"] = str(oid)
                raw_response["activity_type"] = act_type.value
                raw_response["difficulty_level"] = diff
                if isinstance(raw_response.get("content"), dict):
                    raw_response["content"]["activity_type"] = act_type.value

                # 6. Pydantic validation
                activity = Activity.model_validate(raw_response)
                self.activities[activity.id] = activity

                summary = ActivityGenerationSummary(
                    id=activity.id,
                    objective_id=oid,
                    activity_type=activity.activity_type,
                    difficulty_level=activity.difficulty_level,
                    title=activity.title,
                    generation_source=orchestrator.provider.provider_name,
                    fallback_used=False,
                    created_at=datetime.now(UTC).isoformat(),
                    grounding_sources_count=len(grounding_sources),
                )
                self.history[activity.id] = summary

                return ActivityGenerateResponse(
                    activity=activity.to_learner_safe(),
                    fallback_used=False,
                    generation_source=orchestrator.provider.provider_name,
                    learner_id=request.learner_id,
                    objective_id=oid,
                    grounding_sources=grounding_sources,
                )
            except Exception as gen_err:
                import traceback
                traceback.print_exc()
                # Fall through to deterministic fallback

        # ── Deterministic Fallback ──
        activity = create_fallback_activity(
            objective_id=oid,
            objective_title=title,
            objective_description=desc,
            difficulty_level=diff,
            activity_type=act_type,
            language=request.language,
            item_count=request.item_count,
            question_count=request.question_count,
            seed=request.seed or 0,
        )
        self.activities[activity.id] = activity

        summary = ActivityGenerationSummary(
            id=activity.id,
            objective_id=oid,
            activity_type=activity.activity_type,
            difficulty_level=activity.difficulty_level,
            title=activity.title,
            generation_source="deterministic_fallback",
            fallback_used=True,
            created_at=datetime.now(UTC).isoformat(),
            grounding_sources_count=0,
        )
        self.history[activity.id] = summary

        return ActivityGenerateResponse(
            activity=activity.to_learner_safe(),
            fallback_used=True,
            generation_source="deterministic_fallback",
            learner_id=request.learner_id,
            objective_id=oid,
            grounding_sources=[],
        )

    async def generate_lesson(
        self,
        request: ActivityGenerateRequest,
        current_user: User | None = None,
    ) -> LessonGenerateResponse:
        oid = request.objective_id
        title, desc, diff, criteria = self._resolve_objective(oid)
        act_type = request.activity_type or ActivityType.MULTIPLE_CHOICE

        grounding_sources: list[dict[str, Any]] = []
        grounding_chunks = []
        try:
            from app.knowledge.retrieval import get_knowledge_retrieval_service
            retrieval_service = get_knowledge_retrieval_service()
            grounding_chunks = await retrieval_service.retrieve_pedagogical_context(
                query=f"{title} {desc}".strip(),
                top_k=3,
            )
            for c in grounding_chunks:
                grounding_sources.append({
                    "chunk_id": c.chunk_id,
                    "title": c.document_title,
                    "source": c.source,
                    "category": c.category,
                    "score": c.score,
                    "excerpt": c.content[:200],
                })
        except Exception:
            pass

        authoritative_content_payload = None
        try:
            from app.content.bank import get_content_bank
            bank = get_content_bank()
            content_item = bank.get_by_objective(oid, act_type, diff)
            if content_item:
                authoritative_content_payload = {
                    "prompt": content_item.get_prompt(request.language),
                    "correct_answer": content_item.correct_answer,
                    "content_payload": content_item.content_payload,
                }
        except Exception:
            pass

        compiled = compile_lesson_prompt(
            spec=request,
            objective_title=title,
            objective_description=desc,
            grounding_chunks=grounding_chunks,
            authoritative_content=authoritative_content_payload,
        )

        from app.ai.orchestrator.orchestrator import get_ai_orchestrator
        orchestrator = get_ai_orchestrator()

        if orchestrator.is_available:
            try:
                messages = [
                    Message(role=MessageRole.SYSTEM, content=compiled.system_prompt),
                    Message(role=MessageRole.USER, content=compiled.user_prompt),
                ]
                output_schema = LessonPlan.model_json_schema()
                raw_resp = await orchestrator.generate_structured(
                    messages=messages,
                    output_schema=output_schema,
                )
                if not raw_resp.get("id"):
                    raw_resp["id"] = str(uuid.uuid4())
                raw_resp["objective_id"] = str(oid)
                raw_resp["generation_source"] = orchestrator.provider.provider_name
                raw_resp["fallback_used"] = False
                raw_resp["grounding_sources"] = grounding_sources

                # Embed practice activity
                embedded_act = create_fallback_activity(
                    objective_id=oid,
                    objective_title=title,
                    objective_description=desc,
                    difficulty_level=diff,
                    activity_type=act_type,
                    language=request.language,
                    seed=request.seed or 0,
                )
                self.activities[embedded_act.id] = embedded_act
                raw_resp["activity"] = embedded_act.model_dump()

                lesson_plan = LessonPlan.model_validate(raw_resp)
                return LessonGenerateResponse(
                    lesson_plan=lesson_plan,
                    fallback_used=False,
                    generation_source=orchestrator.provider.provider_name,
                    objective_id=oid,
                    grounding_sources=grounding_sources,
                )
            except Exception as e:
                import traceback
                traceback.print_exc()

        fallback_lesson = create_fallback_lesson(
            objective_id=oid,
            objective_title=title,
            objective_description=desc,
            difficulty_level=diff,
            language=request.language,
            suggested_activity_type=act_type,
            seed=request.seed or 0,
        )
        if fallback_lesson.activity:
            self.activities[fallback_lesson.activity.id] = fallback_lesson.activity
        return LessonGenerateResponse(
            lesson_plan=fallback_lesson,
            fallback_used=True,
            generation_source="deterministic_fallback",
            objective_id=oid,
            grounding_sources=[],
        )

    async def update_activity(
        self,
        activity_id: uuid.UUID,
        update: ActivityUpdateRequest,
    ) -> Activity:
        activity = await self.get_activity(activity_id)
        if not activity:
            raise NotFoundError(f"Activity with id '{activity_id}' not found.")
        raw = activity.model_dump()
        if update.title is not None:
            raw["title"] = update.title
        if update.instructions is not None:
            raw["instructions"] = update.instructions
        if update.hints is not None:
            raw["hints"] = update.hints
        if update.teacher_notes is not None:
            if not raw.get("metadata"):
                raw["metadata"] = {}
            raw["metadata"]["teacher_notes"] = update.teacher_notes

        validated = Activity.model_validate(raw)
        self.activities[validated.id] = validated
        return validated

    async def get_history(self) -> list[ActivityGenerationSummary]:
        return list(self.history.values())[-20:]

    async def get_activity(self, activity_id: uuid.UUID) -> Activity | None:
        if activity_id in self.activities:
            return self.activities[activity_id]

        from app.content.bank import get_content_bank
        bank = get_content_bank()
        item = bank.get_by_id(activity_id)
        if item is not None:
            created = bank.create_activity_from_content(
                item,
                target_modality=item.supported_modalities[0],
                activity_id=activity_id,
            )
            self.activities[activity_id] = created
            return created
        return None

    async def evaluate_submission(
        self,
        request: ActivitySubmissionRequest,
    ) -> ActivityEvaluationResponse:
        from app.activities.service import _ACTIVITIES_CACHE
        if request.activity_id in self.activities:
            _ACTIVITIES_CACHE[request.activity_id] = self.activities[request.activity_id]
        return await self.service.evaluate_submission(request=request)


class MockAnalyticsService:
    """In-memory telemetry and performance event registry for development."""

    def __init__(self) -> None:
        self.events: list[PerformanceEvent] = []
        self.attempts: list[ActivityAttempt] = []

    async def record_performance_event(
        self,
        event_in: PerformanceEventCreate,
    ) -> PerformanceEvent:
        event = PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=event_in.learner_id,
            activity_id=event_in.activity_id,
            attempt_id=event_in.attempt_id,
            objective_id=event_in.objective_id,
            activity_type=event_in.activity_type.value,
            modality=event_in.modality.value,
            strategy=event_in.strategy.value,
            correct=event_in.correct,
            score=event_in.score,
            attempts=event_in.attempts,
            response_time_ms=event_in.response_time_ms,
            hints_used=event_in.hints_used,
            assistance_level=event_in.assistance_level,
            completed=event_in.completed,
            difficulty=event_in.difficulty,
            event_metadata=event_in.metadata,
            timestamp=event_in.timestamp or datetime.now(UTC),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self.events.append(event)
        return event

    async def record_activity_attempt(
        self,
        attempt_in: ActivityAttemptCreate,
    ) -> ActivityAttempt:
        attempt = ActivityAttempt(
            id=uuid.uuid4(),
            activity_id=attempt_in.activity_id,
            learner_id=attempt_in.learner_id,
            session_id=attempt_in.session_id,
            started_at=attempt_in.started_at or datetime.now(UTC),
            completed_at=attempt_in.completed_at,
            response_data=attempt_in.response_data,
            score=attempt_in.score,
            completed=attempt_in.completed,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self.attempts.append(attempt)
        return attempt

    async def get_learner_events(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
        filters: PerformanceEventQueryFilter | None = None,
    ) -> list[PerformanceEvent]:
        matching = [e for e in self.events if e.learner_id == learner_id]
        if filters:
            if filters.activity_type:
                matching = [e for e in matching if e.activity_type == filters.activity_type.value]
            if filters.objective_id:
                matching = [e for e in matching if e.objective_id == filters.objective_id]
            if filters.correct is not None:
                matching = [e for e in matching if e.correct == filters.correct]
        return matching

    async def get_event_by_id(
        self,
        event_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> PerformanceEvent:
        for e in self.events:
            if e.id == event_id:
                return e
        from app.core.errors import NotFoundError
        raise NotFoundError(f"Performance event '{event_id}' not found.")

    async def get_learner_summary(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> LearnerAnalyticsSummary:
        matching = [e for e in self.events if e.learner_id == learner_id]
        if not matching:
            return LearnerAnalyticsSummary(
                learner_id=learner_id,
                total_events=0,
                completed_activities=0,
                overall_accuracy=0.0,
                avg_score=0.0,
                avg_response_time_ms=0.0,
                avg_hints_per_activity=0.0,
                avg_assistance_level=0.0,
                modality_breakdown=[],
                activity_type_breakdown=[],
                first_activity_at=None,
                last_activity_at=None,
            )
        total = len(matching)
        completed_activity_ids = {e.activity_id for e in matching if e.completed and e.activity_id is not None}
        completed = len(completed_activity_ids)
        correct = sum(1 for e in matching if e.correct)
        acc = round(correct / total, 4)
        avg_sc = round(sum(e.score for e in matching) / total, 4)
        avg_rt = round(sum(e.response_time_ms for e in matching) / total, 2)
        avg_hints = round(sum(e.hints_used for e in matching) / total, 2)
        avg_assist = round(sum(e.assistance_level for e in matching) / total, 2)

        modality_breakdown: list[ModalityMetrics] = []
        for mod in sorted(list({e.modality for e in matching})):
            m_events = [e for e in matching if e.modality == mod]
            m_total = len(m_events)
            m_correct = sum(1 for e in m_events if e.correct)
            modality_breakdown.append(
                ModalityMetrics(
                    modality=mod,
                    total_events=m_total,
                    accuracy=round(m_correct / m_total, 4) if m_total else 0.0,
                    avg_score=round(sum(e.score for e in m_events) / m_total, 4) if m_total else 0.0,
                    avg_response_time_ms=round(sum(e.response_time_ms for e in m_events) / m_total, 2) if m_total else 0.0,
                    avg_assistance_level=round(sum(e.assistance_level for e in m_events) / m_total, 2) if m_total else 0.0,
                )
            )

        activity_type_breakdown: list[ActivityTypeMetrics] = []
        for at in sorted(list({e.activity_type for e in matching})):
            at_events = [e for e in matching if e.activity_type == at]
            at_total = len(at_events)
            at_correct = sum(1 for e in at_events if e.correct)
            activity_type_breakdown.append(
                ActivityTypeMetrics(
                    activity_type=at,
                    total_events=at_total,
                    accuracy=round(at_correct / at_total, 4) if at_total else 0.0,
                    avg_score=round(sum(e.score for e in at_events) / at_total, 4) if at_total else 0.0,
                )
            )

        return LearnerAnalyticsSummary(
            learner_id=learner_id,
            total_events=total,
            completed_activities=completed,
            overall_accuracy=acc,
            avg_score=avg_sc,
            avg_response_time_ms=avg_rt,
            avg_hints_per_activity=avg_hints,
            avg_assistance_level=avg_assist,
            modality_breakdown=modality_breakdown,
            activity_type_breakdown=activity_type_breakdown,
            first_activity_at=matching[0].timestamp,
            last_activity_at=matching[-1].timestamp,
        )

    async def get_learner_mastery(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> LearnerMasteryReport:
        matching = [e for e in self.events if e.learner_id == learner_id and e.objective_id is not None]
        obj_ids = sorted(list({e.objective_id for e in matching if e.objective_id is not None}))

        objective_statuses: list[ObjectiveMasteryStatus] = []
        for obj_id in obj_ids:
            obj_events = [e for e in matching if e.objective_id == obj_id]
            total_attempts = len(obj_events)
            correct_count = sum(1 for e in obj_events if e.correct)
            acc = round(correct_count / total_attempts, 4) if total_attempts else 0.0
            avg_assist = round(sum(e.assistance_level for e in obj_events) / total_attempts, 2) if total_attempts else 0.0
            mastery_achieved = bool(total_attempts >= 1 and acc >= 0.80 and avg_assist <= 1.0)
            status = "mastered" if mastery_achieved else "in_progress"
            objective_statuses.append(
                ObjectiveMasteryStatus(
                    objective_id=obj_id,
                    objective_title=f"Objective {obj_id}",
                    difficulty_level=1,
                    total_attempts=total_attempts,
                    accuracy=acc,
                    avg_assistance_level=avg_assist,
                    mastery_achieved=mastery_achieved,
                    status=status,
                    last_attempt_at=max((e.timestamp for e in obj_events), default=None),
                )
            )

        total_evaluated = len(objective_statuses)
        mastered = sum(1 for o in objective_statuses if o.status == "mastered")
        in_prog = sum(1 for o in objective_statuses if o.status == "in_progress")
        pct = round((mastered / total_evaluated) * 100.0, 2) if total_evaluated else 0.0
        return LearnerMasteryReport(
            learner_id=learner_id,
            total_objectives_evaluated=total_evaluated,
            mastered_count=mastered,
            in_progress_count=in_prog,
            not_started_count=0,
            mastery_percentage=pct,
            objectives=objective_statuses,
        )

    async def get_learner_progress(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
        days: int = 30,
    ) -> LearnerProgressReport:
        matching = [e for e in self.events if e.learner_id == learner_id]
        groups: dict[str, list[PerformanceEvent]] = {}
        for e in matching:
            d_str = e.timestamp.strftime("%Y-%m-%d")
            groups.setdefault(d_str, []).append(e)

        data_points: list[ProgressDataPoint] = []
        for d in sorted(groups.keys()):
            d_events = groups[d]
            cnt = len(d_events)
            corr = sum(1 for e in d_events if e.correct)
            data_points.append(
                ProgressDataPoint(
                    date=d,
                    events_count=cnt,
                    accuracy=round(corr / cnt, 4) if cnt else 0.0,
                    avg_score=round(sum(e.score for e in d_events) / cnt, 4) if cnt else 0.0,
                )
            )
        return LearnerProgressReport(
            learner_id=learner_id,
            total_days_active=len(data_points),
            data_points=data_points,
        )


_MOCK_ANALYTICS_INSTANCE = MockAnalyticsService()

# ── Load 20 Test Student Scenarios and Telemetry into In-Memory Fixtures ─────
_test_learner_defs = generate_learner_definitions(now=now)
for _s in _test_learner_defs:
    _assigned_tid = teacher_id if _s.cohort_key == "cohort_a" else COHORT_B_TEACHER_ID
    _t_learner = Learner(
        id=_s.learner_id,
        name=_s.name,
        age_group=_s.age_group,
        learning_level=_s.learning_level,
        teacher_id=_assigned_tid,
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    _t_profile = LearnerProfile(
        id=_s.profile_id,
        learner_id=_s.learner_id,
        learner=_t_learner,
        communication_preferences={
            "primary_mode": _s.communication_primary_mode,
            "receptive_preference": _s.receptive_preferences,
            "expressive_preference": _s.expressive_preferences,
            "notes": f"Scenario: {_s.key}. {_s.summary_description}",
        },
        current_skill_level={
            "literacy_stage": _s.literacy_stage,
            "numeracy_stage": _s.numeracy_stage,
            "attention_span_minutes": _s.attention_span_minutes,
            "strengths": _s.strengths,
            "focus_areas": _s.focus_areas,
        },
        support_requirements={
            "sensory_accommodations": _s.sensory_accommodations,
            "pacing": _s.pacing,
            "guidance_level": "standard",
        },
        teacher_constraints={
            "max_session_duration_minutes": _s.attention_span_minutes,
            "excluded_modalities": [],
            "required_modalities": ["Visual"],
        },
        teacher_notes=_s.teacher_notes,
        teacher_overrides={},
        modality_effectiveness=_s.modality_effectiveness,
        strategy_effectiveness={"scaffolded_hints": 0.85, "visual_cueing": 0.88},
        activity_type_effectiveness={"matching": 0.85, "ordering": 0.80},
        difficulty_tolerance=1.5,
        assistance_requirements={"preferred_prompt_hierarchy": "least_to_most"},
        response_behavior={"typical_latency_seconds": 3.0},
        observations={"scenario": _s.key},
        created_at=now,
        updated_at=now,
    )
    _t_learner.profile = _t_profile
    in_memory_learners[_s.learner_id] = _t_learner

    for _idx, _t in enumerate(_s.telemetry_events):
        _event_time = now - timedelta(days=_t.days_ago, minutes=_idx * 15)
        _att_id = get_test_uuid(f"attempt.{_s.key}.{_idx}")
        _act_id = get_test_uuid(f"activity.{_s.key}.{_idx}")

        _att = ActivityAttempt(
            id=_att_id,
            activity_id=_act_id,
            learner_id=_s.learner_id,
            session_id=get_test_uuid(f"session.{_s.key}.{_t.days_ago}"),
            started_at=_event_time - timedelta(minutes=3),
            completed_at=_event_time,
            response_data={"selected": "option_A", "correct": _t.correct, "score": _t.score},
            score=_t.score,
            completed=_t.completed,
            created_at=_event_time,
            updated_at=_event_time,
        )
        _MOCK_ANALYTICS_INSTANCE.attempts.append(_att)

        _pevent = PerformanceEvent(
            id=get_test_uuid(f"event.{_s.key}.{_idx}"),
            learner_id=_s.learner_id,
            activity_id=_act_id,
            attempt_id=_att_id,
            objective_id=_t.objective_id,
            activity_type=_t.activity_type,
            modality=_t.modality,
            strategy=_t.strategy,
            correct=_t.correct,
            score=_t.score,
            attempts=1,
            response_time_ms=_t.response_time_ms,
            hints_used=_t.hints_used,
            assistance_level=_t.assistance_level,
            completed=_t.completed,
            difficulty=_t.difficulty,
            event_metadata={"scenario": _s.key, "test_data": True},
            timestamp=_event_time,
            created_at=_event_time,
            updated_at=_event_time,
        )
        _MOCK_ANALYTICS_INSTANCE.events.append(_pevent)


class MockRecommendationService:
    """Mock RecommendationService for offline development."""

    async def get_recommendation(
        self,
        learner_id: uuid.UUID,
        current_user: User | None = None,
        language: str = "en",
    ) -> RecommendationDecision:
        from app.ai.adaptation.engine import AdaptationEngine
        from app.curriculum.models import LearningObjective

        # Find learner profile
        learner = in_memory_learners.get(learner_id)
        profile = learner.profile if learner else demo_profile

        # Build candidate objectives from mock curriculum fixtures
        obj1_dict = _OBJECTIVES_MAP.get(obj1_id, {"title": {"en": "Demo Objective 1"}, "difficulty_level": 1})
        obj2_dict = _OBJECTIVES_MAP.get(obj2_id, {"title": {"en": "Demo Objective 2"}, "difficulty_level": 2})
        mock_obj1 = LearningObjective(
            id=obj1_id,
            lesson_id=less_id,
            title=obj1_dict["title"],
            description=obj1_dict.get("description"),
            difficulty_level=obj1_dict.get("difficulty_level", 1),
            assessment_criteria=obj1_dict.get("assessment_criteria"),
            order_index=obj1_dict.get("order_index", 1),
            is_active=True,
            prerequisites=[],
        )
        mock_obj2 = LearningObjective(
            id=obj2_id,
            lesson_id=less_id,
            title=obj2_dict["title"],
            description=obj2_dict.get("description"),
            difficulty_level=obj2_dict.get("difficulty_level", 2),
            assessment_criteria=obj2_dict.get("assessment_criteria"),
            order_index=obj2_dict.get("order_index", 2),
            is_active=True,
            prerequisites=[mock_obj1],
        )
        candidate_objectives: list[LearningObjective] = [mock_obj1, mock_obj2]

        summary = await _MOCK_ANALYTICS_INSTANCE.get_learner_summary(learner_id)
        mastery = await _MOCK_ANALYTICS_INSTANCE.get_learner_mastery(learner_id)

        return AdaptationEngine.build_recommendation(
            learner_id=learner_id,
            candidate_objectives=candidate_objectives,
            profile=profile,
            mastery_report=mastery,
            analytics_summary=summary,
            language=language,
        )

    async def get_next_activity(
        self,
        learner_id: uuid.UUID,
        current_user: User | None = None,
        language: str = "en",
    ) -> AdaptiveNextActivityResponse:
        decision = await self.get_recommendation(learner_id, current_user, language=language)
        activity_service = MockActivityService()
        gen_req = ActivityGenerateRequest(
            objective_id=decision.objective_id,
            learner_id=learner_id,
            activity_type=decision.recommended_activity_type,
            difficulty_level=decision.difficulty_level,
            language=language,
        )
        gen_resp = await activity_service.generate_activity(gen_req, current_user or User(id=uuid.uuid4(), email="dev@eduvia.org", hashed_password="", role=UserRole.teacher))
        return AdaptiveNextActivityResponse(
            decision=decision,
            activity=gen_resp.activity,
            fallback_used=gen_resp.fallback_used,
            generation_source=gen_resp.generation_source,
        )

    async def sync_learner_profile_effectiveness(
        self,
        learner_id: uuid.UUID,
        current_user: User | None = None,
    ) -> ProfileSyncResult:
        matching_events = [e for e in _MOCK_ANALYTICS_INSTANCE.events if e.learner_id == learner_id]
        return ProfileSyncResult(
            learner_id=learner_id,
            updated_modalities={"Visual": {"observed_count": len(matching_events), "engagement_rating": 0.85}},
            updated_strategies={"Step-by-Step": {"observed_count": len(matching_events), "success_rate": 0.80}},
            total_events_processed=len(matching_events),
        )


_MOCK_RECOMMENDATION_INSTANCE = MockRecommendationService()


class MockTeacherDashboardService:
    """Mock TeacherDashboardService for offline development with cohort awareness."""

    def _get_scoped_learners(self, teacher_user: User | None = None) -> list[Learner]:
        learners = list(in_memory_learners.values())
        if teacher_user and getattr(teacher_user, "role", None) != UserRole.admin:
            learners = [l for l in learners if getattr(l, "teacher_id", None) == teacher_user.id]
        return learners

    async def get_dashboard_overview(self, teacher_user: User | None = None) -> TeacherDashboardOverview:
        learners = self._get_scoped_learners(teacher_user)
        learner_ids = {l.id for l in learners}
        events = [e for e in _MOCK_ANALYTICS_INSTANCE.events if e.learner_id in learner_ids]
        
        # Consider active in last 7 days
        seven_days_ago = datetime.now(UTC) - timedelta(days=7)
        active_ids = {e.learner_id for e in events if e.timestamp >= seven_days_ago}
        completed_7d = sum(1 for e in events if e.completed and e.timestamp >= seven_days_ago)
        events_7d = [e for e in events if e.timestamp >= seven_days_ago]
        avg_acc = round(sum(1 for e in events_7d if e.correct) / len(events_7d), 2) if events_7d else (
            round(sum(1 for e in events if e.correct) / len(events), 2) if events else 0.85
        )
        
        alerts = await self.get_intervention_alerts(teacher_user)
        teacher_display = teacher_user.full_name if (teacher_user and teacher_user.full_name) else "Alice Teacher"
        
        return TeacherDashboardOverview(
            total_learners=len(learners),
            active_learners_7d=len(active_ids),
            total_activities_completed_7d=completed_7d,
            cohort_average_accuracy_7d=avg_acc,
            active_alerts_count=len(alerts),
            recent_alerts=alerts[:5],
            teacher_id=teacher_user.id if teacher_user else teacher_id,
            teacher_name=teacher_display,
            total_assigned_learners=len(learners),
            active_learners_count=len(active_ids),
            total_completed_activities=completed_7d,
            average_cohort_accuracy=avg_acc,
            pending_alerts=alerts[:5],
            recent_recommendations=[],
        )

    async def get_cohort_insights(self, teacher_user: User | None = None, days: int = 30) -> CohortInsights:
        learners = self._get_scoped_learners(teacher_user)
        learner_ids = {l.id for l in learners}
        cutoff = datetime.now(UTC) - timedelta(days=days)
        events = [e for e in _MOCK_ANALYTICS_INSTANCE.events if e.learner_id in learner_ids and e.timestamp >= cutoff]
        all_events = [e for e in _MOCK_ANALYTICS_INSTANCE.events if e.learner_id in learner_ids]
        
        completed_count = sum(1 for e in events if e.completed)
        avg_acc = round(sum(1 for e in events if e.correct) / len(events), 2) if events else (
            round(sum(1 for e in all_events if e.correct) / len(all_events), 2) if all_events else 0.80
        )
        avg_asst = round(sum(e.assistance_level for e in events) / len(events), 2) if events else (
            round(sum(e.assistance_level for e in all_events) / len(all_events), 2) if all_events else 0.5
        )
        
        modality_distribution = {"visual": 0.45, "interactive": 0.30, "audio": 0.15, "reading": 0.10}
        mastery_counts = {"mastered": 0, "developing": 0, "emerging": 0, "struggling": 0}

        learner_summaries = []
        for l in learners:
            l_events = [e for e in all_events if e.learner_id == l.id]
            l_acc = round(sum(1 for e in l_events if e.correct) / len(l_events), 2) if l_events else 0.50
            l_asst = round(sum(e.assistance_level for e in l_events) / len(l_events), 2) if l_events else 0.50
            
            if l_acc >= 0.85:
                mastery_counts["mastered"] += 1
            elif l_acc >= 0.70:
                mastery_counts["developing"] += 1
            elif l_acc >= 0.50:
                mastery_counts["emerging"] += 1
            else:
                mastery_counts["struggling"] += 1

            comm_pref = "verbal"
            if hasattr(l, "profile") and l.profile and l.profile.communication_preferences:
                comm_pref = l.profile.communication_preferences.get("primary_mode", "verbal")

            learner_name = getattr(l, "name", "Student")
            last_active = l_events[-1].timestamp if l_events else (datetime.now(UTC) - timedelta(days=60))
            
            # Check alerts for this learner
            l_alert_count = 1 if l_acc < 0.50 or l_asst > 1.2 else 0

            learner_summaries.append(
                CohortLearnerSummary(
                    learner_id=l.id,
                    display_name=learner_name,
                    learning_level=l.learning_level.value if hasattr(l.learning_level, "value") else str(l.learning_level),
                    age_group=l.age_group.value if hasattr(l.age_group, "value") else str(l.age_group),
                    communication_preference=str(comm_pref),
                    activities_completed=sum(1 for e in l_events if e.completed),
                    completed_activities=sum(1 for e in l_events if e.completed),
                    total_events=len(l_events),
                    overall_accuracy=l_acc,
                    average_assistance=l_asst,
                    average_assistance_level=l_asst,
                    mastered_objectives_count=2 if l_acc >= 0.80 else (1 if l_acc >= 0.60 else 0),
                    in_progress_objectives_count=1 if l_acc < 0.80 else 0,
                    last_active_at=last_active,
                    active_alert_count=l_alert_count,
                    active_alerts_count=l_alert_count,
                )
            )

        active_in_period = len({e.learner_id for e in events})

        return CohortInsights(
            cohort_size=len(learners),
            reporting_period_days=days,
            average_accuracy=avg_acc,
            average_assistance_level=avg_asst,
            modality_distribution=modality_distribution,
            mastery_distribution=mastery_counts,
            learner_summaries=learner_summaries,
            teacher_id=teacher_user.id if teacher_user else teacher_id,
            reporting_period=f"{days}_days",
            total_cohort_learners=len(learners),
            active_learners_in_period=active_in_period,
            cohort_accuracy=avg_acc,
            cohort_avg_assistance_level=avg_asst,
            total_activities_completed=completed_count,
            mastery_status_counts=mastery_counts,
            learners=learner_summaries,
        )

    async def get_intervention_alerts(
        self, teacher_user: User | None = None, target_learner_id: uuid.UUID | None = None
    ) -> list[InterventionAlert]:
        learners = self._get_scoped_learners(teacher_user)
        if target_learner_id:
            learners = [l for l in learners if l.id == target_learner_id]

        alerts = []
        now_dt = datetime.now(UTC)
        
        for l in learners:
            l_name = getattr(l, "name", "Student")
            l_events = [e for e in _MOCK_ANALYTICS_INSTANCE.events if e.learner_id == l.id]
            if not l_events:
                continue
            l_acc = sum(1 for e in l_events if e.correct) / len(l_events)
            l_asst = sum(e.assistance_level for e in l_events) / len(l_events)

            # Scenario-specific alerts
            if "At Risk" in l_name:
                alerts.append(
                    InterventionAlert(
                        alert_id=f"alert_risk_{l.id}",
                        learner_id=l.id,
                        learner_display_name=l_name,
                        trigger_type=AlertTriggerType.low_accuracy,
                        severity=AlertSeverity.action_required,
                        message="Critical learning regression: Accuracy dropped below 30% with extended inactivity.",
                        summary="Critical learning regression: Accuracy dropped below 30% with extended inactivity.",
                        recommended_action="Schedule 1:1 check-in and re-assign foundational visual vocabulary modules.",
                        recommended_pedagogical_action="Schedule 1:1 check-in and re-assign foundational visual vocabulary modules.",
                        evidence_context={"overall_accuracy": round(l_acc, 2), "days_inactive": 28},
                        evidence_metrics={"overall_accuracy": round(l_acc, 2), "days_inactive": 28},
                        detected_at=now_dt - timedelta(days=2),
                        created_at=now_dt - timedelta(days=2),
                        is_resolved=False,
                    )
                )
            elif "Struggling" in l_name:
                alerts.append(
                    InterventionAlert(
                        alert_id=f"alert_struggle_{l.id}",
                        learner_id=l.id,
                        learner_display_name=l_name,
                        trigger_type=AlertTriggerType.high_assistance,
                        severity=AlertSeverity.warning,
                        message="High assistance dependency detected: Required Level 2 assistance across recent attempts.",
                        summary="High assistance dependency detected: Required Level 2 assistance across recent attempts.",
                        recommended_action="Activate high-contrast visual cues and reduce multiple-choice distractors.",
                        recommended_pedagogical_action="Activate high-contrast visual cues and reduce multiple-choice distractors.",
                        evidence_context={"average_assistance": round(l_asst, 2), "accuracy": round(l_acc, 2)},
                        evidence_metrics={"average_assistance": round(l_asst, 2), "accuracy": round(l_acc, 2)},
                        detected_at=now_dt - timedelta(days=1),
                        created_at=now_dt - timedelta(days=1),
                        is_resolved=False,
                    )
                )
            elif "Inconsistent" in l_name:
                alerts.append(
                    InterventionAlert(
                        alert_id=f"alert_inconsistent_{l.id}",
                        learner_id=l.id,
                        learner_display_name=l_name,
                        trigger_type=AlertTriggerType.stalled_mastery,
                        severity=AlertSeverity.info,
                        message="High performance variance: Alternating between high scores and zero completion.",
                        summary="High performance variance: Alternating between high scores and zero completion.",
                        recommended_action="Review sensory engagement settings and check for environmental fatigue.",
                        recommended_pedagogical_action="Review sensory engagement settings and check for environmental fatigue.",
                        evidence_context={"variance_detected": True, "completed_ratio": 0.5},
                        evidence_metrics={"variance_detected": True, "completed_ratio": 0.5},
                        detected_at=now_dt - timedelta(days=3),
                        created_at=now_dt - timedelta(days=3),
                        is_resolved=False,
                    )
                )
            elif "Low Engagement" in l_name:
                alerts.append(
                    InterventionAlert(
                        alert_id=f"alert_low_eng_{l.id}",
                        learner_id=l.id,
                        learner_display_name=l_name,
                        trigger_type=AlertTriggerType.inactivity,
                        severity=AlertSeverity.warning,
                        message="Declining session frequency despite adequate historical accuracy.",
                        summary="Declining session frequency despite adequate historical accuracy.",
                        recommended_action="Send gamified reminder badge and introduce interactive auditory prompts.",
                        recommended_pedagogical_action="Send gamified reminder badge and introduce interactive auditory prompts.",
                        evidence_context={"last_session_days_ago": 18, "historical_accuracy": round(l_acc, 2)},
                        evidence_metrics={"last_session_days_ago": 18, "historical_accuracy": round(l_acc, 2)},
                        detected_at=now_dt - timedelta(days=4),
                        created_at=now_dt - timedelta(days=4),
                        is_resolved=False,
                    )
                )

        return alerts

    async def get_learner_iep_report(
        self, teacher_user: User | None = None, learner_id: uuid.UUID | None = None, days: int = 30
    ) -> IEPReport:
        target_id = learner_id or demo_learner_id
        learner = in_memory_learners.get(target_id, demo_learner)
        now_dt = datetime.now(UTC)
        summary = await _MOCK_ANALYTICS_INSTANCE.get_learner_summary(target_id)
        mastery = await _MOCK_ANALYTICS_INSTANCE.get_learner_mastery(target_id)

        obj_summaries = [
            IEPObjectiveSummary(
                objective_id=st.objective_id,
                title=getattr(st, "objective_title", getattr(st, "title", "Objective")),
                attempts_count=getattr(st, "total_attempts", getattr(st, "attempts_count", 0)),
                accuracy=st.accuracy,
                average_assistance=getattr(st, "avg_assistance_level", getattr(st, "average_assistance", 0.0)),
                status=st.status,
            )
            for st in mastery.objectives
        ]

        comm_pref = "verbal"
        if hasattr(learner, "profile") and learner.profile and hasattr(learner.profile, "communication_preferences") and isinstance(learner.profile.communication_preferences, dict):
            comm_pref = str(learner.profile.communication_preferences.get("primary_mode", "verbal"))

        return IEPReport(
            report_id=f"iep_demo_{target_id}",
            generated_at=now_dt,
            reporting_period=f"Last {days} Days",
            start_date=now_dt - timedelta(days=days),
            end_date=now_dt,
            learner_id=target_id,
            learner_display_name=learner.name,
            learning_level=learner.learning_level.value if hasattr(learner.learning_level, "value") else str(learner.learning_level),
            communication_preference=comm_pref,
            teacher_notes="Demonstrates strong engagement with visual and interactive activities.",
            total_activities_attempted=summary.completed_activities,
            overall_accuracy=summary.overall_accuracy,
            overall_assistance_average=summary.avg_assistance_level,
            modality_efficacy={"visual": 0.85, "interactive": 0.78, "audio": 0.65},
            objectives_progress=obj_summaries,
            teacher_recommendations=[
                "Continue strong emphasis on visual-first presentation modalities.",
                "Maintain progressive scaffolding to encourage autonomous completion.",
            ],
            printable_summary_markdown=f"# IEP Progress Report: {learner.name}\n\n- **Overall Accuracy**: {summary.overall_accuracy * 100:.1f}%\n- **Average Assistance**: {summary.avg_assistance_level:.1f}\n",
        )


_MOCK_TEACHER_DASHBOARD_INSTANCE = MockTeacherDashboardService()


# Patch dependency overrides on FastAPI app
async def override_get_db_session() -> AsyncGenerator[AsyncMock, None]:
    yield AsyncMock()


from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.router import get_analytics_service
from app.analytics.schemas import (
    ActivityAttemptCreate,
    ActivityTypeMetrics,
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    LearnerProgressReport,
    ModalityMetrics,
    ObjectiveMasteryStatus,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    ProgressDataPoint,
)
from app.recommendations.router import get_recommendation_service
from app.recommendations.schemas import (
    AdaptiveNextActivityResponse,
    ProfileSyncResult,
    RecommendationDecision,
)
from app.teachers.router import get_teacher_dashboard_service
from app.teachers.schemas import (
    AlertSeverity,
    AlertTriggerType,
    CohortInsights,
    CohortLearnerSummary,
    IEPObjectiveSummary,
    IEPReport,
    InterventionAlert,
    TeacherDashboardOverview,
)

from app.instructional.router import get_instructional_service
from app.instructional.schemas import (
    ContentBlockType,
    ExplanationMethod,
    InstructionalBlock,
    InstructionalContentRead,
    InstructionalContentUpdate,
    InstructionalGenerateRequest,
    InstructionalGenerateResponse,
    InstructionalStatus,
)
from app.instructional.service import create_fallback_instructional_content


def _extract_localized_text(val: Any, lang: str = "en") -> str:
    if isinstance(val, dict):
        return str(val.get(lang) or val.get("en") or next(iter(val.values()), ""))
    return str(val) if val is not None else ""


class MockInstructionalService:
    def __init__(self) -> None:
        self.contents: dict[uuid.UUID, InstructionalContentRead] = {}

    async def generate(
        self,
        request: InstructionalGenerateRequest,
        current_user: User,
    ) -> InstructionalGenerateResponse:
        obj = _OBJECTIVES_MAP.get(request.objective_id)
        title = _extract_localized_text(obj.get("title", {}), request.language) if obj else "Learning Concept"
        desc = _extract_localized_text(obj.get("description", {}), request.language) if obj else None

        fallback_dict = create_fallback_instructional_content(
            objective_id=request.objective_id,
            objective_title=title,
            objective_description=desc,
            method=request.explanation_method,
            difficulty_level=request.difficulty_level,
            language=request.language,
        )

        blocks = [
            InstructionalBlock(
                id=b["id"],
                block_type=ContentBlockType(b["block_type"]),
                title=b.get("title"),
                body=b.get("body", ""),
                visual_cue=b.get("visual_cue"),
                order_index=b.get("order_index", 1),
                metadata=b.get("metadata", {}),
            )
            for b in fallback_dict["blocks"]
        ]

        now_dt = datetime.now(UTC)
        content_id = uuid.uuid4()
        read_obj = InstructionalContentRead(
            id=content_id,
            objective_id=request.objective_id,
            title=fallback_dict["title"],
            explanation_method=request.explanation_method,
            difficulty_level=request.difficulty_level,
            language=request.language,
            blocks=blocks,
            summary=fallback_dict["summary"],
            status=InstructionalStatus.REVIEW_REQUIRED,
            teacher_notes=request.teacher_instructions,
            created_by=current_user.id,
            metadata={"mock": True},
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.contents[content_id] = read_obj

        return InstructionalGenerateResponse(
            content=read_obj,
            fallback_used=True,
            generation_source="deterministic_fallback",
            objective_id=request.objective_id,
            grounding_sources=[],
        )

    async def get_by_id(self, content_id: uuid.UUID) -> InstructionalContentRead:
        if content_id in self.contents:
            return self.contents[content_id]
        from app.core.errors import NotFoundError
        raise NotFoundError(f"Instructional content '{content_id}' not found.")

    async def get_by_objective(
        self,
        objective_id: uuid.UUID,
        published_only: bool = True,
    ) -> list[InstructionalContentRead]:
        items = [
            c for c in self.contents.values()
            if c.objective_id == objective_id and (
                not published_only or c.status in (InstructionalStatus.APPROVED, InstructionalStatus.PUBLISHED)
            )
        ]
        if not items and published_only:
            obj = _OBJECTIVES_MAP.get(objective_id)
            title = _extract_localized_text(obj.get("title", {}), "en") if obj else "Learning Concept"
            desc = _extract_localized_text(obj.get("description", {}), "en") if obj else None
            fb = create_fallback_instructional_content(
                objective_id=objective_id,
                objective_title=title,
                objective_description=desc,
                method=ExplanationMethod.STEP_BY_STEP,
                difficulty_level=1,
                language="en",
            )
            blocks = [
                InstructionalBlock(
                    id=b["id"],
                    block_type=ContentBlockType(b["block_type"]),
                    title=b.get("title"),
                    body=b.get("body", ""),
                    visual_cue=b.get("visual_cue"),
                    order_index=b.get("order_index", 1),
                    metadata=b.get("metadata", {}),
                )
                for b in fb["blocks"]
            ]
            now_dt = datetime.now(UTC)
            synth_id = uuid.uuid4()
            synth_obj = InstructionalContentRead(
                id=synth_id,
                objective_id=objective_id,
                title=fb["title"],
                explanation_method=ExplanationMethod.STEP_BY_STEP,
                difficulty_level=1,
                language="en",
                blocks=blocks,
                summary=fb["summary"],
                status=InstructionalStatus.APPROVED,
                created_at=now_dt,
                updated_at=now_dt,
            )
            self.contents[synth_id] = synth_obj
            return [synth_obj]
        return items

    async def update(
        self,
        content_id: uuid.UUID,
        update_in: InstructionalContentUpdate,
        current_user: User,
    ) -> InstructionalContentRead:
        item = await self.get_by_id(content_id)
        raw = item.model_dump()
        if update_in.title is not None:
            raw["title"] = update_in.title
        if update_in.summary is not None:
            raw["summary"] = update_in.summary
        if update_in.teacher_notes is not None:
            raw["teacher_notes"] = update_in.teacher_notes
        if update_in.blocks is not None:
            raw["blocks"] = [b.model_dump() for b in update_in.blocks]
        if update_in.status is not None:
            raw["status"] = update_in.status
        raw["updated_at"] = datetime.now(UTC)
        updated = InstructionalContentRead.model_validate(raw)
        self.contents[content_id] = updated
        return updated

    async def approve(self, content_id: uuid.UUID, current_user: User) -> InstructionalContentRead:
        item = await self.get_by_id(content_id)
        raw = item.model_dump()
        raw["status"] = InstructionalStatus.APPROVED
        raw["updated_at"] = datetime.now(UTC)
        updated = InstructionalContentRead.model_validate(raw)
        self.contents[content_id] = updated
        return updated

    async def publish(self, content_id: uuid.UUID, current_user: User) -> InstructionalContentRead:
        item = await self.get_by_id(content_id)
        raw = item.model_dump()
        raw["status"] = InstructionalStatus.PUBLISHED
        raw["updated_at"] = datetime.now(UTC)
        updated = InstructionalContentRead.model_validate(raw)
        self.contents[content_id] = updated
        return updated



# ── Research Mode Sandbox Mock Service ─────────────────────────────────────────

from app.research.models import (
    ResearchArtifact,
    ResearchEvaluation,
    ResearchExperiment,
    ResearchMetric,
    ResearchProject,
    ResearchRun,
    ResearchSnapshot,
    ResearchVariant,
)
from app.research.router import get_research_service
from app.research.schemas import (
    ArtifactPromotionRequest,
    ArtifactPromotionResponse,
    ExperimentComparisonResponse,
    ResearchEvaluationCreate,
    ResearchExperimentCreate,
    ResearchExperimentUpdate,
    ResearchGenerationRequest,
    ResearchMetricCreate,
    ResearchProjectCreate,
    ResearchProjectUpdate,
    ResearchSnapshotCreate,
    ResearchVariantCreate,
    ResearchVariantUpdate,
    RunCloneRequest,
    VariantCloneRequest,
    VariantComparisonItem,
)
from app.research.generation import ResearchGenerationService, get_research_generation_service


class MockResearchService:
    def __init__(self):
        self.projects: dict[uuid.UUID, ResearchProject] = {}
        self.experiments: dict[uuid.UUID, ResearchExperiment] = {}
        self.variants: dict[uuid.UUID, ResearchVariant] = {}
        self.runs: dict[uuid.UUID, ResearchRun] = {}
        self.artifacts: dict[uuid.UUID, ResearchArtifact] = {}
        self.metrics: dict[uuid.UUID, ResearchMetric] = {}
        self.evaluations: dict[uuid.UUID, ResearchEvaluation] = {}
        self.snapshots: dict[uuid.UUID, ResearchSnapshot] = {}
        self.gen_service = get_research_generation_service()
        self._init_demo_data()

    def _init_demo_data(self):
        proj_id = uuid.UUID("33333333-3333-3333-3333-333333333333")
        exp_id = uuid.UUID("44444444-4444-4444-4444-444444444444")
        var_a_id = uuid.UUID("55555555-5555-5555-5555-555555555555")
        var_b_id = uuid.UUID("66666666-6666-6666-6666-666666666666")
        run_id = uuid.UUID("88888888-8888-8888-8888-888888888888")
        art_id = uuid.UUID("99999999-9999-9999-9999-999999999999")
        met1_id = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        met2_id = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
        eval_id = uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")

        now_dt = datetime.now(UTC)

        proj = ResearchProject(
            id=proj_id,
            name="Multi-Modal Pedagogical Strategies",
            description="Sandbox investigation into multi-modal scaffolds vs text-only explanations.",
            research_question="Does visual cueing combined with step-by-step guidance increase conceptual comprehension compared to text-only explanations?",
            hypothesis="Learners exposed to multi-modal visual steps will demonstrate higher accuracy.",
            owner_id=researcher_id,
            status="active",
            metadata_info={"domain": "special_education", "phase": "pilot"},
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.projects[proj_id] = proj

        exp = ResearchExperiment(
            id=exp_id,
            project_id=proj_id,
            name="Visual vs Text Scaffolding in Early Literacy",
            description="Comparing 5-question multi-modal activities against homogeneous text activities.",
            research_question="How does visual cue placement affect distraction vs engagement?",
            hypothesis="Embedded visual icons reduce question completion time by 20%.",
            status="active",
            metadata_info={},
            created_at=now_dt,
            updated_at=now_dt,
        )
        exp.project = proj
        self.experiments[exp_id] = exp

        var_a = ResearchVariant(
            id=var_a_id,
            experiment_id=exp_id,
            name="Variant A: Visual Scaffolding (5 Questions)",
            description="Includes visual icon cues, step-by-step breakdown, and pictorial choices.",
            configuration={
                "model": "gemini-3.8-flash",
                "temperature": 0.3,
                "scaffolding_style": "visual_assisted",
                "question_count": 5,
            },
            metadata_info={},
            created_at=now_dt,
            updated_at=now_dt,
        )
        var_a.experiment = exp
        self.variants[var_a_id] = var_a

        var_b = ResearchVariant(
            id=var_b_id,
            experiment_id=exp_id,
            name="Variant B: Text-Only Scaffolding (5 Questions)",
            description="Pure text explanations without visual cues.",
            configuration={
                "model": "gemini-3.8-flash",
                "temperature": 0.7,
                "scaffolding_style": "text_only",
                "question_count": 5,
            },
            parent_variant_id=var_a_id,
            metadata_info={"cloned_from": "Variant A"},
            created_at=now_dt,
            updated_at=now_dt,
        )
        var_b.experiment = exp
        self.variants[var_b_id] = var_b

        metric_clarity = ResearchMetric(
            id=met1_id,
            experiment_id=exp_id,
            name="Instructional Clarity",
            description="Clarity and readability of explanatory text (1-5 scale).",
            metric_type="rating",
            configuration={"min": 1, "max": 5},
            created_at=now_dt,
            updated_at=now_dt,
        )
        metric_cognitive = ResearchMetric(
            id=met2_id,
            experiment_id=exp_id,
            name="Cognitive Load Estimate",
            description="Perceived visual complexity and prompt length.",
            metric_type="rating",
            configuration={"min": 1, "max": 5},
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.metrics[met1_id] = metric_clarity
        self.metrics[met2_id] = metric_cognitive

        raw_payload = {
            "assessment_title": "Visual Phonemic Scaffolding",
            "question_count": 5,
            "items": [
                {
                    "id": "q1",
                    "prompt": "Which item starts with the /b/ sound?",
                    "visual_cue": "image_bell",
                    "choices": ["Bell", "Cat", "Sun"],
                    "answer": "Bell",
                },
                {
                    "id": "q2",
                    "prompt": "Identify the word that has 2 syllables.",
                    "visual_cue": "image_robot",
                    "choices": ["Ro-bot", "Dog", "Fish"],
                    "answer": "Ro-bot",
                },
            ],
        }
        raw_text = json.dumps(raw_payload, indent=2)

        sample_run = ResearchRun(
            id=run_id,
            variant_id=var_a_id,
            model="gemini-3.8-flash",
            model_configuration={"temperature": 0.3, "max_output_tokens": 2048},
            system_prompt="You are an educational researcher evaluating visual scaffolding.",
            user_prompt="Generate 5 phonemic awareness questions pairing sound with visual cues.",
            status="completed",
            started_at=now_dt,
            completed_at=now_dt,
            raw_output=raw_text,
            normalized_output=raw_payload,
            metadata_info={"execution_time_ms": 320.5},
            created_at=now_dt,
            updated_at=now_dt,
        )
        sample_run.variant = var_a
        self.runs[run_id] = sample_run

        sample_artifact = ResearchArtifact(
            id=art_id,
            run_id=run_id,
            artifact_type="assessment",
            schema_version="1.0",
            payload=raw_payload,
            raw_text=raw_text,
            is_production_compatible=False,
            promoted_to_production=False,
            metadata_info={"execution_time_ms": 320.5},
            created_at=now_dt,
            updated_at=now_dt,
        )
        sample_artifact.run = sample_run
        sample_run.artifact = sample_artifact
        var_a.runs = [sample_run]
        self.artifacts[art_id] = sample_artifact

        sample_eval = ResearchEvaluation(
            id=eval_id,
            artifact_id=art_id,
            metric_id=met1_id,
            metric_name="Instructional Clarity",
            value={"score": 5, "max": 5},
            evaluator_type="manual",
            evaluator_id=researcher_id,
            notes="Excellent visual alignment and distinct sound associations.",
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.evaluations[eval_id] = sample_eval
        sample_artifact.evaluations = [sample_eval]

    def _check_owner(self, user: User, owner_id: uuid.UUID) -> None:
        if user.role != UserRole.admin and user.id != owner_id:
            from app.core.errors import AuthorizationError
            raise AuthorizationError("Access denied: You do not own this research project.")

    async def list_projects(self, user: User) -> list[ResearchProject]:
        if user.role == UserRole.admin:
            return list(self.projects.values())
        return [p for p in self.projects.values() if p.owner_id == user.id]

    async def create_project(self, user: User, data: ResearchProjectCreate) -> ResearchProject:
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        proj = ResearchProject(
            id=new_id,
            name=data.name,
            description=data.description,
            research_question=data.research_question,
            hypothesis=data.hypothesis,
            owner_id=user.id,
            status=data.status,
            metadata_info=data.metadata_info,
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.projects[new_id] = proj
        return proj

    async def get_project(self, user: User, project_id: uuid.UUID) -> ResearchProject:
        from app.core.errors import NotFoundError
        proj = self.projects.get(project_id)
        if not proj:
            raise NotFoundError(f"Research project {project_id} not found.")
        self._check_owner(user, proj.owner_id)
        return proj

    async def update_project(self, user: User, project_id: uuid.UUID, data: ResearchProjectUpdate) -> ResearchProject:
        proj = await self.get_project(user, project_id)
        if data.name is not None:
            proj.name = data.name
        if data.description is not None:
            proj.description = data.description
        if data.research_question is not None:
            proj.research_question = data.research_question
        if data.hypothesis is not None:
            proj.hypothesis = data.hypothesis
        if data.status is not None:
            proj.status = data.status
        proj.updated_at = datetime.now(UTC)
        return proj

    async def delete_project(self, user: User, project_id: uuid.UUID) -> bool:
        await self.get_project(user, project_id)
        self.projects.pop(project_id, None)
        return True

    async def list_experiments(self, user: User, project_id: uuid.UUID) -> list[ResearchExperiment]:
        await self.get_project(user, project_id)
        return [e for e in self.experiments.values() if e.project_id == project_id]

    async def create_experiment(self, user: User, project_id: uuid.UUID, data: ResearchExperimentCreate) -> ResearchExperiment:
        proj = await self.get_project(user, project_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        exp = ResearchExperiment(
            id=new_id,
            project_id=proj.id,
            name=data.name,
            description=data.description,
            research_question=data.research_question,
            hypothesis=data.hypothesis,
            status=data.status,
            metadata_info=data.metadata_info,
            created_at=now_dt,
            updated_at=now_dt,
        )
        exp.project = proj
        self.experiments[new_id] = exp
        return exp

    async def get_experiment(self, user: User, experiment_id: uuid.UUID) -> ResearchExperiment:
        from app.core.errors import NotFoundError
        exp = self.experiments.get(experiment_id)
        if not exp:
            raise NotFoundError(f"Research experiment {experiment_id} not found.")
        proj = self.projects.get(exp.project_id)
        if proj:
            self._check_owner(user, proj.owner_id)
        return exp

    async def update_experiment(self, user: User, experiment_id: uuid.UUID, data: ResearchExperimentUpdate) -> ResearchExperiment:
        exp = await self.get_experiment(user, experiment_id)
        if data.name is not None:
            exp.name = data.name
        if data.description is not None:
            exp.description = data.description
        if data.research_question is not None:
            exp.research_question = data.research_question
        if data.hypothesis is not None:
            exp.hypothesis = data.hypothesis
        if data.status is not None:
            exp.status = data.status
        exp.updated_at = datetime.now(UTC)
        return exp

    async def delete_experiment(self, user: User, experiment_id: uuid.UUID) -> bool:
        await self.get_experiment(user, experiment_id)
        self.experiments.pop(experiment_id, None)
        return True

    async def list_variants(self, user: User, experiment_id: uuid.UUID) -> list[ResearchVariant]:
        await self.get_experiment(user, experiment_id)
        return [v for v in self.variants.values() if v.experiment_id == experiment_id]

    async def create_variant(self, user: User, experiment_id: uuid.UUID, data: ResearchVariantCreate) -> ResearchVariant:
        exp = await self.get_experiment(user, experiment_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        var = ResearchVariant(
            id=new_id,
            experiment_id=exp.id,
            name=data.name,
            description=data.description,
            configuration=data.configuration,
            parent_variant_id=data.parent_variant_id,
            metadata_info=data.metadata_info,
            created_at=now_dt,
            updated_at=now_dt,
        )
        var.experiment = exp
        self.variants[new_id] = var
        return var

    async def get_variant(self, user: User, variant_id: uuid.UUID) -> ResearchVariant:
        from app.core.errors import NotFoundError
        var = self.variants.get(variant_id)
        if not var:
            raise NotFoundError(f"Research variant {variant_id} not found.")
        exp = self.experiments.get(var.experiment_id)
        if exp:
            proj = self.projects.get(exp.project_id)
            if proj:
                self._check_owner(user, proj.owner_id)
        return var

    async def update_variant(self, user: User, variant_id: uuid.UUID, data: ResearchVariantUpdate) -> ResearchVariant:
        var = await self.get_variant(user, variant_id)
        if data.name is not None:
            var.name = data.name
        if data.description is not None:
            var.description = data.description
        if data.configuration is not None:
            var.configuration = data.configuration
        var.updated_at = datetime.now(UTC)
        return var

    async def clone_variant(self, user: User, variant_id: uuid.UUID, req: VariantCloneRequest) -> ResearchVariant:
        original = await self.get_variant(user, variant_id)
        cloned_config = dict(original.configuration)
        if req.override_configuration:
            cloned_config.update(req.override_configuration)
        new_name = req.new_name or f"{original.name} (Clone)"
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        cloned = ResearchVariant(
            id=new_id,
            experiment_id=original.experiment_id,
            name=new_name,
            description=f"Cloned from {original.name}",
            configuration=cloned_config,
            parent_variant_id=original.id,
            metadata_info={"cloned_from": str(original.id)},
            created_at=now_dt,
            updated_at=now_dt,
        )
        cloned.experiment = original.experiment
        self.variants[new_id] = cloned
        return cloned

    async def execute_run(self, user: User, req: ResearchGenerationRequest) -> ResearchRun:
        variant = await self.get_variant(user, req.variant_id)
        now_dt = datetime.now(UTC)
        run_id = uuid.uuid4()

        # Execute generation through isolated ResearchGenerationService
        gen_result = await self.gen_service.execute_generation(
            prompt=req.prompt,
            system_prompt=req.system_prompt,
            model=req.model,
            model_configuration=req.model_configuration,
            explicit_context=req.explicit_context,
            output_target=req.output_target,
            production_compatibility_mode=req.production_compatibility_mode,
            target_production_schema=req.target_production_schema,
            question_count=req.question_count,
        )

        run = ResearchRun(
            id=run_id,
            variant_id=variant.id,
            model=req.model,
            model_configuration=req.model_configuration,
            system_prompt=req.system_prompt,
            user_prompt=req.prompt,
            input_snapshot={
                "explicit_context": req.explicit_context,
                "output_target": req.output_target,
                "production_compatibility_mode": req.production_compatibility_mode,
                "question_count": req.question_count,
                "project_id": str(req.project_id),
                "experiment_id": str(req.experiment_id),
                "variant_id": str(req.variant_id),
            },
            status=gen_result.get("status", "completed"),
            started_at=now_dt,
            completed_at=datetime.now(UTC),
            raw_output=gen_result.get("raw_output"),
            normalized_output=gen_result.get("normalized_output"),
            error=gen_result.get("error"),
            metadata_info={"execution_time_ms": gen_result.get("execution_time_ms")},
            created_at=now_dt,
            updated_at=now_dt,
        )
        run.variant = variant
        self.runs[run_id] = run
        variant.runs.append(run)

        # Invariant: 1:1 maximum cardinality. Failed runs create zero artifacts.
        if run.status in ("completed", "completed_with_parse_warning") and run.normalized_output:
            art_id = uuid.uuid4()
            artifact = ResearchArtifact(
                id=art_id,
                run_id=run.id,
                artifact_type=req.output_target,
                schema_version="1.0",
                payload=run.normalized_output,
                raw_text=run.raw_output,
                is_production_compatible=gen_result.get("is_production_compatible", False),
                compatibility_validation=gen_result.get("compatibility_validation"),
                metadata_info={"execution_time_ms": gen_result.get("execution_time_ms")},
                created_at=now_dt,
                updated_at=now_dt,
            )
            artifact.run = run
            run.artifact = artifact
            self.artifacts[art_id] = artifact

        return run

    async def get_run(self, user: User, run_id: uuid.UUID) -> ResearchRun:
        from app.core.errors import NotFoundError
        run = self.runs.get(run_id)
        if not run:
            raise NotFoundError(f"Research run {run_id} not found.")
        return run

    async def clone_run(self, user: User, run_id: uuid.UUID, req: RunCloneRequest) -> ResearchRun:
        orig = await self.get_run(user, run_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        new_prompt = req.override_user_prompt or orig.user_prompt
        new_sys = req.override_system_prompt or orig.system_prompt
        new_cfg = dict(orig.model_configuration)
        if req.override_model_configuration:
            new_cfg.update(req.override_model_configuration)
        cloned = ResearchRun(
            id=new_id,
            variant_id=orig.variant_id,
            model=orig.model,
            model_configuration=new_cfg,
            system_prompt=new_sys,
            user_prompt=new_prompt,
            input_snapshot=orig.input_snapshot,
            status="draft",
            parent_run_id=orig.id,
            metadata_info={"cloned_from": str(orig.id)},
            created_at=now_dt,
            updated_at=now_dt,
        )
        cloned.variant = orig.variant
        self.runs[new_id] = cloned
        return cloned

    async def get_artifact(self, user: User, artifact_id: uuid.UUID) -> ResearchArtifact:
        from app.core.errors import NotFoundError
        art = self.artifacts.get(artifact_id)
        if not art:
            raise NotFoundError(f"Research artifact {artifact_id} not found.")
        return art

    async def export_artifact(self, user: User, artifact_id: uuid.UUID, export_format: str = "json") -> dict[str, Any]:
        art = await self.get_artifact(user, artifact_id)
        if export_format.lower() == "markdown":
            md_lines = [
                f"# Research Artifact: {art.artifact_type}",
                f"- **Artifact ID:** {art.id}",
                f"- **Run ID:** {art.run_id}",
                f"- **Production Compatible:** {art.is_production_compatible}",
                f"- **Created At:** {art.created_at.isoformat()}",
                "",
                "## Payload",
                "```json",
                json.dumps(art.payload, indent=2),
                "```",
                "",
                "## Raw Output",
                "```",
                art.raw_text or "",
                "```",
            ]
            return {"format": "markdown", "content": "\n".join(md_lines), "filename": f"artifact_{art.id}.md"}

        return {
            "format": "json",
            "content": {
                "id": str(art.id),
                "run_id": str(art.run_id),
                "artifact_type": art.artifact_type,
                "is_production_compatible": art.is_production_compatible,
                "compatibility_validation": art.compatibility_validation,
                "payload": art.payload,
                "raw_text": art.raw_text,
                "created_at": art.created_at.isoformat(),
            },
            "filename": f"artifact_{art.id}.json",
        }

    async def promote_artifact(self, user: User, artifact_id: uuid.UUID, req: ArtifactPromotionRequest) -> ArtifactPromotionResponse:
        from app.core.errors import AuthorizationError, ValidationError
        if user.role != UserRole.admin:
            raise AuthorizationError("Only administrators can promote research artifacts to production.")
        art = await self.get_artifact(user, artifact_id)
        if not art.is_production_compatible:
            raise ValidationError("Artifact is not marked as production-compatible.")
        promoted_uuid = uuid.uuid4()
        art.promoted_to_production = True
        art.production_entity_id = promoted_uuid
        return ArtifactPromotionResponse(
            success=True,
            promoted_entity_id=promoted_uuid,
            destination=req.target_destination,
            message=f"Artifact promoted to Production Draft ({req.target_destination}) with ID {promoted_uuid}.",
        )

    async def create_metric(self, user: User, experiment_id: uuid.UUID, data: ResearchMetricCreate) -> ResearchMetric:
        exp = await self.get_experiment(user, experiment_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        metric = ResearchMetric(
            id=new_id,
            experiment_id=exp.id,
            name=data.name,
            description=data.description,
            metric_type=data.metric_type,
            configuration=data.configuration,
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.metrics[new_id] = metric
        return metric

    async def list_metrics(self, user: User, experiment_id: uuid.UUID) -> list[ResearchMetric]:
        await self.get_experiment(user, experiment_id)
        return [m for m in self.metrics.values() if m.experiment_id == experiment_id]

    async def create_evaluation(self, user: User, artifact_id: uuid.UUID, data: ResearchEvaluationCreate) -> ResearchEvaluation:
        art = await self.get_artifact(user, artifact_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        ev = ResearchEvaluation(
            id=new_id,
            artifact_id=art.id,
            metric_id=data.metric_id,
            metric_name=data.metric_name,
            value=data.value,
            evaluator_type=data.evaluator_type,
            evaluator_id=user.id,
            notes=data.notes,
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.evaluations[new_id] = ev
        return ev

    async def list_evaluations(self, user: User, artifact_id: uuid.UUID) -> list[ResearchEvaluation]:
        await self.get_artifact(user, artifact_id)
        return [e for e in self.evaluations.values() if e.artifact_id == artifact_id]

    async def get_experiment_comparison(self, user: User, experiment_id: uuid.UUID) -> ExperimentComparisonResponse:
        exp = await self.get_experiment(user, experiment_id)
        metrics = await self.list_metrics(user, experiment_id)
        variants = await self.list_variants(user, experiment_id)

        comparison_items = []
        for var in variants:
            var_runs = [r for r in self.runs.values() if r.variant_id == var.id]
            latest_run = var_runs[-1] if var_runs else None
            artifact = latest_run.artifact if latest_run else None
            evals = [e for e in self.evaluations.values() if artifact and e.artifact_id == artifact.id]
            comparison_items.append(
                VariantComparisonItem(
                    variant=var,
                    latest_run=latest_run,
                    artifact=artifact,
                    evaluations=evals,
                )
            )

        return ExperimentComparisonResponse(
            experiment_id=exp.id,
            experiment_name=exp.name,
            project_id=exp.project_id,
            metrics=metrics,
            variants=comparison_items,
        )

    async def create_snapshot(self, user: User, project_id: uuid.UUID, data: ResearchSnapshotCreate) -> ResearchSnapshot:
        proj = await self.get_project(user, project_id)
        now_dt = datetime.now(UTC)
        new_id = uuid.uuid4()
        snap = ResearchSnapshot(
            id=new_id,
            project_id=proj.id,
            source_type=data.source_type,
            source_reference=data.source_reference,
            snapshot_version=data.snapshot_version,
            snapshot_data=data.snapshot_data,
            created_at=now_dt,
            updated_at=now_dt,
        )
        self.snapshots[new_id] = snap
        return snap

    async def list_snapshots(self, user: User, project_id: uuid.UUID) -> list[ResearchSnapshot]:
        await self.get_project(user, project_id)
        return [s for s in self.snapshots.values() if s.project_id == project_id]


_MOCK_CURRICULUM_INSTANCE = MockCurriculumService()
_MOCK_LEARNER_INSTANCE = MockLearnerService()
_MOCK_ACTIVITY_INSTANCE = MockActivityService()
_MOCK_INSTRUCTIONAL_INSTANCE = MockInstructionalService()
_MOCK_RESEARCH_INSTANCE = MockResearchService()

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_curriculum_service] = lambda: _MOCK_CURRICULUM_INSTANCE
app.dependency_overrides[get_learner_service] = lambda: _MOCK_LEARNER_INSTANCE
app.dependency_overrides[get_activity_service] = lambda: _MOCK_ACTIVITY_INSTANCE
app.dependency_overrides[get_instructional_service] = lambda: _MOCK_INSTRUCTIONAL_INSTANCE
app.dependency_overrides[get_analytics_service] = lambda: _MOCK_ANALYTICS_INSTANCE
app.dependency_overrides[get_recommendation_service] = lambda: _MOCK_RECOMMENDATION_INSTANCE
app.dependency_overrides[get_teacher_dashboard_service] = lambda: _MOCK_TEACHER_DASHBOARD_INSTANCE
app.dependency_overrides[get_research_service] = lambda: _MOCK_RESEARCH_INSTANCE

# Patch UserService where imported
patch("app.auth.router.UserService", return_value=MockUserService()).start()
patch("app.users.router.UserService", return_value=MockUserService()).start()
patch("app.auth.dependencies.UserService", return_value=MockUserService()).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

