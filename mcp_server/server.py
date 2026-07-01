# MCP Server - Security Log Analysis Tools
from fastmcp import FastMCP
import re
from datetime import datetime

# Initialize MCP server
mcp = FastMCP("SecurityLogAnalyzer")

@mcp.tool()
def parse_logs(log_content: str) -> dict:
    """Parse raw security logs into structured format."""
    lines = log_content.strip().split('\n')
    parsed = []
    for line in lines:
        if line.strip():
            level = "INFO"
            if "WARN" in line: level = "WARN"
            elif "ERROR" in line: level = "ERROR"
            parsed.append({"raw": line, "level": level, "timestamp": line[:19] if len(line) > 19 else "unknown"})
    return {"total_lines": len(parsed), "logs": parsed}

@mcp.tool()
def detect_threats(log_content: str) -> dict:
    """Detect security threats in logs."""
    threats = []
    ip_failures = {}
    lines = log_content.strip().split('\n')
    
    for line in lines:
        # Brute force detection
        if "Failed login" in line:
            ip_match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                ip = ip_match.group(1)
                ip_failures[ip] = ip_failures.get(ip, 0) + 1
        # SQL Injection
        if "SQL" in line and "DROP" in line or "SQL" in line and "INSERT" in line:
            threats.append({"type": "SQL Injection", "severity": "CRITICAL", "detail": line.strip()})
        # Port scan
        if "Port scan" in line or "port scan" in line:
            threats.append({"type": "Port Scan", "severity": "HIGH", "detail": line.strip()})
        # XSS
        if "XSS" in line:
            threats.append({"type": "XSS Attack", "severity": "HIGH", "detail": line.strip()})
        # Data exfiltration
        if "bytes 9500000" in line or "Unusual outbound" in line:
            threats.append({"type": "Data Exfiltration", "severity": "HIGH", "detail": line.strip()})

    # Brute force check
    for ip, count in ip_failures.items():
        if count >= 3:
            threats.append({"type": "Brute Force", "severity": "CRITICAL", "detail": f"IP {ip} had {count} failed logins"})

    return {"threat_count": len(threats), "threats": threats}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)