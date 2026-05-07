-- Finance Database Setup Script
-- Run this script in your MySQL database to create the necessary tables

CREATE DATABASE IF NOT EXISTS finance;
USE finance;

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for testing
INSERT INTO transactions (category, amount, date, description) VALUES
('Food', -45.50, '2024-01-15', 'Grocery shopping'),
('Transport', -25.00, '2024-01-16', 'Gas'),
('Entertainment', -60.00, '2024-01-17', 'Movie tickets'),
('Food', -120.00, '2024-01-18', 'Restaurant dinner'),
('Shopping', -85.00, '2024-01-19', 'Clothing'),
('Bills', -200.00, '2024-01-20', 'Electricity bill'),
('Food', -35.00, '2024-01-21', 'Coffee and snacks'),
('Transport', -40.00, '2024-01-22', 'Uber rides'),
('Entertainment', -30.00, '2024-01-23', 'Streaming services'),
('Food', -95.00, '2024-01-24', 'Grocery shopping'),
('Healthcare', -150.00, '2024-01-25', 'Doctor visit'),
('Shopping', -220.00, '2024-01-26', 'Electronics'),
('Food', -55.00, '2024-01-27', 'Restaurant lunch'),
('Transport', -30.00, '2024-01-28', 'Public transport'),
('Entertainment', -75.00, '2024-01-29', 'Concert tickets'),
('Bills', -300.00, '2024-01-30', 'Rent'),
('Food', -40.00, '2024-01-31', 'Groceries'),
('Shopping', -110.00, '2024-02-01', 'Home supplies'),
('Transport', -50.00, '2024-02-02', 'Gas'),
('Food', -80.00, '2024-02-03', 'Restaurant dinner');

-- Add some income transactions (positive amounts)
INSERT INTO transactions (category, amount, date, description) VALUES
('Salary', 3000.00, '2024-01-01', 'Monthly salary'),
('Freelance', 500.00, '2024-01-15', 'Freelance project'),
('Investment', 150.00, '2024-01-20', 'Dividend payment'),
('Salary', 3000.00, '2024-02-01', 'Monthly salary');

-- Create indexes for better performance
CREATE INDEX idx_category ON transactions(category);
CREATE INDEX idx_date ON transactions(date);
CREATE INDEX idx_amount ON transactions(amount);
