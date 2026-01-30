# 🚀 QUICK START - Deploy to Vercel in 5 Minutes

## Prerequisites
- Node.js installed (for Vercel CLI)
- Neon PostgreSQL databases (private & public)
- Database connection strings

## Step-by-Step Deployment

### 1️⃣ Setup Environment

```bash
cd vercel-deployment
cp .env.example .env
```

Edit `.env` with your database URLs:
```bash
DATABASE_URL_PRIVATE="postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"
DATABASE_URL_PUBLIC="postgresql://user:pass@ep-yyy.neon.tech/neondb?sslmode=require"
```

### 2️⃣ Install Vercel CLI

```bash
npm install -g vercel
```

### 3️⃣ Login to Vercel

```bash
vercel login
```

### 4️⃣ Deploy!

**Option A: Using Deploy Script (Recommended)**
```bash
./deploy.sh
```

**Option B: Manual Deployment**
```bash
# For development/preview
vercel

# For production
vercel --prod
```

### 5️⃣ Add Environment Variables

After first deployment, add your database secrets:

**Via CLI:**
```bash
vercel env add DATABASE_URL_PRIVATE
# Paste your private database URL when prompted

vercel env add DATABASE_URL_PUBLIC
# Paste your public database URL when prompted
```

**Via Dashboard:**
1. Go to https://vercel.com/dashboard
2. Select your project
3. Click "Settings" → "Environment Variables"
4. Add both `DATABASE_URL_PRIVATE` and `DATABASE_URL_PUBLIC`
5. Set scope to "Production", "Preview", and "Development"

### 6️⃣ Redeploy with Environment Variables

```bash
vercel --prod
```

## ✅ Verify Deployment

Your MCP server is now live at:
```
https://your-project.vercel.app/mcp
```

Test it:
```bash
curl https://your-project.vercel.app/mcp
```

## 🔍 View Logs

```bash
vercel logs
```

Or visit: https://vercel.com/dashboard → Your Project → Logs

## 🎯 What's Deployed?

✅ 19 Financial MCP Tools  
✅ Serverless Python Functions  
✅ Auto-scaling & HTTPS  
✅ Connected to Neon PostgreSQL  
✅ Production-ready API  

## 📊 Available Tools

**Account Management** (7 tools)
- list_accounts, get_account_balance, get_account_summary
- calculate_net_worth, list_transactions, search_transactions
- get_recurring_transactions

**Analytics** (4 tools)
- get_spending_by_category, get_monthly_trends
- get_top_merchants, get_cashflow_summary

**Budgeting** (3 tools)
- create_budget, list_budgets, get_budget_status

**Utilities** (2 tools)
- get_available_categories, format_currency

**Security** (3 tools)
- get_tool_policy, list_tool_policies, validate_tool_access

## 🛠️ Maintenance

### Update Deployment
```bash
git pull
cd vercel-deployment
vercel --prod
```

### Check Status
```bash
vercel ls
```

### Remove Deployment
```bash
vercel remove finance-mcp-server
```

## 🆘 Troubleshooting

**Issue: Import errors**
- Ensure all files are in `api/` directory
- Check `requirements.txt` has all dependencies

**Issue: Database connection failed**
- Verify environment variables in Vercel Dashboard
- Check database URLs include `?sslmode=require`
- Ensure IP allowlisting is disabled on Neon (or add Vercel IPs)

**Issue: 500 errors**
- Run `vercel logs` to see errors
- Check Python version compatibility (3.9+)

## 📚 Next Steps

1. ✅ Test all 19 tools
2. ✅ Integrate with your finance agent
3. ✅ Monitor usage in Vercel dashboard
4. ✅ Set up custom domain (optional)
5. ✅ Configure alerts and monitoring

---

**Done! Your Finance MCP Server is live on Vercel! 🎉**
