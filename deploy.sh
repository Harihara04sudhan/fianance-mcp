#!/bin/bash

# Finance MCP Vercel Deployment Script
# This script helps you deploy the Finance MCP server to Vercel

set -e

echo "🚀 Finance MCP Server - Vercel Deployment"
echo "=========================================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed"
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    echo "✅ Vercel CLI installed successfully"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "📝 Please create .env file from .env.example"
    echo ""
    echo "Copy and edit .env.example:"
    echo "  cp .env.example .env"
    echo "  nano .env  # or your preferred editor"
    echo ""
    exit 1
fi

echo "✅ Environment file found"
echo ""

# Ask for deployment type
echo "Select deployment type:"
echo "  1) Development (preview)"
echo "  2) Production"
read -p "Enter choice (1 or 2): " deploy_type

if [ "$deploy_type" = "2" ]; then
    echo ""
    echo "🌐 Deploying to PRODUCTION..."
    vercel --prod
elif [ "$deploy_type" = "1" ]; then
    echo ""
    echo "🔧 Deploying to DEVELOPMENT (preview)..."
    vercel
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Set environment variables in Vercel Dashboard"
echo "  2. Test your deployment"
echo "  3. View logs: vercel logs"
echo ""
echo "🔗 Visit: https://vercel.com/dashboard"
