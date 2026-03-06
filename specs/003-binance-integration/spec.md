# Feature Specification: TRDIA - Integracion Binance Spot

**Feature Branch**: `001-binance-integration`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Integracion Binance Spot para TRDIA"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar credenciales Binance de forma segura (Priority: P1)

Como usuario autenticado, quiero guardar mis API keys de Binance para habilitar operaciones reales desde la app.

**Why this priority**: Sin credenciales Binance validas no se puede ejecutar trading real, que es el core del producto.

**Independent Test**: Se puede probar aislado validando guardado cifrado, test de conectividad y lectura enmascarada sin ejecutar operaciones.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado, **When** ingresa API Key y Secret Key validas, **Then** el sistema valida conectividad Binance y guarda ambas cifradas.
2. **Given** un usuario con credenciales guardadas, **When** consulta configuracion, **Then** solo ve clave enmascarada (ultimos 4 caracteres) y estado de verificacion.
3. **Given** credenciales invalidas, **When** intenta guardarlas, **Then** el sistema rechaza la operacion y no persiste datos.

---

### User Story 2 - Ejecutar operaciones Spot con validaciones de negocio (Priority: P2)

Como usuario, quiero ejecutar ordenes Spot (manual o automaticas via agente) respetando limites de plan y reglas de riesgo.

**Why this priority**: Es la funcionalidad de valor principal para usuarios Free/Plus/Premium.

**Independent Test**: Puede validarse con Binance Testnet y mocks verificando reglas de limite semanal, balance y parametros.

**Acceptance Scenarios**:

1. **Given** usuario Free con 0 operaciones esta semana, **When** aprueba una sugerencia BUY, **Then** la orden se ejecuta y su contador semanal incrementa a 1.
2. **Given** usuario Free con 1 operacion usada, **When** intenta otra ejecucion real, **Then** el backend bloquea con estado de limite excedido.
3. **Given** usuario Plus en modo automatico y dentro de limite, **When** el agente emite señal valida, **Then** la orden se ejecuta sin aprobacion manual.
4. **Given** usuario con balance insuficiente, **When** intenta operar, **Then** el sistema rechaza la ejecucion con motivo claro.

---

### User Story 3 - Operar en paper trading ilimitado (Priority: P3)

Como usuario de cualquier plan, quiero probar estrategias en simulacion sin riesgo ni consumo de limite semanal.

**Why this priority**: Reduce friccion de adopcion, permite aprendizaje y mejora conversion de Free a Plus/Premium.

**Independent Test**: Se prueba sin Binance real verificando ejecucion simulada, persistencia en historial y no consumo de contador semanal.

**Acceptance Scenarios**:

1. **Given** modo simulacion activo, **When** se ejecuta una orden simulada, **Then** se guarda en historial como `is_simulation=true`.
2. **Given** usuario Free con limite agotado en real, **When** opera en simulacion, **Then** puede seguir operando sin bloqueo.
3. **Given** historial mixto, **When** usuario consulta operaciones, **Then** el sistema distingue claramente real vs simulacion.

---

### User Story 4 - Notificaciones y trazabilidad por cada ejecucion (Priority: P4)

Como usuario, quiero recibir notificaciones cada vez que se ejecuta (o falla) una operacion para mantener control de mi cuenta.

**Why this priority**: Es un requerimiento explicito del negocio y aumenta confianza del usuario en la automatizacion.

**Independent Test**: Se valida emitiendo ordenes de prueba y verificando evento de notificacion para exito/fallo.

**Acceptance Scenarios**:

1. **Given** una orden ejecutada con exito, **When** finaliza la ejecucion, **Then** el usuario recibe notificacion push con resumen de trade.
2. **Given** una orden fallida por error de exchange, **When** ocurre el fallo, **Then** el usuario recibe notificacion de error con causa.

---

### Edge Cases

- Binance API temporalmente no disponible durante ejecucion.
- Latencia alta provoca timeout en respuesta de orden.
- Orden enviada pero respuesta de confirmacion perdida (estado incierto).
- Usuario revoca API key en Binance despues de configurarla en TRDIA.
- Duplicidad de solicitud de ejecucion por reintento del cliente movil.
- Simbolo no habilitado temporalmente por Binance.
- Precision de cantidad/precio fuera de reglas del par (tick size/lot size).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir guardar API Key y Secret Key de Binance por usuario autenticado.
- **FR-002**: El sistema MUST validar conectividad de credenciales con Binance antes de activar la configuracion.
- **FR-003**: El sistema MUST almacenar credenciales Binance cifradas y nunca en texto plano.
- **FR-004**: El sistema MUST permitir actualizar y revocar credenciales Binance.
- **FR-005**: El sistema MUST soportar ordenes Spot tipo MARKET y LIMIT.
- **FR-006**: El sistema MUST ejecutar operaciones manuales para plan Free solo tras aprobacion explicita del usuario.
- **FR-007**: El sistema MUST permitir en Plus/Premium seleccion entre ejecucion manual o automatica.
- **FR-008**: El sistema MUST validar limite semanal de operaciones en backend antes de ejecutar orden real.
- **FR-009**: El sistema MUST contar operaciones por transaccion individual (BUY=1, SELL=1).
- **FR-010**: El sistema MUST excluir operaciones de paper trading del contador semanal.
- **FR-011**: El sistema MUST bloquear ejecuciones reales cuando limite semanal este excedido.
- **FR-012**: El sistema MUST validar balance suficiente antes de enviar orden a Binance.
- **FR-013**: El sistema MUST validar simbolo permitido y parametros de riesgo configurados por usuario.
- **FR-014**: El sistema MUST registrar cada intento de ejecucion (exito, fallo, bloqueado) en historial/auditoria.
- **FR-015**: El sistema MUST enviar notificacion push por cada ejecucion o fallo de operacion.
- **FR-016**: El sistema MUST soportar modo paper trading para todos los planes sin restricciones de cantidad.
- **FR-017**: El sistema MUST exponer historial de operaciones diferenciando real y simulacion.
- **FR-018**: El sistema MUST aplicar idempotencia para evitar doble ejecucion por reintentos del cliente.

