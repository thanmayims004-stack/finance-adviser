#!/usr/bin/env python3
"""
Create investments table with specific columns as requested
"""

import sqlite3
import os

# Your database path
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def create_investments_table():
    try:
        print(f"🔌 Connecting to database: {DB_PATH}")
        
        # Connect to your existing database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create investments table with requested columns
        print("📋 Creating investments table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_name VARCHAR(255),
            category VARCHAR(50),  -- Equity/Debt
            current_value DECIMAL(10,2),
            purchase_price DECIMAL(10,2)
        )
        ''')
        
        # Add sample investment data
        print("💰 Adding sample investment data...")
        sample_investments = [
            ('Apple Inc. (AAPL)', 'Equity', 1500.00, 1200.00),
            ('US Treasury Bonds', 'Debt', 5000.00, 4800.00),
            ('S&P 500 Index Fund', 'Equity', 2500.00, 2200.00),
            ('Corporate Bonds', 'Debt', 3000.00, 2900.00),
            ('Microsoft Corp. (MSFT)', 'Equity', 1800.00, 1600.00),
            ('Municipal Bonds', 'Debt', 2000.00, 1950.00),
            ('Tesla Inc. (TSLA)', 'Equity', 800.00, 1000.00),
            ('Government Securities', 'Debt', 4000.00, 3900.00)
        ]
        
        cursor.executemany('INSERT INTO investments (asset_name, category, current_value, purchase_price) VALUES (?, ?, ?, ?)', sample_investments)
        
        conn.commit()
        
        # Verify data
        cursor.execute('SELECT COUNT(*) FROM investments')
        count = cursor.fetchone()[0]
        
        print(f"✅ Investments table created successfully!")
        print(f"📊 Inserted {count} investment records")
        
        # Show sample data
        cursor.execute('SELECT * FROM investments LIMIT 5')
        print("📝 Sample investments:")
        for row in cursor.fetchall():
            gain_loss = row[3] - row[4]
            gain_percent = (gain_loss / row[4]) * 100 if row[4] > 0 else 0
            print(f"   {row[1]} ({row[2]}): ${row[3]:.2f} | Purchased: ${row[4]:.2f} | Gain/Loss: ${gain_loss:+.2f} ({gain_percent:+.1f}%)")
        
        # Calculate totals
        cursor.execute('SELECT category, SUM(current_value) as total_value, SUM(purchase_price) as total_cost FROM investments GROUP BY category')
        print(f"\n💼 Portfolio Summary by Category:")
        for row in cursor.fetchall():
            gain_loss = row[1] - row[2]
            gain_percent = (gain_loss / row[2]) * 100 if row[2] > 0 else 0
            print(f"   {row[0]}: ${row[1]:.2f} | Cost: ${row[2]:.2f} | Gain/Loss: ${gain_loss:+.2f} ({gain_percent:+.1f}%)")
        
        cursor.execute('SELECT SUM(current_value) as total_value, SUM(purchase_price) as total_cost FROM investments')
        totals = cursor.fetchone()
        total_gain = totals[0] - totals[1]
        total_gain_percent = (total_gain / totals[1]) * 100 if totals[1] > 0 else 0
        print(f"\n📈 Total Portfolio: ${totals[0]:.2f} | Total Cost: ${totals[1]:.2f}")
        print(f"🎯 Total Gain/Loss: ${total_gain:+.2f} ({total_gain_percent:+.1f}%)")
        
        conn.close()
        print(f"\n🎉 Your investments table is ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_investments_table()
