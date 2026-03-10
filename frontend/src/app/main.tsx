import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import { useEffect } from "react";

import { SessionProvider, useSession } from "../features/auth/session-store";
import { appRouter } from "./router";
import { onUnauthorized, setTokenProvider } from "../services/http/client";

const queryClient = new QueryClient();

function AppProviders() {
  const { session, logout } = useSession();

  // Register token provider synchronously to avoid first-request auth races after login.
  setTokenProvider(() => session.accessToken);

  useEffect(() => {
    onUnauthorized(() => logout());
  }, [logout]);

  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={appRouter} />
    </QueryClientProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <SessionProvider>
      <AppProviders />
    </SessionProvider>
  </React.StrictMode>
);
