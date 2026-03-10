# Data Model: Cryptocurrency UI Kit Integration (Iteracion 1)

**Feature**: `012-cryptocurrency-ui-kit`  
**Date**: 2026-03-10

## Entity: UIThemeContract

- Purpose: definir tokens visuales y reglas base de consistencia para layout privado y paginas en alcance.
- Fields:
  - `theme_id` (string)
  - `color_palette` (object: background, surface, primary, accent, danger, text)
  - `typography_scale` (object: display, h1, h2, body, caption)
  - `spacing_scale` (object)
  - `radius_scale` (object)
  - `shadow_profile` (object)
  - `breakpoints` (object: mobile, tablet, desktop)
- Validation Rules:
  - Debe existir contraste legible para texto principal y acciones.
  - Debe contemplar breakpoints mobile y desktop.

## Entity: AuthenticatedLayoutState

- Purpose: modelar estado visual y de navegacion del layout autenticado con UI Kit.
- Fields:
  - `auth_status` (enum: AUTHENTICATED, UNAUTHENTICATED, EXPIRED)
  - `active_route` (enum: dashboard, trading, notifications, ai-agent)
  - `navigation_state` (enum: EXPANDED, COLLAPSED)
  - `viewport_mode` (enum: MOBILE, DESKTOP)
  - `redirect_target` (string | null)
- Validation Rules:
  - `auth_status != AUTHENTICATED` implica redireccion a login para rutas privadas.
  - `active_route` debe mantenerse consistente con URL actual.

## Entity: DashboardPresentationState

- Purpose: representar la composicion visual de Dashboard sobre datos existentes.
- Fields:
  - `view_status` (enum: LOADING, SUCCESS, EMPTY, ERROR)
  - `summary_cards` (list[object])
  - `history_rows` (list[object])
  - `last_updated_at` (datetime | null)
  - `error_message` (string | null)
  - `retry_enabled` (boolean)
- Validation Rules:
  - `view_status=SUCCESS` requiere datos validados de backend.
  - `view_status=ERROR` debe mostrar feedback accionable y opcion de reintento.

## Entity: TradingPresentationState

- Purpose: representar estado visual del flujo de Trading manteniendo logica actual.
- Fields:
  - `view_status` (enum: IDLE, SUBMITTING, SUCCESS, ERROR)
  - `credentials_status` (enum: UNKNOWN, SAVING, VALID, INVALID)
  - `form_payload` (object: symbol, side, amount)
  - `submit_feedback` (string | null)
  - `backend_validation_result` (enum: PENDING, ACCEPTED, REJECTED)
  - `disable_submit` (boolean)
- Validation Rules:
  - `view_status=SUBMITTING` activa `disable_submit=true` para evitar doble envio.
  - `backend_validation_result` solo puede provenir de respuesta backend.
  - Errores no deben limpiar automaticamente el contexto del formulario.

## Entity: UIRegressionCheckpoint

- Purpose: trazar verificaciones funcionales que deben permanecer invariantes durante el rediseno.
- Fields:
  - `checkpoint_id` (string)
  - `flow` (enum: auth, private-routing, dashboard-load, trading-submit)
  - `expected_behavior` (string)
  - `test_layer` (enum: unit, integration, e2e)
  - `status` (enum: PENDING, PASS, FAIL)
- Validation Rules:
  - Debe existir al menos un checkpoint por flujo critico del alcance.
  - `status=FAIL` bloquea readiness para implementacion final.

## Relationships

- `UIThemeContract` define reglas consumidas por `AuthenticatedLayoutState`, `DashboardPresentationState` y `TradingPresentationState`.
- `AuthenticatedLayoutState.auth_status` gobierna acceso y render de `DashboardPresentationState` y `TradingPresentationState`.
- `UIRegressionCheckpoint` valida que cambios de presentacion no afecten reglas funcionales.

## State Transitions

### AuthenticatedLayoutState.auth_status

- `AUTHENTICATED` -> `EXPIRED` cuando backend/client detecta sesion invalida.
- `EXPIRED` -> `UNAUTHENTICATED` tras limpieza de sesion y redireccion.

### DashboardPresentationState.view_status

- `LOADING` -> `SUCCESS` con datos validos.
- `LOADING` -> `EMPTY` con respuesta sin contenido.
- `LOADING` -> `ERROR` con fallo de red o backend.

### TradingPresentationState.view_status

- `IDLE` -> `SUBMITTING` al enviar accion.
- `SUBMITTING` -> `SUCCESS` con respuesta exitosa.
- `SUBMITTING` -> `ERROR` con rechazo de validacion o error de red.
