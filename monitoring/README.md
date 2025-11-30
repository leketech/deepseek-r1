# Monitoring and Logging Setup for DeepSeek Model Deployment

This document explains how to set up comprehensive monitoring and logging for the DeepSeek model deployment on Google Cloud Platform.

## Overview

The monitoring and logging setup includes:

1. **Cloud Monitoring Dashboards** - Visualize key metrics
2. **Alerting Policies** - Get notified of issues
3. **Centralized Logging** - Collect and analyze logs
4. **Custom Metrics** - Track model-specific performance indicators

## Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Appropriate IAM permissions

## Setup Process

### 1. Enable Required APIs

```bash
gcloud services enable \
  monitoring.googleapis.com \
  logging.googleapis.com \
  bigquery.googleapis.com \
  pubsub.googleapis.com \
  storage.googleapis.com
```

### 2. Run Setup Script

Execute the PowerShell setup script:

```powershell
./setup-monitoring.ps1
```

Or set environment variables and run:

```powershell
$env:PROJECT_ID="your-project-id"
$env:REGION="us-central1"
./setup-monitoring.ps1
```

### 3. Deploy Updated Application

The updated application includes enhanced logging capabilities:

- Structured JSON logging
- Custom metrics exposure
- Error tracking and counting
- Latency measurements

## Monitoring Components

### Dashboards

1. **General Monitoring Dashboard** (`dashboard.json`)
   - CPU and memory utilization
   - Request latency and rate
   - Error rates
   - Replica counts

2. **Model Performance Dashboard** (`model-dashboard.json`)
   - Inference latency
   - Throughput metrics
   - Batch size distribution
   - GPU utilization

### Alerting Policies

1. **Error Rate Alert** (`error-alert.json`)
   - Triggers when error rate exceeds 5 errors per second

2. **Latency Alert** (`latency-alert.json`)
   - Triggers when latency exceeds 1000ms

3. **General Health Alert** (`alert-policy.json`)
   - Triggers when available replicas drop below 1
   - Triggers when CPU utilization exceeds 80%

## Logging Configuration

### Log Exports

Logs are exported to three destinations:

1. **BigQuery** - For analysis and reporting
2. **Cloud Storage** - For long-term archival
3. **Pub/Sub** - For real-time processing

### Custom Metrics

1. **Model Inference Latency** - Tracks inference response times
2. **Inference Count** - Counts total inferences
3. **Error Count** - Tracks inference errors
4. **Batch Size** - Monitors batch processing efficiency

## Verification

After deployment, verify the setup by:

1. Checking Cloud Monitoring dashboards
2. Verifying log exports to BigQuery, Cloud Storage, and Pub/Sub
3. Testing alert policies
4. Monitoring custom metrics

## Maintenance

- Review log retention policies
- Monitor BigQuery dataset costs
- Update alert thresholds as needed
- Regularly review dashboard effectiveness