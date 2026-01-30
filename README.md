# Finance MCP Server - Vercel Deployment

This folder contains the Finance MCP Server configured for serverless deployment on Vercel.

## 📁 Structure

```
vercel-deployment/
├── api/
│   ├── index.py          # Main Vercel handler
│   ├── app_tools.py      # MCP tools registration
│   └── database.py       # Database connection manager
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## 🚀 Quick Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Set Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
DATABASE_URL_PRIVATE="postgresql://user:pass@host/private?sslmode=require"
DATABASE_URL_PUBLIC="postgresql://user:pass@host/public?sslmode=require"
```

### 3. Deploy to Vercel

```bash
cd vercel-deployment
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N** (for first deployment)
- What's your project's name? **finance-mcp-server**
- In which directory is your code located? **./**
- Want to override settings? **N**

### 4. Add Environment Variables to Vercel

After deployment, add your secrets:

```bash
# Add private database URL
vercel env add DATABASE_URL_PRIVATE

# Add public database URL
vercel env add DATABASE_URL_PUBLIC
```

Or add them via Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add `DATABASE_URL_PRIVATE` and `DATABASE_URL_PUBLIC`
4. Redeploy: `vercel --prod`

## 🔧 Configuration

### vercel.json

The `vercel.json` file configures:
- **Python runtime** for serverless functions
- **Routing** to handle MCP endpoints
- **Environment variables** references

### Production Deployment

```bash
vercel --prod
```

Your MCP server will be available at:
```
https://your-project.vercel.app/mcp
```

## 📡 API Endpoints

Once deployed, your MCP server will be accessible at:

- **Main MCP endpoint**: `https://your-project.vercel.app/mcp`
- **Health check**: `https://your-project.vercel.app/`

## 🔐 Security

1. **Never commit `.env` file** - it's already in `.gitignore`
2. **Use Vercel environment variables** for production secrets
3. **Enable SSL** - Vercel provides automatic HTTPS
4. **Database SSL** - Ensure Neon databases use `?sslmode=require`

## 🧪 Testing

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python api/index.py
```

Server runs at `http://localhost:8080`

### Test MCP Endpoint

```bash
curl https://your-project.vercel.app/mcp
```

## 📊 Features

All 19 financial tools are available:

### Account Management
- `list_accounts` - View all accounts
- `get_account_balance` - Get specific account balance
- `get_account_summary` - Complete financial summary

### Transaction Analysis
- `list_transactions` - List with filters
- `search_transactions` - Search by merchant
- `get_recurring_transactions` - Detect recurring payments

### Analytics
- `get_spending_by_category` - Category breakdown
- `get_monthly_trends` - Income/expense trends
- `get_top_merchants` - Top spending merchants
- `get_cashflow_summary` - Income vs expenses

### Budgeting
- `create_budget` - Create new budget
- `list_budgets` - View all budgets
- `get_budget_status` - Budget vs actual spending

### Utilities
- `get_available_categories` - List categories
- `format_currency` - Format amounts
- `calculate_net_worth` - Calculate net worth

### Security & Policies
- `get_tool_policy` - Get tool access policy
- `list_tool_policies` - List all policies
- `validate_tool_access` - Validate permissions

## 🔄 Updates

To update the deployment:

```bash
# Pull latest changes
git pull

# Navigate to vercel-deployment folder
cd vercel-deployment

# Redeploy
vercel --prod
```

## 📝 Logs

View logs in real-time:

```bash
vercel logs
```

Or view in Vercel Dashboard under your project's "Logs" section.

## 🐛 Troubleshooting

### Import Errors
Make sure all Python files are in the `api/` directory and dependencies are in `requirements.txt`.

### Database Connection Issues
- Verify environment variables are set correctly in Vercel
- Check database URLs include `?sslmode=require`
- Ensure Neon databases are accessible

### 500 Server Errors
Check Vercel logs: `vercel logs` or in the dashboard

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Neon PostgreSQL](https://neon.tech/docs)

## 📞 Support

For issues or questions:
1. Check Vercel logs
2. Review environment variables
3. Test database connections
4. Verify Python dependencies

---

**Ready to deploy!** 🚀
