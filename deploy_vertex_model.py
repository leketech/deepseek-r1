import os
from google.cloud import aiplatform
from google.auth import default

# Set the project and location
PROJECT_ID = "golden-capsule-479805-q9"
LOCATION = "us-central1"

def initialize_vertex_ai():
    """Initialize the Vertex AI client"""
    try:
        credentials, project = default()
        aiplatform.init(
            project=PROJECT_ID,
            location=LOCATION,
            credentials=credentials
        )
        print("Vertex AI client initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing Vertex AI client: {e}")
        return False

def create_endpoint():
    """Create a new endpoint for model deployment"""
    try:
        print("Creating endpoint...")
        
        # Create a new endpoint
        endpoint = aiplatform.Endpoint.create(
            display_name="deepseek-endpoint",
            project=PROJECT_ID,
            location=LOCATION
        )
        
        print(f"Endpoint created successfully: {endpoint.resource_name}")
        endpoint_id = endpoint.name.split('/')[-1]
        print("Endpoint ID:", endpoint_id)
        
        # Save the endpoint ID for later use
        with open('vertex_endpoint_id.txt', 'w') as f:
            f.write(endpoint_id)
        print(f"Endpoint ID saved to vertex_endpoint_id.txt: {endpoint_id}")
        
        return endpoint_id
    except Exception as e:
        print(f"Error creating endpoint: {e}")
        print("Make sure you have the necessary permissions to create endpoints in Vertex AI")
        return None

def main():
    """Main function to deploy Vertex AI model"""
    print("Vertex AI Model Deployment")
    print("=" * 30)
    
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        return
    
    # Create endpoint
    endpoint_id = create_endpoint()
    if not endpoint_id:
        return
    
    # Provide instructions for next steps
    print("\nNext steps:")
    print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
    print("2. Select a pre-trained model (e.g., text-bison for text generation)")
    print("3. Deploy it to your endpoint using the endpoint ID above")
    print("4. Update the predict.py script with your endpoint ID")
    print("5. Run the script to make predictions using your deployed model")
    
    print(f"\nYour endpoint ID is: {endpoint_id}")
    print("This has been saved to 'vertex_endpoint_id.txt'")

if __name__ == "__main__":
    main()