from datetime import datetime, timezone


class InMemoryAuthAudit:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def log(self, action: str, user_id: str | None = None, email: str | None = None, outcome: str = "success") -> None:
        self.events.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "user_id": user_id,
                "email": email,
                "outcome": outcome,
            }
        )


auth_audit = InMemoryAuthAudit()
