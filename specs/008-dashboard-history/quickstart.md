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
pytest backend/tests/unit -k dashboard_history
pytest backend/tests/integration -k dashboard_history
pytest backend/tests/contract -k dashboard_history
```
