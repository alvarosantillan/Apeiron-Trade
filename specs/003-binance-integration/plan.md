# Implementation Plan: TRDIA - Binance Integration

**Branch**: `003-binance-integration` | **Date**: 2026-03-06 | **Spec**: `specs/003-binance-integration/spec.md`
**Input**: Feature specification from `/specs/003-binance-integration/spec.md`

## Summary

Implementar la capa de integración con Binance Spot para credenciales seguras por usuario, validación operativa en backend, ejecución real/simulada y trazabilidad completa de operaciones. Esta feature debe garantizar reglas por plan (Free/Plus/Premium), idempotencia y notificación por ejecución.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, ccxt o SDK Binance oficial, Celery, Redis  
**Storage**: PostgreSQL externa (`binance_credentials`, `trades`, `operation_counters`, `audit_logs`)  
**Testing**: pytest, pytest-asyncio, httpx, respx/mocks, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: validación credenciales p95 < 3s, ejecución p95 < 5s  
**Constraints**: cifrado obligatorio de credenciales, backend enforcement de límites, soporte simulación ilimitada  
**Scale/Scope**: MVP con Binance Spot únicamente

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: Plan de tests contract/integration/unit definido
- [x] **Principle III (Security-First)**:
  - [x] Credenciales nunca en texto plano
  - [x] Validación de entradas y payloads definida
  - [x] Estrategia de cifrado de API keys documentada
  - [x] Requisitos de auditoría definidos
- [x] **Principle IV (Modular)**: Encaja en `trading/`, `api/`, `workers/`
- [x] **Principle V (Validation-Strict)**:
  - [x] Validación backend de límites y precondiciones definida
  - [x] Enforcements por plan documentados
  - [x] Frontend no decide autorizaciones de negocio
- [x] **Principle VI (Observability)**: Métricas, alertas y logging definidos
- [x] **Principle VII (Progressive Enhancement)**: Scope limitado a Spot v1.0

## Project Structure

### Documentation (this feature)

```text
specs/003-binance-integration/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── trading.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── trading/
│   ├── services/
│   │   ├── binance/
│   │   └── execution/
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

**Structure Decision**: Se implementa como módulo backend con integración consumida por frontend, manteniendo lógica crítica de validación en API/servicios.

## Phase Plan

### Phase 0 - Research Decisions

1. Librería de exchange (ccxt vs SDK oficial) y estrategia de fallback
2. Política de idempotencia y deduplicación por `request_id`
3. Política de reintentos para errores transitorios del exchange
4. Estrategia de simulación consistente con ejecución real

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades de credenciales, solicitudes, ejecuciones y contadores semanales
2. `contracts/trading.openapi.yaml` con endpoints de configuración, validación y ejecución
3. `quickstart.md` para validación manual en real/simulación

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por US1-US4
- tests-first obligatorios
- secuencia: credenciales -> validación -> ejecución -> simulación -> notificación -> métricas

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de credenciales y ejecución
2. Integration tests con mocks Binance/Testnet para escenarios de éxito/fallo/límite
3. Unit tests para validador de reglas por plan, contador semanal e idempotencia
4. Coverage gate:
   - módulo trading/binance >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: doble ejecución por reintentos/red
  - Mitigación: `request_id` idempotente + bloqueo transaccional
- Riesgo: desincronización con estado real de Binance
  - Mitigación: reconciliación por `exchange_order_id` y logs de auditoría
- Riesgo: fuga de credenciales
  - Mitigación: cifrado fuerte + mascaramiento + controles de logging

## Complexity Tracking

No constitutional violations detected.
