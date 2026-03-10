import { uiKitTheme } from "../../app/content/ui-kit-theme";

export interface DashboardHistoryRow {
  id: string;
  symbol: string;
  status: string;
  quantity: string;
  pnl: string;
}

interface DashboardHistoryPanelProps {
  rows: DashboardHistoryRow[];
}

export default function DashboardHistoryPanel({ rows }: DashboardHistoryPanelProps) {
  return (
    <section
      aria-label="Historial de trading"
      style={{
        background: uiKitTheme.color.panelBg,
        borderRadius: uiKitTheme.radius.md,
        border: `1px solid ${uiKitTheme.color.accentSoft}`,
        boxShadow: uiKitTheme.shadow.card,
        overflow: "hidden"
      }}
    >
      <header style={{ padding: `${uiKitTheme.space.sm}px ${uiKitTheme.space.md}px`, borderBottom: `1px solid ${uiKitTheme.color.accentSoft}` }}>
        <h2 style={{ margin: 0, fontSize: 18 }}>Operaciones recientes</h2>
      </header>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 520 }}>
          <thead>
            <tr style={{ textAlign: "left", color: uiKitTheme.color.textMuted }}>
              <th style={{ padding: 12 }}>Par</th>
              <th style={{ padding: 12 }}>Estado</th>
              <th style={{ padding: 12 }}>Cantidad</th>
              <th style={{ padding: 12 }}>PnL</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td style={{ padding: 12, borderTop: `1px solid ${uiKitTheme.color.accentSoft}` }}>{row.symbol}</td>
                <td style={{ padding: 12, borderTop: `1px solid ${uiKitTheme.color.accentSoft}` }}>{row.status}</td>
                <td style={{ padding: 12, borderTop: `1px solid ${uiKitTheme.color.accentSoft}` }}>{row.quantity}</td>
                <td style={{ padding: 12, borderTop: `1px solid ${uiKitTheme.color.accentSoft}` }}>{row.pnl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
