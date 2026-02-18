from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from .mock_llm import MockLLM

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    researcher_analysis: str
    quant_analysis: str
    risk_calculation: str

class TradingAgents:
    def __init__(self):
        self.researcher_llm = MockLLM("Researcher")
        self.quant_llm = MockLLM("Quant")
        self.manager_llm = MockLLM("Manager")
        self.graph = self._build_graph()
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(ChatState)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("quant", self._quant_node)
        workflow.add_node("manager", self._manager_node)
        workflow.add_edge(START, "researcher")
        workflow.add_edge("researcher", "quant")
        workflow.add_edge("quant", "manager")
        workflow.add_edge("manager", END)
        return workflow.compile()
    def _researcher_node(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        user_message = messages[-1] if messages else HumanMessage(content="")
        response = self.researcher_llm.invoke([user_message])
        return {
            "messages": [response],
            "researcher_analysis": response.content
        }
    def _quant_node(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        user_messages = [m for m in messages if isinstance(m, HumanMessage)]
        user_message = user_messages[0] if user_messages else HumanMessage(content="")
        response = self.quant_llm.invoke([user_message])
        return {
            "messages": [response],
            "quant_analysis": response.content
        }
    def _manager_node(self, state: ChatState) -> ChatState:
        messages = state["messages"]
        user_messages = [m for m in messages if isinstance(m, HumanMessage)]
        user_message = user_messages[0] if user_messages else HumanMessage(content="")
        ticker = state.get("ticker", self.manager_llm._extract_ticker(user_message.content))
        manager_response = self.manager_llm.invoke([user_message])
        risk_calc = self._calculate_risk_mock(ticker, price=125.0, balance=10000.0)
        final_response = AIMessage(content=f"""{manager_response.content}\n\n{risk_calc}\n\n**Final Recommendation:**\nBased on comprehensive analysis from our Researcher and Quant teams:\n- Entry Level: ${115 + len(ticker) * 3}\n- Position Size: As calculated above\n- Stop Loss: ${105 + len(ticker) * 2}\n- Take Profit: ${145 + len(ticker) * 5}\n\n⚠️ **Risk Disclaimer:** This is a demonstration using mock data. Always conduct your own research and consult with financial advisors before making investment decisions.\n""")
        return {
            "messages": [final_response],
            "risk_calculation": risk_calc
        }
    def _calculate_risk_mock(self, ticker: str, price: float, balance: float) -> str:
        risk_per_trade = balance * 0.02
        position_size = int(risk_per_trade / (price * 0.10))
        investment = position_size * price
        return f"""💰 **Risk Calculation Results**\n\n**Portfolio Parameters:**\n- Account Balance: ${balance:,.2f}\n- Risk Per Trade (2%): ${risk_per_trade:,.2f}\n- Stock Price: ${price:.2f}\n\n**Position Sizing:**\n- Recommended Shares: {position_size}\n- Total Investment: ${investment:,.2f}\n- Stop Loss (10%): ${price * 0.90:.2f}\n- Max Loss: ${risk_per_trade:,.2f}\n"""
    def analyze(self, ticker: str, user_message: str = None) -> dict:
        if user_message is None:
            user_message = f"Analyze {ticker} for trading"
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "ticker": ticker,
            "researcher_analysis": "",
            "quant_analysis": "",
            "risk_calculation": ""
        }
        result = self.graph.invoke(initial_state)
        return result
