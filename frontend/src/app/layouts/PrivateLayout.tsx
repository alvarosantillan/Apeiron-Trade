import { NavLink, Navigate, Outlet } from "react-router-dom";

import { useSession } from "../../features/auth/session-store";

function Item({ to, label }: { to: string; label: string }) {
  return (
    <NavLink to={to} style={({ isActive }) => ({ fontWeight: isActive ? 700 : 500, marginRight: 12 })}>
      {label}
    </NavLink>
  );
}

export default function PrivateLayout() {
  const { session, logout } = useSession();

  if (!session.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <main style={{ fontFamily: "Segoe UI, sans-serif", padding: 16 }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <nav>
          <Item to="/dashboard" label="Dashboard" />
          <Item to="/trading" label="Trading" />
          <Item to="/notifications" label="Notifications" />
          <Item to="/ai-agent" label="AI Agent" />
        </nav>
        <button type="button" onClick={logout}>Logout</button>
      </header>
      <Outlet />
    </main>
  );
}
