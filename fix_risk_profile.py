#!/usr/bin/env python3
"""
Fix risk_profile table with proper professional data
"""

import sqlite3
import os

# Your database path
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def fix_risk_profile():
    try:
        print(f"🔌 Connecting to database: {DB_PATH}")
        
        # Connect to your existing database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Clear existing risk profile data
        print("🧹 Cleaning up existing risk profile data...")
        cursor.execute('DELETE FROM risk_profile')
        
        # Add professional risk profile data
        print("📊 Adding professional risk profile...")
        professional_profiles = [
            {
                'investor_name': 'Alex Johnson',
                'age': 35,
                'risk_tolerance': 'Balanced',
                'investment_horizon': 25,
                'annual_income': 85000.00,
                'dependents': 2,
                'investment_experience': 'Intermediate',
                'financial_knowledge': 'Good'
            },
            {
                'investor_name': 'Sarah Williams',
                'age': 28,
                'risk_tolerance': 'Aggressive',
                'investment_horizon': 35,
                'annual_income': 120000.00,
                'dependents': 0,
                'investment_experience': 'Advanced',
                'financial_knowledge': 'Expert'
            },
            {
                'investor_name': 'Michael Chen',
                'age': 45,
                'risk_tolerance': 'Conservative',
                'investment_horizon': 15,
                'annual_income': 95000.00,
                'dependents': 3,
                'investment_experience': 'Beginner',
                'financial_knowledge': 'Basic'
            }
        ]
        
        for profile in professional_profiles:
            cursor.execute('''
            INSERT INTO risk_profile (investor_name, age, risk_tolerance, investment_horizon, annual_income, dependents, investment_experience, financial_knowledge) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile['investor_name'],
                profile['age'],
                profile['risk_tolerance'],
                profile['investment_horizon'],
                profile['annual_income'],
                profile['dependents'],
                profile['investment_experience'],
                profile['financial_knowledge']
            ))
        
        conn.commit()
        
        # Display results
        print("\n✅ Risk profile data fixed successfully!")
        
        cursor.execute('SELECT * FROM risk_profile ORDER BY created_at DESC')
        profiles = cursor.fetchall()
        
        print(f"\n⚖️  Professional Risk Profiles:")
        for profile in profiles:
            print(f"\n   👤 {profile[1] if len(profile) > 1 else 'Unknown'}")
            print(f"   Age: {profile[2] if len(profile) > 2 else 'N/A'}")
            print(f"   Risk Tolerance: {profile[3] if len(profile) > 3 else 'N/A'}")
            print(f"   Investment Horizon: {profile[4] if len(profile) > 4 else 'N/A'} years")
            print(f"   Annual Income: ${profile[5]:,.2f if profile[5] and len(profile) > 5 else 0}")
            print(f"   Dependents: {profile[6] if len(profile) > 6 else 0}")
            print(f"   Experience: {profile[7] if len(profile) > 7 else 'N/A'}")
            print(f"   Knowledge: {profile[8] if len(profile) > 8 else 'N/A'}")
            
            # Show recommendations for each profile
            risk_tolerance = profile[3] if len(profile) > 3 else 'Balanced'
            if risk_tolerance == 'Aggressive':
                allocation = "80% Stocks, 15% Bonds, 5% Cash"
            elif risk_tolerance == 'Conservative':
                allocation = "40% Stocks, 50% Bonds, 10% Cash"
            else:
                allocation = "60% Stocks, 35% Bonds, 5% Cash"
            
            print(f"   💡 Recommended: {allocation}")
        
        # Show final database summary
        print(f"\n📈 Final Database Summary:")
        
        # Transactions
        cursor.execute('SELECT type, COUNT(*) as count FROM transactions GROUP BY type')
        transactions = cursor.fetchall()
        print(f"   Transactions: {sum(row[1] for row in transactions)} total")
        for row in transactions:
            print(f"     - {row[0]}: {row[1]}")
        
        # Goals
        cursor.execute('SELECT COUNT(*) FROM goals')
        goals_count = cursor.fetchone()[0]
        print(f"   Goals: {goals_count} financial goals")
        
        # Risk Profiles
        cursor.execute('SELECT COUNT(*) FROM risk_profile')
        profiles_count = cursor.fetchone()[0]
        print(f"   Risk Profiles: {profiles_count} investor profiles")
        
        conn.close()
        print(f"\n🎉 Your professional Investment Advisor database is now complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_risk_profile()
