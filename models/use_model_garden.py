"""
Simple script to demonstrate using a model deployed from Vertex AI Model Garden
"""

def explain_model_garden_deployment():
    """
    Explain how to deploy and use models from Vertex AI Model Garden
    """
    print("Vertex AI Model Garden Deployment Guide")
    print("=" * 40)
    
    print("""
1. Visit the Vertex AI Model Garden:
   URL: https://console.cloud.google.com/vertex-ai/model-garden

2. Browse and select a pre-trained model:
   - For text classification: Look for BERT, DistilBERT, or similar models
   - For image classification: Look for Vision models
   - For other tasks: Search by task type

3. Deploy the model:
   - Click "DEPLOY" on the model page
   - Choose the smallest machine type (e2-standard-2 or smaller)
   - Set min/max replicas to 1 to stay within free tier
   - Configure endpoint name
   - Click "DEPLOY" to start deployment

4. Get your endpoint ID:
   - After deployment, note the endpoint ID from the console
   - You'll need this for making predictions

5. Use the model for predictions:
   """)
    
    # Example code (commented out since we don't have the actual endpoint)
    print("""
# Example prediction code (replace YOUR_ENDPOINT_ID with actual ID):
from google.cloud import aiplatform

# Initialize
aiplatform.init(project="golden-capsule-479805-q9", location="us-central1")

# Get endpoint
endpoint = aiplatform.Endpoint("YOUR_ENDPOINT_ID")

# Make prediction
instances = [{"text": "I love this product!"}]
predictions = endpoint.predict(instances=instances)

print(predictions)
""")

def create_sample_request():
    """
    Create a sample request file for testing
    """
    sample_request = {
        "instances": [
            {"text": "I love this product!"},
            {"text": "This is terrible."},
            {"text": "It's okay, not great but not bad either."}
        ]
    }
    
    import json
    with open("sample_request.json", "w") as f:
        json.dump(sample_request, f, indent=2)
    
    print("Created sample_request.json with sample data")
    print("Contents:")
    print(json.dumps(sample_request, indent=2))

def show_next_steps():
    """
    Show next steps for the user
    """
    print("\nNext Steps:")
    print("1. Go to https://console.cloud.google.com/vertex-ai/model-garden")
    print("2. Select and deploy a pre-trained model")
    print("3. Note the endpoint ID after deployment")
    print("4. Use the sample_request.json file to test your model")
    print("5. Make predictions using the Vertex AI SDK")

if __name__ == "__main__":
    explain_model_garden_deployment()
    create_sample_request()
    show_next_steps()