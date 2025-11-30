from google.cloud import aiplatform

# Initialize the Vertex AI client
aiplatform.init(project="golden-capsule-479805-q9", location="us-central1")

# List available models
try:
    models = aiplatform.Model.list()
    print("Available models:")
    for model in models:
        print(f"- {model.display_name} ({model.resource_name})")
except Exception as e:
    print(f"Error listing models: {e}")

# Try to list model templates from Model Garden
try:
    # This would typically be how you access Model Garden models
    # Note: Actual API might vary based on permissions and available services
    print("\nModel Garden exploration would go here...")
    print("For Model Garden, you typically access models through the console or specific APIs")
except Exception as e:
    print(f"Error accessing Model Garden: {e}")