# Script to build and run the DeepSeek R1 application locally

Write-Host "Building and running DeepSeek R1 application locally..."

# Navigate to the server directory
Set-Location server

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Build the Docker image
Write-Host "Building Docker image..."
docker build -t deepseek-r1 .

# Run the Docker container
Write-Host "Running Docker container..."
docker run -p 8080:8080 deepseek-r1

Write-Host "Application is now running on http://localhost:8080"
Write-Host "You can test the health endpoint at http://localhost:8080/healthz"
Write-Host "You can test the inference endpoint with a POST request to http://localhost:8080/infer"