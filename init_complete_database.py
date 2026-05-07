#!/usr/bin/env python3
"""
Complete Database Initialization for RIA Investment Advisor
Creates optimized schema with comprehensive sample data
"""

import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
import random

def create_connection():
    """Create database connection"""
    try:
        conn = sqlite3.connect('/Users/thanmayims/Documents/finance.db')
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def initialize_complete_database():
    """Initialize complete database with optimized schema and sample data"""
    conn = create_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Drop existing tables to start fresh
        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute("DROP TABLE IF EXISTS goals")
        cursor.execute("DROP TABLE IF EXISTS risk_profile")
        cursor.execute("DROP TABLE IF EXISTS investments")
        cursor.execute("DROP TABLE IF EXISTS portfolio")
        cursor.execute("DROP TABLE IF EXISTS financial_goals")
        
        # Create optimized transactions table
        cursor.execute("""
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                txn_date DATE NOT NULL,
                description VARCHAR(255) NOT NULL,
                amount DECIMAL(12,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                type VARCHAR(20) DEFAULT 'Expense',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create optimized goals table
        cursor.execute("""
            CREATE TABLE goals (
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
        """)
        
        # Create optimized risk_profile table
        cursor.execute("""
            CREATE TABLE risk_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER NOT NULL,
                risk_tolerance VARCHAR(20) NOT NULL,
                investment_horizon INTEGER,
                annual_income DECIMAL(12,2),
                dependents INTEGER DEFAULT 0,
                investment_experience VARCHAR(20) DEFAULT 'Beginner',
                financial_knowledge VARCHAR(20) DEFAULT 'Basic',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create investments table
        cursor.execute("""
            CREATE TABLE investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investment_type VARCHAR(50) NOT NULL,
                amount DECIMAL(12,2) NOT NULL,
                purchase_date DATE NOT NULL,
                current_value DECIMAL(12,2),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create portfolio table
        cursor.execute("""
            CREATE TABLE portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name VARCHAR(255) NOT NULL,
                category VARCHAR(50) NOT NULL,
                current_value DECIMAL(12,2) NOT NULL,
                purchase_price DECIMAL(12,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert comprehensive sample data
        
        # Sample transactions (realistic mix of income, expenses, investments)
        transactions = [
            # Income
            [(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 'Monthly Salary', 8500.00, 'Income', 'Investment'],
            [(datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'), 'Freelance Project', 2500.00, 'Income', 'Investment'],
            [(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), 'Dividend Payment', 450.00, 'Investment', 'Dividend'],
            
            # Investment transactions
            [(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), 'AAPL Stock Purchase', -2500.00, 'Investment', 'Investment'],
            [(datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'), 'Vanguard ETF', -3000.00, 'Investment', 'Investment'],
            [(datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'), 'Bond Purchase', -5000.00, 'Investment', 'Investment'],
            
            # Regular expenses
            [(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), 'Grocery Store', -125.50, 'Food', 'Expense'],
            [(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), 'Electric Bill', -180.00, 'Bills', 'Expense'],
            [(datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'), 'Internet Service', -60.00, 'Bills', 'Expense'],
            [(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'), 'Gas Station', -65.00, 'Transport', 'Expense'],
            [(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), 'Restaurant Dinner', -85.00, 'Food', 'Expense'],
            [(datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'), 'Netflix Subscription', -15.99, 'Subscription', 'Expense'],
            [(datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d'), 'Gym Membership', -45.00, 'Health', 'Expense'],
            [(datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'), 'Pharmacy', -35.00, 'Health', 'Expense'],
            [(datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d'), 'Clothing Store', -220.00, 'Shopping', 'Expense'],
            [(datetime.now() - timedelta(days=22)).strftime('%Y-%m-%d'), 'Movie Tickets', -30.00, 'Entertainment', 'Expense'],
            [(datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'), 'Coffee Shop', -12.50, 'Food', 'Expense'],
        ]
        
        for transaction in transactions:
            cursor.execute("""
                INSERT INTO transactions (txn_date, description, amount, category, type)
                VALUES (?, ?, ?, ?, ?)
            """, transaction)
        
        # Sample goals with realistic targets and progress
        goals = [
            ['Emergency Fund', 50000.00, 35000.00, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'), 'Emergency', 'High'],
            ['Retirement Fund', 1000000.00, 75000.00, (datetime.now() + timedelta(days=365*20)).strftime('%Y-%m-%d'), 'Retirement', 'High'],
            ['New Car', 45000.00, 9000.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'), 'Transport', 'Medium'],
            ['House Down Payment', 200000.00, 35000.00, (datetime.now() + timedelta(days=365*5)).strftime('%Y-%m-%d'), 'Housing', 'Medium'],
            ['Children Education', 150000.00, 15000.00, (datetime.now() + timedelta(days=365*10)).strftime('%Y-%m-%d'), 'Education', 'Medium'],
            ['Vacation Fund', 12000.00, 2000.00, (datetime.now() + timedelta(days=270)).strftime('%Y-%m-%d'), 'Lifestyle', 'Low'],
            ['Investment Portfolio', 100000.00, 25000.00, (datetime.now() + timedelta(days=365*3)).strftime('%Y-%m-%d'), 'Investment', 'High'],
        ]
        
        for goal in goals:
            cursor.execute("""
                INSERT INTO goals (goal_name, target_amount, current_saved, deadline, goal_category, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, goal)
        
        # Sample risk profile
        cursor.execute("""
            INSERT INTO risk_profile (age, risk_tolerance, investment_horizon, annual_income, dependents, investment_experience, financial_knowledge)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (35, 'Balanced', 25, 95000.00, 2, 'Intermediate', 'Good'))
        
        # Sample investments
        investments = [
            ['Stocks', 2500.00, (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), 2650.00, 'Apple Inc. (AAPL)'],
            ['ETF', 3000.00, (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'), 3150.00, 'Vanguard S&P 500 ETF'],
            ['Bonds', 5000.00, (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'), 5100.00, 'US Treasury Bonds'],
            ['Mutual Funds', 4000.00, (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'), 4200.00, 'Growth Mutual Fund'],
            ['Real Estate', 10000.00, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), 10500.00, 'REIT Investment'],
        ]
        
        for investment in investments:
            cursor.execute("""
                INSERT INTO investments (investment_type, amount, purchase_date, current_value, description)
                VALUES (?, ?, ?, ?, ?)
            """, investment)
        
        # Sample portfolio
        portfolio = [
            ['Apple Stock', 'Equity', 2650.00, 2500.00],
            ['Vanguard ETF', 'Equity', 3150.00, 3000.00],
            ['Treasury Bonds', 'Debt', 5100.00, 5000.00],
            ['Growth Fund', 'Equity', 4200.00, 4000.00],
            ['REIT Investment', 'Real Estate', 10500.00, 10000.00],
            ['Cash Reserve', 'Cash', 8000.00, 8000.00],
        ]
        
        for asset in portfolio:
            cursor.execute("""
                INSERT INTO portfolio (asset_name, category, current_value, purchase_price)
                VALUES (?, ?, ?, ?)
            """, asset)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_transactions_date ON transactions(txn_date)")
        cursor.execute("CREATE INDEX idx_transactions_category ON transactions(category)")
        cursor.execute("CREATE INDEX idx_goals_deadline ON goals(deadline)")
        cursor.execute("CREATE INDEX idx_goals_category ON goals(goal_category)")
        
        conn.commit()
        
        print("✅ Complete database initialized successfully!")
        print("📊 Database Statistics:")
        
        # Show statistics
        cursor.execute("SELECT COUNT(*) FROM transactions")
        print(f"   • Transactions: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM goals")
        print(f"   • Goals: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM investments")
        print(f"   • Investments: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM portfolio")
        print(f"   • Portfolio Assets: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM risk_profile")
        print(f"   • Risk Profiles: {cursor.fetchone()[0]}")
        
        return True
        
    except Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🏦 Initializing RIA Investment Advisor Complete Database...")
    print("=" * 60)
    
    success = initialize_complete_database()
    
    if success:
        print("\n🎉 Database initialization completed successfully!")
        print("🚀 Your RIA Investment Advisor is ready for use!")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above.")
