from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import create_access_token, create_refresh_token, verify_password
from app.database.session import get_db_session
from app.users.service import UserService

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=Token)
async def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user_service = UserService(session)
    user = await user_service.get_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Inactive user"
        )
        
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
