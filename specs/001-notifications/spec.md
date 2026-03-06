# Feature Specification: TRDIA - Notificaciones y Alertas

**Feature Branch**: `001-notifications`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Notificaciones push por eventos críticos de trading y suscripción"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Recibir notificaciones de ejecución de trading (Priority: P1)

Como usuario, quiero recibir una notificación cada vez que una operación se ejecute o falle para tener control inmediato sobre mi cuenta.

**Why this priority**: Es un requisito funcional explícito del producto y un pilar de confianza.

**Independent Test**: Se prueba generando una ejecución exitosa y una fallida y validando la entrega de ambos push.

**Acceptance Scenarios**:

1. **Given** una operación ejecutada con éxito, **When** termina el proceso, **Then** el usuario recibe notificación push con símbolo, lado, precio y hora.
2. **Given** una operación fallida, **When** se captura el error, **Then** el usuario recibe notificación push con motivo resumido del fallo.

---

### User Story 2 - Recibir alertas de límites y plan (Priority: P2)

Como usuario, quiero enterarme cuando llego a límites de plan o cambia mi estado de suscripción para evitar bloqueos inesperados.

**Why this priority**: Reduce frustración, incrementa conversión y refuerza el modelo de monetización.

**Independent Test**: Se prueba cambiando estado de suscripción y agotando límite semanal, verificando alertas correspondientes.

**Acceptance Scenarios**:

1. **Given** un usuario Plus en 10/10 operaciones semanales, **When** intenta una nueva operación real, **Then** recibe alerta de límite alcanzado con CTA de espera o upgrade.

---

### User Story 3 - Gestionar preferencias de notificación (Priority: P3)

Como usuario, quiero configurar qué alertas recibir para evitar ruido y mantener señales importantes.

**Why this priority**: Mejora experiencia y retención, especialmente para usuarios activos.

**Independent Test**: Se prueba activando/desactivando categorías y verificando que solo se envíen las habilitadas.

**Acceptance Scenarios**:

1. **Given** notificaciones de marketing desactivadas y críticas activas, **When** ocurre ejecución de trade y evento promocional, **Then** solo se entrega la notificación crítica.

---

### User Story 4 - Trazabilidad de entregas y reintentos (Priority: P4)

Como sistema, quiero registrar estado de envío de cada notificación para auditar entregabilidad y reintentar cuando sea posible.

**Why this priority**: Necesario para soporte y confiabilidad operativa.

**Independent Test**: Se simula fallo del proveedor push y se valida política de reintento y estado final.

**Acceptance Scenarios**:

1. **Given** fallo temporal del servicio push, **When** se intenta enviar notificación crítica, **Then** el sistema reintenta según política y registra resultado final.

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- Token push del dispositivo expirado o inválido.
- Usuario con múltiples dispositivos y preferencias distintas.
- Picos de eventos (ráfagas de operaciones) en ventana corta.
- Evento repetido por reintento de webhook/exchange.
- Servicio de push temporalmente fuera de línea.
- Desfase horario entre backend y dispositivo al mostrar hora.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: El sistema MUST enviar notificaciones push por cada ejecución de operación (éxito/fallo).
- **FR-002**: El sistema MUST enviar notificaciones por bloqueos de límite semanal y estado de suscripción.
- **FR-003**: El sistema MUST soportar categorías de notificación (trading, suscripción, seguridad, sistema, marketing).
- **FR-004**: El sistema MUST permitir al usuario activar/desactivar categorías no críticas.
- **FR-005**: El sistema MUST forzar entrega de notificaciones críticas de seguridad aunque marketing esté desactivado.
- **FR-006**: El sistema MUST gestionar múltiples tokens push por usuario (multi-dispositivo).
- **FR-007**: El sistema MUST registrar estado por envío (`queued`, `sent`, `delivered`, `failed`, `dropped`).
- **FR-008**: El sistema MUST aplicar idempotencia por evento para evitar duplicados de notificación.
- **FR-009**: El sistema MUST implementar reintentos para fallos transitorios con backoff.
- **FR-010**: El sistema MUST invalidar tokens push no válidos detectados por el proveedor.
- **FR-011**: El sistema MUST permitir consulta de historial reciente de notificaciones por usuario.
- **FR-012**: El sistema MUST incluir metadatos mínimos (tipo evento, timestamp, referencia) sin filtrar datos sensibles.
- **FR-013**: El sistema MUST priorizar notificaciones críticas sobre informativas en colas de envío.
- **FR-014**: El sistema MUST notificar eventos de seguridad relevantes (nuevo dispositivo, múltiples logins fallidos, revocación de sesión).

