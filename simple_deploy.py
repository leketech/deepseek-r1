from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="golden-capsule-479805-q9", location="us-central1")

# Print instructions for deploying a pre-trained model from Model Garden
print("To deploy a pre-trained model from Vertex AI Model Garden:")
print("1. Visit the Vertex AI Model Garden in the Google Cloud Console")
print("2. Select a pre-trained model (e.g., DistilBERT for text classification)")
print("3. Note the model endpoint ID after deployment")
print("4. Update the predict_model.py script with your endpoint ID")
print("5. Run the script to make predictions using your deployed model")

print("\nAlternatively, you can use the gcloud CLI to deploy a model:")
print("gcloud ai models deploy --model=MODEL_ID --endpoint=ENDPOINT_ID --region=us-central1")