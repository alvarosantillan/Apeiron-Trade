import { uiKitTheme } from "../../app/content/ui-kit-theme";

export interface DashboardSummaryCardData {
  label: string;
  value: string;
  tone?: "neutral" | "success" | "warning";
}

interface DashboardSummaryCardsProps {
  cards: DashboardSummaryCardData[];
}

const toneColor: Record<NonNullable<DashboardSummaryCardData["tone"]>, string> = {
  neutral: uiKitTheme.color.textPrimary,
  success: uiKitTheme.color.success,
  warning: uiKitTheme.color.warning
};

export default function DashboardSummaryCards({ cards }: DashboardSummaryCardsProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        gap: uiKitTheme.space.sm,
        marginBottom: uiKitTheme.space.md
      }}
    >
      {cards.map((card) => {
        const tone = card.tone ?? "neutral";
        return (
          <article
            key={card.label}
            style={{
              background: uiKitTheme.color.panelBg,
              borderRadius: uiKitTheme.radius.md,
              border: `1px solid ${uiKitTheme.color.accentSoft}`,
              boxShadow: uiKitTheme.shadow.card,
              padding: `${uiKitTheme.space.sm}px ${uiKitTheme.space.md}px`
            }}
          >
            <p style={{ margin: 0, color: uiKitTheme.color.textMuted, fontSize: 12 }}>{card.label}</p>
            <p style={{ margin: "8px 0 0", fontSize: 20, fontWeight: 800, color: toneColor[tone] }}>{card.value}</p>
          </article>
        );
      })}
    </div>
  );
}
