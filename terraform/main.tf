terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── Enable Required GCP APIs ────────────────────────────────────────────────
resource "google_project_service" "enabled_services" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
  ])

  service            = each.key
  disable_on_destroy = false
}

# ── Artifact Registry for Container Images ──────────────────────────────────
resource "google_artifact_registry_repository" "eduvia_repo" {
  depends_on    = [google_project_service.enabled_services]
  location      = var.region
  repository_id = "eduvia-containers"
  description   = "Eduvia container images repository"
  format        = "DOCKER"
}
