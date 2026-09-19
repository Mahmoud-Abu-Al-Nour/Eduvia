# Eduvia Production & Cloud Deployment

> **Cloud-Native Containerization, Infrastructure as Code, and Zero-Downtime Deployment Topology**

---

## 🎯 Phase 12 Overview & Objectives

Phase 12 established the production cloud architecture for Eduvia, targeting **Google Cloud Platform (GCP)**. The design prioritizes serverless container execution, managed relational persistence, zero-secret repository hygiene, and automated continuous deployment.

> **Important Distinction:** Phase 12 implements and validates the production cloud deployment infrastructure and automation required for GCP deployment. This documentation distinguishes infrastructure defined and tested in code from resources that were actually provisioned and running in a live GCP environment.

For full chronological milestone details, see [[05 - Development History/Phase 12 — Production Cloud Deployment & Staging|Phase 12 — Production Cloud Deployment & Staging]] and the [[05 - Development History/Reports/Phase 12 Report|Phase 12 Report]].

---

## 🏗️ Cloud Infrastructure Topology

```text
                    Eduvia Source Code
                            │
                            ▼
                   Google Cloud Build
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       Artifact Registry           Migration Job
    (`eduvia-containers`)   (executes `run_migrations.py`)
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    Google Cloud Run
                 ┌──────────┴──────────┐
                 ▼                     ▼
          Backend Service       Frontend Service
        (`eduvia-backend`)    (`eduvia-frontend`)
                 │                     │
                 ├─────────────────────┤
                 │                     │
                 ▼                     ▼
       Cloud SQL (Postgres 16)   Secret Manager
     • Managed HA Instance      • Database URL
     • Unix Socket Mount        • JWT & App Secrets
     • Automated Daily Backups  • Gemini API Key
```

---

## 1. Declarative Infrastructure as Code (Terraform)

All cloud resources are codified in declarative **Terraform** configuration files under `terraform/`:

* **`terraform/main.tf`**:
  * Configures the GCP Google provider (`google` and `google-beta`).
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
  * Configures `google_cloud_run_v2_service` for `eduvia-backend-${var.environment}`, `eduvia-frontend-${var.environment}`, and `eduvia-mcp-${var.environment}`.
  * Mounts Cloud SQL instance volume via Unix socket.
  * Injects environment variables directly from Secret Manager secret references.
  * Configures autoscaling (min 0/1, max 10 instances).
  * Provisions public invocation permissions (`roles/run.invoker` for `allUsers`).
* **`terraform/variables.tf`**:
  * Defines configurable inputs: `project_id`, `region` (`us-central1`), `environment` (`production`), `db_name`, `db_user`, `db_tier`.
* **`terraform/outputs.tf`**:
  * Exports service URLs (`backend_url`, `frontend_url`, `mcp_url`) and Cloud SQL connection name.

---

## 2. Production Docker Engineering

Eduvia avoids heavy development containers in favor of hardened, minimal production container images:

### Backend Production Dockerfile (`backend/Dockerfile`)
```dockerfile
# Stage 1: Base & System Dependencies
FROM python:3.12-slim AS base
RUN groupadd --gid 1001 eduvia && useradd --uid 1001 --gid eduvia --shell /bin/bash --create-home eduvia
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Stage 2: Dependencies
FROM base AS dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e "."

# Stage 4: Production Runtime
FROM dependencies AS production
COPY --chown=eduvia:eduvia . .
USER eduvia
ENV PORT=8000
EXPOSE 8000 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f "http://localhost:${PORT:-8000}/api/v1/health" || exit 1
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
```

### Frontend Production Dockerfile & Nginx (`frontend/Dockerfile`, `frontend/nginx.conf`)
* Multi-stage build compiling React 19/TypeScript assets using Vite and serving via Alpine Nginx.
* Listens on ports 80 and 8080 for Cloud Run compatibility.
* Configured with SPA routing fallback (`try_files $uri $uri/ /index.html;`), API reverse proxying (`/api/` $\rightarrow$ `http://backend:8000`), and static asset caching.

---

## 3. Database Migration Automation (`run_migrations.py`)

To ensure database schema consistency without manual intervention during deployments:
* Eduvia provides a headless, programmatic migration runner: `backend/scripts/run_migrations.py`.
* The script programmatically targets `alembic.ini` and executes `command.upgrade(alembic_cfg, "head")`.
* Returns exit code `0` on successful migration, or code `1` with explicit stderr output on failure.
* Designed for pre-deployment execution via Cloud Run Jobs or Cloud Build before routing web traffic to new application revisions.

---

## 4. Continuous Integration & Deployment (Cloud Build)

Continuous deployment is codified in `cloudbuild.yaml`:
1. **Build Backend Image**: Compiles `backend/Dockerfile` targeting `--target=production`.
2. **Build Frontend Image**: Compiles `frontend/Dockerfile` targeting `--target=production`.
3. **Push to Artifact Registry**: Pushes tagged images (`$COMMIT_SHA` and `latest`) to `$_REGION-docker.pkg.dev/$PROJECT_ID/eduvia-containers/`.
4. **Execute Database Migrations**: Runs `eduvia-migration-job` via Cloud Run Jobs to apply schema changes.
5. **Deploy Cloud Run Services**: Deploys `eduvia-backend` and `eduvia-frontend` revisions with zero downtime.

---

## 5. Implementation Status vs. Active Cloud Execution

To maintain strict documentation accuracy, the project distinguishes between codified/validated infrastructure and active cloud billing instances:

| Component | Status in Repository | Active Cloud Deployment |
| :--- | :--- | :--- |
| **Terraform Code** (`main.tf`, `cloud_run.tf`, etc.) | **Implemented & Syntactically Validated** | Verified via test suite (`test_cloud_deployment.py`). Staging/Production plan validated. |
| **Production Dockerfile & Migration Runner** | **Implemented & Verified** | Built and tested locally; non-root user `eduvia:1001` and dynamic `$PORT` verified. |
| **Cloud Build Pipeline** (`cloudbuild.yaml`) | **Implemented & Configured** | Codified with automated build, migration, and deploy steps. |
| **Live Cloud Run Instance (Backend)** | **Infrastructure-Ready** | Ready for execution via `terraform apply` / Cloud Build trigger. |
| **Live Cloud Run Instance (MCP Server)** | **Infrastructure-Ready & Tunnel Verified** | Tested locally via stdio and verified over HTTP tunnel (`Streamable HTTP`). |

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Phase 12 History Note: [[05 - Development History/Phase 12 — Production Cloud Deployment & Staging|Phase 12 — Production Cloud Deployment & Staging]]
* Phase 12 Detailed Report: [[05 - Development History/Reports/Phase 12 Report|Phase 12 Report]]
* Security Engineering: [[Eduvia Security & Privacy Engineering|Eduvia Security & Privacy Engineering]]
* Testing & Verification: [[Eduvia Testing & Verification|Eduvia Testing & Verification]]
* Project MCP Server: [[Eduvia Project MCP|Eduvia Project MCP]]
