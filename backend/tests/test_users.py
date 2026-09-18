import pytest
from pydantic import ValidationError

from app.users.models import UserRole
from app.users.schemas import UserCreate, UserUpdate


def test_user_create_schema_valid() -> None:
    """Test valid UserCreate schema."""
    user = UserCreate(
        email="teacher@eduvia.app",
        full_name="Alice Teacher",
        password="strongpassword123",
        role=UserRole.teacher,
    )
    assert user.email == "teacher@eduvia.app"
    assert user.full_name == "Alice Teacher"
    assert user.role == UserRole.teacher
    assert user.is_active is True


def test_user_create_schema_invalid_email() -> None:
    """Test invalid email in UserCreate."""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            email="not-an-email",
            full_name="Alice Teacher",
            password="strongpassword123",
        )
    assert "value is not a valid email address" in str(exc_info.value).lower()


def test_user_create_schema_short_password() -> None:
    """Test short password in UserCreate."""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            email="teacher@eduvia.app",
            full_name="Alice Teacher",
            password="short",
        )
    assert "string should have at least 8 characters" in str(exc_info.value).lower()


def test_user_update_schema() -> None:
    """Test UserUpdate schema allows partial updates."""
    # Only update name
    update1 = UserUpdate(full_name="Bob Admin")
    assert update1.full_name == "Bob Admin"
    assert update1.email is None
    
    # Update multiple fields
    update2 = UserUpdate(
        email="new@eduvia.app",
        is_active=False
    )
    assert update2.email == "new@eduvia.app"
    assert update2.is_active is False
    assert update2.full_name is None
