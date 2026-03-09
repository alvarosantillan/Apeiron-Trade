from datetime import datetime, timezone
from uuid import uuid4

from services.persistence.database import session_scope
from services.persistence.json_utils import make_json_safe
from services.persistence.models.base import AIAgentConfigModel


class AIAgentConfigStore:
    def __init__(self) -> None:
        self._by_user: dict[str, dict] = {}

    def upsert(self, user_id: str, payload: dict) -> dict:
        with session_scope() as session:
            current_row = session.query(AIAgentConfigModel).filter(AIAgentConfigModel.user_id == user_id).first()
            current = current_row.payload if current_row else {}
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
        payload = make_json_safe(config)
        with session_scope() as session:
            row = session.query(AIAgentConfigModel).filter(AIAgentConfigModel.user_id == user_id).first()
            if row:
                row.payload = payload
                row.updated_at = config["updatedAt"]
            else:
                session.add(
                    AIAgentConfigModel(
                        id=config["id"],
                        user_id=user_id,
                        payload=payload,
                        updated_at=config["updatedAt"],
                    )
                )
        return config

    def get(self, user_id: str) -> dict | None:
        with session_scope() as session:
            row = session.query(AIAgentConfigModel).filter(AIAgentConfigModel.user_id == user_id).first()
            if not row:
                return None
            return row.payload


ai_agent_config_store = AIAgentConfigStore()
