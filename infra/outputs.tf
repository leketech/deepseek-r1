output "project_id" {
  value = var.project_id
  description = "GCP Project ID"
}

output "region" {
  value = var.region
  description = "GCP Region"
}

output "zone" {
  value = var.zone
  description = "GCP Zone"
}

output "cluster_name" {
  value = var.cluster_name
  description = "GKE Cluster Name"
}

output "artifact_repo" {
  value = var.artifact_repo
  description = "Artifact Registry Repository Name"
}