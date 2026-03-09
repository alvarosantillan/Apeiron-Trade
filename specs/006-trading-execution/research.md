# Research: TRDIA - Trading Execution

**Feature**: `006-trading-execution`  
**Date**: 2026-03-06  
**Spec**: `specs/006-trading-execution/spec.md`

## Decision 1: Idempotency by `request_id`

- Decision: Toda solicitud de ejecución requiere `request_id` único por usuario y ventana temporal.
- Rationale: Evita doble ejecución por reintentos/red inestable.
- Alternatives considered:
  - Hash del payload completo: descartado por colisiones semánticas ante cambios menores.
  - Sin idempotencia: descartado por riesgo financiero.

## Decision 2: Explicit Execution State Machine

- Decision: Modelar estados `received`, `validated`, `blocked`, `submitted`, `executed`, `failed`, `pending_reconciliation`, `cancelled`.
- Rationale: Clarifica trazabilidad y manejo de incertidumbre con exchange.
- Alternatives considered:
  - Estados simplificados éxito/fallo: descartado por baja auditabilidad.

## Decision 3: Backend-Only Plan Enforcement

- Decision: Validar plan/límite en backend justo antes de enviar orden real.
- Rationale: Evita bypass y asegura coherencia ante cambios de suscripción.
- Alternatives considered:
  - Validación solo al inicio de sesión: descartado por stale state.
  - Validación en frontend: descartado por inseguro.

## Decision 4: Paper Trading as First-Class Flow

- Decision: La simulación comparte validaciones estructurales (símbolo/parametría), pero no usa saldo real ni incrementa contador semanal.
- Rationale: Permite pruebas realistas sin riesgo ni consumo.
- Alternatives considered:
  - Simulación fuera del mismo flujo: descartado por duplicación de lógica.

## Decision 5: Controlled Retry + Reconciliation

- Decision: Reintentar solo errores transitorios (network/5xx) con backoff y límite; si hay incertidumbre, pasar a `pending_reconciliation`.
- Rationale: Balancea resiliencia y prevención de duplicados.
- Alternatives considered:
  - Reintentos agresivos: descartado por riesgo de órdenes repetidas.
  - Sin reconciliación: descartado por inconsistencias operativas.

## Decision 6: Atomic Counter Updates

- Decision: Contador semanal se incrementa en transacción atómica al confirmar envío/ejecución real válida, contabilizando BUY y SELL por separado.
- Rationale: Alinea con regla de negocio definida y evita race conditions.
- Alternatives considered:
  - Cálculo dinámico por query histórica: descartado por costo y latencia en picos.

## Decision 7: Notification-at-Outcome Policy

- Decision: Emitir notificación en estado terminal (`executed`, `failed`, `blocked`, `cancelled`).
- Rationale: Experiencia consistente y clara para el usuario.
- Alternatives considered:
  - Notificar cada subestado: descartado por ruido excesivo.
