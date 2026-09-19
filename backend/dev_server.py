"""
Eduvia — Development Live Server with In-Memory Demo Fixtures

Enables live end-to-end UI verification (frontend <-> backend <-> browser)
when running in environments without an active Docker / PostgreSQL daemon.
Provides exact demonstration entities matching seed_demo_data.py.
"""
from __future__ import annotations

import os
import sys
import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, patch

import uvicorn

# Ensure backend directory is in sys.path so 'app' can always be resolved
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app.activities.fallbacks import create_fallback_activity
from app.activities.router import get_activity_service
from app.activities.schemas import (
    Activity,
    ActivityEvaluationResponse,
    ActivityGenerateRequest,
    ActivityGenerateResponse,
    ActivitySubmissionRequest,
    ActivityType,
)
from app.activities.service import ActivityService
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

# Demo Curriculum Tree matching seed_demo_data.py
curr_id = uuid.UUID("33333333-3333-3333-3333-333333333333")
subj_id = uuid.UUID("44444444-4444-4444-4444-444444444444")
unit_id = uuid.UUID("55555555-5555-5555-5555-555555555555")
less_id = uuid.UUID("66666666-6666-6666-6666-666666666666")
obj1_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
obj2_id = uuid.UUID("88888888-8888-8888-8888-888888888888")

obj1_dict: dict[str, Any] = {
    "id": obj1_id,
    "lesson_id": less_id,
    "title": {"en": "Recognize numbers 1–5", "ar": "التعرف على الأرقام ١-٥"},
    "description": {
        "en": "Identify written numerals 1 to 5 and match to dot patterns.",
        "ar": "التعرف على الأرقام المكتوبة من ١ إلى ٥ ومطابقتها مع أنماط النقاط.",
    },
    "difficulty_level": 1,
    "assessment_criteria": {"minimum_accuracy": 0.8, "maximum_assistance_level": 2},
    "order_index": 1,
    "is_active": True,
    "prerequisites": [],
}

