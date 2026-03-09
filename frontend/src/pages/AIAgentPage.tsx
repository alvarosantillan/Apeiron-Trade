import { FormEvent, useState } from "react";

import SubmitGuardButton from "../app/components/SubmitGuardButton";
import { useAIAgentViewModel } from "../features/ai-agent/ai-agent.viewmodel";

export default function AIAgentPage() {
  const { config, setConfig, status, save } = useAIAgentViewModel();
  const [apiKey, setApiKey] = useState("ai_valid_key_123");

  const onSave = async (e: FormEvent) => {
    e.preventDefault();
    await save(apiKey);
  };

  return (
    <section>
      <h1>AI Agent</h1>
      <form onSubmit={onSave}>
        <label>
          Provider
          <input value={config.provider} onChange={(e) => setConfig({ ...config, provider: e.target.value })} />
        </label>
        <label>
          Mode
          <input value={config.mode} onChange={(e) => setConfig({ ...config, mode: e.target.value })} />
        </label>
        <label>
          API Key
          <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
        </label>
        <SubmitGuardButton busy={status === "loading"} idleLabel="Guardar Configuracion" />
      </form>
      <p>Estado: {status}</p>
    </section>
  );
}
