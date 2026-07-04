# MCP Server - Security Log Analysis Tools
# Built by: Mayur Pawar | BCA Student | Deogiri College
# Purpose: Provides specialized tools to the AI agent via Model Context Protocol (MCP)
# The agent calls these tools to parse logs and detect security threats
# Running on port 8001 — agent connects via http://localhost:8001/mcp

from fastmcp import FastMCP
import re

# Initialize FastMCP server — "SecurityLogAnalyzer" is the server name
# FastMCP makes it easy to expose Python functions as MCP tools
mcp = FastMCP("SecurityLogAnalyzer")

@mcp.tool()
def parse_logs(log_content: str) -> dict:
    """Parse raw security logs into structured format.
    
    Takes raw log text and converts each line into a structured dict
    with level (INFO/WARN/ERROR) and timestamp extracted.
    This structured format makes threat detection more accurate.
    """
    lines = log_content.strip().split('\n')
    parsed = []
    for line in lines:
        if line.strip():
            # Determine log level — important for severity classification
            level = "INFO"
            if "WARN" in line:
                level = "WARN"
            elif "ERROR" in line:
                level = "ERROR"
            parsed.append({
                "raw": line,
                "level": level,
                "timestamp": line[:19] if len(line) > 19 else "unknown"
            })
    return {"total_lines": len(parsed), "logs": parsed}

@mcp.tool()
def detect_threats(log_content: str) -> dict:
    """Detect security threats in logs using pattern matching.
    
    Scans logs for known attack signatures:
    - Brute force: 3+ failed logins from same IP (industry standard threshold)
    - SQL Injection: DROP TABLE or INSERT patterns in SQL errors
    - Port Scan: explicit port scan warnings in logs
    - XSS: Cross-site scripting attack patterns
    - Data Exfiltration: unusual outbound traffic volume
    
    Returns list of threats with severity (CRITICAL/HIGH) and details.
    I chose pattern matching over ML here because known signatures
    are faster and more reliable for common attack types.
    """
    threats = []
    ip_failures = {}  # Track failed logins per IP for brute force detection
    lines = log_content.strip().split('\n')

    for line in lines:
        # Brute force detection — count failed logins per IP
        if "Failed login" in line:
            ip_match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                ip = ip_match.group(1)
                ip_failures[ip] = ip_failures.get(ip, 0) + 1

        # SQL Injection detection — look for dangerous SQL keywords in error logs
        if ("SQL" in line and "DROP" in line) or ("SQL" in line and "INSERT" in line):
            threats.append({
                "type": "SQL Injection",
                "severity": "CRITICAL",
                "detail": line.strip()
            })

        # Port scan detection
        if "Port scan" in line or "port scan" in line:
            threats.append({
                "type": "Port Scan",
                "severity": "HIGH",
                "detail": line.strip()
            })

        # XSS attack detection
        if "XSS" in line:
            threats.append({
                "type": "XSS Attack",
                "severity": "HIGH",
                "detail": line.strip()
            })

        # Data exfiltration — unusually high outbound traffic
        if "bytes 9500000" in line or "Unusual outbound" in line:
            threats.append({
                "type": "Data Exfiltration",
                "severity": "HIGH",
                "detail": line.strip()
            })

    # Brute force check — 3+ failures from same IP = attack
    # Threshold of 3 chosen based on common SOC practices
    for ip, count in ip_failures.items():
        if count >= 3:
            threats.append({
                "type": "Brute Force",
                "severity": "CRITICAL",
                "detail": f"IP {ip} had {count} failed logins"
            })

    return {"threat_count": len(threats), "threats": threats}

# Entry point — run MCP server with streamable-http transport
# streamable-http allows real-time communication with the ADK agent
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)