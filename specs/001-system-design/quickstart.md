# Quickstart: TRDIA - System Design Foundation

## Objective

Validar que la base arquitectónica del proyecto está lista para implementar features con SDD + TDD.

## Prerequisites

- Entorno local con backend, Redis y PostgreSQL disponible
- Variables de entorno base configuradas (sin secretos hardcodeados)
- Rama `001-system-design` activa

## Step 1: Validate Project Skeleton

1. Confirmar módulos backend: `api`, `trading`, `agents`, `payments`, `analytics`, `workers`.
2. Confirmar estructura frontend: `screens`, `features`, `services`, `state`.

Expected:
- Estructura modular coherente con spec.

## Step 2: Validate Security Baseline

1. Revisar que endpoints críticos exijan autenticación.
2. Verificar estrategia de cifrado para credenciales de exchange/IA.
3. Verificar que logs no incluyan secretos.

Expected:
- Políticas de seguridad base definidas y verificables.

## Step 3: Validate Core Business Invariants

1. Simular usuario con plan Free y límite semanal agotado.
2. Intentar ejecución real de operación.

Expected:
- Operación bloqueada por backend con motivo explícito.

## Step 4: Validate Observability Baseline

1. Ejecutar flujo de operación simulada.
2. Verificar emisión de métricas y eventos de auditoría.

Expected:
- Métricas y logs estructurados presentes para el flujo.

## Step 5: Validate Feature Readiness

1. Revisar que cada feature (`002` a `008`) tenga spec + plan.
2. Confirmar que dependencias entre features estén claras.

Expected:
- Proyecto listo para fase `/speckit.tasks`.

## Test Commands (Reference)

```bash
pytest backend/tests/unit
pytest backend/tests/integration
pytest backend/tests/contract
```
