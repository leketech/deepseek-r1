"""
Vertex AI Model Deployment Script
This script demonstrates how to deploy a pre-trained model from Vertex AI Model Garden.
"""

from google.cloud import aiplatform

def deploy_model_from_garden():
    """
    Deploy a pre-trained model from Vertex AI Model Garden.
    Note: This requires proper permissions and enabled services.
    """
    
    # Initialize Vertex AI
    aiplatform.init(
        project="golden-capsule-479805-q9",
        location="us-central1"
    )
    
    # Example: Deploying a pre-trained text classification model
    # In practice, you would use a specific model from Model Garden
    try:
        # This is a placeholder - actual model deployment would depend on 
        # which specific model you want to use from Model Garden
        print("To deploy a model from Model Garden:")
        print("1. Visit https://console.cloud.google.com/vertex-ai/model-garden")
        print("2. Select a pre-trained model (e.g., BERT, T5, etc.)")
        print("3. Click 'Deploy' and follow the wizard")
        print("4. Get the endpoint URL for inference")
        
        # Placeholder for actual deployment code
        # model = aiplatform.Model.upload(
        #     display_name="my-model",
        #     model_resource_name="projects/PROJECT/locations/LOCATION/models/MODEL_ID"
        # )
        # endpoint = model.deploy(machine_type="e2-standard-2")
        
        return "Model deployment instructions printed above"
        
    except Exception as e:
        print(f"Error deploying model: {e}")
        return None

def test_model_endpoint(endpoint_url, api_key):
    """
    Test the deployed model endpoint.
    """
    import requests
    import json
    
    # Example payload for text classification
    payload = {
        "instances": [
            "I love this product!",
            "This is terrible."
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{endpoint_url}:predict",
            data=json.dumps(payload),
            headers=headers
        )
        return response.json()
    except Exception as e:
        print(f"Error testing model: {e}")
        return None

if __name__ == "__main__":
    print("Vertex AI Model Deployment")
    print("=" * 30)
    
    # Deploy model
    result = deploy_model_from_garden()
    print(result)
    
    print("\nNext steps:")
    print("1. Deploy model through Google Cloud Console")
    print("2. Get your endpoint URL and API key")
    print("3. Use test_model_endpoint() function to test")