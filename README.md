# Multi-Agent Trading Assistant (2026)

## Description
A sophisticated **Multi-Agent Trading Assistant** built with LangGraph, Streamlit, and the Model Context Protocol (MCP). The system coordinates three specialized AI agents to provide comprehensive trading recommendations based on ticker analysis.

## Architecture

### Three Specialized Agents:

1. **📊 Researcher Agent**
   - Analyzes market sentiment
   - Reviews news and social media trends
   - Aggregates analyst recommendations
   - Outputs: Bullish/Bearish sentiment with confidence levels

2. **📈 Quant Agent**
   - Performs technical analysis
   - Calculates indicators (RSI, Moving Averages)
   - Identifies chart patterns and trends
   - Outputs: Technical signals and support/resistance levels

3. **🎯 Manager Agent**
   - Consolidates findings from both agents
   - Calls Risk Calculator tool via MCP
   - Generates final trading recommendation
   - Outputs: Complete trade setup with entry, exit, and position sizing

### Workflow
```
User Input (Ticker)
    ↓
Researcher Agent → Sentiment Analysis
    ↓
Quant Agent → Technical Analysis
    ↓
Manager Agent → Consolidation + Risk Calculation
    ↓
Final Recommendation
```

## Project Structure
```
trading-assistant/
├── app.py               # Streamlit UI + Multi-agent orchestration
├── agents.py            # LangGraph nodes, MockLLM, ChatState
├── mcp_server.py        # MCP server with risk calculation tool
├── requirements.txt     # Dependencies
├── src/
│   ├── __init__.py
│   └── chat_agent.py    # Legacy single-agent (deprecated)
├── test/
│   └── app.py          # Legacy UI (deprecated)
├── visualize_graph.py  # Graph visualization utility
├── .env               # API keys
└── README.md
```

## Technology Stack

- **Orchestration:** LangGraph (StateGraph with linear flow)
- **UI:** Streamlit (wide layout with agent thinking steps)
- **Tool Protocol:** Model Context Protocol (MCP) using FastMCP
- **State Management:** TypedDict with `Annotated[list, add_messages]`
- **Logic:** Python 3.11+
- **Testing:** MockLLM for deterministic responses

## Setup

### 1. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)
Edit `.env` to add real API keys:
```env
# Trading APIs
ALPACA_API_KEY=your_key
ALPHA_VANTAGE_API_KEY=your_key

# AI/LLM APIs  
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Usage

### Run the Multi-Agent Assistant
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### Example Queries
- "Analyze AAPL"
- "What's the outlook for TSLA?"
- "Should I buy MSFT?"
- "Evaluate NVDA for trading"

### Agent Workflow Display
The UI shows each agent's thinking process:
1. **Researcher Analysis** - Sentiment and news
2. **Quant Analysis** - Technical indicators
3. **Manager Recommendation** - Final trade setup with risk metrics

## Key Features

### 🤖 Multi-Agent Collaboration
- Three specialized agents work in sequence
- Each agent has focused expertise
- Linear workflow ensures consistent analysis

### 📊 Comprehensive Analysis
- **Fundamental**: News sentiment, analyst ratings
- **Technical**: RSI, moving averages, chart patterns
- **Risk Management**: 2% rule, position sizing, stop-loss

### 💡 Intelligent State Management
- Uses `ChatState` with message history
- Preserves context across agents
- Aggregates findings for final decision

### 🛠️ MCP Tool Integration
- Risk Calculator tool via MCP protocol
- Calculates position size using 2% risk rule
- Returns formatted risk metrics

### 🎨 Interactive UI
- Real-time agent thinking display
- Visual workflow diagram
- Quick example buttons
- Chat history management

## MCP Server

### Risk Calculator Tool
The MCP server (`mcp_server.py`) provides a `calculate_risk` tool:

**Input:**
- `ticker`: Stock symbol
- `price`: Current stock price
- `balance`: Account balance
- `stop_loss_percent`: Stop loss percentage (default: 10%)

**Output:**
- Position size (number of shares)
- Total investment amount
- Maximum loss (2% of balance)
- Stop-loss price
- Risk/reward ratio

### Running MCP Server Standalone
```bash
python mcp_server.py
```

## Development

### MockLLM Implementation
The `MockLLM` class provides deterministic responses for testing:
- Implements `.invoke()` method
- Returns agent-specific formatted responses
- No API calls required
- Fully reproducible results

### State Definition
```python
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    researcher_analysis: str
    quant_analysis: str
    risk_calculation: str
```

### Adding Custom Agents
1. Create a new `MockLLM` instance in `TradingAgents.__init__()`
2. Add a node method (e.g., `_sentiment_node`)
3. Register node in `_build_graph()`
4. Define edge connections

## Testing

### Run with Mock Data
The system uses `MockLLM` by default - no API keys needed for testing.

### Deterministic Responses
Mock responses are based on ticker characteristics:
- Ticker length determines sentiment (even = bullish, odd = bearish)
- Technical indicators calculated from ticker properties
- Completely reproducible for testing

## Requirements

```
langgraph>=0.2.0
langchain-core>=0.3.0
langchain-mcp>=0.1.0
python-dotenv>=1.0.0
streamlit>=1.30.0
mcp[cli]>=1.0.0
```

## Visualization

### View Agent Graph
```bash
python visualize_graph.py
```

Opens `graph_visualization.md` showing the LangGraph workflow.

## Programmatic Usage

```python
from agents import TradingAgents

# Initialize system
system = TradingAgents()

# Analyze a ticker
result = system.analyze("AAPL", "Should I buy AAPL?")

# Access individual agent outputs
print(result["researcher_analysis"])
print(result["quant_analysis"])
print(result["risk_calculation"])

# Get final recommendation
final_message = result["messages"][-1]
print(final_message.content)
```

## Roadmap

- [ ] Integrate real LLM (OpenAI, Anthropic)
- [ ] Connect live market data APIs
- [ ] Add portfolio tracking agent
- [ ] Implement backtesting module
- [ ] Add real-time price alerts
- [ ] Multi-ticker comparison

## Disclaimer

⚠️ **IMPORTANT:** This is a demonstration project using mock AI responses and simulated data. 

**NOT FINANCIAL ADVICE.** Always:
- Conduct your own research
- Consult with qualified financial advisors
- Never invest more than you can afford to lose
- Understand the risks of trading

## License

Educational and demonstration purposes only.

## Support

For issues or questions, please refer to the documentation or create an issue in the repository.
