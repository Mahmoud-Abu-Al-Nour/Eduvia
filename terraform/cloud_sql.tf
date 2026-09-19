# ── Cloud SQL PostgreSQL 16 Instance ─────────────────────────────────────────
resource "random_password" "db_password" {
  length  = 24
  special = false
}

resource "google_sql_database_instance" "postgres_instance" {
  depends_on          = [google_project_service.enabled_services]
  name                = "eduvia-sql-${var.environment}"
  database_version    = "POSTGRES_16"
  region              = var.region
  deletion_protection = var.environment == "production"

  settings {
    tier              = var.db_tier
    availability_type = var.environment == "production" ? "REGIONAL" : "ZONAL"
    disk_size         = 20
    disk_type         = "PD_SSD"

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    insights_config {
      query_insights_enabled = true
    }

    ip_configuration {
      ipv4_enabled = true
    }
  }
}

resource "google_sql_database" "eduvia_database" {
  name     = var.db_name
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_sql_user" "eduvia_user" {
  name     = var.db_user
  instance = google_sql_database_instance.postgres_instance.name
  password = random_password.db_password.result
}
