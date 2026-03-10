# Contract: Frontend UI Kit Integration (Layout + Dashboard + Trading)

**Feature**: `012-cryptocurrency-ui-kit`  
**Date**: 2026-03-10

## Purpose

Definir el contrato de integracion para aplicar Cryptocurrency App UI Kit en layout autenticado, Dashboard y Trading, preservando flujos y contratos backend existentes.

## Contract Scope

- Included:
  - Reemplazo/ajuste visual de `PrivateLayout`.
  - Reemplazo/ajuste visual de `DashboardPage`.
  - Reemplazo/ajuste visual de `TradingPage`.
  - Consistencia de estados UX (`loading/empty/error/success`).
- Excluded:
  - Nuevos endpoints o cambios de payload backend.
  - Cambios de reglas de autenticacion/autorizacion.
  - Rediseno completo de Notifications y AI Agent.

## Consumer Responsibilities (Frontend)

- Mantener routing privado y guardas de sesion sin cambios funcionales.
- Renderizar componentes UI Kit con datos de APIs ya existentes.
- Preservar comportamiento de submit y manejo de errores en Trading.
- Mantener accesibilidad minima (focus visible, teclado, contraste legible).

## Provider Responsibilities (Backend)

- Mantener contratos vigentes de auth/dashboard/trading.
- Continuar validando reglas de negocio, planes y limites de trading.
- Proveer codigos y mensajes consistentes para feedback UX.

## UI State Contract

- Dashboard:
  - `LOADING`: skeleton/spinner visible.
  - `SUCCESS`: cards/resumen e historial renderizados.
  - `EMPTY`: estado vacio explicativo y no bloqueante.
  - `ERROR`: mensaje accionable + accion de retry.
- Trading:
  - `IDLE`: formulario habilitado.
  - `SUBMITTING`: bloqueo de submit y feedback de progreso.
  - `SUCCESS`: confirmacion de resultado.
  - `ERROR`: mensaje claro, preservando contexto para correccion/reintento.

## Security and Validation Constraints

- Frontend no implementa decision de limites de plan ni autorizacion de trading.
- Tokens y secretos no se imprimen ni persisten fuera de mecanismos existentes.
- Errores tecnicos sensibles no se exponen directamente al usuario final.

## Observability Contract

- Eventos minimos a registrar:
  - `ui.layout.private.rendered`
  - `ui.dashboard.state.changed`
  - `ui.trading.submit.started`
  - `ui.trading.submit.completed`
  - `ui.auth.redirect.triggered`
- Eventos deben excluir payloads sensibles y mantener nivel INFO/ERROR segun criticidad.

## Compatibility Rule

- Esta feature consume contratos backend existentes del frontend base (Sprint 011).
- Cualquier incompatibilidad de API detectada durante implementacion se deriva a feature backend separada, fuera del alcance 012.
