# Feature Specification: TRDIA - Suscripciones y Pagos (MercadoPago)

**Feature Branch**: `004-subscriptions`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Planes Free/Plus/Premium con cobro recurrente por MercadoPago"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Usuario Free se suscribe a Plus o Premium (Priority: P1)

Como usuario Free, quiero suscribirme a un plan de pago para desbloquear mas operaciones semanales y modo automatico.

**Why this priority**: Es el flujo principal de monetizacion del producto y habilita funcionalidades premium.

**Independent Test**: Se puede probar con sandbox de MercadoPago validando creacion de checkout, pago aprobado y actualizacion de plan por webhook.

**Acceptance Scenarios**:

1. **Given** un usuario Free autenticado, **When** elige plan Plus y completa pago aprobado en MercadoPago, **Then** su plan cambia a Plus y se habilitan 10 operaciones semanales.
2. **Given** un usuario Free autenticado, **When** elige plan Premium y el pago es aprobado, **Then** su plan cambia a Premium con operaciones ilimitadas.
3. **Given** un pago rechazado, **When** el usuario vuelve a la app, **Then** conserva plan Free y ve estado de pago fallido con opcion de reintento.

---

### User Story 2 - Usuario gestiona ciclo de vida de suscripcion (Priority: P2)

Como usuario con plan de pago, quiero hacer upgrade, downgrade o cancelacion para adaptar mi suscripcion sin perder control.

**Why this priority**: Reduce churn y mejora experiencia de cliente en pagos recurrentes.

**Independent Test**: Se prueba de forma aislada con transiciones de estado de suscripcion y verificando efecto de cada cambio en limites del plan.

**Acceptance Scenarios**:

1. **Given** usuario Plus activo, **When** hace upgrade a Premium, **Then** el sistema actualiza plan inmediatamente tras confirmacion de pago.
2. **Given** usuario Premium activo, **When** solicita downgrade a Plus, **Then** el cambio queda programado para el siguiente ciclo de facturacion.
3. **Given** usuario Plus activo, **When** cancela suscripcion, **Then** mantiene beneficios hasta fin de periodo y luego pasa a Free.

---

### User Story 3 - Backend valida plan antes de operar (Priority: P3)

Como sistema, quiero validar siempre el estado real de suscripcion en backend para evitar bypass de limites y garantizar consistencia de negocio.

**Why this priority**: Protege ingresos y garantiza enforcement correcto del modelo Free/Plus/Premium.

**Independent Test**: Se prueba con usuarios en distintos estados de suscripcion intentando ejecutar operaciones y verificando bloqueos/permisos.

**Acceptance Scenarios**:

1. **Given** usuario con suscripcion vencida `past_due`, **When** intenta operacion premium, **Then** backend bloquea y devuelve motivo de suscripcion no valida.
2. **Given** usuario Plus con 10 operaciones usadas, **When** intenta nueva operacion real, **Then** backend bloquea por limite semanal.
3. **Given** usuario Premium activo, **When** ejecuta operaciones reales, **Then** no se aplica limite semanal de cantidad.

---

### User Story 4 - Administrador parametriza MercadoPago sin tocar codigo (Priority: P4)

Como administrador, quiero configurar credenciales y planes de MercadoPago via entorno para operar en dev/staging/prod sin cambios manuales en codigo.

**Why this priority**: Facilita operacion segura y despliegues repetibles.

**Independent Test**: Puede validarse levantando backend con variables de entorno y verificando creacion idempotente de planes al iniciar.

**Acceptance Scenarios**:

1. **Given** backend inicia con credenciales MercadoPago validas, **When** arranca modulo de pagos, **Then** crea o sincroniza planes Free/Plus/Premium automaticamente sin duplicados.
2. **Given** webhook firmado validamente, **When** llega evento de pago/suscripcion, **Then** backend actualiza estado interno correspondiente.
3. **Given** webhook con firma invalida, **When** se procesa, **Then** es rechazado y auditado.

---

### Edge Cases

- Webhook duplicado de MercadoPago para el mismo pago.
- Webhook llega antes que redireccion del usuario a la app.
- Pago aprobado parcialmente o en moneda distinta a la esperada.
- Renovacion automatica falla por tarjeta vencida.
- Cambio de plan en mitad de ciclo de facturacion.
- Desfase horario entre proveedor de pago y backend.
- Backend reinicia durante procesamiento de webhook.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST mantener tres planes: `free`, `plus`, `premium` con limites y precios definidos por negocio.
- **FR-002**: El sistema MUST crear/sincronizar automaticamente planes de MercadoPago al iniciar backend de forma idempotente.
- **FR-003**: El sistema MUST exponer endpoint para iniciar checkout de suscripcion para Plus y Premium.
- **FR-004**: El sistema MUST recibir y procesar webhooks de MercadoPago para pagos y cambios de suscripcion.
- **FR-005**: El sistema MUST validar firma/autenticidad de cada webhook antes de procesarlo.
- **FR-006**: El sistema MUST actualizar estado interno de suscripcion en base a eventos de pago aprobados/rechazados/pending.
- **FR-007**: El sistema MUST soportar upgrade inmediato de plan tras confirmacion de pago.
- **FR-008**: El sistema MUST soportar downgrade con aplicacion al siguiente ciclo de facturacion.
- **FR-009**: El sistema MUST soportar cancelacion de suscripcion conservando beneficios hasta fin de periodo pagado.
- **FR-010**: El sistema MUST validar en backend el plan activo antes de cada operacion real.
- **FR-011**: El sistema MUST aplicar limites semanales por plan (Free=1, Plus=10, Premium=ilimitado).
- **FR-012**: El sistema MUST resetear contador semanal automaticamente cada lunes 00:00 UTC.
- **FR-013**: El sistema MUST bloquear ejecuciones reales cuando limite o estado de suscripcion no lo permita.
- **FR-014**: El sistema MUST registrar historial de pagos y cambios de plan por usuario.
- **FR-015**: El sistema MUST notificar al usuario cambios de estado relevantes (pago aprobado, rechazado, renovacion fallida, cancelacion efectiva).
- **FR-016**: El sistema MUST permitir consultar estado actual de suscripcion y proxima fecha de cobro.
- **FR-017**: El sistema MUST manejar webhooks duplicados con idempotencia (sin duplicar cobros/estados).
- **FR-018**: El sistema MUST permitir operar en modo sandbox y produccion segun configuracion de entorno.

