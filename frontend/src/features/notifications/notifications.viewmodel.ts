import { useState } from "react";

import { emitNotification, registerDevice, type NotificationHistoryItem } from "./notifications.api";

export function useNotificationsViewModel() {
  const [status, setStatus] = useState<string>("idle");
  const [items, setItems] = useState<NotificationHistoryItem[]>([]);

  async function register(pushToken: string) {
    setStatus("loading");
    try {
      await registerDevice({ deviceId: "web-device", platform: "WEB", pushToken });
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  async function emit(category: string, title: string, message: string) {
    setStatus("loading");
    try {
      const response = await emitNotification({
        eventId: `evt-ui-${Date.now()}`,
        category,
        priority: "HIGH",
        title,
        message
      });
      setItems(response.items);
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  return { status, items, register, emit };
}
