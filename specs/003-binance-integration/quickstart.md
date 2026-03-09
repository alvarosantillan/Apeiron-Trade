# Quickstart - 003-binance-integration

## Goal

Validar integración Binance Spot (real y simulada) con enforcement de reglas de plan.

## Preconditions

- Backend en ejecución
- PostgreSQL disponible
- Usuario autenticado con JWT
- Credenciales Binance de test (o mocks)

## Flows

1. Configurar credenciales Binance
- POST /v1/trading/binance/credentials
- Expect 200 y estado `verified=true`

2. Ejecutar operación real válida
- POST /v1/trading/execute con is_simulation=false
- Expect 200 y status `executed`

3. Bloqueo por límite semanal
- Forzar contador al límite
- POST /v1/trading/execute
- Expect 403 con reason `weekly_limit_exceeded`

4. Operación simulada ilimitada
- POST /v1/trading/execute con is_simulation=true
- Expect 200/201 y no incremento de operaciones reales

5. Consultar historial
- GET /v1/trading/history
- Expect lista con diferenciación real/simulación

## Negative checks

- Credenciales inválidas -> 400
- request_id repetido -> respuesta idempotente sin duplicar ejecución
- Símbolo inválido o cantidad <= 0 -> 422
- Usuario Free intentando auto-ejecución sin aprobación -> 403

## Validation Evidence

- Command: `python -m pytest tests/contract/trading tests/integration/trading tests/unit/trading -q`
- Result: `11 passed, 1 warning`
- Scenario mapping:
	- Flow 1: `test_save_credentials_returns_200_and_active_status`
	- Flow 2: `test_execute_real_buy_order_success`
	- Flow 3: `test_paper_execution_does_not_consume_real_weekly_limit` (real second order blocked)
	- Flow 4: `test_paper_execution_does_not_consume_real_weekly_limit` (paper order allowed)
	- Flow 5: `test_trade_history_filters_and_pagination`
	- Negative checks: `test_invalid_binance_credentials_return_400`, `test_execute_duplicate_request_id_returns_409`
