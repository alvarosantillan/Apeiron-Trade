# Data Model: TRDIA - Persistence and Hardening Baseline

**Feature**: `009-persistence-hardening`  
**Date**: 2026-03-09

## Entity: UserAccount

- Purpose: Identidad de usuario y credenciales para autenticacion.
- Fields:
  - `id` (UUID, PK)
  - `email` (string, unique, indexed)
  - `password_hash` (string)
  - `status` (enum: ACTIVE, DISABLED)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `email` formato valido y unico.
  - `password_hash` obligatorio; nunca exponer en respuestas API ni logs.

## Entity: AuthSession

- Purpose: Gestion de sesiones y refresh tokens revocables.
- Fields:
  - `id` (UUID, PK)
  - `user_id` (UUID, FK -> UserAccount.id)
  - `refresh_token_id` (string, unique)
  - `expires_at` (timestamp)
  - `revoked_at` (timestamp, nullable)
  - `created_at` (timestamp)
- Validation Rules:
  - `expires_at > created_at`.
  - Sesion revocada no puede reutilizarse.
- State Transitions:
  - `ACTIVE` -> `REVOKED` (logout o invalidacion de seguridad)
  - `ACTIVE` -> `EXPIRED` (por tiempo)

## Entity: AIAgentConfig

- Purpose: Configuracion activa del agente IA por usuario.
- Fields:
  - `id` (UUID, PK)
  - `user_id` (UUID, FK -> UserAccount.id)
  - `provider` (enum/string controlado)
  - `strategy_id` (string)
  - `mode` (enum: SIMULATION, LIVE)
  - `is_active` (boolean)
  - `updated_at` (timestamp)
- Validation Rules:
  - Una sola configuracion activa por `user_id`.
  - `provider` y `mode` en conjunto permitido por backend.

## Entity: TradingExecution

- Purpose: Registro persistente de ejecucion para trazabilidad operativa.
- Fields:
  - `id` (UUID, PK)
  - `user_id` (UUID, FK -> UserAccount.id)
  - `request_id` (string, unique por usuario)
  - `status` (enum: PENDING, EXECUTED, FAILED, CANCELLED, BLOCKED)
  - `execution_type` (enum: BUY, SELL)
  - `symbol` (string)
  - `quantity` (decimal)
  - `price` (decimal, nullable)
  - `error_code` (string, nullable)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `quantity > 0`.
  - `request_id` idempotente para reintentos.
- State Transitions:
  - `PENDING` -> `EXECUTED`
  - `PENDING` -> `FAILED`
  - `PENDING` -> `CANCELLED`
  - `PENDING` -> `BLOCKED`

## Entity: NotificationDelivery

- Purpose: Historial de envios/notificaciones y estado final.
- Fields:
  - `id` (UUID, PK)
  - `user_id` (UUID, FK -> UserAccount.id)
  - `event_id` (string, unique)
  - `category` (string/enum)
  - `priority` (enum: LOW, MEDIUM, HIGH)
  - `status` (enum: PENDING, SENT, FAILED)
  - `payload_ref` (string/jsonb, nullable)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `event_id` idempotente para evitar reenvios duplicados.
  - `status` solo permite transiciones validas por flujo.

## Entity: PersistenceAuditEvent

- Purpose: Auditoria de operaciones criticas de persistencia y fallos.
- Fields:
  - `id` (UUID, PK)
  - `user_id` (UUID, nullable)
  - `domain` (enum: AUTH, TRADING, NOTIFICATIONS, AI_AGENT, DB)
  - `action` (string)
  - `outcome` (enum: SUCCESS, FAILURE)
  - `error_type` (string, nullable)
  - `trace_id` (string, nullable)
  - `created_at` (timestamp)
- Validation Rules:
  - Nunca incluir secretos ni tokens completos en metadatos.
  - `outcome=FAILURE` debe incluir `error_type`.

## Relationships

- `UserAccount` 1..N `AuthSession`
- `UserAccount` 1..N `TradingExecution`
- `UserAccount` 1..N `NotificationDelivery`
- `UserAccount` 1..N `AIAgentConfig` (maximo 1 activo)
- `UserAccount` 1..N `PersistenceAuditEvent`

## Consistency and Idempotency Rules

- `TradingExecution.request_id` y `NotificationDelivery.event_id` son llaves de idempotencia obligatorias.
- Escrituras criticas se ejecutan en transaccion para evitar estados parciales.
- Fallos de DB generan `PersistenceAuditEvent` y error controlado al cliente.
- Reinicio de backend no elimina estado persistido ni invalida historiales ya confirmados.
