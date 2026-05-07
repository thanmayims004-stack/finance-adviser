# Finance Tracker - Setup Guide

## 🚀 Quick Start

### 1. Database Setup

First, set up your MySQL database:

```bash
# Connect to MySQL
mysql -u thanmay -p

# Run the setup script
source /Users/thanmayims/finace\ pro/setup_database.sql
```

### 2. AI Setup (Optional but Recommended)

Add your Groq API key to get AI financial advice:

```bash
# Edit the .env file and replace the placeholder
nano .env

# Replace "your_copied_key_here" with your actual Groq API key
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Backend Setup

```bash
# Navigate to project directory
cd "/Users/thanmayims/finace pro"

# Install Python dependencies
pip3 install -r requirements.txt

# Start the FastAPI server
python3 main.py
```

The API will be available at `http://localhost:8000`

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 📋 Features

- **FastAPI Backend**: RESTful API with MySQL database connection
- **React Frontend**: Modern UI with TypeScript
- **Dark Mode**: Professional dark theme with toggle
- **Recharts Integration**: Beautiful bar charts for spending visualization
- **AI Financial Advisor**: Get personalized saving tips using Groq's Llama 3.3 model
- **Real-time Data**: Live connection status and data refresh
- **Responsive Design**: Works on desktop and mobile

## 🗂️ Project Structure

```
finance pro/
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── .env                   # Database credentials
├── setup_database.sql     # Database setup script
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS config
└── README.md              # Documentation
```

## 🔧 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Database connection status
- `GET /api/spending` - Spending data by category
- `GET /api/spending/monthly` - Monthly spending trends
- `GET /ai-advice` - AI-powered financial advice (requires Groq API key)

## 🎨 UI Components

- **SpendingChart**: Interactive bar chart using Recharts
- **StatsCard**: Display key metrics
- **Header**: Navigation with dark mode toggle
- **AIAdvice**: Interactive AI financial advisor with Groq integration
- **Responsive Layout**: Mobile-friendly design

## 🌐 Database Schema

```sql
transactions table:
- id (INT, Primary Key)
- category (VARCHAR)
- amount (DECIMAL)
- date (DATE)
- description (TEXT)
- created_at (TIMESTAMP)
```

## 📊 Sample Data

The setup script includes sample transactions for:
- Food, Transport, Entertainment, Shopping
- Bills, Healthcare, Salary, Freelance income
- Multiple categories with realistic amounts

## 🔍 Troubleshooting

1. **Database Connection Issues**:
   - Verify MySQL is running
   - Check credentials in `.env` file
   - Ensure database 'finance' exists

2. **Frontend Issues**:
   - Install Node.js dependencies with `npm install`
   - Check that backend is running on port 8000
   - Verify CORS settings in main.py

3. **Dependencies Issues**:
   - Python: `pip install -r requirements.txt`
   - Node.js: `npm install` in frontend directory

## 🚀 Running the Application

1. Start MySQL service
2. Run database setup script
3. Start FastAPI backend: `python main.py`
4. Start React frontend: `npm start` (in frontend directory)
5. Open `http://localhost:3000` in your browser

The app will show:
- Database connection status
- Total spending statistics
- Interactive spending chart by category
- Dark/light mode toggle
- Real-time data refresh
