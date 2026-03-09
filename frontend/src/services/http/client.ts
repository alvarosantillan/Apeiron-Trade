export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type HttpErrorCode =
  | "UNAUTHORIZED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "CONFLICT"
  | "VALIDATION_ERROR"
  | "SERVER_ERROR"
  | "NETWORK_ERROR"
  | "UNKNOWN_ERROR";

export class HttpClientError extends Error {
  readonly status?: number;
  readonly code: HttpErrorCode;
  readonly details?: unknown;

  constructor(message: string, code: HttpErrorCode, status?: number, details?: unknown) {
    super(message);
    this.name = "HttpClientError";
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

type BeforeRequest = (init: RequestInit) => RequestInit;
type OnUnauthorized = () => void;

let tokenProvider: (() => string | null) | null = null;
let unauthorizedHandler: OnUnauthorized | null = null;
const beforeRequestHandlers: BeforeRequest[] = [];

export function setTokenProvider(provider: () => string | null): void {
  tokenProvider = provider;
}

export function onUnauthorized(handler: OnUnauthorized): void {
  unauthorizedHandler = handler;
}

export function registerBeforeRequest(handler: BeforeRequest): void {
  beforeRequestHandlers.push(handler);
}

function mapStatusToCode(status: number): HttpErrorCode {
  if (status === 401) return "UNAUTHORIZED";
  if (status === 403) return "FORBIDDEN";
  if (status === 404) return "NOT_FOUND";
  if (status === 409) return "CONFLICT";
  if (status === 422 || status === 400) return "VALIDATION_ERROR";
  if (status >= 500) return "SERVER_ERROR";
  return "UNKNOWN_ERROR";
}

function buildInit(method: HttpMethod, body?: unknown): RequestInit {
  let init: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  const token = tokenProvider?.();
  if (token) {
    (init.headers as Record<string, string>).Authorization = `Bearer ${token}`;
  }

  if (body !== undefined) {
    init.body = JSON.stringify(body);
  }

  for (const handler of beforeRequestHandlers) {
    init = handler(init);
  }

  return init;
}

export async function httpRequest<T>(url: string, method: HttpMethod, body?: unknown): Promise<T> {
  let response: Response;
  try {
    response = await fetch(url, buildInit(method, body));
  } catch (err) {
    throw new HttpClientError("Network error", "NETWORK_ERROR", undefined, err);
  }

  const contentType = response.headers.get("content-type") ?? "";
  const hasJson = contentType.includes("application/json");
  const payload = hasJson ? await response.json() : await response.text();

  if (!response.ok) {
    const code = mapStatusToCode(response.status);
    if (code === "UNAUTHORIZED") {
      unauthorizedHandler?.();
    }
    throw new HttpClientError(`Request failed with status ${response.status}`, code, response.status, payload);
  }

  return payload as T;
}
