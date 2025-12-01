from google.cloud import aiplatform
import time

# Initialize Vertex AI
aiplatform.init(project="golden-capsule-479805-q9", location="us-central1")

# Read the endpoint ID from the file
try:
    with open('vertex_endpoint_id.txt', 'r') as f:
        ENDPOINT_ID = f.read().strip()
    print(f"Using endpoint ID: {ENDPOINT_ID}")
except FileNotFoundError:
    print("Endpoint ID file not found. Please run create_endpoint.py first.")
    exit(1)

# Create an endpoint object
try:
    endpoint = aiplatform.Endpoint(ENDPOINT_ID)
    print("Endpoint connected successfully")
except Exception as e:
    print(f"Error connecting to endpoint: {e}")
    exit(1)

# Print instructions for making predictions
print("\nTo make predictions using your deployed model:")
print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
print("2. Select a pre-trained model (e.g., text-bison for text generation)")
print("3. Deploy it to your endpoint")
print("4. Run this script to get predictions using your deployed model")

# Example prediction data for text generation
prediction_data = [
    {
        "prompt": "Write a short story about a robot learning to paint",
        "temperature": 0.7,
        "max_output_tokens": 256
    }
]

try:
    # Make a prediction (this will fail if no model is deployed)
    print("\nMaking prediction...")
    start_time = time.time()
    prediction = endpoint.predict(instances=prediction_data)
    end_time = time.time()
    
    print("Prediction results:")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(prediction)
    
    # Print the generated text if available
    if prediction.predictions:
        for i, pred in enumerate(prediction.predictions):
            print(f"\nPrediction {i+1}:")
            if isinstance(pred, dict) and 'predictions' in pred:
                print(pred['predictions'])
            else:
                print(pred)
                
except Exception as e:
    print(f"Error making prediction: {e}")
    print("\nThis is expected if no model has been deployed to the endpoint yet.")
    print("To deploy a model:")
    print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
    print("2. Select a pre-trained model")
    print("3. Deploy it to your endpoint")