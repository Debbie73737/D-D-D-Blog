#!/usr/bin/env python
"""
Script to set up the playlist with the new music files
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

def setup_playlist():
    """Set up the playlist with the new music files"""
    
    # Create the "Playlist" category (admin-only)
    playlist_category, created = Category.objects.get_or_create(
        name="Playlist",
        defaults={
            'description': "Admin-only category for background music management",
            'admin_only': True
        }
    )
    
    if created:
        print(f"✅ Created admin-only 'Playlist' category")
    else:
        print(f"ℹ️  'Playlist' category already exists")
    
    # Define the tracks
    tracks = [
        {
            'title': "Isabella's Lullaby (The Promised Neverland Lofi)",
            'artist': "The Promised Neverland",
            'file_name': "isabellas-lullaby.mp3",
            'is_active': True  # This will be the default active track
        },
        {
            'title': "Bloody Stream (JoJo's Bizarre Adventure Lofi)",
            'artist': "JoJo's Bizarre Adventure",
            'file_name': "bloody-stream-lofi.mp3",
            'is_active': False
        },
        {
            'title': "Gurenge (Demon Slayer Lofi Hiphop)",
            'artist': "Demon Slayer",
            'file_name': "gurenge-demon-slayer-lofi.mp3",
            'is_active': False
        },
        {
            'title': "Blue Bird (Naruto Lofi Hiphop)",
            'artist': "Naruto",
            'file_name': "blue-bird-naruto-lofi.mp3",
            'is_active': False
        }
    ]
    
    # Create playlist entries
    for track_data in tracks:
        track, created = Playlist.objects.get_or_create(
            title=track_data['title'],
            defaults={
                'artist': track_data['artist'],
                'file_name': track_data['file_name'],
                'is_active': track_data['is_active']
            }
        )
        
        if created:
            print(f"✅ Created playlist track: {track.title}")
        else:
            print(f"ℹ️  Playlist track already exists: {track.title}")
    
    # Ensure only one track is active
    active_tracks = Playlist.objects.filter(is_active=True)
    if active_tracks.count() > 1:
        # Keep only the first one active
        first_active = active_tracks.first()
        active_tracks.exclude(id=first_active.id).update(is_active=False)
        print(f"⚠️  Multiple active tracks found. Keeping only '{first_active.title}' active.")
    
    print("\n🎵 Playlist setup complete!")
    print("📁 Please ensure the following files are in PyCharmMiscProject/dnd_blog/static/dnd_blog/audio/:")
    for track in Playlist.objects.all():
        print(f"   - {track.file_name}")
    
    active_track = Playlist.objects.filter(is_active=True).first()
    if active_track:
        print(f"\n🎶 Currently active track: {active_track.title}")
    else:
        print("\n⚠️  No active track set. Please activate a track in the admin panel.")

if __name__ == '__main__':
    setup_playlist() 