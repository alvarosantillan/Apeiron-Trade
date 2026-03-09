import { useEffect, useState } from "react";

import { getAIConfig, upsertAIConfig, type AIConfig } from "./ai-agent.api";

const defaultConfig: AIConfig = {
  provider: "OPENAI",
  strategyId: "11111111-1111-1111-1111-111111111111",
  riskProfile: "MEDIUM",
  mode: "MANUAL",
  isActive: true
};

export function useAIAgentViewModel() {
  const [config, setConfig] = useState<AIConfig>(defaultConfig);
  const [status, setStatus] = useState<string>("idle");

  useEffect(() => {
    getAIConfig()
      .then((value) => {
        setConfig(value);
      })
      .catch(() => {
        setConfig(defaultConfig);
      });
  }, []);

  async function save(apiKey: string) {
    setStatus("loading");
    try {
      const saved = await upsertAIConfig({ ...config, apiKey });
      setConfig(saved);
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  return { config, setConfig, status, save };
}
