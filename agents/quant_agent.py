"""
Quant Agent Tool
"""
from mcp.types import TextContent

async def quant_analysis(ticker: str) -> list[TextContent]:
    """
    Mock quant agent for technical analysis
    """
    rsi = 45 + (len(ticker) * 3)
    ma_signal = "ABOVE" if len(ticker) % 2 == 0 else "BELOW"
    output = f"""
📈 **Quant Analysis for {ticker}**

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
    return [TextContent(type="text", text=output)]
