# Quickstart: TRDIA - Dashboard and Trade History

## Objective

Validar dashboard operativo, historial filtrable, detalle de operación y KPIs en escenarios típicos y edge cases.

## Prerequisites

- Backend y base de datos operativos
- Usuario autenticado con operaciones históricas de prueba
- Dataset con operaciones reales y simuladas

## Scenario 1: Carga de Dashboard

1. Llamar `GET /v1/dashboard/summary`.
2. Verificar presencia de plan, uso/límite semanal, estado de bot y balance.

Expected:
- Respuesta en tiempo objetivo.
- Datos coherentes con estado actual del usuario.

## Scenario 2: Historial Filtrado por Simulación

1. Llamar `GET /v1/history/trades?isSimulation=true&limit=20`.
2. Validar etiquetas de cada item retornado.

Expected:
- Solo operaciones simuladas.
- Orden cronológico descendente.

## Scenario 3: Historial con Filtros Combinados

1. Consultar con `from`, `to`, `status` y `cursor`.
2. Navegar a la siguiente página.

Expected:
- Paginación estable sin duplicados/saltos.
- Errores claros ante filtros inválidos.

## Scenario 4: Detalle de Operación

1. Llamar `GET /v1/history/trades/{tradeId}` para una operación válida del usuario.
2. Verificar trazabilidad y motivo de fallo si aplica.

Expected:
- Detalle completo con referencia de ejecución.
- Registro de auditoría de acceso generado.

## Scenario 5: KPIs 7d y 30d

1. Llamar `GET /v1/dashboard/kpis?window=7d` y `?window=30d`.
2. Validar total trades, win rate y net PnL.

Expected:
- KPIs consistentes con dataset.
- Ventanas no soportadas devuelven validación de error.

## Scenario 6: Usuario Nuevo Sin Historial

1. Repetir escenarios con usuario sin operaciones.

Expected:
- Dashboard con estado vacío informativo.
- Historial vacío sin errores.

## Test Commands (Reference)

```bash
python -m pytest tests/contract/dashboard_history tests/integration/dashboard_history -q
```

## Validation Evidence

- Command: `python -m pytest tests/contract/dashboard_history tests/integration/dashboard_history -q`
- Result: `8 passed, 1 warning`
- Scenario mapping:
	- Scenario 1: `test_dashboard_summary_contract`, `test_dashboard_load_for_active_user`
	- Scenario 2: `test_history_combined_filters_and_cursor_pagination` (with `isSimulation=true`)
	- Scenario 3: `test_history_combined_filters_and_cursor_pagination`, `test_history_contract_returns_items_and_next_cursor`
	- Scenario 4: `test_trade_detail_contract`, `test_trade_detail_access_writes_audit_event`
	- Scenario 5: `test_kpi_endpoint_contract`, `test_kpi_invalid_window_returns_400`
	- Scenario 6: `test_dashboard_summary_contract` (default empty user state)
