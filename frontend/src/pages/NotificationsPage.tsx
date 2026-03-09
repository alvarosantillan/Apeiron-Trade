import { FormEvent, useState } from "react";

import SubmitGuardButton from "../app/components/SubmitGuardButton";
import { useNotificationsViewModel } from "../features/notifications/notifications.viewmodel";

export default function NotificationsPage() {
  const { status, items, register, emit } = useNotificationsViewModel();
  const [token, setToken] = useState("token_ui_123");
  const [title, setTitle] = useState("Alerta");
  const [message, setMessage] = useState("Evento de prueba");

  const onRegister = async (e: FormEvent) => {
    e.preventDefault();
    await register(token);
  };

  const onEmit = async (e: FormEvent) => {
    e.preventDefault();
    await emit("TRADING", title, message);
  };

  return (
    <section>
      <h1>Notifications</h1>
      <form onSubmit={onRegister} style={{ marginBottom: 12 }}>
        <input value={token} onChange={(e) => setToken(e.target.value)} placeholder="Push token" />
        <SubmitGuardButton busy={status === "loading"} idleLabel="Registrar dispositivo" />
      </form>

      <form onSubmit={onEmit}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Titulo" />
        <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Mensaje" />
        <SubmitGuardButton busy={status === "loading"} idleLabel="Emitir" />
      </form>

      <p>Estado: {status}</p>
      <ul>
        {items.map((item) => (
          <li key={item.eventId}>{item.eventId} - {item.status}</li>
        ))}
      </ul>
    </section>
  );
}
