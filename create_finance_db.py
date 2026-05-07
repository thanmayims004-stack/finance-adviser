import sqlite3
import os

# Create finance.db with transactions table
db_path = os.path.join(os.path.dirname(__file__), 'finance.db')

try:
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
        ('2024-05-10', 'Gym Membership', -30.00, 'Health')
    ]
    
    cursor.executemany('INSERT INTO transactions (txn_date, description, amount, category) VALUES (?, ?, ?, ?)', sample_data)
    
    conn.commit()
    
    # Verify data
    cursor.execute('SELECT COUNT(*) FROM transactions')
    count = cursor.fetchone()[0]
    
    print(f'✅ Created finance.db successfully!')
    print(f'📊 Inserted {count} sample transactions')
    print(f'📍 Database location: {db_path}')
    
    # Show sample data
    cursor.execute('SELECT * FROM transactions LIMIT 3')
    print('📝 Sample data:')
    for row in cursor.fetchall():
        print(f'   {row}')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
