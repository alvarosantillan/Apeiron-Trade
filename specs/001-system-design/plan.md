# Implementation Plan: TRDIA - System Design Foundation

**Branch**: `001-system-design` | **Date**: 2026-03-07 | **Spec**: `specs/001-system-design/spec.md`
**Input**: Architecture specification from `/specs/001-system-design/spec.md`

## Summary

Establecer la base arquitectónica del producto TRDIA (mobile + backend + workers + observabilidad + seguridad + pagos + trading + IA) con contratos, dominios y reglas transversales que habiliten implementación incremental y segura de todas las features funcionales.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript (React Native app)  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, Celery, Redis, PostgreSQL, React Native Expo, MercadoPago SDK/API, integración Binance Spot  
**Storage**: PostgreSQL externa + Redis para cola/cache  
**Testing**: pytest + contract/integration/unit + estrategia TDD para backend y flujos críticos  
**Target Platform**: API Linux container, workers Linux container, app móvil iOS/Android  
**Project Type**: Mobile + API con servicios asíncronos  
**Performance Goals**: ejecución operativa p95 <= 5s, actualización de plan p95 <= 15s, dashboard p95 <= 2s  
**Constraints**: backend como source of truth para límites/validaciones; no secretos en logs; Spot-only v1  
**Scale/Scope**: hasta 500 usuarios concurrentes activos en MVP

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: arquitectura definida por especificación antes de implementación
- [x] **Principle II (TDD)**: plan de pruebas transversal definido como criterio de entrada
- [x] **Principle III (Security-First)**: cifrado de credenciales, validación backend y auditoría transversal definidos
- [x] **Principle IV (Modular)**: módulos `api/trading/agents/strategies/analytics/workers` claramente delimitados
- [x] **Principle V (Validation-Strict)**: límites de plan y controles de riesgo solo en backend
- [x] **Principle VI (Observability)**: métricas, logs y alertas como capacidad base del sistema
- [x] **Principle VII (Progressive Enhancement)**: alcance v1 acotado (Spot, proveedores definidos, sin complejidad prematura)

## Project Structure

### Documentation (this feature)

```text
specs/001-system-design/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── platform-core.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── trading/
│   ├── agents/
│   ├── strategies/
│   ├── analytics/
│   ├── payments/
│   ├── models/
│   ├── schemas/
│   └── workers/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
└── src/
    ├── screens/
    ├── features/
    ├── services/
    └── state/

infra/
├── docker/
└── ci/
```

**Structure Decision**: arquitectura modular con backend dominante en reglas de negocio y frontend orientado a experiencia; workers asíncronos para procesos críticos no bloqueantes.

## Phase Plan

### Phase 0 - Research Decisions

1. Delimitación de bounded contexts entre auth, subscriptions, trading, ai-agent y notifications
2. Estrategia de consistencia transaccional y reconciliación para operaciones monetarias
3. Estrategia de secretos/cifrado/rotación de claves
4. Estrategia de observabilidad y alerting de punta a punta

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades núcleo y relaciones cross-feature
2. `contracts/platform-core.openapi.yaml` para endpoints transversales de estado/capacidades/configuración inicial
3. `quickstart.md` para validación de arquitectura base en entorno local

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas base de arquitectura y bootstrap
- tareas de seguridad y observabilidad first-class
- preparación del path de implementación por features en orden de dependencias

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints base de plataforma
2. Integration tests cross-domain (auth + plan + trading validation)
3. Unit tests para validadores de reglas transversales
4. Coverage gate:
   - módulos core backend >= 85%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: acoplamiento excesivo entre módulos
  - Mitigación: interfaces explícitas y contratos de dominio por módulo
- Riesgo: drift de reglas entre frontend y backend
  - Mitigación: backend source of truth + contratos API estrictos
- Riesgo: deuda de observabilidad temprana
  - Mitigación: métricas/logs/alertas obligatorios desde primer sprint

## Complexity Tracking

No constitutional violations detected.
