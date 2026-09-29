"""
Eduvia — User Management & Administration API Router

Provides user self-management and administrative user administration:
- Self profile read/update (without privilege escalation)
- Admin user listing, role management, deactivation
- Platform-wide administrative KPI statistics
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    get_current_active_admin,
    get_current_user,
    get_current_user_optional,
    require_permission,
)
from app.auth.permissions import Permission, get_user_role
from app.database.session import get_db_session
from app.users.models import User, UserRole
from app.users.schemas import (
    PlatformStatsResponse,
    UserAdminUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.users.service import UserService

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: SessionDep,
    current_user: User | None = Depends(get_current_user_optional),
) -> User:
    """
    Register a new user.
    Non-admin callers cannot create admin accounts.
    """
    is_admin = current_user is not None and get_user_role(current_user) == UserRole.admin
    if not is_admin and user_in.role == UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privilege required to create admin accounts.",
        )

    user_service = UserService(session)
    user = await user_service.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    return await user_service.create(user_in)


@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Update current user profile.
    Prevents self-modification of roles or active status.
    """
    user_service = UserService(session)
    if user_in.email and user_in.email != current_user.email:
        existing_user = await user_service.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists.",
            )

    # Self-update cannot alter role or is_active
    sanitized_in = user_in.model_copy(update={"role": None, "is_active": None})
    return await user_service.update(db_obj=current_user, user_in=sanitized_in)


@router.get("/platform/stats", response_model=PlatformStatsResponse)
async def get_platform_stats(
    session: SessionDep,
    current_user: Annotated[User, Depends(require_permission(Permission.ADMIN_DASHBOARD))],
) -> PlatformStatsResponse:
    """Platform-wide statistics for Admin dashboard."""
    user_service = UserService(session)
    stats = await user_service.get_platform_stats()
    return PlatformStatsResponse(**stats)


@router.get("/", response_model=list[UserResponse])
async def list_users(
    session: SessionDep,
    current_user: Annotated[User, Depends(require_permission(Permission.USERS_READ_GLOBAL))],
    role: UserRole | None = Query(default=None, description="Filter users by role"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[User]:
    """List all platform users with optional role filtering. Admin only."""
    user_service = UserService(session)
    users = await user_service.get_multi(skip=skip, limit=limit, role=role)
    return list(users)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Retrieve user details by ID. Accessible to Admin or self."""
    role = get_user_role(current_user)
    if role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to other user accounts is unauthorized.",
        )
    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def admin_update_user(
    user_id: uuid.UUID,
    user_in: UserAdminUpdate,
    session: SessionDep,
    current_user: Annotated[User, Depends(require_permission(Permission.ROLES_MANAGE))],
) -> User:
    """Update user role, active status, or details. Admin only."""
    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return await user_service.update(db_obj=user, user_in=user_in)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(require_permission(Permission.USERS_MANAGE))],
) -> User:
    """Delete or deactivate user. Admin only."""
    user_service = UserService(session)
    user = await user_service.delete(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user
