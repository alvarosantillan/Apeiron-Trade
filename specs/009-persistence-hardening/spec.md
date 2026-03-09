# Feature Specification: TRDIA - Persistence and Hardening Baseline

**Feature Branch**: `009-persistence-hardening`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "Migrar persistencia in-memory a PostgreSQL y hardening para entorno productivo en TRDIA"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistencia real de datos críticos (Priority: P1)

Como operador de la plataforma, quiero que autenticación, ejecuciones, notificaciones y configuración de agente persistan en PostgreSQL para no perder estado al reiniciar el backend.

**Why this priority**: Sin persistencia durable, no hay confiabilidad operativa ni trazabilidad mínima para pruebas serias.

**Independent Test**: Reiniciar backend y validar que usuarios, sesiones, ejecuciones y preferencias siguen disponibles.

**Acceptance Scenarios**:

1. **Given** un usuario registrado con operaciones y notificaciones, **When** se reinicia el backend, **Then** los datos siguen consultables sin pérdida.
2. **Given** una ejecución creada antes de reinicio, **When** se consulta historial y detalle, **Then** el registro aparece con el mismo estado y metadatos.

---

### User Story 2 - Configuración clara para DB host y contenedor (Priority: P2)

Como desarrollador, quiero configurar PostgreSQL de host o contenedor con pasos explícitos para levantar entorno reproducible de pruebas.

**Why this priority**: Reduce errores de onboarding y evita drift entre entornos locales.

**Independent Test**: Configurar conexión en entorno limpio y ejecutar smoke test de API y test suite.

**Acceptance Scenarios**:

1. **Given** un entorno nuevo, **When** se siguen pasos documentados de conexión DB, **Then** la API inicia correctamente con migraciones aplicadas.
2. **Given** PostgreSQL del host, **When** se usa `host.docker.internal` desde contenedor, **Then** la app conecta y ejecuta operaciones CRUD básicas.

---

### User Story 3 - Hardening operativo mínimo para pre-producción (Priority: P3)

Como responsable técnico, quiero controles mínimos de hardening (migraciones, validaciones, auditoría y manejo de fallos) para ejecutar pruebas integrales con mayor confianza.

**Why this priority**: Permite validar negocio con menos riesgo de inconsistencias y fallos silenciosos.

**Independent Test**: Ejecutar suite completa y pruebas de fallos de conexión/transientes verificando comportamiento controlado.

**Acceptance Scenarios**:

1. **Given** un error transitorio de base de datos, **When** el servicio procesa solicitud, **Then** responde con error controlado y evento auditado.
2. **Given** una migración pendiente, **When** inicia el backend, **Then** existe procedimiento claro para aplicar cambios sin corrupción de datos.

### Edge Cases

- Base de datos inaccesible durante arranque.
- Reinicio en mitad de operación de trading.
- Datos parcialmente escritos por fallo de red.
- Cambio de esquema sin migración aplicada.
- Conexión apuntando a DB equivocada (dev vs test).
- Alto volumen de lecturas de historial con paginación profunda.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (P1)**: El sistema MUST persistir en PostgreSQL usuarios, sesiones de auth, configuraciones de agente IA, ejecuciones de trading y notificaciones.
- **FR-002 (P1)**: El sistema MUST reemplazar stores in-memory de producción por repositorios persistentes con equivalencia funcional.
- **FR-003 (P1)**: El sistema MUST conservar compatibilidad de contratos API actuales durante la migración.
- **FR-004 (P1)**: El sistema MUST incluir mecanismo de migraciones versionadas para esquema de base de datos.
- **FR-005 (P1)**: El sistema MUST permitir configuración de conexión a PostgreSQL por variables de entorno documentadas.
- **FR-006 (P2)**: El sistema MUST soportar conexión desde contenedor a PostgreSQL del host para desarrollo local.
- **FR-007 (P2)**: El sistema MUST mantener idempotencia de ejecuciones y eventos al persistir en base de datos.
- **FR-008 (P2)**: El sistema MUST registrar auditoría de operaciones críticas de lectura/escritura relevantes.
- **FR-009 (P2)**: El sistema MUST devolver errores controlados y trazables ante fallos de conexión o transacciones.
- **FR-010 (P1)**: El sistema MUST incluir smoke tests reproducibles para validar flujo básico con DB real.
- **FR-011 (P3)**: El sistema MUST definir explícitamente exclusiones de esta iteración para evitar expansión de alcance durante ejecución.

### Key Entities *(include if feature involves data)*

- **UserAccount**: identidad de usuario y credenciales hash. Campos clave: `id`, `email`, `password_hash`, `created_at`.
- **AuthSession**: sesiones activas y refresh tokens. Campos clave: `user_id`, `refresh_token_id`, `expires_at`, `revoked_at`.
- **TradingExecution**: ejecución persistida con estado y trazabilidad. Campos clave: `id`, `request_id`, `status`, `execution_type`, `created_at`, `updated_at`.
- **NotificationDelivery**: historial de notificaciones y estado final. Campos clave: `event_id`, `category`, `priority`, `status`, `created_at`.
- **AIAgentConfig**: configuración activa de agente por usuario. Campos clave: `user_id`, `provider`, `strategy_id`, `mode`, `is_active`, `updated_at`.

