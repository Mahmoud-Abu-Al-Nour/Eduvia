import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


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

    async def get_multi(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """Get multiple users."""
        result = await self.session.execute(select(User).offset(skip).limit(limit))
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

    async def update(self, db_obj: User, user_in: UserUpdate) -> User:
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
        """Delete a user (soft delete is preferred, but this is a hard delete)."""
        db_obj = await self.get_by_id(user_id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.commit()
        return db_obj
