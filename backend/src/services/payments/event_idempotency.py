class EventIdempotencyStore:
    def __init__(self) -> None:
        self._seen_event_ids: set[str] = set()

    def is_processed(self, event_id: str) -> bool:
        return event_id in self._seen_event_ids

    def mark_processed(self, event_id: str) -> None:
        self._seen_event_ids.add(event_id)


idempotency_store = EventIdempotencyStore()
