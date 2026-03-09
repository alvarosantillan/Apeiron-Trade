# Feature Specification: TRDIA — Arquitectura General del Sistema

**Feature Branch**: `001-system-design`  
**Created**: 2026-03-06  
**Status**: Draft  
**Tipo**: Architecture Spec (base de todas las feature specs)

---

## Visión del Producto

TRDIA es una aplicación móvil multiplataforma de **trading automatizado con inteligencia artificial** orientada a criptomonedas. Los usuarios descargan la app, se autentican, configuran sus credenciales de Binance y su proveedor de IA preferido, y activan un agente que analiza el mercado y ejecuta operaciones de trading en su nombre, según el plan de suscripción contratado.

**Propuesta de valor**: Democratizar el trading algorítmico con IA sin requerir conocimientos de programación, con control granular del riesgo y transparencia total de operaciones.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Nuevo usuario se registra y configura su cuenta (Priority: P1)

Un usuario descarga la app, crea su cuenta (email o OAuth), elige el plan Free, conecta sus API keys de Binance, y queda listo para recibir sugerencias de trading.

**Why this priority**: Sin usuarios autenticados no existe la plataforma. Es el punto de entrada obligatorio de todo flujo.

**Independent Test**: Se puede probar completamente con un entorno de backend + DB sin Binance real (mock). El usuario puede registrarse, autenticarse y acceder al dashboard aunque no ejecute trades.

**Acceptance Scenarios**:

1. **Given** un visitante sin cuenta, **When** se registra con email+password válidos, **Then** recibe email de verificación, puede iniciar sesión y accede al dashboard con plan Free activo.
2. **Given** un visitante, **When** se autentica con Google OAuth, **Then** su cuenta se crea automáticamente con plan Free y puede ingresar directamente al dashboard.
3. **Given** un usuario autenticado, **When** ingresa sus API keys de Binance, **Then** el backend las cifra, verifica conexión, y confirma que están activas sin exponerlas en la UI.
4. **Given** un usuario con API keys configuradas, **When** selecciona un proveedor de IA (ej: OpenAI) y agrega su API key del proveedor, **Then** el agente queda listo para analizar el mercado.

---

### User Story 2 — Usuario Free recibe y aprueba sugerencias de trading (Priority: P2)

Un usuario con plan Free activa el agente IA, que analiza el mercado y genera una sugerencia de operación. El usuario la revisa y puede aprobarla o rechazarla. Tiene 1 operación por semana.

**Why this priority**: Es el flujo core del producto y la demostración de valor que lleva a upgrades de plan.

**Independent Test**: Puede probarse en modo paper trading (simulación) sin fondos reales. El agente genera sugerencia → usuario aprueba → sistema simula ejecución → resultado guardado en historial.

**Acceptance Scenarios**:

1. **Given** un usuario Free con agente activo y estrategia configurada, **When** el agente detecta una oportunidad, **Then** el usuario recibe notificación push con la sugerencia (símbolo, dirección, precio estimado, confianza).
2. **Given** el usuario recibe una sugerencia, **When** la aprueba, **Then** el sistema ejecuta la orden en Binance Spot, guarda el trade, y notifica el resultado.
3. **Given** el usuario Free ya ejecutó 1 operación esta semana, **When** el agente genera otra sugerencia, **Then** el sistema bloquea la ejecución, notifica al usuario y muestra opción de upgrade.
4. **Given** el usuario rechaza una sugerencia, **Then** la sugerencia se descarta, no consume operaciones del límite, y el agente sigue monitoreando.

---

### User Story 3 — Usuario Plus/Premium activa modo automático (Priority: P3)

Un usuario con plan Plus o Premium puede delegar completamente la ejecución al agente IA. El agente opera automáticamente sin requerir aprobación manual por operación.

**Why this priority**: Es el diferenciador premium que justifica el pago. Un usuario Plus/Premium que lo usa intensivamente es el cliente más valioso.

**Independent Test**: Puede probarse en paper trading activando el modo automático con límites de tiempo/cantidad para verificar que el agente ejecuta, notifica, y respeta los límites del plan.

**Acceptance Scenarios**:

