"""
Eduvia — Phase 12: Production Cloud Deployment Tests
Validates Cloud Run configurations, dynamic port binding, Cloud SQL socket URL resolution,
Secret Manager configuration, and deployment automation manifests.
"""
from pathlib import Path
import yaml
from app.core.config import Settings


def test_settings_cloud_run_port_defaults_and_override():
    """Verify default port is 8000 and can be set to Cloud Run's 8080."""
    default_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
    )
    assert default_settings.PORT == 8000

    cloud_run_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
        PORT=8080,
    )
    assert cloud_run_settings.PORT == 8080


def test_settings_cloud_sql_connection_formatting():
    """Verify that CLOUD_SQL_CONNECTION_NAME updates effective_database_url to use Unix socket."""
    standard_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://eduvia_app:pass@/eduvia_db",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
    )
    assert "host=/cloudsql/" not in standard_settings.effective_database_url

    cloud_sql_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://eduvia_app:pass@/eduvia_db",
        CLOUD_SQL_CONNECTION_NAME="eduvia-prod:us-central1:eduvia-sql-production",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
    )
    effective = cloud_sql_settings.effective_database_url
    assert "host=/cloudsql/eduvia-prod:us-central1:eduvia-sql-production" in effective


def test_settings_environment_flags():
    """Verify environment detection properties (staging vs production vs development)."""
    staging_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
        APP_ENV="staging",
    )
    assert staging_settings.is_staging is True
    assert staging_settings.is_production is False
    assert staging_settings.is_development is False

    prod_settings = Settings(
        DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db",
        GEMINI_API_KEY="test_key",
        JWT_SECRET="test_jwt",
        APP_SECRET_KEY="test_secret",
        APP_ENV="production",
    )
    assert prod_settings.is_production is True
    assert prod_settings.is_staging is False
    assert prod_settings.is_development is False


def test_backend_dockerfile_cloud_run_compliance():
    """Verify backend Dockerfile accommodates Cloud Run dynamic $PORT and multi-stage build."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    dockerfile = (repo_root / "backend" / "Dockerfile").read_text(encoding="utf-8")

    assert "ENV PORT=8000" in dockerfile or "PORT" in dockerfile
    assert "EXPOSE" in dockerfile
    assert "${PORT:-8000}" in dockerfile
    assert "production" in dockerfile


def test_frontend_dockerfile_and_nginx_cloud_run_compliance():
    """Verify frontend Dockerfile and nginx configuration support Cloud Run port 8080."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    nginx_conf = (repo_root / "frontend" / "nginx.conf").read_text(encoding="utf-8")
    dockerfile = (repo_root / "frontend" / "Dockerfile").read_text(encoding="utf-8")

    assert "listen 8080;" in nginx_conf
    assert "8080" in dockerfile


def test_migration_runner_structure():
    """Verify run_migrations.py can find and target alembic.ini."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    migration_script = repo_root / "backend" / "scripts" / "run_migrations.py"
    alembic_ini = repo_root / "backend" / "alembic.ini"

    assert migration_script.exists()
    assert alembic_ini.exists()


def test_terraform_manifests_integrity():
    """Verify that Terraform infrastructure definitions exist and specify required services."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    tf_dir = repo_root / "terraform"

    assert (tf_dir / "main.tf").exists()
    assert (tf_dir / "cloud_run.tf").exists()
    assert (tf_dir / "cloud_sql.tf").exists()
    assert (tf_dir / "secret_manager.tf").exists()
    assert (tf_dir / "variables.tf").exists()
    assert (tf_dir / "outputs.tf").exists()

    cloud_run_tf = (tf_dir / "cloud_run.tf").read_text(encoding="utf-8")
    assert "google_cloud_run_v2_service" in cloud_run_tf
    assert "eduvia-backend" in cloud_run_tf
    assert "eduvia-frontend" in cloud_run_tf

    cloud_sql_tf = (tf_dir / "cloud_sql.tf").read_text(encoding="utf-8")
    assert "POSTGRES_16" in cloud_sql_tf

    secrets_tf = (tf_dir / "secret_manager.tf").read_text(encoding="utf-8")
    assert "google_secret_manager_secret" in secrets_tf


def test_cloudbuild_pipeline_integrity():
    """Verify cloudbuild.yaml syntax and deployment steps."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    cloudbuild_file = repo_root / "cloudbuild.yaml"

    assert cloudbuild_file.exists()
    content = yaml.safe_load(cloudbuild_file.read_text(encoding="utf-8"))
    assert "steps" in content
    assert len(content["steps"]) >= 4

    step_ids = [step.get("id") for step in content["steps"]]
    assert "build-backend" in step_ids
    assert "build-frontend" in step_ids
    assert "deploy-backend" in step_ids
    assert "deploy-frontend" in step_ids
