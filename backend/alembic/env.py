"""
Alembic migration environment configuration.

Reads DATABASE_URL from environment to support different
environments (dev, staging, prod) without hardcoded strings.
"""
from __future__ import annotations

from logging.config import fileConfig

from alembic import context

# Import all models so Alembic can detect them for autogenerate
# As models are added in later phases, import them here:
from app.database.base import EduviaBase  # noqa: F401
from sqlalchemy import engine_from_config, pool

from app.users.models import User  # Phase 1
from app.curriculum.models import Curriculum, Subject, Unit, Lesson, LearningObjective  # Phase 2
from app.learners.models import Learner, LearnerProfile  # Phase 3
# from app.activities.models import Activity, ActivityAttempt  # Phase 4
# from app.analytics.models import PerformanceEvent  # Phase 6

config = context.config

# Set DATABASE_URL from environment variable
# This overrides the placeholder in alembic.ini
from app.core.config import settings

database_url = settings.DATABASE_URL
if not database_url:
    raise ValueError(
        "DATABASE_URL environment variable must be set for Alembic migrations. "
        "Copy .env.example to .env and fill in the database URL."
    )

# asyncpg is async-only — use the sync psycopg2 URL for Alembic
# Replace asyncpg driver with psycopg2 for synchronous migration execution
sync_url = database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
config.set_main_option("sqlalchemy.url", sync_url)

# Configure logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = EduviaBase.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Generates SQL scripts without connecting to the database.
    Useful for reviewing migrations before applying them.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Connects to the database and applies migrations directly.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
