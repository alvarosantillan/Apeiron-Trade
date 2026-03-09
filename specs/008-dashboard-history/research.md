# Research: TRDIA - Dashboard and Trade History

**Feature**: `008-dashboard-history`  
**Date**: 2026-03-06  
**Spec**: `specs/008-dashboard-history/spec.md`

## Decision 1: Snapshot + Live Read Hybrid

- Decision: Dashboard combina snapshot reciente (estado de bot/plan/uso) con lectura puntual de datos críticos (balance).
- Rationale: Balancea latencia y frescura de información.
- Alternatives considered:
  - Todo en tiempo real: descartado por costo/latencia en picos.
  - Todo precomputado: descartado por riesgo de staleness.

## Decision 2: Strict Cursor Pagination for History

- Decision: Historial usa paginación cursor-based con orden cronológico descendente por defecto.
- Rationale: Mayor estabilidad en datasets grandes y mejor rendimiento.
- Alternatives considered:
  - Offset pagination: descartado por degradación en páginas profundas.

## Decision 3: Backend Filter Validation Matrix

- Decision: Backend valida combinaciones de filtros (fechas, estado, modo) y aplica límites de rango.
- Rationale: Previene queries costosas o inválidas.
- Alternatives considered:
  - Validación mínima: descartado por riesgo de abuso y errores ambiguos.

## Decision 4: Detail View from Canonical Execution Trace

- Decision: El detalle de operación se construye a partir de trazas canónicas de ejecución/auditoría, no de payloads de cliente.
- Rationale: Garantiza fidelidad y soporte forense.
- Alternatives considered:
  - Ensamblado parcial desde frontend: descartado por inconsistencia.

## Decision 5: KPI Windows 7d/30d as MVP

- Decision: Calcular y exponer KPIs estandarizados para ventanas 7d y 30d en v1.
- Rationale: Entrega valor inmediato sin sobrecomplejidad.
- Alternatives considered:
  - Ventanas arbitrarias ilimitadas: descartado por complejidad inicial.

## Decision 6: Empty-State First-Class UX Contract

- Decision: Definir respuestas explícitas para usuarios sin historial ni actividad.
- Rationale: Evita errores y mejora onboarding.
- Alternatives considered:
  - Respuesta vacía sin contexto: descartado por mala experiencia.

## Decision 7: Audit Access to Operation Detail

- Decision: Registrar accesos a detalle de operación con metadata mínima (`user_id`, `trade_id`, `timestamp`).
- Rationale: Soporte, seguridad y trazabilidad operativa.
- Alternatives considered:
  - Sin auditoría de lectura: descartado por menor control de soporte.
