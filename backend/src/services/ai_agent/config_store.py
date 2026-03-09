from datetime import datetime, timezone
from uuid import uuid4


class AIAgentConfigStore:
    def __init__(self) -> None:
        self._by_user: dict[str, dict] = {}

    def upsert(self, user_id: str, payload: dict) -> dict:
        current = self._by_user.get(user_id, {})
        config = {
            "id": current.get("id", str(uuid4())),
            "provider": payload["provider"],
            "apiKey": payload["apiKey"],
            "strategyId": payload["strategyId"],
            "riskProfile": payload["riskProfile"],
            "mode": payload["mode"],
            "isActive": payload.get("isActive", True),
            "updatedAt": datetime.now(timezone.utc),
        }
        self._by_user[user_id] = config
        return config

    def get(self, user_id: str) -> dict | None:
        return self._by_user.get(user_id)


ai_agent_config_store = AIAgentConfigStore()
