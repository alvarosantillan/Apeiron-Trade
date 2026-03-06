# Quickstart: TRDIA - AI Agent

## Objective

Validar de extremo a extremo la configuración del agente IA, generación de decisiones y enforcement por plan.

## Prerequisites

- Backend y workers en ejecución
- PostgreSQL y Redis disponibles
- Usuario autenticado con plan activo
- Catálogo de estrategias inicializado

## Scenario 1: Configurar Agente (Manual)

1. Consultar proveedores soportados.
2. Guardar configuración con `provider`, `api_key`, `strategy_id`, `risk_profile`, `mode=MANUAL`.
3. Verificar respuesta sin exposición de `api_key`.
4. Consultar estado de configuración activa.

Expected:
- Configuración creada/actualizada correctamente.
- Auditoría de cambio registrada.

## Scenario 2: Intentar Modo Automático en Plan Free

1. Con usuario Free, enviar actualización con `mode=AUTOMATIC`.

Expected:
- Rechazo con error de validación de plan.
- Configuración previa se mantiene intacta.

## Scenario 3: Generación de Decisión Exitosa

1. Disparar ciclo de decisión para símbolo permitido.
2. Simular respuesta válida del proveedor.
3. Consultar última decisión del usuario.

Expected:
- Se persiste `action`, `confidence`, `reasoning`, `status`.
- La decisión queda `PENDING_APPROVAL` en modo manual.

## Scenario 4: Fallback por Error de Proveedor

1. Simular timeout o respuesta inválida del proveedor.
2. Ejecutar ciclo de decisión.

Expected:
- Se persiste decisión con `action=HOLD` y `status=FALLBACK_HOLD`.
- Se registra `fallback_reason` y métrica de fallback.

## Scenario 5: Anti-duplicado de Señales

1. Emitir dos solicitudes equivalentes dentro de la ventana configurada.
2. Consultar historial.

Expected:
- No se duplican decisiones ejecutables equivalentes.
- Se conserva trazabilidad de deduplicación.

## Test Commands (Reference)

```bash
pytest backend/tests/unit -k ai_agent
pytest backend/tests/integration -k ai_agent
pytest backend/tests/contract -k ai_agent
```
