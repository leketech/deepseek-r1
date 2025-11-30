"""
Script to make predictions using a deployed model from Vertex AI Model Garden
"""

def create_prediction_script():
    """
    Create a script that shows how to make predictions with a deployed model
    """
    prediction_script = '''#!/usr/bin/env python3
"""
Make predictions using a deployed model from Vertex AI Model Garden
"""

import json
from google.cloud import aiplatform

# Configuration - Update these values after deploying your model
PROJECT_ID = "golden-capsule-479805-q9"
LOCATION = "us-central1"
ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # Replace with your actual endpoint ID

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
    print("\\n1. Making a single prediction:")
    text = "I love using Google Cloud Platform for my ML projects!"
    print(f"Input: {text}")
    
    # Uncomment the following lines after you have deployed your model and updated ENDPOINT_ID
    # result = make_prediction(text)
    # if result:
    #     print(f"Prediction: {result}")
    
    print("(Note: Uncomment the code above after deploying your model)")
    
    # Example 2: Batch prediction from file
    print("\\n2. Making batch predictions from sample_request.json:")
    print("(Note: Uncomment the code below after deploying your model and updating ENDPOINT_ID)")
    
    # Uncomment the following lines after you have deployed your model and updated ENDPOINT_ID
    # batch_result = batch_predict_from_file("sample_request.json")
    # if batch_result:
    #     print("Batch predictions:")
    #     print(json.dumps(batch_result.predictions, indent=2))

if __name__ == "__main__":
    main()
'''
    
    with open("predict_model.py", "w") as f:
        f.write(prediction_script)
    
    print("Created predict_model.py with prediction code")
    print("Remember to:")
    print("1. Deploy a model from Vertex AI Model Garden")
    print("2. Update the ENDPOINT_ID in the script")
    print("3. Run the script to make predictions")

if __name__ == "__main__":
    create_prediction_script()
    print("\\nTo use this prediction script:")
    print("1. Deploy a model from Vertex AI Model Garden")
    print("2. Update the ENDPOINT_ID in predict_model.py")
    print("3. Run: python predict_model.py")