# nodes.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import os
import json
from openai import OpenAI


def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AgentState(BaseModel):
    user_input: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    analysis: Optional[Dict[str, Any]] = None
    strategy: Optional[Dict[str, Any]] = None
    # optional: for orchestrator decisions
    next_agent: Optional[str] = None


class DataOutput(BaseModel):
    ticker: str
    prices: List[float]


class AnalysisOutput(BaseModel):
    trend: str
    volatility: str
    confidence: float


class StrategyOutput(BaseModel):
    strategy: str
    rationale: str
    hitl_required: bool = False


# ============================================================
# ORCHESTRATOR
# ============================================================

def orchestrator_node(state: AgentState):
    # Simple rule-based routing for now; can be upgraded to LLM-based later
    text = (state.user_input or "").lower()

    if "price" in text or "data" in text:
        state.next_agent = "data_agent"
    elif "trend" in text or "analysis" in text:
        state.next_agent = "analysis_agent"
    else:
        state.next_agent = "strategy_agent"

    return state


def build_orchestrator_graph():
    graph = StateGraph(AgentState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", END)
    return graph.compile()


# ============================================================
# DATA AGENT (LLM uses MCP tools; no local tool calls)
# ============================================================

def data_agent_node(state: AgentState):
    # For now, hard-code ticker; later you can parse from state.user_input
    ticker = "AAPL"

    client = get_client()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a data agent. "
                "You may use available tools (via MCP) to fetch market data. "
                "Return ONLY a JSON object with keys: ticker, prices (list of floats)."
            ),
        },
        {
            "role": "user",
            "content": f"Get recent price data for ticker {ticker}.",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    content = response.choices[0].message.content or "{}"

    try:
        parsed = json.loads(content)
        data_output = DataOutput(**parsed)
        state.data = data_output.dict()
    except Exception:
        # Degraded mode: if tools/MCP fail, LLM might still return something,
        # but if it's not valid JSON, we just leave state.data as None.
        state.data = None

    return state


def build_data_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("data_agent", data_agent_node)
    graph.set_entry_point("data_agent")
    graph.add_edge("data_agent", END)
    return graph.compile()


# ============================================================
# ANALYSIS AGENT (LLM uses MCP tools; no local tool calls)
# ============================================================

def analysis_agent_node(state: AgentState):
    prices = []
    if state.data and "prices" in state.data:
        prices = state.data["prices"]

    client = get_client()
    messages = [
        {
            "role": "system",
            "content": (
                "You are an analysis agent. "
                "You may use available tools (via MCP) to analyze price data. "
                "Return ONLY a JSON object with keys: trend (str), volatility (str), confidence (float)."
            ),
        },
        {
            "role": "user",
            "content": f"Analyze these prices: {prices}.",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    content = response.choices[0].message.content or "{}"

    try:
        parsed = json.loads(content)
        analysis_output = AnalysisOutput(**parsed)
        state.analysis = analysis_output.dict()
    except Exception:
        state.analysis = None

    return state


def build_analysis_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("analysis_agent", analysis_agent_node)
    graph.set_entry_point("analysis_agent")
    graph.add_edge("analysis_agent", END)
    return graph.compile()


# ============================================================
# STRATEGY AGENT (pure reasoning, no tools)
# ============================================================

def strategy_agent_node(state: AgentState):
    analysis = state.analysis or {}
    trend = analysis.get("trend", "unknown")
    volatility = analysis.get("volatility", "low")

    client = get_client()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a trading strategy assistant. "
                "Given trend and volatility, propose a concrete trading strategy and rationale. "
                "Do NOT call tools; use reasoning only."
            ),
        },
        {
            "role": "user",
            "content": f"Trend: {trend}, Volatility: {volatility}. Propose a strategy.",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    content = response.choices[0].message.content or ""
    output = StrategyOutput(
        strategy=f"Strategy based on {trend}/{volatility}",
        rationale=content,
        hitl_required=(volatility == "high"),
    )
    state.strategy = output.dict()
    return state


def build_strategy_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("strategy_agent", strategy_agent_node)
    graph.set_entry_point("strategy_agent")
    graph.add_edge("strategy_agent", END)
    return graph.compile()
