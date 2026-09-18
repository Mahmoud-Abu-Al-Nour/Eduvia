import uuid
from datetime import timedelta

import jwt
import pytest
from passlib.context import CryptContext

from app.auth.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_password_hashing() -> None:
    """Test that password hashing and verification works."""
    password = "supersecretpassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token() -> None:
    """Test creating a JWT access token."""
    user_id = str(uuid.uuid4())
    token = create_access_token(subject=user_id)
    
    # Verify token manually
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert payload["sub"] == user_id
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_refresh_token() -> None:
    """Test creating a JWT refresh token."""
    user_id = str(uuid.uuid4())
    token = create_refresh_token(subject=user_id)
    
    # Verify token manually
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert payload["sub"] == user_id
    assert payload["type"] == "refresh"
    assert "exp" in payload


def test_access_token_custom_expiry() -> None:
    """Test access token with custom expiry."""
    user_id = str(uuid.uuid4())
    expires_delta = timedelta(minutes=5)
    
    token = create_access_token(subject=user_id, expires_delta=expires_delta)
    
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert payload["sub"] == user_id
