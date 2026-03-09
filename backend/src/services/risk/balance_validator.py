from services.execution.execute_order_service import balance_store


def has_sufficient_balance(user_id: str, quantity: float) -> bool:
    return balance_store.get_balance(user_id) >= quantity
