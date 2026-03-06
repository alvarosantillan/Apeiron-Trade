# Data Model: TRDIA - Dashboard and Trade History

**Feature**: `008-dashboard-history`  
**Date**: 2026-03-06

## Entity: DashboardSnapshot

- Purpose: Resumen operativo de alto nivel mostrado al iniciar dashboard.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `plan_code` (string)
  - `operations_used` (integer)
  - `operations_limit` (integer nullable)
  - `bot_status` (enum: ACTIVE, PAUSED, INACTIVE)
  - `balance_snapshot` (decimal nullable)
  - `last_sync_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - Snapshot siempre scoped al `user_id` autenticado.
  - `operations_used >= 0`.

## Entity: TradeHistoryItem

- Purpose: Registro resumido para listado paginado de operaciones.
- Fields:
  - `trade_id` (UUID)
  - `user_id` (UUID, FK)
  - `symbol` (string)
  - `side` (enum: BUY, SELL)
  - `status` (enum: EXECUTED, FAILED, BLOCKED, CANCELLED)
  - `executed_price` (decimal nullable)
  - `quantity` (decimal)
  - `is_simulation` (bool)
  - `pnl` (decimal nullable)
  - `created_at` (timestamp)
- Validation Rules:
  - `quantity > 0`.
  - Etiqueta real/simulación obligatoria.

## Entity: TradeDetailView

- Purpose: Vista detallada de una operación para inspección por usuario.
- Fields:
  - `trade_id` (UUID, PK/FK)
  - `user_id` (UUID, FK)
  - `request_id` (string)
  - `execution_trace` (jsonb)
  - `failure_reason` (string nullable)
  - `risk_params` (jsonb nullable)
  - `notification_refs` (jsonb nullable)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - Solo accesible por dueño de la operación.
  - Debe incluir trazabilidad mínima incluso en fallos.

## Entity: PerformanceKPI

- Purpose: Métricas agregadas por ventana temporal para evaluación rápida.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `window` (enum: D7, D30)
  - `total_trades` (integer)
  - `win_rate` (decimal)
  - `net_pnl` (decimal)
  - `avg_return` (decimal)
  - `updated_at` (timestamp)
- Validation Rules:
  - `win_rate` en rango [0,1].
  - `total_trades >= 0`.

## Entity: TradeDetailAccessAudit

- Purpose: Auditoría de acceso a detalle de operación.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `trade_id` (UUID)
  - `accessed_at` (timestamp)
  - `source` (enum: MOBILE_APP, SUPPORT_VIEW)
- Validation Rules:
  - Registro por cada acceso exitoso a detalle.

## Relationships

- `User` 1..1 `DashboardSnapshot` (vigente)
- `User` 1..N `TradeHistoryItem`
- `TradeHistoryItem` 1..1 `TradeDetailView`
- `User` 1..N `PerformanceKPI` (una fila por ventana)
- `TradeDetailView` 1..N `TradeDetailAccessAudit`

## State and Refresh Rules

- `DashboardSnapshot` se refresca por eventos de ejecución/suscripción o por job periódico.
- `PerformanceKPI` se actualiza por ventana en refresh incremental.
- Historial se consulta en tiempo real con paginación y filtros validados.
