# Vercel Deployment Guide

## 🚀 Deploy to Vercel

### 1. Import Repository

1. Go to [Vercel Dashboard](https://vercel.com)
2. Click **"Add New"** → **"Project"**
3. Select **Import Git Repository**
4. Choose `Harihara04sudhan/fianance-mcp`

### 2. Configure Project

- **Framework Preset**: Other
- **Root Directory**: `./` (default)
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### 3. Add Environment Variables

Click **"Environment Variables"** and add these **two required variables**:

#### Required Environment Variables:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `DATABASE_URL_PRIVATE` | Your Neon Private Database URL | `postgresql://user:pass@host.neon.tech/dbname` |
| `DATABASE_URL_PUBLIC` | Your Neon Public Database URL | `postgresql://user:pass@host.neon.tech/dbname_public` |

**How to get Database URLs:**

1. Go to [Neon Console](https://console.neon.tech)
2. Select your project
3. Go to **Dashboard** → **Connection Details**
4. Copy the **Connection String** (Pooled or Direct)
5. Create TWO databases:
   - `finance_private` - for PII data (users, accounts, transactions)
   - `finance_public` - for analytics (aggregated, non-sensitive data)

**Example URLs:**
```
DATABASE_URL_PRIVATE=postgresql://user:password@ep-cool-mountain-123456.us-east-2.aws.neon.tech/finance_private
DATABASE_URL_PUBLIC=postgresql://user:password@ep-cool-mountain-123456.us-east-2.aws.neon.tech/finance_public
```

### 4. Deploy

Click **"Deploy"** and wait for deployment to complete.

### 5. Test Your Deployment

Once deployed, test your MCP server:

```bash
curl https://your-app.vercel.app/mcp/list_tools
```

You should see a list of available finance tools.

## 🔧 Troubleshooting

### Error: "DATABASE_URL_PRIVATE references Secret"

**Solution**: Make sure you added both environment variables in Vercel dashboard:
1. Go to your project in Vercel
2. Click **Settings** → **Environment Variables**
3. Add both `DATABASE_URL_PRIVATE` and `DATABASE_URL_PUBLIC`
4. Redeploy

### Error: "Connection to database failed"

**Solution**: Verify your database URLs are correct:
1. Test connection locally first
2. Make sure Neon database is active (not paused)
3. Check if IP allowlist is configured (Neon allows all by default)

## 📚 Next Steps

After deployment:
1. Set up your database schema using `/setup_db`
2. Test MCP tools using the API endpoints
3. Integrate with your AI agent

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
