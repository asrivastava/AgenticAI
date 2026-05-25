# app.py

from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END

from nodes import (
    AgentState,
    build_orchestrator_graph,
    build_data_agent_graph,
    build_analysis_agent_graph,
    build_strategy_agent_graph,
)

# Load .env BEFORE anything else
load_dotenv()


# ============================================================
# BUILD MASTER GRAPH
# ============================================================

def build_master_graph():
    graph = StateGraph(AgentState)

    # Import subgraphs
    orchestrator = build_orchestrator_graph()
    data_agent = build_data_agent_graph()
    analysis_agent = build_analysis_agent_graph()
    strategy_agent = build_strategy_agent_graph()

    # Add nodes
    graph.add_node("orchestrator", orchestrator)
    graph.add_node("data_agent", data_agent)
    graph.add_node("analysis_agent", analysis_agent)
    graph.add_node("strategy_agent", strategy_agent)

    # Entry point
    graph.set_entry_point("orchestrator")

    # Conditional routing from orchestrator
    graph.add_conditional_edges(
        "orchestrator",
        lambda state: (
            "data_agent" if "price" in (state.user_input or "").lower() or "data" in (state.user_input or "").lower()
            else "analysis_agent" if "trend" in (state.user_input or "").lower() or "analysis" in (state.user_input or "").lower()
            else "strategy_agent"
        ),
        {
            "data_agent": "data_agent",
            "analysis_agent": "analysis_agent",
            "strategy_agent": "strategy_agent",
        }
    )

    # Linear flow after routing
    graph.add_edge("data_agent", "analysis_agent")
    graph.add_edge("analysis_agent", "strategy_agent")
    graph.add_edge("strategy_agent", END)

    return graph.compile()


# ============================================================
# RUN LOOP
# ============================================================

def main():
    master_graph = build_master_graph()

    print("Multi-agent system ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        state = AgentState(user_input=user_input)
        result = master_graph.invoke(state)

        print("\n=== FINAL OUTPUT ===")
        print(result)
        print("====================\n")


if __name__ == "__main__":
    main()