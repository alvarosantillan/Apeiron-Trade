# Research - 004-subscriptions

## Decision 1: Plan Provisioning at Startup

- Decision: Crear/sincronizar planes de MercadoPago al inicio del backend usando `plan_code` como clave idempotente.
- Rationale: Evita intervención manual y garantiza consistencia entre entornos.
- Alternatives considered:
  - Configuración manual en panel: rechazada por riesgo de drift y errores operativos.

## Decision 2: Webhook Trust Model

- Decision: Aceptar webhooks solo con firma válida y deduplicación por `provider_event_id`.
- Rationale: Previene fraude, replay y actualizaciones duplicadas.
- Alternatives considered:
  - Validar solo origen IP: rechazado por menor robustez.

## Decision 3: Subscription State as Source of Truth

- Decision: Backend mantiene estado interno de suscripción y lo usa para autorizar operaciones.
- Rationale: Frontend y redirecciones no son confiables para lógica de negocio.
- Alternatives considered:
  - Confiar en estado de frontend tras checkout: rechazado por bypass potencial.

## Decision 4: Upgrade/Downgrade Timing

- Decision: Upgrade aplica inmediatamente al confirmar pago; downgrade y cancelación pueden aplicarse al cierre de período.
- Rationale: Balancea UX y consistencia financiera.
- Alternatives considered:
  - Todos los cambios inmediatos: rechazado por riesgo de inconsistencias de facturación.

## Decision 5: Reconciliation Job

- Decision: Job periódico de reconciliación para alinear estados locales con proveedor ante fallos transitorios.
- Rationale: Aumenta resiliencia y reduce desalineación de estado.
