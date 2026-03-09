import { httpRequest } from "../../services/http/client";

export interface RegisterDeviceRequest {
  deviceId: string;
  platform: "ANDROID" | "IOS" | "WEB";
  pushToken: string;
}

export interface EmitNotificationRequest {
  eventId: string;
  category: string;
  priority: string;
  title: string;
  message: string;
}

export interface NotificationHistoryItem {
  eventId: string;
  category: string;
  priority: string;
  title: string;
  message: string;
  status: string;
  referenceId?: string;
  createdAt: string;
}

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8111";
}

export async function registerDevice(payload: RegisterDeviceRequest): Promise<{ deviceId: string; platform: string; active: boolean }> {
  return httpRequest(`${apiBase()}/v1/notifications/device-tokens`, "POST", payload);
}

export async function emitNotification(payload: EmitNotificationRequest): Promise<{ items: NotificationHistoryItem[] }> {
  return httpRequest(`${apiBase()}/v1/notifications/emit`, "POST", payload);
}

export async function getNotificationHistory(limit = 10): Promise<{ items: NotificationHistoryItem[] }> {
  return httpRequest(`${apiBase()}/v1/notifications/history?limit=${limit}`, "GET");
}
