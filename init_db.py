#!/usr/bin/env python3
"""
Script to create thanmayi.db with transactions table
Run this script to initialize the database
"""

import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'thanthayi.db')

def create_database():
    try:
        # Connect to database (will create if doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_date DATE,
            description VARCHAR(255),
            amount DECIMAL(10,2),
            category VARCHAR(50)
        )
        ''')
        
        # Add sample data
        sample_data = [
            ('2024-05-01', 'Grocery Store', -50.25, 'Food'),
            ('2024-05-02', 'Salary Credit', 3000.00, 'Income'),
            ('2024-05-03', 'Netflix', -15.99, 'Subscription'),
            ('2024-05-04', 'Gas Station', -45.00, 'Transport'),
            ('2024-05-05', 'Restaurant', -75.50, 'Food'),
            ('2024-05-06', 'Electric Bill', -120.00, 'Bills'),
            ('2024-05-07', 'Amazon Purchase', -89.99, 'Shopping'),
            ('2024-05-08', 'Coffee Shop', -12.50, 'Food'),
            ('2024-05-09', 'Uber', -25.00, 'Transport'),
            ('2024-05-10', 'Gym Membership', -30.00, 'Health'),
            ('2024-05-11', 'Grocery Shopping', -85.75, 'Food'),
            ('2024-05-12', 'Freelance Payment', 500.00, 'Income'),
            ('2024-05-13', 'Phone Bill', -45.00, 'Bills'),
            ('2024-05-14', 'Movie Tickets', -30.00, 'Entertainment'),
            ('2024-05-15', 'Lunch', -18.50, 'Food')
        ]
        
        cursor.executemany('INSERT INTO transactions (txn_date, description, amount, category) VALUES (?, ?, ?, ?)', sample_data)
        
        conn.commit()
        
        # Verify data
        cursor.execute('SELECT COUNT(*) FROM transactions')
        count = cursor.fetchone()[0]
        
        print(f'✅ Created thanmayi.db successfully!')
        print(f'📊 Inserted {count} sample transactions')
        print(f'📍 Database location: {db_path}')
        
        # Show sample data
        cursor.execute('SELECT * FROM transactions LIMIT 5')
        print('📝 Sample data:')
        for row in cursor.fetchall():
            print(f'   ID: {row[0]}, Date: {row[1]}, Desc: {row[2]}, Amount: ${row[3]}, Category: {row[4]}')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Error creating database: {e}')
        return False

if __name__ == "__main__":
    create_database()
