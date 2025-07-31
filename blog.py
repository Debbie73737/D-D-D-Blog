import requests
import sys
from urllib.parse import urlparse
import os
import zipfile
import platform

def download_html(url, output_file=None):
    """
    Download HTML content from a given URL
    
    Args:
        url (str): The URL to download HTML from
        output_file (str, optional): File path to save the HTML. If None, saves to 'downloaded_page.html'
    
    Returns:
        str: The downloaded HTML content
    """
    try:
        # Send GET request to the URL
        print(f"Downloading HTML from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Get the HTML content
        html_content = response.text
        
        # Determine output filename
        if output_file is None:
            # Extract domain name from URL for default filename
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('.', '_')
            output_file = f"{domain}_downloaded.html"
        
        # Save HTML to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML downloaded successfully!")
        print(f"Content length: {len(html_content)} characters")
        print(f"Saved to: {output_file}")
        
        return html_content
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading HTML: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def download_sqlite():
    """
    Download SQLite for the current platform
    """
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # SQLite download URLs for different platforms
    sqlite_urls = {
        'windows': {
            'x86_64': 'https://www.sqlite.org/2024/sqlite-tools-win32-x86-3450100.zip',
            'amd64': 'https://www.sqlite.org/2024/sqlite-tools-win32-x86-3450100.zip',
            'i386': 'https://www.sqlite.org/2024/sqlite-tools-win32-x86-3450100.zip'
        },
        'linux': {
            'x86_64': 'https://www.sqlite.org/2024/sqlite-tools-linux-x86-3450100.zip',
            'amd64': 'https://www.sqlite.org/2024/sqlite-tools-linux-x86-3450100.zip'
        },
        'darwin': {
            'x86_64': 'https://www.sqlite.org/2024/sqlite-tools-osx-x86-3450100.zip',
            'arm64': 'https://www.sqlite.org/2024/sqlite-tools-osx-x86-3450100.zip'
        }
    }
    
    try:
        # Determine the appropriate URL for the current platform
        if system in sqlite_urls:
            if machine in sqlite_urls[system]:
                url = sqlite_urls[system][machine]
            else:
                # Fallback to x86_64 for most cases
                url = sqlite_urls[system]['x86_64']
        else:
            print(f"Unsupported platform: {system} {machine}")
            print("Please download SQLite manually from: https://www.sqlite.org/download.html")
            return False
        
        print(f"Downloading SQLite for {system} {machine}...")
        print(f"URL: {url}")
        
        # Download the SQLite tools
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the zip file
        zip_filename = f"sqlite-tools-{system}-{machine}.zip"
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        
        print(f"SQLite downloaded successfully!")
        print(f"File size: {len(response.content)} bytes")
        print(f"Saved as: {zip_filename}")
        
        # Extract the zip file
        print("Extracting SQLite tools...")
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        print("SQLite tools extracted successfully!")
        
        # List extracted files
        extracted_dir = None
        for item in os.listdir('.'):
            if item.startswith('sqlite-tools-') and os.path.isdir(item):
                extracted_dir = item
                break
        
        if extracted_dir:
            print(f"SQLite tools directory: {extracted_dir}")
            print("Available tools:")
            for file in os.listdir(extracted_dir):
                if file.endswith('.exe') or file.endswith(''):
                    print(f"  - {file}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading SQLite: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def create_sample_database():
    """
    Create a sample SQLite database to test the installation
    """
    try:
        import sqlite3
        
        # Create a sample database
        db_name = "sample.db"
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create a sample table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data
        cursor.execute('''
            INSERT INTO users (name, email) VALUES 
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com'),
            ('Bob Johnson', 'bob@example.com')
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"Sample database created: {db_name}")
        print("You can test SQLite with: sqlite3 sample.db")
        
    except ImportError:
        print("SQLite3 module not available. Please install Python with SQLite support.")
    except Exception as e:
        print(f"Error creating sample database: {e}")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python blog.py html <URL> [output_file]  - Download HTML")
        print("  python blog.py sqlite                     - Download SQLite")
        print("  python blog.py sample-db                  - Create sample database")
        print("\nExamples:")
        print("  python blog.py html https://example.com")
        print("  python blog.py html https://example.com my_page.html")
        print("  python blog.py sqlite")
        print("  python blog.py sample-db")
        return
    
    command = sys.argv[1].lower()
    
    if command == "html":
        if len(sys.argv) < 3:
            print("Error: URL required for HTML download")
            print("Usage: python blog.py html <URL> [output_file]")
            return
        
        url = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        # Download the HTML
        html_content = download_html(url, output_file)
        
        if html_content:
            print("\nFirst 500 characters of downloaded HTML:")
            print("-" * 50)
            print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
    
    elif command == "sqlite":
        success = download_sqlite()
        if success:
            print("\nSQLite installation completed!")
            print("You can now use SQLite in your Python projects.")
    
    elif command == "sample-db":
        create_sample_database()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: html, sqlite, sample-db")

if __name__ == "__main__":
    main()
