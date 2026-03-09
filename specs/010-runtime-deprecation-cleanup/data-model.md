# Data Model: Runtime Deprecation Cleanup Baseline

**Feature**: `010-runtime-deprecation-cleanup`  
**Date**: 2026-03-09

## Entity: RuntimeWarningRecord

- Purpose: Registrar un warning observado en runtime o suite para decisiones de tratamiento.
- Fields:
  - `id` (string, identificador conceptual)
  - `source` (enum: APP_STARTUP, TEST_SUITE, DEPENDENCY)
  - `warning_class` (string)
  - `message_fingerprint` (string)
  - `first_seen_at` (datetime)
  - `last_seen_at` (datetime)
  - `occurrences` (integer)
  - `severity` (enum: BLOCKING, NON_BLOCKING)
  - `decision` (enum: REMEDIATE, PIN_VERSION, DOCUMENT_EXCEPTION)
  - `decision_owner` (string/role)
  - `decision_status` (enum: OPEN, IN_PROGRESS, CLOSED)
  - `evidence_ref` (string, path a salida de test/log)
- Validation Rules:
  - `decision` obligatorio para warnings recurrentes (FR-004).
  - `message_fingerprint` debe ser estable para agrupar recurrencias.
  - `severity=BLOCKING` requiere `decision_status != OPEN` antes de merge.

## Entity: LifecycleBootstrapPolicy

- Purpose: Definir contrato operativo de inicializacion y cierre de app para evitar uso de patrones deprecados.
- Fields:
  - `policy_id` (string)
  - `lifecycle_pattern` (enum: LIFESPAN_CONTEXT)
  - `startup_steps` (list[string])
  - `shutdown_steps` (list[string])
  - `compatibility_constraints` (list[string])
  - `deprecated_patterns_forbidden` (list[string])
  - `verification_gate` (list[string])
  - `last_reviewed_at` (datetime)
- Validation Rules:
  - `lifecycle_pattern` debe ser patron recomendado vigente.
  - `deprecated_patterns_forbidden` debe incluir eventos de startup obsoletos reemplazados.
  - `verification_gate` debe cubrir SC-001 y SC-002.

## Entity: RuntimeWarningPolicy

- Purpose: Criterio de gobernanza para clasificar, aceptar o bloquear warnings en PR.
- Fields:
  - `policy_version` (string)
  - `blocking_rules` (list[string])
  - `non_blocking_rules` (list[string])
  - `accepted_exception_rules` (list[string])
  - `review_required_by` (string/role)
  - `enforcement_context` (enum: LOCAL, CONTAINER, CI)
- Validation Rules:
  - Prohibida supresion global sin excepcion trazable (FR-005).
  - Toda excepcion requiere fecha de revision futura y owner.
  - Reglas deben ser verificables en revisiones de PR (SC-004).

## Relationships

- `LifecycleBootstrapPolicy` define el marco para detectar `RuntimeWarningRecord` de tipo `APP_STARTUP`.
- `RuntimeWarningPolicy` gobierna la decision y cierre de cada `RuntimeWarningRecord`.
- `RuntimeWarningPolicy` determina si un warning es bloqueante para la aprobacion de PR.

## State Transitions

### RuntimeWarningRecord.decision_status

- `OPEN` -> `IN_PROGRESS` cuando se asigna accion explicita.
- `IN_PROGRESS` -> `CLOSED` cuando hay evidencia verificable de remediacion o excepcion aprobada.
- `OPEN` -> `CLOSED` solo permitido para falsos positivos documentados con evidencia.

### LifecycleBootstrapPolicy lifecycle compliance

- `LEGACY_DEPRECATED` -> `LIFESPAN_COMPLIANT` durante limpieza baseline.
- `LIFESPAN_COMPLIANT` se mantiene si `runtime.lifecycle.deprecation.total = 0` en validaciones.
