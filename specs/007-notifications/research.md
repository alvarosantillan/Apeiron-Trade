# Research: TRDIA - Notifications and Alerts

**Feature**: `007-notifications`  
**Date**: 2026-03-06  
**Spec**: `specs/007-notifications/spec.md`

## Decision 1: Provider Abstraction Layer

- Decision: Implementar interfaz de proveedor push abstracta para desacoplar lógica de negocio de FCM/APNs.
- Rationale: Facilita evolución y testing con mocks consistentes.
- Alternatives considered:
  - Integración directa por endpoint: descartado por acoplamiento alto.
  - Un solo proveedor rígido: descartado por menor resiliencia futura.

## Decision 2: Deduplication by Event Fingerprint

- Decision: Deduplicar por combinación `event_id + user_id + device_id + category` en ventana configurable.
- Rationale: Evita spam de eventos repetidos por reintentos upstream.
- Alternatives considered:
  - Solo `event_id`: descartado por colisiones entre dispositivos/usuarios.
  - Sin deduplicación: descartado por mala UX.

## Decision 3: Critical-First Queueing

- Decision: Procesar eventos críticos con prioridad superior y garantías de envío forzado (respetando seguridad).
- Rationale: Protege casos de riesgo/operación frente a ruido informativo.
- Alternatives considered:
  - Cola única FIFO: descartado por latencia de eventos críticos en picos.

## Decision 4: Retry Policy with Token Invalidation

- Decision: Reintentos con backoff para errores transitorios; invalidación automática de tokens rechazados permanentemente por proveedor.
- Rationale: Mejora entregabilidad y reduce intentos inútiles.
- Alternatives considered:
  - Reintento fijo para todos los errores: descartado por sobrecarga y bajo valor.

## Decision 5: Preference Enforcement in Backend

- Decision: Aplicar preferencias de categorías en backend al generar envíos por dispositivo.
- Rationale: Evita bypass del cliente y garantiza consistencia.
- Alternatives considered:
  - Filtrado en frontend: descartado por inseguridad y desalineación multi-dispositivo.

## Decision 6: Delivery State Tracking per Device

- Decision: Registrar estado de entrega por dispositivo (`queued`, `sent`, `delivered`, `failed`, `dropped`) y `attempt_count`.
- Rationale: Soporte, auditoría y métricas confiables.
- Alternatives considered:
  - Estado agregado por evento: descartado por falta de granularidad.

## Decision 7: Sensitive Payload Discipline

- Decision: Payload mínimo con referencia contextual, sin secretos ni datos financieros sensibles.
- Rationale: Reduce riesgo de exposición en lockscreen/dispositivo comprometido.
- Alternatives considered:
  - Payload completo de operación: descartado por riesgo de privacidad.
