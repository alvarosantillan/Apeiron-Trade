from datetime import datetime, timezone


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
        if user_id not in self._by_user:
            self._by_user[user_id] = []
        self._by_user[user_id].insert(0, record)
        return record

    def list(self, user_id: str, limit: int = 20, category: str | None = None) -> list[dict]:
        items = self._by_user.get(user_id, [])
        if category:
            items = [x for x in items if x["category"] == category]
        return items[:limit]


notification_history_store = NotificationHistoryStore()
