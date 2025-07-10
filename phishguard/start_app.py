#!/usr/bin/env python3
"""
PhishGuard QR - Startup Script
"""

import os
import sys
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pyzbar', 'PIL', 'requests', 
        'tldextract', 'whois'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with:")
        print("pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API keys...")
    
    google_key = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
    virustotal_key = os.getenv("VIRUSTOTAL_API_KEY")
    
    if google_key and google_key != "your_google_api_key_here":
        print("✅ Google Safe Browsing API key configured")
    else:
        print("⚠️  Google Safe Browsing API key not configured (optional)")
    
    if virustotal_key and virustotal_key != "your_virustotal_api_key_here":
        print("✅ VirusTotal API key configured")
    else:
        print("⚠️  VirusTotal API key not configured (optional)")
    
    if not google_key and not virustotal_key:
        print("\n💡 Tip: Configure API keys for enhanced detection:")
        print("1. Copy env_template.txt to .env")
        print("2. Add your API keys to the .env file")
        print("3. Restart the application")

def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("📄 Loading environment variables from .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting PhishGuard QR...")
    
    try:
        from app import app
        
        # Get the port from environment or use default
        port = int(os.getenv("PORT", 5000))
        host = os.getenv("HOST", "127.0.0.1")
        
        print(f"🌐 Server will be available at: http://{host}:{port}")
        print("📱 Camera scanning requires HTTPS in production")
        print("\n⏳ Starting server...")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            url = f"http://{host}:{port}"
            print(f"🌐 Opening browser to: {url}")
            webbrowser.open(url)
        
        # Start browser in a separate thread
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the Flask app
        app.run(
            host=host,
            port=port,
            debug=os.getenv("FLASK_DEBUG", "True").lower() == "true"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        print("Please check the error message above and try again")

def main():
    """Main startup function"""
    print("🛡️  PhishGuard QR - QR Code Phishing Detection System")
    print("=" * 60)
    
    # Load environment variables
    load_env_file()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check API keys
    check_api_keys()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main() 