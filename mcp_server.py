"""
MCP Server for Trading Tools
Implements risk calculation using Model Context Protocol
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


# Initialize MCP Server
app = Server("trading-tools")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available trading tools"""
    return [
        Tool(
            name="calculate_risk",
            description="Calculate position size and risk metrics for a trade using 2% risk rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol"
                    },
                    "price": {
                        "type": "number",
                        "description": "Current stock price"
                    },
                    "balance": {
                        "type": "number",
                        "description": "Account balance"
                    },
                    "stop_loss_percent": {
                        "type": "number",
                        "description": "Stop loss percentage (default: 10)",
                        "default": 10.0
                    }
                },
                "required": ["ticker", "price", "balance"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute trading tools"""
    
    if name == "calculate_risk":
        return await calculate_risk(
            ticker=arguments["ticker"],
            price=arguments["price"],
            balance=arguments["balance"],
            stop_loss_percent=arguments.get("stop_loss_percent", 10.0)
        )
    
    raise ValueError(f"Unknown tool: {name}")


async def calculate_risk(ticker: str, price: float, balance: float, stop_loss_percent: float = 10.0) -> list[TextContent]:
    """
    Calculate position size using 2% risk rule
    
    Args:
        ticker: Stock ticker symbol
        price: Current stock price
        balance: Account balance
        stop_loss_percent: Stop loss percentage (default 10%)
    
    Returns:
        Formatted risk calculation results
    """
    
    # Apply 2% risk rule
    risk_per_trade = balance * 0.02
    
    # Calculate stop loss price
    stop_loss_price = price * (1 - stop_loss_percent / 100)
    
    # Calculate risk per share
    risk_per_share = price - stop_loss_price
    
    # Calculate position size
    if risk_per_share > 0:
        position_size = int(risk_per_trade / risk_per_share)
    else:
        position_size = 0
    
    # Calculate total investment
    total_investment = position_size * price
    
    # Calculate actual max loss
    max_loss = position_size * risk_per_share
    
    # Build result
    result = {
        "ticker": ticker,
        "account_balance": balance,
        "risk_per_trade": risk_per_trade,
        "risk_percentage": 2.0,
        "current_price": price,
        "stop_loss_price": round(stop_loss_price, 2),
        "stop_loss_percent": stop_loss_percent,
        "position_size": position_size,
        "total_investment": round(total_investment, 2),
        "max_loss": round(max_loss, 2),
        "risk_reward_ratio": "1:2"  # Assuming 2x reward target
    }
    
    # Format output
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


def main():
    """Run the MCP server"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
