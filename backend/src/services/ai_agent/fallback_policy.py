from datetime import datetime, timezone


def fallback_hold_decision(symbol: str, timeframe: str, reason: str) -> dict:
    return {
        "action": "HOLD",
        "confidence": 1.0,
        "riskLevel": "LOW",
        "status": "FALLBACK_HOLD",
        "symbol": symbol,
        "timeframe": timeframe,
        "reasoning": "Fallback hold applied",
        "fallbackReason": reason,
        "decisionTs": datetime.now(timezone.utc),
    }
