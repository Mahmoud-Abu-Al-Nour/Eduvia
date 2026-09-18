from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.models import UserRole


class UserBase(BaseModel):
    """Base schema with shared properties."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    role: UserRole = UserRole.teacher
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=2, max_length=255)
    password: str | None = Field(None, min_length=8)
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for returning user data (excluding password)."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
