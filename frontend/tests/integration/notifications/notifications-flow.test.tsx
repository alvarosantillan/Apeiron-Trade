import { vi } from "vitest";

import { emitNotification, registerDevice } from "../../../src/features/notifications/notifications.api";

describe("Notifications flow", () => {
  it("registers device and emits notification", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ deviceId: "d1", platform: "WEB", active: true }) })
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ items: [{ eventId: "e1", category: "TRADING", priority: "HIGH", title: "t", message: "m", status: "DELIVERED", createdAt: new Date().toISOString() }] }) });

    vi.stubGlobal("fetch", fetchMock as unknown as typeof fetch);

    const registered = await registerDevice({ deviceId: "d1", platform: "WEB", pushToken: "p1" });
    const emitted = await emitNotification({ eventId: "e1", category: "TRADING", priority: "HIGH", title: "t", message: "m" });

    expect(registered.active).toBe(true);
    expect(emitted.items[0].eventId).toBe("e1");
  });
});
