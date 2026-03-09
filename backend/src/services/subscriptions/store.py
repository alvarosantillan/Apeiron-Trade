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
            "cancelAtPeriodEnd": False,
            "updatedAt": datetime.now(timezone.utc),
        }
        self._status_by_user[user_id] = default
        return default

    def set_status(self, user_id: str, plan_code: str, status: str, cancel_at_period_end: bool = False) -> dict:
        updated = {
            "userId": user_id,
            "planCode": plan_code,
            "status": status,
            "cancelAtPeriodEnd": cancel_at_period_end,
            "updatedAt": datetime.now(timezone.utc),
        }
        self._status_by_user[user_id] = updated
        return updated


subscription_store = SubscriptionStore()
