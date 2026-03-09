import { HttpClientError } from "../../../src/services/http/client";
import { normalizeError, shouldRetry } from "../../../src/services/http/error-normalizer";

describe("Network retry behavior", () => {
  it("marks network error as retryable", () => {
    const err = new HttpClientError("network", "NETWORK_ERROR");
    const normalized = normalizeError(err);

    expect(normalized.retryable).toBe(true);
    expect(shouldRetry(err, 0, 2)).toBe(true);
  });

  it("stops retry after max attempts", () => {
    const err = new HttpClientError("server", "SERVER_ERROR", 500);
    expect(shouldRetry(err, 2, 2)).toBe(false);
  });
});
