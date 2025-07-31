#!/usr/bin/env python
"""
Script to copy music files from Downloads to the static audio directory
"""
import os
import shutil
from pathlib import Path

def copy_music_files():
    """Copy music files from Downloads to static audio directory"""
    
    # Source directory (Downloads)
    downloads_dir = Path(r"C:\Users\oit-student\Downloads")
    
    # Destination directory
    audio_dir = Path("dnd_blog/static/dnd_blog/audio")
    
    # Create audio directory if it doesn't exist
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the files to copy with their new names
    files_to_copy = {
        "Bloody Stream but is it okay if it's lofi_.mp3": "bloody-stream-lofi.mp3",
        "gurenge (Demon Slayer but is it okay if it's lofi hiphop_).mp3": "gurenge-demon-slayer-lofi.mp3",
        "blue bird (Naruto but is it okay if it's lofi hiphop_).mp3": "blue-bird-naruto-lofi.mp3",
        "isabella's lullaby (The Promised Neverland lofi).mp3": "isabellas-lullaby.mp3"
    }
    
    print("🎵 Copying music files...")
    
    for source_name, dest_name in files_to_copy.items():
        source_path = downloads_dir / source_name
        dest_path = audio_dir / dest_name
        
        if source_path.exists():
            try:
                shutil.copy2(source_path, dest_path)
                print(f"✅ Copied: {source_name} → {dest_name}")
            except Exception as e:
                print(f"❌ Error copying {source_name}: {e}")
        else:
            print(f"⚠️  File not found: {source_name}")
    
    print(f"\n📁 Files copied to: {audio_dir.absolute()}")
    print("📋 Files in audio directory:")
    for file in audio_dir.glob("*.mp3"):
        print(f"   - {file.name}")

if __name__ == '__main__':
    copy_music_files() 