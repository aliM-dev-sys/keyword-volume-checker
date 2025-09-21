#!/usr/bin/env python3
"""
Startup script for Keyword Volume Checker
Provides easy commands for development and testing
"""

import subprocess
import sys
import os
import argparse

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def start_dev_server():
    """Start the development server"""
    print("🚀 Starting Keyword Volume Checker development server...")
    print("📱 Web dashboard: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def run_tests():
    """Run API tests"""
    return run_command("python test_api.py", "Running API tests")

def build_docker():
    """Build Docker image"""
    return run_command("docker build -t keyword-volume-checker .", "Building Docker image")

def run_docker():
    """Run Docker container"""
    print("🚀 Starting Keyword Volume Checker with Docker...")
    print("📱 Web dashboard: http://localhost:8000")
    print("\nPress Ctrl+C to stop the container\n")
    
    try:
        subprocess.run([
            "docker", "run", "--rm", "-p", "8000:8000",
            "-e", "KEYWORD_API_KEY=your_api_key_here",
            "-e", "KEYWORD_API_URL=https://api.example.com/keywords/volume",
            "keyword-volume-checker"
        ])
    except KeyboardInterrupt:
        print("\n👋 Container stopped")

def main():
    parser = argparse.ArgumentParser(description="Keyword Volume Checker Management")
    parser.add_argument("command", choices=[
        "install", "dev", "test", "build", "docker", "all"
    ], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_dependencies()
    elif args.command == "dev":
        if not os.path.exists("app"):
            print("❌ App directory not found. Make sure you're in the project root.")
            sys.exit(1)
        start_dev_server()
    elif args.command == "test":
        run_tests()
    elif args.command == "build":
        build_docker()
    elif args.command == "docker":
        run_docker()
    elif args.command == "all":
        print("🚀 Running full setup and test...")
        if install_dependencies():
            if run_tests():
                print("\n🎉 Setup complete! Run 'python start.py dev' to start the server")
            else:
                print("\n⚠️  Tests failed, but you can still run 'python start.py dev'")
        else:
            print("\n❌ Setup failed")

if __name__ == "__main__":
    main()
