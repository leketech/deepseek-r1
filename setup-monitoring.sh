#!/bin/bash

# Setup script for Google Cloud Monitoring and Logging
# This script creates the necessary resources for monitoring the DeepSeek model deployment

# Set project ID (replace with your actual project ID)
PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
REGION="${REGION:-us-central1}"

echo "Setting up monitoring and logging for project: $PROJECT_ID"

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable \
  monitoring.googleapis.com \
  logging.googleapis.com \
  bigquery.googleapis.com \
  pubsub.googleapis.com \
  storage.googleapis.com

# Create BigQuery dataset for logs
echo "Creating BigQuery dataset for logs..."
bq --location=$REGION mk -d --description "Dataset for DeepSeek model logs" $PROJECT_ID:deepseek_logs

# Create Cloud Storage bucket for log archiving
echo "Creating Cloud Storage bucket for log archiving..."
gsutil mb -l $REGION gs://deepseek-logs-archive-$PROJECT_ID

# Create Pub/Sub topic for real-time log processing
echo "Creating Pub/Sub topic for real-time log processing..."
gcloud pubsub topics create deepseek-model-logs

# Create log sink to export logs to BigQuery
echo "Creating log sink to export logs to BigQuery..."
gcloud logging sinks create deepseek-bq-sink \
  bigquery.googleapis.com/projects/$PROJECT_ID/datasets/deepseek_logs \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' \
  --description="Export model logs to BigQuery"

# Create log sink to export logs to Cloud Storage
echo "Creating log sink to export logs to Cloud Storage..."
gcloud logging sinks create deepseek-storage-sink \
  storage.googleapis.com/deepseek-logs-archive-$PROJECT_ID \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' \
  --description="Archive model logs to Cloud Storage"

# Create log sink to export logs to Pub/Sub
echo "Creating log sink to export logs to Pub/Sub..."
gcloud logging sinks create deepseek-pubsub-sink \
  pubsub.googleapis.com/projects/$PROJECT_ID/topics/deepseek-model-logs \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server"' \
  --description="Stream model logs to Pub/Sub"

# Create custom metrics from logs
echo "Creating custom metrics from logs..."
gcloud logging metrics create model-inference-latency \
  --description="Latency metric for model inference" \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="model_inference"' \
  --metric-descriptor-type=double \
  --metric-descriptor-unit=ms \
  --value-extractor='EXTRACT(jsonPayload.latency_ms)'

gcloud logging metrics create model-inference-count \
  --description="Count of model inferences" \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="model_inference"' \
  --metric-descriptor-type=int64 \
  --value-extractor='1'

gcloud logging metrics create model-inference-errors \
  --description="Count of model inference errors" \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" severity=ERROR' \
  --metric-descriptor-type=int64 \
  --value-extractor='1'

gcloud logging metrics create model-batch-size \
  --description="Batch size distribution" \
  --log-filter='resource.type="k8s_container" resource.labels.container_name="server" jsonPayload.event="inference_success"' \
  --metric-descriptor-type=int64 \
  --value-extractor='EXTRACT(jsonPayload.batch_size)'

echo "Monitoring and logging setup complete!"
echo "Next steps:"
echo "1. Update the deployment with the new configuration"
echo "2. Deploy the updated application"
echo "3. Verify logs are being exported to BigQuery, Cloud Storage, and Pub/Sub"
echo "4. Check the Cloud Monitoring dashboards"