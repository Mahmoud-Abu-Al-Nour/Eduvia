"""
Eduvia — Phase 11 Hardening & Security Tests
Tests for security headers, CORS restrictions, production docs exposure,
in-memory rate limiting, and role-based authorization dependencies.
"""
import uuid
import pytest
from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_active_teacher, get_current_user
from app.core.config import settings
from app.core.rate_limit import (
    InMemoryRateLimiter,
    activity_evaluate_rate_limiter,
    activity_generate_rate_limiter,
    login_rate_limiter,
)
from app.main import app, create_application
from app.users.models import User, UserRole


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_global_rate_limiters():
    """Ensure all rate limiters are reset before and after each test."""
    login_rate_limiter.reset()
    activity_generate_rate_limiter.reset()
    activity_evaluate_rate_limiter.reset()
    yield
    login_rate_limiter.reset()
    activity_generate_rate_limiter.reset()
    activity_evaluate_rate_limiter.reset()


@pytest.fixture
def test_client():
    return TestClient(app)


# ── 1. Security Headers Tests ──────────────────────────────────────────────────

def test_security_headers_present_on_response(test_client):
    """Verify standard security headers are attached to API responses."""
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    headers = response.headers

    # Defense-in-depth headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert headers.get("X-XSS-Protection") == "0"

    # CSP header
    csp = headers.get("Content-Security-Policy", "")
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "https://fonts.googleapis.com" in csp

    # In development, HSTS is omitted
    assert "Strict-Transport-Security" not in headers


def test_hsts_enabled_in_production(monkeypatch):
    """Verify HSTS is included when APP_ENV is production."""
    monkeypatch.setattr(settings, "APP_ENV", "production")
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "Strict-Transport-Security" in response.headers
    assert "max-age=31536000" in response.headers["Strict-Transport-Security"]


# ── 2. Production Documentation Exposure Tests ────────────────────────────────

def test_docs_available_in_development():
    """Verify Swagger/OpenAPI docs are accessible in development mode."""
    dev_app = create_application()
    client = TestClient(dev_app)
    
    docs_resp = client.get("/docs")
    assert docs_resp.status_code == 200

    openapi_resp = client.get("/openapi.json")
    assert openapi_resp.status_code == 200


def test_docs_disabled_in_production(monkeypatch):
    """Verify Swagger/OpenAPI docs return 404 in production mode."""
    monkeypatch.setattr(settings, "APP_ENV", "production")
    prod_app = create_application()
    client = TestClient(prod_app)

    docs_resp = client.get("/docs")
    assert docs_resp.status_code == 404

    redoc_resp = client.get("/redoc")
    assert redoc_resp.status_code == 404

    openapi_resp = client.get("/openapi.json")
    assert openapi_resp.status_code == 404


# ── 3. CORS Hardening Tests ───────────────────────────────────────────────────

def test_cors_preflight_allowed_methods(test_client):
    """Verify CORS preflight succeeds for allowed methods and headers."""
    response = test_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )
    assert response.status_code == 200
    allow_methods = response.headers.get("Access-Control-Allow-Methods", "")
    assert "GET" in allow_methods
    assert "POST" in allow_methods
    assert "PUT" in allow_methods
    assert "PATCH" in allow_methods
    assert "DELETE" in allow_methods
    assert "OPTIONS" in allow_methods
    # Verify wildcard methods are NOT used
    assert allow_methods != "*"


def test_cors_preflight_disallowed_origin(test_client):
    """Verify unauthorized origins do not receive allow origin headers."""
    response = test_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://malicious-site.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("Access-Control-Allow-Origin") != "http://malicious-site.com"


# ── 4. In-Memory Rate Limiter Unit Tests ──────────────────────────────────────

def test_rate_limiter_under_threshold():
    """Verify requests under the limit are allowed."""
    limiter = InMemoryRateLimiter(max_requests=3, window_seconds=60)
    limiter.check("client-1")
    limiter.check("client-1")
    limiter.check("client-1")
    assert limiter.tracked_keys_count == 1


def test_rate_limiter_threshold_exceeded():
    """Verify exceeding the limit raises HTTP 429 with Retry-After."""
    current_time = 1000.0
    limiter = InMemoryRateLimiter(
        max_requests=2,
        window_seconds=60,
        time_func=lambda: current_time,
    )

    limiter.check("user-100")
    limiter.check("user-100")

    with pytest.raises(Exception) as exc_info:
        limiter.check("user-100")

    assert exc_info.value.status_code == 429
    assert "Retry-After" in exc_info.value.headers
    assert int(exc_info.value.headers["Retry-After"]) >= 1


def test_rate_limiter_separate_buckets():
    """Verify separate keys do not share or collide in rate buckets."""
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)

    # user-a consumes limit
    limiter.check("user-a")
    limiter.check("user-a")

    # user-b is unaffected
    limiter.check("user-b")
    limiter.check("user-b")

    # user-a fails
    with pytest.raises(Exception) as exc_info:
        limiter.check("user-a")
    assert exc_info.value.status_code == 429


def test_rate_limiter_sliding_window_expiry():
    """Verify that older requests expire and allow new requests after the window."""
    current_time = 1000.0
    limiter = InMemoryRateLimiter(
        max_requests=2,
        window_seconds=10,
        time_func=lambda: current_time,
    )

    limiter.check("client-x")
    limiter.check("client-x")

    with pytest.raises(Exception):
        limiter.check("client-x")

    # Advance time beyond window
    current_time = 1011.0
    # Should succeed now
    limiter.check("client-x")


