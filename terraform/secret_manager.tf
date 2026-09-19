# ── Service Account for Cloud Run ──────────────────────────────────────────
resource "google_service_account" "cloud_run_sa" {
  account_id   = "eduvia-run-${var.environment}"
  display_name = "Eduvia Cloud Run Service Account (${var.environment})"
}

# Grant Cloud SQL Client permission to Cloud Run
resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# ── Random Generated Secrets ────────────────────────────────────────────────
resource "random_password" "jwt_secret" {
  length  = 48
  special = false
}

resource "random_password" "app_secret_key" {
  length  = 48
  special = false
}

# ── Secret Manager Secrets ──────────────────────────────────────────────────
resource "google_secret_manager_secret" "database_url" {
  depends_on = [google_project_service.enabled_services]
  secret_id  = "eduvia_database_url_${var.environment}"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "database_url_val" {
  secret      = google_secret_manager_secret.database_url.id
  secret_data = "postgresql+asyncpg://${google_sql_user.eduvia_user.name}:${random_password.db_password.result}@/${google_sql_database.eduvia_database.name}?host=/cloudsql/${google_sql_database_instance.postgres_instance.connection_name}"
}

resource "google_secret_manager_secret" "jwt_secret" {
  depends_on = [google_project_service.enabled_services]
  secret_id  = "eduvia_jwt_secret_${var.environment}"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "jwt_secret_val" {
  secret      = google_secret_manager_secret.jwt_secret.id
  secret_data = random_password.jwt_secret.result
}

resource "google_secret_manager_secret" "app_secret" {
  depends_on = [google_project_service.enabled_services]
  secret_id  = "eduvia_app_secret_${var.environment}"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "app_secret_val" {
  secret      = google_secret_manager_secret.app_secret.id
  secret_data = random_password.app_secret_key.result
}

resource "google_secret_manager_secret" "gemini_api_key" {
  depends_on = [google_project_service.enabled_services]
  secret_id  = "eduvia_gemini_api_key_${var.environment}"

  replication {
    auto {}
  }
}

# Grant Secret Manager Access to Cloud Run Service Account
resource "google_secret_manager_secret_iam_member" "db_url_access" {
  secret_id = google_secret_manager_secret.database_url.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "jwt_secret_access" {
  secret_id = google_secret_manager_secret.jwt_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "app_secret_access" {
  secret_id = google_secret_manager_secret.app_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "gemini_access" {
  secret_id = google_secret_manager_secret.gemini_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
