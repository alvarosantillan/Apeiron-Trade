# Research: TRDIA - Persistence and Hardening Baseline

**Feature**: `009-persistence-hardening`  
**Date**: 2026-03-09  
**Spec**: `specs/009-persistence-hardening/spec.md`

## Decision 1: PostgreSQL as Single Source of Truth for Critical Domains

- Decision: Persistir `auth`, `trading_execution`, `notifications` y `ai_agent_config` en PostgreSQL y retirar uso in-memory en flujo operativo.
- Rationale: Cumple FR-001/FR-002 y elimina perdida de estado tras reinicios.
- Alternatives considered:
  - Mantener esquema hibrido in-memory + DB: descartado por inconsistencia y riesgo operacional.
  - Persistencia por archivos locales: descartado por baja confiabilidad y trazabilidad limitada.

## Decision 2: Versioned Migrations as Mandatory Startup Gate

- Decision: Gestionar esquema con migraciones versionadas y procedimiento de aplicacion explicito en arranque/deploy.
- Rationale: Cumple FR-004 y reduce drift de esquema entre entornos.
- Alternatives considered:
  - Crear tablas ad-hoc al iniciar servicio: descartado por falta de control/versionado.
  - Cambios manuales SQL fuera de flujo: descartado por riesgo de errores humanos.

## Decision 3: Repository Boundary to Preserve API Contracts

- Decision: Introducir/usar capa de repositorio persistente debajo de servicios actuales para conservar contratos API sin cambios.
- Rationale: Cumple FR-003 y minimiza regresiones para consumidores existentes.
- Alternatives considered:
  - Reescribir endpoints y payloads durante migracion: descartado por expansion de alcance.
  - Acceso SQL directo desde controladores: descartado por acoplamiento y menor testabilidad.

## Decision 4: Transaction + Idempotency Keys for Execution/Event Writes

- Decision: Mantener idempotencia de ejecuciones/eventos con llaves idempotentes (`request_id`, `event_id`) y escrituras transaccionales.
- Rationale: Cumple FR-007 y SC-005 evitando duplicados en reintentos/fallos transitorios.
- Alternatives considered:
  - Idempotencia solo en memoria: descartado por perdida de estado tras reinicio.
  - Reconciliacion eventual sin constraints: descartado por ventana de inconsistencias.

## Decision 5: Controlled Error Taxonomy with Audit Events

- Decision: Definir errores controlados de conexion/transaccion y registrar eventos de auditoria operativa para operaciones criticas.
- Rationale: Cumple FR-008/FR-009 y requisitos de observabilidad/seguridad del spec.
- Alternatives considered:
  - Propagar errores DB crudos al cliente: descartado por baja trazabilidad y riesgo de filtrado tecnico.
  - Loggear todo payload para debugging: descartado por riesgo sobre datos sensibles.

## Decision 6: Host and Container Connectivity Contract

- Decision: Estandarizar configuracion por variables de entorno y documentar `host.docker.internal` para conexion desde contenedor al PostgreSQL del host.
- Rationale: Cumple FR-005/FR-006 y reduce friccion de onboarding.
- Alternatives considered:
  - Configuracion implicita por defaults no documentados: descartado por drift entre entornos.
  - Soportar solo DB dockerizada interna: descartado por limitar escenarios de desarrollo.

## Decision 7: Smoke + Regression Gate for Implementation Readiness

- Decision: Exigir smoke tests con DB real y regresion de contratos para declarar listo el sprint.
- Rationale: Cumple FR-010 y protege continuidad funcional de features 002-008.
- Alternatives considered:
  - Solo unit tests para la migracion: descartado por cobertura insuficiente de integracion.
  - Validacion manual sin automatizacion: descartado por baja repetibilidad.
