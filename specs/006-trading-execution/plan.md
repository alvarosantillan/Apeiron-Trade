# Implementation Plan: TRDIA - Trading Execution

**Branch**: `006-trading-execution` | **Date**: 2026-03-06 | **Spec**: `specs/006-trading-execution/spec.md`
**Input**: Feature specification from `/specs/006-trading-execution/spec.md`

## Summary

Implementar el motor de ejecución de trading Spot para operaciones reales y simuladas con validación estricta en backend (plan, límites, riesgo, balance, idempotencia), trazabilidad completa de cada solicitud y notificaciones por resultado.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, integración Binance Spot (módulo existente), Celery, Redis  
**Storage**: PostgreSQL externa (`trade_requests`, `trade_executions`, `weekly_operation_counters`, `trade_audit_events`)  
**Testing**: pytest, pytest-asyncio, httpx, mocks de exchange, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: p95 de ejecución <= 5s; p99 de registro en historial <= 10s  
**Constraints**: validación backend no bypassable; operación real consume límite por lado; paper trading ilimitado y sin consumo  
**Scale/Scope**: v1 Spot-only, MARKET/LIMIT, modo manual y automático según plan

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: Plan de pruebas contract/integration/unit definido
- [x] **Principle III (Security-First)**:
  - [x] Sin secretos ni credenciales en logs
  - [x] Validación de inputs de ejecución definida
  - [x] Reglas de autorización y auditoría documentadas
  - [x] Mecanismo de idempotencia para evitar doble ejecución
- [x] **Principle IV (Modular)**: Encaja en `trading/`, `api/`, `workers/`, `notifications/`
- [x] **Principle V (Validation-Strict)**:
  - [x] Validación backend de límites por plan definida
  - [x] Reglas de consumo de operación por BUY/SELL documentadas
  - [x] Simulación excluida del contador semanal
- [x] **Principle VI (Observability)**: Métricas, alertas y logging estructurado definidos
- [x] **Principle VII (Progressive Enhancement)**: alcance acotado a Spot y tipos de orden MVP

## Project Structure

### Documentation (this feature)

```text
specs/006-trading-execution/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── trading-execution.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── trading/
│   ├── services/
│   │   ├── execution/
│   │   ├── risk/
│   │   └── counters/
│   ├── models/
│   ├── schemas/
│   └── workers/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
└── src/
    └── screens/
        └── trading/
```

**Structure Decision**: Back-end como fuente única de decisión/validación; frontend solo inicia solicitud, aprueba manualmente cuando aplique y visualiza estado.

## Phase Plan

### Phase 0 - Research Decisions

1. Política de idempotencia y deduplicación de solicitudes (`request_id`)
2. Estrategia de consistencia ante timeout con estado incierto de orden
3. Reglas de consumo de límite semanal por tipo de operación/modo
4. Reintentos transitorios sin riesgo de ejecución duplicada

### Phase 1 - Design Artifacts

1. `data-model.md` con request, execution, contador semanal y auditoría
2. `contracts/trading-execution.openapi.yaml` para validar/ejecutar/listar operaciones
3. `quickstart.md` para pruebas end-to-end de real/paper y enforcement por plan

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por historias P1-P4
- tests-first obligatorios
- secuencia: validación -> ejecución -> deduplicación -> historial/auditoría -> notificaciones

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de ejecución e historial
2. Integration tests con escenarios: éxito, balance insuficiente, límite excedido, timeout exchange, solicitud duplicada
3. Unit tests para validador de plan/límite, idempotencia, transición de estados y lógica de simulación
4. Coverage gate:
   - módulo trading/execution >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: doble ejecución por reintento del cliente
  - Mitigación: llave idempotente única + locking transaccional
- Riesgo: estado incierto tras timeout de exchange
  - Mitigación: estado `pending_reconciliation` + job de reconciliación por `exchange_order_id`
- Riesgo: drift entre contador semanal y operaciones reales
  - Mitigación: actualización transaccional del contador + reconciliación diaria

## Complexity Tracking

No constitutional violations detected.
