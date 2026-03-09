import { httpRequest } from "../../services/http/client";

export interface TradingCredentialsRequest {
  api_key: string;
  secret_key: string;
}

export interface ExecuteTradeRequest {
  request_id: string;
  symbol: string;
  side: "BUY" | "SELL";
  order_type: "MARKET" | "LIMIT";
  quantity: number;
  limit_price?: number;
  is_simulation: boolean;
  source: string;
}

export interface ExecuteTradeResponse {
  request_id: string;
  status: string;
  execution_type: string;
  symbol: string;
  side: string;
  quantity: number;
  message: string;
}

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8111";
}

export async function saveTradingCredentials(payload: TradingCredentialsRequest): Promise<{ status: string }> {
  return httpRequest<{ status: string }>(`${apiBase()}/v1/trading/binance/credentials`, "POST", payload);
}

export async function executeTrade(payload: ExecuteTradeRequest): Promise<ExecuteTradeResponse> {
  return httpRequest<ExecuteTradeResponse>(`${apiBase()}/v1/trading/execute`, "POST", payload);
}
