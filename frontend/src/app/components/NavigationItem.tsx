import { NavLink } from "react-router-dom";

import { uiKitTheme } from "../content/ui-kit-theme";

interface NavigationItemProps {
  to: string;
  label: string;
  compact?: boolean;
}

export default function NavigationItem({ to, label, compact = false }: NavigationItemProps) {
  return (
    <NavLink
      to={to}
      style={({ isActive }) => ({
        display: "block",
        padding: compact ? "8px 10px" : "10px 12px",
        borderRadius: uiKitTheme.radius.sm,
        textDecoration: "none",
        border: `1px solid ${isActive ? uiKitTheme.color.accent : "transparent"}`,
        color: isActive ? uiKitTheme.color.textOnDark : "#dbeafe",
        background: isActive ? "rgba(14, 165, 233, 0.18)" : "transparent",
        fontWeight: isActive ? 700 : 500,
        outlineOffset: 2
      })}
    >
      {label}
    </NavLink>
  );
}
