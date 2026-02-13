"""
Visualize the Multi-Agent Trading Assistant graph structure
"""
from agents import TradingAgents


def main():
    """Generate graph visualizations"""
    system = TradingAgents()
    
    # Method 1: ASCII representation (works immediately)
    print("=" * 60)
    print("Multi-Agent Trading System - ASCII Graph")
    print("=" * 60)
    try:
        ascii_graph = system.graph.get_graph().draw_ascii()
        print(ascii_graph)
    except Exception as e:
        print(f"ASCII visualization error: {e}")
    
    print("\n" + "=" * 60)
    print("Mermaid Graph Representation")
    print("=" * 60)
    
    # Method 2: Mermaid diagram (view in VS Code with Mermaid extension)
    try:
        mermaid_code = system.graph.get_graph().draw_mermaid()
        print("\nCopy this to a .md file or Mermaid viewer:")
        print("\n```mermaid")
        print(mermaid_code)
        print("```\n")
        
        # Create a simplified version that works better with most renderers
        simplified_mermaid = """flowchart TD
    Start([User Input: Ticker]) --> Researcher[📊 Researcher Agent]
    Researcher --> |Sentiment Analysis| Quant[📈 Quant Agent]
    Quant --> |Technical Analysis| Manager[🎯 Manager Agent]
    Manager --> |Risk Calculation| End([Final Recommendation])
    
    style Start fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Researcher fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style Quant fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    style Manager fill:#e8f5e9,stroke:#388e3c,stroke-width:3px
    style End fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px"""
        
        # Save to file for easy viewing
        with open("graph_visualization.md", "w") as f:
            f.write("# Multi-Agent Trading Assistant - Workflow\n\n")
            f.write("## Agent Collaboration Flow\n\n")
            f.write("```mermaid\n")
            f.write(simplified_mermaid)
            f.write("\n```\n\n")
            f.write("## Process Description\n\n")
            f.write("1. **User Input**: Ticker symbol (e.g., AAPL, TSLA)\n")
            f.write("2. **Researcher Agent**: Analyzes market sentiment and news\n")
            f.write("3. **Quant Agent**: Performs technical analysis (RSI, MA)\n")
            f.write("4. **Manager Agent**: Consolidates findings and calculates risk\n")
            f.write("5. **Final Recommendation**: Complete trade setup with position sizing\n")
        
        print("✓ Saved Mermaid diagram to: graph_visualization.md")
        print("  Open this file in VS Code to see the visual graph")
        
    except Exception as e:
        print(f"Mermaid visualization error: {e}")
    
    # Method 3: PNG (requires pygraphviz - optional)
    print("\n" + "=" * 60)
    print("PNG Export (Optional)")
    print("=" * 60)
    print("To export as PNG image:")
    print("1. Install pygraphviz: pip install pygraphviz")
    print("2. Use: system.graph.get_graph().draw_png('graph.png')")


if __name__ == "__main__":
    main()
