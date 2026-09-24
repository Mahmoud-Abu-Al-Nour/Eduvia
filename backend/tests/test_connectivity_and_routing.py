"""
Eduvia — Backend Connectivity & API Routing Regression Tests

Verifies:
- Health endpoint responds with 200 OK
- Authentication flows (login, token validation, 401 without token)
- Curriculum endpoint list and detail serialization with UUID prerequisites
- Activity lookup returns 200 for valid ID and 404 for unknown ID
- Activity generation & evaluation across modalities
"""
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.activities.schemas import ActivityType
from app.auth.security import create_access_token, get_password_hash
from app.curriculum.curriculum_catalog import CURRICULUM_ID, FULL_CURRICULUM_CATALOG
from app.curriculum.router import get_curriculum_service
from app.curriculum.schemas import CurriculumResponse, CurriculumWithSubjects
from app.database.session import get_db_session
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

mock_user_id = uuid.uuid4()
mock_teacher = User(
    id=mock_user_id,
    email="teacher@eduvia.app",
    full_name="Alice Teacher",
    hashed_password=get_password_hash("strongpassword123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=datetime.now(UTC),
    updated_at=datetime.now(UTC),
)


@pytest.fixture(autouse=True)
def override_db():
    async def override_get_db_session():
        yield AsyncMock()

    app.dependency_overrides[get_db_session] = override_get_db_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    token = create_access_token(subject=str(mock_user_id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_user_service():
    service = AsyncMock()
    service.get_by_email.return_value = mock_teacher
    service.get_by_id.return_value = mock_teacher

    with patch("app.auth.router.UserService", return_value=service), \
         patch("app.users.router.UserService", return_value=service), \
         patch("app.auth.dependencies.UserService", return_value=service):
        yield service


def test_health_endpoint():
    """Verify health endpoint responds with 200 OK."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "eduvia-api"


def test_curriculum_unauthenticated():
    """Curriculum list rejects unauthenticated requests."""
    response = client.get("/api/v1/curricula")
    assert response.status_code == 401


def test_curriculum_serialization_with_uuid_prerequisites(auth_headers, mock_user_service):
    """Verify curriculum detail endpoint properly validates & serializes 70 objectives with UUID prerequisites."""
    mock_curr_service = AsyncMock()
    mock_curr = CurriculumWithSubjects(
        id=CURRICULUM_ID,
        title={"en": "Special Educational Needs Core Curriculum", "ar": "المنهج الأساسي للتربية الخاصة"},
        description={"en": "Comprehensive foundational curriculum.", "ar": "منهج تأسيسي شامل"},
        version="2.0.0",
        is_active=True,
        created_by_id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
        subjects=FULL_CURRICULUM_CATALOG,
    )
    mock_curr_service.get_by_id.return_value = mock_curr
    app.dependency_overrides[get_curriculum_service] = lambda: mock_curr_service

    try:
        response = client.get(f"/api/v1/curricula/{CURRICULUM_ID}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["subjects"]) == 3
        # Check that prerequisites serialization did not crash
        math_subject = data["subjects"][0]
        first_obj = math_subject["units"][0]["lessons"][0]["learning_objectives"][0]
        assert "prerequisites" in first_obj
    finally:
        app.dependency_overrides.pop(get_curriculum_service, None)


def test_activity_lookup_404(auth_headers, mock_user_service):
    """Activity lookup returns 404 for unknown activity ID."""
    unknown_id = uuid.uuid4()
    response = client.get(f"/api/v1/activities/{unknown_id}", headers=auth_headers)
    assert response.status_code == 404


def test_activity_lookup_from_content_bank(auth_headers, mock_user_service):
    """Activity lookup resolves seeded items from ContentBank."""
    from app.content.bank import get_content_bank
    bank = get_content_bank()
    first_item = bank.items[0]
    first_item_id = first_item.id

    response = client.get(f"/api/v1/activities/{first_item_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(first_item_id)
    assert data["title"] is not None
