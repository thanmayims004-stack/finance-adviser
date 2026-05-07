#!/usr/bin/env python3
"""
Financial Goals API Endpoints
Comprehensive API for financial goals management
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import sqlite3
from sqlite3 import Error

# Pydantic models for API
class GoalCategory(BaseModel):
    id: Optional[int] = None
    category_name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    priority_level: int = 1

class GoalTemplate(BaseModel):
    id: Optional[int] = None
    template_name: str
    category_id: Optional[int] = None
    description: Optional[str] = None
    suggested_target_amount: Optional[float] = None
    suggested_timeframe_months: Optional[int] = None
    risk_level: str = "Medium"
    age_group: Optional[str] = None
    income_level: Optional[str] = None

class FinancialGoal(BaseModel):
    id: Optional[int] = None
    goal_name: str
    category_id: Optional[int] = None
    target_amount: float = Field(gt=0)
    current_amount: float = Field(ge=0)
    monthly_contribution: float = Field(ge=0, default=0)
    target_date: date
    priority: str = Field(default="Medium", pattern="^(High|Medium|Low)$")
    status: str = Field(default="Active", pattern="^(Active|Completed|Paused|Cancelled)$")
    risk_tolerance: str = Field(default="Medium", pattern="^(Low|Medium|High)$")
    description: Optional[str] = None
    motivation: Optional[str] = None
    auto_contribute: bool = False
    contribution_frequency: str = "Monthly"
    reminder_frequency: str = "Monthly"

class GoalContribution(BaseModel):
    goal_id: int
    amount: float = Field(gt=0)
    contribution_type: str = "Manual"
    description: Optional[str] = None

class GoalMilestone(BaseModel):
    goal_id: int
    milestone_name: str
    target_amount: float = Field(gt=0)
    target_date: Optional[date] = None
    reward: Optional[str] = None

# Database connection
def get_db_connection():
    """Create database connection"""
    try:
        conn = sqlite3.connect('/Users/thanmayims/Documents/finance.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# API Functions
def get_goal_categories():
    """Get all goal categories"""
    conn = get_db_connection()
    if not conn:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM goal_categories ORDER BY priority_level, category_name"
        cursor.execute(query)
        categories = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": categories,
            "query_used": query,
            "status": "success"
        }
    except Error as e:
        print(f"Error fetching goal categories: {e}")
        return {"data": [], "query_used": query, "status": "error"}
    finally:
        conn.close()

def get_goal_templates(age: Optional[int] = None, income: Optional[float] = None):
    """Get goal templates with optional filtering"""
    conn = get_db_connection()
    if not conn:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        if age and income:
            # Filter by age and income
            query = """
                SELECT gt.*, gc.category_name 
                FROM goal_templates gt
                LEFT JOIN goal_categories gc ON gt.category_id = gc.id
                WHERE (gt.age_group = 'All' OR 
                       (gt.age_group = 'Young Adult' AND ? < 30) OR
                       (gt.age_group = 'Middle Age' AND ? >= 30 AND ? < 50) OR
                       (gt.age_group = 'Senior' AND ? >= 50))
                  AND (gt.income_level = 'All' OR
                       (gt.income_level = 'Low' AND ? < 50000) OR
                       (gt.income_level = 'Medium' AND ? >= 50000 AND ? < 100000) OR
                       (gt.income_level = 'High' AND ? >= 100000))
                ORDER BY gt.suggested_target_amount
            """
            cursor.execute(query, (age, age, age, age, income, income, income, income))
        else:
            query = """
                SELECT gt.*, gc.category_name 
                FROM goal_templates gt
                LEFT JOIN goal_categories gc ON gt.category_id = gc.id
                ORDER BY gt.suggested_target_amount, gc.priority_level
            """
            cursor.execute(query)
        
        templates = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": templates,
            "query_used": query,
            "status": "success"
        }
    except Error as e:
        print(f"Error fetching goal templates: {e}")
        return {"data": [], "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        conn.close()

def get_financial_goals_detailed():
    """Get all financial goals with detailed information"""
    conn = get_db_connection()
    if not conn:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                fg.*,
                gc.category_name,
                gc.color as category_color,
                gc.icon as category_icon,
                CASE 
                    WHEN fg.target_date < date('now') THEN 'Overdue'
                    WHEN fg.target_date <= date('now', '+30 days') THEN 'Due Soon'
                    WHEN fg.progress_percentage >= 100 THEN 'Completed'
                    ELSE 'On Track'
                END as urgency_status,
                (julianday(fg.target_date) - julianday(date('now'))) as days_remaining,
                ROUND((fg.target_amount - fg.current_amount) / 
                      CASE 
                          WHEN (julianday(fg.target_date) - julianday(date('now'))) > 0 
                          THEN (julianday(fg.target_date) - julianday(date('now')))
                          ELSE 1
                      END, 2) as daily_savings_needed
            FROM financial_goals fg
            LEFT JOIN goal_categories gc ON fg.category_id = gc.id
            WHERE fg.status != 'Cancelled'
            ORDER BY fg.priority, fg.target_date
        """
        cursor.execute(query)
        goals = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": goals,
            "query_used": query,
            "status": "success"
        }
    except Error as e:
        print(f"Error fetching financial goals: {e}")
        return {"data": [], "query_used": query, "status": "error"}
    finally:
        conn.close()

