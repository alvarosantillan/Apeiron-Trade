# Feature Specification: TRDIA - Dashboard e Historial de Operaciones

**Feature Branch**: `008-dashboard-history`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Resumen operativo y trazabilidad histórica"

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

### User Story 1 - Ver estado actual de cuenta y bot (Priority: P1)

Como usuario, quiero abrir la app y ver un resumen claro de mi estado operativo para tomar decisiones rápidas.

**Why this priority**: Es la pantalla más consultada y base de usabilidad diaria.

**Independent Test**: Se prueba cargando dashboard con datos de usuario y validando métricas clave visibles.

**Acceptance Scenarios**:

1. **Given** usuario autenticado con operaciones recientes, **When** ingresa al dashboard, **Then** ve balance, plan, operaciones usadas/limite semanal y estado del bot.
2. **Given** bot pausado, **When** usuario consulta dashboard, **Then** visualiza estado "pausado" con última actualización registrada.

---

### User Story 2 - Consultar historial filtrable de operaciones (Priority: P2)

Como usuario, quiero explorar historial de operaciones con filtros para analizar desempeño y comportamiento del agente.

**Why this priority**: Es esencial para evaluación de resultados y confianza del usuario.

**Independent Test**: Se prueba listando historial y aplicando filtros por fecha, tipo, estado y modo real/simulado.

**Acceptance Scenarios**:

1. **Given** historial con operaciones mixtas, **When** el usuario filtra por `is_simulation=true`, **Then** solo ve operaciones de simulación.

---

### User Story 3 - Inspeccionar detalle de operación (Priority: P3)

Como usuario, quiero abrir una operación específica para entender qué pasó en esa ejecución.

**Why this priority**: Mejora transparencia y reduce tickets de soporte.

**Independent Test**: Se valida obteniendo detalle por `trade_id` y mostrando datos completos de ejecución.

**Acceptance Scenarios**:

1. **Given** una operación registrada, **When** el usuario abre su detalle, **Then** ve símbolo, lado, precio, cantidad, estado, timestamp, resultado y referencia de ejecución.

---

### User Story 4 - Visualizar KPIs de rendimiento recientes (Priority: P4)

Como usuario, quiero indicadores de rendimiento recientes para evaluar si mantener o ajustar estrategia.

**Why this priority**: Conecta operación diaria con toma de decisiones estratégicas.

**Independent Test**: Se prueba con dataset de operaciones y cálculo de KPIs de ventana configurable.

**Acceptance Scenarios**:

1. **Given** operaciones históricas disponibles, **When** se consulta sección de rendimiento, **Then** se muestran métricas agregadas de periodo (win rate, PnL neto, operaciones totales).

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- Usuario nuevo sin operaciones aún.
- Operaciones en alta frecuencia con paginación profunda.
- Datos de balance temporalmente no disponibles por exchange.
- Historial con eventos inconsistentes (operación sin precio final).
- Filtros combinados que devuelven cero resultados.
- Diferencias de zona horaria en presentación de timestamps.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: El sistema MUST mostrar en dashboard resumen de cuenta: plan activo, operaciones usadas/límite, estado del bot y últimas operaciones.
- **FR-002**: El sistema MUST mostrar balance disponible y timestamp de última sincronización.
- **FR-003**: El sistema MUST permitir listar historial paginado de operaciones.
- **FR-004**: El sistema MUST permitir filtrar historial por rango de fechas.
- **FR-005**: El sistema MUST permitir filtrar por estado de operación (`executed`, `failed`, `blocked`, `cancelled`).
- **FR-006**: El sistema MUST permitir filtrar por modo (`real` vs `simulación`).
- **FR-007**: El sistema MUST exponer detalle completo de operación por identificador.
- **FR-008**: El sistema MUST distinguir visualmente operaciones simuladas y reales.
- **FR-009**: El sistema MUST incluir en cada operación campos de trazabilidad mínima (origen, timestamp, resultado, motivo de fallo si aplica).
- **FR-010**: El sistema MUST mostrar KPIs agregados de periodo configurable (mínimo 7d y 30d).
- **FR-011**: El sistema MUST responder de forma consistente para usuarios sin historial (estado vacío informativo).
- **FR-012**: El sistema MUST proteger endpoints de dashboard/historial con autenticación.
- **FR-013**: El sistema MUST soportar ordenamiento cronológico descendente por defecto.
- **FR-014**: El sistema MUST registrar acceso a detalle de operación en auditoría para soporte y trazabilidad.

