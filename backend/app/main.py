"""
Eduvia Backend
FastAPI application entry point.
"""
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.database.session import create_db_engine, dispose_db_engine

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup and shutdown logic."""
    configure_logging()
    logger.info(
        "eduvia_startup",
        environment=settings.APP_ENV,
        debug=settings.APP_DEBUG,
    )

    # Create database engine pool
    await create_db_engine()
    logger.info("database_engine_created")

    yield  # ← Application is running

    # Cleanup on shutdown
    await dispose_db_engine()
    logger.info("eduvia_shutdown")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Eduvia API",
        description=(
            "Adaptive educational platform for learners with special educational needs. "
            "Provides curriculum management, learner profiling, activity generation, "
            "and adaptive learning intelligence."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── API Routers ────────────────────────────────────────────────────
    application.include_router(api_router, prefix="/api/v1")

    return application


app = create_application()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: object, exc: Exception) -> JSONResponse:
    """Global fallback exception handler."""
    logger.error("unhandled_exception", error=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
        },
    )
