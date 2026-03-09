import { useState } from "react";

import { executeTrade, saveTradingCredentials } from "./trading.api";

export function useTradingViewModel() {
  const [status, setStatus] = useState<string>("idle");
  const [message, setMessage] = useState<string>("");

  async function saveCredentials(apiKey: string, secretKey: string) {
    setStatus("loading");
    try {
      const result = await saveTradingCredentials({ api_key: apiKey, secret_key: secretKey });
      setStatus("success");
      setMessage(result.status);
    } catch {
      setStatus("error");
      setMessage("No se pudo verificar credenciales");
    }
  }

  async function submitTrade(symbol: string, quantity: number, simulation: boolean) {
    setStatus("loading");
    try {
      const result = await executeTrade({
        request_id: `req-ui-${Date.now()}`,
        symbol,
        side: "BUY",
        order_type: "MARKET",
        quantity,
        is_simulation: simulation,
        source: "manual"
      });
      setStatus("success");
      setMessage(`${result.status}: ${result.message}`);
    } catch {
      setStatus("error");
      setMessage("No se pudo ejecutar la orden");
    }
  }

  return { status, message, saveCredentials, submitTrade };
}
