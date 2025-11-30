FROM python:3.11-slim

# Install minimal deps; if GPU image needed, use nvidia/cuda base instead.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for performance optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONMALLOC=malloc \
    UVICORN_TIMEOUT=300 \
    UVICORN_KEEPALIVE=60 \
    UVICORN_BACKLOG=2048 \
    UVICORN_WORKERS=4 \
    BATCH_SIZE=32 \
    BATCH_TIMEOUT=0.01 \
    MAX_CONCURRENT_BATCHES=4

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py /app/

# Expose port
EXPOSE 8080

# Run as non-root user
USER 1000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/healthz || exit 1

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]