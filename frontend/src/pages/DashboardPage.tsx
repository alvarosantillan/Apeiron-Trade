import { useDashboardViewModel } from "../features/dashboard/dashboard.viewmodel";
import StatePanel from "../app/components/StatePanel";

export default function DashboardPage() {
  const state = useDashboardViewModel();

  return (
    <section>
      <h1>Dashboard</h1>
      {state.kind === "loading" ? <StatePanel kind="loading" message="Cargando dashboard" /> : null}
      {state.kind === "error" ? <StatePanel kind="error" message={state.message} /> : null}
      {state.kind === "success" && state.data.recentTrades.length === 0 ? (
        <StatePanel kind="empty" message="Sin operaciones recientes" />
      ) : null}
      {state.kind === "success" ? (
        <>
          <p>Balance: {state.data.summary.balance}</p>
          <p>PNL Diario: {state.data.summary.pnlDaily}</p>
          <h2>Operaciones recientes</h2>
          <ul>
            {state.data.recentTrades.map((trade) => (
              <li key={trade.tradeId}>
                {trade.symbol} - {trade.status}
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </section>
  );
}
