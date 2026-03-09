CATEGORIES = {"TRADING", "SUBSCRIPTION", "SECURITY", "SYSTEM", "MARKETING"}


class NotificationPreferenceStore:
    def __init__(self) -> None:
        self._by_user: dict[str, dict[str, bool]] = {}

    def _ensure_user(self, user_id: str) -> dict[str, bool]:
        if user_id not in self._by_user:
            self._by_user[user_id] = {
                "TRADING": True,
                "SUBSCRIPTION": True,
                "SECURITY": True,
                "SYSTEM": True,
                "MARKETING": False,
            }
        return self._by_user[user_id]

    def get_all(self, user_id: str) -> list[dict]:
        current = self._ensure_user(user_id)
        return [{"category": key, "enabled": value} for key, value in current.items()]

    def update(self, user_id: str, items: list[dict]) -> list[dict]:
        current = self._ensure_user(user_id)
        for item in items:
            category = item["category"]
            if category not in CATEGORIES:
                raise ValueError("invalid_category")
            current[category] = item["enabled"]
        return [{"category": key, "enabled": value} for key, value in current.items()]

    def is_enabled(self, user_id: str, category: str) -> bool:
        current = self._ensure_user(user_id)
        return current.get(category, False)


notification_preference_store = NotificationPreferenceStore()
