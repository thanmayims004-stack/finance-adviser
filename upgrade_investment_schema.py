#!/usr/bin/env python3
"""
Upgrade database schema to professional Investment Advisor structure
- Keep existing transactions table but add type column
- Create new goals table
- Create new risk_profile table
- Add sample data for professional investment tracking
"""

import sqlite3
import os
from datetime import datetime, timedelta

# Your database path
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def upgrade_investment_schema():
    try:
        print(f"🔌 Connecting to database: {DB_PATH}")
        
        # Connect to your existing database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Upgrade transactions table - add type column
        print("📋 Upgrading transactions table...")
        try:
            cursor.execute('ALTER TABLE transactions ADD COLUMN type VARCHAR(20) DEFAULT "Expense"')
            print("✅ Added type column to transactions table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ Type column already exists in transactions table")
            else:
                print(f"⚠️  Warning: {e}")
        
        # Update existing transactions to have appropriate types
        print("🏷️  Categorizing existing transactions...")
        cursor.execute('''
        UPDATE transactions 
        SET type = CASE 
            WHEN amount > 0 THEN 'Investment'
            WHEN category IN ('Food', 'Transport', 'Entertainment', 'Bills') THEN 'Expense'
            WHEN category LIKE '%Dividend%' OR description LIKE '%dividend%' THEN 'Dividend'
            ELSE 'Expense'
        END
        WHERE type IS NULL OR type = 'Expense'
        ''')
        
        # Add some investment and dividend transactions
        sample_investment_transactions = [
            ('2024-05-01', 'Stock Purchase - AAPL', -1000.00, 'Investment', 'Investment'),
            ('2024-05-02', 'Dividend from MSFT', 50.00, 'Investment', 'Dividend'),
            ('2024-05-03', 'Bond Purchase', -2000.00, 'Investment', 'Investment'),
            ('2024-05-04', 'Mutual Fund Dividend', 75.00, 'Investment', 'Dividend'),
            ('2024-05-05', 'ETF Purchase', -500.00, 'Investment', 'Investment')
        ]
        
        cursor.executemany('INSERT INTO transactions (txn_date, description, amount, category, type) VALUES (?, ?, ?, ?, ?)', sample_investment_transactions)
        
        # 2. Create goals table
        print("🎯 Creating goals table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name VARCHAR(255) NOT NULL,
            target_amount DECIMAL(12,2) NOT NULL,
            current_saved DECIMAL(12,2) DEFAULT 0.00,
            deadline DATE NOT NULL,
            goal_category VARCHAR(50) DEFAULT 'General',
            priority VARCHAR(20) DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Add sample goals
        sample_goals = [
            ('Retirement Fund', 1000000.00, 50000.00, '2045-12-31', 'Retirement', 'High'),
            ('Emergency Fund', 50000.00, 35000.00, '2024-12-31', 'Emergency', 'High'),
            ('House Down Payment', 200000.00, 25000.00, '2026-06-30', 'Housing', 'Medium'),
            ('Children Education', 150000.00, 10000.00, '2035-08-15', 'Education', 'Medium'),
            ('Vacation Fund', 15000.00, 2000.00, '2025-07-01', 'Lifestyle', 'Low'),
            ('New Car', 40000.00, 8000.00, '2025-03-31', 'Transport', 'Medium')
        ]
        
        cursor.executemany('INSERT INTO goals (goal_name, target_amount, current_saved, deadline, goal_category, priority) VALUES (?, ?, ?, ?, ?, ?)', sample_goals)
        
        # 3. Create risk_profile table
        print("⚖️  Creating risk_profile table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investor_name VARCHAR(255),
            age INTEGER,
            risk_tolerance VARCHAR(20) NOT NULL CHECK (risk_tolerance IN ('Aggressive', 'Conservative', 'Balanced')),
            investment_horizon INTEGER, -- in years
            annual_income DECIMAL(12,2),
            dependents INTEGER DEFAULT 0,
            investment_experience VARCHAR(20) DEFAULT 'Beginner',
            financial_knowledge VARCHAR(20) DEFAULT 'Basic',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Add sample risk profile
        sample_risk_profile = {
            'investor_name': 'John Doe',
            'age': 35,
            'risk_tolerance': 'Balanced',
            'investment_horizon': 25,
            'annual_income': 85000.00,
            'dependents': 2,
            'investment_experience': 'Intermediate',
            'financial_knowledge': 'Good'
        }
        
        cursor.execute('''
        INSERT INTO risk_profile (investor_name, age, risk_tolerance, investment_horizon, annual_income, dependents, investment_experience, financial_knowledge) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sample_risk_profile['investor_name'],
            sample_risk_profile['age'],
            sample_risk_profile['risk_tolerance'],
            sample_risk_profile['investment_horizon'],
            sample_risk_profile['annual_income'],
            sample_risk_profile['dependents'],
            sample_risk_profile['investment_experience'],
            sample_risk_profile['financial_knowledge']
        ))
        
        conn.commit()
        
        # Verify and display results
        print("\n✅ Schema upgrade completed successfully!")
        
        # Show transactions summary
        cursor.execute('SELECT type, COUNT(*) as count, SUM(amount) as total FROM transactions GROUP BY type')
        transactions_summary = cursor.fetchall()
        print(f"\n📊 Transactions Summary:")
        for row in transactions_summary:
            print(f"   {row[0]}: {row[1]} transactions, Total: ${row[2]:,.2f}")
        
        # Show goals progress
        cursor.execute('SELECT goal_name, target_amount, current_saved, deadline, priority FROM goals ORDER BY deadline')
        goals = cursor.fetchall()
        print(f"\n🎯 Financial Goals:")
        for goal in goals:
            progress = (goal[2] / goal[1]) * 100 if goal[1] > 0 else 0
            print(f"   {goal[0]}: ${goal[2]:,.2f} / ${goal[1]:,.2f} ({progress:.1f}%) - Due: {goal[3]} [{goal[4]}]")
        
        # Show risk profile
        cursor.execute('SELECT * FROM risk_profile ORDER BY created_at DESC LIMIT 1')
        profile = cursor.fetchone()
        if profile:
            print(f"\n⚖️  Risk Profile:")
            print(f"   Investor: {profile[1]}")
            print(f"   Age: {profile[2]}")
            print(f"   Risk Tolerance: {profile[3]}")
            print(f"   Investment Horizon: {profile[4]} years")
            print(f"   Annual Income: ${profile[5]:,.2f}")
            print(f"   Dependents: {profile[6]}")
            print(f"   Experience: {profile[7]}")
            print(f"   Knowledge: {profile[8]}")
        
        # Investment recommendations based on risk profile
        if profile and profile[3] == 'Aggressive':
            allocation = "80% Stocks, 15% Bonds, 5% Cash"
        elif profile and profile[3] == 'Conservative':
            allocation = "40% Stocks, 50% Bonds, 10% Cash"
        else:
            allocation = "60% Stocks, 35% Bonds, 5% Cash"
        
        print(f"\n💡 Recommended Asset Allocation: {allocation}")
        
        conn.close()
        print(f"\n🎉 Your Investment Advisor database is now ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    upgrade_investment_schema()