### Key Entities *(include if feature involves data)*

- **PlanCatalog**: Definicion de planes de negocio. Campos: `plan_code`, `display_name`, `weekly_limit`, `monthly_price`, `currency`, `is_active`.
- **Subscription**: Estado contractual del usuario. Campos: `user_id`, `plan_code`, `status`, `provider_subscription_id`, `current_period_start`, `current_period_end`, `next_billing_date`, `cancel_at_period_end`.
- **PaymentRecord**: Registro de transacciones de cobro. Campos: `user_id`, `subscription_id`, `provider_payment_id`, `amount`, `currency`, `status`, `paid_at`, `raw_event_id`.
- **WebhookEvent**: Evento entrante de proveedor. Campos: `provider_event_id`, `event_type`, `signature_valid`, `processed_at`, `processing_status`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% de upgrades Free->Plus/Premium se reflejan en perfil del usuario en menos de 15 segundos tras pago aprobado.
- **SC-002**: 100% de webhooks validos se procesan una sola vez (sin efectos duplicados).
- **SC-003**: 100% de intentos de trading respetan estado real de suscripcion y limites por plan.
- **SC-004**: 99% de eventos de cobro quedan registrados en historial de pagos en menos de 10 segundos.
- **SC-005**: 0 casos de plan premium activo sin pago aprobado asociado.
- **SC-006**: 0 exposiciones de secretos de MercadoPago en logs o respuestas API.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: tokens de MercadoPago, estado de pagos, metadatos de facturacion.
  - **Encryption strategy**: secretos de proveedor en variables de entorno seguras; identificadores sensibles protegidos en almacenamiento.
  - **Storage**: Backend only; frontend no accede a secretos ni firmas.
  - **Logging**: nunca loggear access token completo ni payload sensible sin sanitizar.

### Input Validation

- **Backend validation rules**: validacion de payload webhook, tipos de evento permitidos, estado de pago esperado, monto y moneda.
- **SQL injection prevention**: ORM + validacion de esquemas.
- **Payload limits**: limite de tamano de webhook y de requests de checkout; rate limiting en endpoints de suscripcion.

### Authentication & Authorization

- **Auth required?** Yes para endpoints de usuario; No para webhook pero con verificacion de firma estricta.
- **Roles/plans that can access**: usuarios autenticados gestionan su propia suscripcion; solo backend/proveedor cambia estado por webhook.
- **Plan validation**: enforcement en backend antes de operacion real.

### Audit Trail

- **What must be logged**: inicio de checkout, cambio de plan, pago aprobado/rechazado, webhook recibido/rechazado, renovaciones y cancelaciones.
- **Log level**: INFO (flujo), WARNING (inconsistencias/duplicados), ERROR (fallos de procesamiento).
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** Yes
  - Validar `subscription.status` y `weekly_limit` antes de permitir operaciones reales.

- **Does this feature execute real monetary operations?** Yes
  - Validar firma webhook, estado de pago aprobado y consistencia de monto/plan antes de activar beneficios.

- **Capital limits**: No define capital por operacion directamente; delega enforcement de capital al modulo de trading, pero define habilitacion por plan.

### Frontend Behavior

- **Frontend role**: iniciar checkout y mostrar estado; no confirma pagos por si mismo.
- **How frontend gets validation state**: endpoint de `subscription/status` provisto por backend.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **subscriptions.checkout_started_total**: Counter - Checkouts iniciados.
- **subscriptions.upgrade_success_total**: Counter - Upgrades exitosos.
- **subscriptions.downgrade_scheduled_total**: Counter - Downgrades programados.
- **payments.webhook.received_total**: Counter - Webhooks recibidos.
- **payments.webhook.processed_total**: Counter - Webhooks procesados con exito.
- **payments.webhook.rejected_total**: Counter - Webhooks rechazados.
- **subscriptions.validation_block_total**: Counter - Bloqueos por suscripcion invalida.

### Alerts

- **Alert 1**: tasa de `payments.webhook.rejected_total` > 5% en 10 minutos.
- **Alert 2**: incremento de `subscriptions.validation_block_total` > 3x baseline en 30 minutos.

### Logging

- **Key events to log**: checkout_created, webhook_received, webhook_validated, plan_updated, payment_recorded, subscription_blocked.
- **Log level**: INFO para eventos esperados; WARNING para anomalías; ERROR para fallos internos.

