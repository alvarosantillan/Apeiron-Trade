export type ViewStateKind = "idle" | "loading" | "empty" | "success" | "error";

export type ViewState<T> =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "empty"; message?: string }
  | { kind: "success"; data: T }
  | { kind: "error"; message: string; retryable?: boolean };

export function idleState<T>(): ViewState<T> {
  return { kind: "idle" };
}

export function loadingState<T>(): ViewState<T> {
  return { kind: "loading" };
}

export function emptyState<T>(message?: string): ViewState<T> {
  return { kind: "empty", message };
}

export function successState<T>(data: T): ViewState<T> {
  return { kind: "success", data };
}

export function errorState<T>(message: string, retryable = false): ViewState<T> {
  return { kind: "error", message, retryable };
}
