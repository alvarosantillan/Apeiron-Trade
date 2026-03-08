from fastapi import APIRouter, Header, HTTPException, status

from schemas.subscriptions.schemas import (
    CheckoutRequest,
    CheckoutResponse,
    SubscriptionStatusResponse,
    WebhookRequest,
)
from services.payments.event_idempotency import idempotency_store
from services.payments.mercadopago_client import mp_client
from services.payments.webhook_validator import validate_signature
from services.subscriptions.state_mapper import map_payment_event_to_subscription_status
from services.subscriptions.store import subscription_store

router = APIRouter(prefix="/v1/subscriptions", tags=["subscriptions"])


@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(payload: CheckoutRequest, x_user_id: str = Header(default="demo-user")) -> CheckoutResponse:
    plan_code = payload.planCode.lower()
    if plan_code not in {"plus", "premium"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid plan for checkout")

    checkout = mp_client.create_checkout(x_user_id, plan_code)
    return CheckoutResponse(
        checkoutId=checkout["checkoutId"],
        checkoutUrl=checkout["checkoutUrl"],
        provider=checkout["provider"],
    )


@router.get("/status", response_model=SubscriptionStatusResponse)
def get_subscription_status(x_user_id: str = Header(default="demo-user")) -> SubscriptionStatusResponse:
    current = subscription_store.get_status(x_user_id)
    return SubscriptionStatusResponse(**current)


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
def process_webhook(payload: WebhookRequest, x_signature: str | None = Header(default=None)) -> None:
    if not validate_signature(x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid webhook signature")

    if idempotency_store.is_processed(payload.eventId):
        return

    try:
        user_id, plan_code, _ = payload.externalReference.split(":", 2)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid external reference")

    mapped_status = map_payment_event_to_subscription_status(payload.eventType, payload.status)
    if mapped_status in {"active", "past_due"}:
        subscription_store.set_status(user_id, plan_code, mapped_status)

    idempotency_store.mark_processed(payload.eventId)
