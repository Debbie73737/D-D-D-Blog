#!/usr/bin/env python3
"""
D&D&D Blog - Public Server Starter
This script starts the Django server and creates a public tunnel using ngrok.
Players can access your blog using the generated public URL.
"""

import subprocess
import time
import sys
from pyngrok import ngrok
import threading

def start_django_server():
    """Start the Django development server"""
    print("🚀 Starting Django server...")
    try:
        # Start Django server on all interfaces
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Error starting Django server: {e}")
        return None

def create_public_tunnel():
    """Create a public tunnel using ngrok"""
    print("🌐 Creating public tunnel...")
    try:
        # Create HTTP tunnel to port 8000
        public_url = ngrok.connect(8000, "http")
        print(f"✅ Public URL created: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        return None

def main():
    print("🐉 D&D&D Blog - Public Server")
    print("=" * 40)
    
    # Start Django server
    django_process = start_django_server()
    if not django_process:
        print("❌ Failed to start Django server")
        return
    
    # Wait a moment for Django to start
    time.sleep(3)
    
    # Create public tunnel
    public_url = create_public_tunnel()
    if not public_url:
        print("❌ Failed to create public tunnel")
        django_process.terminate()
        return
    
    print("\n🎉 SUCCESS! Your D&D&D blog is now public!")
    print("=" * 50)
    print(f"🌐 Public URL: {public_url}")
    print("📱 Share this URL with your players!")
    print("🔗 They can access it from anywhere!")
    print("=" * 50)
    print("\n💡 Tips:")
    print("• The URL will change each time you restart the server")
    print("• Keep this terminal open to keep the server running")
    print("• Press Ctrl+C to stop the server")
    print("• Players can bookmark the URL for easy access")
    
    try:
        # Keep the server running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        django_process.terminate()
        ngrok.kill()
        print("✅ Server stopped")

if __name__ == "__main__":
    main() 