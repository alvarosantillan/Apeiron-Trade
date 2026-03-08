from datetime import datetime, timezone


class SubscriptionStore:
    def __init__(self) -> None:
        self._status_by_user: dict[str, dict] = {}

    def get_status(self, user_id: str) -> dict:
        existing = self._status_by_user.get(user_id)
        if existing:
            return existing
        default = {
            "userId": user_id,
            "planCode": "free",
            "status": "active",
            "updatedAt": datetime.now(timezone.utc),
        }
        self._status_by_user[user_id] = default
        return default

    def set_status(self, user_id: str, plan_code: str, status: str) -> dict:
        updated = {
            "userId": user_id,
            "planCode": plan_code,
            "status": status,
            "updatedAt": datetime.now(timezone.utc),
        }
        self._status_by_user[user_id] = updated
        return updated


subscription_store = SubscriptionStore()
