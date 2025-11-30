#!/bin/bash

# Script to set up Workload Identity for the DeepSeek R1 project

# Variables - Update these with your actual values
PROJECT_ID="your-project-id"
GSA_NAME="deepseek-ci"  # Google Service Account
KSA_NAME="deepseek-ci-ksa"  # Kubernetes Service Account
NAMESPACE="default"

# Create the Workload Identity binding
gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KSA_NAME}]" \
  ${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

echo "Workload Identity binding created successfully!"
echo "Remember to update the service account annotation in k8s/service-account.yaml with your actual project ID"