import { FormEvent, useState } from "react";

import SubmitGuardButton from "../app/components/SubmitGuardButton";
import { useTradingViewModel } from "../features/trading/trading.viewmodel";

export default function TradingPage() {
  const { status, message, saveCredentials, submitTrade } = useTradingViewModel();
  const [apiKey, setApiKey] = useState("bnc_ui_12345");
  const [secretKey, setSecretKey] = useState("sec_ui_12345");
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [quantity, setQuantity] = useState(50);

  const onSave = async (e: FormEvent) => {
    e.preventDefault();
    await saveCredentials(apiKey, secretKey);
  };

  const onTrade = async (e: FormEvent) => {
    e.preventDefault();
    await submitTrade(symbol, Number(quantity), false);
  };

  return (
    <section>
      <h1>Trading</h1>
      <form onSubmit={onSave} style={{ marginBottom: 12 }}>
        <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="API Key" />
        <input value={secretKey} onChange={(e) => setSecretKey(e.target.value)} placeholder="Secret Key" />
        <SubmitGuardButton busy={status === "loading"} idleLabel="Guardar Credenciales" />
      </form>

      <form onSubmit={onTrade}>
        <input value={symbol} onChange={(e) => setSymbol(e.target.value)} placeholder="Symbol" />
        <input type="number" value={quantity} onChange={(e) => setQuantity(Number(e.target.value))} />
        <SubmitGuardButton busy={status === "loading"} idleLabel="Ejecutar Orden" />
      </form>

      <p>Estado: {status}</p>
      <p>{message}</p>
    </section>
  );
}
