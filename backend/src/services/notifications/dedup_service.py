class NotificationDedupService:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def should_deliver(self, user_id: str, device_id: str, event_id: str) -> bool:
        key = f"{user_id}:{device_id}:{event_id}"
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


notification_dedup_service = NotificationDedupService()
