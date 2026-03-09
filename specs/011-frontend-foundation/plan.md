# Implementation Plan: Frontend Foundation MVP

**Branch**: `011-frontend-foundation` | **Date**: 2026-03-09 | **Spec**: `specs/011-frontend-foundation/spec.md`
**Input**: Feature specification from `/specs/011-frontend-foundation/spec.md`

## Summary

Construir la base de una experiencia frontend MVP para TRDIA con autenticacion, navegacion privada y flujos core (dashboard, trading, notifications y AI agent) consumiendo contratos backend existentes, con foco en estados UX confiables y sin introducir implementacion de negocio adicional.

## Technical Context

**Language/Version**: TypeScript 5.x (planificado para frontend)  
**Primary Dependencies**: Framework web SPA, router con guardas de sesion, cliente HTTP, libreria de testing de UI (seleccion exacta diferida a `/speckit.tasks`)  
**Storage**: N/A para persistencia de negocio; almacenamiento de sesion minimizado en cliente segun politicas de seguridad del spec  
**Testing**: Estrategia TDD con unit + integration de UI y smoke E2E de historias P1-P3  
**Target Platform**: Web app responsive para navegadores modernos (desktop y mobile web)
**Project Type**: Web application frontend + backend existente  
**Performance Goals**: cumplir SC-001 (login+dashboard < 2 min para 95% usuarios de prueba) y mantener feedback inmediato de estados de carga/error en flujos MVP  
**Constraints**: alcance cerrado a fundacion MVP; sin endpoints nuevos backend; sin apps moviles nativas; sin hardening de produccion en este sprint  
**Scale/Scope**: 5 vistas privadas principales, 1 experiencia de autenticacion, y cobertura de historias P1-P3 para validacion funcional

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec y checklist de requerimientos completados antes de planificar.
- [x] **Principle II (TDD)**: Estrategia de pruebas definida para `/speckit.tasks` (RED -> GREEN -> REFACTOR) en historias P1-P3.
- [x] **Principle III (Security-First)**:
  - [x] no credenciales en codigo/logs
  - [x] validaciones de entrada basicas en frontend y enforcement fuerte en backend
  - [x] no persistir secretos completos en cliente
  - [x] eventos auditables definidos para login/trading/notifications/ai-agent
- [ ] **Technology Stack (Constitution - Immutable V1.0)**: existe desalineacion entre stack frontend constitucional (React Native Expo) y alcance web del spec 011; requiere excepcion o amendment antes de implementar.
- [x] **Principle IV (Modular)**: se mantiene separacion frontend/back-end con contratos claros.
- [x] **Principle V (Validation-Strict)**:
  - [x] backend sigue validando limites de plan y operaciones monetarias
  - [x] frontend no decide reglas de negocio
  - [x] validacion de negocio no se mueve al cliente
- [x] **Principle VI (Observability)**: metricas y eventos frontend definidos en spec y contratos.
- [x] **Principle VII (Progressive Enhancement)**: alcance MVP sin complejidad prematura.

**Gate Result (Pre-Phase 0)**: PASS WITH GOVERNANCE CONDITION (una desviacion documentada con justificacion en Complexity Tracking).

## Project Structure

### Documentation (this feature)

```text
specs/011-frontend-foundation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── frontend-backend-integration.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── services/
│   ├── analytics/
│   └── workers/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── app/
│   ├── pages/
│   ├── features/
│   └── services/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

**Structure Decision**: Estructura de aplicacion web con backend existente y nuevo modulo `frontend/` para fundacion MVP; la implementacion fisica de `frontend/` queda para `/speckit.tasks` y fases de ejecucion.

## Phase Plan

### Phase 0 - Research Decisions

1. Confirmar alcance web MVP y su impacto de gobernanza frente al stack constitucional.
2. Definir estrategia de integracion usando APIs backend existentes (sin endpoints nuevos).
3. Definir estrategia TDD por capas (unit, integration, smoke E2E).
4. Definir contrato transversal de estados UX (`loading/empty/error/success`).

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades de estado UI para sesion, dashboard, trading, notifications y ai-agent.
2. `contracts/frontend-backend-integration.md` con responsabilidades frontend/backend y manejo de respuestas.
3. `quickstart.md` con criterios de readiness para `/speckit.tasks`.
4. Actualizacion de contexto de agente via script oficial de Speckit.

### Phase 2 - Implementation Readiness

Para `/speckit.tasks`:
- desglosar tareas en orden P1 -> P2 -> P3 con enfoque tests-first
- incluir tareas de guardas de sesion, navegacion base y contratos de estados UX
- incluir evidencia por success criteria SC-001..SC-004
- incluir tarea de resolucion de condicion de gobernanza (exception/amendment de stack) antes de iniciar codigo

## Testing Strategy (TDD Gate)

1. Unit tests de estado de sesion, validaciones ligeras de formularios y mapeo de errores.
2. Integration tests de navegacion protegida y flujos por modulo (dashboard/trading/notifications/ai-agent).
3. Smoke E2E de historias P1, P2 y P3 con criterios de aceptacion del spec.
4. Validacion explicita de edge cases: sesion expirada, doble submit, red intermitente y datos vacios.

## Risks & Mitigations

- Riesgo: conflicto de stack constitucional bloquea implementacion.
  - Mitigacion: registrar en tasks una aprobacion obligatoria (exception/amendment) antes de codificar.
- Riesgo: expansion de alcance por cambios backend.
  - Mitigacion: mantener contrato de consumo de APIs existentes, sin endpoints nuevos en sprint 011.
- Riesgo: UX inconsistente entre modulos.
  - Mitigacion: aplicar contrato transversal de estados y mensajes accionables.

## Post-Design Constitution Re-check

- [x] Artefactos `research.md`, `data-model.md`, `quickstart.md` y `contracts/` completados.
- [x] Se mantiene cumplimiento de principios I-VII, con una unica desviacion de stack documentada y gobernada.
- [x] No quedan `NEEDS CLARIFICATION` abiertos para pasar a `/speckit.tasks`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Stack frontend constitucional (React Native) vs alcance web del spec 011 | El spec de feature aprobado acota Sprint 011 a web MVP para validar flujos funcionales con usuarios de prueba | Forzar React Native en este sprint rompe alcance cerrado y retrasa validacion MVP; ignorar conflicto viola gobernanza. Se requiere exception/amendment explicito antes de implementar |
