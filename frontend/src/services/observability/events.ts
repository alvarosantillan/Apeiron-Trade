const REDACT_KEYS = new Set(["token", "accessToken", "refreshToken", "apiKey", "secretKey", "password"]);

export type FrontendEventLevel = "info" | "warning" | "error";

export interface FrontendEvent {
  event: string;
  level: FrontendEventLevel;
  details?: Record<string, unknown>;
  timestamp: string;
}

function redact(input: Record<string, unknown> | undefined): Record<string, unknown> | undefined {
  if (!input) return undefined;
  const sanitized: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(input)) {
    sanitized[key] = REDACT_KEYS.has(key) ? "***" : value;
  }
  return sanitized;
}

export function logFrontendEvent(event: string, level: FrontendEventLevel, details?: Record<string, unknown>): FrontendEvent {
  const record: FrontendEvent = {
    event,
    level,
    details: redact(details),
    timestamp: new Date().toISOString()
  };

  if (level === "error") {
    console.error("[frontend-event]", record);
  } else if (level === "warning") {
    console.warn("[frontend-event]", record);
  } else {
    console.info("[frontend-event]", record);
  }

  return record;
}
