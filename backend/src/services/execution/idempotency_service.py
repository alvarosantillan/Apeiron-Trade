class IdempotencyService:
    def __init__(self) -> None:
        self._seen: dict[str, dict] = {}

    def check_and_mark(self, user_id: str, request_id: str) -> bool:
        key = f"{user_id}:{request_id}"
        if key in self._seen:
            return False
        self._seen[key] = {}
        return True

    def save(self, user_id: str, request_id: str, payload: dict) -> None:
        key = f"{user_id}:{request_id}"
        self._seen[key] = payload

    def get(self, user_id: str, request_id: str) -> dict | None:
        key = f"{user_id}:{request_id}"
        value = self._seen.get(key)
        if not value:
            return None
        return value


idempotency_service = IdempotencyService()
