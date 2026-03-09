import { httpRequest } from "../../services/http/client";

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
}

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8111";
}

export async function login(payload: LoginRequest): Promise<LoginResponse> {
  return httpRequest<LoginResponse>(`${apiBase()}/v1/auth/login`, "POST", payload);
}

export async function register(payload: LoginRequest): Promise<{ id: string; email: string }> {
  return httpRequest<{ id: string; email: string }>(`${apiBase()}/v1/auth/register`, "POST", payload);
}
