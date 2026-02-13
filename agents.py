"""
Multi-Agent Trading Assistant using LangGraph
Implements Researcher, Quant, and Manager agents
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class MockLLM:
    """Mock LLM for deterministic testing"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
    
    def invoke(self, messages: list[BaseMessage]) -> AIMessage:
        """Process messages and return a mock response"""
        if not messages:
            return AIMessage(content=f"[{self.agent_name}] No input received.")
        
        last_message = messages[-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Extract ticker from content
        ticker = self._extract_ticker(content)
        
        # Generate agent-specific response
        if self.agent_name == "Researcher":
            return AIMessage(content=self._researcher_response(ticker))
        elif self.agent_name == "Quant":
            return AIMessage(content=self._quant_response(ticker))
        elif self.agent_name == "Manager":
            return AIMessage(content=self._manager_response(ticker, content))
        
        return AIMessage(content=f"[{self.agent_name}] Acknowledged: {content}")
    
    def _extract_ticker(self, content: str) -> str:
        """Extract ticker symbol from content"""
        # Simple extraction - look for uppercase words
        words = content.upper().split()
        for word in words:
            if word.isalpha() and 2 <= len(word) <= 5:
                return word
        return "UNKNOWN"
    
    def _researcher_response(self, ticker: str) -> str:
        """Generate sentiment analysis response"""
        # Mock sentiment based on ticker length (deterministic)
        sentiment = "BULLISH" if len(ticker) % 2 == 0 else "BEARISH"
        confidence = 75 + (len(ticker) * 2)
        
        return f"""📊 **Researcher Analysis for {ticker}**

**Market Sentiment:** {sentiment}
**Confidence Level:** {confidence}%

**Key Findings:**
- Recent news sentiment indicates {sentiment.lower()} momentum
- Social media mentions trending {'upward' if sentiment == 'BULLISH' else 'downward'}
- Analyst ratings: {'Majority Buy recommendations' if sentiment == 'BULLISH' else 'Mixed with caution signals'}

**Recommendation:** {sentiment.capitalize()} outlook based on current market sentiment.
"""
    
    def _quant_response(self, ticker: str) -> str:
        """Generate technical analysis response"""
        # Mock technical indicators based on ticker
        rsi = 45 + (len(ticker) * 3)
        ma_signal = "ABOVE" if len(ticker) % 2 == 0 else "BELOW"
        
        return f"""📈 **Quant Analysis for {ticker}**

**Technical Indicators:**
- RSI (14-day): {rsi} - {'Neutral' if 40 <= rsi <= 60 else 'Overbought' if rsi > 60 else 'Oversold'}
- 50-day MA: ${120 + len(ticker) * 5}
- 200-day MA: ${100 + len(ticker) * 3}
- Price Position: {ma_signal} moving averages

**Pattern Recognition:**
- Trend: {'Uptrend' if ma_signal == 'ABOVE' else 'Downtrend'}
- Support Level: ${95 + len(ticker) * 2}
- Resistance Level: ${135 + len(ticker) * 4}

**Technical Signal:** {'Buy' if ma_signal == 'ABOVE' else 'Sell'} signal based on moving average crossover.
"""
    
    def _manager_response(self, ticker: str, context: str) -> str:
        """Generate consolidated manager response"""
        return f"""🎯 **Manager Consolidation for {ticker}**

**Analysis Summary:**
I've reviewed both the Researcher's sentiment analysis and the Quant's technical indicators.

**Consensus Building:**
- Fundamental sentiment and technical signals are being evaluated
- Risk management parameters are being calculated
- Position sizing will be determined based on portfolio balance

**Next Step:** Calculating risk metrics using the Risk Calculator tool...
"""


class ChatState(TypedDict):
    """State for the trading assistant with message history"""
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    researcher_analysis: str
    quant_analysis: str
    risk_calculation: str


class TradingAgents:
    """Multi-agent trading system orchestrator"""
    
    def __init__(self):
        self.researcher_llm = MockLLM("Researcher")
        self.quant_llm = MockLLM("Quant")
        self.manager_llm = MockLLM("Manager")
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the multi-agent graph"""
        workflow = StateGraph(ChatState)
        
        # Add agent nodes
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("quant", self._quant_node)
        workflow.add_node("manager", self._manager_node)
        
        # Define linear flow
        workflow.add_edge(START, "researcher")
        workflow.add_edge("researcher", "quant")
        workflow.add_edge("quant", "manager")
        workflow.add_edge("manager", END)
        
        return workflow.compile()
    
    def _researcher_node(self, state: ChatState) -> ChatState:
        """Researcher agent - analyzes market sentiment"""
        messages = state["messages"]
        
        # Get latest user message
        user_message = messages[-1] if messages else HumanMessage(content="")
        
        # Generate research analysis
        response = self.researcher_llm.invoke([user_message])
        
        # Update state
        return {
            "messages": [response],
            "researcher_analysis": response.content
        }
    
    def _quant_node(self, state: ChatState) -> ChatState:
        """Quant agent - performs technical analysis"""
        messages = state["messages"]
        
        # Get the original user query for context
        user_messages = [m for m in messages if isinstance(m, HumanMessage)]
        user_message = user_messages[0] if user_messages else HumanMessage(content="")
        
        # Generate quant analysis
        response = self.quant_llm.invoke([user_message])
        
        # Update state
        return {
            "messages": [response],
            "quant_analysis": response.content
        }
    
    def _manager_node(self, state: ChatState) -> ChatState:
        """Manager agent - consolidates findings and calculates risk"""
        messages = state["messages"]
        
        # Get the original user query
        user_messages = [m for m in messages if isinstance(m, HumanMessage)]
        user_message = user_messages[0] if user_messages else HumanMessage(content="")
        
        # Get ticker from state or extract from message
        ticker = state.get("ticker", self.manager_llm._extract_ticker(user_message.content))
        
        # Generate manager consolidation
        manager_response = self.manager_llm.invoke([user_message])
        
        # Mock risk calculation (in real implementation, this would call MCP tool)
        risk_calc = self._calculate_risk_mock(ticker, price=125.0, balance=10000.0)
        
        # Create final recommendation
        final_response = AIMessage(content=f"""{manager_response.content}

{risk_calc}

**Final Recommendation:**
Based on comprehensive analysis from our Researcher and Quant teams:
- Entry Level: ${115 + len(ticker) * 3}
- Position Size: As calculated above
- Stop Loss: ${105 + len(ticker) * 2}
- Take Profit: ${145 + len(ticker) * 5}

⚠️ **Risk Disclaimer:** This is a demonstration using mock data. Always conduct your own research and consult with financial advisors before making investment decisions.
""")
        
        return {
            "messages": [final_response],
            "risk_calculation": risk_calc
        }
    
    def _calculate_risk_mock(self, ticker: str, price: float, balance: float) -> str:
        """Mock risk calculation (would call MCP tool in production)"""
        risk_per_trade = balance * 0.02  # 2% rule
        position_size = int(risk_per_trade / (price * 0.10))  # Assuming 10% stop loss
        investment = position_size * price
        
        return f"""💰 **Risk Calculation Results**

**Portfolio Parameters:**
- Account Balance: ${balance:,.2f}
- Risk Per Trade (2%): ${risk_per_trade:,.2f}
- Stock Price: ${price:.2f}

**Position Sizing:**
- Recommended Shares: {position_size}
- Total Investment: ${investment:,.2f}
- Stop Loss (10%): ${price * 0.90:.2f}
- Max Loss: ${risk_per_trade:,.2f}
"""
    
    def analyze(self, ticker: str, user_message: str = None) -> dict:
        """Analyze a ticker and return recommendations"""
        if user_message is None:
            user_message = f"Analyze {ticker} for trading"
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "ticker": ticker,
            "researcher_analysis": "",
            "quant_analysis": "",
            "risk_calculation": ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result
