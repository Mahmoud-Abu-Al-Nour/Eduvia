# Phase 12 — Production Cloud Deployment & Staging

**Status:** `PHASE 12 — LOCKED`  
**Completed:** 2026-09-19  
**Git Commit:** `b19168a`  
**Test Baseline:** 217/217 backend tests passing (209 regression + 8 Phase 12 cloud deployment tests)  
**Deployment Tests:** 8/8 passing (`backend/tests/test_cloud_deployment.py`)  
**Frontend Tests:** 13/13 passing  
**Frontend Build:** Passing (0 errors, 0 type-check warnings)  
**Infrastructure Target:** Google Cloud Platform (Cloud Run, Cloud SQL, Secret Manager, Cloud Build)  

---

## 🎯 Objective

Phase 12 transforms the containerized, application-ready Eduvia system into a production-oriented cloud deployment architecture. It defines Infrastructure as Code (IaC) via Terraform, configures multi-stage production Docker containers for Cloud Run serverless hosting, establishes managed PostgreSQL integration with Cloud SQL, isolates sensitive credentials in Google Secret Manager, automates database migrations via Alembic runners, and sets up continuous deployment with Google Cloud Build.

> **Important Distinction:** Phase 12 implements and validates the production cloud infrastructure configuration as code. This documentation distinguishes infrastructure defined and tested in code from resources that were actually provisioned and running in a live GCP environment.

---

## 🛠️ What Phase 12 Actually Implemented

### 1. Cloud-Ready Application Configuration (`backend/app/core/config.py`)
- **Dynamic Port Binding**: Added `PORT: int = 8000` supporting Cloud Run's dynamic `$PORT` environment variable injection (e.g., binding to `8080`).
- **Environment Detection**: Added property flags `is_production`, `is_staging`, and `is_development` based on `APP_ENV` (`development`, `staging`, `production`).
- **Cloud SQL Unix Socket Resolution**: Added `CLOUD_SQL_CONNECTION_NAME: str = ""` configuration.
- **Effective Database URL**: Implemented `effective_database_url` property that transparently appends `host=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}` when deployed against Cloud SQL without mutating the base credentials.

### 2. Cloud SQL Integration (`backend/app/database/session.py`)
- Relational database engine remains PostgreSQL with asynchronous `asyncpg` driver.
- Engine creation uses `settings.effective_database_url`, providing full compatibility between local Docker development and production Cloud SQL Unix sockets.
- Connection pooling configured with `pool_pre_ping=True`, `pool_size=5`, and `max_overflow=10` to gracefully handle serverless container scaling.

### 3. Backend Containerization (`backend/Dockerfile`)
- Multi-stage build (`base`, `dependencies`, `development`, `production`).
- Hardened unprivileged execution under user `eduvia` (UID `1001`).
- Dynamic port exposure (`EXPOSE 8000 8080`) and startup command:
  ```bash
  CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
  ```
- Built-in container health check querying `/api/v1/health`.

### 4. Frontend Containerization & Nginx (`frontend/Dockerfile`, `frontend/nginx.conf`)
- Multi-stage build compiling React 19/TypeScript assets using Vite and serving via Alpine Nginx.
- Dual port listening (`listen 80; listen 8080;`) for local and Cloud Run compatibility.
- SPA routing support (`try_files $uri $uri/ /index.html;`).
- API reverse-proxy pass (`/api/` $\rightarrow$ `http://backend:8000`).
- Security headers and static asset caching with 1-year immutable headers.

### 5. Database Migration Automation (`backend/scripts/run_migrations.py`)
- Headless, programmatic migration runner executing `alembic upgrade head`.
- Validates the presence of `alembic.ini` and exits cleanly with code 0 on success or code 1 on failure.
- Designed for pre-deployment execution via Cloud Run Jobs or Cloud Build before traffic routing.

---

## 🏗️ Infrastructure as Code (Terraform)

All infrastructure is codified declaratively in `terraform/`:

* **`terraform/main.tf`**:
  * Configures GCP Google provider (`google` and `google-beta`).
  * Enables required Google APIs: `run.googleapis.com`, `sqladmin.googleapis.com`, `secretmanager.googleapis.com`, `artifactregistry.googleapis.com`, `compute.googleapis.com`.
  * Provisions Google Artifact Registry repository `eduvia-containers` for Docker images.
* **`terraform/cloud_sql.tf`**:
  * Provisions `google_sql_database_instance` with `POSTGRES_16` database engine.
  * Configures environment-aware tier (`var.db_tier`, e.g., `db-custom-2-7680` or `db-f1-micro`).
  * Automates daily backups (`03:00` UTC) and Query Insights.
  * Provisions database `var.db_name` and user `var.db_user` with randomized password.
