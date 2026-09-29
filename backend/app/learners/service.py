"""
Eduvia -- Learner Service Layer (Phase 3 & RBAC Extension)

Encapsulates all database operations for Learners and Learner Profiles.
Maintains teacher ownership isolation, admin platform visibility,
and authenticated learner self-access.
"""
from __future__ import annotations

import copy
import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.auth.permissions import get_user_role
from app.learners.models import Learner, LearnerProfile
from app.learners.schemas import (
    LearnerCreate,
    LearnerObservationCreate,
    LearnerUpdate,
)
from app.users.models import User, UserRole


class LearnerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_learners(
        self,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
        current_user: Optional[User] = None,
    ) -> list[Learner]:
        """
        List learners according to requester scope:
        - Admin: receives all registered learners.
        - Teacher: receives only assigned learners.
        - Learner: receives only their own learner record.
        """
        stmt = (
            select(Learner)
            .options(selectinload(Learner.profile))
            .order_by(Learner.created_at.desc())
        )

        if current_user:
            role = get_user_role(current_user)
            if role == UserRole.admin:
                pass
            elif role == UserRole.teacher:
                stmt = stmt.where(Learner.teacher_id == current_user.id)
            elif role == UserRole.learner:
                stmt = stmt.where(Learner.user_id == current_user.id)
            else:
                return []
        elif is_admin:
            pass
        elif teacher_id is not None:
            stmt = stmt.where(Learner.teacher_id == teacher_id)
        else:
            return []

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(
        self,
        learner_id: uuid.UUID,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
        current_user: Optional[User] = None,
    ) -> Optional[Learner]:
        """
        Retrieve a learner with full profile.
        Enforces server-side IDOR protection:
        - Admin: Full access.
        - Teacher: Authorized only if learner.teacher_id == teacher.id.
        - Learner: Authorized only if learner.user_id == user.id.
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

        if current_user:
            role = get_user_role(current_user)
            if role == UserRole.admin:
                return learner
            elif role == UserRole.teacher:
                if learner.teacher_id != current_user.id:
                    return None
            elif role == UserRole.learner:
                if learner.user_id != current_user.id:
                    return None
            else:
                return None
        elif not is_admin:
            if teacher_id is not None and learner.teacher_id != teacher_id:
                return None
            elif teacher_id is None:
                return None

        return learner

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Learner]:
        """Retrieve learner record linked to an authenticated User account."""
        stmt = (
            select(Learner)
            .options(selectinload(Learner.profile))
            .where(Learner.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        data: LearnerCreate,
        teacher_id: Optional[uuid.UUID] = None,
        user_id: Optional[uuid.UUID] = None,
    ) -> Learner:
        """
        Create a new learner and initialize their associated LearnerProfile.
        """
        learner = Learner(
            name=data.name,
            age_group=data.age_group,
            learning_level=data.learning_level,
            teacher_id=teacher_id,
            user_id=data.user_id or user_id,
        )

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

        return await self.get_by_id(learner.id, is_admin=True)  # type: ignore

    async def update(
        self,
        learner_id: uuid.UUID,
        data: LearnerUpdate,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
        current_user: Optional[User] = None,
    ) -> Optional[Learner]:
        """
        Update learner metadata and/or profile fields.
        Enforces scope rules: learners can only edit allowed personal preferences.
        """
        learner = await self.get_by_id(
            learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user
        )
        if not learner:
            return None

        is_learner_role = False
        if current_user:
            role = get_user_role(current_user)
            if role == UserRole.learner:
                is_learner_role = True

        if is_learner_role:
            # Learner self-update: allowed personal preferences only
            if data.profile and learner.profile:
                profile = learner.profile
                p_data = data.profile

                if p_data.communication_preferences is not None:
                    profile.communication_preferences = {
                        **profile.communication_preferences,
                        **p_data.communication_preferences,
                    }
                    flag_modified(profile, "communication_preferences")

                if p_data.support_requirements is not None:
                    # Allow sensory and pacing accommodations
                    profile.support_requirements = {
                        **profile.support_requirements,
                        **p_data.support_requirements,
                    }
                    flag_modified(profile, "support_requirements")

            await self.session.commit()
            return await self.get_by_id(learner.id, current_user=current_user)

        # Teacher / Admin update:
        if data.name is not None:
            learner.name = data.name
        if data.age_group is not None:
            learner.age_group = data.age_group
        if data.learning_level is not None:
            learner.learning_level = data.learning_level
        if data.is_active is not None:
            learner.is_active = data.is_active
        if data.user_id is not None:
            learner.user_id = data.user_id

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
        return await self.get_by_id(
            learner.id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user
        )

    async def delete(
        self,
        learner_id: uuid.UUID,
        teacher_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
        current_user: Optional[User] = None,
    ) -> bool:
        """
        Delete learner (cascade deletes learner_profile). Learners cannot delete.
        """
        if current_user:
            role = get_user_role(current_user)
            if role == UserRole.learner:
                return False

        learner = await self.get_by_id(
            learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user
        )
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
        current_user: Optional[User] = None,
    ) -> Optional[dict]:
        """
        Record a learning pattern observation to the learner profile. Learners cannot record teacher observations.
        """
        if current_user:
            role = get_user_role(current_user)
            if role == UserRole.learner:
                return None

        learner = await self.get_by_id(
            learner_id, teacher_id=teacher_id, is_admin=is_admin, current_user=current_user
        )
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

        current_obs = list(learner.profile.observations)
        current_obs.append(obs_item)
        learner.profile.observations = current_obs
        flag_modified(learner.profile, "observations")

        await self.session.commit()
        return obs_item
