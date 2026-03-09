# Runtime Deprecation Continuity Contract

**Feature**: `010-runtime-deprecation-cleanup`  
**Type**: Runtime behavior and quality gate contract  
**Scope**: Continuidad de comportamiento externo durante limpieza de deprecaciones

## Contract Intent

Este sprint no introduce nuevos endpoints ni cambia payloads de negocio. El contrato de esta feature define condiciones de continuidad y calidad runtime que deben cumplirse antes de avanzar a implementacion de tareas.

## Public Interface Invariants

- Los endpoints existentes mantienen rutas, metodos, codigos de estado y formatos de respuesta vigentes.
- No se agregan ni remueven campos obligatorios en contratos API actuales.
- Errores funcionales mantienen semantica previa de dominios (`auth`, `trading`, `notifications`, `ai_agent`).

## Runtime Quality Gates

- `runtime.lifecycle.deprecation.total = 0` durante arranque de app y ejecucion de suites objetivo.
- Warnings de dependencias recurrentes tienen tratamiento explicito (`REMEDIATE`, `PIN_VERSION`, `DOCUMENT_EXCEPTION`).
- Queda prohibida la supresion global de warnings sin justificacion trazable.

## Evidence Requirements

- Evidencia de ejecucion de pruebas en contenedor con resumen de warnings.
- Comparativa baseline pre/post para mostrar reduccion de warning surface.
- Referencia a politica de runtime warnings utilizable en revision de PR (`docs/methodology/runtime-warning-policy.md`).

## Out of Scope Guardrails

- No cambios de logica de negocio, planes, trading operations o contratos de producto.
- No refactor amplio de modulos no relacionados con lifecycle/runtime warnings.
- No cambios de stack tecnologico en Sprint 010.
