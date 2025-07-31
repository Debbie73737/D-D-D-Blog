#!/usr/bin/env python
"""
Setup script for D&D&D blog
Creates initial categories and superuser
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from dnd_blog.models import Category

def create_categories():
    """Create the three main categories for D&D&D"""
    categories = [
        {
            'name': 'World Building',
            'description': 'Share your campaign worlds, maps, lore, and creative world-building ideas.'
        },
        {
            'name': 'Character Design',
            'description': 'Discuss character concepts, backstories, builds, and character development.'
        },
        {
            'name': 'Community Feedback',
            'description': 'Get feedback on your ideas, share experiences, and help other D&D enthusiasts.'
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✓ Created category: {category.name}")
        else:
            print(f"✓ Category already exists: {category.name}")
        created_categories.append(category)
    
    return created_categories

def create_superuser():
    """Create a superuser if none exists"""
    if not User.objects.filter(is_superuser=True).exists():
        print("\nCreating superuser...")
        username = "admin"
        email = "admin@dndd.com"
        password = "admin123"
        
        user = User.objects.create_superuser(username, email, password)
        print(f"✓ Created superuser: {username}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        return user
    else:
        print("✓ Superuser already exists")
        return User.objects.filter(is_superuser=True).first()

def main():
    print("Setting up D&D&D Blog...")
    print("=" * 40)
    
    # Create categories
    print("\n1. Creating categories...")
    categories = create_categories()
    
    # Create superuser
    print("\n2. Setting up superuser...")
    superuser = create_superuser()
    
    print("\n" + "=" * 40)
    print("Setup complete!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    if superuser:
        print(f"3. Login to admin at: http://127.0.0.1:8000/admin/")
        print(f"   Username: {superuser.username}")
        print(f"   Password: admin123")
    
    print("\nCategories created:")
    for category in categories:
        print(f"  - {category.name}: {category.description}")

if __name__ == "__main__":
    main() 