1. **Given** usuario Plus con modo automático habilitado, **When** el agente detecta oportunidad válida, **Then** ejecuta la orden directamente en Binance sin esperar aprobación y envía notificación push post-ejecución.
2. **Given** usuario Plus en modo automático que alcanzó 10 operaciones semanales, **When** el agente detecta nueva oportunidad, **Then** la ejecución es bloqueada automáticamente hasta el reset semanal (lunes 00:00 UTC).
3. **Given** usuario Premium en modo automático, **When** el agente opera, **Then** no hay límite de operaciones semanales y el agente puede ejecutar sin restricciones de cantidad.
4. **Given** usuario Plus/Premium, **When** decide volver a modo manual, **Then** el cambio es efectivo de inmediato y el agente vuelve a sugerir en lugar de ejecutar.

---

### User Story 4 — Usuario suscribe y gestiona su plan (Priority: P4)

Un usuario Free quiere más operaciones. Selecciona el plan Plus o Premium, paga con MercadoPago, y su plan se actualiza inmediatamente. Puede hacer upgrade, downgrade y cancelar.

**Why this priority**: Es el modelo de monetización del producto. Sin cobros no hay negocio.

**Independent Test**: Se puede probar con sandbox de MercadoPago, verificando que el webhook actualiza el plan en la DB y el usuario gana acceso a las operaciones correspondientes.

**Acceptance Scenarios**:

1. **Given** un usuario Free, **When** selecciona plan Plus y completa el pago en MercadoPago, **Then** su plan se actualiza a Plus inmediatamente al recibir confirmación del webhook.
2. **Given** un usuario Plus, **When** hace upgrade a Premium, **Then** se cobra el diferencial prorrateado y el plan se actualiza.
3. **Given** un usuario Plus que cancela, **Then** mantiene acceso Plus hasta el fin del período pagado, luego degrada a Free automáticamente.
4. **Given** un pago rechazado por MercadoPago, **Then** el plan no cambia, el usuario recibe notificación del fallo con opción de reintentar.

---

### User Story 5 — Usuario opera en modo simulación (paper trading) (Priority: P5)

Cualquier usuario (cualquier plan) puede activar el modo paper trading, donde el agente opera con dinero simulado sin ejecutar órdenes reales en Binance. No consume el límite de operaciones.

**Why this priority**: Reduce la barrera de entrada (usuarios nuevos pueden experimentar sin riesgo), y es la herramienta de validación de estrategias.

**Independent Test**: Se puede probar completamente sin conectar Binance real. El sistema simula ejecuciones, registra resultados y muestra historial de paper trades separado del historial real.

**Acceptance Scenarios**:

1. **Given** cualquier usuario, **When** activa modo simulación, **Then** todas las operaciones del agente son simuladas y no ejecutadas en Binance real.
2. **Given** modo simulación activo, **When** el agente ejecuta una operación simulada, **Then** NO se consume el límite semanal del plan.
3. **Given** historial de trades, **Then** los paper trades aparecen claramente distinguidos de los trades reales (badge/etiqueta "Simulación").

---

### Edge Cases

- ¿Qué pasa si Binance API está caída durante una ejecución automática? → Reintento 3 veces con backoff exponencial; si falla, notificación al usuario + log de error.
- ¿Qué pasa si el proveedor de IA (OpenAI, Groq, etc.) falla? → El agente detiene el ciclo, notifica al usuario, reintenta en el siguiente ciclo.
- ¿Qué pasa si el usuario queda sin balance en Binance? → Validación pre-ejecución; si balance insuficiente, la operación se cancela y se notifica.
- ¿Qué pasa si el webhook de MercadoPago llega duplicado? → Idempotencia: se valida el pago_id antes de actualizar el plan; duplicados son ignorados.
- ¿Qué pasa si el usuario revoca sus API keys de Binance? → El agente detecta error 401 de Binance, pausa operaciones, notifica al usuario para re-configurar.
- ¿Reset semanal y usuario sin plan activo? → El cronjob de reset lunes 00:00 UTC sólo resetea usuarios con plan activo; usuarios Free resetan siempre.
- ¿Múltiples dispositivos del mismo usuario? → Las sesiones son múltiples (JWT separados); operaciones son del usuario (no del dispositivo).

---

## Requirements *(mandatory)*

### Functional Requirements

**Autenticación y Usuarios**
- **FR-001**: El sistema DEBE permitir registro con email+password (bcrypt hash, mínimo 8 caracteres).
- **FR-002**: El sistema DEBE permitir autenticación OAuth con Google y Facebook.
- **FR-003**: El sistema DEBE emitir JWT (access 15 min) + refresh token (7 días) en cada login.
- **FR-004**: Los usuarios DEBEN tener uno de los roles: `free`, `plus`, `premium`.
- **FR-005**: El sistema DEBE gestionar sesiones múltiples por usuario (multi-dispositivo).

