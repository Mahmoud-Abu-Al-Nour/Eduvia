import asyncio
import os
import sys

# Ensure the app module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal
from app.curriculum.models import Curriculum, Subject, Unit, Lesson, LearningObjective

async def seed_curriculum():
    print("Starting Eduvia Demonstration Curriculum seeding...")
    async with SessionLocal() as session:
        # Check if already exists
        from sqlalchemy import select
        result = await session.execute(select(Curriculum).where(Curriculum.version == "demo-1.0"))
        existing = result.scalars().first()
        if existing:
            print("Demonstration curriculum already exists. Skipping.")
            return

        # 1. Curriculum
        curriculum = Curriculum(
            title={"en": "Eduvia Demonstration Curriculum", "ar": "منهج إدوفيا التجريبي"},
            description={"en": "A small demonstration curriculum for testing hierarchy.", "ar": "منهج تجريبي صغير لاختبار التسلسل الهرمي."},
            version="demo-1.0",
        )
        session.add(curriculum)
        await session.flush()
        
        # 2. Subject
        subject_math = Subject(
            curriculum_id=curriculum.id,
            title={"en": "Mathematics", "ar": "الرياضيات"},
            description={"en": "Basic mathematics.", "ar": "الرياضيات الأساسية."},
            order_index=1
        )
        session.add(subject_math)
        await session.flush()

        # 3. Unit
        unit_numbers = Unit(
            subject_id=subject_math.id,
            title={"en": "Numbers", "ar": "الأرقام"},
            order_index=1
        )
        session.add(unit_numbers)
        await session.flush()

        # 4. Lesson
        lesson_recog = Lesson(
            unit_id=unit_numbers.id,
            title={"en": "Number Recognition", "ar": "التعرف على الأرقام"},
            order_index=1
        )
        session.add(lesson_recog)
        await session.flush()

        # 5. Learning Objectives
        obj_1_5 = LearningObjective(
            lesson_id=lesson_recog.id,
            title={"en": "Recognize numbers 1–5", "ar": "التعرف على الأرقام ١-٥"},
            difficulty_level=1,
            assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 2},
            order_index=1
        )
        session.add(obj_1_5)
        await session.flush()
        
        obj_1_10 = LearningObjective(
            lesson_id=lesson_recog.id,
            title={"en": "Recognize numbers 1–10", "ar": "التعرف على الأرقام ١-١٠"},
            difficulty_level=2,
            assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
            order_index=2
        )
        session.add(obj_1_10)
        await session.flush()

        # Prerequisites (1-5 is required for 1-10)
        obj_1_10.prerequisites.append(obj_1_5)

        await session.commit()
        print("Curriculum seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_curriculum())