## Assumptions & Dependencies

- Se conserva el comportamiento funcional actual de features `002` a `008` durante la migración.
- Existe una instancia PostgreSQL accesible para entorno de desarrollo/pruebas.
- La migración de datos históricos previos en memoria se limita a lo estrictamente necesario para continuidad operativa en entorno de pruebas.
- Los consumidores actuales de API no cambian contratos ni secuencia de llamadas.

## Sprint Scope (Closed)

### In Scope (Sprint 009)

- Persistencia PostgreSQL para dominios críticos ya activos: auth, trading execution, notifications y AI agent config.
- Migraciones versionadas del esquema necesarias para esos dominios.
- Manejo de errores de conexión/transacción con respuesta controlada y auditada.
- Compatibilidad funcional de contratos existentes para no romper consumidores actuales.
- Configuración documentada para PostgreSQL en host y contenedor para entorno de pruebas.
- Smoke tests y pruebas de regresión funcional centradas en persistencia y continuidad operativa.

### Out of Scope (Future Feature)

- Rediseño completo de modelo de datos para analytics avanzados.
- Replicación multi-zona, alta disponibilidad y failover automático.
- Estrategia formal de backup/restore con RPO/RTO de producción.
- Optimización avanzada de performance a gran escala.
- Refactor masivo de contratos API o rediseño de endpoints.
- Cambios de producto fuera de persistencia/hardening baseline.

### Delivery Boundary

- Esta feature se considera completada cuando la plataforma mantiene estado tras reinicios, conserva contratos y opera con DB real en pruebas sin degradar reglas de negocio existentes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% de datos críticos creados antes de reinicio permanecen disponibles después del reinicio.
- **SC-002**: 95% de operaciones CRUD críticas responden en menos de 300 ms en entorno local de pruebas.
- **SC-003**: 100% de endpoints existentes mantienen compatibilidad funcional verificable por suite de contratos.
- **SC-004**: 100% de despliegues de entorno de pruebas aplican migraciones sin intervención manual ad hoc.
- **SC-005**: 0 pérdidas de idempotencia observadas en pruebas de reintento de ejecuciones/eventos.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: credenciales hash, refresh tokens, configuraciones de agente, historial de trading/notificaciones.
  - **Encryption strategy**: secretos en variables de entorno; cifrado/aplicación de hash donde corresponda para datos sensibles.
  - **Storage**: backend y base de datos controlada; nunca exponer secretos completos en API.
  - **Logging**: prohibido loggear passwords, refresh tokens completos o credenciales de proveedores.

### Input Validation

- **Backend validation rules**: validar tipos/rangos en payloads, parámetros de filtros y estados permitidos antes de persistir.
- **SQL injection prevention**: acceso a DB mediante capa de repositorio con consultas parametrizadas/ORM.
- **Payload limits**: límites de tamaño de payload y paginación para evitar abuso.

### Authentication & Authorization

- **Auth required?** Yes para endpoints de usuario.
- **Roles/plans that can access**: usuarios autenticados acceden solo a sus propios datos operativos.
- **Plan validation**: mantener enforcement de límites por plan en backend, ahora persistido.

### Audit Trail

- **What must be logged**: fallos de conexión DB, errores de transacción, accesos de detalle trade, cambios de config crítica.
- **Log level**: INFO para flujo normal, WARNING para degradación, ERROR para fallos persistentes.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** Yes.
  - Persistir y validar consistentemente `operations_used < plan_limit` antes de ejecución real.

- **Does this feature execute real monetary operations?** Indirectamente, al persistir flujo de ejecución.
  - Mantener checks previos existentes (credenciales activas, balance, riesgo, idempotencia) sin degradación.

- **Capital limits**: respetar reglas ya definidas por plan durante y después de la migración de persistencia.

### Frontend Behavior

- **Frontend role**: consumo y visualización; no aplica reglas de persistencia ni de límites de negocio.
- **How frontend gets validation state**: endpoints existentes (`dashboard`, `history`, `trading`) con estado calculado en backend persistente.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **db.connection.errors_total**: Counter - errores de conexión a base de datos.
- **db.query.latency_seconds**: Histogram - latencia de operaciones críticas de repositorio.
- **persistence.migration.success_total**: Counter - migraciones aplicadas con éxito.
- **persistence.migration.failure_total**: Counter - migraciones fallidas.
- **api.compatibility.regression_total**: Counter - regresiones detectadas en pruebas de contrato tras migración.

### Alerts

- **Alert 1**: `db.connection.errors_total` > 0 continuo durante 5 minutos.
- **Alert 2**: `persistence.migration.failure_total` > 0 en cualquier despliegue.

### Logging

- **Key events to log**: db_connected, db_connection_failed, migration_started, migration_completed, migration_failed, repository_write_failed.
- **Log level**: INFO/WARNING/ERROR según severidad.
