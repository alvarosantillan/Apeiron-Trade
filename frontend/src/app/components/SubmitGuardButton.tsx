interface SubmitGuardButtonProps {
  busy: boolean;
  idleLabel: string;
  busyLabel?: string;
}

export default function SubmitGuardButton({ busy, idleLabel, busyLabel }: SubmitGuardButtonProps) {
  return (
    <button type="submit" disabled={busy}>
      {busy ? (busyLabel ?? "Enviando...") : idleLabel}
    </button>
  );
}
