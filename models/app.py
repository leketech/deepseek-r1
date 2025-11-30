from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize a lightweight transformer model
# Using a small model to stay within free tier limits
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    # Perform inference
    result = classifier(text)
    
    return jsonify({
        'text': text,
        'prediction': result
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)