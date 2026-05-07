#!/usr/bin/env python3
"""
Financial Goals Database Initialization Script
Comprehensive database setup for RIA Investment Advisor
"""

import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
import os

def create_connection():
    """Create database connection"""
    try:
        # Use the same database path as the main application
        db_path = '/Users/thanmayims/Documents/finance.db'
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_sql_script(conn, script_path):
    """Execute SQL script from file"""
    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()
        
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        
        print("✅ Financial goals database initialized successfully!")
        return True
        
    except Error as e:
        print(f"Error executing SQL script: {e}")
        return False

def display_database_summary(conn):
    """Display database summary after initialization"""
    try:
        cursor = conn.cursor()
        
        print("\n📊 Database Summary:")
        print("=" * 50)
        
        # Count records in each table
        tables = [
            ('goal_categories', 'Goal Categories'),
            ('goal_templates', 'Goal Templates'),
            ('financial_goals', 'Financial Goals'),
            ('goal_contributions', 'Goal Contributions'),
            ('goal_milestones', 'Goal Milestones')
        ]
        
        for table_name, display_name in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"• {display_name}: {count} records")
        
        # Display sample goals
        print("\n🎯 Sample Financial Goals:")
        print("=" * 50)
        
        cursor.execute("""
            SELECT 
                fg.goal_name,
                gc.category_name,
                fg.target_amount,
                fg.current_amount,
                fg.progress_percentage,
                fg.target_date,
                fg.priority
            FROM financial_goals fg
            JOIN goal_categories gc ON fg.category_id = gc.id
            ORDER BY fg.priority, fg.target_date
            LIMIT 5
        """)
        
        goals = cursor.fetchall()
        for goal in goals:
            print(f"• {goal[0]} ({goal[1]})")
            print(f"  Target: ${goal[2]:,.2f} | Current: ${goal[3]:,.2f} ({goal[4]:.1f}%)")
            print(f"  Due: {goal[5]} | Priority: {goal[6]}")
            print()
        
        # Display upcoming milestones
        print("🏆 Upcoming Milestones:")
        print("=" * 50)
        
        cursor.execute("""
            SELECT 
                fg.goal_name,
                gm.milestone_name,
                gm.target_amount,
                gm.target_date,
                gm.achieved
            FROM goal_milestones gm
            JOIN financial_goals fg ON gm.goal_id = fg.id
            WHERE gm.achieved = FALSE
            ORDER BY gm.target_date
            LIMIT 3
        """)
        
        milestones = cursor.fetchall()
        for milestone in milestones:
            status = "✅ Achieved" if milestone[4] else "🎯 Pending"
            print(f"• {milestone[0]} - {milestone[1]}")
            print(f"  Target: ${milestone[2]:,.2f} | Due: {milestone[3]} | {status}")
            print()
        
        return True
        
    except Error as e:
        print(f"Error displaying database summary: {e}")
        return False

def add_sample_user_goals(conn):
    """Add additional sample goals for demonstration"""
    try:
        cursor = conn.cursor()
        
        # Additional sample goals
        additional_goals = [
            ('Wedding Fund', 6, 30000.00, 5000.00, 1000.00, 
             (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'), 
             'Medium', 'Active', 'Low',
             'Dream wedding celebration', 'Starting our new life together'),
            
            ('Home Renovation', 4, 50000.00, 10000.00, 1500.00,
             (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d'),
             'Medium', 'Active', 'Medium',
             'Kitchen and bathroom renovation', 'Making our house perfect'),
            
            ('Emergency Travel Fund', 1, 8000.00, 2000.00, 300.00,
             (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
             'High', 'Active', 'Low',
             'Emergency travel for family needs', 'Always ready for family emergencies'),
            
            ('Gadget Upgrade Fund', 6, 5000.00, 1200.00, 200.00,
             (datetime.now() + timedelta(days=270)).strftime('%Y-%m-%d'),
             'Low', 'Active', 'Low',
             'Latest technology and gadgets', 'Staying up to date with technology'),
            
            ('Charitable Giving', 10, 12000.00, 3000.00, 500.00,
             (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
             'Medium', 'Active', 'Low',
             'Annual charitable donations', 'Giving back to the community')
        ]
        
        for goal in additional_goals:
            cursor.execute("""
                INSERT INTO financial_goals (
                    goal_name, category_id, target_amount, current_amount,
                    monthly_contribution, target_date, priority, status,
                    risk_tolerance, description, motivation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, goal)
        
        conn.commit()
        print("✅ Additional sample goals added successfully!")
        
        # Add sample contributions for the new goals
        cursor.execute("SELECT id FROM financial_goals WHERE goal_name IN ('Wedding Fund', 'Home Renovation', 'Emergency Travel Fund')")
        new_goal_ids = cursor.fetchall()
        
        for goal_id in new_goal_ids:
            cursor.execute("""
                INSERT INTO goal_contributions (goal_id, amount, contribution_type, description)
                VALUES (?, ?, ?, ?)
            """, (goal_id[0], 500.00, 'Manual', 'Initial contribution'))
        
        conn.commit()
        print("✅ Sample contributions added for new goals!")
        
        return True
        
    except Error as e:
        print(f"Error adding sample goals: {e}")
        return False

def main():
    """Main function to initialize the financial goals database"""
    print("🏦 Initializing Financial Goals Database")
    print("=" * 60)
    
    # Check if SQL script exists
    script_path = '/Users/thanmayims/finace pro/financial_goals_database.sql'
    if not os.path.exists(script_path):
        print(f"❌ SQL script not found: {script_path}")
        return False
    
    # Create database connection
    conn = create_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return False
    
    try:
        # Execute the SQL script
        if execute_sql_script(conn, script_path):
            # Add additional sample goals
            add_sample_user_goals(conn)
            
            # Display database summary
            display_database_summary(conn)
            
            print("\n🎉 Financial Goals Database Setup Complete!")
            print("🚀 Your RIA Investment Advisor is ready with comprehensive goal tracking!")
            return True
        else:
            print("❌ Failed to initialize database")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All systems ready! You can now:")
        print("   • Create and manage financial goals")
        print("   • Track contributions and progress")
        print("   • Set milestones and rewards")
        print("   • Generate goal-based recommendations")
        print("   • Monitor goal completion status")
    else:
        print("\n❌ Database initialization failed. Please check the error messages above.")
