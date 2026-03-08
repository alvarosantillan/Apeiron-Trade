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
    updatedAt: datetime


class WebhookRequest(BaseModel):
    eventId: str
    externalReference: str
    eventType: str
    status: str
