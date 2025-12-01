# Production deployment script for DeepSeek R1 on GCP
# This script handles the deployment of the full infrastructure including:
# - GKE cluster with GPU support
# - Artifact Registry
# - Vertex AI model deployment
# - Kubernetes deployments (CPU and GPU)

Write-Host "Starting production deployment of DeepSeek R1..." -ForegroundColor Green

# Check if required tools are installed
$requiredTools = @("gcloud", "kubectl", "terraform", "docker")
foreach ($tool in $requiredTools) {
    if (!(Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Host "Error: $tool is not installed or not in PATH" -ForegroundColor Red
        exit 1
    }
}

# Navigate to the infra directory
Set-Location -Path "$PSScriptRoot\infra"

# Initialize Terraform
Write-Host "Initializing Terraform..." -ForegroundColor Yellow
terraform init
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error initializing Terraform" -ForegroundColor Red
    exit 1
}

# Apply Terraform configuration
Write-Host "Applying Terraform configuration..." -ForegroundColor Yellow
terraform apply -auto-approve
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error applying Terraform configuration" -ForegroundColor Red
    exit 1
}

# Wait for resources to be ready
Write-Host "Waiting for resources to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Get project information from terraform outputs
$projectId = terraform output -raw project_id
$region = terraform output -raw region
$artifactRepo = terraform output -raw artifact_repo
$clusterName = terraform output -raw cluster_name
$zone = terraform output -raw zone

# Navigate back to the root directory
Set-Location -Path $PSScriptRoot

# Configure Docker auth
Write-Host "Configuring Docker authentication..." -ForegroundColor Yellow
gcloud auth configure-docker "${region}-docker.pkg.dev" -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error configuring Docker authentication" -ForegroundColor Red
    exit 1
}

# Build and push CPU image
$imageName = "us-docker.pkg.dev/$projectId/$artifactRepo/deepseek-r1:latest"
Write-Host "Building and pushing CPU image: $imageName" -ForegroundColor Yellow
docker build -t $imageName ./server
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error building CPU image" -ForegroundColor Red
    exit 1
}

docker push $imageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error pushing CPU image" -ForegroundColor Red
    exit 1
}

# Build and push GPU image
$gpuImageName = "us-docker.pkg.dev/$projectId/$artifactRepo/deepseek-r1-gpu:latest"
Write-Host "Building and pushing GPU image: $gpuImageName" -ForegroundColor Yellow
docker build -t $gpuImageName -f ./server/Dockerfile.gpu ./server
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error building GPU image" -ForegroundColor Red
    exit 1
}

docker push $gpuImageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error pushing GPU image" -ForegroundColor Red
    exit 1
}

# Get GKE credentials
Write-Host "Getting GKE credentials..." -ForegroundColor Yellow
gcloud container clusters get-credentials $clusterName --zone=$zone --project=$projectId
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error getting GKE credentials" -ForegroundColor Red
    exit 1
}

# Apply Kubernetes manifests
Write-Host "Applying Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f k8s/service-account.yaml
kubectl apply -f k8s/logging-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/gpu-deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Display deployment status
Write-Host "Checking deployment status..." -ForegroundColor Yellow
kubectl get pods

Write-Host "Production deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Monitor the deployment with: kubectl get pods" -ForegroundColor White
Write-Host "2. Check logs with: kubectl logs -l app=deepseek" -ForegroundColor White
Write-Host "3. Test the service with: kubectl port-forward service/deepseek-service 8080:8080" -ForegroundColor White
Write-Host "4. Access the service at: http://localhost:8080" -ForegroundColor White