# Implementation Plan: Runtime Deprecation Cleanup Baseline

**Branch**: `010-runtime-deprecation-cleanup` | **Date**: 2026-03-09 | **Spec**: `specs/010-runtime-deprecation-cleanup/spec.md`
**Input**: Feature specification from `/specs/010-runtime-deprecation-cleanup/spec.md`

## Summary

Eliminar deprecaciones de runtime del ciclo de vida de FastAPI, reducir ruido de warnings recurrentes de dependencias con acciones explicitas y documentar una politica de baseline para evitar regresiones, sin introducir cambios funcionales de negocio ni romper contratos existentes.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, Pydantic v2, pytest, httpx, SQLAlchemy 2.x (sin cambios de stack)  
**Storage**: PostgreSQL 15+ sin cambios de modelo persistente para esta feature  
**Testing**: pytest (`tests/contract`, `tests/integration`, `tests/unit`) con ejecucion en contenedor  
**Target Platform**: Backend FastAPI en contenedor Docker (`Apeiron-Trade`)  
**Project Type**: Web-service backend  
**Performance Goals**: mantener throughput/latencia actuales y lograr `runtime.lifecycle.deprecation.total = 0` en arranque y suite  
**Constraints**: no cambios de contrato API ni de logica de negocio; no supresion global de warnings; alcance cerrado Sprint 010  
**Scale/Scope**: limpieza de baseline runtime en inicializacion y superficie de warnings del backend existente

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: `specs/010-runtime-deprecation-cleanup/spec.md` y checklist de requerimientos completos antes de planificar
- [x] **Principle II (TDD)**: estrategia de pruebas definida para `/speckit.tasks` (RED -> GREEN -> REFACTOR) con foco en warnings/lifecycle
- [x] **Principle III (Security-First)**:
  - [x] no credenciales en codigo/logs
  - [x] no se alteran reglas de validacion de entrada de negocio
  - [x] estrategia de secretos/cifrado sin cambios
  - [x] requisitos de auditoria de eventos startup/shutdown identificados
- [x] **Principle IV (Modular)**: cambios acotados a `backend/src/main.py`, middleware/runtime wiring y documentacion de metodologia
- [x] **Principle V (Validation-Strict)**:
  - [x] no aplica validacion de limites de plan (feature no trading/subscription)
  - [x] no se delega logica de negocio al frontend
  - [x] sin impacto en enforcement existente
- [x] **Principle VI (Observability)**: metricas y alertas de warnings runtime definidas en spec y plan
- [x] **Principle VII (Progressive Enhancement)**: baseline incremental (cleanup) sin complejidad prematura ni refactor amplio

## Project Structure

### Documentation (this feature)

```text
specs/010-runtime-deprecation-cleanup/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── runtime-deprecation-continuity.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py
│   ├── api/
│   ├── services/
│   └── middleware/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

docs/
└── methodology/
```

**Structure Decision**: Feature backend-only y de politica operacional; se priorizan ajustes en inicializacion runtime y suites existentes de pruebas, sin crear nuevos modulos de dominio.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia de migracion de eventos de startup al patron lifespan recomendado por FastAPI.
2. Politica de tratamiento de warnings recurrentes (remediar, fijar version o excepcion documentada).
3. Definicion de baseline reproducible para comparar ruido de warnings en contenedor.
4. Criterio de no-regresion funcional durante cleanup runtime.

### Phase 1 - Design Artifacts

1. `data-model.md` para entidades conceptuales `RuntimeWarningRecord` y `LifecycleBootstrapPolicy`.
2. `contracts/runtime-deprecation-continuity.md` con contrato de continuidad (sin cambios de API de negocio).
3. `quickstart.md` con pasos de validacion de baseline runtime y gates de warnings.
4. Actualizacion de contexto de agente via script Speckit oficial.

### Phase 2 - Implementation Readiness

Para `/speckit.tasks`:
- priorizar historias P1 -> P2 -> P3 del spec
- desglosar tareas tests-first para lifecycle, warning surface y politica documental
- incluir gates de evidencia para SC-001..SC-004 antes de marcar done

## Testing Strategy (TDD Gate)

1. Contract tests para confirmar continuidad de endpoints existentes sin cambios de comportamiento.
2. Integration tests de arranque/apagado para validar lifecycle recomendado sin warning deprecado.
3. Unit tests para utilidades/filtros de runtime warning policy (si aplica en implementacion).
4. Ejecucion en contenedor para comparar baseline de warnings pre/post cleanup.
5. Coverage objetivo constitucional: >=80% global y >=90% en componentes criticos impactados.

## Risks & Mitigations

- Riesgo: migracion de lifecycle rompe inicializacion de dependencias internas.
  - Mitigacion: pruebas de smoke en startup/shutdown y validacion de readiness antes de merge.
- Riesgo: ocultar warnings reales por filtrado excesivo.
  - Mitigacion: prohibir supresion global; cada warning tratado con decision explicita y evidencia.
- Riesgo: diferencia de warnings entre local y contenedor.
  - Mitigacion: baseline y validacion obligatoria en entorno contenedor oficial.

## Post-Design Constitution Re-check

- [x] `research.md`, `data-model.md`, `quickstart.md` y `contracts/` mantienen cumplimiento de principios I-VII.
- [x] No se identifican violaciones constitucionales ni excepciones necesarias.

## Complexity Tracking

No constitutional violations detected.
