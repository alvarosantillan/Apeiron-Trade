from datetime import datetime, timezone


def transition_status(current: str, target: str) -> str:
    allowed = {
        "QUEUED": {"SENT", "FAILED", "DROPPED"},
        "SENT": {"DELIVERED", "FAILED"},
        "FAILED": {"SENT", "DROPPED"},
        "DELIVERED": set(),
        "DROPPED": set(),
    }
    if target in allowed.get(current, set()):
        return target
    return current


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
