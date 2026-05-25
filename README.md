
# 🛩️ MarketPilot

MarketPilot is an AI‑powered **market analysis and strategy assistant** built using a multi‑agent architecture. It retrieves market data, analyzes trends, and generates trading strategies through a combination of LLM reasoning and MCP‑powered tools. The system is designed to be modular, extensible, and resilient — capable of operating with or without tool access.

---

## 🎯 Purpose & Goal

MarketPilot aims to provide:

- Automated market data retrieval  
- Intelligent trend and volatility analysis  
- LLM‑generated trading strategies  
- A clean, agent‑orchestrated workflow  
- A tool‑driven architecture that gracefully degrades when tools are unavailable  

It functions as a **market strategist assistant**, helping users explore signals, insights, and strategy ideas through natural language.

---

## 🧱 Architecture Overview

MarketPilot uses a **multi‑agent LangGraph architecture** with a dedicated MCP server for tool execution.

### Core Components

- **Orchestrator Agent**  
  Routes user requests to the appropriate agent based on intent.

- **Data Agent**  
  Fetches price data via MCP tools.

- **Analysis Agent**  
  Computes trend, volatility, and confidence metrics.

- **Strategy Agent**  
  Generates trading strategies using LLM reasoning.

- **MCP Server**  
  Exposes tools such as:
  - `fetch_price_data`
  - `analyze_prices`
  - `generate_strategy`

### Design Principles

- Tools run **only** through MCP — agents never import tool code directly.  
- If MCP is offline, the system continues in **reasoning‑only mode**.  
- Clean separation between agents, tools, and orchestration.  
- Minimal repo footprint — only essential source files are tracked.

---

## 🧰 Tech Stack

### Core Frameworks

- **LangGraph** — agent orchestration and workflow graph  
- **OpenAI** — LLM reasoning and tool‑calling  
- **FastMCP** — MCP server for tool execution  
- **Python** — core application logic  

### Project Structure

```
.
├── app.py            # Main entry point, builds and runs the master graph
├── nodes.py          # All agent nodes + orchestrator logic
├── mcp_server.py     # MCP server exposing tools
├── requirements.txt  # Python dependencies
└── .gitignore        # Minimal ignore rules
```

---

## ⚙️ Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create your `.env` file

(Not tracked by Git)

```
OPENAI_API_KEY=your_key_here
```

---

### 4. Start the MCP server

```bash
python mcp_server.py
```

---

### 5. Run MarketPilot

```bash
python app.py
```

You can now ask:

- “Fetch price data for TSLA”  
- “Analyze the trend”  
- “Generate a strategy”  

MarketPilot will route the request to the correct agent.