def test_rate_limiter_stale_eviction():
    """Verify that stale entries are pruned when capacity limit is reached."""
    current_time = 1000.0
    limiter = InMemoryRateLimiter(
        max_requests=5,
        window_seconds=10,
        max_entries=2,
        time_func=lambda: current_time,
    )

    limiter.check("key-1")
    limiter.check("key-2")
    assert limiter.tracked_keys_count == 2

    # Advance time so key-1 and key-2 become stale
    current_time = 1015.0
    limiter.check("key-3")
    # key-1 and key-2 should have been evicted
    assert limiter.tracked_keys_count <= 2


# ── 5. API Endpoint Rate Limiting Tests ────────────────────────────────────────

def test_login_rate_limiting_enforcement(test_client):
    """Verify that rapid successive login attempts trigger HTTP 429."""
    from unittest.mock import AsyncMock, MagicMock
    from app.database.session import get_db_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    app.dependency_overrides[get_db_session] = lambda: mock_session

    try:
        # Custom client IP to isolate test
        headers = {"X-Forwarded-For": "203.0.113.195"}

        for _ in range(5):
            resp = test_client.post(
                "/api/v1/auth/login",
                data={"username": "nobody@example.com", "password": "wrongpassword"},
                headers=headers,
            )
            assert resp.status_code in (401, 422)

        # 6th request should exceed 5/min limit
        throttled_resp = test_client.post(
            "/api/v1/auth/login",
            data={"username": "nobody@example.com", "password": "wrongpassword"},
            headers=headers,
        )
        assert throttled_resp.status_code == 429
        assert "Retry-After" in throttled_resp.headers
    finally:
        app.dependency_overrides.pop(get_db_session, None)


def test_activity_evaluation_rate_limiting(test_client):
    """Verify that activity evaluation is rate limited to prevent automated abuse."""
    from unittest.mock import AsyncMock, MagicMock
    from app.database.session import get_db_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    app.dependency_overrides[get_db_session] = lambda: mock_session

    headers = {"X-Forwarded-For": "203.0.113.196"}

    # Temporarily set limit to 3 for fast deterministic testing
    original_limit = activity_evaluate_rate_limiter.max_requests
    activity_evaluate_rate_limiter.max_requests = 3
    try:
        payload = {
            "activity_id": str(uuid.uuid4()),
            "objective_id": str(uuid.uuid4()),
            "activity_type": "multiple_choice",
            "submission": {
                "activity_type": "multiple_choice",
                "selected_option_id": "opt-1",
            },
            "activity_content": {
                "activity_type": "multiple_choice",
                "question": "What is 2 + 2?",
                "options": [
                    {"id": "opt-1", "text": "4", "is_correct": True},
                    {"id": "opt-2", "text": "5", "is_correct": False},
                ],
                "correct_answer_id": "opt-1",
                "explanation": "Two plus two equals four.",
            },
        }

        for _ in range(3):
            resp = test_client.post(
                "/api/v1/activities/evaluate",
                json=payload,
                headers=headers,
            )
            assert resp.status_code in (200, 422)

        # 4th request must be throttled
        throttled = test_client.post(
            "/api/v1/activities/evaluate",
            json=payload,
            headers=headers,
        )
        assert throttled.status_code == 429
        assert "Retry-After" in throttled.headers
    finally:
        activity_evaluate_rate_limiter.max_requests = original_limit
        app.dependency_overrides.pop(get_db_session, None)


def test_activity_generation_rate_limiting(test_client):
    """Verify that activity generation by teacher identity is rate limited."""
    from unittest.mock import AsyncMock, MagicMock
    from app.database.session import get_db_session

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    app.dependency_overrides[get_db_session] = lambda: mock_session

    teacher_user = User(
        id=uuid.uuid4(),
        email="teacher.gen@example.com",
        full_name="Teacher Gen",
        hashed_password="hash",
        role=UserRole.teacher,
        is_active=True,
    )
    app.dependency_overrides[get_current_user] = lambda: teacher_user

    original_limit = activity_generate_rate_limiter.max_requests
    activity_generate_rate_limiter.max_requests = 2
    try:
        payload = {
            "objective_id": str(uuid.uuid4()),
            "difficulty_level": 1,
            "language": "en",
        }

        for _ in range(2):
            resp = test_client.post(
                "/api/v1/activities/generate",
                json=payload,
            )
            assert resp.status_code in (200, 404, 422, 500)

        # 3rd request must be throttled
        throttled = test_client.post(
            "/api/v1/activities/generate",
            json=payload,
        )
        assert throttled.status_code == 429
        assert "Retry-After" in throttled.headers
    finally:
        activity_generate_rate_limiter.max_requests = original_limit
        app.dependency_overrides.pop(get_db_session, None)
        app.dependency_overrides.pop(get_current_user, None)


# ── 6. Teacher Authorization Dependency Tests ─────────────────────────────────

@pytest.mark.asyncio
async def test_get_current_active_teacher_success():
    """Verify that an active teacher passes the dependency."""
    teacher = User(
        id=uuid.uuid4(),
        email="teacher@example.com",
        full_name="Teacher Sam",
        hashed_password="hash",
        role=UserRole.teacher,
        is_active=True,
    )
    result = await get_current_active_teacher(current_user=teacher)
    assert result == teacher


@pytest.mark.asyncio
async def test_get_current_active_teacher_admin_allowed():
    """Verify that an active administrator also passes teacher dependency."""
    admin = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hash",
        role=UserRole.admin,
        is_active=True,
    )
    result = await get_current_active_teacher(current_user=admin)
    assert result == admin


@pytest.mark.asyncio
async def test_get_current_active_teacher_invalid_role():
    """Verify that a user with an unauthorized role is rejected with 403."""
    class FakeUser:
        role = type("Role", (), {"value": "student"})()
        is_active = True

    with pytest.raises(Exception) as exc_info:
        await get_current_active_teacher(current_user=FakeUser())
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "The user doesn't have enough privileges"
