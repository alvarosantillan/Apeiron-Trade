from datetime import datetime, timezone

from services.execution.execution_repository import execution_repository
from services.execution.state_machine import can_transition


def reconcile_execution(execution_id: str) -> dict | None:
    current = execution_repository.get_execution(execution_id)
    if not current:
        return None

    if current["status"] != "PENDING_RECONCILIATION":
        return current

    if can_transition(current["status"], "EXECUTED"):
        current["status"] = "EXECUTED"
        current["executedQty"] = current["quantity"]
        current["executedPrice"] = current["limitPrice"] or current["quantity"]
        current["updatedAt"] = datetime.now(timezone.utc)
        execution_repository.update_execution(current)

    return current
