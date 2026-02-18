"""
Researcher Agent Tool
"""
from mcp.types import TextContent

async def researcher_analysis(ticker: str) -> list[TextContent]:
    """
    Mock researcher agent for sentiment analysis
    """
    sentiment = "BULLISH" if len(ticker) % 2 == 0 else "BEARISH"
    confidence = 75 + (len(ticker) * 2)
    output = f"""
📊 **Researcher Analysis for {ticker}**

**Market Sentiment:** {sentiment}
**Confidence Level:** {confidence}%

**Key Findings:**
- Recent news sentiment indicates {sentiment.lower()} momentum
- Social media mentions trending {'upward' if sentiment == 'BULLISH' else 'downward'}
- Analyst ratings: {'Majority Buy recommendations' if sentiment == 'BULLISH' else 'Mixed with caution signals'}

**Recommendation:** {sentiment.capitalize()} outlook based on current market sentiment.
"""
    return [TextContent(type="text", text=output)]
