from pyngrok import ngrok

try:
    tunnels = ngrok.get_tunnels()
    if tunnels:
        print("🌐 Active Public URLs:")
        for tunnel in tunnels:
            print(f"  📱 {tunnel.public_url}")
            print(f"     → {tunnel.config['addr']}")
    else:
        print("❌ No active tunnels found")
        print("💡 Run 'python start_public_server.py' to create a public URL")
except Exception as e:
    print(f"❌ Error checking tunnels: {e}") 