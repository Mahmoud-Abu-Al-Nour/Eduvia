import uuid
from datetime import timedelta
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, get_password_hash
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

from datetime import datetime, timedelta, timezone

# Mock user for testing
now = datetime.now(timezone.utc)
mock_user_id = uuid.uuid4()
mock_user = User(
    id=mock_user_id,
    email="teacher@eduvia.app",
    full_name="Alice Teacher",
    hashed_password=get_password_hash("strongpassword123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

# Mock admin user
mock_admin_id = uuid.uuid4()
mock_admin = User(
    id=mock_admin_id,
    email="admin@eduvia.app",
    full_name="Bob Admin",
    hashed_password=get_password_hash("adminpassword123"),
    role=UserRole.admin,
    is_active=True,
    created_at=now,
    updated_at=now,
)

from app.database.session import get_db_session

@pytest.fixture(autouse=True)
def override_db_session():
    async def override_get_db_session():
        yield AsyncMock()
    app.dependency_overrides[get_db_session] = override_get_db_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def mock_user_service():
    mock_user_service = AsyncMock()
    mock_user_service.get_by_email.return_value = mock_user
    mock_user_service.get_by_id.return_value = mock_user
    
    async def override_get_db_session():
        yield AsyncMock()

    app.dependency_overrides[get_db_session] = override_get_db_session
    
    # We also need to patch the UserService instantiation in the routers
    with patch("app.auth.router.UserService", return_value=mock_user_service), \
         patch("app.users.router.UserService", return_value=mock_user_service), \
         patch("app.auth.dependencies.UserService", return_value=mock_user_service):
        yield mock_user_service
    
    app.dependency_overrides.clear()


def test_login_success(mock_user_service):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "teacher@eduvia.app", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(mock_user_service):
    """Test login with wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "teacher@eduvia.app", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_unknown_user(mock_user_service):
    """Test login with unknown user."""
    mock_user_service.get_by_email.return_value = None
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "unknown@eduvia.app", "password": "password"},
    )
    assert response.status_code == 401


def test_protected_endpoint_success(mock_user_service):
    """Test accessing protected endpoint with valid JWT."""
    token = create_access_token(subject=str(mock_user_id))
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "teacher@eduvia.app"


def test_protected_endpoint_missing_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_protected_endpoint_invalid_token():
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401


def test_protected_endpoint_expired_token(mock_user_service):
    """Test accessing protected endpoint with expired token."""
    token = create_access_token(
        subject=str(mock_user_id), expires_delta=timedelta(seconds=-1)
    )
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


def test_role_restriction(mock_user_service):
    """Test admin role restriction."""
    # Teacher tries to access admin-only endpoint (we need an admin endpoint to test)
    # Since we haven't implemented an admin-only endpoint yet, we can test the dependency itself
    from app.auth.dependencies import get_current_active_admin
    import asyncio
    
    with pytest.raises(Exception) as exc_info:
        asyncio.run(get_current_active_admin(current_user=mock_user))
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "The user doesn't have enough privileges"

    # Admin access should pass
    result = asyncio.run(get_current_active_admin(current_user=mock_admin))
    assert result.email == "admin@eduvia.app"
