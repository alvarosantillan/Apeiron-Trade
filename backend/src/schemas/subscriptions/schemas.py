from datetime import datetime
from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    planCode: str


class CheckoutResponse(BaseModel):
    checkoutId: str
    checkoutUrl: str
    provider: str


class SubscriptionStatusResponse(BaseModel):
    userId: str
    planCode: str
    status: str
    cancelAtPeriodEnd: bool = False
    updatedAt: datetime


class TransitionRequest(BaseModel):
    targetPlanCode: str


class CancelRequest(BaseModel):
    cancelAtPeriodEnd: bool = True


class WebhookRequest(BaseModel):
    eventId: str
    externalReference: str
    eventType: str
    status: str
