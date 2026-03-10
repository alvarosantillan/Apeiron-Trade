import { useEffect, useState } from "react";

import { errorState, loadingState, successState, type ViewState } from "../../app/state/view-state";
import { getDashboardSummary, getTradeHistory, type DashboardSummary, type HistoryItem } from "./dashboard.api";

export interface DashboardSummaryViewData {
  balance: string;
  pnlDaily: string;
  pnlWeekly: string;
  openPositions: string;
}

export interface DashboardHistoryViewData {
  id: string;
  symbol: string;
  status: string;
  quantity: string;
  pnl: string;
}

export interface DashboardViewData {
  summary: DashboardSummaryViewData;
  recentTrades: DashboardHistoryViewData[];
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("es-ES", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2
  }).format(value);
}

function mapSummary(summary: DashboardSummary): DashboardSummaryViewData {
  return {
    balance: formatCurrency(summary.balance),
    pnlDaily: formatCurrency(summary.pnlDaily),
    pnlWeekly: formatCurrency(summary.pnlWeekly),
    openPositions: String(summary.openPositions)
  };
}

function mapHistory(rows: HistoryItem[]): DashboardHistoryViewData[] {
  return rows.map((row) => ({
    id: row.tradeId,
    symbol: row.symbol,
    status: row.status,
    quantity: `${row.quantity}`,
    pnl: row.pnl === null ? "--" : formatCurrency(row.pnl)
  }));
}

export function useDashboardViewModel() {
  const [state, setState] = useState<ViewState<DashboardViewData>>(loadingState());

  const load = () => {
    setState(loadingState());
    Promise.all([getDashboardSummary(), getTradeHistory(8)])
      .then(([summary, history]) => {
        setState(
          successState({
            summary: mapSummary(summary),
            recentTrades: mapHistory(history.items)
          })
        );
      })
      .catch(() => {
        setState(errorState("No se pudo cargar el dashboard", true));
      });
  };

  useEffect(() => {
    load();
  }, []);

  return { state, reload: load };
}
