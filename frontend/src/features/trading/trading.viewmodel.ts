import { useState } from "react";

import { emitTradingSubmitCompleted, emitTradingSubmitStarted } from "../../services/observability/events";
import { executeTrade, saveTradingCredentials } from "./trading.api";

export type TradingStatus = "idle" | "submitting" | "success" | "error";

export function useTradingViewModel() {
  const [status, setStatus] = useState<TradingStatus>("idle");
  const [message, setMessage] = useState<string>("");

  async function saveCredentials(apiKey: string, secretKey: string) {
    setStatus("submitting");
    try {
      const result = await saveTradingCredentials({ api_key: apiKey, secret_key: secretKey });
      setStatus("success");
      setMessage(result.status);
      emitTradingSubmitCompleted("success", result.status);
    } catch {
      setStatus("error");
      setMessage("No se pudo verificar credenciales");
      emitTradingSubmitCompleted("error", "No se pudo verificar credenciales");
    }
  }

  async function submitTrade(symbol: string, quantity: number, simulation: boolean) {
    setStatus("submitting");
    emitTradingSubmitStarted(symbol);
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
      emitTradingSubmitCompleted("success", `${result.status}: ${result.message}`);
    } catch {
      setStatus("error");
      setMessage("No se pudo ejecutar la orden");
      emitTradingSubmitCompleted("error", "No se pudo ejecutar la orden");
    }
  }

  return { status, message, saveCredentials, submitTrade };
}
