import { vi } from "vitest";

import { getDashboardSummary, getTradeHistory } from "../../../src/features/dashboard/dashboard.api";

describe("Dashboard history flow", () => {
  it("loads summary and history", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ balance: 1000, pnlDaily: 1, pnlWeekly: 5, openPositions: 0, updatedAt: new Date().toISOString() }) })
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ items: [], nextCursor: null }) });

    vi.stubGlobal("fetch", fetchMock as unknown as typeof fetch);

    const summary = await getDashboardSummary();
    const history = await getTradeHistory();

    expect(summary.balance).toBe(1000);
    expect(history.items).toHaveLength(0);
    expect(fetchMock).toHaveBeenNthCalledWith(2, expect.stringContaining("/v1/history/trades?limit=10"), expect.any(Object));
  });
});
