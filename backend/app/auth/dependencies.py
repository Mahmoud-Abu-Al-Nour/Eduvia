import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.session import get_db_session
from app.users.models import User
from app.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Dependency to get the current authenticated user from the JWT access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id_str = payload.get("sub")
        token_type = payload.get("type")

        if user_id_str is None or token_type != "access":
            raise credentials_exception

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise credentials_exception

    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception

    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


async def get_current_user_optional(
    session: SessionDep,
    token: Annotated[str | None, Depends(oauth2_scheme_optional)] = None,
) -> User | None:
    """
    Optional user dependency. Returns active User if valid bearer token present, else None.
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id_str = payload.get("sub")
        token_type = payload.get("type")
        if user_id_str is None or token_type != "access":
            return None
        user_id = uuid.UUID(user_id_str)
        user_service = UserService(session)
        user = await user_service.get_by_id(user_id)
        if user and user.is_active:
            return user
    except Exception:
        return None
    return None


async def get_current_active_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Dependency to check if the current user is an admin."""
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_teacher(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency to check if the current user is an active teacher or admin.
    Administrators retain administrative access across teacher workflows.
    """
    role_val = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if role_val not in ("teacher", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_learner(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency to check if the current user is an active learner.
    """
    role_val = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if role_val != "learner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have learner privileges"
        )
    return current_user


async def get_current_active_researcher(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency to check if the current user is an active researcher or admin.
    Administrators retain administrative access across research workflows.
    """
    role_val = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if role_val not in ("researcher", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have researcher privileges",
        )
    return current_user


def require_permission(permission: str):
    """
    FastAPI dependency factory enforcing a specific centralized RBAC permission.
    """
    from app.auth.permissions import has_permission

    async def _dependency(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires '{permission}' permission",
            )
        return current_user

    return _dependency

