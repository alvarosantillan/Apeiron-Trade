import { useEffect } from "react";

import StatePanel from "../app/components/StatePanel";
import { getErrorMessage } from "../app/content/error-messages";
import { emitDashboardStateChanged } from "../services/observability/events";
import DashboardHistoryPanel from "../features/dashboard/DashboardHistoryPanel";
import DashboardSummaryCards from "../features/dashboard/DashboardSummaryCards";
import { useDashboardViewModel } from "../features/dashboard/dashboard.viewmodel";

export default function DashboardPage() {
  const { state, reload } = useDashboardViewModel();

  useEffect(() => {
    if (state.kind === "loading" || state.kind === "success" || state.kind === "error" || state.kind === "empty") {
      emitDashboardStateChanged(state.kind);
    }
  }, [state.kind]);

  return (
    <section>
      {state.kind === "loading" ? <StatePanel kind="loading" message="Cargando dashboard" /> : null}
      {state.kind === "error" ? <StatePanel kind="error" message={getErrorMessage("DASHBOARD_LOAD_ERROR")} onRetry={reload} /> : null}
      {state.kind === "success" && state.data.recentTrades.length === 0 ? (
        <StatePanel kind="empty" message={getErrorMessage("DASHBOARD_EMPTY")} />
      ) : null}
      {state.kind === "success" ? (
        <>
          <DashboardSummaryCards
            cards={[
              { label: "Balance", value: state.data.summary.balance },
              { label: "PnL Diario", value: state.data.summary.pnlDaily, tone: "success" },
              { label: "PnL Semanal", value: state.data.summary.pnlWeekly },
              { label: "Posiciones", value: state.data.summary.openPositions, tone: "warning" }
            ]}
          />
          <DashboardHistoryPanel rows={state.data.recentTrades} />
        </>
      ) : null}
    </section>
  );
}