* **`terraform/secret_manager.tf`**:
  * Provisions `google_secret_manager_secret` for `DATABASE_URL`, `JWT_SECRET`, `APP_SECRET_KEY`, and `GEMINI_API_KEY`.
  * Automatically formats and stores `DATABASE_URL` referencing the Cloud SQL instance connection name and generated password.
  * Provisions dedicated Cloud Run Service Account (`eduvia-run-${var.environment}`) and grants `roles/secretmanager.secretAccessor` and `roles/cloudsql.client`.
* **`terraform/cloud_run.tf`**:
  * Configures `google_cloud_run_v2_service` for `eduvia-backend-${var.environment}` and `eduvia-frontend-${var.environment}`.
  * Mounts Cloud SQL instance volume via Unix socket.
  * Injects environment variables directly from Secret Manager secret references.
  * Configures autoscaling (min 0/1, max 10 instances).
  * Provisions public invocation permissions (`roles/run.invoker` for `allUsers`).
* **`terraform/variables.tf`**:
  * Defines configurable inputs: `project_id`, `region` (`us-central1`), `environment` (`production`), `db_name`, `db_user`, `db_tier`.
* **`terraform/outputs.tf`**:
  * Exports service URLs (`backend_url`, `frontend_url`) and Cloud SQL connection name.

---

## 🔒 Secret Management Architecture

```text
Application (Runtime)
       ▲
       │ Environment Variable Mount
       ▼
Google Cloud Run
       ▲
       │ IAM Bound Access (`roles/secretmanager.secretAccessor`)
       ▼
Google Secret Manager
  • eduvia_database_url_production
  • eduvia_jwt_secret_production
  • eduvia_app_secret_production
  • eduvia_gemini_api_key_production
```

No secrets, passwords, or API keys are stored in Git. Local development relies strictly on `.env`, while production relies exclusively on Secret Manager.

---

## 🚀 Continuous Deployment (Cloud Build)

Defined in `cloudbuild.yaml`:

```text
Source Commit
      │
      ▼
1. Build Backend Docker Image (`--target=production`)
      │
      ▼
2. Build Frontend Docker Image (`--target=production`)
      │
      ▼
3. Push Images to Artifact Registry
      │
      ▼
4. Execute Database Migrations (Cloud Run Job: `eduvia-migration-job`)
      │
      ▼
5. Deploy Backend Service to Cloud Run
      │
      ▼
6. Deploy Frontend Service to Cloud Run
```

---

## 🧪 Verification & Testing

Phase 12 introduced a dedicated automated test suite in **`backend/tests/test_cloud_deployment.py`** containing 8 targeted deployment validation tests:

1. `test_settings_cloud_run_port_defaults_and_override`: Validates default port 8000 and Cloud Run override to 8080.
2. `test_settings_cloud_sql_connection_formatting`: Validates Unix socket formatting for `effective_database_url`.
3. `test_settings_environment_flags`: Verifies staging vs. production vs. development environment properties.
4. `test_backend_dockerfile_cloud_run_compliance`: Validates `$PORT` handling and production target in `backend/Dockerfile`.
5. `test_frontend_dockerfile_and_nginx_cloud_run_compliance`: Validates Nginx configuration and port 8080 listening in `frontend/Dockerfile`.
6. `test_migration_runner_structure`: Validates presence and execution integrity of `run_migrations.py` and `alembic.ini`.
7. `test_terraform_manifests_integrity`: Verifies syntax and resource definitions across all 6 Terraform files.
8. `test_cloudbuild_pipeline_integrity`: Verifies YAML syntax and mandatory pipeline steps in `cloudbuild.yaml`.

### Regression Verification
* **Backend Suite**: **217/217 passing tests** (209 regression + 8 cloud deployment tests).
* **Frontend Suite**: **13/13 passing tests**.
* **TypeScript & Build**: `tsc -b` and `vite build` completed with 0 errors.

---

## 🏁 Phase 12 Final Gate

```text
Commit:
b19168a

Message:
feat(phase-12): complete production cloud deployment infrastructure

Push:
PASS

Working tree:
CLEAN
```

```text
PHASE 12 — LOCKED
```

---

## 🔗 Related Notes
- [[00 - MOC/Current Status|Current Status]]
- [[00 - MOC/Eduvia Home|Eduvia Home]]
- [[05 - Development History/Eduvia Development History|Eduvia Development History]]
- [[05 - Development History/Reports/Phase 12 Report|Phase 12 Report]]
- [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
- [[Eduvia Testing & Verification|Eduvia Testing & Verification]]
- [[05 - Development History/Phase 11 — System Hardening & Accessibility Audit|Phase 11 — System Hardening & Accessibility Audit]]
