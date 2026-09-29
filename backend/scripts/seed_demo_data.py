"""
Eduvia — Demo Data Seeding Script

Creates initial demo users (Admin & Teacher), the expanded foundational
curriculum hierarchy (3 Subjects, 13 Units, 70 Objectives) with realistic
prerequisite relationships, the Content Bank items, and learner profiles.
"""
import asyncio
import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.security import get_password_hash
from app.content.definitions import ALL_CONTENT_ITEMS
from app.content.models import ContentItem
from app.core.config import settings
from app.curriculum.curriculum_catalog import (
    CURRICULUM_DESCRIPTION,
    CURRICULUM_ID,
    CURRICULUM_TITLE,
    CURRICULUM_VERSION,
    FULL_CURRICULUM_CATALOG,
)
from app.curriculum.models import (
    Curriculum,
    LearningObjective,
    Lesson,
    Subject,
    Unit,
    objective_prerequisites,
)
from app.learners.models import Learner, LearnerProfile
from app.research.models import (
    ResearchArtifact,
    ResearchEvaluation,
    ResearchExperiment,
    ResearchMetric,
    ResearchProject,
    ResearchRun,
    ResearchVariant,
)
from app.users.models import User, UserRole


async def seed_demo_data() -> None:
    print("Starting Eduvia comprehensive demonstration and curriculum data seeding...")
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

        teacher2_email = "teacher2@eduvia.app"
        result = await session.execute(select(User).where(User.email == teacher2_email))
        teacher2 = result.scalars().first()
        if not teacher2:
            teacher2 = User(
                email=teacher2_email,
                full_name="Bob Teacher (Cohort B)",
                hashed_password=get_password_hash("strongpassword123"),
                role=UserRole.teacher,
                is_active=True,
            )
            session.add(teacher2)
            print(f"Created demo teacher 2: {teacher2_email}")

        learner_user_email = "learner@eduvia.app"
        result = await session.execute(select(User).where(User.email == learner_user_email))
        learner_user = result.scalars().first()
        if not learner_user:
            learner_user = User(
                email=learner_user_email,
                full_name="Tariq Al-Mansoor",
                hashed_password=get_password_hash("learnerpassword123"),
                role=UserRole.learner,
                is_active=True,
            )
            session.add(learner_user)
            print(f"Created demo learner user: {learner_user_email}")

        learner2_user_email = "learner2@eduvia.app"
        result = await session.execute(select(User).where(User.email == learner2_user_email))
        learner2_user = result.scalars().first()
        if not learner2_user:
            learner2_user = User(
                email=learner2_user_email,
                full_name="Laila Hassan",
                hashed_password=get_password_hash("learnerpassword123"),
                role=UserRole.learner,
                is_active=True,
            )
            session.add(learner2_user)
            print(f"Created demo learner 2 user: {learner2_user_email}")

        researcher_email = "researcher@eduvia.app"
        result = await session.execute(select(User).where(User.email == researcher_email))
        researcher = result.scalars().first()
        if not researcher:
            researcher = User(
                email=researcher_email,
                full_name="Dr. Elena Vance (Researcher)",
                hashed_password=get_password_hash("researcherpassword123"),
                role=UserRole.researcher,
                is_active=True,
            )
            session.add(researcher)
            print(f"Created demo researcher user: {researcher_email}")
        else:
            print(f"Demo researcher already exists: {researcher_email}")

        await session.flush()

        # ── 2. Seed Full Curriculum Hierarchy ─────────────────────────────────
        result = await session.execute(select(Curriculum).where(Curriculum.id == CURRICULUM_ID))
        curriculum = result.scalars().first()
        if not curriculum:
            curriculum = Curriculum(
                id=CURRICULUM_ID,
                title=CURRICULUM_TITLE,
                description=CURRICULUM_DESCRIPTION,
                version=CURRICULUM_VERSION,
                created_by_id=admin.id,
            )
            session.add(curriculum)
            await session.flush()
            print(f"Created curriculum: {CURRICULUM_VERSION}")
        else:
            print(f"Curriculum already exists: {CURRICULUM_VERSION}")

        # Seed subjects, units, lessons, objectives
        prereq_links: list[tuple[any, any]] = []
        seeded_objs_count = 0

        for subj_data in FULL_CURRICULUM_CATALOG:
            s_res = await session.execute(select(Subject).where(Subject.id == subj_data["id"]))
            subject = s_res.scalars().first()
            if not subject:
                subject = Subject(
                    id=subj_data["id"],
                    curriculum_id=curriculum.id,
                    title=subj_data["title"],
                    description=subj_data["description"],
                    order_index=subj_data["order_index"],
                )
                session.add(subject)
                await session.flush()

            for unit_data in subj_data.get("units", []):
                u_res = await session.execute(select(Unit).where(Unit.id == unit_data["id"]))
                unit = u_res.scalars().first()
                if not unit:
                    unit = Unit(
                        id=unit_data["id"],
                        subject_id=subject.id,
                        title=unit_data["title"],
                        description=unit_data["description"],
                        order_index=unit_data["order_index"],
                    )
                    session.add(unit)
                    await session.flush()

                for lesson_data in unit_data.get("lessons", []):
                    l_res = await session.execute(select(Lesson).where(Lesson.id == lesson_data["id"]))
                    lesson = l_res.scalars().first()
                    if not lesson:
                        lesson = Lesson(
                            id=lesson_data["id"],
                            unit_id=unit.id,
                            title=lesson_data["title"],
                            description=lesson_data["description"],
                            order_index=lesson_data["order_index"],
                        )
                        session.add(lesson)
                        await session.flush()

                    for obj_data in lesson_data.get("learning_objectives", []):
                        o_res = await session.execute(select(LearningObjective).where(LearningObjective.id == obj_data["id"]))
                        objective = o_res.scalars().first()
                        if not objective:
                            objective = LearningObjective(
                                id=obj_data["id"],
                                lesson_id=lesson.id,
                                title=obj_data["title"],
                                description=obj_data["description"],
                                difficulty_level=obj_data["difficulty_level"],
                                assessment_criteria=obj_data["assessment_criteria"],
                                order_index=obj_data["order_index"],
                                is_active=obj_data.get("is_active", True),
                            )
                            session.add(objective)
                            seeded_objs_count += 1

                        for prereq_id in obj_data.get("prerequisites", []):
                            prereq_links.append((obj_data["id"], prereq_id))

        await session.flush()
        print(f"Curriculum objectives seeded: {seeded_objs_count} new objectives.")

        # Seed Prerequisites idempotently
        for target_id, prereq_id in prereq_links:
            # Check if pair already exists
            existing_p = await session.execute(
                select(objective_prerequisites).where(
                    objective_prerequisites.c.objective_id == target_id,
                    objective_prerequisites.c.prerequisite_id == prereq_id,
                )
            )
            if not existing_p.first():
                await session.execute(
                    objective_prerequisites.insert().values(
                        objective_id=target_id,
                        prerequisite_id=prereq_id,
                    )
                )

        await session.flush()
        print(f"Prerequisite relationships linked ({len(prereq_links)} total pairs mapped).")

        # ── 3. Seed Content Bank Items ─────────────────────────────────────────
        seeded_content_count = 0
        for item in ALL_CONTENT_ITEMS:
            c_res = await session.execute(select(ContentItem).where(ContentItem.id == item.id))
            if not c_res.scalars().first():
                content_row = ContentItem(
                    id=item.id,
                    objective_id=item.objective_id,
                    subject_code=item.subject_code,
                    unit_code=item.unit_code,
                    content_key=item.content_key,
                    difficulty_level=item.difficulty_level,
                    supported_modalities=item.supported_modalities,
                    prompt=item.prompt,
                    content_payload=item.content_payload,
                    correct_answer=item.correct_answer,
                    hints=item.hints,
                    metadata_info=item.metadata_info,
                    is_active=getattr(item, "is_active", True),
                )
                session.add(content_row)
                seeded_content_count += 1

        await session.flush()
        print(f"Content Bank items seeded: {seeded_content_count} new authoritative content items.")

        # ── 4. Seed Demo Learner & Profile ───────────────────────────────────
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
                user_id=learner_user.id,
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

        # Seed Cohort B learner (Laila Hassan)
        learner2_name = "Laila Hassan"
        result = await session.execute(select(Learner).where(Learner.name == learner2_name))
        existing_learner2 = result.scalars().first()
        if not existing_learner2:
            demo_learner2 = Learner(
                name=learner2_name,
                age_group="primary",
                learning_level="beginner",
                is_active=True,
                teacher_id=teacher2.id,
                user_id=learner2_user.id,
            )
            session.add(demo_learner2)
            await session.flush()

            demo_profile2 = LearnerProfile(
                learner_id=demo_learner2.id,
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
                    "strengths": ["visual memory"],
                    "focus_areas": ["letter sounds"],
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
                teacher_notes="Cohort B learner assigned to Bob Teacher.",
                teacher_overrides={},
                modality_effectiveness={"visual": 0.80, "interactive": 0.70},
                strategy_effectiveness={"scaffolded_hints": 0.85},
                activity_type_effectiveness={"matching": 0.88},
                difficulty_tolerance=1.0,
                assistance_requirements={"preferred_prompt_hierarchy": "least_to_most"},
                response_behavior={"typical_latency_seconds": 4.1},
                observations={"recorded_by": "Bob Teacher", "date": "2026-09-21"},
            )
            session.add(demo_profile2)
            print(f"Created demo learner 2 and profile: {learner2_name}")
        # ── 5. Seed Research Sandbox Demo Entities ───────────────────────────
        res_proj_name = "Multi-Modal Pedagogical Strategies"
        result = await session.execute(select(ResearchProject).where(ResearchProject.name == res_proj_name))
        res_project = result.scalars().first()
        if not res_project:
            res_project = ResearchProject(
                name=res_proj_name,
                description="Sandbox investigation into multi-modal scaffolds vs text-only explanations.",
                research_question="Does visual cueing combined with step-by-step guidance increase conceptual comprehension compared to text-only explanations?",
                hypothesis="Learners exposed to multi-modal visual steps will demonstrate higher accuracy.",
                owner_id=researcher.id,
                status="active",
                metadata_info={"domain": "special_education", "phase": "pilot"},
            )
            session.add(res_project)
            await session.flush()

            res_exp = ResearchExperiment(
                project_id=res_project.id,
                name="Visual vs Text Scaffolding in Early Literacy",
                description="Comparing 5-question multi-modal activities against homogeneous text activities.",
                research_question="How does visual cue placement affect distraction vs engagement?",
                hypothesis="Embedded visual icons reduce question completion time by 20%.",
                status="active",
                metadata_info={},
            )
            session.add(res_exp)
            await session.flush()

            metric_clarity = ResearchMetric(
                experiment_id=res_exp.id,
                name="Instructional Clarity",
                description="Clarity and readability of explanatory text (1-5 scale).",
                metric_type="rating",
                configuration={"min": 1, "max": 5},
            )
            metric_cognitive = ResearchMetric(
                experiment_id=res_exp.id,
                name="Cognitive Load Estimate",
                description="Perceived visual complexity and prompt length.",
                metric_type="rating",
                configuration={"min": 1, "max": 5},
            )
            session.add(metric_clarity)
            session.add(metric_cognitive)
            await session.flush()

            var_a = ResearchVariant(
                experiment_id=res_exp.id,
                name="Variant A: Visual Scaffolding (5 Questions)",
                description="Includes visual icon cues, step-by-step breakdown, and pictorial choices.",
                configuration={
                    "model": "gemini-2.5-flash",
                    "temperature": 0.3,
                    "scaffolding_style": "visual_assisted",
                    "question_count": 5,
                },
                metadata_info={},
            )
            var_b = ResearchVariant(
                experiment_id=res_exp.id,
                name="Variant B: Text-Only Scaffolding (5 Questions)",
                description="Pure text explanations without visual cues.",
                configuration={
                    "model": "gemini-2.5-flash",
                    "temperature": 0.7,
                    "scaffolding_style": "text_only",
                    "question_count": 5,
                },
                parent_variant_id=var_a.id,
                metadata_info={"cloned_from": "Variant A"},
            )
            session.add(var_a)
            session.add(var_b)
            await session.flush()

            sample_run = ResearchRun(
                variant_id=var_a.id,
                model="gemini-2.5-flash",
                model_configuration={"temperature": 0.3, "max_output_tokens": 2048},
                system_prompt="You are an educational researcher evaluating visual scaffolding.",
                user_prompt="Generate 5 phonemic awareness questions pairing sound with visual cues.",
                status="completed",
                started_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
                raw_output='{"assessment_title": "Visual Phonemic Scaffolding", "question_count": 5, "items": [{"id": "q1", "prompt": "Which item starts with the /b/ sound?", "visual_cue": "image_bell", "choices": ["Bell", "Cat", "Sun"], "answer": "Bell"}]}',
                normalized_output={
                    "assessment_title": "Visual Phonemic Scaffolding",
                    "question_count": 5,
                    "items": [
                        {
                            "id": "q1",
                            "prompt": "Which item starts with the /b/ sound?",
                            "visual_cue": "image_bell",
                            "choices": ["Bell", "Cat", "Sun"],
                            "answer": "Bell",
                        }
                    ],
                },
                metadata_info={"execution_time_ms": 320.5},
            )
            session.add(sample_run)
            await session.flush()

            sample_artifact = ResearchArtifact(
                run_id=sample_run.id,
                artifact_type="assessment",
                schema_version="1.0",
                payload=sample_run.normalized_output,
                raw_text=sample_run.raw_output,
                is_production_compatible=False,
                promoted_to_production=False,
                metadata_info={},
            )
            session.add(sample_artifact)
            await session.flush()

            sample_eval = ResearchEvaluation(
                artifact_id=sample_artifact.id,
                metric_id=metric_clarity.id,
                metric_name="Instructional Clarity",
                value={"score": 5, "max": 5},
                evaluator_type="manual",
                evaluator_id=researcher.id,
                notes="Excellent visual alignment and distinct sound associations.",
            )
            session.add(sample_eval)
            print(f"Created demo research project, experiment, variants, run, and artifact: {res_proj_name}")
        else:
            print(f"Demo research project already exists: {res_proj_name}")

        await session.commit()
    await engine.dispose()
    print("Full demo and curriculum data seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
