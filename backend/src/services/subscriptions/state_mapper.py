def map_payment_event_to_subscription_status(event_type: str, status: str) -> str:
    if event_type == "payment" and status == "approved":
        return "active"
    if event_type == "payment" and status in {"rejected", "cancelled"}:
        return "past_due"
    return "pending"
