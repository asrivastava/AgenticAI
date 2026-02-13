"""
Multi-Agent Trading Assistant - Streamlit UI
Orchestrates Researcher, Quant, and Manager agents
"""
import streamlit as st
from agents import TradingAgents
from langchain_core.messages import HumanMessage, AIMessage
import time


# Page configuration
st.set_page_config(
    page_title="Multi-Agent Trading Assistant",
    page_icon="🤖📈",
    layout="wide"
)


@st.cache_resource
def get_trading_system():
    """Initialize and cache the multi-agent trading system"""
    return TradingAgents()


def extract_ticker(message: str) -> str:
    """Extract ticker from user message"""
    words = message.upper().split()
    for word in words:
        # Look for potential ticker symbols (2-5 uppercase letters)
        if word.isalpha() and 2 <= len(word) <= 5:
            return word
    return None


def display_agent_thinking(agent_name: str, content: str, icon: str):
    """Display agent thinking process"""
    with st.chat_message("assistant", avatar=icon):
        with st.expander(f"🤔 {agent_name} Agent Thinking...", expanded=True):
            st.markdown(content)


def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🤖📈 Multi-Agent Trading Assistant")
    st.caption("Powered by LangGraph | Researcher → Quant → Manager")
    
    # Initialize system
    trading_system = get_trading_system()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "show_thinking" not in st.session_state:
        st.session_state.show_thinking = True
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Multi-Agent System")
        
        st.info("""
        **Three Specialized Agents:**
        
        📊 **Researcher Agent**
        - Market sentiment analysis
        - News and social media
        - Analyst recommendations
        
        📈 **Quant Agent**
        - Technical indicators (RSI, MA)
        - Chart pattern recognition
        - Price action analysis
        
        🎯 **Manager Agent**
        - Consolidates findings
        - Risk calculation (2% rule)
        - Final recommendation
        """)
        
        st.header("⚙️ Settings")
        st.session_state.show_thinking = st.checkbox(
            "Show Agent Thinking Steps", 
            value=True,
            help="Display detailed analysis from each agent"
        )
        
        st.header("💡 Quick Examples")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Analyze AAPL", use_container_width=True):
                st.session_state.demo_query = "Analyze AAPL"
            if st.button("📈 Check TSLA", use_container_width=True):
                st.session_state.demo_query = "Check TSLA"
        with col2:
            if st.button("💼 Review MSFT", use_container_width=True):
                st.session_state.demo_query = "Review MSFT"
            if st.button("🔍 Evaluate NVDA", use_container_width=True):
                st.session_state.demo_query = "Evaluate NVDA"
        
        st.header("🎛️ Controls")
        if st.button("🗑️ Clear History", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.header("📊 Stats")
        st.metric("Total Queries", len([m for m in st.session_state.messages if m["role"] == "user"]))
        
        st.divider()
        st.caption("⚠️ Demo system with mock data. Not financial advice.")
    
    # Main chat area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        user_input = st.chat_input("Enter a ticker symbol (e.g., 'Analyze AAPL')...")
        
        # Handle demo query from sidebar
        if "demo_query" in st.session_state and st.session_state.demo_query:
            user_input = st.session_state.demo_query
            st.session_state.demo_query = None
        
        if user_input:
            # Extract ticker
            ticker = extract_ticker(user_input)
            
            if not ticker:
                with st.chat_message("assistant"):
                    st.error("⚠️ Please provide a valid ticker symbol (e.g., AAPL, MSFT, TSLA)")
            else:
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # Show system processing
                with st.chat_message("assistant"):
                    with st.status("🔄 Activating Multi-Agent System...", expanded=True) as status:
                        st.write("📝 Initializing agent workflow...")
                        time.sleep(0.5)
                        
                        st.write(f"🎯 Target Ticker: **{ticker}**")
                        st.write("🚀 Starting agent sequence...")
                        time.sleep(0.5)
                        
                        # Run the multi-agent system
                        result = trading_system.analyze(ticker, user_input)
                        
                        status.update(label="✅ Analysis Complete!", state="complete")
                
                # Display agent thinking steps if enabled
                if st.session_state.show_thinking:
                    # Researcher
                    if result.get("researcher_analysis"):
                        display_agent_thinking(
                            "Researcher", 
                            result["researcher_analysis"],
                            "📊"
                        )
                        time.sleep(0.3)
                    
                    # Quant
                    if result.get("quant_analysis"):
                        display_agent_thinking(
                            "Quant",
                            result["quant_analysis"],
                            "📈"
                        )
                        time.sleep(0.3)
                
                # Final recommendation from Manager
                final_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
                if final_messages:
                    final_content = final_messages[-1].content
                    
                    with st.chat_message("assistant", avatar="🎯"):
                        st.markdown("### 🎯 Manager - Final Recommendation")
                        st.markdown(final_content)
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_content
                    })
    
    with col2:
        st.subheader("🔄 Agent Workflow")
        
        # Visual workflow diagram
        st.markdown("""
        ```
        📥 User Input
            ↓
        📊 Researcher Agent
            ↓ (Sentiment)
        📈 Quant Agent  
            ↓ (Technicals)
        🎯 Manager Agent
            ↓ (Consolidation)
        💰 Risk Calculator
            ↓
        ✅ Recommendation
        ```
        """)
        
        st.subheader("📋 Latest Analysis")
        if st.session_state.messages:
            last_query = [m for m in st.session_state.messages if m["role"] == "user"]
            if last_query:
                st.info(f"**Last Query:** {last_query[-1]['content']}")
        
        st.subheader("🛠️ System Status")
        st.success("✅ All agents operational")
        st.success("✅ Risk calculator ready")
        st.success("✅ MCP protocol active")


if __name__ == "__main__":
    main()
