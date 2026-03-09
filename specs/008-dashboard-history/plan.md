# Implementation Plan: TRDIA - Dashboard and Trade History

**Branch**: `008-dashboard-history` | **Date**: 2026-03-06 | **Spec**: `specs/008-dashboard-history/spec.md`
**Input**: Feature specification from `/specs/008-dashboard-history/spec.md`

## Summary

Implementar el dashboard operativo y el historial de operaciones con filtros, detalle de ejecución y KPIs recientes, asegurando consultas autenticadas, trazabilidad completa y rendimiento consistente para uso diario en móvil.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, Redis (cache opcional de snapshots), Celery (refresh de agregados)  
**Storage**: PostgreSQL externa (lectura de operaciones, suscripciones y métricas agregadas)  
**Testing**: pytest, pytest-asyncio, httpx, fixtures de dataset histórico, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: dashboard p95 < 2s, historial paginado p95 < 3s  
**Constraints**: control de acceso por usuario estricto, paginación obligatoria, consistencia real/simulación  
**Scale/Scope**: v1 con dashboard resumen, listado filtrable, detalle y KPIs 7d/30d

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: plan de pruebas contract/integration/unit definido
- [x] **Principle III (Security-First)**:
  - [x] endpoints protegidos por autenticación/autorización
  - [x] validación de filtros e IDs en backend
  - [x] logs sin datos sensibles innecesarios
  - [x] auditoría de acceso a detalle definida
- [x] **Principle IV (Modular)**: Encaja en `analytics/`, `trading/`, `api/`
- [x] **Principle V (Validation-Strict)**:
  - [x] backend calcula estado de plan/límites visibles
  - [x] frontend solo consume datos calculados
  - [x] no hay lógica crítica de negocio en cliente
- [x] **Principle VI (Observability)**: métricas y alertas de latencia/error definidas
- [x] **Principle VII (Progressive Enhancement)**: alcance MVP sin reporting avanzado extra

## Project Structure

### Documentation (this feature)

```text
specs/008-dashboard-history/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── dashboard-history.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── analytics/
│   ├── services/
│   │   ├── dashboard/
│   │   ├── history/
│   │   └── kpi/
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
        └── dashboard/
```

**Structure Decision**: backend unifica composición del snapshot, queries históricas filtradas y agregados KPI; frontend prioriza visualización y UX de exploración.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia de agregado de KPIs (on-demand vs precomputado)
2. Diseño de filtros/paginación para historial de alto volumen
3. Política de fallback cuando balance/snapshot no está disponible
4. Definición de trazabilidad mínima en detalle de operación

### Phase 1 - Design Artifacts

1. `data-model.md` para snapshot, historial y KPIs
2. `contracts/dashboard-history.openapi.yaml` para dashboard/list/history/detail/kpis
3. `quickstart.md` para validar casos de usuario nuevo, filtros y detalle

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por historias P1-P4
- tests-first obligatorios
- secuencia: dashboard snapshot -> historial filtrado -> detalle -> KPIs -> observabilidad

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de dashboard, historial, detalle y KPIs
2. Integration tests con datasets: usuario nuevo, alto volumen, filtros combinados, paginación profunda
3. Unit tests para validadores de filtros, cálculo de KPIs y mapeo de trazabilidad
4. Coverage gate:
   - módulo dashboard/history >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: latencia alta en historial con filtros complejos
  - Mitigación: índices adecuados, paginación estricta y límites de query
- Riesgo: inconsistencia entre snapshot y detalle
  - Mitigación: timestamp de última actualización y estrategia de refresco definida
- Riesgo: exposición de datos de otro usuario
  - Mitigación: scoping obligatorio por `user_id` en todas las consultas

## Complexity Tracking

No constitutional violations detected.
