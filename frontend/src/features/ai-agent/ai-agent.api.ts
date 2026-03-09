import { httpRequest } from "../../services/http/client";

export interface AIConfig {
  id?: string;
  provider: string;
  strategyId: string;
  riskProfile: string;
  mode: string;
  isActive: boolean;
  updatedAt?: string;
}

export interface AIConfigUpsertRequest extends AIConfig {
  apiKey: string;
}

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8111";
}

export async function getAIConfig(): Promise<AIConfig> {
  return httpRequest<AIConfig>(`${apiBase()}/v1/ai-agent/config`, "GET");
}

export async function upsertAIConfig(payload: AIConfigUpsertRequest): Promise<AIConfig> {
  return httpRequest<AIConfig>(`${apiBase()}/v1/ai-agent/config`, "PUT", payload);
}
