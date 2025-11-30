"""
Vertex AI Model Deployment from Model Garden
This script demonstrates how to deploy a pre-trained model from Vertex AI Model Garden.
"""

import os
from google.cloud import aiplatform

# Initialize Vertex AI
PROJECT_ID = "golden-capsule-479805-q9"
LOCATION = "us-central1"
ENDPOINT_NAME = "distilbert-endpoint"

# Initialize the Vertex AI client
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def list_available_models():
    """List available pre-trained models in Model Garden"""
    try:
        # List public models
        models = aiplatform.Model.list()
        print("Available models:")
        for model in models:
            print(f"- {model.display_name}")
    except Exception as e:
        print(f"Error listing models: {e}")

def deploy_distilbert_model():
    """Deploy a pre-trained DistilBERT model from Model Garden"""
    try:
        # For demonstration purposes, we'll show how to deploy a model
        # In practice, you would use a specific model from Model Garden
        
        print("To deploy a pre-trained model from Model Garden:")
        print("1. Visit https://console.cloud.google.com/vertex-ai/model-garden")
        print("2. Browse and select a model (e.g., BERT, DistilBERT, etc.)")
        print("3. Click 'DEPLOY' and follow the wizard")
        print("4. Configure the endpoint settings")
        print("5. Deploy the model")
        
        # Example code for deploying a model (this is pseudo-code as actual model IDs vary)
        # model = aiplatform.Model.upload(
        #     display_name="pretrained-distilbert",
        #     model_resource_name="projects/PROJECT/locations/LOCATION/models/MODEL_ID"
        # )
        # 
        # endpoint = model.deploy(
        #     machine_type="n1-standard-2",
        #     min_replica_count=1,
        #     max_replica_count=1
        # )
        # 
        # print(f"Model deployed to endpoint: {endpoint.resource_name}")
        
        print("\nFor free tier usage, select the smallest machine type available.")
        print("Vertex AI offers free tier benefits for model deployment.")
        
    except Exception as e:
        print(f"Error deploying model: {e}")

def create_prediction_script():
    """Create a sample prediction script"""
    prediction_script = '''
"""
Sample prediction script for Vertex AI deployed model
"""

from google.cloud import aiplatform

# Initialize Vertex AI
PROJECT_ID = "golden-capsule-479805-q9"
LOCATION = "us-central1"
ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # Replace with your actual endpoint ID

# Initialize client
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def predict_text_sentiment(text):
    """Predict sentiment of text using deployed model"""
    # Get the endpoint
    endpoint = aiplatform.Endpoint(ENDPOINT_ID)
    
    # Prepare instances
    instances = [{"text": text}]
    
    # Make prediction
    predictions = endpoint.predict(instances=instances)
    
    return predictions

if __name__ == "__main__":
    # Example usage
    text = "I love using Google Cloud Platform for my ML projects!"
    result = predict_text_sentiment(text)
    print(f"Text: {text}")
    print(f"Prediction: {result}")
'''
    
    with open("prediction_sample.py", "w") as f:
        f.write(prediction_script)
    
    print("Created prediction_sample.py with sample prediction code")

if __name__ == "__main__":
    print("Vertex AI Model Garden Deployment Script")
    print("=" * 40)
    
    # List available models
    list_available_models()
    
    print("\n")
    
    # Deploy model
    deploy_distilbert_model()
    
    # Create prediction script
    create_prediction_script()
    
    print("\nNext steps:")
    print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
    print("2. Select and deploy a pre-trained model")
    print("3. Use the prediction_sample.py script for making predictions")