**Integración Binance**
- **FR-006**: El usuario DEBE poder registrar API Key + Secret Key de Binance desde la app.
- **FR-007**: Las credenciales de Binance DEBEN cifrarse con AES-256 (Fernet) en el backend. Nunca almacenadas en texto plano ni enviadas al frontend.
- **FR-008**: El sistema DEBE validar las credenciales de Binance en el momento del registro (test de conectividad).
- **FR-009**: El sistema DEBE soportar operaciones Spot: Market Order y Limit Order.
- **FR-010**: El sistema DEBE soportar modo Paper Trading (simulación) para todos los planes, sin consumir límite de operaciones.

**Agente IA**
- **FR-011**: El usuario DEBE poder seleccionar uno de los proveedores IA disponibles: OpenAI (GPT), Groq, DeepSeek, Gemini.
- **FR-012**: El usuario DEBE ingresar su propia API key del proveedor IA seleccionado. La key se cifra en backend igual que las de Binance.
- **FR-013**: El usuario DEBE poder seleccionar una estrategia de trading de un catálogo predefinido (mínimo 12 estrategias, ver sección Key Entities).
- **FR-014**: La estrategia seleccionada DEBE incorporarse dinámicamente al system prompt del agente.
- **FR-015**: El usuario DEBE poder configurar parámetros de riesgo: stop-loss (%), take-profit (%), capital por operación (% del balance), activos permitidos, timeframe.
- **FR-016**: El sistema DEBE permitir al agente operar en modo manual (sugerencias) o automático:
  - Plan Free: siempre manual (sugerencia + aprobación del usuario).
  - Plan Plus/Premium: el usuario elige entre manual o automático.
- **FR-017**: El sistema DEBE enviar notificación push al usuario en cada ejecución de operación (éxito o fallo).

**Planes y Suscripciones**
- **FR-018**: El sistema DEBE implementar 3 planes: Free (1 op/sem, $0), Plus (10 ops/sem, USD 20/mes), Premium (ilimitadas, USD 200/mes).
- **FR-019**: Cada transacción individual cuenta como una operación: 1 BUY = 1 operación, 1 SELL = 1 operación. Stop-loss ejecutado automáticamente NO cuenta.
- **FR-020**: El sistema DEBE bloquear ejecuciones cuando el usuario alcanza el límite semanal de su plan.
- **FR-021**: El límite semanal DEBE resetearse automáticamente cada lunes a las 00:00 UTC.
- **FR-022**: El sistema DEBE integrar MercadoPago para cobros de suscripciones recurrentes mensuales.
- **FR-023**: Los planes en MercadoPago DEBEN crearse automáticamente al iniciar el backend (idempotente).
- **FR-024**: El sistema DEBE procesar webhooks de MercadoPago para actualizar estados de suscripción.
- **FR-025**: El sistema DEBE soportar upgrade, downgrade y cancelación de plan desde la app.

**Historial y Dashboard**
- **FR-026**: El sistema DEBE mantener historial completo de operaciones (reales y simuladas, distinguidas).
- **FR-027**: El dashboard DEBE mostrar: balance de cuenta Binance, operaciones de la semana (usadas/límite), estado del bot (activo/pausado/modo), y últimas operaciones.
- **FR-028**: El historial DEBE incluir: símbolo, dirección (BUY/SELL), precio ejecutado, cantidad, resultado (ganancia/pérdida), timestamp, modo (real/simulación).

### Key Entities

**Users**
- `id` (UUID), `email`, `password_hash`, `auth_provider` (email/google/facebook), `oauth_id`
- `plan` (free/plus/premium), `plan_status` (active/cancelled/past_due)
- `operations_used_this_week` (int), `week_reset_at` (datetime)
- `is_active`, `created_at`, `updated_at`

**BinanceCredentials**
- `id`, `user_id` (FK), `api_key_encrypted`, `secret_key_encrypted`
- `is_active`, `last_verified_at`, `created_at`

**AIProviderCredentials**
- `id`, `user_id` (FK), `provider` (openai/groq/deepseek/gemini)
- `api_key_encrypted`, `is_active`, `created_at`

**TradingStrategies (Catálogo predefinido)**
- `id`, `name`, `slug`, `description`, `category`
- `system_prompt_template` (texto para el agente)
- `is_active`
  
  *Categorías y estrategias iniciales (12 mínimo):*
  - Dirección/Tendencia: Trend Following, Momentum Trading, Breakout Trading
  - Reversión/Valor: Mean Reversion, Range Trading
  - Arbitraje/Alta Frecuencia: Statistical Arbitrage, Market Making, Scalping Algorítmico
  - Datos Externos: News/Events Trading, On-Chain Analysis
  - Gestión Avanzada: Smart Beta/Rebalancing, Adaptive Risk Management, Fractal Models

