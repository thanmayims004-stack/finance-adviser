# Finance Tracker

A FastAPI backend with React frontend for tracking personal finances.

## Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/spending` - Get spending data by category
- `GET /api/spending/monthly` - Get monthly spending trends

## Database

The backend connects to a MySQL database named 'finance' with the following credentials:
- Host: localhost
- Port: 3306
- Database: finance
- User: thanmay
- Password: Thanmayi@123

Expected table structure:
```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    amount DECIMAL(10, 2),
    date DATE,
    description TEXT
);
```
