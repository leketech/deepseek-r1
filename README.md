# DeepSeek R1 Deployment

## Quick Commands & Tips

### Authenticate locally (gcloud):
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT
gcloud services enable container.googleapis.com artifactregistry.googleapis.com compute.googleapis.com
```

### Apply Terraform:
```bash
cd infra
terraform init
terraform plan -var="project_id=YOUR_PROJECT" -var="region=us-central1" -var="zone=us-central1-a"
terraform apply -var="project_id=YOUR_PROJECT" -auto-approve
```

### Create GPU node pool if not created or scale it:
```bash
gcloud container node-pools create gpu-pool \
  --cluster deepseek-gke \
  --zone us-central1-a \
  --num-nodes 1 \
  --machine-type n1-highmem-16 \
  --accelerator type=nvidia-tesla-a100,count=1 \
  --enable-autoscaling --min-nodes=0 --max-nodes=5
```

### Apply k8s manifests:
```bash
kubectl apply -f k8s/service-account.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

### Set up Workload Identity binding:
After deploying the infrastructure and Kubernetes manifests, run the Workload Identity setup script:

On Linux/Mac:
```bash
./setup-workload-identity.sh
```

On Windows:
```powershell
./setup-workload-identity.ps1
```

Make sure to update the script variables with your actual project ID before running.

## Local Deployment

If you don't have access to a GCP project with billing enabled, you can run the application locally:

On Linux/Mac:
```bash
./local-deployment.sh
```

On Windows:
```powershell
./local-deployment.ps1
```

This will build and run the application locally using Docker.

## Secrets for GitHub Repo

Create these secrets in your GitHub repository:

- `GCP_PROJECT` = your GCP project id
- `GCP_REGION` = e.g. us-central1
- `GKE_CLUSTER` = cluster name
- `WIF_PROVIDER` = Workload Identity Provider ID (e.g., projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID)
- `WIF_SERVICE_ACCOUNT` = Service account email for Workload Identity Federation
- Optionally `ARTIFACT_REPO` if you want to parameterize

## Security Note

This workflow now uses Workload Identity Federation (WIF) with short-lived tokens instead of long-lived service account keys, providing enhanced security.

## DevOps Best-Practice Checklist

- **IaC**: Terraform + remote state + review CI plan on PRs
- **CI**: Build, unit test, vulnerability scan (Trivy) and push images to Artifact Registry
- **CD**: Rolling/canary deployments; keep rollback image tag strategy
- **Secrets**: Secret Manager + Workload Identity Federation (avoid JSON keys entirely)
- **Observability**: Export /metrics (Prometheus) and logs to Cloud Logging. Set alerts for P95 latency, GPU memory OOMs
- **Security**: Binary Authorization or image vulnerability scanning, least-privilege IAM
- **Cost**: Use preemptible GPUs for batch workloads; scale-to-zero for low-traffic endpoints
- **Quotas**: Request GPU quotas early for your chosen region