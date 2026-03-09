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


ai_decision_repository = AIDecisionRepository()
