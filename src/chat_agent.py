"""
AI Trading Assistant using LangGraph with MockLLM
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.language_models.fake_chat_models import FakeChatModel


class TradingState(TypedDict):
    """State for the trading assistant"""
    messages: Annotated[list[BaseMessage], "Trading conversation messages"]


class TradingAssistant:
    """AI Trading Assistant using LangGraph and MockLLM"""
    
    def __init__(self):
        # Initialize a mock LLM with trading-specific responses
        self.llm = FakeChatModel(
            responses=[
                "Hello! I'm your AI Trading Assistant. I can help you with market analysis, portfolio management, and trading strategies. What would you like to know?",
                "Based on current market conditions, that's an interesting strategy. Let me analyze the risk/reward ratio for you.",
                "I recommend reviewing the technical indicators before making that trade. The RSI is showing overbought conditions.",
                "Your portfolio diversification looks good. Consider adding some defensive positions to hedge against volatility.",
                "Market trends suggest a bullish sentiment. However, always remember to set stop-loss orders to manage risk.",
                "That stock shows strong fundamentals. The P/E ratio is attractive, and earnings growth has been consistent.",
                "I advise caution with that position. The sector is experiencing headwinds, and volatility is expected.",
                "Great question! For long-term investing, focus on companies with strong balance sheets and competitive advantages."
            ]
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the trading assistant graph"""
        workflow = StateGraph(TradingState)
        
        # Add nodes
        workflow.add_node("analyze", self._analyze_node)
        
        # Set entry point
        workflow.set_entry_point("analyze")
        
        # Add edge to end
        workflow.add_edge("analyze", END)
        
        return workflow.compile()
    
    def _analyze_node(self, state: TradingState) -> TradingState:
        """Analyze trading queries and provide insights"""
        messages = state["messages"]
        
        # Get last user message
        last_message = messages[-1] if messages else None
        
        if last_message:
            # Generate response using mock LLM
            response = self.llm.invoke([last_message])
            messages.append(AIMessage(content=response.content))
        
        return {"messages": messages}
    
    def analyze(self, user_input: str) -> str:
        """Analyze trading query and get AI insights"""
        return self.chat(user_input)
    
    def chat(self, user_input: str) -> str:
        """Send a message and get a response"""
        # Create initial state
        state = {
            "messages": [HumanMessage(content=user_input)]
        }
        
        # Run the graph
        result = self.graph.invoke(state)
        
        # Return the last AI message
        ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
        return ai_messages[-1].content if ai_messages else "No response generated"

