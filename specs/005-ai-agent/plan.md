# Implementation Plan: TRDIA - AI Agent

**Branch**: `005-ai-agent` | **Date**: 2026-03-06 | **Spec**: `specs/005-ai-agent/spec.md`
**Input**: Feature specification from `/specs/005-ai-agent/spec.md`

## Summary

Implementar el módulo de agente IA multi-proveedor para análisis de mercado y generación de decisiones operativas estructuradas, con configuración por usuario (proveedor, estrategia y riesgo), comportamiento por plan (Free manual, Plus/Premium manual o automático), trazabilidad y degradación segura ante fallos.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, SDKs OpenAI/Groq/DeepSeek/Gemini, Celery, Redis  
**Storage**: PostgreSQL externa (`ai_agent_config`, `ai_strategy_catalog`, `ai_decisions`, `ai_execution_links`)  
**Testing**: pytest, pytest-asyncio, httpx, provider mocks, pytest-cov  
**Target Platform**: Backend API Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend-centric)  
**Performance Goals**: ciclo de decisión p95 < 5s, activación de configuración p95 < 20s  
**Constraints**: no exponer API keys de proveedores, fallback a HOLD ante incertidumbre/fallo, historial obligatorio de decisiones  
**Scale/Scope**: v1 con 4 proveedores soportados y catálogo predefinido de estrategias

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec completa antes de implementación
- [x] **Principle II (TDD)**: plan de pruebas definido (contract/integration/unit)
- [x] **Principle III (Security-First)**:
  - [x] credenciales IA no se exponen en código/logs
  - [x] validación de entradas definida
  - [x] cifrado de API keys documentado
  - [x] auditoría de cambios/decisiones definida
- [x] **Principle IV (Modular)**: Encaja en `agents/`, `strategies/`, `api/`, `workers/`
- [x] **Principle V (Validation-Strict)**:
  - [x] validación backend de elegibilidad por plan/modo
  - [x] enforcement Free vs Plus/Premium documentado
  - [x] frontend no decide reglas de negocio
- [x] **Principle VI (Observability)**: métricas y alertas del agente definidas
- [x] **Principle VII (Progressive Enhancement)**: alcance acotado a catálogo predefinido y providers definidos

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-agent/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ai-agent.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── ai_agent/
│   ├── services/
│   │   ├── ai_agent/
│   │   └── ai_providers/
│   ├── models/
│   ├── schemas/
│   └── workers/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
└── src/
    └── screens/
        └── bot_config/
```

**Structure Decision**: módulo de agente implementado en backend con interfaces de proveedor desacopladas; frontend solo configura y consume estados/resultados.

## Phase Plan

### Phase 0 - Research Decisions

1. Estandarizar contrato de salida de decisiones entre proveedores heterogéneos
2. Definir política de fallback/degradación a HOLD
3. Definir control anti-duplicado de señales en ventana temporal
4. Definir estrategia de composición segura del system prompt por estrategia

### Phase 1 - Design Artifacts

1. `data-model.md` con configuración, catálogo de estrategias y decisiones
2. `contracts/ai-agent.openapi.yaml` para endpoints de config, estado y decisiones
3. `quickstart.md` para validar activación, ciclo de decisión y modos por plan

### Phase 2 - Implementation Ready

Para `/speckit.tasks`:
- tareas por US1-US4
- tests-first obligatorios
- secuencia: config + providers -> decisión -> reglas por plan -> trazabilidad/notificaciones

## Testing Strategy (TDD Gate)

1. Contract tests para endpoints de configuración y consulta de decisiones
2. Integration tests con mocks de providers (respuesta válida, timeout, respuesta inválida)
3. Unit tests para composición de prompt, parser de salida estructurada y reglas de modo por plan
4. Coverage gate:
   - módulo ai-agent >= 90%
   - global backend >= 80%

## Risks & Mitigations

- Riesgo: respuestas no estructuradas entre proveedores
  - Mitigación: contrato normalizado + validación estricta + fallback a HOLD
- Riesgo: decisiones repetitivas/ruido
  - Mitigación: ventana anti-duplicado y threshold de confianza
- Riesgo: fuga de prompts con secretos
  - Mitigación: sanitización y segregación de secretos fuera del prompt persistido

## Complexity Tracking

No constitutional violations detected.
