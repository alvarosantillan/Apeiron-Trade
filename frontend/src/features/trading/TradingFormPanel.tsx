import { FormEvent } from "react";

import SubmitGuardButton from "../../app/components/SubmitGuardButton";
import { uiKitTheme } from "../../app/content/ui-kit-theme";

interface TradingFormPanelProps {
  status: "idle" | "submitting" | "success" | "error";
  apiKey: string;
  secretKey: string;
  symbol: string;
  quantity: number;
  onApiKeyChange: (value: string) => void;
  onSecretKeyChange: (value: string) => void;
  onSymbolChange: (value: string) => void;
  onQuantityChange: (value: number) => void;
  onSave: (event: FormEvent<HTMLFormElement>) => Promise<void>;
  onTrade: (event: FormEvent<HTMLFormElement>) => Promise<void>;
}

const panelStyle = {
  background: uiKitTheme.color.panelBg,
  borderRadius: uiKitTheme.radius.md,
  border: `1px solid ${uiKitTheme.color.accentSoft}`,
  boxShadow: uiKitTheme.shadow.card,
  padding: `${uiKitTheme.space.sm}px ${uiKitTheme.space.md}px`
};

export default function TradingFormPanel(props: TradingFormPanelProps) {
  const isSubmitting = props.status === "submitting";

  return (
    <div style={{ display: "grid", gap: uiKitTheme.space.sm }}>
      <form onSubmit={props.onSave} style={panelStyle}>
        <h2 style={{ marginTop: 0, marginBottom: 10, fontSize: 18 }}>Credenciales Binance</h2>
        <div style={{ display: "grid", gap: 10 }}>
          <label>
            API Key
            <input value={props.apiKey} onChange={(e) => props.onApiKeyChange(e.target.value)} placeholder="API Key" />
          </label>
          <label>
            Secret Key
            <input value={props.secretKey} onChange={(e) => props.onSecretKeyChange(e.target.value)} placeholder="Secret Key" />
          </label>
          <SubmitGuardButton busy={isSubmitting} idleLabel="Guardar Credenciales" busyLabel="Guardando..." />
        </div>
      </form>

      <form onSubmit={props.onTrade} style={panelStyle}>
        <h2 style={{ marginTop: 0, marginBottom: 10, fontSize: 18 }}>Ejecucion de orden</h2>
        <div style={{ display: "grid", gap: 10 }}>
          <label>
            Simbolo
            <input value={props.symbol} onChange={(e) => props.onSymbolChange(e.target.value)} placeholder="BTCUSDT" />
          </label>
          <label>
            Cantidad
            <input type="number" min={0} value={props.quantity} onChange={(e) => props.onQuantityChange(Number(e.target.value))} />
          </label>
          <SubmitGuardButton busy={isSubmitting} idleLabel="Ejecutar Orden" busyLabel="Enviando orden..." />
        </div>
      </form>
    </div>
  );
}
