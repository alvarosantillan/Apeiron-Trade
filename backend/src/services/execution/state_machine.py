ALLOWED_TRANSITIONS = {
    "RECEIVED": {"VALIDATED", "BLOCKED"},
    "VALIDATED": {"SUBMITTED", "BLOCKED"},
    "SUBMITTED": {"EXECUTED", "FAILED", "PENDING_RECONCILIATION"},
    "PENDING_RECONCILIATION": {"EXECUTED", "FAILED"},
    "BLOCKED": set(),
    "EXECUTED": set(),
    "FAILED": set(),
    "CANCELLED": set(),
}


def can_transition(current_status: str, target_status: str) -> bool:
    return target_status in ALLOWED_TRANSITIONS.get(current_status, set())
