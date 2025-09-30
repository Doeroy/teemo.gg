#!/usr/bin/env python3
"""
Test script to diagnose MySQL connection issues
"""
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL connection with detailed error reporting"""
    print("=== MySQL Connection Test ===")
    
    # Get connection details
    host = os.getenv('DB_HOST')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    
    print(f"Attempting to connect to:")
    print(f"Host: {host}")
    print(f"Username: {username}")
    print(f"Database: {database}")
    print(f"Password: {'*' * len(password) if password else 'None'}")
    print()
    
    try:
        # Attempt connection
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Successfully connected to MySQL Server version {db_info}")
            
            # Test a simple query
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"✅ You're connected to database: {database_name[0]}")
            
            cursor.close()
            connection.close()
            print("✅ MySQL connection test passed!")
            return True
            
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        
        # Provide specific solutions based on error type
        error_msg = str(e).lower()
        
        if "host" in error_msg and "not allowed" in error_msg:
            print("\n🔧 SOLUTION: Host not allowed error")
            print("Your MySQL server is rejecting connections from your IP address.")
            print("Try one of these solutions:")
            print("1. If using MySQL locally:")
            print("   - Log into MySQL as root: mysql -u root -p")
            print("   - Run: CREATE USER 'your_username'@'%' IDENTIFIED BY 'your_password';")
            print("   - Run: GRANT ALL PRIVILEGES ON your_database.* TO 'your_username'@'%';")
            print("   - Run: FLUSH PRIVILEGES;")
            print()
            print("2. If using cloud MySQL (AWS RDS, etc.):")
            print("   - Check your security groups/firewall rules")
            print("   - Allow connections from your current IP address")
            print("   - Or use 0.0.0.0/0 for testing (not recommended for production)")
            
        elif "access denied" in error_msg:
            print("\n🔧 SOLUTION: Wrong username/password")
            print("Check your .env file credentials")
            
        elif "unknown database" in error_msg:
            print("\n🔧 SOLUTION: Database doesn't exist")
            print("Create the database first or check the DB_NAME in your .env file")
            
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()
