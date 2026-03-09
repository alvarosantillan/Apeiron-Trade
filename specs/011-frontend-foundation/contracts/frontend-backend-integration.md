# Contract: Frontend-Backend Integration for MVP Foundation

**Feature**: `011-frontend-foundation`  
**Date**: 2026-03-09

## Purpose

Definir el contrato funcional entre la UI MVP y endpoints backend ya existentes para auth, dashboard/history, trading, notifications y ai-agent, sin introducir interfaces nuevas en Sprint 011.

## Contract Scope

- Included:
  - Login/logout y verificacion de sesion activa.
  - Lectura de datos base de dashboard/historial.
  - Guardado de credenciales trading y envio de orden.
  - Registro de dispositivo y emision de notificacion.
  - Lectura/actualizacion de configuracion de AI Agent.
- Excluded:
  - Nuevos endpoints backend.
  - Cambios de reglas de negocio de planes, limites o ejecucion.

## Consumer Responsibilities (Frontend)

- Enviar payloads con formato y limites definidos por backend.
- Mostrar estados de carga, vacio, error y exito por flujo.
- Redirigir a autenticacion ante sesion invalida/expirada.
- No persistir secretos completos ni exponerlos en logs de cliente.

## Provider Responsibilities (Backend)

- Mantener validacion de autenticacion/autorizacion y limites de plan.
- Devolver codigos de estado y mensajes consistentes para UX accionable.
- Mantener proteccion de datos sensibles en respuestas y logs.

## Response Handling Contract

- Success (2xx):
  - Frontend actualiza estado a `READY/SUCCESS/SAVED/SENT` segun flujo.
- User/Domain error (4xx):
  - Frontend muestra mensaje accionable y conserva contexto para reintento.
- Auth/session error (401/403):
  - Frontend invalida sesion local y redirige a login si aplica.
- Server/transient error (5xx/network):
  - Frontend muestra error recuperable con opcion de retry.

## Security and Validation Constraints

- Frontend no decide habilitacion de operaciones de trading por plan.
- Backend sigue siendo autoridad para plan limits, capital limits y validaciones pre-ejecucion.
- Datos sensibles (tokens, API keys, secretos) nunca se exponen en logs UI.

## Observability Contract

- Eventos minimos a registrar en cliente:
  - `auth.login.success|failure`
  - `trading.order.submit.success|failure`
  - `notifications.emit.success|failure`
  - `ai_agent.config.save.success|failure`
- Los eventos deben excluir payloads sensibles.

## Compatibility Rule

- Sprint 011 consume contratos backend vigentes (features `002` a `010`) y no define versionado nuevo.
- Cualquier incompatibilidad detectada durante implementacion se deriva a feature backend separada, fuera de este sprint.
