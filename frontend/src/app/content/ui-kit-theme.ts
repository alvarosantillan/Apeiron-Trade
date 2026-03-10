export interface UiKitNavItem {
  to: string;
  label: string;
  scope: "core" | "secondary";
}

export const uiKitTheme = {
  color: {
    pageBg: "#f4f7fb",
    shellBg: "#0f172a",
    shellMuted: "#1e293b",
    shellBorder: "#334155",
    textPrimary: "#0b1220",
    textMuted: "#4b5563",
    textOnDark: "#f8fafc",
    accent: "#0ea5e9",
    accentSoft: "#e0f2fe",
    success: "#16a34a",
    danger: "#dc2626",
    warning: "#d97706",
    panelBg: "#ffffff"
  },
  radius: {
    sm: "8px",
    md: "14px",
    lg: "20px"
  },
  shadow: {
    soft: "0 10px 24px rgba(15, 23, 42, 0.08)",
    card: "0 8px 16px rgba(15, 23, 42, 0.06)"
  },
  space: {
    xs: 8,
    sm: 12,
    md: 16,
    lg: 24,
    xl: 32
  },
  font: {
    family: "'Segoe UI', 'Trebuchet MS', sans-serif"
  }
} as const;

export const privateRouteNavItems: UiKitNavItem[] = [
  { to: "/dashboard", label: "Dashboard", scope: "core" },
  { to: "/trading", label: "Trading", scope: "core" },
  { to: "/notifications", label: "Notifications", scope: "secondary" },
  { to: "/ai-agent", label: "AI Agent", scope: "secondary" }
];
