import { vi } from "vitest";

import { executeTrade, saveTradingCredentials } from "../../../src/features/trading/trading.api";

describe("Trading API flow", () => {
  it("saves credentials and executes trade", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ status: "verified" }) })
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ request_id: "r1", status: "executed", execution_type: "REAL", symbol: "BTCUSDT", side: "BUY", quantity: 10, message: "ok" }) });

    vi.stubGlobal("fetch", fetchMock as unknown as typeof fetch);

    const credentials = await saveTradingCredentials({ api_key: "a", secret_key: "b" });
    const result = await executeTrade({ request_id: "r1", symbol: "BTCUSDT", side: "BUY", order_type: "MARKET", quantity: 10, is_simulation: false, source: "manual" });

    expect(credentials.status).toBe("verified");
    expect(result.status).toBe("executed");
    expect(fetchMock).toHaveBeenNthCalledWith(2, expect.stringContaining("/v1/trading/execute"), expect.objectContaining({ method: "POST" }));
  });
});
