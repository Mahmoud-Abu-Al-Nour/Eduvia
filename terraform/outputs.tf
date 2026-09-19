output "backend_url" {
  description = "Public URL of the backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend_service.uri
}

output "frontend_url" {
  description = "Public URL of the frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend_service.uri
}

output "cloud_sql_connection_name" {
  description = "Connection name for the Cloud SQL PostgreSQL instance"
  value       = google_sql_database_instance.postgres_instance.connection_name
}

output "artifact_registry_repo" {
  description = "Artifact Registry Docker repository"
  value       = google_artifact_registry_repository.eduvia_repo.name
}
