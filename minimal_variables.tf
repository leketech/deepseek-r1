variable "project_id" { 
  type = string 
}

variable "region" { 
  type = string 
  default = "us-west1" 
}

variable "zone" { 
  type = string 
  default = "us-west1-a" 
}

variable "cluster_name" { 
  type = string 
  default = "deepseek-gke" 
}

variable "vpc_name" { 
  type = string 
  default = "deepseek-vpc" 
}

variable "artifact_repo" { 
  type = string 
  default = "deepseek-repo" 
}