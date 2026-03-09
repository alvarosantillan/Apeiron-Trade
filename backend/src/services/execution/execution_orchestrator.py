from datetime import datetime, timezone
from uuid import uuid4

from services.binance.credential_service import credential_store
from services.counters.weekly_counter_service import weekly_counter_service
from services.execution.block_reason_mapper import map_block_reason
from services.execution.execution_repository import execution_repository
from services.execution.idempotency_service import idempotency_service
from services.execution.state_machine import can_transition
from services.risk.balance_validator import has_sufficient_balance
from services.subscriptions.store import subscription_store
from services.validation.plan_limit_validator import plan_limit_validator


def _base_response(payload: dict) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": str(uuid4()),
        "requestId": payload["requestId"],
        "symbol": payload["symbol"],
        "side": payload["side"],
        "orderType": payload["orderType"],
        "quantity": payload["quantity"],
        "limitPrice": payload.get("limitPrice"),
        "executionType": "PAPER" if payload["isSimulation"] else "REAL",
        "mode": "AUTOMATIC" if payload.get("source") == "AI_AGENT" else "MANUAL",
        "status": "RECEIVED",
        "executedPrice": None,
        "executedQty": None,
        "blockedReason": None,
        "failureReason": None,
        "createdAt": now,
        "updatedAt": now,
    }


def create_execution(user_id: str, payload: dict) -> dict:
    existing = idempotency_service.get(user_id, payload["requestId"])
    if existing:
        return existing

    execution = _base_response(payload)

    if not payload["isSimulation"] and not credential_store.has_active_credentials(user_id):
        execution["status"] = "BLOCKED"
        execution["blockedReason"] = map_block_reason("credentials")
        execution_repository.add_execution(user_id, execution)
        idempotency_service.save(user_id, payload["requestId"], execution)
        return execution

    plan_code = subscription_store.get_status(user_id)["planCode"]
    if not payload["isSimulation"] and not plan_limit_validator.can_execute_real(user_id, plan_code):
        execution["status"] = "BLOCKED"
        execution["blockedReason"] = map_block_reason("limit")
        execution_repository.add_execution(user_id, execution)
        idempotency_service.save(user_id, payload["requestId"], execution)
        return execution

    if not payload["isSimulation"] and not has_sufficient_balance(user_id, payload["quantity"]):
        execution["status"] = "BLOCKED"
        execution["blockedReason"] = map_block_reason("balance")
        execution_repository.add_execution(user_id, execution)
        idempotency_service.save(user_id, payload["requestId"], execution)
        return execution

    if can_transition("RECEIVED", "VALIDATED"):
        execution["status"] = "VALIDATED"

    if can_transition(execution["status"], "SUBMITTED"):
        execution["status"] = "SUBMITTED"

    if payload["isSimulation"]:
        execution["status"] = "EXECUTED"
        execution["executedQty"] = payload["quantity"]
        execution["executedPrice"] = payload.get("limitPrice") or payload["quantity"]
    elif payload["symbol"] == "TIMEOUTUSDT":
        execution["status"] = "PENDING_RECONCILIATION"
    else:
        execution["status"] = "EXECUTED"
        execution["executedQty"] = payload["quantity"]
        execution["executedPrice"] = payload.get("limitPrice") or payload["quantity"]
        weekly_counter_service.increment_real(user_id, plan_code)

    execution["updatedAt"] = datetime.now(timezone.utc)
    execution_repository.add_execution(user_id, execution)
    idempotency_service.save(user_id, payload["requestId"], execution)
    return execution
