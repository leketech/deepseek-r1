#!/bin/bash

# Script to build and run the DeepSeek R1 application locally

echo "Building and running DeepSeek R1 application locally..."

# Navigate to the server directory
cd server

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build the Docker image
echo "Building Docker image..."
docker build -t deepseek-r1 .

# Run the Docker container
echo "Running Docker container..."
docker run -p 8080:8080 deepseek-r1

echo "Application is now running on http://localhost:8080"
echo "You can test the health endpoint at http://localhost:8080/healthz"
echo "You can test the inference endpoint with a POST request to http://localhost:8080/infer"