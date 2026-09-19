"""
Eduvia — Development Live Server with In-Memory Demo Fixtures

Enables live end-to-end UI verification (frontend <-> backend <-> browser)
when running in environments without an active Docker / PostgreSQL daemon.
Provides exact demonstration entities matching seed_demo_data.py.
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.main import app
from app.auth.security import get_password_hash
from app.users.models import User, UserRole
from app.database.session import get_db_session
from app.curriculum.router import get_curriculum_service

now = datetime.now(timezone.utc)
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

obj1_dict = {
    "id": obj1_id,
    "lesson_id": less_id,
    "title": {"en": "Recognize numbers 1–5", "ar": "التعرف على الأرقام ١-٥"},
    "description": {"en": "Identify written numerals 1 to 5 and match to dot patterns.", "ar": "التعرف على الأرقام المكتوبة من ١ إلى ٥ ومطابقتها مع أنماط النقاط."},
    "difficulty_level": 1,
    "assessment_criteria": {"minimum_accuracy": 0.8, "maximum_assistance_level": 2},
    "order_index": 1,
    "is_active": True,
    "prerequisites": [],
}

obj2_dict = {
    "id": obj2_id,
    "lesson_id": less_id,
    "title": {"en": "Recognize numbers 6–10", "ar": "التعرف على الأرقام ٦-١٠"},
    "description": {"en": "Identify written numerals 6 to 10 and order them progressively.", "ar": "التعرف على الأرقام المكتوبة من ٦ إلى ١٠ وترتيبها تدريجياً."},
    "difficulty_level": 2,
    "assessment_criteria": {"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
    "order_index": 2,
    "is_active": True,
    "prerequisites": [obj1_dict],
}

lesson_dict = {
    "id": less_id,
    "unit_id": unit_id,
    "title": {"en": "Number Recognition 1–10", "ar": "التعرف على الأرقام من ١ إلى ١٠"},
    "description": {"en": "Identifying digits visually and mapping them to quantities.", "ar": "التعرف البصري على الأرقام وربطها بالكميات."},
    "order_index": 1,
    "learning_objectives": [obj1_dict, obj2_dict],
}

unit_dict = {
    "id": unit_id,
    "subject_id": subj_id,
    "title": {"en": "Number Sense & Counting", "ar": "الحس العددي والعد"},
    "description": {"en": "Understanding discrete quantities and numerical representations.", "ar": "فهم الكميات المنفصلة والتمثيلات العددية."},
    "order_index": 1,
    "lessons": [lesson_dict],
}

subject_dict = {
    "id": subj_id,
    "curriculum_id": curr_id,
    "title": {"en": "Foundational Mathematics", "ar": "أساسيات الرياضيات"},
    "description": {"en": "Basic mathematical reasoning, pattern recognition, and number sense.", "ar": "التفكير الرياضي الأساسي، التعرف على الأنماط، والحس العددي."},
    "order_index": 1,
    "units": [unit_dict],
}

curriculum_full_dict = {
    "id": curr_id,
    "title": {"en": "Eduvia Demonstration Curriculum", "ar": "منهج إدوفيا التجريبي"},
    "description": {"en": "A standardized demonstration curriculum for inclusive numeracy.", "ar": "منهج تجريبي معياري لتطوير مهارات الحساب الشاملة."},
    "version": "demo-1.0",
    "is_active": True,
    "created_by_id": admin_id,
    "subjects": [subject_dict],
}

curriculum_summary_dict = {
    "id": curr_id,
    "title": curriculum_full_dict["title"],
    "description": curriculum_full_dict["description"],
    "version": curriculum_full_dict["version"],
    "is_active": True,
    "created_by_id": admin_id,
}


class MockUserService:
    async def get_by_email(self, email: str):
        if email == "teacher@eduvia.app":
            return demo_teacher
        if email == "admin@eduvia.app":
            return demo_admin
        return None

    async def get_by_id(self, uid: uuid.UUID):
        if uid == teacher_id:
            return demo_teacher
        if uid == admin_id:
            return demo_admin
        return None


class MockCurriculumService:
    async def get_all(self):
        return [curriculum_summary_dict]

    async def get_by_id(self, cid: uuid.UUID):
        if cid == curr_id:
            return curriculum_full_dict
        return None

    async def get_subject(self, sid: uuid.UUID):
        if sid == subj_id:
            return subject_dict
        return None

    async def get_unit(self, uid: uuid.UUID):
        if uid == unit_id:
            return unit_dict
        return None

    async def get_lesson(self, lid: uuid.UUID):
        if lid == less_id:
            return lesson_dict
        return None

    async def get_learning_objective(self, oid: uuid.UUID):
        if oid == obj1_id:
            return obj1_dict
        if oid == obj2_id:
            return obj2_dict
        return None


from app.learners.models import Learner, LearnerProfile
from app.learners.router import get_learner_service

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

in_memory_learners = {demo_learner_id: demo_learner}


class MockLearnerService:
    async def list_learners(self, teacher_id: uuid.UUID | None, is_admin: bool = False):
        if is_admin:
            return list(in_memory_learners.values())
        return [l for l in in_memory_learners.values() if l.teacher_id == teacher_id]

    async def get_by_id(self, learner_id: uuid.UUID, teacher_id: uuid.UUID | None = None, is_admin: bool = False):
        l = in_memory_learners.get(learner_id)
        if not l:
            return None
        if not is_admin and teacher_id is not None and l.teacher_id != teacher_id:
            return None
        return l

    async def create(self, data, teacher_id: uuid.UUID | None):
        new_id = uuid.uuid4()
        l = Learner(
            id=new_id,
            name=data.name,
            age_group=data.age_group,
            learning_level=data.learning_level,
            teacher_id=teacher_id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        p = LearnerProfile(
            id=uuid.uuid4(),
            learner_id=new_id,
            learner=l,
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
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        l.profile = p
        in_memory_learners[new_id] = l
        return l

    async def update(self, learner_id: uuid.UUID, data, teacher_id: uuid.UUID | None = None, is_admin: bool = False):
        l = in_memory_learners.get(learner_id)
        if not l:
            return None
        if not is_admin and teacher_id is not None and l.teacher_id != teacher_id:
            return None
        if data.name is not None:
            l.name = data.name
        if data.learning_level is not None:
            l.learning_level = data.learning_level
        if data.age_group is not None:
            l.age_group = data.age_group
        if data.profile and l.profile:
            p = l.profile
            if data.profile.teacher_notes is not None:
                p.teacher_notes = data.profile.teacher_notes
            if data.profile.support_requirements is not None:
                p.support_requirements = data.profile.support_requirements
            if data.profile.teacher_constraints is not None:
                p.teacher_constraints = data.profile.teacher_constraints
            if data.profile.teacher_overrides is not None:
                p.teacher_overrides = data.profile.teacher_overrides
        l.updated_at = datetime.now(timezone.utc)
        return l

    async def delete(self, learner_id: uuid.UUID, teacher_id: uuid.UUID | None = None, is_admin: bool = False):
        l = in_memory_learners.get(learner_id)
        if not l:
            return False
        if not is_admin and teacher_id is not None and l.teacher_id != teacher_id:
            return False
        del in_memory_learners[learner_id]
        return True

    async def add_observation(self, learner_id: uuid.UUID, observation, teacher_id: uuid.UUID | None = None, is_admin: bool = False):
        l = in_memory_learners.get(learner_id)
        if not l or not l.profile:
            return None
        if not is_admin and teacher_id is not None and l.teacher_id != teacher_id:
            return None
        obs_item = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": observation.category,
            "summary": observation.summary,
            "context": observation.context or {},
            "teacher_note": observation.teacher_note,
        }
        obs = list(l.profile.observations)
        obs.append(obs_item)
        l.profile.observations = obs
        return obs_item


# Patch dependency overrides on FastAPI app
async def override_get_db_session():
    yield AsyncMock()

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_curriculum_service] = lambda: MockCurriculumService()
app.dependency_overrides[get_learner_service] = lambda: MockLearnerService()

# Patch UserService where imported
patch("app.auth.router.UserService", return_value=MockUserService()).start()
patch("app.users.router.UserService", return_value=MockUserService()).start()
patch("app.auth.dependencies.UserService", return_value=MockUserService()).start()

if __name__ == "__main__":
    print("Starting Eduvia Dev Mock Server on http://localhost:8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

