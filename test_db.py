import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing Database Connection...")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"Port: {os.getenv('DB_PORT')}")
print(f"Database: {os.getenv('DB_NAME')}")
print(f"User: {os.getenv('DB_USER')}")

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        
        # Check if transactions table exists
        cursor.execute("SHOW TABLES LIKE 'transactions'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Transactions table exists")
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            print(f"📊 Found {count} transactions")
            
            # Show sample data
            cursor.execute("SELECT * FROM transactions LIMIT 3")
            records = cursor.fetchall()
            print("📝 Sample data:")
            for record in records:
                print(f"   {record}")
        else:
            print("❌ Transactions table not found")
            print("Please run your SQL script to create the table and insert data")
        
        cursor.close()
        connection.close()
        
except Error as e:
    print(f"❌ Database Error: {e}")
    print("\n💡 Solutions:")
    print("1. Check if MySQL is running")
    print("2. Verify username and password")
    print("3. Make sure the database 'finance_expert' exists")
    print("4. Check if the user has permissions for this database")
