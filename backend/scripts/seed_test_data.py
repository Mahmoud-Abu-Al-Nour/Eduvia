"""
Eduvia — Development Test Data Seeding Script

Idempotently seeds 20 educational scenario students across 2 cohorts
(Cohort A: Alice Teacher, Cohort B: Marcus Teacher) with realistic historical
telemetry spanning 60 days.

Deterministic IDs ensure safety, zero data loss, and complete reversibility.
"""
import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.analytics.models import ActivityAttempt, PerformanceEvent
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
from app.seeds.test_data_definitions import (
    COHORT_A_TEACHER_EMAIL,
    COHORT_A_TEACHER_ID,
    COHORT_B_NAME,
    COHORT_B_TEACHER_EMAIL,
    COHORT_B_TEACHER_ID,
    COHORT_B_TEACHER_NAME,
    CURRICULUM_ID,
    LESSON_ID,
    OBJ_1_5_ID,
    OBJ_6_10_ID,
    OBJ_PATTERNS_ID,
    SUBJECT_ID,
    UNIT_ID,
    generate_learner_definitions,
    get_test_uuid,
)
from app.users.models import User, UserRole


async def seed_test_data() -> None:
    print("\n=======================================================")
    print("  EDUVIA DEVELOPMENT TEST DATA SEEDING (20 STUDENTS)  ")
    print("=======================================================\n")

    engine = create_async_engine(settings.effective_database_url)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    now = datetime.now(UTC)
    learner_definitions = generate_learner_definitions(now=now)

    async with session_factory() as session:
        # ── 1. Ensure Teachers & Cohorts Exist ────────────────────────────────
        # Cohort A Teacher (Existing Alice Teacher)
        result = await session.execute(select(User).where(User.email == COHORT_A_TEACHER_EMAIL))
        teacher_a = result.scalars().first()
        if not teacher_a:
            teacher_a = User(
                id=COHORT_A_TEACHER_ID,
                email=COHORT_A_TEACHER_EMAIL,
                full_name="Alice Teacher",
                hashed_password=get_password_hash("strongpassword123"),
                role=UserRole.teacher,
                is_active=True,
            )
            session.add(teacher_a)
            print(f"[+] Created Cohort A Teacher: {COHORT_A_TEACHER_EMAIL}")
        else:
            print(f"[*] Cohort A Teacher active: {teacher_a.email}")

        # Cohort B Teacher (Marcus Teacher for Diverse/Struggling cohort)
        result = await session.execute(select(User).where(User.email == COHORT_B_TEACHER_EMAIL))
        teacher_b = result.scalars().first()
        if not teacher_b:
            teacher_b = User(
                id=COHORT_B_TEACHER_ID,
                email=COHORT_B_TEACHER_EMAIL,
                full_name=COHORT_B_TEACHER_NAME,
                hashed_password=get_password_hash("strongpassword123"),
                role=UserRole.teacher,
                is_active=True,
            )
            session.add(teacher_b)
            print(f"[+] Created Cohort B Teacher: {COHORT_B_TEACHER_EMAIL}")
        else:
            print(f"[*] Cohort B Teacher active: {teacher_b.email}")

        await session.flush()

        # ── 2. Ensure Curriculum & Objectives Exist ───────────────────────────
        # Check Curriculum
        result = await session.execute(select(Curriculum).where(Curriculum.id == CURRICULUM_ID))
        curriculum = result.scalars().first()
        if not curriculum:
            curriculum = Curriculum(
                id=CURRICULUM_ID,
                title={"en": "Eduvia Demonstration Curriculum", "ar": "منهج إدوفيا التجريبي"},
                description={
                    "en": "A standardized demonstration curriculum for inclusive numeracy.",
                    "ar": "منهج تجريبي معياري لتطوير مهارات الحساب الشاملة.",
                },
                version="demo-1.0",
                created_by_id=teacher_a.id,
            )
            session.add(curriculum)
            await session.flush()

        # Subject
        result = await session.execute(select(Subject).where(Subject.id == SUBJECT_ID))
        subject = result.scalars().first()
        if not subject:
            subject = Subject(
                id=SUBJECT_ID,
                curriculum_id=curriculum.id,
                title={"en": "Foundational Mathematics", "ar": "أساسيات الرياضيات"},
                description={"en": "Basic mathematical reasoning and number sense.", "ar": "التفكير الرياضي الأساسي."},
                order_index=1,
            )
            session.add(subject)
            await session.flush()

        # Unit
        result = await session.execute(select(Unit).where(Unit.id == UNIT_ID))
        unit = result.scalars().first()
        if not unit:
            unit = Unit(
                id=UNIT_ID,
                subject_id=subject.id,
                title={"en": "Number Sense & Counting", "ar": "الحس العددي والعد"},
                description={"en": "Understanding discrete quantities.", "ar": "فهم الكميات المنفصلة."},
                order_index=1,
            )
            session.add(unit)
            await session.flush()

        # Lesson
        result = await session.execute(select(Lesson).where(Lesson.id == LESSON_ID))
        lesson = result.scalars().first()
        if not lesson:
            lesson = Lesson(
                id=LESSON_ID,
                unit_id=unit.id,
                title={"en": "Number Recognition 1–10", "ar": "التعرف على الأرقام من ١ إلى ١٠"},
                description={"en": "Identifying digits visually.", "ar": "التعرف البصري على الأرقام."},
                order_index=1,
            )
            session.add(lesson)
            await session.flush()

        # Objectives
        # 1. Obj 1-5
        result = await session.execute(select(LearningObjective).where(LearningObjective.id == OBJ_1_5_ID))
        obj_1_5 = result.scalars().first()
        if not obj_1_5:
            obj_1_5 = LearningObjective(
                id=OBJ_1_5_ID,
                lesson_id=lesson.id,
                title={"en": "Recognize numbers 1–5", "ar": "التعرف على الأرقام ١-٥"},
                description={"en": "Identify numerals 1 to 5 and match to quantities.", "ar": "التعرف على الأرقام ١ إلى ٥."},
                difficulty_level=1,
                assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 2},
                order_index=1,
                is_active=True,
            )
            session.add(obj_1_5)
            await session.flush()

        # 2. Obj 6-10
        result = await session.execute(select(LearningObjective).where(LearningObjective.id == OBJ_6_10_ID))
        obj_6_10 = result.scalars().first()
        if not obj_6_10:
            obj_6_10 = LearningObjective(
                id=OBJ_6_10_ID,
                lesson_id=lesson.id,
                title={"en": "Recognize numbers 6–10", "ar": "التعرف على الأرقام ٦-١٠"},
                description={"en": "Identify written numerals 6 to 10.", "ar": "التعرف على الأرقام ٦ إلى ١٠."},
                difficulty_level=2,
                assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
                order_index=2,
                is_active=True,
            )
            session.add(obj_6_10)
            await session.flush()
            # Prereq
            await session.execute(
                objective_prerequisites.insert().values(
                    objective_id=obj_6_10.id, prerequisite_id=obj_1_5.id
                )
            )

        # 3. Obj Patterns
        result = await session.execute(select(LearningObjective).where(LearningObjective.id == OBJ_PATTERNS_ID))
        obj_patterns = result.scalars().first()
        if not obj_patterns:
            obj_patterns = LearningObjective(
                id=OBJ_PATTERNS_ID,
                lesson_id=lesson.id,
                title={"en": "Number Patterns & Sequencing", "ar": "الأنماط العددية والتسلسل"},
                description={"en": "Recognize ascending and descending sequences.", "ar": "التعرف على الأنماط التصاعدية والتنازلية."},
                difficulty_level=3,
                assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                order_index=3,
                is_active=True,
            )
            session.add(obj_patterns)
            await session.flush()
            await session.execute(
                objective_prerequisites.insert().values(
                    objective_id=obj_patterns.id, prerequisite_id=obj_6_10.id
                )
            )

        await session.flush()

        # ── 3. Seed 20 Test Students & Profiles ──────────────────────────────
        total_seeded_students = 0
        total_seeded_events = 0
        total_seeded_attempts = 0

        for s in learner_definitions:
            assigned_teacher_id = teacher_a.id if s.cohort_key == "cohort_a" else teacher_b.id

            result = await session.execute(select(Learner).where(Learner.id == s.learner_id))
            learner = result.scalars().first()
            if not learner:
                learner = Learner(
                    id=s.learner_id,
                    name=s.name,
                    age_group=s.age_group,
                    learning_level=s.learning_level,
                    is_active=True,
                    teacher_id=assigned_teacher_id,
                )
                session.add(learner)
                await session.flush()

            # Profile
            result = await session.execute(select(LearnerProfile).where(LearnerProfile.learner_id == s.learner_id))
            profile = result.scalars().first()
            if not profile:
                profile = LearnerProfile(
                    id=s.profile_id,
                    learner_id=s.learner_id,
                    communication_preferences={
                        "primary_mode": s.communication_primary_mode,
                        "receptive_preference": s.receptive_preferences,
                        "expressive_preference": s.expressive_preferences,
                        "notes": f"Scenario: {s.key}. {s.summary_description}",
                    },
                    current_skill_level={
                        "literacy_stage": s.literacy_stage,
                        "numeracy_stage": s.numeracy_stage,
                        "attention_span_minutes": s.attention_span_minutes,
                        "strengths": s.strengths,
                        "focus_areas": s.focus_areas,
                    },
                    support_requirements={
                        "sensory_accommodations": s.sensory_accommodations,
                        "pacing": s.pacing,
                        "guidance_level": "standard",
                    },
                    teacher_constraints={
                        "max_session_duration_minutes": s.attention_span_minutes,
                        "excluded_modalities": [],
                        "required_modalities": ["Visual"],
                    },
                    teacher_notes=s.teacher_notes,
                    teacher_overrides={},
                    modality_effectiveness=s.modality_effectiveness,
                    strategy_effectiveness={"scaffolded_hints": 0.85, "visual_cueing": 0.88},
                    activity_type_effectiveness={"matching": 0.85, "ordering": 0.80},
                    difficulty_tolerance=1.5,
                    assistance_requirements={"preferred_prompt_hierarchy": "least_to_most"},
                    response_behavior={"typical_latency_seconds": 3.0},
                    observations={"scenario": s.key, "seeded_at": now.isoformat()},
                )
                session.add(profile)
                await session.flush()

            total_seeded_students += 1

            # ── 4. Seed Telemetry & Activity Attempts ─────────────────────────
            # Clear any previously seeded events for this test learner to ensure clean idempotent seed
            await session.execute(delete(PerformanceEvent).where(PerformanceEvent.learner_id == s.learner_id))
            await session.execute(delete(ActivityAttempt).where(ActivityAttempt.learner_id == s.learner_id))

            for idx, t in enumerate(s.telemetry_events):
                event_time = now - timedelta(days=t.days_ago, minutes=idx * 15)
                attempt_id = get_test_uuid(f"attempt.{s.key}.{idx}")
                activity_id = get_test_uuid(f"activity.{s.key}.{idx}")

                attempt = ActivityAttempt(
                    id=attempt_id,
                    activity_id=activity_id,
                    learner_id=s.learner_id,
                    session_id=get_test_uuid(f"session.{s.key}.{t.days_ago}"),
                    started_at=event_time - timedelta(minutes=3),
                    completed_at=event_time,
                    response_data={"selected": "option_A", "correct": t.correct, "score": t.score},
                    score=t.score,
                    completed=t.completed,
                )
                session.add(attempt)
                total_seeded_attempts += 1

                event = PerformanceEvent(
                    id=get_test_uuid(f"event.{s.key}.{idx}"),
                    learner_id=s.learner_id,
                    activity_id=activity_id,
                    attempt_id=attempt_id,
                    objective_id=t.objective_id,
                    activity_type=t.activity_type,
                    modality=t.modality,
                    strategy=t.strategy,
                    correct=t.correct,
                    score=t.score,
                    attempts=1,
                    response_time_ms=t.response_time_ms,
                    hints_used=t.hints_used,
                    assistance_level=t.assistance_level,
                    completed=t.completed,
                    difficulty=t.difficulty,
                    event_metadata={"scenario": s.key, "test_data": True},
                )
                session.add(event)
                total_seeded_events += 1

            print(f"  [+] {s.name:<45} | Cohort: {s.cohort_key.upper()} | Telemetry Events: {len(s.telemetry_events)}")

        await session.commit()

    await engine.dispose()
    print("\n-------------------------------------------------------")
    print(f"  SEEDING COMPLETE:")
    print(f"  - Test Learners:          {total_seeded_students}")
    print(f"  - Activity Attempts:      {total_seeded_attempts}")
    print(f"  - Performance Events:     {total_seeded_events}")
    print(f"  - Cohort A (Teacher: {COHORT_A_TEACHER_EMAIL})")
    print(f"  - Cohort B (Teacher: {COHORT_B_TEACHER_EMAIL})")
    print("=======================================================\n")


if __name__ == "__main__":
    asyncio.run(seed_test_data())