### Key Entities *(include if feature involves data)*

- **PushDeviceToken**: token registrado por dispositivo. Campos: `user_id`, `device_id`, `platform`, `push_token`, `is_active`, `last_seen_at`.
- **NotificationPreference**: configuración por usuario/categoría. Campos: `user_id`, `category`, `enabled`, `updated_at`.
- **NotificationEvent**: evento lógico a notificar. Campos: `event_id`, `user_id`, `category`, `priority`, `title`, `message`, `reference_id`, `created_at`.
- **NotificationDelivery**: resultado de envío por dispositivo. Campos: `event_id`, `device_id`, `status`, `attempt_count`, `last_error`, `sent_at`, `delivered_at`.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 99% de notificaciones críticas se encolan en menos de 2 segundos desde el evento origen.
- **SC-002**: 95% de notificaciones de trading se entregan al menos a un dispositivo activo en menos de 10 segundos.
- **SC-003**: 100% de eventos duplicados se deduplican antes de envío (cero duplicados por evento/usuario/dispositivo).
- **SC-004**: 99% de preferencias de usuario se aplican correctamente en el siguiente envío.
- **SC-005**: 0 filtraciones de datos sensibles en payload de notificaciones.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

<!--
  ACTION REQUIRED: Document security considerations for this feature.
  All features MUST address these areas per TRDIA Constitution.
-->

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: tokens push, metadatos de eventos operativos y de seguridad.
  - **Encryption strategy**: almacenamiento protegido de tokens; mascaramiento de valores en logs.
  - **Storage**: backend only.
  - **Logging**: no exponer tokens push completos ni contenido sensible de negocio.

### Input Validation

- **Backend validation rules**: categoría permitida, usuario objetivo válido, prioridad válida, token activo, payload bajo tamaño máximo.
- **SQL injection prevention**: validación + ORM.
- **Payload limits**: límites de tamaño por mensaje y rate limiting de eventos por usuario.

### Authentication & Authorization

- **Auth required?** Sí para gestionar preferencias y tokens; envíos internos se ejecutan por servicios autorizados.
- **Roles/plans that can access**: todos los usuarios autenticados gestionan preferencias propias.
- **Plan validation**: no restringe por plan la recepción de eventos críticos.

### Audit Trail

- **What must be logged**: registro de token, cambio de preferencias, encolado de evento, envío, fallo y reintento.
- **Log level**: INFO/WARNING/ERROR.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

<!--
  ACTION REQUIRED: If this feature involves trading operations or subscription validation,
  document the backend validation strategy per Constitution Principle V.
-->

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** No, pero consume eventos provenientes de módulos que sí validan plan.
  
- **Does this feature execute real monetary operations?** No.

- **Capital limits**: N/A.

### Frontend Behavior

- **Frontend role**: registrar token push, configurar preferencias y mostrar historial.
- **How frontend gets validation state**: endpoints de preferencias/historial y eventos recibidos en push.

## Observability *(mandatory - Constitution Principle VI)*

<!--
  ACTION REQUIRED: Define metrics and monitoring for this feature.
-->

### Metrics

- **notifications.event.created_total**: Counter - Eventos de notificación creados.
- **notifications.queue.latency_seconds**: Histogram - Tiempo de encolado.
- **notifications.sent_total**: Counter - Notificaciones enviadas.
- **notifications.failed_total**: Counter - Notificaciones fallidas.
- **notifications.retry_total**: Counter - Reintentos ejecutados.
- **notifications.delivery.success_ratio**: Gauge - Tasa de entrega exitosa.

### Alerts

- **Alert 1**: `notifications.failed_total` > 5% de envíos en 10 minutos.
- **Alert 2**: `notifications.queue.latency_seconds` p95 > 5 segundos en 15 minutos.

### Logging

- **Key events to log**: token_registered, preference_updated, event_created, event_deduplicated, notification_sent, notification_failed, token_invalidated.
- **Log level**: INFO para flujo normal, WARNING para degradaciones, ERROR para fallos no recuperables.
