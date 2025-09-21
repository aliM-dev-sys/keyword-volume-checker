#!/bin/bash

# Keyword Volume Checker Deployment Script
# This script helps you deploy the keyword volume checker on your server

set -e

echo "🚀 Keyword Volume Checker Deployment Script"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created. You can modify it if needed."
else
    echo "✅ .env file already exists"
fi

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data
chmod 755 data

# Build and start the service
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting the service..."
docker-compose up -d

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if the service is running
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Service is running successfully!"
    echo ""
    echo "🌐 Access points:"
    echo "   Web Dashboard: http://localhost:8001"
    echo "   API Documentation: http://localhost:8001/docs"
    echo "   Health Check: http://localhost:8001/health"
    echo ""
    echo "📚 Example API calls:"
    echo "   curl 'http://localhost:8001/check-volume?keyword=seo&country=US'"
    echo "   curl 'http://localhost:8001/methods'"
    echo ""
    echo "🔧 Management commands:"
    echo "   docker-compose logs -f          # View logs"
    echo "   docker-compose down             # Stop service"
    echo "   docker-compose restart          # Restart service"
    echo "   docker-compose exec keyword-volume-checker python -c \"from app.services import clear_cache; clear_cache()\"  # Clear cache"
else
    echo "❌ Service failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "🎉 Deployment complete! Your keyword volume checker is ready to use."
echo "   No API keys required - it uses open-source data sources!"
