# ── Backend Cloud Run Service ───────────────────────────────────────────────
resource "google_cloud_run_v2_service" "backend_service" {
  depends_on = [
    google_project_service.enabled_services,
    google_sql_database_instance.postgres_instance
  ]
  name     = "eduvia-backend-${var.environment}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloud_run_sa.email

    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = 10
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.postgres_instance.connection_name]
      }
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/eduvia-containers/eduvia-backend:latest"

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }

      env {
        name  = "APP_ENV"
        value = var.environment
      }

      env {
        name  = "CLOUD_SQL_CONNECTION_NAME"
        value = google_sql_database_instance.postgres_instance.connection_name
      }

      # Secrets mounted from Secret Manager
      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.database_url.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "JWT_SECRET"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.jwt_secret.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "APP_SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.app_secret.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_api_key.secret_id
            version = "latest"
          }
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }

      startup_probe {
        http_get {
          path = "/api/v1/health"
          port = 8000
        }
        initial_delay_seconds = 10
        period_seconds        = 10
        failure_threshold     = 5
      }

      liveness_probe {
        http_get {
          path = "/api/v1/health"
          port = 8000
        }
        period_seconds = 30
      }
    }
  }
}

# Allow public invocations of the backend API
resource "google_cloud_run_v2_service_iam_member" "backend_public_invoker" {
  location = google_cloud_run_v2_service.backend_service.location
  name     = google_cloud_run_v2_service.backend_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ── Frontend Cloud Run Service ──────────────────────────────────────────────
resource "google_cloud_run_v2_service" "frontend_service" {
  depends_on = [google_project_service.enabled_services]
  name       = "eduvia-frontend-${var.environment}"
  location   = var.region
  ingress    = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 5
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/eduvia-containers/eduvia-frontend:latest"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      startup_probe {
        http_get {
          path = "/"
          port = 8080
        }
        initial_delay_seconds = 5
        period_seconds        = 10
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public_invoker" {
  location = google_cloud_run_v2_service.frontend_service.location
  name     = google_cloud_run_v2_service.frontend_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
