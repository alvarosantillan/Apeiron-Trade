# Data Model: TRDIA - AI Agent

**Feature**: `005-ai-agent`  
**Date**: 2026-03-06

## Entity: AIAgentConfig

- Purpose: Almacena configuración activa del agente IA por usuario.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `provider` (enum: OPENAI, GROQ, DEEPSEEK, GEMINI)
  - `api_key_encrypted` (text)
  - `strategy_id` (UUID, FK -> AIStrategyCatalog)
  - `risk_profile` (enum: LOW, MEDIUM, HIGH)
  - `mode` (enum: MANUAL, AUTOMATIC)
  - `is_active` (bool)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `mode=AUTOMATIC` solo permitido para planes Plus/Premium.
  - `api_key_encrypted` nunca se expone en respuestas API.
  - Un usuario solo puede tener una configuración activa.

## Entity: AIStrategyCatalog

- Purpose: Catálogo predefinido de estrategias seleccionables.
- Fields:
  - `id` (UUID)
  - `code` (string, unique)
  - `name` (string)
  - `description` (text)
  - `timeframes_supported` (jsonb)
  - `risk_levels_supported` (jsonb)
  - `is_enabled` (bool)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `code` único.
  - Estrategias deshabilitadas no pueden seleccionarse en configuración nueva.

## Entity: AIDecision

- Purpose: Registro histórico de decisiones generadas por el agente.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `config_id` (UUID, FK -> AIAgentConfig)
  - `provider` (enum)
  - `symbol` (string)
  - `timeframe` (string)
  - `action` (enum: BUY, SELL, HOLD)
  - `confidence` (decimal 0..1)
  - `risk_level` (enum)
  - `reasoning` (text)
  - `status` (enum: PENDING_APPROVAL, EXECUTED, REJECTED, FALLBACK_HOLD)
  - `fallback_reason` (text, nullable)
  - `idempotency_key` (string, unique)
  - `decision_ts` (timestamp)
  - `created_at` (timestamp)
- Validation Rules:
  - `confidence` en rango [0,1].
  - `status=FALLBACK_HOLD` requiere `fallback_reason`.
  - `idempotency_key` evita duplicados de decisión equivalentes.

## Entity: AIExecutionLink

- Purpose: Vincula decisiones del agente con ejecuciones de trading reales o simuladas.
- Fields:
  - `id` (UUID)
  - `decision_id` (UUID, FK -> AIDecision, unique)
  - `execution_id` (UUID, FK a módulo de ejecución)
  - `execution_type` (enum: PAPER, REAL)
  - `linked_at` (timestamp)
- Validation Rules:
  - Una decisión se vincula como máximo a una ejecución.

## Relationships

- `AIAgentConfig` 1..N `AIDecision`
- `AIStrategyCatalog` 1..N `AIAgentConfig`
- `AIDecision` 1..0..1 `AIExecutionLink`

## State Transitions

## AIAgentConfig Lifecycle

- `INACTIVE` -> `ACTIVE` cuando credenciales y estrategia son válidas.
- `ACTIVE` -> `INACTIVE` cuando usuario desactiva agente o plan deja de cumplir restricciones.

## AIDecision Lifecycle

- `PENDING_APPROVAL` -> `EXECUTED` (aprobación manual o auto permitida por plan)
- `PENDING_APPROVAL` -> `REJECTED` (usuario rechaza)
- `*` -> `FALLBACK_HOLD` (error proveedor/validación/timeout)
