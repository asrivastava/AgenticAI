# app.py

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from nodes import (
    AgentState,
    build_orchestrator_graph,
    build_data_agent_graph,
    build_analysis_agent_graph,
    build_strategy_agent_graph,
)

load_dotenv()


def build_master_graph():
    graph = StateGraph(AgentState)

    orchestrator = build_orchestrator_graph()
    data_agent = build_data_agent_graph()
    analysis_agent = build_analysis_agent_graph()
    strategy_agent = build_strategy_agent_graph()

    graph.add_node("orchestrator", orchestrator)
    graph.add_node("data_agent", data_agent)
    graph.add_node("analysis_agent", analysis_agent)
    graph.add_node("strategy_agent", strategy_agent)

    graph.set_entry_point("orchestrator")

    def route_from_orchestrator(state: AgentState):
        # Use the decision set in orchestrator_node
        return state.next_agent or "strategy_agent"

    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "data_agent": "data_agent",
            "analysis_agent": "analysis_agent",
            "strategy_agent": "strategy_agent",
        },
    )

    # Normal forward flow: data → analysis → strategy
    graph.add_edge("data_agent", "analysis_agent")
    graph.add_edge("analysis_agent", "strategy_agent")
    graph.add_edge("strategy_agent", END)

    return graph.compile()


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

        print("\n=== FINAL STATE ===")
        print(result)
        print("===================\n")


if __name__ == "__main__":
    main()
