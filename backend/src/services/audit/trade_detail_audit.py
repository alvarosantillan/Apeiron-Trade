from datetime import datetime, timezone


class TradeDetailAuditStore:
    def __init__(self) -> None:
        self._events: list[dict] = []

    def log(self, user_id: str, trade_id: str) -> None:
        self._events.append(
            {
                "userId": user_id,
                "tradeId": trade_id,
                "action": "trade_detail_access",
                "createdAt": datetime.now(timezone.utc),
            }
        )


trade_detail_audit_store = TradeDetailAuditStore()
