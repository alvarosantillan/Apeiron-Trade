MAX_FAILED_ATTEMPTS = 5


class InMemoryLoginProtection:
    def __init__(self) -> None:
        self._failed_by_email: dict[str, int] = {}

    def can_attempt(self, email: str) -> bool:
        return self._failed_by_email.get(email, 0) < MAX_FAILED_ATTEMPTS

    def register_failure(self, email: str) -> None:
        self._failed_by_email[email] = self._failed_by_email.get(email, 0) + 1

    def register_success(self, email: str) -> None:
        self._failed_by_email.pop(email, None)


login_protection = InMemoryLoginProtection()
