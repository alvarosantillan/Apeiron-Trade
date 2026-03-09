from services.execution.execution_repository import execution_repository
from services.history.filter_validator import validate_filters
from services.history.pagination_service import decode_cursor, encode_cursor


def _to_item(execution: dict) -> dict:
    return {
        "tradeId": execution["id"],
        "symbol": execution["symbol"],
        "side": execution["side"],
        "status": execution["status"],
        "executedPrice": execution.get("executedPrice"),
        "quantity": execution["quantity"],
        "isSimulation": execution["executionType"] == "PAPER",
        "pnl": None,
        "createdAt": execution["createdAt"],
    }


def list_history(
    user_id: str,
    from_ts: str | None,
    to_ts: str | None,
    status: str | None,
    is_simulation: bool | None,
    limit: int,
    cursor: str | None,
) -> dict:
    parsed_from, parsed_to = validate_filters(from_ts, to_ts, status)

    items = execution_repository.get_all_executions(user_id)

    if parsed_from:
        items = [x for x in items if x["createdAt"] >= parsed_from]
    if parsed_to:
        items = [x for x in items if x["createdAt"] <= parsed_to]
    if status:
        items = [x for x in items if x["status"] == status]
    if is_simulation is not None:
        expected = "PAPER" if is_simulation else "REAL"
        items = [x for x in items if x["executionType"] == expected]

    start = decode_cursor(cursor)
    page = items[start : start + limit]
    next_offset = start + limit
    next_cursor = encode_cursor(next_offset) if next_offset < len(items) else None

    return {"items": [_to_item(x) for x in page], "nextCursor": next_cursor}


def get_trade_detail(user_id: str, trade_id: str) -> dict | None:
    trade = execution_repository.get_execution(trade_id)
    if not trade:
        return None

    if trade not in execution_repository.get_all_executions(user_id):
        return None

    return {
        "tradeId": trade["id"],
        "requestId": trade["requestId"],
        "status": trade["status"],
        "symbol": trade["symbol"],
        "side": trade["side"],
        "quantity": trade["quantity"],
        "executedPrice": trade.get("executedPrice"),
        "isSimulation": trade["executionType"] == "PAPER",
        "failureReason": trade.get("failureReason"),
        "executionTrace": {"mode": trade.get("mode"), "updatedAt": trade.get("updatedAt")},
        "createdAt": trade["createdAt"],
    }
