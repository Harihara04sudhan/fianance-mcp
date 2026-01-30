"""
Database Connection Manager
===========================
Manages connections to both private and public Neon PostgreSQL databases.

Private DB: Contains PII - users, accounts, transactions
Public DB: Contains aggregated analytics, non-sensitive data
"""

import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    """Manages connections to private and public databases."""
    
    def __init__(self):
        self.private_url = os.getenv("DATABASE_URL_PRIVATE")
        self.public_url = os.getenv("DATABASE_URL_PUBLIC")
        
        if not self.private_url:
            raise ValueError("DATABASE_URL_PRIVATE environment variable is required")
        if not self.public_url:
            raise ValueError("DATABASE_URL_PUBLIC environment variable is required")
    
    @contextmanager
    def get_private_connection(self):
        """Get a connection to the private database (PII data)."""
        conn = None
        try:
            conn = psycopg2.connect(self.private_url, cursor_factory=RealDictCursor)
            yield conn
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_public_connection(self):
        """Get a connection to the public database (analytics)."""
        conn = None
        try:
            conn = psycopg2.connect(self.public_url, cursor_factory=RealDictCursor)
            yield conn
        finally:
            if conn:
                conn.close()
    
    # ==========================================
    # PRIVATE DB OPERATIONS (PII Data)
    # ==========================================
    
    def get_user_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all accounts for a user from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, type, "currentBalance" as balance, currency, 
                           provider as institution, mask as account_number_masked, 
                           status, "createdAt" as created_at, "updatedAt" as updated_at
                    FROM accounts 
                    WHERE "userId" = %s AND status = 'ACTIVE'
                    ORDER BY type, name
                """, (user_id,))
                return [dict(row) for row in cur.fetchall()]
    
    def get_account_by_id(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific account by ID from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, "userId" as user_id, name, type, 
                           "currentBalance" as balance, currency, 
                           provider as institution, mask as account_number_masked, 
                           status, "createdAt" as created_at, "updatedAt" as updated_at
                    FROM accounts 
                    WHERE id = %s
                """, (account_id,))
                row = cur.fetchone()
                return dict(row) if row else None
    
    def get_transactions(
        self, 
        user_id: str, 
        account_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get transactions with filters from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT t.id, t."accountId" as account_id, t.amount, t.currency,
                           CASE WHEN t.amount < 0 THEN 'debit' ELSE 'credit' END as type,
                           t.category, t.subcategory, t."merchantName" as merchant_name, 
                           t.name as description, t.date as transaction_date, t.pending as is_pending,
                           t."createdAt" as created_at
                    FROM transactions t
                    JOIN accounts a ON t."accountId" = a.id
                    WHERE a."userId" = %s
                """
                params = [user_id]
                
                if account_id:
                    query += " AND t.\"accountId\" = %s"
                    params.append(account_id)
                
                if start_date:
                    query += " AND t.date >= %s"
                    params.append(start_date)
                
                if end_date:
                    query += " AND t.date <= %s"
                    params.append(end_date)
                
                if category:
                    query += " AND t.category = %s"
                    params.append(category)
                
                query += " ORDER BY t.date DESC LIMIT %s"
                params.append(limit)
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def search_transactions(
        self, 
        user_id: str, 
        query: str, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search transactions by merchant or description from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                search_pattern = f"%{query}%"
                cur.execute("""
                    SELECT t.id, t."accountId" as account_id, t.amount, t.currency,
                           CASE WHEN t.amount < 0 THEN 'debit' ELSE 'credit' END as type,
                           t.category, t."merchantName" as merchant_name, 
                           t.name as description, t.date as transaction_date
                    FROM transactions t
                    JOIN accounts a ON t."accountId" = a.id
                    WHERE a."userId" = %s 
                      AND (t."merchantName" ILIKE %s OR t.name ILIKE %s)
                    ORDER BY t.date DESC
                    LIMIT %s
                """, (user_id, search_pattern, search_pattern, limit))
                return [dict(row) for row in cur.fetchall()]
    
    def get_account_summary(self, user_id: str) -> Dict[str, Any]:
        """Get account summary with totals from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        type,
                        SUM(CASE WHEN "currentBalance" >= 0 THEN "currentBalance" ELSE 0 END) as assets,
                        SUM(CASE WHEN "currentBalance" < 0 THEN ABS("currentBalance") ELSE 0 END) as liabilities,
                        COUNT(*) as count
                    FROM accounts
                    WHERE "userId" = %s AND status = 'ACTIVE'
                    GROUP BY type
                """, (user_id,))
                
                summary = {
                    "total_assets": 0.0,
                    "total_liabilities": 0.0,
                    "by_type": {}
                }
                
                for row in cur.fetchall():
                    row_dict = dict(row)
                    summary["by_type"][str(row_dict["type"])] = {
                        "assets": float(row_dict["assets"] or 0),
                        "liabilities": float(row_dict["liabilities"] or 0),
                        "count": row_dict["count"]
                    }
                    summary["total_assets"] += float(row_dict["assets"] or 0)
                    summary["total_liabilities"] += float(row_dict["liabilities"] or 0)
                
                summary["net_worth"] = summary["total_assets"] - summary["total_liabilities"]
                return summary
    
    def get_recurring_transactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Detect recurring transactions from private DB."""
        with self.get_private_connection() as conn:
            with conn.cursor() as cur:
                # Find transactions that appear regularly with similar amounts
                cur.execute("""
                    WITH transaction_patterns AS (
                        SELECT 
                            t."merchantName" as merchant_name,
                            t.category,
                            ROUND(AVG(t.amount)::numeric, 2) as avg_amount,
                            COUNT(*) as occurrence_count,
                            MAX(t.date) as last_date,
                            MIN(t.date) as first_date
                        FROM transactions t
                        JOIN accounts a ON t."accountId" = a.id
                        WHERE a."userId" = %s
                          AND t.date >= CURRENT_DATE - INTERVAL '90 days'
                          AND t.amount < 0
                        GROUP BY t."merchantName", t.category
                        HAVING COUNT(*) >= 2
                    )
                    SELECT * FROM transaction_patterns
                    WHERE occurrence_count >= 2
                    ORDER BY occurrence_count DESC, avg_amount DESC
                """, (user_id,))
                return [dict(row) for row in cur.fetchall()]
    
    # ==========================================
    # PUBLIC DB OPERATIONS (Analytics)
    # ==========================================
    
    def get_spending_by_category(
        self, 
        user_id: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get spending breakdown by category from public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT 
                        category,
                        SUM(amount) as total_amount,
                        COUNT(*) as transaction_count,
                        ROUND(AVG(amount)::numeric, 2) as avg_amount
                    FROM spending_analytics
                    WHERE user_id = %s
                """
                params = [user_id]
                
                if start_date:
                    query += " AND date >= %s"
                    params.append(start_date)
                
                if end_date:
                    query += " AND date <= %s"
                    params.append(end_date)
                
                query += " GROUP BY category ORDER BY total_amount DESC"
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def get_monthly_trends(self, user_id: str, months: int = 6) -> List[Dict[str, Any]]:
        """Get monthly income/expense trends from public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        month,
                        income,
                        expenses,
                        net
                    FROM monthly_summary
                    WHERE user_id = %s
                      AND date >= CURRENT_DATE - INTERVAL '%s months'
                    ORDER BY month DESC
                """, (user_id, months))
                
                results = []
                for row in cur.fetchall():
                    row_dict = dict(row)
                    row_dict["income"] = float(row_dict.get("income") or 0)
                    row_dict["expenses"] = float(row_dict.get("expenses") or 0)
                    row_dict["net"] = float(row_dict.get("net") or 0)
                    results.append(row_dict)
                return results
    
    def get_top_merchants(
        self, 
        user_id: str, 
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get top merchants by spending from public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT 
                        merchant_name,
                        SUM(amount) as total_spent,
                        COUNT(*) as transaction_count,
                        MAX(date) as last_transaction
                    FROM merchant_analytics
                    WHERE user_id = %s
                """
                params = [user_id]
                
                if start_date:
                    query += " AND date >= %s"
                    params.append(start_date)
                
                if end_date:
                    query += " AND date <= %s"
                    params.append(end_date)
                
                query += " GROUP BY merchant_name ORDER BY total_spent DESC LIMIT %s"
                params.append(limit)
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def save_budget(
        self, 
        user_id: str, 
        name: str, 
        category: str, 
        amount: float, 
        period: str
    ) -> Dict[str, Any]:
        """Save a budget to public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO budgets (user_id, name, category, amount, period, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                    RETURNING id, user_id, name, category, amount, period, created_at
                """, (user_id, name, category, amount, period))
                conn.commit()
                row = cur.fetchone()
                return dict(row) if row else {}
    
    def get_budgets(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all budgets for a user from public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, category, amount, period, created_at
                    FROM budgets
                    WHERE user_id = %s AND is_active = true
                    ORDER BY category
                """, (user_id,))
                return [dict(row) for row in cur.fetchall()]
    
    def get_budget_status(self, user_id: str) -> List[Dict[str, Any]]:
        """Get budget status with current spending from public DB."""
        with self.get_public_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        b.id,
                        b.name,
                        b.category,
                        b.amount as budget_limit,
                        b.period,
                        COALESCE(s.spent, 0) as spent,
                        b.amount - COALESCE(s.spent, 0) as remaining,
                        ROUND((COALESCE(s.spent, 0) / b.amount * 100)::numeric, 1) as percentage
                    FROM budgets b
                    LEFT JOIN (
                        SELECT category, SUM(amount) as spent
                        FROM spending_analytics
                        WHERE user_id = %s
                          AND date >= DATE_TRUNC('month', CURRENT_DATE)
                        GROUP BY category
                    ) s ON b.category = s.category
                    WHERE b.user_id = %s AND b.is_active = true
                    ORDER BY percentage DESC NULLS LAST
                """, (user_id, user_id))
                return [dict(row) for row in cur.fetchall()]


# Global database manager instance
db = DatabaseManager()
