variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region for deployment"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment name (staging or production)"
  type        = string
  default     = "production"
}

variable "db_tier" {
  description = "Cloud SQL machine tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_name" {
  description = "Cloud SQL PostgreSQL database name"
  type        = string
  default     = "eduvia_db"
}

variable "db_user" {
  description = "Cloud SQL PostgreSQL database user"
  type        = string
  default     = "eduvia_app"
}
