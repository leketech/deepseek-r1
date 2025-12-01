resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone  # Use zone instead of region for single-zone cluster
  network  = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id
  initial_node_count = 1  # Use default node pool instead of removing it

  # Configure default node pool for minimal resources
  node_config {
    machine_type = "e2-medium"
    disk_type    = "pd-standard"
    disk_size_gb = 20  # Increased to meet minimum requirement
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
    service_account = google_service_account.ci.email
  }

  # Enable Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Enable Autopilot mode for better resource management
  enable_autopilot = false

  # Enable necessary addons
  addons_config {
    horizontal_pod_autoscaling {
      disabled = false
    }
    http_load_balancing {
      disabled = false
    }
    # Removed network_policy_config as it conflicts with enable_autopilot
  }

  # Enable logging and monitoring
  logging_service    = "logging.googleapis.com/kubernetes"
  monitoring_service = "monitoring.googleapis.com/kubernetes"

  # Disable deletion protection for testing
  deletion_protection = false

  ip_allocation_policy {}
}

// GPU node pool for accelerated workloads (conditionally created)
resource "google_container_node_pool" "gpu_pool" {
  count      = var.enable_gpu ? 1 : 0
  name       = "gpu-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    machine_type = "n1-standard-2"
    disk_size_gb = 30
    disk_type    = "pd-standard"
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]

    service_account = google_service_account.ci.email
    
    # Enable GPU accelerators
    guest_accelerator {
      type  = "nvidia-tesla-t4"
      count = 1
    }
    
    # Taints to ensure only GPU workloads run on these nodes
    taint {
      key    = "nvidia.com/gpu"
      value  = "present"
      effect = "NO_SCHEDULE"
    }
  }
  
  # Auto-scaling configuration
  autoscaling {
    min_node_count = 0
    max_node_count = 3
  }
  
  # Management configuration
  management {
    auto_repair  = true
    auto_upgrade = true
  }
}