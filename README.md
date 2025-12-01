# DeepSeek R1 - AI Model Deployment Platform

## Overview

This project provides a complete infrastructure for deploying and serving AI models on Google Cloud Platform, with a focus on the DeepSeek model. It includes automated CI/CD pipelines, monitoring, logging, and performance optimization features.

## Features

• Automated infrastructure provisioning with Terraform
• Kubernetes-based model deployment on GKE
• CI/CD pipeline with GitHub Actions
• Comprehensive monitoring and alerting
• Centralized logging with export to BigQuery, Cloud Storage, and Pub/Sub
• Performance optimization through batching and concurrency tuning
• Secure service account management
• GPU support for accelerated inference
• Vertex AI integration for managed model serving

## Prerequisites

• Google Cloud Platform account with billing enabled
• Google Cloud SDK installed and configured
• kubectl CLI
• Terraform
• Docker
• Python 3.8+

## Setup Instructions

### 1. Google Cloud Setup

1. Create a Google Cloud Project
2. Enable required APIs:
```bash
gcloud services enable \
  compute.googleapis.com \
  container.googleapis.com \
  artifactregistry.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  bigquery.googleapis.com \
  pubsub.googleapis.com \
  storage.googleapis.com \
  aiplatform.googleapis.com
```

### 2. Service Account Setup

1. Create a service account for Terraform:
```bash
gcloud iam service-accounts create terraform-sa \
  --display-name="Terraform Service Account"
```

2. Grant necessary roles:
```bash
export PROJECT_ID="your-project-id"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:terraform-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/owner"
```

3. Create and download the service account key:
```bash
gcloud iam service-accounts keys create infra/terraform-key.json \
  --iam-account="terraform-sa@$PROJECT_ID.iam.gserviceaccount.com"
```

### 3. Infrastructure Deployment

You can deploy the infrastructure using either the manual approach or the automated production deployment script.

#### Manual Deployment

1. Initialize Terraform:
```bash
cd infra
terraform init
```

2. Apply the infrastructure:
```bash
terraform apply
```

#### Automated Production Deployment

Run the production deployment script:

**On Windows:**
```powershell
.\deploy-production.ps1
```

**On Linux/Mac (using the Python script):**
```bash
python3 deploy_production.py
```

### 4. Monitoring and Logging Setup

Run the monitoring setup script:

```powershell
$env:PROJECT_ID="your-project-id"
$env:REGION="us-central1"
./setup-monitoring.ps1
```

### 5. CI/CD Pipeline

The GitHub Actions workflow will automatically:

• Build and push Docker images (both CPU and GPU versions)
• Deploy to GKE
• Set up monitoring dashboards
• Configure alerting policies

### 6. GPU Support

The infrastructure includes:

• Dedicated GPU node pools in GKE
• GPU-optimized Docker images
• Kubernetes deployments configured for GPU resources
• Appropriate resource requests and limits

### 7. Vertex AI Integration

The project includes scripts for deploying models to Vertex AI:

• Pre-trained models from Model Garden
• Custom model deployment
• Endpoint management

## Performance Optimization

The project includes several performance optimization features:

• Dynamic batching with configurable batch sizes and timeouts
• Concurrency tuning with multiple batch workers
• Container-level optimizations for better resource utilization
• Kubernetes HPA configuration for automatic scaling
• GPU acceleration for compute-intensive workloads

## Monitoring and Alerting

• Cloud Monitoring dashboards for infrastructure and model performance
• Custom alert policies for errors, latency, and resource utilization
• Centralized logging with export to multiple destinations
• Custom metrics derived from application logs

## Security Considerations

• Service account keys are excluded from version control
• Role-based access control for different components
• Secure workload identity for GKE pods
• Private networking for internal services

## Troubleshooting

Common issues and solutions:

1. If you encounter permission errors, verify your service account has the necessary roles
2. If monitoring resources fail to create, ensure the required APIs are enabled
3. If deployments fail, check the logs in Cloud Logging
4. For GPU-related issues, ensure the GPU node pool is properly configured

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

<!-- Workflow trigger update -->