### Key Entities *(include if feature involves data)*

- **BinanceCredential**: Credenciales por usuario. Campos clave: `user_id`, `api_key_encrypted`, `secret_key_encrypted`, `is_active`, `last_verified_at`, `masked_key_suffix`.
- **TradeExecutionRequest**: Solicitud de ejecucion. Campos: `user_id`, `symbol`, `side`, `order_type`, `quantity`, `limit_price`, `is_simulation`, `request_id`.
- **TradeExecution**: Resultado de orden. Campos: `trade_id`, `user_id`, `symbol`, `side`, `status`, `executed_price`, `quantity`, `exchange_order_id`, `is_simulation`, `failure_reason`, `created_at`.
- **OperationCounter**: Contador semanal por usuario. Campos: `user_id`, `week_start_utc`, `operations_used`, `plan_limit`, `last_updated_at`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% de validaciones de credenciales Binance completadas en menos de 3 segundos.
- **SC-002**: 99% de operaciones Spot validas se registran en historial en menos de 5 segundos tras la ejecucion.
- **SC-003**: 100% de operaciones bloqueadas por limite semanal son rechazadas en backend (cero bypass).
- **SC-004**: 100% de operaciones en simulacion no incrementan contador semanal.
- **SC-005**: 99% de notificaciones de ejecucion (exito/fallo) se emiten dentro de 10 segundos.
- **SC-006**: 0 exposiciones de API keys de Binance en logs, respuestas o UI.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: API Key Binance, Secret Key Binance, datos de ordenes y balance.
  - **Encryption strategy**: Cifrado fuerte de credenciales antes de persistencia; desencriptado solo en backend al ejecutar.
  - **Storage**: Backend only; frontend nunca recibe secretos completos.
  - **Logging**: Solo datos enmascarados de credenciales; no secretos en texto.

### Input Validation

- **Backend validation rules**: `symbol` valido, `quantity > 0`, `limit_price > 0` cuando aplique, precision aceptada por par, `request_id` obligatorio para idempotencia.
- **SQL injection prevention**: Pydantic + ORM.
- **Payload limits**: max 128KB por solicitud de ejecucion; rate limiting por usuario.

### Authentication & Authorization

- **Auth required?** Yes
- **Roles/plans that can access**: usuarios autenticados Free/Plus/Premium.
- **Plan validation**: enforcement estricto de limite semanal y modo permitido por plan.

### Audit Trail

- **What must be logged**: configuracion/actualizacion de credenciales, validacion de credenciales, cada intento de ejecucion, bloqueos por plan, errores de Binance.
- **Log level**: INFO (flujo normal), WARNING (bloqueos/errores de usuario), ERROR (fallos internos/exchange).
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** Yes
  - Check: `operations_used < plan_limit` antes de toda ejecucion real.

- **Does this feature execute real monetary operations?** Yes
  - Checks pre-ejecucion: credenciales activas, balance suficiente, simbolo permitido, parametros de riesgo validos, modo de ejecucion permitido por plan.

- **Capital limits**: aplicar segun plan configurado por constitucion (Free 10%, Plus 20%, Premium 50% del balance por operacion).

### Frontend Behavior

- **Frontend role**: captura y muestra estado; no decide autorizacion final de operacion.
- **How frontend gets validation state**: endpoint de estado de trading que retorna contador semanal, limite y habilitacion actual.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **binance.credentials.verify_success_total**: Counter - Validaciones de credenciales exitosas.
- **binance.credentials.verify_failure_total**: Counter - Validaciones fallidas.
- **trading.execution.success_total**: Counter - Ejecuciones exitosas.
- **trading.execution.failure_total**: Counter - Ejecuciones fallidas.
- **trading.execution.blocked_total**: Counter - Bloqueos por validacion de negocio.
- **trading.execution.latency_seconds**: Histogram - Latencia total de ejecucion.
- **trading.simulation.total**: Counter - Operaciones en paper trading.

### Alerts

- **Alert 1**: `trading.execution.failure_total` > 5% en ventana de 5 minutos.
- **Alert 2**: `binance.credentials.verify_failure_total` anomalo (>3x baseline) en 15 minutos.

### Logging

- **Key events to log**: credential_saved, credential_verified, trade_requested, trade_executed, trade_blocked, trade_failed, simulation_executed.
- **Log level**: INFO para eventos normales, WARNING para bloqueos y validaciones fallidas, ERROR para excepciones internas o exchange.
