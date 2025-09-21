@echo off
REM Keyword Volume Checker Deployment Script for Windows
REM This script helps you deploy the keyword volume checker on your Windows server

echo 🚀 Keyword Volume Checker Deployment Script
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Visit: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo    Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ✅ .env file created. You can modify it if needed.
) else (
    echo ✅ .env file already exists
)

REM Create data directory
echo 📁 Creating data directory...
if not exist data mkdir data

REM Build and start the service
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting the service...
docker-compose up -d

REM Wait for the service to be ready
echo ⏳ Waiting for service to be ready...
timeout /t 10 /nobreak >nul

REM Check if the service is running
curl -f http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Service is running successfully!
    echo.
    echo 🌐 Access points:
    echo    Web Dashboard: http://localhost:8001
    echo    API Documentation: http://localhost:8001/docs
    echo    Health Check: http://localhost:8001/health
    echo.
    echo 📚 Example API calls:
    echo    curl "http://localhost:8001/check-volume?keyword=seo&country=US"
    echo    curl "http://localhost:8001/methods"
    echo.
    echo 🔧 Management commands:
    echo    docker-compose logs -f          # View logs
    echo    docker-compose down             # Stop service
    echo    docker-compose restart          # Restart service
) else (
    echo ❌ Service failed to start. Check logs with: docker-compose logs
    pause
    exit /b 1
)

echo.
echo 🎉 Deployment complete! Your keyword volume checker is ready to use.
echo    No API keys required - it uses open-source data sources!
pause
