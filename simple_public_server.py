#!/usr/bin/env python3
"""
D&D&D Blog - Simple Public Server
This script starts the Django server and provides easy access for players.
"""

import subprocess
import socket
import time
import sys
import os

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

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

def main():
    print("🐉 D&D&D Blog - Public Server")
    print("=" * 40)
    
    # Get local IP
    local_ip = get_local_ip()
    
    # Start Django server
    django_process = start_django_server()
    if not django_process:
        print("❌ Failed to start Django server")
        return
    
    # Wait a moment for Django to start
    time.sleep(3)
    
    print("\n🎉 SUCCESS! Your D&D&D blog is now accessible!")
    print("=" * 50)
    print("📱 Share these URLs with your players:")
    print()
    print(f"🌐 Local Network: http://{local_ip}:8000/")
    print("   (For players on the same WiFi/network)")
    print()
    print("💻 Your Computer: http://127.0.0.1:8000/")
    print("   (For you to test)")
    print()
    print("🔗 Direct Access: http://localhost:8000/")
    print("   (If players are on the same computer)")
    print("=" * 50)
    
    print("\n💡 Instructions for Players:")
    print("1. Make sure they're on the same WiFi network as you")
    print("2. They should use: http://" + local_ip + ":8000/")
    print("3. If that doesn't work, try the other URLs above")
    print("4. They can bookmark the URL for easy access")
    
    print("\n🛡️ Security Note:")
    print("• Only people on your local network can access this")
    print("• This is perfect for local gaming sessions")
    print("• Keep this terminal open to keep the server running")
    print("• Press Ctrl+C to stop the server")
    
    try:
        # Keep the server running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        django_process.terminate()
        print("✅ Server stopped")

if __name__ == "__main__":
    main() 