from services.binance.client import binance_client
from services.binance.market_rules import validate_order_shape
from services.execution.execution_repository import execution_repository


class PaperExecutionError(ValueError):
    pass


def execute_paper_order(payload: dict) -> dict:
    validate_order_shape(payload["side"], payload["order_type"], payload["quantity"], payload.get("limit_price"))
    if not binance_client.validate_symbol(payload["symbol"]):
        raise PaperExecutionError("invalid_symbol")

    result = {
        "request_id": payload["request_id"],
        "status": "executed",
        "execution_type": "PAPER",
        "symbol": payload["symbol"],
        "side": payload["side"],
        "quantity": payload["quantity"],
        "message": "paper order processed",
    }
    execution_repository.add(result)
    return result
