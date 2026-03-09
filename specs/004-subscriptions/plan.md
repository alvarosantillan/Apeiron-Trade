# Implementation Plan: TRDIA - Subscriptions and Payments

**Branch**: `004-subscriptions` | **Date**: 2026-03-06 | **Spec**: `specs/004-subscriptions/spec.md`
**Input**: Feature specification from `/specs/004-subscriptions/spec.md`

## Summary

Implementar gestión de suscripciones Free/Plus/Premium y cobro recurrente con MercadoPago, incluyendo creación automática e idempotente de planes al iniciar backend, procesamiento seguro de webhooks, y validación backend del estado de suscripción antes de habilitar operaciones.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, MercadoPago SDK/API HTTP, Celery, Redis  
**Storage**: PostgreSQL externa (`plan_catalog`, `subscriptions`, `payment_records`, `webhook_events`)  
**Testing**: pytest, pytest-asyncio, httpx, webhook signature mocks, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: actualización de plan p95 < 15s tras pago aprobado; procesamiento webhook p95 < 5s  
**Constraints**: webhook idempotente, firma obligatoria, backend source of truth para plan activo  
**Scale/Scope**: v1 con MercadoPago único proveedor

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: Plan de tests contract/integration/unit definido
- [x] **Principle III (Security-First)**:
  - [x] Secretos de pago no se exponen en código/logs
  - [x] Validación estricta de payloads y firmas
  - [x] Estrategia de manejo seguro de credenciales documentada
  - [x] Auditoría de eventos de pago definida
- [x] **Principle IV (Modular)**: Encaja en `payments/`, `subscriptions/`, `workers/`
- [x] **Principle V (Validation-Strict)**:
  - [x] Validación backend del plan antes de operar definida
  - [x] Límites por plan documentados
  - [x] Sin enforcement en frontend
- [x] **Principle VI (Observability)**: Métricas/alertas/logging definidos
- [x] **Principle VII (Progressive Enhancement)**: MercadoPago-only en v1

## Project Structure

### Documentation (this feature)

```text
specs/004-subscriptions/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── subscriptions.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── subscriptions/
│   ├── services/
│   │   ├── subscriptions/
│   │   └── payments/
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
        └── subscriptions/
```

**Structure Decision**: Módulo backend especializado en suscripciones/pagos; frontend solo inicia checkout y consulta estado.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia de creación automática de planes MP (idempotente por código de plan)
2. Estrategia de validación de firma y deduplicación de webhooks
3. Reglas de upgrade/downgrade/cancelación por ciclo de facturación
4. Integración de estado de suscripción con módulo de ejecución de trading

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades de catálogo, suscripciones, pagos y eventos webhook
2. `contracts/subscriptions.openapi.yaml` con endpoints de checkout, estado y webhooks
3. `quickstart.md` para validación de flujos en sandbox

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por historias P1-P4
- tests-first obligatorios
- secuencia: catálogo planes -> checkout -> webhooks -> estado plan -> auditoría -> notificaciones

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de checkout, status y webhook
2. Integration tests con sandbox/mock MercadoPago (aprobado, rechazado, duplicado, firma inválida)
3. Unit tests para mapeo de estados, idempotencia y políticas de transición
4. Coverage gate:
   - módulo subscriptions/payments >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: webhook duplicado cambia estado múltiples veces
  - Mitigación: persistir `provider_event_id` y rechazar re-procesamiento
- Riesgo: pago aprobado no refleja upgrade oportuno
  - Mitigación: procesamiento asíncrono confiable + reconciliación programada
- Riesgo: firma webhook inválida aceptada
  - Mitigación: validación criptográfica obligatoria y rechazo temprano

## Complexity Tracking

No constitutional violations detected.
