# Implementation Plan: TRDIA - Persistence and Hardening Baseline

**Branch**: `009-persistence-hardening` | **Date**: 2026-03-09 | **Spec**: `specs/009-persistence-hardening/spec.md`
**Input**: Feature specification from `/specs/009-persistence-hardening/spec.md`

## Summary

Migrar persistencia in-memory a PostgreSQL para auth, trading execution, notifications y AI agent config, manteniendo contratos API vigentes y agregando baseline de hardening operativo (migraciones versionadas, manejo de errores controlado, auditoria y smoke tests reproducibles) dentro del alcance cerrado de Sprint 009.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, Pydantic v2, pytest, httpx, SQLAlchemy 2.x + driver PostgreSQL (alineado a stack constitucional)  
**Storage**: PostgreSQL 15+ como storage durable para dominios criticos (sin fallback in-memory en flujo de produccion)  
**Testing**: pytest (contract, integration, unit), smoke tests reproducibles sobre DB real  
**Target Platform**: Backend FastAPI en contenedor Docker para entorno local/staging, conectando a PostgreSQL host o contenedor  
**Project Type**: Web-service backend  
**Performance Goals**: cumplir SC-002 del spec: >=95% CRUD critico <300 ms en entorno local de pruebas  
**Constraints**: compatibilidad 100% de contratos existentes, idempotencia preservada, auditoria sin exponer secretos, alcance cerrado Sprint 009  
**Scale/Scope**: migracion de persistencia para 4 dominios criticos ya activos (`auth`, `trading_execution`, `notifications`, `ai_agent`) y hardening minimo pre-produccion

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: `specs/009-persistence-hardening/spec.md` completo y usado como source of truth
- [x] **Principle II (TDD)**: estrategia de pruebas definida (contract/integration/unit + smoke), para implementar RED -> GREEN -> REFACTOR en `tasks.md`
- [x] **Principle III (Security-First)**:
  - [x] no credenciales en codigo/logs
  - [x] reglas de validacion de entrada y consultas parametrizadas definidas
  - [x] estrategia de secretos/credenciales mantenida por variables de entorno y hash/cifrado donde aplica
  - [x] eventos de auditoria criticos definidos para DB y operaciones
- [x] **Principle IV (Modular)**: cambios acotados a `api/`, `services/`, `schemas/`, `workers/` por dominio, sin romper modularidad
- [x] **Principle V (Validation-Strict)**:
  - [x] validaciones backend y enforcement de limites de plan se mantienen
  - [x] idempotencia de ejecuciones/eventos explicitamente preservada
  - [x] frontend sigue sin decidir logica critica
- [x] **Principle VI (Observability)**: metricas, alertas y logging de persistencia/hardening definidos en spec y plan
- [x] **Principle VII (Progressive Enhancement)**: baseline de persistencia/hardening sin expansion a HA/failover/performance avanzada

## Project Structure

### Documentation (this feature)

```text
specs/009-persistence-hardening/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── persistence-hardening.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── auth/
│   │   ├── trading/
│   │   ├── notifications/
│   │   └── ai_agent/
│   ├── schemas/
│   │   ├── auth/
│   │   ├── trading/
│   │   ├── notifications/
│   │   └── ai_agent/
│   ├── services/
│   │   ├── auth/
│   │   ├── execution/
│   │   ├── notifications/
│   │   ├── ai_agent/
│   │   ├── audit/
│   │   └── validation/
│   └── workers/
│       └── execution_reconciliation_worker.py
└── tests/
    ├── contract/
    │   ├── auth/
    │   ├── trading_execution/
    │   ├── notifications/
    │   └── ai_agent/
    ├── integration/
    └── unit/
```

**Structure Decision**: feature backend-only, con migracion por capas (api -> services -> repositorios persistentes) y cobertura de regresion por suites existentes de `contract`, `integration` y `unit` sin agregar nuevos modulos fuera de Sprint 009.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia de migracion de stores in-memory a repositorios PostgreSQL con compatibilidad de contratos.
2. Versionado de migraciones y procedimiento de arranque seguro.
3. Patrones para idempotencia transaccional en ejecuciones y eventos.
4. Manejo de errores controlado + auditoria sin exponer datos sensibles.
5. Configuracion host/container (`host.docker.internal`) para entornos reproducibles.

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades, relaciones, validaciones y transiciones de estado.
2. `contracts/persistence-hardening.openapi.yaml` con contratos de continuidad y errores controlados.
3. `quickstart.md` con escenarios de reinicio, conectividad host/container y fallos transitorios.
4. Actualizacion de contexto de agente por script oficial de Speckit.

### Phase 2 - Implementation Readiness

Para `/speckit.tasks`:
- desglose por historias P1/P2/P3 del spec (en ese orden), sin expansion de alcance
- tareas tests-first por capa (`contract` -> `integration` -> `unit`)
- secuencia de ejecucion: migraciones y bootstrap DB -> repositorios persistentes -> compatibilidad API -> observabilidad/auditoria -> smoke/regresion

## Testing Strategy (TDD Gate)

1. Contract tests para garantizar que endpoints existentes mantienen formato y semantica.
2. Integration tests con PostgreSQL real para persistencia tras reinicio e idempotencia.
3. Unit tests para mapeo repositorio-modelo, validadores de entrada y manejo de errores DB.
4. Smoke suite reproducible que verifique conectividad, migraciones y CRUD basico critico.
5. Coverage objetivo segun constitucion: >=80% global y >=90% en componentes criticos tocados.

## Risks & Mitigations

- Riesgo: divergencia de comportamiento entre store in-memory y persistente.
  - Mitigacion: suite de regresion contractual y pruebas de equivalencia funcional por dominio.
- Riesgo: errores transitorios DB afectando continuidad operativa.
  - Mitigacion: errores controlados estandarizados, auditoria de fallos y retries acotados cuando corresponda.
- Riesgo: drift de configuracion entre host DB y contenedor.
  - Mitigacion: quickstart con variables de entorno canonicas y smoke test obligatorio en ambos modos.

## Post-Design Constitution Re-check

- [x] Phase 1 artifacts (`research.md`, `data-model.md`, `quickstart.md`, `contracts/`) mantienen cumplimiento de principios I-VII.
- [x] No se detectan violaciones constitucionales ni necesidad de excepciones.

## Complexity Tracking

No constitutional violations detected.
