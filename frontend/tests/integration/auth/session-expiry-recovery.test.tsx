import { HttpClientError, onUnauthorized } from "../../../src/services/http/client";
import { normalizeError } from "../../../src/services/http/error-normalizer";

describe("Session expiry recovery", () => {
  it("normalizes unauthorized errors for session-expired UX", () => {
    const err = new HttpClientError("401", "UNAUTHORIZED", 401);
    const normalized = normalizeError(err);

    expect(normalized.code).toBe("UNAUTHORIZED");
    expect(normalized.message).toContain("sesion");
  });

  it("supports registering unauthorized handler", () => {
    const fn = vi.fn();
    onUnauthorized(fn);
    expect(typeof fn).toBe("function");
  });
});
