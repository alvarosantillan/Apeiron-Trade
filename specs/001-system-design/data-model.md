# Data Model: TRDIA - System Design Foundation

**Feature**: `001-system-design`  
**Date**: 2026-03-07

## Core Entity: User

- Purpose: Identidad principal y contexto de plan para todo flujo.
- Fields:
  - `id` (UUID)
  - `email` (string)
  - `auth_provider` (enum: EMAIL, GOOGLE, FACEBOOK)
  - `plan_code` (enum: FREE, PLUS, PREMIUM)
  - `plan_status` (enum: ACTIVE, CANCELLED, PAST_DUE)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)

## Core Entity: Subscription

- Purpose: Estado de suscripción y ciclo de facturación.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `provider` (enum: MERCADOPAGO)
  - `provider_subscription_id` (string)
  - `status` (enum: ACTIVE, CANCELLED, PAST_DUE, TRIALING)
  - `period_start` (timestamp)
  - `period_end` (timestamp)
  - `next_billing_at` (timestamp)

## Core Entity: OperationCounter

- Purpose: Control de operaciones semanales por usuario para enforcement de plan.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `week_start_utc` (date)
  - `operations_used` (integer)
  - `plan_limit` (integer nullable)
  - `updated_at` (timestamp)

## Core Entity: ExchangeCredential

- Purpose: Credenciales cifradas de integración con exchange por usuario.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `exchange` (enum: BINANCE)
  - `api_key_encrypted` (text)
  - `secret_key_encrypted` (text)
  - `is_active` (bool)
  - `last_verified_at` (timestamp)

## Core Entity: AIProviderCredential

- Purpose: API key cifrada de proveedor IA por usuario.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `provider` (enum: OPENAI, GROQ, DEEPSEEK, GEMINI)
  - `api_key_encrypted` (text)
  - `is_active` (bool)
  - `updated_at` (timestamp)

## Core Entity: Trade

- Purpose: Registro canónico de ejecución de operación.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `symbol` (string)
  - `side` (enum: BUY, SELL)
  - `order_type` (enum: MARKET, LIMIT)
  - `status` (enum: PENDING, EXECUTED, FAILED, BLOCKED, CANCELLED)
  - `is_simulation` (bool)
  - `executed_price` (decimal nullable)
  - `quantity` (decimal)
  - `pnl` (decimal nullable)
  - `created_at` (timestamp)

## Core Entity: AuditLog

- Purpose: Trazabilidad de eventos de seguridad y negocio.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID nullable)
  - `action` (string)
  - `resource_type` (string)
  - `resource_id` (string)
  - `details` (jsonb)
  - `created_at` (timestamp)

## Relationships Summary

- `User` 1..N `Subscription` (histórico)
- `User` 1..N `OperationCounter` (por semana)
- `User` 1..N `ExchangeCredential`
- `User` 1..N `AIProviderCredential`
- `User` 1..N `Trade`
- `User` 1..N `AuditLog`

## Cross-Domain Invariants

- Toda ejecución real de trade debe validar `Subscription` + `OperationCounter`.
- Credenciales de exchange/IA nunca se exponen en respuestas públicas.
- Eventos críticos deben generar `AuditLog`.
