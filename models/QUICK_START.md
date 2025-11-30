# Quick Start: Vertex AI Model Garden

## Deploy and Use Pre-trained Models

### 1. Deploy a Model
1. Go to [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Select project: `golden-capsule-479805-q9`
3. Find a model (e.g., DistilBERT)
4. Click "DEPLOY"
5. Use smallest machine type, 1 replica
6. Wait for deployment (~10 minutes)

### 2. Get Endpoint ID
1. Go to "Endpoints" section
2. Copy your endpoint ID

### 3. Install Libraries
```bash
pip install google-cloud-aiplatform
```

### 4. Update Prediction Script
Edit [predict_model.py](file:///C:/Users/Leke/deepseek/deepseek-r1/models/predict_model.py):
1. Replace `YOUR_ENDPOINT_ID` with actual ID
2. Uncomment prediction code

### 5. Make Predictions
```bash
python predict_model.py
```

### 6. Test with Sample Data
Use [sample_request.json](file:///C:/Users/Leke/deepseek/deepseek-r1/models/sample_request.json) for batch testing

---

## Key Files

- [predict_model.py](file:///C:/Users/Leke/deepseek/deepseek-r1/models/predict_model.py) - Main prediction script
- [sample_request.json](file:///C:/Users/Leke/deepseek/deepseek-r1/models/sample_request.json) - Sample data
- [requirements.txt](file:///C:/Users/Leke/deepseek/deepseek-r1/models/requirements.txt) - Dependencies (if using custom model)

## Free Tier Tips

- Use smallest machine types
- Keep replica count at 1
- Delete endpoints when not in use
- Monitor usage regularly