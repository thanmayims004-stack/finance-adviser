# 🏦 RIA Investment Advisor

A professional-grade Registered Investment Advisor (RIA) platform built with FastAPI and React, featuring AI-powered financial advice, goal tracking, and portfolio management with a premium Deep Navy & Emerald Green interface.

## ✨ Features

### 🎯 **Investment Advisory**
- **AI-Powered Advice**: Groq AI integration with Llama 3.3 70B model
- **Risk Profiling**: Personalized investment style assessment (Aggressive/Conservative/Balanced)
- **50/30/20 Strategy**: Professional asset allocation recommendations
- **Portfolio Analysis**: Real-time investment performance tracking

### 📊 **Financial Goals & Milestones**
- **Goal Tracking**: Set and monitor multiple financial goals
- **Progress Visualization**: Color-coded progress bars (Green/Yellow/Blue scheme)
- **Smart Recommendations**: AI suggests spending optimizations to reach goals faster
- **Deadline Management**: Track time remaining for each goal

### 💼 **Portfolio Management**
- **Investment Tracking**: Stocks, Bonds, Mutual Funds, ETFs
- **Performance Metrics**: Gain/Loss calculations and percentage returns
- **Asset Allocation**: Diversified portfolio analysis
- **Transaction History**: Complete audit trail with categorization

### 🎨 **Premium UI/UX**
- **Deep Navy & Emerald Green Theme**: Professional financial services aesthetic
- **Lucide-React Icons**: Modern, scalable iconography
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Micro-interactions**: Smooth animations and hover effects
## 🏗️ Architecture

### Backend (FastAPI)
```
├── � Database Schema
│   ├── transactions (with type column)
│   ├── goals (target_amount, current_saved, deadline)
│   └── risk_profile (investment style, horizon, income)
├── 🔗 API Endpoints
│   ├── /api/transactions - Transaction management
│   ├── /api/goals - Goal CRUD operations
│   ├── /api/risk-profile - Risk assessment
│   ├── /ria-advice - Portfolio recommendations
│   └── /get-goals - AI-powered goal advice
└── 🤖 AI Integration
    └── Groq AI with Certified Financial Planner prompts
```

### Frontend (React)
```
├── 🎯 Components
│   ├── FinancialMilestones - Progress tracking
│   ├── Portfolio - Investment overview
│   ├── RiskProfile - Risk assessment
│   ├── RIAAdvice - AI recommendations
│   └── Dashboard - Main interface
├── 🎨 Styling
│   ├── Tailwind CSS
│   ├── Custom CSS variables
│   └── Premium color scheme
└── 🔗 API Services
    └── Axios-based HTTP client
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- SQLite 3
- Groq API key

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/thanmayims004-stack/finance-adviser.git
cd finance-adviser
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

4. **Initialize the database**
```bash
python check_and_fix_schema.py
```

5. **Start the backend server**
```bash
python main.py
```

The API will be available at `http://localhost:8001`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

The application will be available at `http://localhost:3000`

## � Database Schema

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    txn_date DATE,
    description VARCHAR(255),
    amount DECIMAL(10,2),
    category VARCHAR(100),
    type VARCHAR(20) -- 'Investment', 'Dividend', 'Expense'
);
```

### Goals Table
```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY,
    goal_name VARCHAR(255),
    target_amount DECIMAL(12,2),
    current_saved DECIMAL(12,2),
    deadline DATE,
    goal_category VARCHAR(50),
    priority VARCHAR(20)
);
```

### Risk Profile Table
```sql
CREATE TABLE risk_profile (
    id INTEGER PRIMARY KEY,
    age INTEGER,
    risk_tolerance VARCHAR(20), -- 'Aggressive', 'Conservative', 'Balanced'
    investment_horizon INTEGER,
    annual_income DECIMAL(12,2),
    dependents INTEGER
);
```

## 🎯 Progress Bar Color Scheme

- 🟢 **Green (#10b981)**: Goals more than 50% complete
- 🟡 **Yellow (#f59e0b)**: Goals less than 50% complete
- 🔵 **Blue (#3b82f6)**: Investment-related goals (Retirement, Savings)

## 🤖 AI Features

### Investment Advice
- Portfolio analysis based on current holdings
- Risk-adjusted recommendations
- 50/30/20 asset allocation strategy
- Professional Certified Financial Planner persona

### Goal-Based Recommendations
- Spending pattern analysis
- Goal completion optimization
- Category-specific savings suggestions
- Timeline acceleration strategies

## 🔧 API Endpoints

### Transactions
- `GET /api/transactions` - Get all transactions with type filtering
- `GET /api/spending` - Get spending data by category

### Goals
- `GET /api/goals` - Get all financial goals with progress
- `POST /api/financial-goals` - Create new financial goal

### Risk Profile
- `GET /api/risk-profile` - Get current risk profile
- `POST /api/risk-profile` - Create/update risk profile

### AI Advice
- `GET /ria-advice` - Get portfolio investment advice
- `GET /get-goals` - Get AI-powered goal recommendations

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight, serverless database
- **Groq AI**: Advanced AI model integration
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful & consistent icon toolkit
- **Axios**: Promise-based HTTP client

## 🎨 UI Components

### Financial Milestones
- Progress bars with custom color coding
- Goal status indicators (Achieved, On Track, Needs Attention)
- Deadline tracking with urgency indicators
- Interactive AI advice integration

### Portfolio Dashboard
- Investment performance metrics
- Asset allocation visualization
- Gain/Loss tracking
- Transaction history

### Risk Assessment
- Interactive risk profiling questionnaire
- Investment style recommendations
- Asset allocation suggestions
- Professional financial guidance

## 🔒 Security Features

- Environment variable configuration
- SQL injection prevention with parameterized queries
- CORS configuration for API security
- Input validation with Pydantic models

## 📈 Performance

- Optimized database queries with indexing
- Efficient React component rendering
- Lazy loading for large datasets
- Responsive design for all devices

## 📱 Screenshots

### Dashboard View
- Premium Deep Navy & Emerald Green interface
- Financial milestones with progress tracking
- AI-powered recommendations panel

### Goal Tracking
- Color-coded progress bars
- Deadline management
- Interactive goal creation

### Portfolio Analysis
- Investment performance metrics
- Asset allocation charts
- Risk assessment tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please email thanmayims@example.com or create an issue in the repository.

## 🙏 Acknowledgments

- **Groq AI** for providing the powerful language model
- **FastAPI** for the excellent web framework
- **React** for the amazing UI library
- **Tailwind CSS** for the utility-first CSS framework

---

**Built with ❤️ for professional financial advisory services**

<div align="center">
  <p>🏦 Professional Investment Advisor Platform</p>
  <p>📊 AI-Powered • 🎯 Goal-Oriented • 💼 Portfolio Management</p>
</div>