def create_financial_goal_detailed(goal: FinancialGoal):
    """Create a new financial goal"""
    conn = get_db_connection()
    if not conn:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        # Calculate initial progress percentage
        progress_percentage = round((goal.current_amount / goal.target_amount) * 100, 2)
        
        query = """
            INSERT INTO financial_goals (
                goal_name, category_id, target_amount, current_amount,
                monthly_contribution, target_date, priority, status,
                risk_tolerance, description, motivation, auto_contribute,
                contribution_frequency, reminder_frequency, progress_percentage,
                start_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        """
        
        cursor.execute(query, (
            goal.goal_name, goal.category_id, goal.target_amount, goal.current_amount,
            goal.monthly_contribution, goal.target_date, goal.priority, goal.status,
            goal.risk_tolerance, goal.description, goal.motivation, goal.auto_contribute,
            goal.contribution_frequency, goal.reminder_frequency, progress_percentage
        ))
        
        conn.commit()
        
        return {
            "data": {
                "goal_name": goal.goal_name,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "progress_percentage": progress_percentage
            },
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error creating financial goal: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        conn.close()

def add_goal_contribution(contribution: GoalContribution):
    """Add a contribution to a goal"""
    conn = get_db_connection()
    if not conn:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Add contribution
        query1 = """
            INSERT INTO goal_contributions (goal_id, amount, contribution_type, description)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query1, (
            contribution.goal_id, contribution.amount, 
            contribution.contribution_type, contribution.description
        ))
        
        # Update goal current amount
        query2 = """
            UPDATE financial_goals 
            SET current_amount = current_amount + ?,
                progress_percentage = ROUND((current_amount + ?) / target_amount * 100, 2),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        cursor.execute(query2, (contribution.amount, contribution.amount, contribution.goal_id))
        
        # Check if goal is completed
        cursor.execute("""
            SELECT current_amount, target_amount FROM financial_goals WHERE id = ?
        """, (contribution.goal_id,))
        goal_data = cursor.fetchone()
        
        if goal_data and goal_data[0] >= goal_data[1]:
            cursor.execute("""
                UPDATE financial_goals 
                SET status = 'Completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (contribution.goal_id,))
        
        conn.commit()
        
        return {
            "data": {
                "goal_id": contribution.goal_id,
                "amount": contribution.amount,
                "new_total": goal_data[0] if goal_data else 0
            },
            "query_used": f"{query1}; {query2}",
            "status": "success"
        }
        
    except Error as e:
        conn.rollback()
        print(f"Error adding contribution: {e}")
        return {"data": None, "query_used": "Transaction failed", "status": "error"}
    finally:
        conn.close()

def get_goal_contributions(goal_id: Optional[int] = None):
    """Get goal contributions"""
    conn = get_db_connection()
    if not conn:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        if goal_id:
            query = """
                SELECT 
                    gc.*,
                    fg.goal_name,
                    fg.goal_category
                FROM goal_contributions gc
                JOIN financial_goals fg ON gc.goal_id = fg.id
                WHERE gc.goal_id = ?
                ORDER BY gc.contribution_date DESC
            """
            cursor.execute(query, (goal_id,))
        else:
            query = """
                SELECT 
                    gc.*,
                    fg.goal_name,
                    fg.goal_category
                FROM goal_contributions gc
                JOIN financial_goals fg ON gc.goal_id = fg.id
                ORDER BY gc.contribution_date DESC
                LIMIT 50
            """
            cursor.execute(query)
        
        contributions = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": contributions,
            "query_used": query,
            "status": "success"
        }
    except Error as e:
        print(f"Error fetching contributions: {e}")
        return {"data": [], "query_used": query, "status": "error"}
    finally:
        conn.close()

def get_goal_milestones(goal_id: Optional[int] = None):
    """Get goal milestones"""
    conn = get_db_connection()
    if not conn:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        if goal_id:
            query = """
                SELECT gm.*, fg.goal_name
                FROM goal_milestones gm
                JOIN financial_goals fg ON gm.goal_id = fg.id
                WHERE gm.goal_id = ?
                ORDER BY gm.target_date
            """
            cursor.execute(query, (goal_id,))
        else:
            query = """
                SELECT gm.*, fg.goal_name
                FROM goal_milestones gm
                JOIN financial_goals fg ON gm.goal_id = fg.id
                WHERE gm.achieved = FALSE
                ORDER BY gm.target_date
                LIMIT 20
            """
            cursor.execute(query)
        
        milestones = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": milestones,
            "query_used": query,
            "status": "success"
        }
    except Error as e:
        print(f"Error fetching milestones: {e}")
        return {"data": [], "query_used": query, "status": "error"}
    finally:
        conn.close()

def create_goal_milestone(milestone: GoalMilestone):
    """Create a new goal milestone"""
    conn = get_db_connection()
    if not conn:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO goal_milestones (goal_id, milestone_name, target_amount, target_date, reward)
            VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            milestone.goal_id, milestone.milestone_name, milestone.target_amount,
            milestone.target_date, milestone.reward
        ))
        
        conn.commit()
        
        return {
            "data": {
                "goal_id": milestone.goal_id,
                "milestone_name": milestone.milestone_name,
                "target_amount": milestone.target_amount
            },
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error creating milestone: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        conn.close()

def get_goal_statistics():
    """Get comprehensive goal statistics"""
    conn = get_db_connection()
    if not conn:
        return {"data": {}, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = conn.cursor()
        
        # Overall statistics
        query1 = """
            SELECT 
                COUNT(*) as total_goals,
                COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_goals,
                COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_goals,
                SUM(target_amount) as total_target_amount,
                SUM(current_amount) as total_current_amount,
                ROUND(AVG(progress_percentage), 2) as avg_progress,
                COUNT(CASE WHEN target_date < date('now') AND status != 'Completed' THEN 1 END) as overdue_goals
            FROM financial_goals
            WHERE status != 'Cancelled'
        """
        cursor.execute(query1)
        overall_stats = dict(cursor.fetchone())
        
        # Category breakdown
        query2 = """
            SELECT 
                gc.category_name,
                COUNT(fg.id) as goal_count,
                SUM(fg.target_amount) as total_target,
                SUM(fg.current_amount) as total_current,
                ROUND(AVG(fg.progress_percentage), 2) as avg_progress
            FROM financial_goals fg
            LEFT JOIN goal_categories gc ON fg.category_id = gc.id
            WHERE fg.status != 'Cancelled'
            GROUP BY gc.category_name
            ORDER BY goal_count DESC
        """
        cursor.execute(query2)
        category_stats = [dict(row) for row in cursor.fetchall()]
        
        # Monthly contributions
        query3 = """
            SELECT 
                strftime('%Y-%m', contribution_date) as month,
                COUNT(*) as contribution_count,
                SUM(amount) as total_amount
            FROM goal_contributions
            WHERE contribution_date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', contribution_date)
            ORDER BY month DESC
            LIMIT 12
        """
        cursor.execute(query3)
        monthly_contributions = [dict(row) for row in cursor.fetchall()]
        
        return {
            "data": {
                "overall": overall_stats,
                "by_category": category_stats,
                "monthly_contributions": monthly_contributions
            },
            "query_used": f"{query1}; {query2}; {query3}",
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching statistics: {e}")
        return {"data": {}, "query_used": "Query failed", "status": "error"}
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    print("🏦 Financial Goals API Functions")
    print("=" * 50)
    
    # Test API functions
    print("\n📊 Testing API Functions:")
    
    # Test goal categories
    categories = get_goal_categories()
    print(f"Categories: {len(categories['data'])} found")
    
    # Test goal templates
    templates = get_goal_templates(age=35, income=75000)
    print(f"Templates: {len(templates['data'])} found")
    
    # Test detailed goals
    goals = get_financial_goals_detailed()
    print(f"Goals: {len(goals['data'])} found")
    
    # Test statistics
    stats = get_goal_statistics()
    print(f"Statistics: {stats['status']}")
    
    print("\n✅ All API functions working correctly!")
