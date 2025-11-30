# Setup script for Google Cloud Monitoring and Logging
# This script creates the necessary resources for monitoring the DeepSeek model deployment

# Set project ID (replace with your actual project ID)
$PROJECT_ID = if ($env:PROJECT_ID) { $env:PROJECT_ID } else { "YOUR_PROJECT_ID" }
$REGION = if ($env:REGION) { $env:REGION } else { "us-central1" }

Write-Host "Setting up monitoring and logging for project: $PROJECT_ID"

# Enable required APIs
Write-Host "Enabling required APIs..."
gcloud services enable `
  monitoring.googleapis.com `
  logging.googleapis.com `
  bigquery.googleapis.com `
  pubsub.googleapis.com `
  storage.googleapis.com

# Create BigQuery dataset for logs
Write-Host "Creating BigQuery dataset for logs..."
bq --location=$REGION mk -d --description "Dataset for DeepSeek model logs" "$PROJECT_ID:deepseek_logs"

# Create Cloud Storage bucket for log archiving
Write-Host "Creating Cloud Storage bucket for log archiving..."
gsutil mb -l $REGION "gs://deepseek-logs-archive-$PROJECT_ID"

# Create Pub/Sub topic for real-time log processing
Write-Host "Creating Pub/Sub topic for real-time log processing..."
gcloud pubsub topics create deepseek-model-logs

# Create log sink to export logs to BigQuery
Write-Host "Creating log sink to export logs to BigQuery..."
gcloud logging sinks create deepseek-bq-sink `
  "bigquery.googleapis.com/projects/$PROJECT_ID/datasets/deepseek_logs" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' `
  --description="Export model logs to BigQuery"

# Create log sink to export logs to Cloud Storage
Write-Host "Creating log sink to export logs to Cloud Storage..."
gcloud logging sinks create deepseek-storage-sink `
  "storage.googleapis.com/deepseek-logs-archive-$PROJECT_ID" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' `
  --description="Archive model logs to Cloud Storage"

# Create log sink to export logs to Pub/Sub
Write-Host "Creating log sink to export logs to Pub/Sub..."
gcloud logging sinks create deepseek-pubsub-sink `
  "pubsub.googleapis.com/projects/$PROJECT_ID/topics/deepseek-model-logs" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' `
  --description="Stream model logs to Pub/Sub"

# Create custom metrics from logs
Write-Host "Creating custom metrics from logs..."
gcloud logging metrics create model-inference-latency `
  --description="Latency metric for model inference" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="model_inference"' `
  --metric-descriptor-type=double `
  --metric-descriptor-unit=ms `
  --value-extractor='EXTRACT(jsonPayload.latency_ms)'

gcloud logging metrics create model-inference-count `
  --description="Count of model inferences" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="model_inference"' `
  --metric-descriptor-type=int64 `
  --value-extractor='1'

gcloud logging metrics create model-inference-errors `
  --description="Count of model inference errors" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" severity=ERROR' `
  --metric-descriptor-type=int64 `
  --value-extractor='1'

gcloud logging metrics create model-batch-size `
  --description="Batch size distribution" `
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="inference_success"' `
  --metric-descriptor-type=int64 `
  --value-extractor='EXTRACT(jsonPayload.batch_size)'

Write-Host "Monitoring and logging setup complete!"
Write-Host "Next steps:"
Write-Host "1. Update the deployment with the new configuration"
Write-Host "2. Deploy the updated application"
Write-Host "3. Verify logs are being exported to BigQuery, Cloud Storage, and Pub/Sub"
Write-Host "4. Check the Cloud Monitoring dashboards"