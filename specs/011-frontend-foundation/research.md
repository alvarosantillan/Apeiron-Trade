# Research: Frontend Foundation MVP

**Feature**: `011-frontend-foundation`  
**Date**: 2026-03-09  
**Spec**: `specs/011-frontend-foundation/spec.md`

## Decision 1: Frontend MVP Target Is Web Application

- Decision: Planificar Sprint 011 como frontend web MVP para validacion funcional de flujos end-to-end.
- Rationale: El spec oficial de la feature define alcance web y excluye apps moviles para este sprint.
- Alternatives considered:
  - React Native (Expo) desde el inicio: descartado para este sprint por conflicto con alcance cerrado en spec y mayor costo de bootstrap para validacion funcional inmediata.
  - CLI/Swagger-only operations: descartado porque no cumple FR-001, FR-002 y FR-003 de experiencia de usuario.

## Decision 2: Backend Existing APIs Are the Integration Source of Truth

- Decision: Reutilizar contratos backend existentes de features `002` a `010` sin introducir endpoints nuevos en Sprint 011.
- Rationale: Mantiene alcance MVP frontend foundation y reduce riesgo de expansion de dominio.
- Alternatives considered:
  - Crear endpoints agregadores nuevos para UI: descartado por ampliar alcance y mezclar implementacion backend fuera de sprint.
  - Mock-only frontend flows: descartado porque no valida comportamiento real del sistema.

## Decision 3: Auth Guard and Session Handling Stay Thin in Frontend

- Decision: Definir capa de sesion y guardas de rutas como orquestacion de UX; toda autorizacion y validacion de negocio permanece en backend.
- Rationale: Cumple Principle V (Validation-Strict) y FR-003 evitando mover logica critica al cliente.
- Alternatives considered:
  - Enforce de limites/planes en frontend: descartado por violar constitucion.
  - Persistencia amplia de credenciales en cliente: descartado por Principle III (Security-First).

## Decision 4: Test Strategy for Frontend Foundation Uses Layered Checks

- Decision: Preparar estrategia TDD con pruebas unitarias de estado/guardas, integracion de vistas por flujo y smoke E2E de historias P1-P3.
- Rationale: Alinea Principle II y permite validar SC-001..SC-004 por historia priorizada.
- Alternatives considered:
  - Solo pruebas manuales: descartado por baja repetibilidad.
  - Solo E2E extensivo: descartado para MVP por costo de mantenimiento y baja velocidad de feedback.

## Decision 5: Error and Empty-State UX Is Contractual for MVP

- Decision: Tratar estados `loading/empty/error/success` como contrato transversal en dashboard, trading, notifications y ai-agent.
- Rationale: Cubre FR-009/FR-010 y reduce friccion operativa en pruebas con usuarios.
- Alternatives considered:
  - Manejo ad hoc por pantalla: descartado por inconsistencia UX.
  - Mostrar errores tecnicos de backend al usuario final: descartado por seguridad y claridad.

## Decision 6: Constitution Conflict Requires Governance Note Before Implementation

- Decision: Registrar en plan la desviacion temporal entre stack frontend constitucional (React Native) y alcance web del spec 011, condicionando implementacion a validacion de maintainer (exception o amendment).
- Rationale: Evita incumplimiento silencioso y deja trazabilidad de gobernanza.
- Alternatives considered:
  - Ignorar conflicto y avanzar: descartado por riesgo de violacion constitucional no documentada.
  - Reescribir alcance del spec sin aprobacion: descartado porque el spec es fuente de verdad de la feature.
