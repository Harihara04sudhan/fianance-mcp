"""
Finance MCP Tools
=================
Financial tools exposed via MCP protocol for AI agents.
Connected to Neon PostgreSQL (Private + Public databases).

Tools include:
- Account management (list, balance, summary)
- Transaction analysis (list, search, categorize)
- Analytics (spending, trends, forecasting)
- Budgeting (create, track, alerts)

Database Classification:
- PRIVATE DB: Contains PII - users, accounts, transactions (HIGH sensitivity)
- PUBLIC DB: Contains aggregated analytics, non-sensitive data (MEDIUM sensitivity)
"""

from typing import Optional
from datetime import datetime
from database import db


# ==========================================
# TOOL CLASSIFICATION & ACCESS CONTROL
# ==========================================
# This defines which database each tool accesses and required scopes

TOOL_CLASSIFICATION = {
    # Private DB Tools (PII - HIGH sensitivity)
    "list_accounts": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Access user account list with balances"
    },
    "get_account_balance": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Access specific account balance"
    },
    "get_account_summary": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Access complete financial summary"
    },
    "list_transactions": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Access transaction history"
    },
    "search_transactions": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Search transaction data"
    },
    "get_recurring_transactions": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Detect recurring payment patterns"
    },
    "calculate_net_worth": {
        "database": "private",
        "scope": "read:private",
        "sensitivity": "HIGH",
        "requires_auth": True,
        "audit_log": True,
        "description": "Calculate total net worth"
    },
    
    # Public DB Tools (Analytics - MEDIUM sensitivity)
    "get_spending_by_category": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "MEDIUM",
        "requires_auth": True,
        "audit_log": False,
        "description": "Aggregated category spending"
    },
    "get_monthly_trends": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "MEDIUM",
        "requires_auth": True,
        "audit_log": False,
        "description": "Monthly income/expense trends"
    },
    "get_top_merchants": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "MEDIUM",
        "requires_auth": True,
        "audit_log": False,
        "description": "Top merchants by spending"
    },
    "get_cashflow_summary": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "MEDIUM",
        "requires_auth": True,
        "audit_log": False,
        "description": "Income vs expenses summary"
    },
    "create_budget": {
        "database": "public",
        "scope": "write:public",
        "sensitivity": "MEDIUM",
        "requires_auth": True,
        "audit_log": True,
        "description": "Create budget entry"
    },
    "list_budgets": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "LOW",
        "requires_auth": True,
        "audit_log": False,
        "description": "List user budgets"
    },
    "get_budget_status": {
        "database": "public",
        "scope": "read:public",
        "sensitivity": "LOW",
        "requires_auth": True,
        "audit_log": False,
        "description": "Budget vs actual spending"
    },
    
    # Utility Tools (No DB - No sensitivity)
    "get_available_categories": {
        "database": None,
        "scope": None,
        "sensitivity": "NONE",
        "requires_auth": False,
        "audit_log": False,
        "description": "Static category list"
    },
    "format_currency": {
        "database": None,
        "scope": None,
        "sensitivity": "NONE",
        "requires_auth": False,
        "audit_log": False,
        "description": "Format currency amounts"
    },
}


def get_tool_classification(tool_name: str) -> dict:
    """Get classification metadata for a specific tool."""
    return TOOL_CLASSIFICATION.get(tool_name, {
        "database": None,
        "scope": None,
        "sensitivity": "UNKNOWN",
        "requires_auth": True,
        "audit_log": True,
        "description": "Unknown tool"
    })


def get_tools_by_database(database: str) -> list:
    """Get list of tools that access a specific database."""
    return [
        name for name, config in TOOL_CLASSIFICATION.items()
        if config.get("database") == database
    ]


def get_tools_by_scope(scope: str) -> list:
    """Get list of tools that require a specific scope."""
    return [
        name for name, config in TOOL_CLASSIFICATION.items()
        if config.get("scope") == scope
    ]


