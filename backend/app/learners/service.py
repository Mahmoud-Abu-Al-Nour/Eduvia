"""
Eduvia -- Learner Service Layer (Phase 3)

Encapsulates all database operations for Learners and Learner Profiles.
Maintains teacher ownership isolation and admin visibility.
"""
import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.learners.models import Learner, LearnerProfile
from app.learners.schemas import (
    LearnerCreate,
    LearnerObservationCreate,
    LearnerUpdate,
)


class LearnerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_learners(
        self, teacher_id: Optional[uuid.UUID], is_admin: bool = False
    ) -> list[Learner]:
        """
        List learners. Admins can view all learners; teachers can only view their own.
        """
        stmt = select(Learner).options(selectinload(Learner.profile)).order_by(Learner.created_at.desc())
        if not is_admin and teacher_id is not None:
            stmt = stmt.where(Learner.teacher_id == teacher_id)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(
        self,
        learner_id: uuid.UUID,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Optional[Learner]:
        """
        Retrieve a learner with full profile.
        Enforces teacher ownership check unless is_admin is True.
        """
        stmt = (
            select(Learner)
            .options(selectinload(Learner.profile))
            .where(Learner.id == learner_id)
        )
        result = await self.session.execute(stmt)
        learner = result.scalars().first()

        if not learner:
            return None

        if not is_admin and teacher_id is not None and learner.teacher_id != teacher_id:
            return None

        return learner

    async def create(
        self, data: LearnerCreate, teacher_id: Optional[uuid.UUID]
    ) -> Learner:
        """
        Create a new learner and initialize their associated LearnerProfile.
        """
        learner = Learner(
            name=data.name,
            age_group=data.age_group,
            learning_level=data.learning_level,
            teacher_id=teacher_id,
        )

        # Build initial profile with defaults and any teacher-provided values
        profile = LearnerProfile(learner=learner)

        if data.communication_preferences:
            profile.communication_preferences = {
                **profile.communication_preferences,
                **data.communication_preferences,
            }

        if data.support_requirements:
            profile.support_requirements = {
                **profile.support_requirements,
                **data.support_requirements,
            }

        if data.current_skill_level:
            profile.current_skill_level = {
                **profile.current_skill_level,
                **data.current_skill_level,
            }

        if data.teacher_notes is not None:
            profile.teacher_notes = data.teacher_notes

        if data.teacher_constraints:
            profile.teacher_constraints = {
                **profile.teacher_constraints,
                **data.teacher_constraints,
            }

        self.session.add(learner)
        self.session.add(profile)
        await self.session.commit()

        # Re-fetch with eager profile loading
        return await self.get_by_id(learner.id, teacher_id=teacher_id, is_admin=True)  # type: ignore

    async def update(
        self,
        learner_id: uuid.UUID,
        data: LearnerUpdate,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Optional[Learner]:
        """
        Update learner metadata and/or profile fields.
        """
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin)
        if not learner:
            return None

        # Update basic learner fields
        if data.name is not None:
            learner.name = data.name
        if data.age_group is not None:
            learner.age_group = data.age_group
        if data.learning_level is not None:
            learner.learning_level = data.learning_level
        if data.is_active is not None:
            learner.is_active = data.is_active

        # Update profile fields if provided
        if data.profile and learner.profile:
            profile = learner.profile
            p_data = data.profile

            if p_data.communication_preferences is not None:
                profile.communication_preferences = p_data.communication_preferences
                flag_modified(profile, "communication_preferences")

            if p_data.current_skill_level is not None:
                profile.current_skill_level = p_data.current_skill_level
                flag_modified(profile, "current_skill_level")

            if p_data.support_requirements is not None:
                profile.support_requirements = p_data.support_requirements
                flag_modified(profile, "support_requirements")

            if p_data.teacher_constraints is not None:
                profile.teacher_constraints = p_data.teacher_constraints
                flag_modified(profile, "teacher_constraints")

            if p_data.teacher_notes is not None:
                profile.teacher_notes = p_data.teacher_notes

            if p_data.teacher_overrides is not None:
                profile.teacher_overrides = p_data.teacher_overrides
                flag_modified(profile, "teacher_overrides")

        await self.session.commit()
        return await self.get_by_id(learner.id, teacher_id=teacher_id, is_admin=is_admin)

    async def delete(
        self,
        learner_id: uuid.UUID,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> bool:
        """
        Delete learner (cascade deletes learner_profile).
        """
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin)
        if not learner:
            return False

        await self.session.delete(learner)
        await self.session.commit()
        return True

    async def add_observation(
        self,
        learner_id: uuid.UUID,
        observation: LearnerObservationCreate,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Optional[dict]:
        """
        Record a learning pattern observation to the learner profile.
        """
        learner = await self.get_by_id(learner_id, teacher_id=teacher_id, is_admin=is_admin)
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

        # Append to observations list
        current_obs = list(learner.profile.observations)
        current_obs.append(obs_item)
        learner.profile.observations = current_obs
        flag_modified(learner.profile, "observations")

        await self.session.commit()
        return obs_item
