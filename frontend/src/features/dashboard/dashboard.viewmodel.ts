import { useEffect, useState } from "react";

import { errorState, loadingState, successState, type ViewState } from "../../app/state/view-state";
import { getDashboardSummary, getTradeHistory, type DashboardSummary, type HistoryItem } from "./dashboard.api";

export interface DashboardData {
  summary: DashboardSummary;
  recentTrades: HistoryItem[];
}

export function useDashboardViewModel() {
  const [state, setState] = useState<ViewState<DashboardData>>(loadingState());

  useEffect(() => {
    let active = true;
    Promise.all([getDashboardSummary(), getTradeHistory(8)])
      .then(([summary, history]) => {
        if (!active) return;
        setState(successState({ summary, recentTrades: history.items }));
      })
      .catch(() => {
        if (!active) return;
        setState(errorState("No se pudo cargar el dashboard", true));
      });

    return () => {
      active = false;
    };
  }, []);

  return state;
}
