const REDACT_KEYS = new Set(["token", "accessToken", "refreshToken", "apiKey", "secretKey", "password"]);

export type FrontendEventLevel = "info" | "warning" | "error";

export interface FrontendEvent {
  event: string;
  level: FrontendEventLevel;
  details?: Record<string, unknown>;
  timestamp: string;
}

export type DashboardUiState = "loading" | "success" | "empty" | "error";
export type TradingUiState = "idle" | "submitting" | "success" | "error";

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

export function emitPrivateLayoutRendered(pathname: string): FrontendEvent {
  return logFrontendEvent("ui.layout.private.rendered", "info", { pathname });
}

export function emitAuthRedirectTriggered(reason: string, fromPath: string, toPath: string): FrontendEvent {
  return logFrontendEvent("ui.auth.redirect.triggered", "warning", { reason, fromPath, toPath });
}

export function emitDashboardStateChanged(state: DashboardUiState): FrontendEvent {
  return logFrontendEvent("ui.dashboard.state.changed", "info", { state });
}

export function emitTradingSubmitStarted(symbol: string): FrontendEvent {
  return logFrontendEvent("ui.trading.submit.started", "info", { symbol });
}

export function emitTradingSubmitCompleted(status: Exclude<TradingUiState, "idle" | "submitting">, message: string): FrontendEvent {
  const level: FrontendEventLevel = status === "error" ? "error" : "info";
  return logFrontendEvent("ui.trading.submit.completed", level, { status, message });
}
