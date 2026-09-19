"""
Eduvia — Database Session Management

Provides async SQLAlchemy engine and session factory.
Uses asyncpg driver for PostgreSQL.
"""
from collections.abc import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Module-level engine and session factory — initialized on app startup
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


async def create_db_engine() -> None:
    """
    Create the async database engine and session factory.
    Called once on application startup via lifespan.
    """
    global _engine, _async_session_factory

    _engine = create_async_engine(
        settings.effective_database_url,
        echo=settings.APP_DEBUG,  # Log SQL in debug mode only
        pool_pre_ping=True,        # Verify connections before use
        pool_size=5,
        max_overflow=10,
    )

    _async_session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    logger.info("database_engine_created", url=_redact_db_url(settings.effective_database_url))


async def dispose_db_engine() -> None:
    """Dispose the database engine on application shutdown."""
    global _engine
    if _engine:
        await _engine.dispose()
        logger.info("database_engine_disposed")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency — yields an async database session.

    Usage in route handlers:
        async def my_route(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    if _async_session_factory is None:
        raise RuntimeError("Database engine not initialized. Was create_db_engine() called?")

    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_engine() -> AsyncEngine:
    """Return the current engine instance (for admin operations like migrations)."""
    if _engine is None:
        raise RuntimeError("Database engine not initialized.")
    return _engine


def _redact_db_url(url: str) -> str:
    """Redact password from database URL for safe logging."""
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        if parsed.password:
            netloc = parsed.netloc.replace(f":{parsed.password}@", ":***@")
            return urlunparse(parsed._replace(netloc=netloc))
    except Exception:  # noqa: BLE001
        pass
    return "***"
