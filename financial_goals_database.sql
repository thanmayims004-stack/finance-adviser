-- ========================================
-- RIA Investment Advisor - Financial Goals Database
-- Complete SQL Schema for Financial Goals Management
-- ========================================

-- Drop existing tables to start fresh
DROP TABLE IF EXISTS goal_transactions;
DROP TABLE IF EXISTS goal_milestones;
DROP TABLE IF EXISTS goal_contributions;
DROP TABLE IF EXISTS financial_goals;
DROP TABLE IF EXISTS goal_categories;
DROP TABLE IF EXISTS goal_templates;

-- ========================================
-- 1. Goal Categories Table
-- ========================================
CREATE TABLE goal_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    priority_level INTEGER DEFAULT 1, -- 1=High, 2=Medium, 3=Low
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default goal categories
INSERT INTO goal_categories (category_name, description, icon, color, priority_level) VALUES
('Emergency', 'Emergency fund for unexpected expenses', 'shield', '#10b981', 1),
('Retirement', 'Long-term retirement savings', 'sun', '#3b82f6', 1),
('Housing', 'Home purchase or renovation', 'home', '#f59e0b', 2),
('Education', 'Education expenses for self or dependents', 'graduation-cap', '#8b5cf6', 2),
('Transport', 'Vehicle purchase or transportation', 'car', '#ef4444', 2),
('Lifestyle', 'Travel, hobbies, and lifestyle goals', 'plane', '#06b6d4', 3),
('Investment', 'Investment portfolio growth', 'trending-up', '#10b981', 1),
('Health', 'Medical expenses and wellness', 'heart', '#ec4899', 2),
('Debt', 'Debt repayment goals', 'credit-card', '#f97316', 1),
('Savings', 'General savings goals', 'piggy-bank', '#6b7280', 3);

-- ========================================
-- 2. Goal Templates Table
-- ========================================
CREATE TABLE goal_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name VARCHAR(100) NOT NULL,
    category_id INTEGER,
    description TEXT,
    suggested_target_amount DECIMAL(12,2),
    suggested_timeframe_months INTEGER,
    risk_level VARCHAR(20) DEFAULT 'Medium', -- Low, Medium, High
    age_group VARCHAR(50), -- Young Adult, Middle Age, Senior
    income_level VARCHAR(50), -- Low, Medium, High
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES goal_categories(id)
);

-- Insert goal templates
INSERT INTO goal_templates (template_name, category_id, description, suggested_target_amount, suggested_timeframe_months, risk_level, age_group, income_level) VALUES
('Emergency Fund', 1, '3-6 months of living expenses', 15000.00, 12, 'Low', 'All', 'All'),
('Retirement - Young Professional', 2, 'Start retirement savings early', 50000.00, 60, 'High', 'Young Adult', 'Medium'),
('Retirement - Mid Career', 2, 'Accelerate retirement savings', 200000.00, 120, 'Medium', 'Middle Age', 'High'),
('First Home Down Payment', 4, '20% down payment for first home', 80000.00, 36, 'Medium', 'All', 'Medium'),
('New Car', 5, 'Reliable vehicle purchase', 25000.00, 24, 'Low', 'All', 'Medium'),
('Children Education Fund', 3, 'College savings for children', 100000.00, 180, 'Medium', 'Middle Age', 'High'),
('Dream Vacation', 6, 'International travel experience', 15000.00, 18, 'Low', 'All', 'Medium'),
('Investment Portfolio Growth', 7, 'Diversified investment portfolio', 100000.00, 48, 'High', 'All', 'High'),
('Medical Emergency Fund', 8, 'Healthcare emergency savings', 10000.00, 24, 'Low', 'All', 'Medium'),
('Credit Card Debt Payoff', 9, 'Eliminate high-interest debt', 10000.00, 12, 'Low', 'All', 'All');

