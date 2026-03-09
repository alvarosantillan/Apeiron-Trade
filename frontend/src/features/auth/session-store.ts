import { ReactNode, createContext, createElement, useContext, useMemo, useState } from "react";

export interface SessionState {
  accessToken: string | null;
  isAuthenticated: boolean;
}

interface SessionContextValue {
  session: SessionState;
  login: (accessToken: string) => void;
  logout: () => void;
}

const SessionContext = createContext<SessionContextValue | null>(null);

function loadInitialToken(): string | null {
  return localStorage.getItem("trdia.accessToken");
}

export function SessionProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(() => loadInitialToken());

  const value = useMemo<SessionContextValue>(
    () => ({
      session: {
        accessToken,
        isAuthenticated: Boolean(accessToken)
      },
      login: (token: string) => {
        localStorage.setItem("trdia.accessToken", token);
        setAccessToken(token);
      },
      logout: () => {
        localStorage.removeItem("trdia.accessToken");
        setAccessToken(null);
      }
    }),
    [accessToken]
  );

  return createElement(SessionContext.Provider, { value }, children);
}

export function useSession(): SessionContextValue {
  const ctx = useContext(SessionContext);
  if (!ctx) {
    throw new Error("useSession must be used within SessionProvider");
  }
  return ctx;
}
