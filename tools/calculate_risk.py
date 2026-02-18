"""
Risk calculation tool for MCP server
"""
from mcp.types import TextContent

async def calculate_risk(ticker: str, price: float, balance: float, stop_loss_percent: float = 10.0) -> list[TextContent]:
    """
    Calculate position size using 2% risk rule
    """
    risk_per_trade = balance * 0.02
    stop_loss_price = price * (1 - stop_loss_percent / 100)
    risk_per_share = price - stop_loss_price
    position_size = int(risk_per_trade / risk_per_share) if risk_per_share > 0 else 0
    total_investment = position_size * price
    max_loss = position_size * risk_per_share
    output = f"""
💰 **Risk Calculator Results for {ticker}**

**Portfolio Parameters:**
- Account Balance: ${balance:,.2f}
- Risk Per Trade (2% Rule): ${risk_per_trade:,.2f}

**Trade Setup:**
- Current Price: ${price:.2f}
- Stop Loss Price: ${stop_loss_price:.2f} ({stop_loss_percent}% below)
- Risk Per Share: ${risk_per_share:.2f}

**Position Sizing:**
- Recommended Shares: {position_size}
- Total Investment: ${total_investment:,.2f}
- Portfolio Allocation: {(total_investment/balance*100):.1f}%

**Risk Management:**
- Maximum Loss: ${max_loss:,.2f}
- Risk/Reward Ratio: 1:2
- Take Profit Target: ${price * 1.20:.2f} (20% gain)

✅ **Position sized to risk exactly 2% of portfolio balance**
"""
    return [
        TextContent(
            type="text",
            text=output
        )
    ]
