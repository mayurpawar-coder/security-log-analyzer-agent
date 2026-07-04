# 🔐 Security Log Analyzer Agent

> Built by Mayur Pawar | BCA Student | Deogiri College, Chhatrapati Sambhajinagar  
> Kaggle AI Agents Capstone — Agents for Business Track

---

## 💡 Why I Built This

I'm studying to become a SOC (Security Operations Center) Analyst. During my learning, I realized that one of the most time-consuming parts of a SOC analyst's job is manually reading through thousands of log lines to find threats. A single brute force attack can generate hundreds of log entries — and analysts have to catch it in real time.

I thought — what if an AI agent could do this automatically? Not just search for keywords, but actually reason about the logs, connect the dots, and give actionable recommendations like a real analyst would.

That's exactly what this project does.

---

## 🤖 What It Does

The Security Log Analyzer Agent takes raw security logs as input and:

1. **Parses** the logs into structured format
2. **Detects threats** — brute force, SQL injection, XSS attacks, port scans, data exfiltration
3. **Classifies severity** — CRITICAL, HIGH, MEDIUM
4. **Generates a threat report** with recommended actions

---

## 🏗️ Architecture
User Input (raw logs)
↓
Root Agent (Google ADK + Gemini 2.5 Flash)
↓
MCP Server (FastMCP) — 2 tools:
├── parse_logs      → structures raw log lines
└── detect_threats  → finds attack patterns
↓
Threat Report Output

**Why this architecture?**  
I chose MCP (Model Context Protocol) because it separates the tool logic from the agent logic cleanly. The agent focuses on reasoning, the MCP server focuses on detection. This makes it easy to add new detection tools later without touching the agent code.

---

## 🛠️ Tech Stack

| Tool | Version | Why I chose it |
|---|---|---|
| Google ADK | 2.3.0 | Official agent framework, works great with Gemini |
| FastMCP | 3.4.2 | Easiest way to build MCP server in Python |
| Gemini 2.5 Flash | latest | Fast, accurate, good at structured reasoning |
| Python | 3.11+ | My primary language |
| Cloud Run | — | Serverless, free tier available |

---

## 📁 Project Structure

security-log-analyzer-agent/
├── agent/
│   ├── agent.py          # Root agent definition
│   └── init.py
├── mcp_server/
│   └── server.py         # FastMCP tools: parse_logs, detect_threats
├── sample_logs/
│   └── sample.log        # Sample security logs for testing
├── .env                  # API keys (never committed)
├── .gitignore
└── README.md

## 🚀 Setup Instructions

### Prerequisites
- Python 3.11+
- Google Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Installation

```bash
git clone https://github.com/mayurpawar-coder/security-log-analyzer-agent.git
cd security-log-analyzer-agent
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install google-adk fastmcp python-dotenv
```

### Configure API Key

Create a `.env` file:

GOOGLE_API_KEY=your_key_here

### Run

Open two terminals:

**Terminal 1 — Start MCP Server:**
```bash
python mcp_server/server.py
```

**Terminal 2 — Start Agent:**
```bash
adk web
```

Open browser at `http://127.0.0.1:8000` and select `agent`.

---

## 🧪 Test It

Paste this into the agent chat:

Analyze these security logs and identify all threats:
2026-07-01 08:23:11 WARN Failed login attempt for user admin from IP 192.168.1.105
2026-07-01 08:23:14 WARN Failed login attempt for user admin from IP 192.168.1.105
2026-07-01 08:23:17 WARN Failed login attempt for user admin from IP 192.168.1.105
2026-07-01 08:31:44 ERROR SQL error near "DROP TABLE users" from IP 203.0.113.42
2026-07-01 08:45:12 WARN Port scan detected from IP 198.51.100.7 ports 22,80,443,3306
2026-07-01 09:45:03 ERROR Possible XSS attack detected in request from IP 203.0.113.42

## 🔒 Security

- API keys stored in `.env` only — never committed to GitHub
- `.gitignore` protects all sensitive files
- Input validation in MCP tools

---

## 📌 Course Concepts Used

| Concept | Where |
|---|---|
| Agent / Multi-agent (ADK) | `agent/agent.py` |
| MCP Server | `mcp_server/server.py` |
| Security features | `.env`, `.gitignore`, input validation |
| Deployability | Cloud Run |
| Antigravity IDE | Used for development |

---

*Made with curiosity and a lot of terminal errors — Mayur Pawar*