**UserBotConfig**
- `id`, `user_id` (FK), `strategy_id` (FK)
- `ai_provider` (openai/groq/deepseek/gemini)
- `execution_mode` (manual/automatic)
- `risk_percent` (float), `stop_loss_percent` (float), `take_profit_percent` (float)
- `timeframe` (1m/5m/15m/1h/4h/1d), `allowed_symbols` (array)
- `max_operations_per_day` (int, optional limit adicional por usuario)
- `is_active`, `updated_at`

**Trades**
- `id` (UUID), `user_id` (FK), `symbol`, `side` (BUY/SELL)
- `order_type` (MARKET/LIMIT), `quantity` (decimal), `limit_price` (decimal, nullable)
- `stop_loss_percent` (float), `take_profit_percent` (float)
- `status` (pending/executed/failed/cancelled)
- `executed_price` (decimal), `executed_at` (datetime)
- `binance_order_id` (string), `is_simulation` (bool)
- `pnl` (profit/loss en USD, calculado post-cierre), `created_at`

**Subscriptions**
- `id`, `user_id` (FK), `plan` (free/plus/premium)
- `status` (active/cancelled/past_due/trialing)
- `mp_subscription_id`, `mp_preapproval_id`
- `current_period_start`, `current_period_end`, `next_billing_date`
- `cancelled_at` (nullable), `created_at`

**Payments**
- `id`, `user_id` (FK), `subscription_id` (FK)
- `mp_payment_id`, `amount` (decimal), `currency` (USD/ARS)
- `status` (approved/rejected/pending/refunded)
- `payment_method`, `created_at`

**Logs (Auditoría)**
- `id`, `user_id` (FK, nullable), `action` (string)
- `resource_type`, `resource_id`, `details` (JSONB)
- `ip_address`, `user_agent`, `created_at`

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un usuario nuevo puede registrarse, configurar Binance y activar el agente en menos de 5 minutos desde la descarga de la app.
- **SC-002**: El agente IA ejecuta una orden en Binance en menos de 3 segundos desde la decisión de compra/venta.
- **SC-003**: El sistema soporta al menos 500 usuarios activos simultáneos sin degradación de performance.
- **SC-004**: El 99.5% de las órdenes enviadas a Binance son registradas correctamente en el historial (cero pérdidas de datos de trades).
- **SC-005**: Los webhooks de MercadoPago actualizan el plan del usuario en menos de 10 segundos desde el pago aprobado.
- **SC-006**: El límite semanal de operaciones se aplica correctamente en el 100% de los casos (cero bypasses).
- **SC-007**: Las credenciales de Binance y proveedores IA nunca aparecen en texto plano en logs, respuestas API, ni base de datos.
- **SC-008**: El reset semanal del lunes 00:00 UTC ocurre con un margen de error menor a 1 minuto para todos los usuarios activos.

---

## Security Requirements *(mandatory — Constitution Principle III)*

### Credentials & Sensitive Data

- **Datos sensibles**: API keys de Binance (API Key + Secret Key), API keys de proveedores IA, contraseñas de usuarios, tokens de MercadoPago.
- **Encryption strategy**:
  - Binance API keys: Fernet (AES-256-CBC) con HMAC-SHA256. La clave de cifrado derivada de `USER_ID` + `APP_SECRET` (en `.env`, nunca en código).
  - AI Provider API keys: mismo mecanismo que Binance.
  - Contraseñas: bcrypt con salt automático (work factor 12).
- **Storage**: Solo en backend, tabla `binance_credentials` y `ai_provider_credentials`. Nunca en frontend.
- **Logging**: Solo últimos 4 caracteres de cualquier API key (`****abcd`). Tokens completos nunca en logs.

### Input Validation

- Pydantic V2 en todos los endpoints (FastAPI).
- ORM exclusivo (SQLAlchemy) — cero SQL raw con input del usuario.
- Límite de tamaño de payload: 1MB por request.
- Símbolos de trading: solo formato `[A-Z]{2,10}` (whitelist de símbolos activos de Binance).
- Cantidades: float positivo, máximo 8 decimales.

### Authentication & Authorization

