from datetime import datetime, timezone
from uuid import uuid4

from services.persistence.database import session_scope
from services.persistence.json_utils import make_json_safe
from services.persistence.models.base import NotificationDeliveryModel


class NotificationHistoryStore:
    def __init__(self) -> None:
        self._by_user: dict[str, list[dict]] = {}

    def add(self, user_id: str, item: dict) -> dict:
        record = {
            "eventId": item["eventId"],
            "category": item["category"],
            "priority": item["priority"],
            "title": item["title"],
            "message": item["message"],
            "status": item["status"],
            "referenceId": item.get("referenceId"),
            "createdAt": item.get("createdAt", datetime.now(timezone.utc)),
        }
        payload = make_json_safe(record)
        with session_scope() as session:
            session.add(
                NotificationDeliveryModel(
                    id=str(uuid4()),
                    user_id=user_id,
                    event_id=record["eventId"],
                    payload=payload,
                    created_at=record["createdAt"],
                )
            )
        return payload

    def list(self, user_id: str, limit: int = 20, category: str | None = None) -> list[dict]:
        with session_scope() as session:
            items = [x.payload for x in session.query(NotificationDeliveryModel).filter(NotificationDeliveryModel.user_id == user_id).all()]
        if category:
            items = [x for x in items if x["category"] == category]
        items.sort(key=lambda item: item.get("createdAt"), reverse=True)
        return items[:limit]


notification_history_store = NotificationHistoryStore()
