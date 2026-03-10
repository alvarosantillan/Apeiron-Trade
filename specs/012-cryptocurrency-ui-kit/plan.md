# Implementation Plan: Cryptocurrency UI Kit Integration (Iteracion 1)

**Branch**: `012-cryptocurrency-ui-kit` | **Date**: 2026-03-10 | **Spec**: `specs/012-cryptocurrency-ui-kit/spec.md`
**Input**: Feature specification from `/specs/012-cryptocurrency-ui-kit/spec.md`

## Summary

Integrar Cryptocurrency App UI Kit en el frontend web existente para el layout autenticado y las paginas Dashboard y Trading, preservando contratos backend, flujos de autenticacion y pruebas vigentes. La estrategia tecnica se centra en reemplazo de capa visual y composicion de componentes, sin cambios de endpoints ni logica de negocio.

## Technical Context

**Language/Version**: TypeScript 5.6 + React 18 (frontend), Python 3.11 (backend sin cambios)  
**Primary Dependencies**: React Router 6, Vite 5, Vitest 2, Playwright 1.50; UI Kit criptocurrency integrado en capa de UI  
**Storage**: N/A para esta feature (sin cambios de persistencia ni contratos de datos)  
**Testing**: Vitest (unit/integration), Playwright (e2e scaffold), validacion de regresion sobre tests existentes  
**Target Platform**: Web responsive (desktop y mobile) en frontend TRDIA
**Project Type**: Web application (frontend + backend existente)  
**Performance Goals**: mantener tiempos de carga percibidos en Dashboard/Trading y preservar feedback visible de submit en Trading segun SC de la spec  
**Constraints**: alcance cerrado a layout autenticado + Dashboard + Trading; sin cambios backend; preservar auth/routing y pruebas existentes; Notifications y AI Agent fuera del rediseno completo  
**Scale/Scope**: 1 layout privado + 2 paginas principales + estados UX (`loading/empty/error/success`) en iteracion visual

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa en `specs/012-cryptocurrency-ui-kit/spec.md` antes de tareas de implementacion.
- [x] **Principle II (TDD)**: Estrategia de pruebas de regresion y pruebas nuevas definida para `/speckit.tasks` con enfoque tests-first por historia.
- [x] **Principle III (Security-First)**:
  - [x] Sin exposicion de credenciales/tokens en cliente o logs
  - [x] Validacion de entrada permanece en backend
  - [x] No se cambia estrategia de cifrado/secretos
  - [x] Eventos auditables de auth/dashboard/trading identificados
- [x] **Principle IV (Modular)**: Integracion acotada a modulos frontend existentes (`app/layouts`, `pages`, `features`).
- [x] **Principle V (Validation-Strict)**:
  - [x] Trading mantiene validacion de plan/limites en backend
  - [x] No se introduce enforcement de negocio en frontend
  - [x] Frontend solo refleja estados devueltos por API
- [x] **Principle VI (Observability)**: metricas/eventos UI definidos en spec y en contrato de integracion.
- [x] **Principle VII (Progressive Enhancement)**: iteracion visual incremental, sin expansion a features fuera de alcance.

**Gate Result (Pre-Phase 0)**: PASS WITH GOVERNANCE CONDITION (revalidacion de excepcion de stack web para Sprint 012).

## Project Structure

### Documentation (this feature)

```text
specs/012-cryptocurrency-ui-kit/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── frontend-ui-kit-integration.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── services/
│   └── workers/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── app/
│   │   └── layouts/
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── trading/
│   ├── pages/
│   └── services/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

**Structure Decision**: Se mantiene arquitectura web existente (frontend + backend) y la feature 012 modifica solo capas de presentacion del frontend para layout privado, Dashboard y Trading.

## Phase Plan

### Phase 0 - Research Decisions

1. Definir estrategia de adopcion del UI Kit sin romper guardas de sesion ni rutas privadas.
2. Definir patron de mapeo de componentes del UI Kit para Dashboard y Trading manteniendo estados UX actuales.
3. Confirmar estrategia de regresion para evitar impactos en tests existentes y flujos de auth.
4. Delimitar criterios responsive y accesibilidad minima para esta iteracion.

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades de estado de presentacion para layout, dashboard y trading.
2. `contracts/frontend-ui-kit-integration.md` con contrato de responsabilidades UI/frontend-backend.
3. `quickstart.md` con flujo de readiness para `/speckit.tasks` y validaciones de alcance cerrado.
4. Actualizacion de contexto de agente con script oficial Speckit.

### Phase 2 - Implementation Readiness

Para `/speckit.tasks`:
- Desglosar tareas por historias P1 -> P2 -> P3 con orden tests-first.
- Incluir tareas de regresion explicita en auth y private routing.
- Incluir tareas de validacion responsive/accesibilidad para layout, Dashboard y Trading.
- Mantener restriccion de no tocar backend/endpoints.

## Testing Strategy (TDD Gate)

1. Unit tests de componentes de layout y render de estados visuales en Dashboard/Trading.
2. Integration tests para login -> acceso privado -> dashboard/trading y manejo de sesion expirada.
3. Regression tests de flujo de trading para submit, respuesta exitosa y error sin bloqueo de UI.
4. Smoke e2e de navegacion privada y carga de vistas redisenadas.

## Risks & Mitigations

- Riesgo: divergencia visual al integrar UI Kit con estructura actual de componentes.
  - Mitigacion: contrato de mapeo de componentes y tokens visuales definidos en `research.md`.
- Riesgo: regresion de rutas privadas o redireccion post-login por cambios de layout.
  - Mitigacion: mantener `PrivateLayout` y guardas existentes como inmutables funcionales; reforzar tests de navegacion.
- Riesgo: deuda de responsive/accesibilidad en breakpoints pequenos.
  - Mitigacion: checklist de validacion UX en `quickstart.md` y tareas dedicadas en `/speckit.tasks`.
- Riesgo: conflicto de gobernanza por stack constitucional React Native vs alcance web.
  - Mitigacion: registrar pendiente de revalidacion para Sprint 012 en `Complexity Tracking` segun guardrail vigente.

## Post-Design Constitution Re-check

- [x] `research.md`, `data-model.md`, `quickstart.md` y `contracts/` generados para la feature 012.
- [x] No hay `NEEDS CLARIFICATION` abiertos tras Phase 0.
- [x] Se preserva principio de backend-as-authority para trading y auth.
- [x] Se mantiene alcance incremental sin expansion fuera de Dashboard/Trading/layout privado.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Frontend stack constitucional (React Native) vs alcance web de feature 012 | La feature 012 extiende la base web ya aprobada en sprint previo para validar UI Kit en flujos autenticados existentes | Migrar a React Native en este sprint rompe alcance cerrado y no cumple objetivo de iteracion visual sobre frontend web actual |
