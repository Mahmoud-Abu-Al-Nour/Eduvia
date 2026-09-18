"""
Eduvia — Database Initialization

Utilities for creating tables and verifying database connectivity.
Used during development startup and testing.
"""
import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database.base import EduviaBase
from app.database.session import get_engine

logger = structlog.get_logger(__name__)


async def init_db() -> None:
    """
    Initialize the database schema.

    Creates all tables defined in ORM models if they do not exist.
    In production, use Alembic migrations instead.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await _create_tables(conn)
    logger.info("database_initialized")


async def _create_tables(conn: AsyncConnection) -> None:
    """Create all SQLAlchemy-managed tables."""
    await conn.run_sync(EduviaBase.metadata.create_all)


async def check_db_connectivity() -> bool:
    """
    Verify database connectivity by executing a simple query.

    Returns:
        True if the database is reachable, False otherwise.
    """
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning("database_connectivity_check_failed", error=str(e))
        return False
