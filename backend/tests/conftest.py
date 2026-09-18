"""
Pytest configuration for Eduvia backend tests.

Configures test settings, async support, and shared fixtures.
"""
from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# ── Set test environment variables BEFORE importing app settings ──────────────
# This prevents the app from trying to read a .env file during tests
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("APP_DEBUG", "true")
os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://eduvia:eduvia_password@localhost:5432/eduvia_test",
)
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("QDRANT_API_KEY", "")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key-placeholder")
os.environ.setdefault("GEMINI_MODEL", "gemini-2.0-flash-exp")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-for-testing-only-minimum-32-chars")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("CORS_ORIGINS_RAW", "http://localhost:5173")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def app() -> Any:
    """Create the FastAPI application for testing."""
    # Clear settings cache to pick up test environment variables
    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.main import create_application
    application = create_application()
    return application


@pytest_asyncio.fixture(scope="session")
async def client(app: Any) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client for API tests.

    Uses httpx with ASGITransport to test FastAPI without
    starting a real server.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
