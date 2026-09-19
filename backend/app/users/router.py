from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.users.models import User
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: SessionDep,
) -> User:
    """
    Register a new user.
    """
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
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Update current user.
    """
    user_service = UserService(session)
    if user_in.email and user_in.email != current_user.email:
        existing_user = await user_service.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists.",
            )

    return await user_service.update(db_obj=current_user, user_in=user_in)
