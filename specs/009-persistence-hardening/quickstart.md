# Quickstart: TRDIA - Persistence and Hardening Baseline

## Objective

Validar que Sprint 009 mantiene estado tras reinicios, preserva contratos API existentes y opera con PostgreSQL real bajo condiciones nominales y fallos controlados.

## Prerequisites

- PostgreSQL accesible para entorno de pruebas.
- Variables de entorno de conexion configuradas (host, port, db, user, password).
- Backend levantado con acceso a la base configurada.
- Migraciones versionadas disponibles para aplicar.

## Environment Setup

1. Configurar variables de entorno de DB para modo local/host.
2. Si backend corre en contenedor y DB en host, usar `host.docker.internal` como `DB_HOST`.
3. Ejecutar procedimiento de migraciones antes de iniciar pruebas de API.

Expected:
- Conexion establecida (`db_connected`) y migraciones aplicadas sin errores (`migration_completed`).

## Scenario 1: Persistence After Restart (P1)

1. Crear usuario, sesion, ejecucion de trading, notificacion y config de agente por endpoints existentes.
2. Reiniciar backend.
3. Consultar de nuevo los recursos creados.

Expected:
- No se pierde informacion critica (SC-001).
- Estados y metadatos permanecen consistentes.

## Scenario 2: Contract Compatibility Gate (P1)

1. Ejecutar tests de contrato de `auth`, `trading_execution`, `notifications`, `ai_agent`.
2. Comparar respuestas con contratos vigentes.

Expected:
- No hay ruptura de formato ni semantica en endpoints existentes (SC-003).

## Scenario 3: Host/Container DB Connectivity (P2)

1. Levantar backend en contenedor con `DB_HOST=host.docker.internal`.
2. Ejecutar CRUD basico en dominios criticos.

Expected:
- Conexion funcional desde contenedor al PostgreSQL del host (FR-006).

## Scenario 4: Idempotent Retries for Execution/Events (P2)

1. Reenviar una solicitud con mismo `request_id` en trading execution.
2. Reenviar un evento de notificacion con mismo `event_id`.

Expected:
- No se crean duplicados; backend retorna resultado idempotente (FR-007, SC-005).

## Scenario 5: Controlled Failure Handling (P3)

1. Forzar fallo transitorio de DB (por ejemplo, cortar conectividad temporal).
2. Ejecutar operacion critica de escritura.

Expected:
- API responde error controlado y trazable.
- Se registra evento de auditoria de fallo (`db_connection_failed` o `repository_write_failed`).

## Suggested Test Commands (Reference)

```bash
python -m pytest tests/contract/auth tests/contract/trading_execution tests/contract/notifications tests/contract/ai_agent -q
python -m pytest tests/integration -q
```

## Readiness Evidence for /speckit.tasks

- Historias P1/P2/P3 tienen escenarios verificables.
- Se definio gate de migraciones + smoke + regresion de contratos.
- Criterios de exito del spec mapeados a pruebas de aceptacion.
