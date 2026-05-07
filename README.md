# 💰 Finance Adviser

A modern finance tracking application with AI-powered financial advice, featuring a FastAPI backend and React frontend with real-time spending visualization.

## 🌟 Features

- 🤖 **AI Financial Advice** - Get personalized saving tips powered by Groq's Llama 3.3 70B model
- 📊 **Interactive Dashboard** - Beautiful pie charts showing spending by category
- 🔍 **SQL Trace Transparency** - See exactly what queries power your financial insights
- 🌙 **Dark Mode** - Modern, professional dark theme
- 📱 **Responsive Design** - Works perfectly on desktop and mobile
- 💾 **SQLite Database** - Local database for secure transaction storage

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **SQLite** - Lightweight, serverless database engine
- **Groq AI** - Fast inference platform for Llama 3.3 70B model
- **Python** - Core backend programming language

### Frontend
- **React** - Modern JavaScript library for building user interfaces
- **TypeScript** - Type-safe JavaScript for better code quality
- **TailwindCSS** - Utility-first CSS framework for rapid styling
- **Recharts** - Composable charting library for data visualization
- **Axios** - Promise-based HTTP client for API communication

## 🚀 How to Install

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### 1. Clone the Repository
```bash
git clone https://github.com/thanmayims004-stack/finance-adviser.git
cd finance-adviser
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the root directory:
```env
DB_PATH=/path/to/your/finance.db
GROQ_API_KEY=your_groq_api_key_here
```

#### Get Groq API Key
1. Visit [Groq Console](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

#### Start the Backend Server
```bash
python3 -m uvicorn main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Node.js Dependencies
```bash
npm install
```

#### Start the Frontend Server
```bash
npm start
```

The application will be available at `http://localhost:3000`

### 4. Database Setup

#### Create SQLite Database
The application uses SQLite for local data storage. Create a database file and set up the transactions table:

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_date DATE,
    description VARCHAR(255),
    amount DECIMAL(10,2),
    category VARCHAR(50)
);
```

#### Add Sample Data (Optional)
```sql
INSERT INTO transactions (txn_date, description, amount, category) VALUES 
('2024-05-01', 'Grocery Store', -50.25, 'Food'),
('2024-05-02', 'Salary Credit', 3000.00, 'Income'),
('2024-05-03', 'Netflix', -15.99, 'Subscription');
```

## 📡 API Endpoints

### Core Endpoints
- `GET /health` - Health check and database connection status
- `GET /api/spending` - Get spending data grouped by category with SQL trace
- `GET /get-advice` - Get AI financial advice based on last 5 transactions

### API Documentation
Visit `http://localhost:8001/docs` for interactive API documentation.

## 🎯 How It Works

### AI Advice System
1. **Data Collection**: Retrieves your last 5 transactions from the database
2. **AI Analysis**: Sends transaction data to Groq's Llama 3.3 70B model
3. **Smart Tips**: Returns funny but useful saving suggestions
4. **Transparency**: Shows the exact SQL query used for data retrieval

### Spending Visualization
- **Real-time Data**: Fetches latest spending information
- **Category Breakdown**: Groups expenses by category
- **Interactive Charts**: Hover over pie slices for detailed information
- **Color Coding**: Each category has a unique color for easy identification

## 🎨 UI Components

- **Dashboard**: Main overview with spending statistics
- **Pie Chart**: Visual representation of spending by category
- **AI Advice Section**: Get personalized financial tips
- **Technical Trace**: SQL query transparency for educational purposes
- **Dark Mode**: Easy-on-the-eyes professional theme

## 📊 Sample Categories

The application tracks expenses across common categories:
- 🍔 **Food & Dining**
- 💡 **Bills & Utilities**
- 🛍️ **Shopping**
- 🚗 **Transportation**
- 💪 **Health & Fitness**
- 🎬 **Entertainment**
- 📱 **Subscriptions**

## 🔧 Configuration

### Environment Variables
```env
DB_PATH=/Users/thanmayims/Documents/finance.db
GROQ_API_KEY=gsk_your_api_key_here
```

### Port Configuration
- Backend: `8001` (configurable)
- Frontend: `3000` (standard React port)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing fast AI inference capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [React](https://reactjs.org/) for the powerful frontend library
- [Recharts](https://recharts.org/) for the beautiful charting components
- [TailwindCSS](https://tailwindcss.com/) for the utility-first CSS framework

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ for smarter financial management** 🚀
