# Quickstart: TRDIA - Notifications and Alerts

## Objective

Validar envíos push por eventos críticos, preferencias por categoría, deduplicación y trazabilidad de entregas.

## Prerequisites

- Backend y workers en ejecución
- Integración proveedor push configurada en entorno de prueba
- Usuario autenticado con al menos un token de dispositivo registrado

## Scenario 1: Registrar Token de Dispositivo

1. Enviar `POST /v1/notifications/device-tokens` con `deviceId`, `platform` y `pushToken`.
2. Consultar tokens activos del usuario.

Expected:
- Token registrado/actualizado correctamente.
- No se exponen tokens completos en respuestas o logs.

## Scenario 2: Envío por Evento de Trading Exitoso

1. Simular creación de evento de ejecución exitosa.
2. Procesar cola de notificaciones.
3. Consultar historial de notificaciones.

Expected:
- Se crea evento y entrega por dispositivo activo.
- Estado final `SENT` o `DELIVERED`.

## Scenario 3: Preferencias de Usuario

1. Desactivar categoría `MARKETING` y mantener `TRADING` activa.
2. Emitir evento marketing y evento trading.

Expected:
- Evento marketing no genera entrega.
- Evento trading sí genera entrega.

## Scenario 4: Deduplicación

1. Emitir dos veces el mismo `eventId` para usuario/dispositivo.
2. Consultar entregas registradas.

Expected:
- Solo una entrega efectiva por dispositivo.
- Evento duplicado marcado/ignorado en auditoría.

## Scenario 5: Reintento e Invalidez de Token

1. Simular fallo transitorio del proveedor push y luego recuperación.
2. Simular token inválido permanente.

Expected:
- Fallo transitorio dispara reintentos con backoff.
- Token inválido se desactiva (`is_active=false`) y entrega pasa a `DROPPED`.

## Test Commands (Reference)

```bash
python -m pytest tests/contract/notifications tests/integration/notifications -q
```

## Validation Evidence

- Command: `python -m pytest tests/contract/notifications tests/integration/notifications -q`
- Result: `7 passed, 1 warning`
- Scenario mapping:
	- Scenario 1: `test_upsert_and_list_device_tokens`
	- Scenario 2: `test_trading_event_push_delivery`
	- Scenario 3: `test_marketing_disabled_but_critical_override_allows_delivery`
	- Scenario 4: `test_same_event_id_is_deduplicated_per_device`
	- Scenario 5: `test_transient_failure_ends_in_failed_after_retries`, `test_invalid_token_is_dropped_and_deactivated`
