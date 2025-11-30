import requests
import json

# Test the model endpoint
def test_model():
    # Replace with your actual service IP/hostname
    url = "http://localhost:8080/predict"
    
    # Test data
    test_data = {
        "text": "I love this product! It's amazing."
    }
    
    try:
        response = requests.post(url, json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Input: {test_data['text']}")
            print(f"Prediction: {result}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_model()