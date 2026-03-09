# Quickstart: Frontend Foundation MVP

## Objective

Validar readiness de Sprint 011 para construir la fundacion frontend MVP (autenticacion, navegacion y flujos core) sin implementar codigo de feature en esta etapa.

## Prerequisites

- Spec y checklist de requerimientos aprobados:
  - `specs/011-frontend-foundation/spec.md`
  - `specs/011-frontend-foundation/checklists/requirements.md`
- Plan, research, data model y contracts de Sprint 011 completados.
- Backend de features `002` a `010` disponible en entorno de desarrollo.

## Readiness Flow

1. Confirmar historias priorizadas P1, P2, P3 y criterios SC-001..SC-004.
2. Verificar que el alcance se mantiene en frontend foundation MVP (sin hardening de produccion ni apps moviles).
3. Confirmar contrato de integracion frontend-backend sin endpoints nuevos en Sprint 011.
4. Validar estrategia TDD para `/speckit.tasks` con pruebas por historia y por estados UI.
5. Confirmar tratamiento de conflicto de stack (web MVP vs constitucion frontend React Native) con decision de gobernanza explicita antes de implementar.

## Scenario 1: P1 Access and Navigation Readiness

1. Revisar contrato de sesion y guardas privadas.
2. Validar definicion de navegacion base: Dashboard, Trading, Notifications, AI Agent.

Expected:
- El plan cubre FR-001, FR-002 y FR-003 sin ambiguedad.
- Existe definicion de redireccion y expiracion de sesion.

## Scenario 2: P2 Core Flow Readiness

1. Revisar entidades de estado para trading, historial, notifications y AI config.
2. Verificar que backend sigue siendo autoridad para validaciones de negocio.

Expected:
- El plan cubre FR-004..FR-008 con dependencias existentes.
- No hay logica de plan limits movida al frontend.

## Scenario 3: P3 UX Reliability Readiness

1. Verificar contrato transversal de estados `loading/empty/error/success`.
2. Revisar lineamientos de mensajes accionables y manejo de errores de red/sesion.

Expected:
- El plan cubre FR-009 y FR-010.
- SC-004 queda mapeado a comportamiento verificable.

## Scenario 4: Constitution and Scope Gate

1. Re-evaluar principios constitucionales para Sprint 011.
2. Confirmar que cualquier desviacion esta documentada en `plan.md` y condicionada a aprobacion.

Expected:
- No hay violaciones silenciosas.
- Alcance permanece cerrado al MVP frontend foundation.

## Governance Exception Record (T006-T007)

- Exception document: `docs/methodology/constitution-exceptions.md`
- Exception type: temporal (stack frontend para Sprint 011)
- Approval status: approved
- Approved by: Project Owner
- Approval date: 2026-03-09
- Implementation gate: habilitado para iniciar tareas de historias P1-P3 dentro del alcance cerrado.

## Readiness Evidence for /speckit.tasks

- Historias P1-P3 con criterios de aceptacion trazables a FR y SC.
- Modelo de datos de estados UI completo para los flujos del MVP.
- Contrato de integracion definido para auth, dashboard, trading, notifications y ai-agent.
- Riesgos y bloqueadores de gobernanza explicitados para planificacion de tareas.

## Final Implementation Readiness (/speckit.implement)

- Setup and foundational tasks completed for frontend workspace bootstrap.
- Governance exception `T006-T007` documented and approved.
- P1, P2, P3 baseline implemented with container-based validation evidence.
- Remaining non-blocking item: ejecutar E2E con browser runtime provisionado en contenedor.

## Go/No-Go Checklist (Sprint 011)

- [x] Contratos backend existentes reutilizados sin expansion de endpoints.
- [x] Validacion en contenedor `Apeiron-Trade` para tests y build.
- [x] Cobertura de pruebas unit + integration en verde.
- [x] Trazabilidad SC-001..SC-004 documentada en `docs/qa/frontend-foundation.md`.
- [ ] E2E browser run completado en contenedor (pendiente no bloqueante para baseline).
