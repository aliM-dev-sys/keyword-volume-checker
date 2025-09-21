FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app ./app

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV CACHE_DB_PATH=/app/data/keyword_volumes.db

# Expose port
EXPOSE 8001

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run with error handling
CMD ["python", "-c", "import app.main; print('App imported successfully'); import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8001, log_level='debug')"]
