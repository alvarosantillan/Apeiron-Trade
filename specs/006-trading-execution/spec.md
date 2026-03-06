# Feature Specification: TRDIA - Ejecucion de Trading Spot

**Feature Branch**: `006-trading-execution`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Ejecucion real y simulada con validacion estricta"

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

### User Story 1 - Ejecutar operacion Spot validada (Priority: P1)

Como usuario, quiero ejecutar una operación Spot (BUY/SELL) para materializar la decisión del bot o una acción manual dentro de reglas seguras.

**Why this priority**: Es el núcleo funcional del producto: convertir señales en operaciones reales o simuladas.

**Independent Test**: Se prueba end-to-end con una solicitud de ejecución y validación de persistencia en historial.

**Acceptance Scenarios**:

1. **Given** usuario con credenciales Binance válidas y balance suficiente, **When** envía orden Spot MARKET, **Then** la orden se ejecuta y se registra en historial como `executed`.
2. **Given** usuario sin balance suficiente, **When** intenta ejecutar orden, **Then** backend rechaza con motivo `insufficient_balance` y no consume operación.

---

### User Story 2 - Aplicar límites de plan en backend (Priority: P2)

Como sistema, quiero aplicar en backend los límites por plan para asegurar monetización y evitar bypass por frontend.

**Why this priority**: Regla de negocio crítica del modelo Free/Plus/Premium.

**Independent Test**: Se prueba con cuentas Free/Plus/Premium en diferentes contadores semanales.

**Acceptance Scenarios**:

1. **Given** usuario Free con 1 operación usada, **When** intenta ejecutar una orden real adicional, **Then** backend bloquea con error `weekly_limit_exceeded`.

---

### User Story 3 - Operar en simulación sin consumo de límite (Priority: P3)

Como usuario de cualquier plan, quiero ejecutar operaciones simuladas para probar estrategias sin riesgo y sin consumir cupo semanal.

**Why this priority**: Reduce barrera de entrada y aumenta adopción.

**Independent Test**: Se prueba ejecutando operaciones simuladas y verificando contador semanal intacto.

**Acceptance Scenarios**:

1. **Given** usuario Free con límite real agotado, **When** ejecuta orden en `paper trading`, **Then** la operación simulada se registra y el contador real no cambia.

---

### User Story 4 - Notificar y auditar cada ejecución (Priority: P4)

Como usuario, quiero notificación y trazabilidad de cada operación para entender resultado y confiar en la automatización.

**Why this priority**: Requisito explícito de producto y factor de confianza.

**Independent Test**: Se valida con ejecución exitosa y fallida comprobando notificación y log de auditoría.

**Acceptance Scenarios**:

1. **Given** una ejecución exitosa, **When** finaliza la operación, **Then** el usuario recibe notificación push con resumen.
2. **Given** una ejecución fallida, **When** se detecta error, **Then** se registra auditoría con motivo y se notifica fallo al usuario.

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- Error temporal de Binance durante envío de orden.
- Timeout de red tras enviar orden (estado incierto).
- Orden duplicada por reintento del cliente.
- Diferencias de precisión de lote/precio por símbolo.
- Cambio de plan en medio de una ráfaga de ejecuciones.
- Desincronización entre contador semanal y reset programado.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: El sistema MUST ejecutar operaciones Spot BUY/SELL tipo MARKET y LIMIT.
- **FR-002**: El sistema MUST validar en backend plan activo, límite semanal y elegibilidad antes de cualquier ejecución real.
- **FR-003**: El sistema MUST contar cada BUY y cada SELL como una operación independiente.
- **FR-004**: El sistema MUST excluir ejecuciones de simulación del contador semanal.
- **FR-005**: El sistema MUST bloquear ejecución real al superar límite semanal (Free=1, Plus=10, Premium=ilimitado).
- **FR-006**: El sistema MUST validar balance suficiente antes de enviar orden al exchange.
- **FR-007**: El sistema MUST validar símbolo permitido y parámetros de riesgo del usuario.
- **FR-008**: El sistema MUST aplicar idempotencia por `request_id` para evitar doble ejecución.
- **FR-009**: El sistema MUST registrar toda ejecución con estado final (`executed`, `failed`, `blocked`, `cancelled`).
- **FR-010**: El sistema MUST registrar motivo detallado de fallos y bloqueos.
- **FR-011**: El sistema MUST enviar notificación por cada ejecución exitosa o fallida.
- **FR-012**: El sistema MUST soportar modo manual (aprobación previa) y automático según plan/configuración.
- **FR-013**: El sistema MUST reintentar de forma controlada errores transitorios del exchange sin duplicar órdenes.
- **FR-014**: El sistema MUST exponer historial de operaciones con diferenciación real/simulación.
- **FR-015**: El sistema MUST conservar trazabilidad completa desde señal/solicitud hasta resultado final.

