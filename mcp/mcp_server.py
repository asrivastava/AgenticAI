"""
MCP Server for Trading Tools
Implements risk calculation using Model Context Protocol
"""
from fastmcp.server import Server

from mcp.types import Tool, TextContent
from tools.calculate_risk import calculate_risk
import json

# Initialize MCP Server
app = Server("trading-tools")

def risk_input_schema():
    """Schema for risk calculation tool input"""
    return {
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

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available trading tools"""
    return [
        Tool(
            name="calculate_risk",
            description="Calculate position size and risk metrics for a trade using 2% risk rule",
            inputSchema=risk_input_schema()
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
