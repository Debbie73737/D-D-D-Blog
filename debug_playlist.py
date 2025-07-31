#!/usr/bin/env python
"""
Debug script to check playlist tracks in the database
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from dnd_blog.models import Playlist, Category

def debug_playlist():
    """Debug the playlist system"""
    
    print("🔍 Debugging Playlist System...")
    print("=" * 50)
    
    # Check if Playlist model exists
    try:
        tracks = Playlist.objects.all()
        print(f"✅ Found {tracks.count()} playlist tracks in database")
        
        if tracks.count() > 0:
            print("\n📋 Playlist Tracks:")
            for track in tracks:
                status = "🟢 ACTIVE" if track.is_active else "⚪ INACTIVE"
                print(f"   {status} - {track.title}")
                print(f"      Artist: {track.artist}")
                print(f"      File: {track.file_name}")
                print()
        else:
            print("❌ No playlist tracks found in database")
            
    except Exception as e:
        print(f"❌ Error accessing Playlist model: {e}")
    
    # Check if Playlist category exists
    try:
        playlist_category = Category.objects.filter(name="Playlist").first()
        if playlist_category:
            print(f"✅ Playlist category exists (ID: {playlist_category.id})")
            print(f"   Admin only: {playlist_category.admin_only}")
        else:
            print("❌ Playlist category not found")
    except Exception as e:
        print(f"❌ Error accessing Category model: {e}")
    
    # Check all categories
    try:
        categories = Category.objects.all()
        print(f"\n📂 All Categories ({categories.count()}):")
        for cat in categories:
            admin_only = " (Admin Only)" if cat.admin_only else ""
            print(f"   - {cat.name}{admin_only}")
    except Exception as e:
        print(f"❌ Error accessing categories: {e}")

if __name__ == '__main__':
    debug_playlist() 