-- ========================================
-- 3. Financial Goals Table (Main Table)
-- ========================================
CREATE TABLE financial_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1, -- For future multi-user support
    goal_name VARCHAR(255) NOT NULL,
    category_id INTEGER,
    template_id INTEGER,
    target_amount DECIMAL(12,2) NOT NULL,
    current_amount DECIMAL(12,2) DEFAULT 0.00,
    monthly_contribution DECIMAL(10,2) DEFAULT 0.00,
    target_date DATE NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE,
    priority VARCHAR(20) DEFAULT 'Medium', -- High, Medium, Low
    status VARCHAR(20) DEFAULT 'Active', -- Active, Completed, Paused, Cancelled
    risk_tolerance VARCHAR(20) DEFAULT 'Medium', -- Low, Medium, High
    description TEXT,
    motivation TEXT, -- User's personal motivation
    auto_contribute BOOLEAN DEFAULT FALSE,
    contribution_frequency VARCHAR(20) DEFAULT 'Monthly', -- Weekly, Bi-weekly, Monthly, Quarterly
    reminder_frequency VARCHAR(20) DEFAULT 'Monthly', -- Daily, Weekly, Monthly, Quarterly
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (category_id) REFERENCES goal_categories(id),
    FOREIGN KEY (template_id) REFERENCES goal_templates(id),
    
    -- Constraints for data integrity
    CHECK (target_amount > 0),
    CHECK (current_amount >= 0),
    CHECK (monthly_contribution >= 0),
    CHECK (target_date > start_date),
    CHECK (priority IN ('High', 'Medium', 'Low')),
    CHECK (status IN ('Active', 'Completed', 'Paused', 'Cancelled')),
    CHECK (risk_tolerance IN ('Low', 'Medium', 'High')),
    CHECK (progress_percentage >= 0 AND progress_percentage <= 100)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_goals_user_id ON financial_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_goals_category_id ON financial_goals(category_id);
CREATE INDEX IF NOT EXISTS idx_goals_status ON financial_goals(status);
CREATE INDEX IF NOT EXISTS idx_goals_target_date ON financial_goals(target_date);
CREATE INDEX IF NOT EXISTS idx_goals_priority ON financial_goals(priority);
CREATE INDEX IF NOT EXISTS idx_goals_created_at ON financial_goals(created_at);

-- ========================================
-- 4. Goal Contributions Table
-- ========================================
CREATE TABLE goal_contributions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    contribution_date DATE DEFAULT CURRENT_DATE,
    contribution_type VARCHAR(50) DEFAULT 'Manual', -- Manual, Auto, Bonus, Refund
    description TEXT,
    transaction_reference VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (goal_id) REFERENCES financial_goals(id) ON DELETE CASCADE,
    CHECK (amount > 0)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_contributions_goal_id ON goal_contributions(goal_id);
CREATE INDEX IF NOT EXISTS idx_contributions_date ON goal_contributions(contribution_date);
CREATE INDEX IF NOT EXISTS idx_contributions_type ON goal_contributions(contribution_type);

-- ========================================
-- 5. Goal Milestones Table
-- ========================================
CREATE TABLE goal_milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    milestone_name VARCHAR(255) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    target_date DATE,
    achieved BOOLEAN DEFAULT FALSE,
    achieved_date DATE NULL,
    reward TEXT, -- Reward for achieving milestone
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (goal_id) REFERENCES financial_goals(id) ON DELETE CASCADE,
    CHECK (target_amount > 0)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_milestones_goal_id ON goal_milestones(goal_id);
CREATE INDEX IF NOT EXISTS idx_milestones_achieved ON goal_milestones(achieved);

-- ========================================
-- 6. Goal Transactions Table
-- ========================================
CREATE TABLE goal_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- Deposit, Withdrawal, Adjustment
    amount DECIMAL(10,2) NOT NULL,
    balance_before DECIMAL(12,2),
    balance_after DECIMAL(12,2),
    transaction_date DATE DEFAULT CURRENT_DATE,
    description TEXT,
    reference_id INTEGER, -- Reference to contribution or other transaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (goal_id) REFERENCES financial_goals(id) ON DELETE CASCADE,
    CHECK (amount != 0)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_transactions_goal_id ON goal_transactions(goal_id);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON goal_transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON goal_transactions(transaction_date);

-- ========================================
-- 7. Triggers for Automatic Updates
-- ========================================

-- Trigger to update progress percentage when current amount changes
CREATE TRIGGER update_goal_progress 
AFTER UPDATE OF current_amount ON financial_goals
BEGIN
    UPDATE financial_goals 
    SET progress_percentage = ROUND((current_amount / target_amount) * 100, 2),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
    
    -- Update status if goal is completed
    UPDATE financial_goals 
    SET status = 'Completed',
        completed_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id AND current_amount >= target_amount AND status != 'Completed';
END;

-- Trigger to create transaction record for contributions
CREATE TRIGGER log_contribution_transaction
AFTER INSERT ON goal_contributions
BEGIN
    -- Get current balance before update
    UPDATE financial_goals 
    SET current_amount = current_amount + NEW.amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.goal_id;
    
    -- Log the transaction
    INSERT INTO goal_transactions (goal_id, transaction_type, amount, balance_before, balance_after, description, reference_id)
    SELECT 
        NEW.goal_id,
        'Deposit',
        NEW.amount,
        (SELECT current_amount - NEW.amount FROM financial_goals WHERE id = NEW.goal_id),
        (SELECT current_amount FROM financial_goals WHERE id = NEW.goal_id),
        'Contribution: ' || COALESCE(NEW.description, 'Manual contribution'),
        NEW.id;
