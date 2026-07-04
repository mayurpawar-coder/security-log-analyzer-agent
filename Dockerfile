FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install google-adk fastmcp python-dotenv
EXPOSE 8080
CMD ["python", "mcp_server/server.py"]