import { vi } from "vitest";

import { getAIConfig, upsertAIConfig } from "../../../src/features/ai-agent/ai-agent.api";

describe("AI agent config flow", () => {
  it("loads and updates config", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ provider: "OPENAI", strategyId: "11111111-1111-1111-1111-111111111111", riskProfile: "MEDIUM", mode: "MANUAL", isActive: true, updatedAt: new Date().toISOString() }) })
      .mockResolvedValueOnce({ ok: true, headers: new Headers({ "content-type": "application/json" }), json: async () => ({ provider: "OPENAI", strategyId: "11111111-1111-1111-1111-111111111111", riskProfile: "MEDIUM", mode: "MANUAL", isActive: true, updatedAt: new Date().toISOString() }) });

    vi.stubGlobal("fetch", fetchMock as unknown as typeof fetch);

    const cfg = await getAIConfig();
    const saved = await upsertAIConfig({ ...cfg, apiKey: "k" });

    expect(cfg.provider).toBe("OPENAI");
    expect(saved.mode).toBe("MANUAL");
  });
});
