"""
Streamlit UI for the AI Trading Assistant
Run with: streamlit run test/app.py
"""
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.chat_agent import TradingAssistant


# Page configuration
st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="centered"
)

# Initialize the agent
@st.cache_resource
def get_agent():
    """Initialize and cache the trading assistant"""
    return TradingAssistant()


def main():
    """Main Streamlit app"""
    st.title("📈 AI Trading Assistant")
    st.caption("Powered by LangGraph | Market Analysis & Portfolio Management")
    
    # Initialize agent
    agent = get_agent()
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input with trading-specific placeholder
    if prompt := st.chat_input("Ask about stocks, market analysis, trading strategies..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = agent.analyze(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with info and controls
    with st.sidebar:
        st.header("🎯 Features")
        st.info("""
        Your AI-powered trading companion:
        - 📊 **Market Analysis** - Real-time insights
        - 💼 **Portfolio Management** - Strategy advice
        - 📈 **Technical Analysis** - Chart patterns & indicators
        - ⚠️ **Risk Management** - Stop-loss recommendations
        
        Built with:
        - **LangGraph** for intelligent workflows
        - **MockLLM** for demo (no API costs)
        - **Streamlit** for interactive UI
        """)
        
        st.header("⚡ Quick Queries")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Portfolio Review", use_container_width=True):
                st.session_state.demo_query = "Review my portfolio diversification"
            if st.button("📈 Market Trends", use_container_width=True):
                st.session_state.demo_query = "What are current market trends?"
        with col2:
            if st.button("💡 Strategy Tips", use_container_width=True):
                st.session_state.demo_query = "Give me a long-term investment strategy"
            if st.button("⚠️ Risk Analysis", use_container_width=True):
                st.session_state.demo_query = "How do I manage portfolio risk?"
        
        st.header("🎛️ Controls")
        if st.button("Clear Chat History", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.header("📊 Session Stats")
        st.metric("Total Messages", len(st.session_state.messages))
        if len(st.session_state.messages) > 0:
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("Your Questions", user_msgs)
        
        st.header("🔄 System Flow")
        st.code("Start → Analyze → Insights → End", language="text")
        
        st.divider()
        st.caption("⚠️ Disclaimer: This is a demo AI assistant using mock responses. Not real financial advice.")


if __name__ == "__main__":
    main()
