"""
Eduvia — Production Database Migration Runner
Executes Alembic migrations headlessly for Google Cloud Run Jobs, Cloud Build, or CI/CD pipelines.
"""
import os
import sys
from pathlib import Path
from alembic import command
from alembic.config import Config


def run_migrations() -> int:
    backend_dir = Path(__file__).resolve().parent.parent
    alembic_ini_path = backend_dir / "alembic.ini"

    if not alembic_ini_path.exists():
        print(f"Error: alembic.ini not found at {alembic_ini_path}", file=sys.stderr)
        return 1

    print(f"Running database migrations using config: {alembic_ini_path}")
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))

    try:
        command.upgrade(alembic_cfg, "head")
        print("Database migrations applied successfully.")
        return 0
    except Exception as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_migrations())
