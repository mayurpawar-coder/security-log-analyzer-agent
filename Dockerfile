# Base image — Python 3.11 slim for minimal container size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy entire project into container
COPY . .

# Install all required dependencies
# google-adk: Google Agent Development Kit for building AI agents
# fastmcp: FastMCP server for Model Context Protocol tools
# python-dotenv: Load environment variables from .env file
RUN pip install google-adk fastmcp python-dotenv

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the MCP server when container launches
# MCP server provides log parsing and threat detection tools to the agent
CMD ["python", "mcp_server/server.py"]