- JWT obligatorio en todos los endpoints excepto `/auth/*` y `/webhooks/mercadopago`.
- Middleware de validación de plan en todos los endpoints de trading y agente.
- Webhook de MercadoPago: validación de signature + IP whitelist.

### Audit Trail

- Logs de: cada intento de login (éxito/fallo), cada ejecución de trade (éxito/fallo/bloqueo), cada cambio de plan, cada actualización de API keys, cada pago.
- Nivel: INFO para éxito, WARNING para intentos fallidos repetidos, ERROR para fallos de sistema.
- Retención: 2 años mínimo (cumplimiento regulatorio financiero).

---

## Validation Strategy *(mandatory — Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

Antes de cada ejecución de trade, el backend DEBE validar en este orden:

1. JWT válido y no expirado.
2. Plan del usuario activo (no `past_due`, no `cancelled`).
3. `operations_used_this_week` < límite del plan (excepto Premium).
4. Credenciales de Binance configuradas y activas.
5. Balance de Binance suficiente para la operación.
6. Símbolo en lista de `allowed_symbols` del `UserBotConfig`.
7. Capital de la operación ≤ `risk_percent` del balance total.
8. Stop-loss configurado (obligatorio para Free y Plus).

### Frontend Behavior

- Frontend solo **muestra** el estado actual (operaciones restantes, plan activo, etc.).
- La lógica de bloqueo reside **exclusivamente** en el backend.
- Si el frontend intenta forzar una operación bloqueada, el backend responde `HTTP 403` con mensaje de upgrade.

---

## Observability *(mandatory — Constitution Principle VI)*

### Metrics

- `trades.executed.total` — Counter — Trades ejecutados exitosamente
- `trades.failed.total` — Counter — Trades fallidos (Binance error)
- `trades.blocked.total` — Counter — Trades bloqueados por límite de plan
- `trades.execution_time_seconds` — Histogram — Latencia end-to-end de ejecución
- `binance.api.latency_seconds` — Histogram — Latencia de Binance API
- `ai_agent.decision_time_seconds` — Histogram — Tiempo de decisión del agente
- `subscriptions.active` — Gauge — Suscripciones activas por plan (labels: free/plus/premium)
- `webhooks.mercadopago.processed` — Counter — Webhooks procesados (labels: status)

### Alerts

- **CRITICAL**: Tasa de error de Binance API > 5% en ventana de 5 minutos.
- **CRITICAL**: Fallo de webhook de MercadoPago (pago no procesado).
- **WARNING**: Tiempo de ejecución de trade > 5s (P95).
- **WARNING**: Más de 10 operaciones bloqueadas por límite en 1 minuto (posible abuso).
- **INFO**: Reset semanal completado (con conteo de usuarios reseteados).

### Logging

- Formato: JSON estructurado (campo `timestamp`, `level`, `service`, `user_id`, `action`, `details`).
- Producción: nivel INFO+. Desarrollo: nivel DEBUG+.
- Campos prohibidos en logs: `api_key_full`, `secret_key`, `password`, `mp_access_token`.

---

## Architecture Overview

### Componentes del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (React Native)                │
│  Expo + Redux Toolkit + React Navigation                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Dashboard │ │Bot Config│ │Strategies│ │Subs/Pay  │  │
│  │Historial │ │Auth/Perfil│ │Binance   │ │Settings  │  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS / JWT
┌────────────────────────▼────────────────────────────────┐
│                   BACKEND (FastAPI)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │   api/   │ │ trading/ │ │ agents/  │ │payments/ │  │
│  │  auth    │ │ binance  │ │ core     │ │  mp      │  │
│  │  users   │ │ executor │ │ providers│ │  webhooks│  │
│  │  subs    │ │ validator│ │ strategies│ │         │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────────────────────────────────┐  │
│  │analytics/│ │            workers/ (Celery)          │  │
│  │ ta-lib   │ │  trade_executor  │  weekly_reset      │  │
│  │ pandas   │ │  agent_scheduler │  subscription_sync │  │
│  └──────────┘ └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                    │                │
┌────────▼──────┐   ┌─────────▼──────┐  ┌─────▼──────────┐
│  PostgreSQL   │   │  Redis (Cache  │  │  Binance API   │
│  (Externa,    │   │  + Celery      │  │  (ccxt lib)    │
│  no Docker)   │   │  + WebSockets) │  │                │
└───────────────┘   └────────────────┘  └────────────────┘
         │                                       │
