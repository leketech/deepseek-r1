# DeepSeek R1 - AI Model Deployment Platform

## Overview
This project provides a complete infrastructure for deploying and serving AI models on Google Cloud Platform, with a focus on the DeepSeek model. It includes automated CI/CD pipelines, monitoring, logging, and performance optimization features.

## Features
- Automated infrastructure provisioning with Terraform
- Kubernetes-based model deployment on GKE
- CI/CD pipeline with GitHub Actions
- Comprehensive monitoring and alerting
- Centralized logging with export to BigQuery, Cloud Storage, and Pub/Sub
- Performance optimization through batching and concurrency tuning
- Secure service account management

## Prerequisites
- Google Cloud Platform account with billing enabled
- Google Cloud SDK installed and configured
- kubectl CLI
- Terraform
- Docker
- Python 3.8+

## Setup Instructions

### 1. Google Cloud Setup
1. Create a Google Cloud Project
2. Enable required APIs:
   ```
   gcloud services enable \
     compute.googleapis.com \
     container.googleapis.com \
     artifactregistry.googleapis.com \
     monitoring.googleapis.com \
     logging.googleapis.com \
     bigquery.googleapis.com \
     pubsub.googleapis.com \
     storage.googleapis.com
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
1. Initialize Terraform:
   ```bash
   cd infra
   terraform init
   ```

2. Apply the infrastructure:
   ```bash
   terraform apply
   ```

### 4. Monitoring and Logging Setup
Run the monitoring setup script:
```bash
$env:PROJECT_ID="your-project-id"
$env:REGION="us-central1"
./setup-monitoring.ps1
```

### 5. CI/CD Pipeline
The GitHub Actions workflow will automatically:
- Build and push Docker images
- Deploy to GKE
- Set up monitoring dashboards
- Configure alerting policies

## Performance Optimization
The project includes several performance optimization features:
- Dynamic batching with configurable batch sizes and timeouts
- Concurrency tuning with multiple batch workers
- Container-level optimizations for better resource utilization
- Kubernetes HPA configuration for automatic scaling

## Monitoring and Alerting
- Cloud Monitoring dashboards for infrastructure and model performance
- Custom alert policies for errors, latency, and resource utilization
- Centralized logging with export to multiple destinations
- Custom metrics derived from application logs

## Security Considerations
- Service account keys are excluded from version control
- Role-based access control for different components
- Secure workload identity for GKE pods

## Troubleshooting
Common issues and solutions:
1. If you encounter permission errors, verify your service account has the necessary roles
2. If monitoring resources fail to create, ensure the required APIs are enabled
3. If deployments fail, check the logs in Cloud Logging

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request