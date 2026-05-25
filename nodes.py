# nodes.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import os
from openai import OpenAI


# ============================================================
# SAFE CLIENT INITIALIZATION
# ============================================================

def get_client():
    """Create OpenAI client only when needed (prevents import-time failures)."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# 1. SHARED STATE MODEL
# ============================================================

class AgentState(BaseModel):
    user_input: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    analysis: Optional[Dict[str, Any]] = None
    strategy: Optional[Dict[str, Any]] = None


# ============================================================
# 2. STRUCTURED OUTPUT MODELS
# ============================================================

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
# 3. ORCHESTRATOR SUBGRAPH
# ============================================================

def orchestrator_node(state: AgentState):
    """Return state only. Routing is handled by conditional edges."""
    return state


def build_orchestrator_graph():
    graph = StateGraph(AgentState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", END)
    return graph.compile()


# ============================================================
# 4. DATA AGENT SUBGRAPH
# ============================================================

def data_agent_node(state: AgentState):
    """Simulates fetching price data."""
    output = DataOutput(
        ticker="AAPL",
        prices=[100, 101, 102, 103, 104]
    )
    state.data = output.dict()
    return state


def build_data_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("data_agent", data_agent_node)
    graph.set_entry_point("data_agent")
    graph.add_edge("data_agent", END)
    return graph.compile()


# ============================================================
# 5. ANALYSIS AGENT SUBGRAPH
# ============================================================

def analysis_agent_node(state: AgentState):
    """Simulates trend analysis."""
    prices = state.data["prices"] if state.data else []
    trend = "uptrend" if prices[-1] > prices[0] else "downtrend"

    output = AnalysisOutput(
        trend=trend,
        volatility="medium",
        confidence=0.72
    )
    state.analysis = output.dict()
    return state


def build_analysis_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("analysis_agent", analysis_agent_node)
    graph.set_entry_point("analysis_agent")
    graph.add_edge("analysis_agent", END)
    return graph.compile()


# ============================================================
# 6. STRATEGY AGENT SUBGRAPH (HITL-ready)
# ============================================================

def strategy_agent_node(state: AgentState):
    """Produces a strategy recommendation."""
    analysis = state.analysis or {}
    trend = analysis.get("trend", "unknown")

    strategy = "trend_following" if trend == "uptrend" else "mean_reversion"

    output = StrategyOutput(
        strategy=strategy,
        rationale="Based on trend and volatility.",
        hitl_required=analysis.get("confidence", 1) < 0.6
    )

    state.strategy = output.dict()
    return state


def build_strategy_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("strategy_agent", strategy_agent_node)
    graph.set_entry_point("strategy_agent")
    graph.add_edge("strategy_agent", END)
    return graph.compile()
