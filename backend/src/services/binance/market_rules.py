def validate_order_shape(side: str, order_type: str, quantity: float, limit_price: float | None) -> None:
    if side not in {"BUY", "SELL"}:
        raise ValueError("invalid_side")
    if order_type not in {"MARKET", "LIMIT"}:
        raise ValueError("invalid_order_type")
    if quantity <= 0:
        raise ValueError("invalid_quantity")
    if order_type == "LIMIT" and (limit_price is None or limit_price <= 0):
        raise ValueError("invalid_limit_price")
