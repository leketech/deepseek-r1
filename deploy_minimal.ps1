# Deploy minimal infrastructure for DeepSeek R1 project
# This script deploys only the basic infrastructure without GKE cluster

Write-Host "Setting up environment variables..."
$env:GOOGLE_APPLICATION_CREDENTIALS = "infra/terraform-key.json"

Write-Host "Initializing Terraform..."
Set-Location -Path "infra"
terraform init -reconfigure

Write-Host "Applying minimal infrastructure..."
terraform apply -auto-approve

Write-Host "Minimal infrastructure deployment complete!"
Write-Host "You can now proceed with requesting SSD quota increase using the instructions in quota_increase_instructions.txt"