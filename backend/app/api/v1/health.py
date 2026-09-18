"""
Eduvia — Health Check Endpoints

Provides system health information including:
- Application status
- Database connectivity
- Qdrant connectivity
- AI provider status

Used by:
- Docker Compose healthcheck
- Load balancer health probes
- Frontend connectivity verification
- Monitoring systems
"""
import platform
import time
from typing import Any

import structlog
from fastapi import APIRouter

from app.ai.orchestrator.orchestrator import get_ai_orchestrator
from app.database.init_db import check_db_connectivity
from app.knowledge.qdrant_client import get_qdrant_client

logger = structlog.get_logger(__name__)
router = APIRouter()

# Track application start time for uptime calculation
_start_time = time.time()


@router.get(
    "",
    summary="Basic health check",
    description="Returns application status. Used by load balancers and Docker healthchecks.",
    response_model=dict[str, Any],
)
async def health_check() -> dict[str, Any]:
    """
    Basic health check — fast response for load balancer probes.

    Returns:
        Application name, version, and status.
    """
    return {
        "status": "ok",
        "service": "eduvia-api",
        "version": "0.1.0",
    }


@router.get(
    "/detailed",
    summary="Detailed health check",
    description=(
        "Returns detailed health status including database, Qdrant, and AI provider. "
        "May be slower due to connectivity checks."
    ),
    response_model=dict[str, Any],
)
async def detailed_health_check() -> dict[str, Any]:
    """
    Detailed health check with dependency status.

    Checks all external dependencies and returns their status.
    Does NOT expose sensitive configuration details.
    """
    uptime_seconds = time.time() - _start_time

    # Check database
    db_healthy = await check_db_connectivity()

    # Check Qdrant
    qdrant = get_qdrant_client()
    qdrant_healthy = await qdrant.health_check()

    # Check AI provider
    orchestrator = get_ai_orchestrator()
    ai_status = await orchestrator.health_check()

    overall_healthy = db_healthy and qdrant_healthy

    logger.info(
        "detailed_health_check",
        db_healthy=db_healthy,
        qdrant_healthy=qdrant_healthy,
        ai_configured=ai_status.get("configured"),
        uptime_seconds=uptime_seconds,
    )

    return {
        "status": "ok" if overall_healthy else "degraded",
        "service": "eduvia-api",
        "version": "0.1.0",
        "uptime_seconds": round(uptime_seconds, 2),
        "python_version": platform.python_version(),
        "dependencies": {
            "database": {
                "status": "ok" if db_healthy else "unreachable",
                "healthy": db_healthy,
            },
            "qdrant": {
                "status": "ok" if qdrant_healthy else "unreachable",
                "healthy": qdrant_healthy,
            },
            "ai_provider": {
                "provider": ai_status.get("provider"),
                "configured": ai_status.get("configured"),
                "healthy": ai_status.get("healthy"),
            },
        },
    }
