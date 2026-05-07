from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from groq import Groq

load_dotenv()

app = FastAPI(title="Finance API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_PATH = '/Users/thanmayims/Documents/finance.db'

def get_db_connection():
    """Create and return a SQLite database connection"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row  # Enable dictionary-like access
        return connection
    except Error as e:
        print(f"Error connecting to SQLite Database: {e}")
        return None

class SpendingData(BaseModel):
    category: str
    amount: float
    date: str

class AIAdviceResponse(BaseModel):
    advice: str
    status: str

# RIA Models
class Investment(BaseModel):
    id: int
    investment_type: str
    amount: float
    purchase_date: str
    current_value: float
    description: str

class RiskProfile(BaseModel):
    id: int
    age: int
    risk_tolerance: str
    created_at: str

class FinancialGoal(BaseModel):
    id: int
    goal_name: str
    target_amount: float
    current_amount: float
    target_date: str
    goal_type: str
    created_at: str

class RiskProfileRequest(BaseModel):
    age: int
    risk_tolerance: str

class FinancialGoalRequest(BaseModel):
    goal_name: str
    target_amount: float
    current_amount: float
    target_date: str
    goal_type: str

@app.get("/")
async def root():
    return {"message": "Finance API is running"}

@app.get("/health")
async def health_check():
    """Check if the database connection is working"""
    connection = get_db_connection()
    if connection:
        connection.close()
        return {"status": "healthy", "database": "connected"}
    else:
        return {"status": "unhealthy", "database": "disconnected"}

@app.get("/api/transactions")
async def get_transactions():
    """Get all transactions with type filtering"""
    connection = get_db_connection()
    if not connection:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id, txn_date, description, amount, category, type 
        FROM transactions 
        ORDER BY txn_date DESC
        """
        
        cursor.execute(query)
        transactions = cursor.fetchall()
        
        # Convert to list of dicts
        transaction_data = []
        for txn in transactions:
            transaction_data.append({
                "id": txn['id'],
                "txn_date": txn['txn_date'],
                "description": txn['description'],
                "amount": float(txn['amount']),
                "category": txn['category'],
                "type": txn['type']
            })
        
        return {
            "data": transaction_data,
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching transactions: {e}")
        return {"data": [], "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/api/spending")
async def get_spending_data():
    """Get spending data grouped by category"""
    connection = get_db_connection()
    if not connection:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        # Query to get spending by category
        query = """
        SELECT 
            category,
            SUM(amount) as total_amount,
            COUNT(*) as transaction_count
        FROM transactions 
        WHERE amount < 0  -- Assuming expenses are negative
        GROUP BY category
        ORDER BY total_amount ASC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Format the data for the chart
        spending_data = []
        for row in results:
            spending_data.append({
                "category": row['category'],
                "amount": abs(float(row['total_amount'])),
                "count": row['transaction_count']
            })
        
        return {
            "data": spending_data,
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching spending data: {e}")
        return {"data": [], "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/api/spending/monthly", response_model=List[Dict[str, Any]])
async def get_monthly_spending():
    """Get monthly spending trends"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            DATE_FORMAT(date, '%Y-%m') as month,
            SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income
        FROM transactions 
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(date, '%Y-%m')
        ORDER BY month
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
        
    except Error as e:
        print(f"Error fetching monthly spending: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_latest_transactions(limit=10):
    """Get latest transactions from database"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT category, amount, date, description
        FROM transactions 
        ORDER BY date DESC, created_at DESC
        LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        return results
        
    except Error as e:
        print(f"Error fetching latest transactions: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/ai-advice", response_model=AIAdviceResponse)
async def get_ai_advice():
    """Get AI-powered financial advice based on spending data"""
    try:
        # Get latest transaction data
        transactions = get_latest_transactions(10)
        
        if not transactions:
            return {
                "advice": "No transaction data available. Start tracking your expenses to get personalized advice!",
                "status": "no_data"
            }
        
        # Format transaction data for AI
        transaction_summary = "Recent spending data:\n"
        for transaction in transactions:
            transaction_summary += f"- {transaction['category']}: ${abs(float(transaction['amount'])):.2f} on {transaction['date']}\n"
        
        # Initialize Groq client
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key or groq_api_key == 'your_copied_key_here':
            return {
                "advice": "Please add your Groq API key to the .env file to get AI advice!",
                "status": "no_api_key"
            }
        
        client = Groq(api_key=groq_api_key)
        
        # Create the prompt
        prompt = f"""Based on this spending data, give me one short, witty, and helpful saving tip.
        
{transaction_summary}
        
Make it concise (under 50 words), practical, and slightly humorous. Focus on the spending patterns shown."""
        
        # Get AI response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            temperature=0.7,
        )
        
        advice = chat_completion.choices[0].message.content.strip()
        
        return {
            "advice": advice,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error getting AI advice: {e}")
        return {
            "advice": "Oops! Something went wrong while getting your AI advice. Please try again.",
            "status": "error"
        }

@app.get("/get-advice")
async def get_financial_advice():
    """Get financial advice by analyzing transactions data with Groq"""
    connection = get_db_connection()
    if not connection:
        return {
            "advice": "Unable to connect to database.",
            "query_used": "Failed to connect",
            "status": "error"
        }
    
    try:
        cursor = connection.cursor()
        
        # Query last 5 transactions
        query = """
        SELECT category, amount, txn_date, description 
        FROM transactions 
        ORDER BY txn_date DESC 
        LIMIT 5
        """
        
        cursor.execute(query)
        transactions = cursor.fetchall()
        
        # Convert transactions to string format
        transactions_str = "Last 5 Transactions:\n"
        for t in transactions:
            transactions_str += f"- {t['txn_date']}: {t['category']} - ${abs(float(t['amount'])):.2f}"
            if t['description']:
                transactions_str += f" ({t['description']})"
            transactions_str += "\n"
        
        # Get Groq API key
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key or groq_api_key == 'your_copied_key_here':
            return {
                "advice": "Please add your Groq API key to the .env file to get AI advice!",
                "query_used": query,
                "status": "no_api_key"
            }
        
        # Initialize Groq client
        client = Groq(api_key=groq_api_key)
        
        # Create the specific prompt
        prompt = f"""Based on these transactions, give me one funny but useful saving tip.

{transactions_str}

Please respond with one funny but useful saving tip that's concise and actionable."""
        
        # Get AI response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=200,
            temperature=0.7,
        )
        
        advice = chat_completion.choices[0].message.content.strip()
        
        return {
            "advice": advice,
            "query_used": query,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error getting financial advice: {e}")
        return {
            "advice": "Error processing your financial data. Please try again.",
            "query_used": query if 'query' in locals() else "Query failed",
            "status": "error"
        }
    finally:
        if connection:
            cursor.close()
            connection.close()

# RIA Endpoints

@app.get("/api/investments")
async def get_investments():
    """Get all investments with portfolio diversification data"""
    connection = get_db_connection()
    if not connection:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id, investment_type, amount, purchase_date, current_value, description 
        FROM investments 
        ORDER BY purchase_date DESC
        """
        
        cursor.execute(query)
        investments = cursor.fetchall()
        
        # Convert to list of dicts
        investment_data = []
        for inv in investments:
            investment_data.append({
                "id": inv['id'],
                "investment_type": inv['investment_type'],
                "amount": float(inv['amount']),
                "purchase_date": inv['purchase_date'],
                "current_value": float(inv['current_value']),
                "description": inv['description']
            })
        
        return {
            "data": investment_data,
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching investments: {e}")
        return {"data": [], "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/api/risk-profile")
async def get_risk_profile():
    """Get user's risk profile"""
    connection = get_db_connection()
    if not connection:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id, age, risk_tolerance, created_at 
        FROM risk_profile 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        
        cursor.execute(query)
        profile = cursor.fetchone()
        
        if profile:
            profile_data = {
                "id": profile['id'],
                "age": profile['age'],
                "risk_tolerance": profile['risk_tolerance'],
                "created_at": profile['created_at']
            }
        else:
            profile_data = None
        
        return {
            "data": profile_data,
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching risk profile: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.post("/api/risk-profile")
async def create_risk_profile(profile: RiskProfileRequest):
    """Create or update risk profile"""
    connection = get_db_connection()
    if not connection:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO risk_profile (age, risk_tolerance) 
        VALUES (?, ?)
        """
        
        cursor.execute(query, (profile.age, profile.risk_tolerance))
        connection.commit()
        
        return {
            "data": {"message": "Risk profile created successfully"},
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error creating risk profile: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/api/goals")
async def get_goals():
    """Get all financial goals with progress tracking"""
    connection = get_db_connection()
    if not connection:
        return {"data": [], "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id, goal_name, target_amount, current_saved, deadline, goal_category, priority, created_at, updated_at 
        FROM goals 
        ORDER BY deadline ASC
        """
        
        cursor.execute(query)
        goals = cursor.fetchall()
        
        # Convert to list of dicts with progress calculation
        goals_data = []
        for goal in goals:
            progress = (float(goal['current_saved']) / float(goal['target_amount'])) * 100 if goal['target_amount'] > 0 else 0
            goals_data.append({
                "id": goal['id'],
                "goal_name": goal['goal_name'],
                "target_amount": float(goal['target_amount']),
                "current_saved": float(goal['current_saved']),
                "deadline": goal['deadline'],
                "goal_category": goal['goal_category'],
                "priority": goal['priority'],
                "progress_percentage": round(progress, 1),
                "created_at": goal['created_at'],
                "updated_at": goal['updated_at']
            })
        
        return {
            "data": goals_data,
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error fetching goals: {e}")
        return {"data": [], "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.post("/api/financial-goals")
async def create_financial_goal(goal: FinancialGoalRequest):
    """Create a new financial goal"""
    connection = get_db_connection()
    if not connection:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO financial_goals (goal_name, target_amount, current_amount, target_date, goal_type) 
        VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (goal.goal_name, goal.target_amount, goal.current_amount, goal.target_date, goal.goal_type))
        connection.commit()
        
        return {
            "data": {
                "goal_name": goal.goal_name,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "target_date": goal.target_date,
                "goal_type": goal.goal_type
            },
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error creating financial goal: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.put("/api/financial-goals/{goal_id}")
async def update_financial_goal(goal_id: int, goal_update: dict):
    """Update a financial goal's target amount"""
    connection = get_db_connection()
    if not connection:
        return {"data": None, "query_used": "Failed to connect", "status": "error"}
    
    try:
        cursor = connection.cursor()
        
        # Check if goal exists
        check_query = "SELECT id FROM goals WHERE id = ?"
        cursor.execute(check_query, (goal_id,))
        existing_goal = cursor.fetchone()
        
        if not existing_goal:
            return {"data": None, "query_used": check_query, "status": "error", "message": "Goal not found"}
        
        # Update the target amount
        query = """
        UPDATE goals 
        SET target_amount = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        
        cursor.execute(query, (
            goal_update.get('target_amount'),
            goal_id
        ))
        
        connection.commit()
        
        return {
            "data": {
                "goal_id": goal_id,
                "target_amount": goal_update.get('target_amount')
            },
            "query_used": query,
            "status": "success"
        }
        
    except Error as e:
        print(f"Error updating financial goal: {e}")
        return {"data": None, "query_used": query if 'query' in locals() else "Query failed", "status": "error"}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/get-goals")
async def get_goals_advice():
    """Get AI advice based on goals and transactions"""
    connection = get_db_connection()
    if not connection:
        return {
            "advice": "Unable to connect to database.",
            "query_used": "Failed to connect",
            "status": "error"
        }
    
    try:
        cursor = connection.cursor()
        
        # Get goals data
        goals_query = """
        SELECT goal_name, target_amount, current_saved, deadline, goal_category, priority 
        FROM goals 
        ORDER BY deadline ASC
        """
        cursor.execute(goals_query)
        goals_data = cursor.fetchall()
        
        # Get recent transactions (last 30 days)
        transactions_query = """
        SELECT txn_date, description, amount, category, type 
        FROM transactions 
        WHERE txn_date >= date('now', '-30 days')
        ORDER BY txn_date DESC
        """
        cursor.execute(transactions_query)
        transactions_data = cursor.fetchall()
        
        # Get spending by category for last 30 days
        spending_query = """
        SELECT category, SUM(amount) as total_spent 
        FROM transactions 
        WHERE txn_date >= date('now', '-30 days') AND amount < 0 AND type = 'Expense'
        GROUP BY category 
        ORDER BY total_spent ASC
        """
        cursor.execute(spending_query)
        spending_data = cursor.fetchall()
        
        # Format data for AI
        goals_str = "Financial Goals:\n"
        for goal in goals_data:
            progress = (float(goal['current_saved']) / float(goal['target_amount'])) * 100 if goal['target_amount'] > 0 else 0
            goals_str += f"- {goal['goal_name']}: ${goal['current_saved']:.2f} / ${goal['target_amount']:.2f} ({progress:.1f}%) - Due: {goal['deadline']}\n"
        
        transactions_str = f"\nRecent Transactions (Last 30 days):\n"
        for txn in transactions_data[:10]:  # Show last 10 transactions
            transactions_str += f"- {txn['description']}: ${txn['amount']:.2f} ({txn['category']})\n"
        
        spending_str = f"\nMonthly Spending by Category:\n"
        for spending in spending_data:
            spending_str += f"- {spending['category']}: ${spending['total_spent']:.2f}\n"
        
        # Get Groq API key
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key or groq_api_key == 'your_copied_key_here':
            return {
                "advice": "Please add your Groq API key to the .env file to get goals advice!",
                "query_used": goals_query + " | " + transactions_query,
                "status": "no_api_key"
            }
        
        # Initialize Groq client
        client = Groq(api_key=groq_api_key)
        
        # Find the most urgent goal (closest deadline with lowest progress)
        urgent_goal = None
        for goal in goals_data:
            progress = (float(goal['current_saved']) / float(goal['target_amount'])) * 100 if goal['target_amount'] > 0 else 0
            if urgent_goal is None or (progress < 50 and goal['priority'] == 'High'):
                urgent_goal = goal
        
        # Create enhanced AI prompt
        prompt = f"""You are a Certified Financial Planner specializing in goal-based financial advice. Analyze the user's goals and spending to provide actionable advice.

{goals_str}

{transactions_str}

{spending_str}

Please provide specific advice in this format:
1. Start with the most urgent goal progress: 'You have saved X% of your [Goal Name].'
2. Based on their spending patterns, identify the best category to reduce: 'Based on your spending this month, you can reach your goal 2 months early if you cut back on [Category].'
3. Provide 1-2 specific, actionable savings tips
4. End with encouragement

Keep it concise, actionable, and motivating."""

        # Get AI response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            temperature=0.7,
        )
        
        advice = chat_completion.choices[0].message.content.strip()
        
        return {
            "advice": advice,
            "query_used": goals_query + " | " + transactions_query + " | " + spending_query,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error getting goals advice: {e}")
        return {
            "advice": "Error processing your goals and transactions. Please try again.",
            "query_used": "Query failed",
            "status": "error"
        }
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/ria-advice")
async def get_ria_advice():
    """Get RIA-style investment advice using portfolio and risk profile"""
    connection = get_db_connection()
    if not connection:
        return {
            "advice": "Unable to connect to database.",
            "query_used": "Failed to connect",
            "status": "error"
        }
    
    try:
        cursor = connection.cursor()
        
        # Get portfolio data
        portfolio_query = """
        SELECT investment_type, SUM(current_value) as total_value 
        FROM investments 
        GROUP BY investment_type
        """
        cursor.execute(portfolio_query)
        portfolio_data = cursor.fetchall()
        
        # Get risk profile
        risk_query = """
        SELECT age, risk_tolerance 
        FROM risk_profile 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        cursor.execute(risk_query)
        risk_profile = cursor.fetchone()
        
        # Calculate total portfolio value
        total_portfolio = sum(float(row['total_value']) for row in portfolio_data)
        
        # Format data for AI
        portfolio_str = f"Portfolio Value: ${total_portfolio:.2f}\n"
        portfolio_str += "Investments:\n"
        for inv in portfolio_data:
            portfolio_str += f"- {inv['investment_type']}: ${inv['total_value']:.2f}\n"
        
        if risk_profile:
            portfolio_str += f"\nUser Profile: Age {risk_profile['age']}, Risk Tolerance: {risk_profile['risk_tolerance']}"
        else:
            portfolio_str += "\nUser Profile: Age 30, Risk Tolerance: Medium (default)"
        
        # Get Groq API key
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key or groq_api_key == 'your_copied_key_here':
            return {
                "advice": "Please add your Groq API key to the .env file to get RIA advice!",
                "query_used": portfolio_query + " | " + risk_query,
                "status": "no_api_key"
            }
        
        # Initialize Groq client
        client = Groq(api_key=groq_api_key)
        
        # Create RIA-style prompt
        prompt = f"""You are a Certified Financial Planner. Analyze this user's ${total_portfolio:.2f} portfolio and their {risk_profile['risk_tolerance'] if risk_profile else 'Medium'} risk tolerance. Suggest a diversification strategy using the 50/30/20 rule and recommend asset allocation.

{portfolio_str}

Please respond with professional investment advice including:
1. Current portfolio analysis
2. Recommended asset allocation (50/30/20 rule)
3. Specific investment suggestions
4. Risk considerations"""
        
        # Get AI response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            temperature=0.3,
        )
        
        advice = chat_completion.choices[0].message.content.strip()
        
        return {
            "advice": advice,
            "query_used": portfolio_query + " | " + risk_query,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error getting RIA advice: {e}")
        return {
            "advice": "Error processing your portfolio data. Please try again.",
            "query_used": "Query failed",
            "status": "error"
        }
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
