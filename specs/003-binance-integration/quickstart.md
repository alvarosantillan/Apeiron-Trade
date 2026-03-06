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
- POST /api/v1/trading/binance/credentials
- Expect 200 y estado `verified=true`

2. Ejecutar operación real válida
- POST /api/v1/trading/execute con is_simulation=false
- Expect 200 y status `executed`

3. Bloqueo por límite semanal
- Forzar contador al límite
- POST /api/v1/trading/execute
- Expect 403 con reason `weekly_limit_exceeded`

4. Operación simulada ilimitada
- POST /api/v1/trading/execute con is_simulation=true
- Expect 200/201 y no incremento de operaciones reales

5. Consultar historial
- GET /api/v1/trading/history
- Expect lista con diferenciación real/simulación

## Negative checks

- Credenciales inválidas -> 400
- request_id repetido -> respuesta idempotente sin duplicar ejecución
- Símbolo inválido o cantidad <= 0 -> 422
- Usuario Free intentando auto-ejecución sin aprobación -> 403
