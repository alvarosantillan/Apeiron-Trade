def build_strategy_prompt(strategy_id: str, risk_profile: str, symbol: str, timeframe: str) -> str:
    return (
        f"strategy={strategy_id}; risk={risk_profile}; symbol={symbol}; timeframe={timeframe}; "
        "return structured decision"
    )
