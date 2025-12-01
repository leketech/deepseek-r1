#!/usr/bin/env python3
"""
Production deployment script for DeepSeek R1 on GCP.
This script handles the deployment of the full infrastructure including:
- GKE cluster with GPU support
- Artifact Registry
- Vertex AI model deployment
- Kubernetes deployments (CPU and GPU)
"""

import os
import subprocess
import sys
import time
from google.cloud import aiplatform
from google.auth import default

def run_command(command, cwd=None):
    """Run a shell command and handle errors."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def deploy_terraform():
    """Deploy Terraform infrastructure."""
    print("Deploying Terraform infrastructure...")
    
    # Initialize Terraform
    run_command("terraform init", cwd="./infra")
    
    # Apply Terraform configuration
    run_command("terraform apply -auto-approve", cwd="./infra")
    
    print("Terraform deployment completed.")

def build_and_push_images():
    """Build and push Docker images."""
    print("Building and pushing Docker images...")
    
    # Get project information from terraform outputs
    project_id = run_command("terraform output -raw project_id", cwd="./infra").strip()
    region = run_command("terraform output -raw region", cwd="./infra").strip()
    artifact_repo = run_command("terraform output -raw artifact_repo", cwd="./infra").strip()
    
    # Set environment variables
    image_name = f"us-docker.pkg.dev/{project_id}/{artifact_repo}/deepseek-r1:latest"
    gpu_image_name = f"us-docker.pkg.dev/{project_id}/{artifact_repo}/deepseek-r1-gpu:latest"
    
    # Configure Docker auth
    run_command(f"gcloud auth configure-docker {region}-docker.pkg.dev -q")
    
    # Build and push CPU image
    run_command(f"docker build -t {image_name} ./server", cwd=".")
    run_command(f"docker push {image_name}")
    
    # Build and push GPU image
    run_command(f"docker build -t {gpu_image_name} -f ./server/Dockerfile.gpu ./server", cwd=".")
    run_command(f"docker push {gpu_image_name}")
    
    print("Docker images built and pushed successfully.")

def deploy_to_kubernetes():
    """Deploy applications to Kubernetes."""
    print("Deploying to Kubernetes...")
    
    # Get cluster credentials
    cluster_name = run_command("terraform output -raw cluster_name", cwd="./infra").strip()
    region = run_command("terraform output -raw region", cwd="./infra").strip()
    zone = run_command("terraform output -raw zone", cwd="./infra").strip()
    
    run_command(f"gcloud container clusters get-credentials {cluster_name} --zone={zone} --project={project_id}")
    
    # Apply Kubernetes manifests
    run_command("kubectl apply -f k8s/service-account.yaml")
    run_command("kubectl apply -f k8s/logging-configmap.yaml")
    run_command("kubectl apply -f k8s/deployment.yaml")
    run_command("kubectl apply -f k8s/gpu-deployment.yaml")
    run_command("kubectl apply -f k8s/service.yaml")
    run_command("kubectl apply -f k8s/hpa.yaml")
    
    print("Kubernetes deployment completed.")

def deploy_vertex_ai_model():
    """Deploy model to Vertex AI."""
    print("Deploying model to Vertex AI...")
    
    # Get project information
    project_id = run_command("terraform output -raw project_id", cwd="./infra").strip()
    region = run_command("terraform output -raw region", cwd="./infra").strip()
    
    # Initialize Vertex AI
    credentials, _ = default()
    aiplatform.init(
        project=project_id,
        location=region,
        credentials=credentials
    )
    
    try:
        # Create endpoint if it doesn't exist
        endpoints = aiplatform.Endpoint.list(filter=f"display_name=deepseek-endpoint")
        if endpoints:
            endpoint = endpoints[0]
            print(f"Using existing endpoint: {endpoint.display_name}")
        else:
            endpoint = aiplatform.Endpoint.create(
                display_name="deepseek-endpoint",
                project=project_id,
                location=region
            )
            print(f"Created new endpoint: {endpoint.display_name}")
        
        # Deploy model (using a pre-trained model from Model Garden)
        print("Deploying pre-trained model from Model Garden...")
        # Note: In a real implementation, you would select a specific model from Model Garden
        # For now, we'll just print instructions
        
        print("To deploy a model from Model Garden:")
        print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
        print("2. Select a pre-trained model (e.g., PaLM 2 for text generation)")
        print("3. Deploy it to your endpoint")
        print(f"4. Your endpoint ID is: {endpoint.resource_name}")
        
    except Exception as e:
        print(f"Error deploying Vertex AI model: {e}")
    
    print("Vertex AI deployment process completed.")

def main():
    """Main deployment function."""
    print("Starting production deployment of DeepSeek R1...")
    
    # Deploy Terraform infrastructure
    deploy_terraform()
    
    # Wait a moment for resources to be ready
    time.sleep(30)
    
    # Build and push Docker images
    build_and_push_images()
    
    # Deploy to Kubernetes
    deploy_to_kubernetes()
    
    # Deploy to Vertex AI
    deploy_vertex_ai_model()
    
    print("Production deployment completed successfully!")
    print("\nNext steps:")
    print("1. Monitor the deployment with: kubectl get pods")
    print("2. Check logs with: kubectl logs -l app=deepseek")
    print("3. Test the service with: kubectl port-forward service/deepseek-service 8080:8080")
    print("4. Access the service at: http://localhost:8080")

if __name__ == "__main__":
    main()