from services.execution.execution_repository import execution_repository


class IdempotencyService:
    def __init__(self) -> None:
        self._seen: dict[str, dict] = {}

    def check_and_mark(self, user_id: str, request_id: str) -> bool:
        if execution_repository.get_by_request_id(user_id, request_id):
            return False
        return True

    def save(self, user_id: str, request_id: str, payload: dict) -> None:
        key = f"{user_id}:{request_id}"
        self._seen[key] = payload

    def get(self, user_id: str, request_id: str) -> dict | None:
        persisted = execution_repository.get_by_request_id(user_id, request_id)
        if persisted:
            return persisted
        key = f"{user_id}:{request_id}"
        return self._seen.get(key)


idempotency_service = IdempotencyService()