### Key Entities *(include if feature involves data)*

- **TradeRequest**: solicitud inicial de operación. Campos: `request_id`, `user_id`, `symbol`, `side`, `order_type`, `quantity`, `limit_price`, `is_simulation`, `source`.
- **TradeExecution**: resultado final de una ejecución. Campos: `trade_id`, `request_id`, `status`, `executed_price`, `executed_qty`, `exchange_order_id`, `failure_reason`, `created_at`.
- **WeeklyOperationCounter**: control de uso por semana. Campos: `user_id`, `week_start_utc`, `operations_used`, `plan_limit`, `updated_at`.
- **TradeAuditEvent**: eventos de trazabilidad. Campos: `trade_id`, `event_type`, `event_payload`, `created_at`.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 95% de ejecuciones válidas finalizan (éxito o fallo definitivo) en menos de 5 segundos.
- **SC-002**: 100% de bloqueos por límite semanal ocurren en backend (cero bypass).
- **SC-003**: 100% de operaciones simuladas no incrementan contador semanal.
- **SC-004**: 99% de ejecuciones registran historial completo en menos de 10 segundos.
- **SC-005**: 99% de eventos de ejecución generan notificación al usuario en menos de 10 segundos.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

<!--
  ACTION REQUIRED: Document security considerations for this feature.
  All features MUST address these areas per TRDIA Constitution.
-->

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: credenciales exchange (indirectas), montos, estado de cuenta y decisiones operativas.
  - **Encryption strategy**: credenciales cifradas en backend; referencia segura en tiempo de ejecución.
  - **Storage**: backend solamente; frontend recibe datos enmascarados y resultados no sensibles.
  - **Logging**: no loggear claves ni secretos; solo identificadores y motivos.

### Input Validation

- **Backend validation rules**: validar símbolo, lado, tipo orden, cantidad > 0, precio > 0 si LIMIT, request_id único, modo permitido por plan.
- **SQL injection prevention**: validación de esquemas + ORM.
- **Payload limits**: límite de tamaño de request y rate limiting por usuario en endpoints de ejecución.

### Authentication & Authorization

- **Auth required?** Yes
- **Roles/plans that can access**: usuarios autenticados Free/Plus/Premium.
- **Plan validation**: enforcement estricto en backend por estado de suscripción y contador semanal.

### Audit Trail

- **What must be logged**: solicitud recibida, validación de reglas, orden enviada, respuesta exchange, bloqueo, fallo y notificación emitida.
- **Log level**: INFO para flujo normal, WARNING para bloqueos/validaciones, ERROR para fallos internos/exchange.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

<!--
  ACTION REQUIRED: If this feature involves trading operations or subscription validation,
  document the backend validation strategy per Constitution Principle V.
-->

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** Yes
  - Checks: `plan_status=active`, `operations_used < plan_limit` para ejecución real, Free siempre manual.
  
- **Does this feature execute real monetary operations?** Yes
  - Checks pre-ejecución: balance, símbolo habilitado, modo permitido, parámetros de riesgo, idempotencia.

- **Capital limits**: respetar límites por plan definidos en constitución (Free 10%, Plus 20%, Premium 50% del balance por operación).

### Frontend Behavior

- **Frontend role**: enviar solicitudes y mostrar estado; no puede autorizar por sí solo operaciones prohibidas.
- **How frontend gets validation state**: endpoint de estado de cuenta operativa y resultado de validación de backend.

## Observability *(mandatory - Constitution Principle VI)*

<!--
  ACTION REQUIRED: Define metrics and monitoring for this feature.
-->

### Metrics

- **trading.request.received_total**: Counter - Solicitudes de ejecución recibidas.
- **trading.execution.success_total**: Counter - Ejecuciones exitosas.
- **trading.execution.failure_total**: Counter - Ejecuciones fallidas.
- **trading.execution.blocked_total**: Counter - Bloqueos por reglas de negocio.
- **trading.execution.simulation_total**: Counter - Ejecuciones en modo simulación.
- **trading.execution.latency_seconds**: Histogram - Latencia end-to-end de ejecución.

### Alerts

- **Alert 1**: tasa de `trading.execution.failure_total` > 5% en ventana de 5 minutos.
- **Alert 2**: `trading.execution.blocked_total` anómalo (>3x baseline) en 15 minutos.

### Logging

- **Key events to log**: trade_requested, trade_validated, trade_blocked, trade_sent_to_exchange, trade_executed, trade_failed, trade_simulated, notification_sent.
- **Log level**: INFO/WARNING/ERROR según severidad.

