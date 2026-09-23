"""
Eduvia — Demo Data Seeding Script

Creates initial demo users (Admin & Teacher) and the standard
demonstration curriculum hierarchy for testing and development.
"""
import asyncio
import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.security import get_password_hash
from app.core.config import settings
from app.curriculum.models import (
    Curriculum,
    Lesson,
    LearningObjective,
    Subject,
    Unit,
    objective_prerequisites,
)
from app.learners.models import Learner, LearnerProfile
from app.users.models import User, UserRole


async def seed_demo_data() -> None:
    print("Starting Eduvia full demonstration data seeding...")
    engine = create_async_engine(settings.effective_database_url)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        # ── 1. Seed Demo Users ────────────────────────────────────────────────
        admin_email = "admin@eduvia.app"
        result = await session.execute(select(User).where(User.email == admin_email))
        admin = result.scalars().first()
        if not admin:
            admin = User(
                email=admin_email,
                full_name="Eduvia Admin",
                hashed_password=get_password_hash("adminpassword123"),
                role=UserRole.admin,
                is_active=True,
            )
            session.add(admin)
            print(f"Created demo admin: {admin_email}")
        else:
            print(f"Demo admin already exists: {admin_email}")

        teacher_email = "teacher@eduvia.app"
        result = await session.execute(select(User).where(User.email == teacher_email))
        teacher = result.scalars().first()
        if not teacher:
            teacher = User(
                email=teacher_email,
                full_name="Alice Teacher",
                hashed_password=get_password_hash("strongpassword123"),
                role=UserRole.teacher,
                is_active=True,
            )
            session.add(teacher)
            print(f"Created demo teacher: {teacher_email}")
        else:
            print(f"Demo teacher already exists: {teacher_email}")

        await session.flush()

        # ── 2. Seed Demo Curriculum Hierarchy ─────────────────────────────────
        result = await session.execute(select(Curriculum).where(Curriculum.version == "demo-1.0"))
        existing_curr = result.scalars().first()
        if not existing_curr:
            curriculum = Curriculum(
                title={"en": "Eduvia Demonstration Curriculum", "ar": "منهج إدوفيا التجريبي"},
                description={
                    "en": "A standardized demonstration curriculum for inclusive numeracy.",
                    "ar": "منهج تجريبي معياري لتطوير مهارات الحساب الشاملة.",
                },
                version="demo-1.0",
                created_by_id=admin.id,
            )
            session.add(curriculum)
            await session.flush()

            # Subject
            subject_math = Subject(
                curriculum_id=curriculum.id,
                title={"en": "Foundational Mathematics", "ar": "أساسيات الرياضيات"},
                description={
                    "en": "Basic mathematical reasoning, pattern recognition, and number sense.",
                    "ar": "التفكير الرياضي الأساسي، التعرف على الأنماط، والحس العددي.",
                },
                order_index=1,
            )
            session.add(subject_math)
            await session.flush()

            # Unit
            unit_numbers = Unit(
                subject_id=subject_math.id,
                title={"en": "Number Sense & Counting", "ar": "الحس العددي والعد"},
                description={
                    "en": "Understanding discrete quantities and numerical representations.",
                    "ar": "فهم الكميات المنفصلة والتمثيلات العددية.",
                },
                order_index=1,
            )
            session.add(unit_numbers)
            await session.flush()

            # Lesson
            lesson_recog = Lesson(
                unit_id=unit_numbers.id,
                title={"en": "Number Recognition 1–10", "ar": "التعرف على الأرقام من ١ إلى ١٠"},
                description={
                    "en": "Identifying digits visually and mapping them to quantities.",
                    "ar": "التعرف البصري على الأرقام وربطها بالكميات.",
                },
                order_index=1,
            )
            session.add(lesson_recog)
            await session.flush()

            # Objective 1 (Foundation)
            obj_1_5 = LearningObjective(
                lesson_id=lesson_recog.id,
                title={"en": "Recognize numbers 1–5", "ar": "التعرف على الأرقام ١-٥"},
                description={
                    "en": "Identify written numerals 1 to 5 and match to dot patterns.",
                    "ar": "التعرف على الأرقام المكتوبة من ١ إلى ٥ ومطابقتها مع أنماط النقاط.",
                },
                difficulty_level=1,
                assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 2},
                order_index=1,
            )
            session.add(obj_1_5)
            await session.flush()

            # Objective 2 (Advanced with prerequisite)
            obj_1_10 = LearningObjective(
                lesson_id=lesson_recog.id,
                title={"en": "Recognize numbers 6–10", "ar": "التعرف على الأرقام ٦-١٠"},
                description={
                    "en": "Identify written numerals 6 to 10 and order them progressively.",
                    "ar": "التعرف على الأرقام المكتوبة من ٦ إلى ١٠ وترتيبها تدريجياً.",
                },
                difficulty_level=2,
                assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
                order_index=2,
            )
            session.add(obj_1_10)
            await session.flush()

            # Link prerequisite
            await session.execute(
                objective_prerequisites.insert().values(
                    objective_id=obj_1_10.id, prerequisite_id=obj_1_5.id
                )
            )

            print("Created demonstration curriculum hierarchy with prerequisites.")
        else:
            print("Demonstration curriculum already exists. Skipping.")

        # ── 3. Seed Demo Learner & Profile ───────────────────────────────────
        learner_name = "Tariq Al-Mansoor"
        result = await session.execute(select(Learner).where(Learner.name == learner_name))
        existing_learner = result.scalars().first()
        if not existing_learner:
            demo_learner = Learner(
                name=learner_name,
                age_group="primary",
                learning_level="beginner",
                is_active=True,
                teacher_id=teacher.id,
            )
            session.add(demo_learner)
            await session.flush()

            demo_profile = LearnerProfile(
                learner_id=demo_learner.id,
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
                teacher_overrides={},
                modality_effectiveness={"visual": 0.85, "interactive": 0.75, "auditory": 0.60},
                strategy_effectiveness={"scaffolded_hints": 0.88, "direct_instruction": 0.70},
                activity_type_effectiveness={"matching": 0.90, "sorting": 0.82},
                difficulty_tolerance=1.5,
                assistance_requirements={"preferred_prompt_hierarchy": "least_to_most"},
                response_behavior={"typical_latency_seconds": 3.2},
                observations={"recorded_by": "Alice Teacher", "date": "2026-09-20"},
            )
            session.add(demo_profile)
            print(f"Created demo learner and profile: {learner_name}")
        else:
            print(f"Demo learner already exists: {learner_name}")

        await session.commit()
    await engine.dispose()
    print("Demo data seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
