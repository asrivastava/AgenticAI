"""
Test script for Multi-Agent Trading Assistant
"""
from agents import TradingAgents


def test_multi_agent_system():
    """Test the multi-agent trading system"""
    print("=" * 70)
    print("Testing Multi-Agent Trading Assistant")
    print("=" * 70)
    
    # Initialize system
    print("\n1. Initializing Trading System...")
    system = TradingAgents()
    print("   ✅ System initialized")
    
    # Test analysis
    test_tickers = ["AAPL", "TSLA", "MSFT"]
    
    for ticker in test_tickers:
        print(f"\n{'=' * 70}")
        print(f"2. Testing Analysis for {ticker}")
        print("=" * 70)
        
        result = system.analyze(ticker, f"Analyze {ticker} for trading")
        
        print(f"\n📊 Researcher Analysis:")
        print("-" * 70)
        print(result["researcher_analysis"][:200] + "...")
        
        print(f"\n📈 Quant Analysis:")
        print("-" * 70)
        print(result["quant_analysis"][:200] + "...")
        
        print(f"\n🎯 Manager Recommendation:")
        print("-" * 70)
        final_msg = result["messages"][-1]
        print(final_msg.content[:300] + "...")
        
        print(f"\n✅ Analysis complete for {ticker}")
    
    print(f"\n{'=' * 70}")
    print("✅ All tests completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    test_multi_agent_system()