obj2_dict: dict[str, Any] = {
    "id": obj2_id,
    "lesson_id": less_id,
    "title": {"en": "Recognize numbers 6–10", "ar": "التعرف على الأرقام ٦-١٠"},
    "description": {
        "en": "Identify written numerals 6 to 10 and order them progressively.",
        "ar": "التعرف على الأرقام المكتوبة من ٦ إلى ١٠ وترتيبها تدريجياً.",
    },
    "difficulty_level": 2,
    "assessment_criteria": {"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
    "order_index": 2,
    "is_active": True,
    "prerequisites": [obj1_dict],
}

lesson_dict: dict[str, Any] = {
    "id": less_id,
    "unit_id": unit_id,
    "title": {"en": "Number Recognition 1–10", "ar": "التعرف على الأرقام من ١ إلى ١٠"},
    "description": {"en": "Identifying digits visually and mapping them to quantities.", "ar": "التعرف البصري على الأرقام وربطها بالكميات."},
    "order_index": 1,
    "learning_objectives": [obj1_dict, obj2_dict],
}

unit_dict: dict[str, Any] = {
    "id": unit_id,
    "subject_id": subj_id,
    "title": {"en": "Number Sense & Counting", "ar": "الحس العددي والعد"},
    "description": {"en": "Understanding discrete quantities and numerical representations.", "ar": "فهم الكميات المنفصلة والتمثيلات العددية."},
    "order_index": 1,
    "lessons": [lesson_dict],
}

subject_dict: dict[str, Any] = {
    "id": subj_id,
    "curriculum_id": curr_id,
    "title": {"en": "Foundational Mathematics", "ar": "أساسيات الرياضيات"},
    "description": {"en": "Basic mathematical reasoning, pattern recognition, and number sense.", "ar": "التفكير الرياضي الأساسي، التعرف على الأنماط، والحس العددي."},
    "order_index": 1,
    "units": [unit_dict],
}

curriculum_full_dict: dict[str, Any] = {
    "id": curr_id,
    "title": {"en": "Eduvia Demonstration Curriculum", "ar": "منهج إدوفيا التجريبي"},
    "description": {"en": "A standardized demonstration curriculum for inclusive numeracy.", "ar": "منهج تجريبي معياري لتطوير مهارات الحساب الشاملة."},
    "version": "demo-1.0",
    "is_active": True,
    "created_by_id": admin_id,
    "subjects": [subject_dict],
}

curriculum_summary_dict: dict[str, Any] = {
    "id": curr_id,
    "title": curriculum_full_dict["title"],
    "description": curriculum_full_dict["description"],
    "version": curriculum_full_dict["version"],
    "is_active": True,
    "created_by_id": admin_id,
}


class MockUserService:
    async def get_by_email(self, email: str) -> User | None:
        if email == "teacher@eduvia.app":
            return demo_teacher
        if email == "admin@eduvia.app":
            return demo_admin
        return None

    async def get_by_id(self, uid: uuid.UUID) -> User | None:
        if uid == teacher_id:
            return demo_teacher
        if uid == admin_id:
            return demo_admin
        return None


class MockCurriculumService:
    async def get_all(self) -> list[dict[str, Any]]:
        return [curriculum_summary_dict]

    async def get_by_id(self, cid: uuid.UUID) -> dict[str, Any] | None:
        if cid == curr_id:
            return curriculum_full_dict
        return None

    async def get_subject(self, sid: uuid.UUID) -> dict[str, Any] | None:
        if sid == subj_id:
            return subject_dict
        return None

    async def get_unit(self, uid: uuid.UUID) -> dict[str, Any] | None:
        if uid == unit_id:
            return unit_dict
        return None

    async def get_lesson(self, lid: uuid.UUID) -> dict[str, Any] | None:
        if lid == less_id:
            return lesson_dict
        return None

    async def get_learning_objective(self, oid: uuid.UUID) -> dict[str, Any] | None:
        if oid == obj1_id:
            return obj1_dict
        if oid == obj2_id:
            return obj2_dict
        return None


# Demo Learner fixture matching seed_demo_data.py
demo_learner_id = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
demo_learner = Learner(
    id=demo_learner_id,
    name="Tariq Al-Mansoor",
    age_group="primary",
    learning_level="beginner",
    is_active=True,
    teacher_id=teacher_id,
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

in_memory_learners: dict[uuid.UUID, Learner] = {demo_learner_id: demo_learner}


class MockLearnerService:
    async def list_learners(
        self, teacher_id: uuid.UUID | None, is_admin: bool = False
    ) -> list[Learner]:
        if is_admin:
            return list(in_memory_learners.values())
        return [learner for learner in in_memory_learners.values() if learner.teacher_id == teacher_id]

    async def get_by_id(
        self,
        learner_id: uuid.UUID,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
    ) -> Learner | None:
        learner = in_memory_learners.get(learner_id)
        if not learner:
            return None
        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
            return None
        return learner

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
    ) -> Learner | None:
        learner = in_memory_learners.get(learner_id)
        if not learner:
            return None
        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
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
    ) -> bool:
        learner = in_memory_learners.get(learner_id)
        if not learner:
            return False
        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
            return False
        del in_memory_learners[learner_id]
        return True

    async def add_observation(
        self,
        learner_id: uuid.UUID,
        observation: LearnerObservationCreate,
        teacher_id: uuid.UUID | None = None,
        is_admin: bool = False,
    ) -> dict[str, Any] | None:
        learner = in_memory_learners.get(learner_id)
        if not learner or not learner.profile:
            return None
        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
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

    async def generate_activity(
        self,
        request: ActivityGenerateRequest,
        current_user: User | None = None,
    ) -> ActivityGenerateResponse:
        oid = request.objective_id
        obj: dict[str, Any] | None = None
        if oid == obj1_id:
            obj = obj1_dict
        elif oid == obj2_id:
            obj = obj2_dict

        title = "Numeracy Practice"
        desc = "Foundational practice."
        diff = 1

        if obj:
            title_dict = obj.get("title")
            if isinstance(title_dict, dict):
                title = str(title_dict.get("en", "Demo Objective"))
            desc_dict = obj.get("description")
            if isinstance(desc_dict, dict):
                desc = str(desc_dict.get("en", "Practice counting"))
            diff = int(obj.get("difficulty_level", 1))

        if request.difficulty_level is not None:
            diff = request.difficulty_level

        act_type = request.activity_type or ActivityType.MULTIPLE_CHOICE

        activity = create_fallback_activity(
            objective_id=oid,
            objective_title=title,
            objective_description=desc,
            difficulty_level=diff,
            activity_type=act_type,
            language=request.language,
        )
        self.activities[activity.id] = activity

        return ActivityGenerateResponse(
            activity=activity,
            fallback_used=True,
            generation_source="dev_mock_engine",
            learner_id=request.learner_id,
            objective_id=oid,
        )

    async def get_activity(self, activity_id: uuid.UUID) -> Activity | None:
        return self.activities.get(activity_id)

    async def evaluate_submission(
        self,
        request: ActivitySubmissionRequest,
    ) -> ActivityEvaluationResponse:
        if request.activity_content is None and request.activity_id in self.activities:
            request = request.model_copy(
                update={"activity_content": self.activities[request.activity_id].content}
            )
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
        completed = sum(1 for e in matching if e.completed)
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

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_curriculum_service] = lambda: MockCurriculumService()
app.dependency_overrides[get_learner_service] = lambda: MockLearnerService()
app.dependency_overrides[get_activity_service] = lambda: MockActivityService()
app.dependency_overrides[get_analytics_service] = lambda: _MOCK_ANALYTICS_INSTANCE
app.dependency_overrides[get_recommendation_service] = lambda: _MOCK_RECOMMENDATION_INSTANCE

# Patch UserService where imported
patch("app.auth.router.UserService", return_value=MockUserService()).start()
patch("app.users.router.UserService", return_value=MockUserService()).start()
patch("app.auth.dependencies.UserService", return_value=MockUserService()).start()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

