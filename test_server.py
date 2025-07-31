#!/usr/bin/env python3
"""
Test script to verify D&D&D blog server accessibility
"""

import requests
import socket

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def test_server():
    """Test if the server is accessible"""
    local_ip = get_local_ip()
    
    print("🧪 Testing D&D&D Blog Server Access")
    print("=" * 40)
    
    # Test URLs
    test_urls = [
        f"http://{local_ip}:8000/",
        "http://127.0.0.1:8000/",
        "http://localhost:8000/"
    ]
    
    for url in test_urls:
        try:
            print(f"🔍 Testing: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ SUCCESS: {url} - Status: {response.status_code}")
            else:
                print(f"⚠️  WARNING: {url} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: {url} - {e}")
    
    print("\n📱 For Players:")
    print(f"🌐 Primary URL: http://{local_ip}:8000/")
    print("💡 If the primary URL fails, try:")
    print("   • http://127.0.0.1:8000/")
    print("   • http://localhost:8000/")
    
    print("\n🎯 Test Results:")
    print("• ✅ = Server accessible")
    print("• ⚠️  = Server responding but with issues")
    print("• ❌ = Server not accessible")

if __name__ == "__main__":
    test_server() 