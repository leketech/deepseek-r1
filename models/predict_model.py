#!/usr/bin/env python3
"""
Make predictions using a deployed model from Vertex AI Model Garden
"""

import json
from google.cloud import aiplatform

# Configuration - Update these values after deploying your model
PROJECT_ID = "golden-capsule-479805-q9"
LOCATION = "us-central1"
# ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # Replace with your actual endpoint ID
# For demonstration purposes, we'll use a placeholder
ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # You'll replace this with your actual endpoint ID

def make_prediction(text):
    """
    Make a prediction using the deployed model
    
    Args:
        text (str): Input text for prediction
        
    Returns:
        dict: Prediction results
    """
    try:
        # Initialize Vertex AI
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
        
        # Get the endpoint
        endpoint = aiplatform.Endpoint(ENDPOINT_ID)
        
        # Prepare instances
        instances = [{"text": text}]
        
        # Make prediction
        predictions = endpoint.predict(instances=instances)
        
        return predictions
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None

def batch_predict_from_file(filename):
    """
    Make batch predictions from a JSON file
    
    Args:
        filename (str): Path to JSON file with instances
        
    Returns:
        list: List of predictions
    """
    try:
        # Load instances from file
        with open(filename, 'r') as f:
            data = json.load(f)
            
        instances = data.get('instances', [])
        
        if not instances:
            print("No instances found in the file")
            return []
            
        # Initialize Vertex AI
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
        
        # Get the endpoint
        endpoint = aiplatform.Endpoint(ENDPOINT_ID)
        
        # Make batch prediction
        predictions = endpoint.predict(instances=instances)
        
        return predictions
        
    except Exception as e:
        print(f"Error making batch prediction: {e}")
        return None

def main():
    """
    Main function to demonstrate predictions
    """
    print("Vertex AI Model Garden Prediction Demo")
    print("=" * 40)
    
    # Example 1: Single prediction
    print("\n1. Making a single prediction:")
    text = "I love using Google Cloud Platform for my ML projects!"
    print(f"Input: {text}")
    
    # For demonstration, we'll show what the code would look like
    # when you have a real endpoint deployed
    print("\nTo make actual predictions, you need to:")
    print("1. Deploy a model from Vertex AI Model Garden")
    print("2. Replace YOUR_ENDPOINT_ID with the actual endpoint ID")
    print("3. Uncomment the following lines:")
    print("")
    print("# result = make_prediction(text)")
    print("# if result:")
    print("#     print(f\"Prediction: {result}\")")
    
    # Example 2: Batch prediction from file
    print("\n2. Making batch predictions from sample_request.json:")
    print("To make batch predictions, uncomment the following lines after deploying your model:")
    print("")
    print("# batch_result = batch_predict_from_file(\"sample_request.json\")")
    print("# if batch_result:")
    print("#     print(\"Batch predictions:\")")
    print("#     print(json.dumps(batch_result.predictions, indent=2))")

    print("\n" + "=" * 40)
    print("NEXT STEPS:")
    print("1. Visit https://console.cloud.google.com/vertex-ai/model-garden")
    print("2. Select and deploy a pre-trained model (e.g., DistilBERT)")
    print("3. Note the endpoint ID after deployment")
    print("4. Update ENDPOINT_ID in this script with your actual endpoint ID")
    print("5. Uncomment the prediction code to make actual predictions")

if __name__ == "__main__":
    main()