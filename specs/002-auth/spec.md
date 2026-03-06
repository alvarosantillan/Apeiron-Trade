# Feature Specification: TRDIA - Autenticacion y Usuarios

**Feature Branch**: `002-auth`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Especificacion de autenticacion y usuarios para TRDIA"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registro e inicio de sesion por email (Priority: P1)

Como nuevo usuario, quiero registrarme con email y password para acceder rapidamente a la app y comenzar con el plan Free.

**Why this priority**: Es el punto de entrada base del producto y requisito para cualquier funcionalidad posterior.

**Independent Test**: Puede probarse de forma aislada creando usuario, verificando login, emision de tokens y acceso a endpoint protegido.

**Acceptance Scenarios**:

1. **Given** un usuario no registrado, **When** se registra con email valido y password fuerte, **Then** el sistema crea su cuenta con plan `free` y estado activo.
2. **Given** un usuario registrado, **When** inicia sesion con credenciales correctas, **Then** recibe `access_token` y `refresh_token` validos.
3. **Given** un usuario autenticado, **When** accede a un endpoint protegido con `access_token` valido, **Then** obtiene respuesta exitosa.

---

### User Story 2 - Inicio de sesion social (Google/Facebook) (Priority: P2)

Como usuario, quiero autenticarme con Google o Facebook para entrar sin crear una password local.

**Why this priority**: Reduce friccion de onboarding y mejora conversion en primer uso.

**Independent Test**: Puede probarse con tokens OAuth de prueba, verificando creacion/actualizacion de usuario y entrega de JWT internos.

**Acceptance Scenarios**:

1. **Given** un usuario sin cuenta local, **When** inicia sesion con Google con token valido, **Then** el sistema crea usuario y devuelve JWT de TRDIA.
2. **Given** un usuario existente por Google, **When** inicia sesion nuevamente, **Then** el sistema reutiliza la misma cuenta y devuelve nuevos tokens.
3. **Given** un token OAuth invalido o vencido, **When** intenta autenticarse, **Then** el sistema rechaza la solicitud con error de autenticacion.

---

### User Story 3 - Renovacion de sesion segura (Priority: P3)

Como usuario activo, quiero renovar mi sesion sin volver a loguearme constantemente para mantener la experiencia fluida y segura.

**Why this priority**: Mejora UX y mantiene seguridad mediante access token corto + refresh token controlado.

**Independent Test**: Se prueba expirando access token, renovando con refresh token valido y revocando refresh token comprometido.

**Acceptance Scenarios**:

1. **Given** un `access_token` expirado y `refresh_token` valido, **When** solicita renovacion, **Then** recibe nuevo par de tokens sin ingresar credenciales de nuevo.
2. **Given** un `refresh_token` revocado, **When** intenta renovar sesion, **Then** el sistema rechaza y exige nuevo login.
3. **Given** un usuario que cierra sesion, **When** intenta usar refresh token previo, **Then** el token es invalido y no se emiten nuevos tokens.

---

### User Story 4 - Perfil y rol inicial del usuario (Priority: P4)

Como usuario autenticado, quiero consultar mi perfil y plan actual para entender mi estado de cuenta y limites disponibles.

**Why this priority**: Permite al usuario confirmar identidad, plan activo y estado base para avanzar a configuracion del bot.

**Independent Test**: Se prueba endpoint de perfil autenticado y validacion de asignacion de rol inicial `free`.

**Acceptance Scenarios**:

1. **Given** un usuario recien registrado, **When** consulta su perfil, **Then** ve plan `free` y datos basicos de cuenta.
2. **Given** un usuario autenticado, **When** consulta su perfil, **Then** obtiene datos consistentes con su sesion actual.

---

### Edge Cases

- Registro con email ya existente por otro proveedor (email/password vs OAuth) debe vincular cuenta o rechazar de forma consistente.
- Intentos repetidos de login fallido desde misma IP deben activar rate limiting temporal.
- Refresh token reutilizado tras rotacion (token replay) debe invalidar la sesion completa.
- Usuario desactivado/bloqueado no puede autenticarse aunque credenciales sean correctas.
- Cambios de reloj del dispositivo no deben invalidar evaluacion de expiracion (servidor es fuente de verdad).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir registro por email/password con validacion de email y password fuerte.
- **FR-002**: El sistema MUST rechazar registros con email duplicado.
- **FR-003**: El sistema MUST hashear passwords con bcrypt antes de persistirlas.
- **FR-004**: El sistema MUST permitir login por email/password y emitir `access_token` + `refresh_token`.
- **FR-005**: El sistema MUST soportar autenticacion OAuth con Google.
- **FR-006**: El sistema MUST soportar autenticacion OAuth con Facebook.
- **FR-007**: El sistema MUST mapear identidades OAuth a una cuenta unica por usuario.
- **FR-008**: El sistema MUST asignar plan inicial `free` al crear cualquier cuenta nueva.
- **FR-009**: El sistema MUST exponer endpoint de renovacion de tokens mediante refresh token.
- **FR-010**: El sistema MUST permitir cierre de sesion revocando refresh token activo.
- **FR-011**: El sistema MUST permitir cierre de todas las sesiones de un usuario.
- **FR-012**: El sistema MUST proteger endpoints privados con validacion JWT.
- **FR-013**: El sistema MUST exponer endpoint `me/profile` con datos basicos y plan actual.
- **FR-014**: El sistema MUST registrar auditoria de registro, login exitoso/fallido, refresh, logout y revocaciones.
- **FR-015**: El sistema MUST aplicar rate limiting en endpoints de auth para mitigar fuerza bruta.
- **FR-016**: El sistema MUST diferenciar errores de autenticacion sin filtrar informacion sensible (sin revelar si email existe).