END;

-- ========================================
-- 8. Views for Common Queries
-- ========================================

-- View for goal summary with category information
CREATE VIEW IF NOT EXISTS goal_summary AS
SELECT 
    fg.id,
    fg.goal_name,
    fg.target_amount,
    fg.current_amount,
    fg.progress_percentage,
    fg.target_date,
    fg.start_date,
    fg.priority,
    fg.status,
    fg.monthly_contribution,
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
WHERE fg.status != 'Cancelled';

-- View for contribution history
CREATE VIEW IF NOT EXISTS contribution_history AS
SELECT 
    gc.id,
    gc.goal_id,
    gc.amount,
    gc.contribution_date,
    gc.contribution_type,
    gc.description,
    fg.goal_name,
    gc.category_name,
    gc.progress_percentage
FROM goal_contributions gc
JOIN financial_goals fg ON gc.goal_id = fg.id
LEFT JOIN goal_categories gc2 ON fg.category_id = gc2.id
ORDER BY gc.contribution_date DESC;

-- ========================================
-- 9. Sample Data Insertion
-- ========================================

-- Insert sample financial goals
INSERT INTO financial_goals (
    goal_name, category_id, target_amount, current_amount, 
    monthly_contribution, target_date, priority, status, 
    risk_tolerance, description, motivation
) VALUES
('Emergency Fund', 1, 50000.00, 35000.00, 2000.00, 
 date('now', '+6 months'), 'High', 'Active', 'Low',
 '6 months of living expenses for financial security',
 'Peace of mind knowing I can handle any emergency'),

('Retirement Fund', 2, 1000000.00, 75000.00, 1500.00, 
 date('now', '+25 years'), 'High', 'Active', 'Medium',
 'Long-term retirement savings for comfortable future',
 'Financial independence and freedom to choose'),

('New Car', 5, 45000.00, 9000.00, 1000.00, 
 date('now', '+3 years'), 'Medium', 'Active', 'Low',
 'Reliable vehicle for daily commute and family',
 'Safe and comfortable transportation for my family'),

('House Down Payment', 4, 200000.00, 35000.00, 2500.00, 
 date('now', '+5 years'), 'Medium', 'Active', 'Medium',
 '20% down payment for dream home',
 'Building equity and having a place to call home'),

('Children Education', 3, 150000.00, 15000.00, 800.00, 
 date('now', '+10 years'), 'Medium', 'Active', 'Medium',
 'College fund for children''s education',
 'Giving my children the best education opportunities'),

('Vacation Fund', 6, 12000.00, 2000.00, 500.00, 
 date('now', '+9 months'), 'Low', 'Active', 'Low',
 'Dream vacation to Europe',
 'Creating memories and experiencing new cultures'),

('Investment Portfolio', 7, 100000.00, 25000.00, 2000.00, 
 date('now', '+3 years'), 'High', 'Active', 'High',
 'Diversified investment portfolio for wealth growth',
 'Building long-term wealth and financial freedom');

-- Insert sample contributions
INSERT INTO goal_contributions (goal_id, amount, contribution_type, description) VALUES
(1, 2000.00, 'Manual', 'Monthly emergency fund contribution'),
(2, 1500.00, 'Auto', 'Automatic retirement contribution'),
(3, 1000.00, 'Manual', 'Car savings'),
(4, 2500.00, 'Manual', 'House down payment'),
(5, 800.00, 'Auto', 'Education fund'),
(6, 500.00, 'Manual', 'Vacation savings'),
(7, 2000.00, 'Manual', 'Investment contribution');

-- Insert sample milestones
INSERT INTO goal_milestones (goal_id, milestone_name, target_amount, target_date, reward) VALUES
(1, 'First $10,000', 10000.00, date('now', '-2 months'), 'Nice dinner celebration'),
(1, 'Halfway There', 25000.00, date('now', '-1 month'), 'Weekend getaway'),
(2, 'First $100K', 100000.00, date('now', '+2 years'), 'Investment course'),
(3, 'Down Payment Ready', 45000.00, date('now', '+3 years'), 'New car!'),
(4, 'First $50K', 50000.00, date('now', '+1 year'), 'Home shopping spree');

-- ========================================
-- 10. Database Initialization Complete
-- ========================================

-- Display summary
SELECT 'Financial Goals Database Initialized Successfully' as status;
SELECT COUNT(*) as total_categories FROM goal_categories;
SELECT COUNT(*) as total_templates FROM goal_templates;
SELECT COUNT(*) as total_goals FROM financial_goals;
SELECT COUNT(*) as total_contributions FROM goal_contributions;
SELECT COUNT(*) as total_milestones FROM goal_milestones;
