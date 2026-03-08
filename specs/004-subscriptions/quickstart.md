# Quickstart - 004-subscriptions

## Goal

Validar flujo completo de suscripciones y pagos con MercadoPago sandbox.

## Preconditions

- Backend en ejecución
- Variables de entorno de MercadoPago sandbox configuradas
- Usuario autenticado con plan Free

## Flows

1. Inicialización de planes
- Reiniciar backend
- Verificar que Free/Plus/Premium existen/sincronizados sin duplicados

2. Checkout Plus
- POST /v1/subscriptions/checkout con plan=plus
- Completar pago sandbox
- Esperar webhook aprobado
- GET /v1/subscriptions/status -> plan=plus

3. Upgrade a Premium
- Repetir checkout con plan=premium
- Verificar estado plan actualizado

4. Downgrade/Cancelación
- POST /v1/subscriptions/transition (targetPlanCode=plus|premium|free)
- POST /v1/subscriptions/cancel (cancelAtPeriodEnd=true|false)
- Verificar `cancelAtPeriodEnd=true` o cambio inmediato a `free`

5. Validación en trading
- Forzar estado `past_due`
- Intentar operación real
- Esperar bloqueo por suscripción inválida

## Negative checks

- Webhook firma inválida -> rechazado
- Webhook duplicado -> marcado duplicate, sin re-procesar
- Pago rechazado -> no cambia plan

## Validation Notes (2026-03-08)

- Tests de contract e integración de subscriptions ejecutados en `Apeiron-Trade`.
- Regresión auth incluida para evitar roturas cross-feature.
