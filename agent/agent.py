# Security Log Analyzer Agent - Google ADK
# Built by: Mayur Pawar | BCA Student | Deogiri College
# Kaggle AI Agents Capstone 2026 - Agents for Business Track
# Purpose: Automatically analyze security logs and detect threats like a SOC analyst

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

# Load API keys from .env file — never hardcode keys in source code
load_dotenv()

# Root agent — the brain of the system
# Uses Gemini 2.5 Flash for fast, accurate security analysis
# Connects to MCP server for specialized log parsing and threat detection tools
root_agent = LlmAgent(
    model="gemini-2.5-flash",  # Fast model — important for real-time SOC analysis
    name="security_log_analyzer",
    description="Analyzes security logs to detect threats and provide actionable insights.",
    instruction="""You are an expert SOC (Security Operations Center) analyst agent.

Your job:
1. When given security logs, use parse_logs tool to structure them
2. Use detect_threats tool to find attack patterns  
3. Provide a clear threat report with:
   - CRITICAL threats first
   - HIGH threats second
   - Summary of what happened
   - Recommended actions

Always be concise and actionable. Format your response clearly.""",
    tools=[
        # McpToolset connects agent to MCP server running on port 8001
        # MCP server provides: parse_logs and detect_threats tools
        # URL can be overridden via MCP_SERVER_URL environment variable for deployment
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp")
            )
        )
    ],
)