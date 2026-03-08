# Research: TRDIA - System Design Foundation

**Feature**: `001-system-design`  
**Date**: 2026-03-07  
**Spec**: `specs/001-system-design/spec.md`

## Decision 1: Modular Monolith as MVP Core

- Decision: Iniciar con monolito modular en backend (módulos por dominio), evitando microservicios tempranos.
- Rationale: Reduce complejidad operativa y acelera entrega de valor en MVP.
- Alternatives considered:
  - Microservicios desde inicio: descartado por sobrecosto de coordinación/infra.

## Decision 2: Backend as Single Source of Truth

- Decision: Toda validación crítica de plan, riesgo y ejecución reside exclusivamente en backend.
- Rationale: Evita bypass y asegura consistencia regulatoria/operativa.
- Alternatives considered:
  - Reglas compartidas frontend/backend: descartado por riesgo de divergencia.

## Decision 3: Event-Driven Async for Non-Blocking Operations

- Decision: Usar workers para tareas asíncronas (ejecución, notificaciones, webhooks, reconciliaciones).
- Rationale: Mejora resiliencia y latencia percibida en API.
- Alternatives considered:
  - Todo síncrono en API: descartado por bloqueo y fragilidad.

## Decision 4: Security Baseline from Day 1

- Decision: Cifrado de secrets en repositorio de credenciales + política de logs sanitizados + auditoría estructurada.
- Rationale: Datos financieros y llaves de terceros exigen hardening temprano.
- Alternatives considered:
  - Hardening posterior: descartado por riesgo y retrabajo.

## Decision 5: Domain Contracts Before Implementation

- Decision: Definir contratos API/DTO y fronteras de dominio antes de codificar flows.
- Rationale: Reduce ambigüedad y facilita TDD/contract testing.
- Alternatives considered:
  - Contratos emergentes durante desarrollo: descartado por cambios costosos.

## Decision 6: Observability as Product Capability

- Decision: Métricas, trazas y alertas se definen por feature y se agregan a baseline de plataforma.
- Rationale: Permite detectar fallos de trading/pagos con baja latencia operativa.
- Alternatives considered:
  - Logging básico sin métricas: descartado por poca visibilidad.

## Decision 7: Progressive Scope Control

- Decision: Mantener v1 acotado a Binance Spot, planes definidos y catálogo de estrategias predefinidas.
- Rationale: Entrega controlada y menos riesgo de dispersión.
- Alternatives considered:
  - Multi-exchange/multi-activos desde inicio: descartado por complejidad temprana.
