import { FormEvent, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { login } from "../features/auth/auth.api";
import { useSession } from "../features/auth/session-store";
import { HttpClientError } from "../services/http/client";

export default function LoginPage() {
  const navigate = useNavigate();
  const { session, login: setSession } = useSession();

  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("Password123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await login({ email, password });
      setSession(response.accessToken);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      if (err instanceof HttpClientError) {
        setError(err.code === "UNAUTHORIZED" ? "Credenciales invalidas" : "No se pudo iniciar sesion");
      } else {
        setError("Error inesperado");
      }
    } finally {
      setLoading(false);
    }
  }

  if (session.isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <main style={{ fontFamily: "Segoe UI, sans-serif", maxWidth: 380, margin: "32px auto" }}>
      <h1>TRDIA Login</h1>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button type="submit" disabled={loading}>{loading ? "Ingresando..." : "Ingresar"}</button>
      </form>
      {error ? <p role="alert" style={{ color: "crimson" }}>{error}</p> : null}
    </main>
  );
}
