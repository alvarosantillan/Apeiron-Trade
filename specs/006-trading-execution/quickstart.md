# Quickstart: TRDIA - Trading Execution

## Objective

Validar el flujo de ejecución Spot real/simulado con enforcement de reglas de plan, idempotencia y trazabilidad.

## Prerequisites

- Backend y workers corriendo
- Integración Binance configurada para usuario de prueba
- Suscripción activa (Free/Plus/Premium)
- Endpoints de notificaciones disponibles

## Scenario 1: Ejecutar Orden Real Exitosa

1. Enviar solicitud `POST /v1/trading/executions` con `isSimulation=false`, orden MARKET válida y `requestId` nuevo.
2. Consultar ejecución por `executionId`.
3. Verificar historial y evento de notificación.

Expected:
- Estado terminal `EXECUTED`.
- Registro de auditoría completo.
- Contador semanal incrementado en 1.

## Scenario 2: Bloqueo por Límite de Plan

1. Preparar usuario Free con límite semanal agotado.
2. Enviar orden real adicional.

Expected:
- Estado `BLOCKED` con razón `weekly_limit_exceeded`.
- No se envía orden al exchange.
- No cambia el contador.

## Scenario 3: Simulación sin Consumo de Límite

1. Con mismo usuario Free agotado, enviar orden con `isSimulation=true`.
2. Consultar ejecución y contador.

Expected:
- Flujo finaliza en `EXECUTED` (simulado).
- `operations_used` se mantiene igual.

## Scenario 4: Idempotencia por Request ID

1. Reenviar la misma solicitud con igual `requestId`.
2. Comparar respuesta y registros.

Expected:
- Se devuelve misma ejecución lógica (sin duplicado).
- Solo una ejecución real registrada.

## Scenario 5: Timeout y Reconciliación

1. Simular timeout después de `SUBMITTED`.
2. Verificar transición a `PENDING_RECONCILIATION`.
3. Ejecutar reconciliación.

Expected:
- Estado final consistente (`EXECUTED` o `FAILED`).
- Auditoría refleja proceso de reconciliación.

## Test Commands (Reference)

```bash
python -m pytest tests/contract/trading_execution tests/integration/trading_execution -q
```

## Validation Evidence

- Command: `python -m pytest tests/contract/trading_execution tests/integration/trading_execution -q`
- Result: `7 passed, 1 warning`
- Scenario mapping:
	- Scenario 1: `test_create_execution_returns_201_and_shape`, `test_real_execution_success_and_fetch_by_id`
	- Scenario 2: `test_weekly_limit_exceeded_is_blocked`
	- Scenario 3: `test_paper_execution_does_not_increment_real_counter`
	- Scenario 4: `test_same_request_id_replays_same_execution_without_duplicate`
	- Scenario 5: `test_timeout_goes_to_reconciliation_and_resolves`
