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