def register_finance_tools(app):
    """Register all financial tools with the MCP app"""

    # ==========================================
    # ACCOUNT TOOLS (Private DB)
    # ==========================================

    @app.tool()
    def list_accounts(user_id: str) -> dict:
        """
        List all financial accounts for a user.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"accounts": [list of account objects]}
            On error: {"error": <error message>}
        """
        try:
            accounts = db.get_user_accounts(user_id)
            return {
                "accounts": accounts,
                "total": len(accounts)
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_account_balance(account_id: str) -> dict:
        """
        Get the current balance of a specific account.
        
        Args:
            account_id: The unique identifier of the account.
            
        Returns:
            On success: {"account_id": str, "balance": float, "currency": str, "as_of": datetime}
            On error: {"error": <error message>}
        """
        try:
            account = db.get_account_by_id(account_id)
            if not account:
                return {"error": "Account not found"}
            
            return {
                "account_id": account_id,
                "name": account.get("name"),
                "balance": float(account.get("balance", 0)),
                "currency": account.get("currency", "USD"),
                "type": account.get("type"),
                "as_of": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_account_summary(user_id: str) -> dict:
        """
        Get a summary of all accounts including total assets, liabilities, and net worth.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"total_assets": float, "total_liabilities": float, "net_worth": float, "by_type": dict}
            On error: {"error": <error message>}
        """
        try:
            summary = db.get_account_summary(user_id)
            summary["currency"] = "USD"
            summary["as_of"] = datetime.now().isoformat()
            return summary
        except Exception as e:
            return {"error": str(e)}

    # ==========================================
    # TRANSACTION TOOLS (Private DB)
    # ==========================================

    @app.tool()
    def list_transactions(
        user_id: str,
        account_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> dict:
        """
        List transactions with optional filters.
        
        Args:
            user_id: The unique identifier of the user.
            account_id: Optional account to filter by.
            start_date: Optional start date (ISO format: YYYY-MM-DD).
            end_date: Optional end date (ISO format: YYYY-MM-DD).
            category: Optional category to filter by.
            limit: Maximum number of transactions to return (default 50).
            
        Returns:
            On success: {"transactions": [list of transaction objects], "total": int}
            On error: {"error": <error message>}
        """
        try:
            transactions = db.get_transactions(
                user_id=user_id,
                account_id=account_id,
                start_date=start_date,
                end_date=end_date,
                category=category,
                limit=limit
            )
            return {
                "transactions": transactions,
                "total": len(transactions),
                "filters": {
                    "account_id": account_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "category": category,
                    "limit": limit
                }
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def search_transactions(
        user_id: str,
        query: str,
        limit: int = 20
    ) -> dict:
        """
        Search transactions by merchant name or description.
        
        Args:
            user_id: The unique identifier of the user.
            query: Search query string.
            limit: Maximum number of results (default 20).
            
        Returns:
            On success: {"transactions": [list of matching transactions], "query": str}
            On error: {"error": <error message>}
        """
        try:
            transactions = db.search_transactions(user_id, query, limit)
            return {
                "transactions": transactions,
                "query": query,
                "total": len(transactions)
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_recurring_transactions(user_id: str) -> dict:
        """
        Detect recurring transactions (subscriptions, bills, regular payments).
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"recurring": [list of recurring transaction patterns]}
            On error: {"error": <error message>}
        """
        try:
            recurring = db.get_recurring_transactions(user_id)
            
            # Categorize into subscriptions, bills, income
            subscriptions = [r for r in recurring if r.get("category") in ["Subscriptions", "Entertainment", "Software"]]
            bills = [r for r in recurring if r.get("category") in ["Utilities", "Housing", "Insurance"]]
            income = [r for r in recurring if float(r.get("avg_amount", 0)) > 0]
            
            total_monthly = sum(float(r.get("avg_amount", 0)) for r in recurring if float(r.get("avg_amount", 0)) < 0)
            
            return {
                "recurring": recurring,
                "subscriptions": subscriptions,
                "bills": bills,
                "income_patterns": income,
                "total_monthly_recurring": abs(total_monthly)
            }
        except Exception as e:
            return {"error": str(e)}

    # ==========================================
    # ANALYTICS TOOLS (Public DB)
    # ==========================================

    @app.tool()
    def get_spending_by_category(
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """
        Get spending breakdown by category for a date range.
        
        Args:
            user_id: The unique identifier of the user.
            start_date: Start date (ISO format). Defaults to 30 days ago.
            end_date: End date (ISO format). Defaults to today.
            
        Returns:
            On success: {"categories": [{"category": str, "total_amount": float, "count": int}], "total": float}
            On error: {"error": <error message>}
        """
        try:
            categories = db.get_spending_by_category(user_id, start_date, end_date)
            total_spending = sum(float(c.get("total_amount", 0)) for c in categories)
            
            # Add percentage to each category
            for cat in categories:
                amount = float(cat.get("total_amount", 0))
                cat["percentage"] = round((amount / total_spending * 100) if total_spending > 0 else 0, 1)
            
            return {
                "categories": categories,
                "total_spending": total_spending,
                "period": {
                    "start": start_date,
                    "end": end_date
                },
                "currency": "USD"
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_monthly_trends(
        user_id: str,
        months: int = 6
    ) -> dict:
        """
        Get monthly income and expense trends.
        
        Args:
            user_id: The unique identifier of the user.
            months: Number of months to analyze (default 6).
            
        Returns:
            On success: {"months": [{"month": str, "income": float, "expenses": float, "net": float}]}
            On error: {"error": <error message>}
        """
        try:
            trends = db.get_monthly_trends(user_id, months)
            
            # Calculate averages
            if trends:
                avg_income = sum(float(t.get("income", 0)) for t in trends) / len(trends)
                avg_expenses = sum(float(t.get("expenses", 0)) for t in trends) / len(trends)
                avg_net = sum(float(t.get("net", 0)) for t in trends) / len(trends)
            else:
                avg_income = avg_expenses = avg_net = 0.0
            
            return {
                "months": trends,
                "average_income": round(avg_income, 2),
                "average_expenses": round(avg_expenses, 2),
                "average_net": round(avg_net, 2),
                "currency": "USD"
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_top_merchants(
        user_id: str,
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """
        Get top merchants by spending amount.
        
        Args:
            user_id: The unique identifier of the user.
            limit: Number of top merchants to return (default 10).
            start_date: Optional start date filter.
            end_date: Optional end date filter.
            
        Returns:
            On success: {"merchants": [{"merchant_name": str, "total_spent": float, "count": int}]}
            On error: {"error": <error message>}
        """
        try:
            merchants = db.get_top_merchants(user_id, limit, start_date, end_date)
            return {
                "merchants": merchants,
                "period": {
                    "start": start_date,
                    "end": end_date
                },
                "currency": "USD"
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def calculate_net_worth(user_id: str) -> dict:
        """
        Calculate the user's current net worth.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"assets": float, "liabilities": float, "net_worth": float, "breakdown": dict}
            On error: {"error": <error message>}
        """
        try:
            summary = db.get_account_summary(user_id)
            return {
                "assets": summary.get("total_assets", 0),
                "liabilities": summary.get("total_liabilities", 0),
                "net_worth": summary.get("net_worth", 0),
                "breakdown": summary.get("by_type", {}),
                "currency": "USD",
                "as_of": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    # ==========================================
    # BUDGET TOOLS (Public DB)
    # ==========================================

    @app.tool()
    def create_budget(
        user_id: str,
        name: str,
        category: str,
        amount: float,
        period: str = "monthly"
    ) -> dict:
        """
        Create a new budget for a category.
        
        Args:
            user_id: The unique identifier of the user.
            name: Name for the budget.
            category: Spending category to track.
            amount: Budget amount limit.
            period: Budget period - "weekly", "monthly", "yearly" (default monthly).
            
        Returns:
            On success: {"budget_id": str, "created": bool}
            On error: {"error": <error message>}
        """
        try:
            budget = db.save_budget(user_id, name, category, amount, period)
            return {
                "budget_id": str(budget.get("id")),
                "name": name,
                "category": category,
                "amount": amount,
                "period": period,
                "created": True
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_budget_status(user_id: str) -> dict:
        """
        Get status of all budgets including spending vs limits.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"budgets": [{"name": str, "limit": float, "spent": float, "remaining": float, "percentage": float}]}
            On error: {"error": <error message>}
        """
        try:
            budgets = db.get_budget_status(user_id)
            
            total_budgeted = sum(float(b.get("budget_limit", 0)) for b in budgets)
            total_spent = sum(float(b.get("spent", 0)) for b in budgets)
            
            return {
                "budgets": budgets,
                "total_budgeted": total_budgeted,
                "total_spent": total_spent,
                "total_remaining": total_budgeted - total_spent,
                "overall_percentage": round((total_spent / total_budgeted * 100) if total_budgeted > 0 else 0, 1)
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def list_budgets(user_id: str) -> dict:
        """
        List all budgets for a user.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            On success: {"budgets": [list of budget objects]}
            On error: {"error": <error message>}
        """
        try:
            budgets = db.get_budgets(user_id)
            return {
                "budgets": budgets,
                "total": len(budgets)
            }
        except Exception as e:
            return {"error": str(e)}

    # ==========================================
    # UTILITY TOOLS
    # ==========================================

    @app.tool()
    def get_available_categories() -> dict:
        """
        Get list of available transaction categories.
        
        Returns:
            On success: {"categories": [list of category names]}
            On error: {"error": <error message>}
        """
        try:
            return {
                "categories": [
                    "Income",
                    "Housing",
                    "Utilities",
                    "Food & Dining",
                    "Groceries",
                    "Transportation",
                    "Shopping",
                    "Entertainment",
                    "Health & Fitness",
                    "Travel",
                    "Education",
                    "Personal Care",
                    "Gifts & Donations",
                    "Bills & Subscriptions",
                    "Insurance",
                    "Taxes",
                    "Investment",
                    "Transfer",
                    "Other"
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def format_currency(
        amount: float,
        currency: str = "USD"
    ) -> dict:
        """
        Format an amount as currency string.
        
        Args:
            amount: The numeric amount.
            currency: Currency code (default USD).
            
        Returns:
            On success: {"formatted": str}
            On error: {"error": <error message>}
        """
        try:
            currency_symbols = {
                "USD": "$",
                "EUR": "€",
                "GBP": "£",
                "INR": "₹",
                "JPY": "¥",
                "SGD": "S$"
            }
            symbol = currency_symbols.get(currency, currency + " ")
            formatted = f"{symbol}{amount:,.2f}"
            return {"formatted": formatted}
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def get_cashflow_summary(
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """
        Get income vs expenses summary for a period.
        
        Args:
            user_id: The unique identifier of the user.
            start_date: Start date (ISO format).
            end_date: End date (ISO format).
            
        Returns:
            On success: {"income": float, "expenses": float, "net": float, "savings_rate": float}
            On error: {"error": <error message>}
        """
        try:
            categories = db.get_spending_by_category(user_id, start_date, end_date)
            
            income = 0.0
            expenses = 0.0
            
            for cat in categories:
                amount = float(cat.get("total_amount", 0))
                if cat.get("category") == "Income":
                    income += amount
                else:
                    expenses += amount
            
            net = income - expenses
            savings_rate = (net / income * 100) if income > 0 else 0
            
            return {
                "income": income,
                "expenses": expenses,
                "net": net,
                "savings_rate": round(savings_rate, 1),
                "period": {
                    "start": start_date,
                    "end": end_date
                },
                "currency": "USD"
            }
        except Exception as e:
            return {"error": str(e)}

    # ==========================================
    # POLICY & CLASSIFICATION TOOLS
    # ==========================================

    @app.tool()
    def get_tool_policy(tool_name: str) -> dict:
        """
        Get access policy and classification for a specific tool.
        Used by agents to validate access before calling sensitive tools.
        
        Args:
            tool_name: Name of the tool to check policy for.
            
        Returns:
            On success: {"tool": str, "policy": dict with database, scope, sensitivity, requires_auth, audit_log}
            On error: {"error": <error message>}
        """
        try:
            policy = get_tool_classification(tool_name)
            return {
                "tool": tool_name,
                "policy": policy,
                "exists": tool_name in TOOL_CLASSIFICATION
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def list_tool_policies() -> dict:
        """
        List all tools with their access policies and classifications.
        Used by agents to understand what permissions are needed.
        
        Returns:
            On success: {
                "tools": dict of all tool classifications,
                "by_database": {"private": [...], "public": [...], "none": [...]},
                "by_sensitivity": {"HIGH": [...], "MEDIUM": [...], "LOW": [...], "NONE": [...]}
            }
            On error: {"error": <error message>}
        """
        try:
            by_database = {
                "private": get_tools_by_database("private"),
                "public": get_tools_by_database("public"),
                "none": get_tools_by_database(None)
            }
            
            by_sensitivity = {
                "HIGH": [n for n, c in TOOL_CLASSIFICATION.items() if c.get("sensitivity") == "HIGH"],
                "MEDIUM": [n for n, c in TOOL_CLASSIFICATION.items() if c.get("sensitivity") == "MEDIUM"],
                "LOW": [n for n, c in TOOL_CLASSIFICATION.items() if c.get("sensitivity") == "LOW"],
                "NONE": [n for n, c in TOOL_CLASSIFICATION.items() if c.get("sensitivity") == "NONE"]
            }
            
            by_scope = {
                "read:private": get_tools_by_scope("read:private"),
                "read:public": get_tools_by_scope("read:public"),
                "write:public": get_tools_by_scope("write:public"),
                "no_scope": get_tools_by_scope(None)
            }
            
            return {
                "tools": TOOL_CLASSIFICATION,
                "by_database": by_database,
                "by_sensitivity": by_sensitivity,
                "by_scope": by_scope,
                "total_count": len(TOOL_CLASSIFICATION)
            }
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    def validate_tool_access(
        tool_name: str,
        user_scopes: list[str]
    ) -> dict:
        """
        Validate if a user has permission to call a specific tool.
        
        Args:
            tool_name: Name of the tool to validate access for.
            user_scopes: List of scopes the user has been granted.
            
        Returns:
            On success: {"allowed": bool, "reason": str, "required_scope": str}
            On error: {"error": <error message>}
        """
        try:
            if tool_name not in TOOL_CLASSIFICATION:
                return {
                    "allowed": False,
                    "reason": f"Tool '{tool_name}' not found",
                    "required_scope": None
                }
            
            policy = TOOL_CLASSIFICATION[tool_name]
            required_scope = policy.get("scope")
            
            # Utility tools with no scope requirement
            if required_scope is None:
                return {
                    "allowed": True,
                    "reason": "No scope required",
                    "required_scope": None
                }
            
            # Check if user has required scope
            if required_scope in user_scopes:
                return {
                    "allowed": True,
                    "reason": f"User has required scope '{required_scope}'",
                    "required_scope": required_scope
                }
            
            # Check for wildcard scopes
            scope_parts = required_scope.split(":")
            if len(scope_parts) == 2:
                action, database = scope_parts
                wildcard_scope = f"{action}:*"
                all_scope = "*:*"
                
                if wildcard_scope in user_scopes or all_scope in user_scopes:
                    return {
                        "allowed": True,
                        "reason": f"User has wildcard scope for '{required_scope}'",
                        "required_scope": required_scope
                    }
            
            return {
                "allowed": False,
                "reason": f"Missing required scope '{required_scope}'",
                "required_scope": required_scope
            }
        except Exception as e:
            return {"error": str(e)}
