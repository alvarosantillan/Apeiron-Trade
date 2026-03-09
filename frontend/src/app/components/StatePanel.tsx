interface StatePanelProps {
  kind: "loading" | "empty" | "error" | "success";
  message?: string;
  onRetry?: () => void;
}

export default function StatePanel({ kind, message, onRetry }: StatePanelProps) {
  if (kind === "loading") {
    return <p>Loading...</p>;
  }

  if (kind === "empty") {
    return <p>{message ?? "No data available."}</p>;
  }

  if (kind === "error") {
    return (
      <div>
        <p role="alert">{message ?? "Error"}</p>
        {onRetry ? <button type="button" onClick={onRetry}>Retry</button> : null}
      </div>
    );
  }

  return <p>{message ?? "Success"}</p>;
}
