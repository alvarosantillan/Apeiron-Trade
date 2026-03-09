from services.binance.client import binance_client
from services.binance.market_rules import validate_order_shape
from services.execution.execution_repository import execution_repository


class ExecutionError(ValueError):
    pass


class BalanceStore:
    def __init__(self) -> None:
        self._balance: dict[str, float] = {}

    def get_balance(self, user_id: str) -> float:
        return self._balance.get(user_id, 1000.0)

    def set_balance(self, user_id: str, amount: float) -> None:
        self._balance[user_id] = amount


balance_store = BalanceStore()


def execute_order(user_id: str, payload: dict) -> dict:
    validate_order_shape(payload["side"], payload["order_type"], payload["quantity"], payload.get("limit_price"))

    if not binance_client.validate_symbol(payload["symbol"]):
        raise ExecutionError("invalid_symbol")

    execution_type = "REAL"
    status = "executed"

    if payload["side"] == "BUY":
        current_balance = balance_store.get_balance(user_id)
        required = payload["quantity"]
        if required > current_balance:
            result = {
                "request_id": payload["request_id"],
                "status": "failed",
                "execution_type": execution_type,
                "symbol": payload["symbol"],
                "side": payload["side"],
                "quantity": payload["quantity"],
                "message": "insufficient balance",
            }
            execution_repository.add_execution(user_id, result)
            return result

        balance_store.set_balance(user_id, current_balance - required)

    result = {
        "request_id": payload["request_id"],
        "status": status,
        "execution_type": execution_type,
        "symbol": payload["symbol"],
        "side": payload["side"],
        "quantity": payload["quantity"],
        "message": "order processed",
    }
    execution_repository.add_execution(user_id, result)
    return result
