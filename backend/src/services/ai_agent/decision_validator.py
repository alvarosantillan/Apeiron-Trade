def validate_decision_shape(decision: dict) -> None:
    required = {"action", "confidence", "riskLevel", "status", "symbol", "timeframe", "reasoning"}
    missing = required.difference(decision.keys())
    if missing:
        raise ValueError("invalid_decision_shape")

    if decision["action"] not in {"BUY", "SELL", "HOLD"}:
        raise ValueError("invalid_action")

    confidence = decision["confidence"]
    if not isinstance(confidence, (float, int)) or confidence < 0 or confidence > 1:
        raise ValueError("invalid_confidence")
