import { getErrorMessage } from "../../app/content/error-messages";
import { HttpClientError } from "./client";

export interface NormalizedError {
  code: string;
  message: string;
  retryable: boolean;
}

export function normalizeError(error: unknown): NormalizedError {
  if (error instanceof HttpClientError) {
    const code = error.code;
    return {
      code,
      message: getErrorMessage(code),
      retryable: code === "NETWORK_ERROR" || code === "SERVER_ERROR"
    };
  }

  return {
    code: "UNKNOWN_ERROR",
    message: getErrorMessage("UNKNOWN_ERROR"),
    retryable: false
  };
}

export function shouldRetry(error: unknown, attempts: number, maxAttempts = 2): boolean {
  if (attempts >= maxAttempts) {
    return false;
  }
  const normalized = normalizeError(error);
  return normalized.retryable;
}
