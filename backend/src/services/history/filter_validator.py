from datetime import datetime


VALID_STATUS = {"EXECUTED", "FAILED", "BLOCKED", "CANCELLED"}


def validate_filters(from_ts: str | None, to_ts: str | None, status: str | None) -> tuple[datetime | None, datetime | None]:
    parsed_from = datetime.fromisoformat(from_ts.replace("Z", "+00:00")) if from_ts else None
    parsed_to = datetime.fromisoformat(to_ts.replace("Z", "+00:00")) if to_ts else None

    if status and status not in VALID_STATUS:
        raise ValueError("invalid_status")
    if parsed_from and parsed_to and parsed_from > parsed_to:
        raise ValueError("invalid_range")

    return parsed_from, parsed_to
