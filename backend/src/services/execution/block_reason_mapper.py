def map_block_reason(code: str) -> str:
    mapping = {
        "limit": "weekly_limit_exceeded",
        "balance": "insufficient_balance",
        "credentials": "missing_active_binance_credentials",
    }
    return mapping.get(code, "blocked_by_policy")
