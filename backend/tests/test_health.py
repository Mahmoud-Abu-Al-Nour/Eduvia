"""
Tests for health check endpoints.

These tests verify:
1. Basic health endpoint returns 200
2. Response schema is correct
3. Service name and version are present
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_basic_health_check(client: AsyncClient) -> None:
    """Basic health endpoint should return 200 with status ok."""
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "eduvia-api"
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check_response_schema(client: AsyncClient) -> None:
    """Health endpoint response must include all required fields."""
    response = await client.get("/api/v1/health")
    data = response.json()

    required_fields = {"status", "service", "version"}
    assert required_fields.issubset(data.keys()), (
        f"Missing fields: {required_fields - data.keys()}"
    )


@pytest.mark.asyncio
async def test_detailed_health_check_returns_200(client: AsyncClient) -> None:
    """
    Detailed health endpoint should return 200 even when dependencies are down.

    In a test environment without a running database/Qdrant, the status
    may be 'degraded' but the HTTP status code should still be 200.
    """
    response = await client.get("/api/v1/health/detailed")

    assert response.status_code == 200
    data = response.json()

    # Status is either 'ok' or 'degraded' depending on dependency availability
    assert data["status"] in ("ok", "degraded")
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert "qdrant" in data["dependencies"]
    assert "ai_provider" in data["dependencies"]


@pytest.mark.asyncio
async def test_detailed_health_check_dependency_schema(client: AsyncClient) -> None:
    """Dependency status objects must have required fields."""
    response = await client.get("/api/v1/health/detailed")
    data = response.json()

    db_status = data["dependencies"]["database"]
    assert "status" in db_status
    assert "healthy" in db_status
    assert isinstance(db_status["healthy"], bool)

    ai_status = data["dependencies"]["ai_provider"]
    assert "provider" in ai_status
    assert "configured" in ai_status
    assert "healthy" in ai_status


@pytest.mark.asyncio
async def test_nonexistent_endpoint_returns_404(client: AsyncClient) -> None:
    """Non-existent endpoints should return 404."""
    response = await client.get("/api/v1/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_api_docs_accessible(client: AsyncClient) -> None:
    """API documentation should be accessible."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_schema_accessible(client: AsyncClient) -> None:
    """OpenAPI schema endpoint should return valid JSON."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Eduvia API"
