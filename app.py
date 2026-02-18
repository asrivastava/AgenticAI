"""
Multi-Agent Trading Assistant - Streamlit UI
Orchestrates Researcher, Quant, and Manager agents
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents')))
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

# ...existing code...
