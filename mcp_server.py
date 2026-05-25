# mcp_server.py

from typing import List, Dict, Any
import random

from fastmcp import FastMCP
from fastmcp.tools import tool


app = FastMCP("trading-tools")


@tool()
def fetch_price_data(ticker: str) -> Dict[str, Any]:
    """
    Fetch price data for a ticker.
    In this demo, returns hard-coded / synthetic data.
    """
    # In real life, call your data provider here.
    prices = [100 + random.uniform(-1, 1) for _ in range(30)]
    return {
        "ticker": ticker,
        "prices": prices,
    }


@tool()
def analyze_prices(prices: List[float]) -> Dict[str, Any]:
    """
    Analyze price data and return a simple trend/volatility signal.
    """
    if not prices:
        return {
            "trend": "unknown",
            "volatility": "low",
            "confidence": 0.0,
        }

    # Very naive demo logic
    first = prices[0]
    last = prices[-1]
    change = (last - first) / first if first != 0 else 0.0

    trend = "up" if change > 0.01 else "down" if change < -0.01 else "sideways"

    # Fake volatility classification
    max_p = max(prices)
    min_p = min(prices)
    vol_range = (max_p - min_p) / first if first != 0 else 0.0

    if vol_range > 0.05:
        volatility = "high"
    elif vol_range > 0.02:
        volatility = "medium"
    else:
        volatility = "low"

    confidence = min(0.99, max(0.1, abs(change) * 10))

    return {
        "trend": trend,
        "volatility": volatility,
        "confidence": confidence,
    }


if __name__ == "__main__":
    # Run the MCP server; OpenAI / client side must be configured
    # to discover and use this MCP server.
    app.run()
