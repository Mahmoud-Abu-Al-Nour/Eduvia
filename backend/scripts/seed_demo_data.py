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
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash
from app.curriculum.models import Curriculum, Lesson, LearningObjective, Subject, Unit
from app.database.session import SessionLocal
from app.users.models import User, UserRole


async def seed_demo_data() -> None:
    print("Starting Eduvia full demonstration data seeding...")
    async with SessionLocal() as session:
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
            obj_1_10.prerequisites.append(obj_1_5)

            print("Created demonstration curriculum hierarchy with prerequisites.")
        else:
            print("Demonstration curriculum already exists. Skipping.")

        await session.commit()
        print("Demo data seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
