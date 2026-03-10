import { FormEvent, useState } from "react";

import StatePanel from "../app/components/StatePanel";
import { getErrorMessage } from "../app/content/error-messages";
import TradingFormPanel from "../features/trading/TradingFormPanel";
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
      <TradingFormPanel
        status={status}
        apiKey={apiKey}
        secretKey={secretKey}
        symbol={symbol}
        quantity={quantity}
        onApiKeyChange={setApiKey}
        onSecretKeyChange={setSecretKey}
        onSymbolChange={setSymbol}
        onQuantityChange={setQuantity}
        onSave={onSave}
        onTrade={onTrade}
      />

      {status === "submitting" ? <StatePanel kind="loading" message="Procesando solicitud de trading" /> : null}
      {status === "error" ? <StatePanel kind="error" message={getErrorMessage("TRADING_ERROR")} /> : null}
      {status === "success" ? <StatePanel kind="success" message={message || getErrorMessage("TRADING_SUCCESS")} /> : null}

      <p aria-live="polite">Estado: {status}</p>
      {message ? <p>{message}</p> : null}
    </section>
  );
}
