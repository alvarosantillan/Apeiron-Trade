# Research: TRDIA - AI Agent

**Feature**: `005-ai-agent`  
**Date**: 2026-03-06  
**Spec**: `specs/005-ai-agent/spec.md`

## Decision 1: Unified Provider Adapter Contract

- Decision: Definir una interfaz interna única para proveedores IA con dos operaciones: `validate_credentials` y `generate_trade_decision`.
- Rationale: Permite sumar proveedores sin tocar reglas de negocio y reduce acoplamiento con SDKs.
- Alternatives considered:
  - Llamadas directas a SDK en casos de uso: descartado por acoplamiento alto.
  - Normalización parcial por endpoint: descartado por inconsistencias y lógica duplicada.

## Decision 2: Structured Decision Output as Source of Truth

- Decision: Toda respuesta de proveedor se normaliza a `action`, `confidence`, `reasoning`, `risk_level`, `symbol`, `timeframe`, `decision_ts`.
- Rationale: Facilita validación, trazabilidad, reglas por plan y ejecución posterior.
- Alternatives considered:
  - Guardar texto libre y parsear ad-hoc: descartado por fragilidad y baja auditabilidad.
  - Esquema diferente por proveedor: descartado por complejidad operativa.

## Decision 3: Safe Fallback Policy

- Decision: Ante timeout, error de proveedor o salida inválida, persistir decisión con `action=HOLD` y motivo de fallback.
- Rationale: Seguridad operacional y continuidad del sistema sin decisiones ciegas.
- Alternatives considered:
  - Reintentos indefinidos: descartado por latencia y bloqueo.
  - Omitir decisión: descartado por pérdida de trazabilidad.

## Decision 4: Prompt Composition with Strategy Guardrails

- Decision: Construir prompt con plantillas controladas por catálogo de estrategia y parámetros del usuario (riesgo/timeframe), sin prompts libres.
- Rationale: Mantiene coherencia de producto y reduce variabilidad de salida.
- Alternatives considered:
  - Prompt libre por usuario: descartado por alcance v1 y riesgo de resultados inconsistentes.
  - Prompt único fijo para todos: descartado por poca adaptabilidad.

## Decision 5: Plan-Aware Execution Eligibility

- Decision: El backend valida elegibilidad de modo automático por plan en cada decisión antes de emitir señal ejecutable.
- Rationale: Regla de negocio crítica no delegable al frontend.
- Alternatives considered:
  - Validar solo al guardar configuración: descartado por riesgo ante cambios de plan.
  - Validar en frontend: descartado por bypass fácil.

## Decision 6: Anti-Duplicate Signals Window

- Decision: Aplicar ventana temporal configurable por estrategia/símbolo para evitar decisiones repetidas equivalentes.
- Rationale: Disminuye ruido y sobre-operación.
- Alternatives considered:
  - Sin filtro de duplicados: descartado por riesgo de spam de decisiones.
  - Filtro global único: descartado por no respetar contexto de estrategia.

## Decision 7: Observability Baseline

- Decision: Instrumentar métricas por proveedor (`latency_ms`, `success_rate`, `fallback_rate`, `decision_count`) y logs estructurados con IDs correlacionados.
- Rationale: Diagnóstico rápido y control operativo del agente.
- Alternatives considered:
  - Solo logs texto: descartado por baja capacidad analítica.
  - Métricas solo globales: descartado por falta de visibilidad por proveedor.
