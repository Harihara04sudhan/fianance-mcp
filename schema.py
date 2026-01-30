"""
Database Schema Setup
=====================
SQL scripts to create tables in both private and public Neon databases.

Run these scripts manually in Neon Console or via psql.
"""

# ==========================================
# PRIVATE DATABASE SCHEMA (PII Data)
# ==========================================

PRIVATE_DB_SCHEMA = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Accounts table (bank accounts, credit cards, etc.)
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- checking, savings, credit, investment, loan
    balance DECIMAL(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    institution VARCHAR(255),
    account_number_masked VARCHAR(20), -- Last 4 digits only
    plaid_account_id VARCHAR(255), -- For Plaid integration
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    type VARCHAR(20) NOT NULL, -- debit, credit
    category VARCHAR(100),
    subcategory VARCHAR(100),
    merchant_name VARCHAR(255),
    description TEXT,
    transaction_date DATE NOT NULL,
    is_pending BOOLEAN DEFAULT false,
    plaid_transaction_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_merchant ON transactions(merchant_name);

-- Updated at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""


# ==========================================
# PUBLIC DATABASE SCHEMA (Analytics)
# ==========================================

PUBLIC_DB_SCHEMA = """
-- Spending analytics (aggregated, no PII)
CREATE TABLE IF NOT EXISTS spending_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- Reference only, no FK
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    type VARCHAR(20) NOT NULL, -- income, expense
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Monthly summary (pre-aggregated)
CREATE TABLE IF NOT EXISTS monthly_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    month VARCHAR(7) NOT NULL, -- YYYY-MM
    income DECIMAL(15, 2) DEFAULT 0.00,
    expenses DECIMAL(15, 2) DEFAULT 0.00,
    net DECIMAL(15, 2) DEFAULT 0.00,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, month)
);

-- Merchant analytics (aggregated spending by merchant)
CREATE TABLE IF NOT EXISTS merchant_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    merchant_name VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Budgets
CREATE TABLE IF NOT EXISTS budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    period VARCHAR(20) DEFAULT 'monthly', -- weekly, monthly, yearly
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alerts configuration
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- low_balance, large_transaction, budget_threshold
    threshold DECIMAL(15, 2),
    config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_spending_user_date ON spending_analytics(user_id, date);
CREATE INDEX IF NOT EXISTS idx_spending_category ON spending_analytics(category);
CREATE INDEX IF NOT EXISTS idx_monthly_user ON monthly_summary(user_id);
CREATE INDEX IF NOT EXISTS idx_merchant_user ON merchant_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_budgets_user ON budgets(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_user ON alerts(user_id);

-- Updated at trigger for budgets
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_budgets_updated_at BEFORE UPDATE ON budgets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""


def print_schemas():
    """Print schemas for manual execution."""
    print("=" * 60)
    print("PRIVATE DATABASE SCHEMA")
    print("Run this in your Neon Private Database")
    print("=" * 60)
    print(PRIVATE_DB_SCHEMA)
    print("\n" + "=" * 60)
    print("PUBLIC DATABASE SCHEMA")
    print("Run this in your Neon Public Database")
    print("=" * 60)
    print(PUBLIC_DB_SCHEMA)


if __name__ == "__main__":
    print_schemas()
