resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone  # Use zone instead of region for single-zone cluster
  network  = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id
  initial_node_count = 1  # Use default node pool instead of removing it

  # Configure default node pool for minimal resources
  node_config {
    machine_type = "e2-micro"
    disk_type    = "pd-standard"
    disk_size_gb = 12  # Increased to meet minimum requirement
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
    service_account = google_service_account.ci.email
  }

  # Enable Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Minimal configuration for free tier
  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }

  # Disable features that might require additional resources
  addons_config {
    horizontal_pod_autoscaling {
      disabled = true
    }
    http_load_balancing {
      disabled = true
    }
    network_policy_config {
      disabled = true
    }
  }

  # Disable deletion protection for testing
  deletion_protection = false

  ip_allocation_policy {}
}

// No separate node pools to reduce complexity