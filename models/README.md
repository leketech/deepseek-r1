# Transformer Model Deployment

This directory contains the necessary files to deploy a lightweight transformer model (DistilBERT) on Google Kubernetes Engine.

## Files

- `Dockerfile`: Defines the container image for the model
- `requirements.txt`: Python dependencies
- `app.py`: Flask application serving the transformer model
- `deployment.yaml`: Kubernetes deployment and service configuration
- `test_model.py`: Script to test the deployed model

## Deployment Steps

1. Build the Docker image:
   ```
   docker build -t transformer-model .
   ```

2. Tag and push to Google Artifact Registry:
   ```
   docker tag transformer-model us-central1-docker.pkg.dev/golden-capsule-479805-q9/deepseek-repo/transformer-model:latest
   docker push us-central1-docker.pkg.dev/golden-capsule-479805-q9/deepseek-repo/transformer-model:latest
   ```

3. Deploy to GKE cluster:
   ```
   kubectl apply -f deployment.yaml
   ```

4. Check deployment status:
   ```
   kubectl get pods
   kubectl get services
   ```

5. Test the model:
   ```
   python test_model.py
   ```

## Model Details

The deployed model is a lightweight DistilBERT model fine-tuned for sentiment analysis. It takes text input and returns sentiment predictions.

## Resource Considerations

This deployment is optimized for the Google Cloud free tier:
- Uses e2-micro instances
- Limits CPU and memory resources
- Uses a lightweight model to minimize resource usage