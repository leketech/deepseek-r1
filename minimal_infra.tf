// Minimal infrastructure for DeepSeek R1 project
// This can be deployed while waiting for SSD quota increase

resource "google_compute_network" "vpc" {
  name                    = var.vpc_name
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.vpc_name}-subnet"
  ip_cidr_range = "10.10.0.0/16"
  network       = google_compute_network.vpc.id
  region        = var.region
  project       = var.project_id
}

resource "google_artifact_registry_repository" "repo" {
  provider      = google
  location      = var.region
  repository_id = var.artifact_repo
  description   = "Docker images for DeepSeek R1"
  format        = "DOCKER"
  project       = var.project_id
}

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