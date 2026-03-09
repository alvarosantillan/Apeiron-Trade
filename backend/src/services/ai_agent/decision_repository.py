from datetime import datetime, timezone
from uuid import uuid4


class AIDecisionRepository:
    def __init__(self) -> None:
        self._by_user: dict[str, list[dict]] = {}

    def add(self, user_id: str, decision: dict) -> dict:
        record = {
            "id": str(uuid4()),
            "action": decision["action"],
            "confidence": decision["confidence"],
            "riskLevel": decision["riskLevel"],
            "status": decision["status"],
            "symbol": decision["symbol"],
            "timeframe": decision["timeframe"],
            "reasoning": decision["reasoning"],
            "fallbackReason": decision.get("fallbackReason"),
            "decisionTs": decision.get("decisionTs", datetime.now(timezone.utc)),
        }
        if user_id not in self._by_user:
            self._by_user[user_id] = []
        self._by_user[user_id].insert(0, record)
        return record

    def list(self, user_id: str, limit: int = 20) -> list[dict]:
        return self._by_user.get(user_id, [])[:limit]

    def find_recent_equivalent(
        self,
        user_id: str,
        symbol: str,
        timeframe: str,
        action: str,
        window_seconds: int = 300,
    ) -> dict | None:
        now = datetime.now(timezone.utc)
        for item in self._by_user.get(user_id, []):
            age = (now - item["decisionTs"]).total_seconds()
            if age > window_seconds:
                continue
            if (
                item["symbol"] == symbol
                and item["timeframe"] == timeframe
                and item["action"] == action
                and item["status"] in {"PENDING_APPROVAL", "EXECUTED"}
            ):
                return item
        return None


ai_decision_repository = AIDecisionRepository()
