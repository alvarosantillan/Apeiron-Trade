# Research: Runtime Deprecation Cleanup Baseline

**Feature**: `010-runtime-deprecation-cleanup`  
**Date**: 2026-03-09  
**Spec**: `specs/010-runtime-deprecation-cleanup/spec.md`

## Decision 1: Migrate Startup Events to Lifespan Pattern

- Decision: Reemplazar manejo obsoleto de startup/shutdown por patron lifespan recomendado por FastAPI.
- Rationale: Cumple FR-001 y SC-001 eliminando warning deprecado en arranque sin cambiar contratos funcionales.
- Alternatives considered:
  - Mantener eventos obsoletos temporalmente: descartado por deuda tecnica activa y riesgo en upgrades.
  - Suprimir warning en runtime: descartado por FR-005 (oculta problema en lugar de resolverlo).

## Decision 2: Preserve Bootstrap Behavior as Compatibility Gate

- Decision: Definir equivalencia funcional explicita del bootstrap antes/despues de la migracion.
- Rationale: Cumple FR-002 y protege estabilidad operativa del backend.
- Alternatives considered:
  - Aceptar cambios colaterales de inicializacion: descartado por riesgo de regresion en flujos existentes.
  - Posponer pruebas de equivalencia para post-merge: descartado por violar enfoque TDD del proyecto.

## Decision 3: Runtime Warning Baseline in Container as Source of Truth

- Decision: Usar ejecucion en contenedor `Apeiron-Trade` como baseline canonico para medir warning surface.
- Rationale: Cumple FR-003 y reduce variabilidad entre entornos locales.
- Alternatives considered:
  - Baseline solo en entorno local: descartado por baja reproducibilidad.
  - Baseline manual sin evidencia automatizada: descartado por baja trazabilidad para PR review.

## Decision 4: Explicit Treatment Matrix for Recurrent Dependency Warnings

- Decision: Clasificar warnings recurrentes por accion explicita: remediar, fijar version o documentar excepcion temporal con justificacion.
- Rationale: Cumple FR-004 y FR-005, evitando supresion global sin criterio.
- Alternatives considered:
  - Ignorar warnings no bloqueantes: descartado por normalizar ruido en CI.
  - Silenciar todos los warnings de terceros: descartado por riesgo de ocultar fallos reales.

## Decision 5: Runtime Warning Policy as Documentation Contract

- Decision: Documentar politica operativa de warnings (bloqueante vs no bloqueante), evidencia requerida y ownership de seguimiento.
- Rationale: Cumple FR-006 y SC-004 para prevenir regresion silenciosa.
- Alternatives considered:
  - Dejar criterio implicito en revisiones ad hoc: descartado por inconsistencia entre PRs.
  - Registrar solo una lista de warnings permitidos sin reglas: descartado por falta de gobernanza.

## Decision 6: Scope Lock to Baseline Cleanup Only

- Decision: Limitar Sprint 010 a lifecycle deprecation cleanup, warning surface control y policy docs; excluir refactors de negocio o cambios de contrato.
- Rationale: Alinea alcance cerrado del spec y Principle VII (Progressive Enhancement).
- Alternatives considered:
  - Incluir refactor amplio de dependencias: descartado por expansion de alcance.
  - Incluir cambios de producto/API: descartado por no estar en historias P1-P3.
