# Quickstart: Runtime Deprecation Cleanup Baseline

## Objective

Validar que Sprint 010 elimina warnings deprecados de lifecycle, mantiene comportamiento funcional y deja politica de warnings runtime lista para revisiones futuras.

## Prerequisites

- Entorno backend ejecutable en contenedor `Apeiron-Trade`.
- Dependencias del backend instaladas.
- Suite `pytest` disponible para `tests/contract`, `tests/integration` y `tests/unit`.
- Spec y plan de Sprint 010 aprobados.

## Validation Flow

1. Ejecutar baseline de arranque y tests en contenedor para capturar warning surface actual.
2. Validar que warnings de lifecycle deprecado se reduzcan a cero tras cleanup.
3. Confirmar que los flujos funcionales existentes siguen estables.
4. Registrar decisiones explicitas para warnings de dependencias recurrentes.
5. Confirmar que la politica de warnings queda referenciable para PR review.

## Scenario 1: Startup Deprecation Removal (P1)

1. Iniciar backend en contenedor.
2. Revisar salida de runtime y arranque de app.

Expected:
- No aparece warning por patron de lifecycle obsoleto (SC-001).
- Eventos de startup/shutdown relevantes permanecen observables.

## Scenario 2: Behavioral Compatibility Gate (P1)

1. Ejecutar suites de contrato e integracion existentes.
2. Comparar resultados frente a baseline previo.

Expected:
- 100% de pruebas existentes pasan (SC-002).
- Sin regresion funcional por migracion de lifecycle.

## Scenario 3: Dependency Warning Surface Stabilization (P2)

1. Ejecutar suite en contenedor y listar warnings recurrentes.
2. Para cada warning recurrente, asignar accion explicita (remediar, pin, excepcion documentada).

Expected:
- Reduccion observable de warnings totales vs baseline (SC-003).
- No supresion global de warnings sin justificacion (FR-005).

## Scenario 4: Runtime Warning Policy Readiness (P3)

1. Revisar documentacion de metodologia/politica runtime warnings.
2. Verificar criterio de warnings bloqueantes vs no bloqueantes para PRs.
3. Confirmar referencia explicita a `docs/methodology/runtime-warning-policy.md` en artefactos de feature.

Expected:
- Politica documentada, clara y referenciable (SC-004).
- Cada excepcion potencial tiene owner y rationale.

## Policy Reference (Required)

- `docs/methodology/runtime-warning-policy.md`

## Suggested Test Commands (Reference)

```bash
python -m pytest tests/contract -q
python -m pytest tests/integration -q
python -m pytest tests/unit -q
```

## Readiness Evidence for /speckit.tasks

- Historias P1, P2 y P3 tienen escenarios verificables y secuencia clara.
- Gates de exito SC-001..SC-004 mapeados a evidencia de runtime/tests/documentacion.
- Alcance cerrado a cleanup de baseline runtime sin cambios de negocio.
