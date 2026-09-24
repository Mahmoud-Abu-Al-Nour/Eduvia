"""
Eduvia — Development Test Data Cleanup Script

Safely and idempotently removes ONLY the 20 development test students, their
telemetry events, activity attempts, profiles, and secondary test teachers.

GUARANTEES:
- NEVER deletes admin users (admin@eduvia.app).
- NEVER deletes primary demo teacher (teacher@eduvia.app).
- NEVER deletes core demo learner (Tariq Al-Mansoor).
- NEVER deletes core curriculum or production data.
"""
import asyncio
import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.core.config import settings
from app.learners.models import Learner, LearnerProfile
from app.seeds.test_data_definitions import (
    COHORT_B_TEACHER_EMAIL,
    generate_learner_definitions,
)
from app.users.models import User


async def clear_test_data() -> None:
    print("\n=======================================================")
    print("  EDUVIA DEVELOPMENT TEST DATA CLEANUP                ")
    print("=======================================================\n")

    engine = create_async_engine(settings.effective_database_url)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    learner_definitions = generate_learner_definitions()
    test_learner_ids = [s.learner_id for s in learner_definitions]

    async with session_factory() as session:
        # 1. Delete PerformanceEvents for test learners
        res_events = await session.execute(
            delete(PerformanceEvent).where(PerformanceEvent.learner_id.in_(test_learner_ids))
        )
        print(f"[-] Removed {res_events.rowcount} test performance telemetry events.")

        # 2. Delete ActivityAttempts for test learners
        res_attempts = await session.execute(
            delete(ActivityAttempt).where(ActivityAttempt.learner_id.in_(test_learner_ids))
        )
        print(f"[-] Removed {res_attempts.rowcount} test activity attempts.")

        # 3. Delete LearnerProfiles for test learners
        res_profiles = await session.execute(
            delete(LearnerProfile).where(LearnerProfile.learner_id.in_(test_learner_ids))
        )
        print(f"[-] Removed {res_profiles.rowcount} test learner profiles.")

        # 4. Delete Learners matching test IDs or names starting with "Test Student - "
        res_learners = await session.execute(
            delete(Learner).where(
                (Learner.id.in_(test_learner_ids)) | (Learner.name.startswith("Test Student - "))
            )
        )
        print(f"[-] Removed {res_learners.rowcount} test student records.")

        # 5. Delete Test Cohort B Teacher user
        res_teacher = await session.execute(
            delete(User).where(User.email == COHORT_B_TEACHER_EMAIL)
        )
        print(f"[-] Removed secondary test teacher ({COHORT_B_TEACHER_EMAIL}): {res_teacher.rowcount} row(s).")

        await session.commit()

    await engine.dispose()
    print("\n-------------------------------------------------------")
    print("  TEST DATA CLEANUP COMPLETE (Core data untouched).    ")
    print("=======================================================\n")


if __name__ == "__main__":
    asyncio.run(clear_test_data())
