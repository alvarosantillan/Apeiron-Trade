import { useEffect } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useSession } from "../../features/auth/session-store";
import AuthenticatedShell from "../components/AuthenticatedShell";
import { emitAuthRedirectTriggered, emitPrivateLayoutRendered } from "../../services/observability/events";

export default function PrivateLayout() {
  const { session, logout } = useSession();
  const location = useLocation();

  useEffect(() => {
    emitPrivateLayoutRendered(location.pathname);
  }, [location.pathname]);

  if (!session.isAuthenticated) {
    emitAuthRedirectTriggered("unauthenticated", location.pathname, "/login");
    return <Navigate to="/login" replace />;
  }

  return (
    <AuthenticatedShell onLogout={logout} activePathname={location.pathname}>
      <Outlet />
    </AuthenticatedShell>
  );
}
