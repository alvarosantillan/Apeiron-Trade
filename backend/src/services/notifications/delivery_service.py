from services.notifications.dedup_service import notification_dedup_service
from services.notifications.delivery_status_service import now_utc, transition_status
from services.notifications.history_store import notification_history_store
from services.notifications.preference_store import notification_preference_store
from services.notifications.priority_policy import should_override_preferences
from services.notifications.push_provider import push_provider
from services.notifications.retry_policy import retry_policy_service
from services.notifications.token_service import notification_token_service


def dispatch_notification(user_id: str, payload: dict) -> list[dict]:
    category = payload["category"]
    if not notification_preference_store.is_enabled(user_id, category) and not should_override_preferences(payload["priority"]):
        return []

    deliveries: list[dict] = []
    for token in notification_token_service.list_active(user_id):
        if not notification_dedup_service.should_deliver(user_id, token["deviceId"], payload["eventId"]):
            continue

        status = "QUEUED"
        attempts = 0
        while True:
            ok, error_code = push_provider.send(token["pushToken"], payload["title"], payload["message"])
            if ok:
                status = transition_status(status, "SENT")
                status = transition_status(status, "DELIVERED")
                break

            if error_code == "invalid_token":
                notification_token_service.deactivate_by_token(user_id, token["pushToken"])
                status = transition_status(status, "DROPPED")
                break

            attempts += 1
            if retry_policy_service.should_retry(attempts, error_code or ""):
                continue
            status = transition_status(status, "FAILED")
            break

        item = notification_history_store.add(
            user_id,
            {
                "eventId": payload["eventId"],
                "category": category,
                "priority": payload["priority"],
                "title": payload["title"],
                "message": payload["message"],
                "status": status,
                "referenceId": payload.get("referenceId"),
                "createdAt": now_utc(),
            },
        )
        deliveries.append(item)

    return deliveries
