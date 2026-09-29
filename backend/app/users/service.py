"""
Eduvia — User Service Layer
"""
from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash
from app.users.models import User, UserRole
from app.users.schemas import UserAdminUpdate, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Get a user by ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        role: UserRole | None = None,
    ) -> Sequence[User]:
        """Get multiple users with optional role filtering."""
        query = select(User)
        if role is not None:
            query = query.where(User.role == role)
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, user_in: UserCreate) -> User:
        """Create a new user."""
        db_obj = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role,
            is_active=user_in.is_active,
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: User, user_in: UserUpdate | UserAdminUpdate) -> User:
        """Update a user."""
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, user_id: uuid.UUID) -> User | None:
        """Delete a user."""
        db_obj = await self.get_by_id(user_id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.commit()
        return db_obj

    async def get_platform_stats(self) -> dict[str, int]:
        """Compute platform-wide KPIs for administrative oversight."""
        from app.analytics.models import PerformanceEvent
        from app.curriculum.models import Curriculum
        from app.learners.models import Learner

        total_users = (await self.session.execute(select(func.count(User.id)))).scalar_one() or 0
        total_admins = (
            await self.session.execute(select(func.count(User.id)).where(User.role == UserRole.admin))
        ).scalar_one() or 0
        total_teachers = (
            await self.session.execute(select(func.count(User.id)).where(User.role == UserRole.teacher))
        ).scalar_one() or 0
        total_learners = (
            await self.session.execute(select(func.count(Learner.id)))
        ).scalar_one() or 0
        total_curricula = (
            await self.session.execute(select(func.count(Curriculum.id)))
        ).scalar_one() or 0
        total_activities_completed = (
            await self.session.execute(select(func.count(PerformanceEvent.id)))
        ).scalar_one() or 0

        return {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_teachers": total_teachers,
            "total_learners": total_learners,
            "total_curricula": total_curricula,
            "total_activities_completed": total_activities_completed,
        }
