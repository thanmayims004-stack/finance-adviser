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
    allow_origins=["http://localhost:3000"],  # React frontend
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
