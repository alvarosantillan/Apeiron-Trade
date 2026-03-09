# Data Model: Frontend Foundation MVP

**Feature**: `011-frontend-foundation`  
**Date**: 2026-03-09

## Entity: UserSessionViewState

- Purpose: Representar estado de autenticacion y acceso a vistas privadas.
- Fields:
  - `status` (enum: UNAUTHENTICATED, AUTHENTICATING, AUTHENTICATED, EXPIRED)
  - `user_id` (string | null)
  - `access_scope` (list[string])
  - `last_auth_at` (datetime | null)
  - `session_error_code` (string | null)
  - `session_error_message` (string | null)
- Validation Rules:
  - `status=AUTHENTICATED` requiere `user_id` no nulo.
  - `status=EXPIRED` obliga redireccion a login en rutas privadas.
  - Mensajes de error no deben exponer tokens ni payloads sensibles.

## Entity: DashboardSummaryViewState

- Purpose: Consolidar estado visual de dashboard para metricas e historial base.
- Fields:
  - `status` (enum: IDLE, LOADING, READY, EMPTY, ERROR)
  - `metrics` (list[object])
  - `recent_operations` (list[object])
  - `last_refresh_at` (datetime | null)
  - `error_message` (string | null)
- Validation Rules:
  - `status=READY` requiere al menos una fuente de datos evaluada.
  - `status=EMPTY` no se considera error funcional.
  - `error_message` debe ser accionable y no tecnico.

## Entity: TradingFlowViewState

- Purpose: Gestionar captura de credenciales de trading, envio de orden y respuesta de ejecucion.
- Fields:
  - `credentials_status` (enum: UNKNOWN, SAVING, VALID, INVALID)
  - `order_form` (object: symbol, side, amount, order_type)
  - `submission_status` (enum: IDLE, SUBMITTING, SUCCESS, FAILURE)
  - `backend_validation_status` (enum: PENDING, APPROVED, REJECTED)
  - `execution_result` (object | null)
  - `error_message` (string | null)
- Validation Rules:
  - Envio bloqueado mientras `submission_status=SUBMITTING` para prevenir doble submit.
  - `backend_validation_status` siempre proviene de respuesta backend.
  - Errores de limites/plan deben mostrarse sin intentar bypass local.

## Entity: NotificationFlowViewState

- Purpose: Controlar registro de dispositivo y emision de notificaciones desde UI.
- Fields:
  - `device_registration_status` (enum: IDLE, REGISTERING, REGISTERED, FAILED)
  - `registered_device_id` (string | null)
  - `emit_status` (enum: IDLE, SENDING, SENT, FAILED)
  - `last_emit_at` (datetime | null)
  - `error_message` (string | null)
- Validation Rules:
  - Emision requiere `registered_device_id` valido.
  - Si backend indica sin dispositivos activos, UI muestra estado recuperable.

## Entity: AIAgentConfigViewState

- Purpose: Gestionar lectura/edicion de configuracion de AI Agent.
- Fields:
  - `load_status` (enum: IDLE, LOADING, READY, ERROR)
  - `save_status` (enum: IDLE, SAVING, SAVED, ERROR)
  - `config_payload` (object)
  - `validation_issues` (list[string])
  - `last_saved_at` (datetime | null)
  - `error_message` (string | null)
- Validation Rules:
  - Guardado solo permitido con validaciones de formulario basicas aprobadas.
  - Backend mantiene validacion final de reglas de negocio.

## Relationships

- `UserSessionViewState` gobierna acceso a `DashboardSummaryViewState`, `TradingFlowViewState`, `NotificationFlowViewState` y `AIAgentConfigViewState`.
- `TradingFlowViewState.backend_validation_status` depende de validacion backend de planes y limites.
- Todos los ViewState exponen contrato comun de estado (`LOADING/ERROR/EMPTY/SUCCESS`) para FR-009.

## State Transitions

### UserSessionViewState.status

- `UNAUTHENTICATED` -> `AUTHENTICATING` -> `AUTHENTICATED` en login exitoso.
- `AUTHENTICATED` -> `EXPIRED` cuando backend devuelve sesion invalida/expirada.
- `EXPIRED` -> `UNAUTHENTICATED` tras limpiar contexto y redirigir.

### TradingFlowViewState.submission_status

- `IDLE` -> `SUBMITTING` al enviar orden.
- `SUBMITTING` -> `SUCCESS` si backend acepta y ejecuta.
- `SUBMITTING` -> `FAILURE` con mensaje accionable y opcion de reintento.

### NotificationFlowViewState.emit_status

- `IDLE` -> `SENDING` -> `SENT` en emision exitosa.
- `SENDING` -> `FAILED` si no hay dispositivo activo o error de red.

### AIAgentConfigViewState.save_status

- `IDLE` -> `SAVING` -> `SAVED` en persistencia exitosa.
- `SAVING` -> `ERROR` ante rechazo backend o falla de red.
