class IdempotencyService:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def check_and_mark(self, user_id: str, request_id: str) -> bool:
        key = f"{user_id}:{request_id}"
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


idempotency_service = IdempotencyService()
