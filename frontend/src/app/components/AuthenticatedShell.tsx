import { ReactNode } from "react";

import { privateRouteNavItems, uiKitTheme } from "../content/ui-kit-theme";
import NavigationItem from "./NavigationItem";

interface AuthenticatedShellProps {
  onLogout: () => void;
  children: ReactNode;
  activePathname: string;
}

function dashboardTitle(pathname: string): string {
  if (pathname.startsWith("/trading")) return "Trading";
  if (pathname.startsWith("/notifications")) return "Notifications";
  if (pathname.startsWith("/ai-agent")) return "AI Agent";
  return "Dashboard";
}

export default function AuthenticatedShell({ onLogout, children, activePathname }: AuthenticatedShellProps) {
  return (
    <main
      style={{
        fontFamily: uiKitTheme.font.family,
        minHeight: "100vh",
        display: "grid",
        gridTemplateColumns: "minmax(220px, 260px) 1fr",
        background: uiKitTheme.color.pageBg,
        color: uiKitTheme.color.textPrimary
      }}
    >
      <aside
        aria-label="Navegacion privada"
        style={{
          background: `linear-gradient(160deg, ${uiKitTheme.color.shellBg}, ${uiKitTheme.color.shellMuted})`,
          color: uiKitTheme.color.textOnDark,
          padding: uiKitTheme.space.lg,
          borderRight: `1px solid ${uiKitTheme.color.shellBorder}`
        }}
      >
        <p style={{ margin: 0, fontWeight: 800, letterSpacing: 0.5 }}>TRDIA</p>
        <p style={{ margin: "4px 0 20px", color: "#93c5fd", fontSize: 13 }}>Cryptocurrency UI Kit</p>
        <nav aria-label="Navegacion privada" style={{ display: "grid", gap: 8 }}>
          {privateRouteNavItems.map((item) => (
            <NavigationItem key={item.to} to={item.to} label={item.label} compact={item.scope === "secondary"} />
          ))}
        </nav>
      </aside>

      <div style={{ minWidth: 0 }}>
        <header
          style={{
            margin: uiKitTheme.space.lg,
            marginBottom: uiKitTheme.space.md,
            background: uiKitTheme.color.panelBg,
            border: `1px solid ${uiKitTheme.color.accentSoft}`,
            borderRadius: uiKitTheme.radius.lg,
            boxShadow: uiKitTheme.shadow.soft,
            padding: `${uiKitTheme.space.sm}px ${uiKitTheme.space.lg}px`,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: uiKitTheme.space.sm,
            flexWrap: "wrap"
          }}
        >
          <div>
            <p style={{ margin: 0, color: uiKitTheme.color.textMuted, fontSize: 13 }}>Area autenticada</p>
            <h1 style={{ margin: "3px 0 0", fontSize: 24 }}>{dashboardTitle(activePathname)}</h1>
          </div>
          <button
            type="button"
            onClick={onLogout}
            style={{
              border: `1px solid ${uiKitTheme.color.shellBorder}`,
              background: uiKitTheme.color.panelBg,
              borderRadius: uiKitTheme.radius.sm,
              color: uiKitTheme.color.textPrimary,
              fontWeight: 700,
              padding: "10px 14px",
              cursor: "pointer"
            }}
          >
            Logout
          </button>
        </header>

        <section style={{ margin: `0 ${uiKitTheme.space.lg}px ${uiKitTheme.space.lg}px` }}>{children}</section>
      </div>
    </main>
  );
}
