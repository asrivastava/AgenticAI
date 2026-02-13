# Multi-Agent Trading Assistant - Workflow

## Agent Collaboration Flow

```mermaid
graph TD
    Start([START]) --> Researcher[Researcher Agent]
    Researcher --> |Sentiment Analysis| Quant[Quant Agent]
    Quant --> |Technical Analysis| Manager[Manager Agent]
    Manager --> |Risk Calculation| End([END])
    
    style Start fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Researcher fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style Quant fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    style Manager fill:#e8f5e9,stroke:#388e3c,stroke-width:3px
    style End fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

## Process Description

1. **START**: User provides a ticker symbol (e.g., AAPL, TSLA, MSFT)
2. **Researcher Agent**: Analyzes market sentiment, news, and analyst recommendations
3. **Quant Agent**: Performs technical analysis with RSI, moving averages, and chart patterns
4. **Manager Agent**: Consolidates findings, calculates risk using 2% rule, and generates final recommendation
5. **END**: Complete trade setup with entry/exit points and position sizing

## Agent Details

### Researcher Agent (Orange)
- Market sentiment analysis
- News aggregation
- Social media trends
- Analyst ratings

### Quant Agent (Purple)
- RSI (Relative Strength Index)
- Moving averages (50-day, 200-day)
- Support/resistance levels
- Chart pattern recognition

### Manager Agent (Green)
- Consolidates all findings
- Calls risk calculator tool
- 2% risk rule application
- Position sizing calculation
- Final recommendation
