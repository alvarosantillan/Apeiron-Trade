# Data Model: TRDIA - Trading Execution

**Feature**: `006-trading-execution`  
**Date**: 2026-03-06

## Entity: TradeRequest

- Purpose: Registrar la intención inicial de ejecutar una operación.
- Fields:
  - `id` (UUID)
  - `request_id` (string, unique por usuario)
  - `user_id` (UUID, FK)
  - `source` (enum: MANUAL, AI_AGENT)
  - `symbol` (string)
  - `side` (enum: BUY, SELL)
  - `order_type` (enum: MARKET, LIMIT)
  - `quantity` (decimal)
  - `limit_price` (decimal, nullable)
  - `is_simulation` (bool)
  - `requested_at` (timestamp)
- Validation Rules:
  - `quantity > 0`
  - `order_type=LIMIT` requiere `limit_price > 0`
  - `request_id` obligatorio para idempotencia

## Entity: TradeExecution

- Purpose: Representar el resultado operativo de una solicitud.
- Fields:
  - `id` (UUID)
  - `trade_request_id` (UUID, FK -> TradeRequest)
  - `user_id` (UUID, FK)
  - `mode` (enum: MANUAL, AUTOMATIC)
  - `execution_type` (enum: REAL, PAPER)
  - `status` (enum: RECEIVED, VALIDATED, BLOCKED, SUBMITTED, EXECUTED, FAILED, PENDING_RECONCILIATION, CANCELLED)
  - `executed_price` (decimal, nullable)
  - `executed_qty` (decimal, nullable)
  - `exchange_order_id` (string, nullable)
  - `failure_reason` (string, nullable)
  - `blocked_reason` (string, nullable)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `status=BLOCKED` requiere `blocked_reason`
  - `status=FAILED` requiere `failure_reason`
  - `status=EXECUTED` requiere `executed_price` y `executed_qty`

## Entity: WeeklyOperationCounter

- Purpose: Controlar consumo de operaciones reales por plan y semana.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `week_start_utc` (date)
  - `operations_used` (integer)
  - `plan_limit` (integer nullable para ilimitado)
  - `updated_at` (timestamp)
- Validation Rules:
  - Solo incrementa con `execution_type=REAL` y estado terminal válido.
  - BUY y SELL cuentan cada una como 1.

## Entity: TradeAuditEvent

- Purpose: Auditoría detallada del ciclo de ejecución.
- Fields:
  - `id` (UUID)
  - `trade_execution_id` (UUID, FK -> TradeExecution)
  - `event_type` (string)
  - `event_payload` (jsonb)
  - `created_at` (timestamp)
- Validation Rules:
  - Debe existir al menos un evento por transición de estado.

## Relationships

- `TradeRequest` 1..N `TradeExecution` (en la práctica 1..1 bajo idempotencia)
- `TradeExecution` 1..N `TradeAuditEvent`
- `User` 1..N `WeeklyOperationCounter` (por semana)

## State Transitions

## Real Execution Flow

- `RECEIVED` -> `VALIDATED` -> `SUBMITTED` -> `EXECUTED`
- `RECEIVED|VALIDATED` -> `BLOCKED`
- `SUBMITTED` -> `FAILED`
- `SUBMITTED` -> `PENDING_RECONCILIATION` -> `EXECUTED|FAILED|CANCELLED`

## Paper Execution Flow

- `RECEIVED` -> `VALIDATED` -> `EXECUTED`
- `RECEIVED|VALIDATED` -> `BLOCKED`

## Counter Update Rule

- Incrementar `operations_used` en transición a `EXECUTED` con `execution_type=REAL`.
- No incrementar para `PAPER`.
