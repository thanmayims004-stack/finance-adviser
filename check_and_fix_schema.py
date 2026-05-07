#!/usr/bin/env python3
"""
Check and fix database schema properly
"""

import sqlite3
import os

# Your database path
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def check_and_fix_schema():
    try:
        print(f"🔌 Connecting to database: {DB_PATH}")
        
        # Connect to your existing database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check transactions table structure
        print("📋 Checking transactions table...")
        cursor.execute('PRAGMA table_info(transactions)')
        transactions_columns = cursor.fetchall()
        print(f"   Columns: {[col[1] for col in transactions_columns]}")
        
        # Check goals table structure
        print("🎯 Checking goals table...")
        cursor.execute('PRAGMA table_info(goals)')
        goals_columns = cursor.fetchall()
        print(f"   Columns: {[col[1] for col in goals_columns]}")
        
        # Check risk_profile table structure
        print("⚖️  Checking risk_profile table...")
        cursor.execute('PRAGMA table_info(risk_profile)')
        risk_columns = cursor.fetchall()
        print(f"   Columns: {[col[1] for col in risk_columns]}")
        
        # Clear and properly populate risk_profile
        print("🧹 Clearing and repopulating risk_profile...")
        cursor.execute('DELETE FROM risk_profile')
        
        # Insert proper data in correct order
        cursor.execute('''
        INSERT INTO risk_profile (age, risk_tolerance) VALUES (?, ?)
        ''', (35, 'Balanced'))
        
        conn.commit()
        
        # Show sample data
        print("\n📊 Sample Data:")
        
        # Transactions
        cursor.execute('SELECT type, COUNT(*) as count, SUM(amount) as total FROM transactions GROUP BY type LIMIT 5')
        transactions = cursor.fetchall()
        print(f"   Transactions by type:")
        for row in transactions:
            print(f"     {row[0]}: {row[1]} transactions, Total: ${row[2]:,.2f}")
        
        # Goals
        cursor.execute('SELECT goal_name, target_amount, current_saved FROM goals LIMIT 3')
        goals = cursor.fetchall()
        print(f"   Sample goals:")
        for goal in goals:
            progress = (goal[2] / goal[1]) * 100 if goal[1] > 0 else 0
            print(f"     {goal[0]}: ${goal[2]:,.2f} / ${goal[1]:,.2f} ({progress:.1f}%)")
        
        # Risk Profile
        cursor.execute('SELECT age, risk_tolerance FROM risk_profile LIMIT 1')
        profile = cursor.fetchone()
        if profile:
            print(f"   Risk Profile: Age {profile[0]}, Risk Tolerance: {profile[1]}")
            
            # Show recommendation
            if profile[1] == 'Aggressive':
                allocation = "80% Stocks, 15% Bonds, 5% Cash"
            elif profile[1] == 'Conservative':
                allocation = "40% Stocks, 50% Bonds, 10% Cash"
            else:
                allocation = "60% Stocks, 35% Bonds, 5% Cash"
            
            print(f"   💡 Recommended: {allocation}")
        
        conn.close()
        print(f"\n✅ Database schema check completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_and_fix_schema()
