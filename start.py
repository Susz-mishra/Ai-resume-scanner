#!/usr/bin/env python3
"""
AI Resume Scanner - Startup Script
This script handles environment setup and starts the Flask application.
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'flask', 'werkzeug', 'PyPDF2', 'docx', 'multipart'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if package == 'docx':
            spec = importlib.util.find_spec('docx')
        elif package == 'multipart':
            spec = importlib.util.find_spec('multipart')
        else:
            spec = importlib.util.find_spec(package)
        
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install requirements first:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['uploads', 'temp', 'backups']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def start_flask_app():
    """Start the Flask application."""
    try:
        print("\n🚀 Starting AI Resume Scanner...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the application")
        print("=" * 50)
        
        # Import and run the Flask app
        from app import app
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False
        )
        
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Make sure all requirements are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        sys.exit(1)

def main():
    """Main startup function."""
    print("=" * 50)
    print("    AI Resume Scanner - Startup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main()
