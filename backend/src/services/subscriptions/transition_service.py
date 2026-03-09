from services.subscriptions.store import subscription_store


def transition_plan(user_id: str, target_plan_code: str) -> dict:
    target = target_plan_code.lower()
    if target not in {"free", "plus", "premium"}:
        raise ValueError("invalid_target_plan")

    return subscription_store.set_status(user_id, target, "active", cancel_at_period_end=False)


def cancel_subscription(user_id: str, cancel_at_period_end: bool) -> dict:
    current = subscription_store.get_status(user_id)

    if cancel_at_period_end:
        return subscription_store.set_status(
            user_id,
            current["planCode"],
            current["status"],
            cancel_at_period_end=True,
        )

    return subscription_store.set_status(user_id, "free", "active", cancel_at_period_end=False)