┌────────▼──────┐                       ┌────────▼───────┐
│ MercadoPago   │                       │  AI Providers  │
│ SDK (Webhooks │                       │ OpenAI, Groq,  │
│  + Preapprove)│                       │ DeepSeek,      │
└───────────────┘                       │ Gemini         │
                                        └────────────────┘
```

### Docker Stack

```
docker-compose.yml
├── api          (FastAPI — puerto 8000)
├── worker       (Celery worker — trading/agent tasks)
├── scheduler    (Celery beat — cronjobs: reset semanal, sync subs)
├── redis        (Cache + message broker — puerto 6379)
└── [excluido]   PostgreSQL (externa, conectar vía .env)
```

### Build Móvil

```
docker-compose-mobile.yml
└── mobile-builder  (Node + Expo CLI — para generar APK/IPA)
```

---

## Assumptions

- **Solo Binance v1.0**: Aunque la arquitectura es extensible a otros exchanges (ccxt soporta 100+), v1.0 solo soporta Binance.
- **Solo Spot v1.0**: Sin Futures ni margin trading en esta versión.
- **Estrategias predefinidas**: No hay editor de estrategias custom. Los usuarios eligen del catálogo.
- **Solo MercadoPago v1.0**: Stripe y PayPal son extensiones futuras.
- **API keys propias de IA**: Cada usuario aporta su propia API key del proveedor IA elegido. No hay costo centralizado de IA.
- **Push notifications vía Firebase Cloud Messaging (FCM)**: Para Android e iOS.
- **Monolito modular**: El backend es un único servicio Docker con módulos bien separados, listo para extraer `agents/` como microservicio en v2.0 si la carga lo justifica.

---

**Status**: Draft | **Owner**: TRDIA Dev | **Last Updated**: 2026-03-06

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

<!--
  ACTION REQUIRED: Document security considerations for this feature.
  All features MUST address these areas per TRDIA Constitution.
-->

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** [Yes/No/N/A]
  - If Yes: [List what data: API keys, passwords, tokens, payment info, etc.]
  - **Encryption strategy**: [e.g., "Binance API keys encrypted with Fernet (AES-256)", "N/A", etc.]
  - **Storage**: [Backend only/Never persisted/Encrypted in DB, etc.]
  - **Logging**: [What can be logged, what MUST NOT appear in logs]

### Input Validation

- **Backend validation rules**: [List all inputs that must be validated, e.g., "Symbol format (BTCUSDT), quantity > 0, etc."]
- **SQL injection prevention**: [Strategy, e.g., "Pydantic models + SQLAlchemy ORM"]
- **Payload limits**: [Max request size, rate limiting requirements]

### Authentication & Authorization

- **Auth required?** [Yes/No]
- **Roles/plans that can access**: [e.g., "All authenticated users", "Plus and Premium only", "Admin only"]
- **Plan validation**: [If feature is plan-restricted, document validation strategy]

### Audit Trail

- **What must be logged**: [List events that need audit logs, e.g., "All trade executions", "Plan upgrades", "API key updates"]
- **Log level**: [INFO/WARNING/ERROR]
- **Sensitive data exclusion**: [Confirm no credentials/tokens in logs]

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

<!--
  ACTION REQUIRED: If this feature involves trading operations or subscription validation,
  document the backend validation strategy per Constitution Principle V.
-->

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** [Yes/No/N/A]
  - If Yes: [Document checks, e.g., "Validate operations_used < plan.limit before execution"]
  
- **Does this feature execute real monetary operations?** [Yes/No/N/A]
  - If Yes: [Document pre-execution checks, e.g., "Binance balance check", "Stop-loss validation"]

- **Capital limits**: [Document if max capital per operation applies, e.g., "Free: 10%, Plus: 20%, Premium: 50%"]

### Frontend Behavior

- **Frontend role**: [Display only/Soft warning/etc. - NEVER business logic enforcement]
- **How frontend gets validation state**: [API endpoint that returns current status]

## Observability *(mandatory - Constitution Principle VI)*

<!--
  ACTION REQUIRED: Define metrics and monitoring for this feature.
-->

### Metrics

- **[metric_name_1]**: [Type: Counter/Gauge/Histogram] - [Description, e.g., "trades.executed.count - Total trades executed"]
- **[metric_name_2]**: [Type] - [Description]

### Alerts

- **Alert 1**: [Condition that triggers alert, e.g., "Error rate > 5% in 5 min window"]
- **Alert 2**: [Condition]

### Logging

- **Key events to log**: [List important events, e.g., "Trade execution start/success/failure", "API key validation"]
- **Log level**: [INFO/DEBUG/ERROR per event type]
