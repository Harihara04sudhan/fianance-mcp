"""
Finance MCP Server - Vercel Deployment
========================================
Serverless deployment of Finance MCP server on Vercel.
"""

import os
from fastmcp import FastMCP
from app_tools import register_finance_tools

# Initialize the FastMCP server
mcp = FastMCP(name="Finance MCP with Financial Tools")

# Register all financial tools
register_finance_tools(mcp)

# Create the Vercel handler
# Vercel expects a handler function for serverless deployments
def handler(request, response):
    """Vercel serverless handler."""
    return mcp.handle_request(request, response)

# For local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(
        transport="http",
        port=port,
        host="0.0.0.0"
    )
