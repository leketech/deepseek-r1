resource "google_artifact_registry_repository" "repo" {
  provider = google
  location     = var.region
  repository_id = var.artifact_repo
  description   = "Docker images for DeepSeek R1"
  format        = "DOCKER"
}

# Service account for CI to push images & deploy
resource "google_service_account" "ci" {
  account_id   = "deepseek-ci"
  display_name = "DeepSeek CI service account"
  project      = var.project_id
}

resource "google_project_iam_member" "ci_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.ci.email}"
}

# Additional roles for CI service account for GKE deployment
resource "google_project_iam_member" "ci_gke_admin" {
  project = var.project_id
  role    = "roles/container.developer"
  member  = "serviceAccount:${google_service_account.ci.email}"
}