# Security Log Analyzer Agent - Google ADK
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

load_dotenv()

# Root agent - orchestrates everything
root_agent = LlmAgent(
    model="gemini-2.5-flash",
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
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8001/mcp")
            )
        )
    ],
)