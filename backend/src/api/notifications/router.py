from fastapi import APIRouter, Depends, Query

from api.middleware.auth_middleware import get_current_user
from schemas.notifications.schemas import (
    DeviceTokenListResponse,
    DeviceTokenResponse,
    EmitNotificationRequest,
    NotificationHistoryResponse,
    PreferencesResponse,
    PreferencesUpdateRequest,
    UpsertDeviceTokenRequest,
)
from services.notifications.delivery_service import dispatch_notification
from services.notifications.history_store import notification_history_store
from services.notifications.preference_store import notification_preference_store
from services.notifications.token_service import notification_token_service

router = APIRouter(prefix="/v1/notifications", tags=["notifications"])


@router.post("/device-tokens", response_model=DeviceTokenResponse)
def upsert_device_token(payload: UpsertDeviceTokenRequest, user: dict = Depends(get_current_user)) -> DeviceTokenResponse:
    stored = notification_token_service.upsert(user["id"], payload.deviceId, payload.platform, payload.pushToken)
    sanitized = {k: v for k, v in stored.items() if k != "pushToken"}
    return DeviceTokenResponse(**sanitized)


@router.get("/device-tokens", response_model=DeviceTokenListResponse)
def list_device_tokens(user: dict = Depends(get_current_user)) -> DeviceTokenListResponse:
    items = [{k: v for k, v in x.items() if k != "pushToken"} for x in notification_token_service.list_active(user["id"])]
    return DeviceTokenListResponse(items=items)


@router.get("/preferences", response_model=PreferencesResponse)
def get_preferences(user: dict = Depends(get_current_user)) -> PreferencesResponse:
    return PreferencesResponse(items=notification_preference_store.get_all(user["id"]))


@router.put("/preferences", response_model=PreferencesResponse)
def update_preferences(payload: PreferencesUpdateRequest, user: dict = Depends(get_current_user)) -> PreferencesResponse:
    return PreferencesResponse(items=notification_preference_store.update(user["id"], [x.model_dump() for x in payload.items]))


@router.get("/history", response_model=NotificationHistoryResponse)
def list_history(
    user: dict = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=100),
    category: str | None = None,
) -> NotificationHistoryResponse:
    return NotificationHistoryResponse(items=notification_history_store.list(user["id"], limit=limit, category=category))


@router.post("/emit", response_model=NotificationHistoryResponse)
def emit_notification(payload: EmitNotificationRequest, user: dict = Depends(get_current_user)) -> NotificationHistoryResponse:
    items = dispatch_notification(user["id"], payload.model_dump())
    return NotificationHistoryResponse(items=items)