### Key Entities *(include if feature involves data)*

- **User**: Representa identidad principal del cliente. Atributos clave: `id`, `email`, `password_hash`, `auth_provider`, `provider_user_id`, `plan`, `status`, `created_at`, `updated_at`.
- **RefreshSession**: Representa sesion renovable. Atributos: `id`, `user_id`, `refresh_token_hash`, `device_info`, `ip_address`, `expires_at`, `revoked_at`, `rotated_from_id`.
- **AuthAuditLog**: Registro de eventos de autenticacion. Atributos: `id`, `user_id`, `event_type`, `result`, `ip_address`, `user_agent`, `metadata`, `created_at`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% de registros exitosos completados en menos de 60 segundos.
- **SC-002**: 99% de logins exitosos responden en menos de 1.5 segundos.
- **SC-003**: 100% de nuevas cuentas se crean con plan `free` correctamente.
- **SC-004**: 0 incidentes de password en texto plano en base de datos o logs.
- **SC-005**: 100% de refresh tokens revocados no pueden reutilizarse.
- **SC-006**: Menos de 1% de errores de autenticacion por problemas internos del sistema (excluyendo credenciales invalidas).

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: passwords, JWT access tokens, refresh tokens, identificadores OAuth, IP/device metadata.
  - **Encryption strategy**: password con bcrypt; refresh tokens hasheados antes de almacenar; JWT firmados (clave privada en backend).
  - **Storage**: Backend only. No se almacena password ni refresh token en texto plano.
  - **Logging**: No loggear password, tokens completos ni secretos OAuth; solo IDs y trazas seguras.

### Input Validation

- **Backend validation rules**: formato email RFC basico, password minima 8 caracteres con complejidad, payload JSON estricto, longitud maxima de campos.
- **SQL injection prevention**: Pydantic + SQLAlchemy ORM, sin concatenacion de SQL.
- **Payload limits**: max 64KB por request de auth; rate limiting por IP y por cuenta.

### Authentication & Authorization

- **Auth required?** No para `register/login/oauth/refresh`; Yes para `logout/me/profile`.
- **Roles/plans that can access**: Todos los usuarios autenticados pueden consultar perfil; acciones admin fuera de este feature.
- **Plan validation**: No aplica bloqueo por plan en autenticacion; solo asignacion plan `free` inicial.

### Audit Trail

- **What must be logged**: intento de registro, login exitoso/fallido, refresh, logout, revocacion global, bloqueo por rate limit.
- **Log level**: INFO para eventos exitosos, WARNING para fallos repetidos, ERROR para fallos internos.
- **Sensitive data exclusion**: confirmado, sin passwords ni tokens completos en logs.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** No (N/A a limites de operaciones).
- **Does this feature execute real monetary operations?** No.
- **Capital limits**: N/A.

### Frontend Behavior

- **Frontend role**: Captura credenciales y muestra errores amigables; no decide autorizacion final.
- **How frontend gets validation state**: respuestas de endpoints `/auth/*` y `/users/me`.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **auth.register.success_total**: Counter - Registros exitosos.
- **auth.register.failure_total**: Counter - Registros fallidos.
- **auth.login.success_total**: Counter - Logins exitosos.
- **auth.login.failure_total**: Counter - Logins fallidos.
- **auth.refresh.success_total**: Counter - Renovaciones exitosas.
- **auth.refresh.failure_total**: Counter - Renovaciones fallidas.
- **auth.login.latency_seconds**: Histogram - Latencia de login.
- **auth.rate_limit.block_total**: Counter - Bloqueos por rate limiting.

### Alerts

- **Alert 1**: tasa de fallo de login > 20% durante 10 minutos (posible ataque de fuerza bruta o incidencia).
- **Alert 2**: incremento > 5x en `auth.refresh.failure_total` en 15 minutos (posible replay o expiracion masiva).

### Logging

- **Key events to log**: register_attempt, register_success, login_success, login_failed, oauth_login_success, refresh_success, refresh_failed, logout_success, revoke_all_sessions.
- **Log level**: INFO para flujo normal; WARNING para eventos sospechosos; ERROR para excepciones internas.

