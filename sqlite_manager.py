import sqlite3
import os
import sys
from datetime import datetime

class SQLiteManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            print("Disconnected from database")
    
    def create_table(self, table_name, columns):
        """
        Create a table with specified columns
        
        Args:
            table_name (str): Name of the table
            columns (list): List of column definitions
        """
        try:
            columns_str = ", ".join(columns)
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
    
    def insert_data(self, table_name, data):
        """
        Insert data into a table
        
        Args:
            table_name (str): Name of the table
            data (dict): Dictionary of column_name: value pairs
        """
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ", ".join(["?" for _ in values])
            columns_str = ", ".join(columns)
            
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Data inserted into '{table_name}' successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")
    
    def query_data(self, query, params=None):
        """
        Execute a query and return results
        
        Args:
            query (str): SQL query
            params (tuple, optional): Query parameters
        
        Returns:
            list: Query results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
    
    def show_tables(self):
        """Show all tables in the database"""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.cursor.fetchall()
            if tables:
                print("Tables in database:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("No tables found in database")
        except Exception as e:
            print(f"Error showing tables: {e}")
    
    def describe_table(self, table_name):
        """Show table structure"""
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            if columns:
                print(f"Table structure for '{table_name}':")
                print("Column Name | Type | Not Null | Primary Key | Default")
                print("-" * 60)
                for col in columns:
                    print(f"{col[1]:<12} | {col[2]:<8} | {col[3]:<8} | {col[5]:<12} | {col[4]}")
            else:
                print(f"Table '{table_name}' not found")
        except Exception as e:
            print(f"Error describing table: {e}")

def create_sample_database():
    """Create a sample database with multiple tables"""
    manager = SQLiteManager("sample_complete.db")
    
    if not manager.connect():
        return
    
    # Create users table
    users_columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "username TEXT UNIQUE NOT NULL",
        "email TEXT UNIQUE NOT NULL",
        "full_name TEXT",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ]
    manager.create_table("users", users_columns)
    
    # Create posts table
    posts_columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id INTEGER",
        "title TEXT NOT NULL",
        "content TEXT",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (user_id) REFERENCES users (id)"
    ]
    manager.create_table("posts", posts_columns)
    
    # Insert sample users
    users_data = [
        {"username": "john_doe", "email": "john@example.com", "full_name": "John Doe"},
        {"username": "jane_smith", "email": "jane@example.com", "full_name": "Jane Smith"},
        {"username": "bob_wilson", "email": "bob@example.com", "full_name": "Bob Wilson"}
    ]
    
    for user in users_data:
        manager.insert_data("users", user)
    
    # Insert sample posts
    posts_data = [
        {"user_id": 1, "title": "My First Post", "content": "This is my first blog post!"},
        {"user_id": 1, "title": "Learning SQLite", "content": "SQLite is a great database for small projects."},
        {"user_id": 2, "title": "Hello World", "content": "Hello from Jane!"},
        {"user_id": 3, "title": "Database Design", "content": "Good database design is crucial for any application."}
    ]
    
    for post in posts_data:
        manager.insert_data("posts", post)
    
    # Show tables
    manager.show_tables()
    
    # Show sample data
    print("\nSample Users:")
    users = manager.query_data("SELECT * FROM users")
    for user in users:
        print(f"  {user}")
    
    print("\nSample Posts:")
    posts = manager.query_data("SELECT * FROM posts")
    for post in posts:
        print(f"  {post}")
    
    manager.disconnect()
    print(f"\nSample database created: sample_complete.db")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("SQLite Manager - Database Management Tool")
        print("\nUsage:")
        print("  python sqlite_manager.py sample     - Create sample database")
        print("  python sqlite_manager.py interactive - Start interactive mode")
        print("  python sqlite_manager.py test       - Test SQLite functionality")
        return
    
    command = sys.argv[1].lower()
    
    if command == "sample":
        create_sample_database()
    
    elif command == "test":
        # Test SQLite functionality
        print("Testing SQLite functionality...")
        manager = SQLiteManager("test.db")
        
        if manager.connect():
            # Create a test table
            manager.create_table("test_table", [
                "id INTEGER PRIMARY KEY",
                "name TEXT",
                "value INTEGER"
            ])
            
            # Insert test data
            manager.insert_data("test_table", {"id": 1, "name": "Test Item", "value": 100})
            
            # Query test data
            results = manager.query_data("SELECT * FROM test_table")
            print(f"Test query results: {results}")
            
            manager.disconnect()
            os.remove("test.db")  # Clean up
            print("SQLite test completed successfully!")
    
    elif command == "interactive":
        print("SQLite Interactive Mode")
        print("Type 'help' for commands, 'exit' to quit")
        
        db_name = input("Enter database name (or press Enter for 'interactive.db'): ").strip()
        if not db_name:
            db_name = "interactive.db"
        
        manager = SQLiteManager(db_name)
        if not manager.connect():
            return
        
        while True:
            try:
                command = input(f"\n[{db_name}]> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'help':
                    print("Available commands:")
                    print("  tables                    - Show all tables")
                    print("  describe <table_name>     - Show table structure")
                    print("  query <sql_query>         - Execute SQL query")
                    print("  exit/quit                 - Exit interactive mode")
                elif command.lower() == 'tables':
                    manager.show_tables()
                elif command.startswith('describe '):
                    table_name = command.split(' ', 1)[1]
                    manager.describe_table(table_name)
                elif command.startswith('query '):
                    sql_query = command.split(' ', 1)[1]
                    results = manager.query_data(sql_query)
                    if results:
                        print("Results:")
                        for row in results:
                            print(f"  {row}")
                    else:
                        print("No results")
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        manager.disconnect()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: sample, test, interactive")

if __name__ == "__main__":
    main() 