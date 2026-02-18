from langchain_core.messages import AIMessage, BaseMessage

class MockLLM:
    """Mock LLM for deterministic testing"""
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
    
    def invoke(self, messages: list[BaseMessage]) -> AIMessage:
        if not messages:
            return AIMessage(content=f"[{self.agent_name}] No input received.")
        last_message = messages[-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        ticker = self._extract_ticker(content)
        if self.agent_name == "Researcher":
            return AIMessage(content=self._researcher_response(ticker))
        elif self.agent_name == "Quant":
            return AIMessage(content=self._quant_response(ticker))
        elif self.agent_name == "Manager":
            return AIMessage(content=self._manager_response(ticker, content))
        return AIMessage(content=f"[{self.agent_name}] Acknowledged: {content}")
    def _extract_ticker(self, content: str) -> str:
        words = content.upper().split()
        for word in words:
            if word.isalpha() and 2 <= len(word) <= 5:
                return word
        return "UNKNOWN"
    def _researcher_response(self, ticker: str) -> str:
        sentiment = "BULLISH" if len(ticker) % 2 == 0 else "BEARISH"
        confidence = 75 + (len(ticker) * 2)
        return f"""📊 **Researcher Analysis for {ticker}**\n\n**Market Sentiment:** {sentiment}\n**Confidence Level:** {confidence}%\n\n**Key Findings:**\n- Recent news sentiment indicates {sentiment.lower()} momentum\n- Social media mentions trending {'upward' if sentiment == 'BULLISH' else 'downward'}\n- Analyst ratings: {'Majority Buy recommendations' if sentiment == 'BULLISH' else 'Mixed with caution signals'}\n\n**Recommendation:** {sentiment.capitalize()} outlook based on current market sentiment.\n"""
    def _quant_response(self, ticker: str) -> str:
        rsi = 45 + (len(ticker) * 3)
        ma_signal = "ABOVE" if len(ticker) % 2 == 0 else "BELOW"
        return f"""📈 **Quant Analysis for {ticker}**\n\n**Technical Indicators:**\n- RSI (14-day): {rsi} - {'Neutral' if 40 <= rsi <= 60 else 'Overbought' if rsi > 60 else 'Oversold'}\n- 50-day MA: ${120 + len(ticker) * 5}\n- 200-day MA: ${100 + len(ticker) * 3}\n- Price Position: {ma_signal} moving averages\n\n**Pattern Recognition:**\n- Trend: {'Uptrend' if ma_signal == 'ABOVE' else 'Downtrend'}\n- Support Level: ${95 + len(ticker) * 2}\n- Resistance Level: ${135 + len(ticker) * 4}\n\n**Technical Signal:** {'Buy' if ma_signal == 'ABOVE' else 'Sell'} signal based on moving average crossover.\n"""
    def _manager_response(self, ticker: str, context: str) -> str:
        return f"""🎯 **Manager Consolidation for {ticker}**\n\n**Analysis Summary:**\nI've reviewed both the Researcher's sentiment analysis and the Quant's technical indicators.\n\n**Consensus Building:**\n- Fundamental sentiment and technical signals are being evaluated\n- Risk management parameters are being calculated\n- Position sizing will be determined based on portfolio balance\n\n**Next Step:** Calculating risk metrics using the Risk Calculator tool...\n"""
