#!/usr/bin/env python3
"""
Update database for RIA (Registered Investment Advisor) features
- Add investments tracking
- Add risk profiling
- Add financial goals tracking
"""

import sqlite3
import os

# Your database path
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def update_ria_database():
    try:
        print(f"🔌 Connecting to database: {DB_PATH}")
        
        # Connect to your existing database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create investments table
        print("📋 Creating investments table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investment_type VARCHAR(50),  -- Stocks, Mutual Funds, Gold, Cash
            amount DECIMAL(10,2),
            purchase_date DATE,
            current_value DECIMAL(10,2),
            description TEXT
        )
        ''')
        
        # Create risk_profile table
        print("📋 Creating risk_profile table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            risk_tolerance VARCHAR(20),  -- Low, Medium, High
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create financial_goals table
        print("📋 Creating financial_goals table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name VARCHAR(100),  -- Retirement, Emergency Fund, etc.
            target_amount DECIMAL(10,2),
            current_amount DECIMAL(10,2),
            target_date DATE,
            goal_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Add sample investment data
        print("💰 Adding sample investment data...")
        sample_investments = [
            ('Stocks', 1000.00, '2024-01-15', 1100.00, 'Tech stocks portfolio'),
            ('Mutual Funds', 800.00, '2024-02-01', 850.00, 'Index fund investment'),
            ('Gold', 500.00, '2024-01-20', 520.00, 'Gold ETF'),
            ('Cash', 700.00, '2024-03-01', 700.00, 'Emergency fund cash')
        ]
        
        cursor.executemany('INSERT INTO investments (investment_type, amount, purchase_date, current_value, description) VALUES (?, ?, ?, ?, ?)', sample_investments)
        
        # Add sample risk profile
        print("🎯 Adding sample risk profile...")
        cursor.execute('INSERT INTO risk_profile (age, risk_tolerance) VALUES (?, ?)', (30, 'Medium'))
        
        # Add sample financial goals
        print("🎯 Adding sample financial goals...")
        sample_goals = [
            ('Retirement Fund', 100000.00, 5000.00, '2045-01-01', 'Long-term'),
            ('Emergency Fund', 10000.00, 7000.00, '2024-12-31', 'Short-term'),
            ('House Down Payment', 50000.00, 8000.00, '2026-06-01', 'Medium-term')
        ]
        
        cursor.executemany('INSERT INTO financial_goals (goal_name, target_amount, current_amount, target_date, goal_type) VALUES (?, ?, ?, ?, ?)', sample_goals)
        
        conn.commit()
        
        # Verify data
        cursor.execute('SELECT COUNT(*) FROM investments')
        investment_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM risk_profile')
        risk_profile_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM financial_goals')
        goals_count = cursor.fetchone()[0]
        
        print(f"✅ RIA Database update complete!")
        print(f"📊 Investments: {investment_count} records")
        print(f"🎯 Risk Profiles: {risk_profile_count} records")
        print(f"🎯 Financial Goals: {goals_count} records")
        
        # Show sample data
        print("\n💰 Sample Investments:")
        cursor.execute('SELECT * FROM investments LIMIT 2')
        for row in cursor.fetchall():
            print(f"   {row[1]}: ${row[2]} → ${row[4]}")
        
        print("\n🎯 Sample Risk Profile:")
        cursor.execute('SELECT * FROM risk_profile LIMIT 1')
        row = cursor.fetchone()
        if row:
            print(f"   Age: {row[1]}, Risk Tolerance: {row[2]}")
        
        print("\n🎯 Sample Financial Goals:")
        cursor.execute('SELECT * FROM financial_goals LIMIT 2')
        for row in cursor.fetchall():
            progress = (row[3] / row[2]) * 100 if row[2] > 0 else 0
            print(f"   {row[1]}: ${row[3]}/${row[2]} ({progress:.1f}%)")
        
        conn.close()
        print(f"\n🎉 Your RIA tool is now ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_ria_database()