### Key Entities *(include if feature involves data)*

- **DashboardSnapshot**: resumen de estado por usuario. Campos: `user_id`, `plan_code`, `operations_used`, `operations_limit`, `bot_status`, `balance_snapshot`, `updated_at`.
- **TradeHistoryItem**: ítem de listado de operaciones. Campos: `trade_id`, `symbol`, `side`, `status`, `executed_price`, `quantity`, `is_simulation`, `pnl`, `created_at`.
- **TradeDetailView**: vista extendida por operación. Campos: `trade_id`, `request_id`, `execution_trace`, `failure_reason`, `risk_params`, `notification_refs`.
- **PerformanceKPI**: métricas agregadas por ventana temporal. Campos: `user_id`, `window`, `total_trades`, `win_rate`, `net_pnl`, `avg_return`, `updated_at`.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 95% de cargas de dashboard completan en menos de 2 segundos.
- **SC-002**: 95% de consultas de historial paginado responden en menos de 3 segundos.
- **SC-003**: 100% de operaciones mostradas incluyen etiquetado correcto real/simulación.
- **SC-004**: 99% de detalles de operación contienen trazabilidad mínima completa.
- **SC-005**: Reducción del 30% en consultas de soporte relacionadas con "no sé qué pasó con mi operación" tras habilitar detalle completo.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

<!--
  ACTION REQUIRED: Document security considerations for this feature.
  All features MUST address these areas per TRDIA Constitution.
-->

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: historial de operaciones financieras y métricas de rendimiento.
  - **Encryption strategy**: acceso autenticado, almacenamiento protegido y minimización de exposición.
  - **Storage**: backend only; frontend recibe solo datos necesarios para visualización.
  - **Logging**: no exponer credenciales ni datos sensibles no necesarios.

### Input Validation

- **Backend validation rules**: validar filtros (fechas, estados, página, tamaño), IDs de operación y pertenencia al usuario autenticado.
- **SQL injection prevention**: validación + ORM.
- **Payload limits**: límites de paginación y rate limiting de consultas intensivas.

### Authentication & Authorization

- **Auth required?** Yes
- **Roles/plans that can access**: todos los usuarios autenticados consultan su propio dashboard/historial.
- **Plan validation**: no bloquea acceso por plan; muestra contexto de límites y estado de suscripción.

### Audit Trail

- **What must be logged**: accesos a dashboard, consultas de historial, apertura de detalle de operación, errores de consulta.
- **Log level**: INFO/WARNING/ERROR.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

<!--
  ACTION REQUIRED: If this feature involves trading operations or subscription validation,
  document the backend validation strategy per Constitution Principle V.
-->

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** No para lectura, pero debe mostrar estado de límite actual.
  
- **Does this feature execute real monetary operations?** No.

- **Capital limits**: N/A.

### Frontend Behavior

- **Frontend role**: visualizar y filtrar datos; no altera lógica de negocio.
- **How frontend gets validation state**: endpoints de dashboard/historial/detalle con datos calculados por backend.

## Observability *(mandatory - Constitution Principle VI)*

<!--
  ACTION REQUIRED: Define metrics and monitoring for this feature.
-->

### Metrics

- **dashboard.load.success_total**: Counter - Cargas exitosas de dashboard.
- **dashboard.load.latency_seconds**: Histogram - Latencia de carga de dashboard.
- **history.query.success_total**: Counter - Consultas exitosas de historial.
- **history.query.latency_seconds**: Histogram - Latencia de historial.
- **history.query.empty_total**: Counter - Consultas sin resultados.
- **trade.detail.view_total**: Counter - Aperturas de detalle de operación.

### Alerts

- **Alert 1**: `dashboard.load.latency_seconds` p95 > 3s durante 15 minutos.
- **Alert 2**: error rate de `history.query` > 5% en ventana de 10 minutos.

### Logging

- **Key events to log**: dashboard_loaded, history_queried, trade_detail_viewed, history_filter_applied, query_failed.
- **Log level**: INFO para uso normal, WARNING para respuestas degradadas, ERROR para fallos de backend.

