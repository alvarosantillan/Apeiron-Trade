import { httpRequest } from "../../services/http/client";

export interface DashboardSummary {
  balance: number;
  pnlDaily: number;
  pnlWeekly: number;
  openPositions: number;
  updatedAt: string;
}

export interface HistoryItem {
  tradeId: string;
  symbol: string;
  side: string;
  status: string;
  executedPrice: number | null;
  quantity: number;
  isSimulation: boolean;
  pnl: number | null;
  createdAt: string;
}

export interface HistoryResponse {
  items: HistoryItem[];
  nextCursor: string | null;
}

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8111";
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  return httpRequest<DashboardSummary>(`${apiBase()}/v1/dashboard/summary`, "GET");
}

export async function getTradeHistory(limit = 10): Promise<HistoryResponse> {
  return httpRequest<HistoryResponse>(`${apiBase()}/v1/history/trades?limit=${limit}`, "GET");
}
