from datetime import datetime

from pydantic import BaseModel, Field


class UpsertDeviceTokenRequest(BaseModel):
    deviceId: str
    platform: str
    pushToken: str = Field(min_length=16)


class DeviceTokenResponse(BaseModel):
    id: str
    deviceId: str
    platform: str
    isActive: bool
    updatedAt: datetime


class DeviceTokenListResponse(BaseModel):
    items: list[DeviceTokenResponse]


class Preference(BaseModel):
    category: str
    enabled: bool


class PreferenceUpdate(BaseModel):
    category: str
    enabled: bool


class PreferencesUpdateRequest(BaseModel):
    items: list[PreferenceUpdate]


class PreferencesResponse(BaseModel):
    items: list[Preference]


class NotificationHistoryItem(BaseModel):
    eventId: str
    category: str
    priority: str
    title: str
    message: str
    status: str
    referenceId: str | None = None
    createdAt: datetime


class NotificationHistoryResponse(BaseModel):
    items: list[NotificationHistoryItem]


class EmitNotificationRequest(BaseModel):
    eventId: str
    category: str
    priority: str
    title: str
    message: str
    referenceId: str | None = None
