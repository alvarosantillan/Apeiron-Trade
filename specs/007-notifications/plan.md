# Implementation Plan: TRDIA - Notifications and Alerts

**Branch**: `007-notifications` | **Date**: 2026-03-06 | **Spec**: `specs/007-notifications/spec.md`
**Input**: Feature specification from `/specs/007-notifications/spec.md`

## Summary

Implementar un sistema de notificaciones push para eventos críticos de trading y suscripción, con preferencias configurables por usuario, soporte multi-dispositivo, deduplicación por evento e historial auditable de entregas con política de reintentos.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, Celery, Redis, proveedor push (FCM/APNs abstraction)  
**Storage**: PostgreSQL externa (`push_device_tokens`, `notification_preferences`, `notification_events`, `notification_deliveries`)  
**Testing**: pytest, pytest-asyncio, httpx, mocks de proveedor push, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: encolado crítico p95 < 2s; entrega p95 < 10s a un dispositivo activo  
**Constraints**: no exponer tokens push en logs, deduplicación estricta, prioridad de eventos críticos  
**Scale/Scope**: v1 con categorías de notificación y preferencias por usuario

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: estrategia de pruebas contract/integration/unit definida
- [x] **Principle III (Security-First)**:
  - [x] tokens push tratados como datos sensibles
  - [x] validación de payload/categoría/prioridad
  - [x] exclusión de secretos en logs
  - [x] trazabilidad de cambios de preferencias y entregas
- [x] **Principle IV (Modular)**: Encaja en `notifications/`, `api/`, `workers/`
- [x] **Principle V (Validation-Strict)**:
  - [x] validación backend de elegibilidad de envío por preferencias
  - [x] eventos críticos se fuerzan según política definida
  - [x] frontend no controla deduplicación ni reintentos
- [x] **Principle VI (Observability)**: métricas, alertas y logging estructurado definidos
- [x] **Principle VII (Progressive Enhancement)**: alcance acotado a push + historial básico

## Project Structure

### Documentation (this feature)

```text
specs/007-notifications/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── notifications.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── notifications/
│   ├── services/
│   │   └── notifications/
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
        └── notifications/
```

**Structure Decision**: backend centraliza encolado, deduplicación, política de prioridad y reintentos; frontend gestiona tokens, preferencias y visualización de historial.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia proveedor push y abstracción por plataforma
2. Política de deduplicación por `event_id`/usuario/dispositivo
3. Política de reintentos y manejo de tokens inválidos
4. Priorización de eventos críticos sobre informativos en colas

### Phase 1 - Design Artifacts

1. `data-model.md` con tokens, preferencias, eventos y entregas
2. `contracts/notifications.openapi.yaml` para registro de token, preferencias e historial
3. `quickstart.md` para validar envíos críticos, deduplicación y reintentos

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por historias P1-P4
- tests-first obligatorios
- secuencia: tokens -> preferencias -> encolado/deduplicación -> envío/reintentos -> historial

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de tokens, preferencias e historial
2. Integration tests: envío exitoso/fallido, token inválido, evento duplicado, ráfagas
3. Unit tests para política de prioridad, deduplicación, reintentos y filtrado por preferencias
4. Coverage gate:
   - módulo notifications >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: duplicados por reintentos o eventos repetidos
  - Mitigación: llave idempotente y constraints por evento/usuario/dispositivo
- Riesgo: caída temporal del proveedor push
  - Mitigación: cola persistente, backoff exponencial y estado final auditable
- Riesgo: ruido excesivo para usuario
  - Mitigación: preferencias granulares y priorización de críticos

## Complexity Tracking

No constitutional violations detected.
