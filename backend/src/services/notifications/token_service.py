from datetime import datetime, timezone
from uuid import uuid4


class NotificationTokenService:
    def __init__(self) -> None:
        self._by_user: dict[str, list[dict]] = {}

    def upsert(self, user_id: str, device_id: str, platform: str, push_token: str) -> dict:
        items = self._by_user.get(user_id, [])
        existing = next((x for x in items if x["deviceId"] == device_id), None)
        if existing:
            existing["platform"] = platform
            existing["pushToken"] = push_token
            existing["isActive"] = True
            existing["updatedAt"] = datetime.now(timezone.utc)
            return existing

        created = {
            "id": str(uuid4()),
            "deviceId": device_id,
            "platform": platform,
            "pushToken": push_token,
            "isActive": True,
            "updatedAt": datetime.now(timezone.utc),
        }
        items.append(created)
        self._by_user[user_id] = items
        return created

    def list_active(self, user_id: str) -> list[dict]:
        return [x for x in self._by_user.get(user_id, []) if x["isActive"]]

    def deactivate_by_token(self, user_id: str, push_token: str) -> None:
        for item in self._by_user.get(user_id, []):
            if item["pushToken"] == push_token:
                item["isActive"] = False
                item["updatedAt"] = datetime.now(timezone.utc)


notification_token_service = NotificationTokenService()
