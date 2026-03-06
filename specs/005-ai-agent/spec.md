# Feature Specification: TRDIA - Agente IA de Trading

**Feature Branch**: `005-ai-agent`  
**Created**: 2026-03-06  
**Status**: Draft  
**Input**: User description: "Agente IA multi-proveedor con estrategias predefinidas"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar proveedor IA y estrategia (Priority: P1)

Como usuario autenticado, quiero elegir proveedor IA y estrategia predefinida para activar el agente con mis reglas de trading.

**Why this priority**: Es el punto de entrada funcional al core de IA; sin esta configuración no hay decisiones del agente.

**Independent Test**: Puede probarse aislado guardando configuración de agente y verificando generación de prompt sin ejecutar órdenes reales.

**Acceptance Scenarios**:

1. **Given** un usuario con sesión activa, **When** selecciona proveedor IA válido y registra su API key, **Then** el sistema guarda la configuración y marca agente como listo.
2. **Given** un usuario con catálogo de estrategias disponible, **When** selecciona una estrategia, **Then** el sistema la asocia al perfil del agente del usuario.
3. **Given** API key del proveedor inválida, **When** intenta activar agente, **Then** el sistema rechaza activación y notifica error de credencial.

---

### User Story 2 - El agente genera señales de trading consistentes (Priority: P2)

Como usuario, quiero que el agente analice el mercado y genere decisiones claras (BUY/SELL/HOLD) según mi estrategia y riesgo.

**Why this priority**: Es el valor diferencial principal del producto y el motor de automatización.

**Independent Test**: Se puede validar con datos de mercado de prueba verificando que el agente devuelve decisión estructurada y trazable.

**Acceptance Scenarios**:

1. **Given** un agente activo y datos de mercado disponibles, **When** se ejecuta un ciclo de análisis, **Then** el agente produce salida estructurada con acción, confianza y justificación.
2. **Given** parámetros de riesgo configurados, **When** el agente propone operación, **Then** la propuesta respeta esos límites.
3. **Given** señales ambiguas, **When** no hay criterio suficiente, **Then** el agente retorna HOLD en lugar de forzar una operación.

---

### User Story 3 - Modo de ejecución por plan (manual/automático) (Priority: P3)

Como usuario, quiero que el agente opere según mi plan: Free en manual, Plus/Premium en manual o automático.

**Why this priority**: Alinea el comportamiento del agente con la monetización y reduce riesgo en usuarios nuevos.

**Independent Test**: Se prueba con usuarios de distintos planes y misma señal del agente para validar flujos diferenciados.

**Acceptance Scenarios**:

1. **Given** usuario Free, **When** agente genera señal ejecutable, **Then** se crea sugerencia pendiente de aprobación manual.
2. **Given** usuario Plus en modo automático, **When** agente genera señal válida, **Then** se envía a ejecución sin aprobación manual.
3. **Given** usuario Premium en modo manual, **When** agente genera señal, **Then** se comporta como sugerencia manual.

---

### User Story 4 - Notificaciones y trazabilidad de decisiones IA (Priority: P4)

Como usuario, quiero ver por qué el agente tomó una decisión y recibir notificación de cada ejecución/fallo para mantener control y confianza.

**Why this priority**: Transparencia y confianza son clave en un sistema que impacta dinero real.

**Independent Test**: Se puede probar verificando historial de decisiones y emisión de notificaciones en ciclos de prueba.

**Acceptance Scenarios**:

1. **Given** una decisión emitida por el agente, **When** se consulta historial, **Then** se muestra razonamiento resumido y parámetros usados.
2. **Given** ejecución exitosa/fallida disparada por agente, **When** termina el flujo, **Then** el usuario recibe notificación correspondiente.

---

### Edge Cases

- Proveedor IA no disponible o timeout en respuesta.
- Respuesta del modelo no estructurada o incompleta.
- API key de proveedor revocada en medio del ciclo.
- Cambios de estrategia mientras un ciclo de análisis está en curso.
- Decisiones repetidas idénticas en ventanas cortas (spam de señales).
- Diferencias de precisión entre proveedores para la misma entrada.
- Señal generada con mercado cerrado o par no habilitado.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir seleccionar proveedor IA entre OpenAI, Groq, DeepSeek y Gemini.
- **FR-002**: El sistema MUST permitir registrar API key del proveedor IA por usuario.
- **FR-003**: El sistema MUST validar conectividad básica del proveedor antes de activar configuración.
- **FR-004**: El sistema MUST permitir seleccionar estrategia desde catálogo predefinido.
- **FR-005**: El sistema MUST incorporar dinámicamente la estrategia seleccionada al system prompt del agente.
- **FR-006**: El sistema MUST permitir configurar parámetros: risk management, timeframe, activos permitidos, stop-loss, take-profit, límite operativo adicional opcional.
- **FR-007**: El sistema MUST generar salida estructurada por ciclo: acción sugerida, nivel de confianza, razones y parámetros usados.
- **FR-008**: El sistema MUST soportar modo manual para usuarios Free (sugerencia, no ejecución directa).
- **FR-009**: El sistema MUST soportar modo manual o automático para usuarios Plus/Premium según preferencia.
- **FR-010**: El sistema MUST registrar historial de decisiones del agente, incluso cuando no hay ejecución.
- **FR-011**: El sistema MUST notificar al usuario por cada ejecución/fallo derivado del agente.
- **FR-012**: El sistema MUST soportar paper trading y ejecución real en función del modo operativo activo.
- **FR-013**: El sistema MUST permitir pausar/reanudar agente por usuario.
- **FR-014**: El sistema MUST evitar duplicidad de señales operativas equivalentes en ventana configurable.
- **FR-015**: El sistema MUST degradar de forma controlada a HOLD ante fallas de proveedor IA.
- **FR-016**: El sistema MUST mantener arquitectura extensible para incorporar nuevos proveedores sin romper contratos actuales.

### Key Entities *(include if feature involves data)*

- **AIAgentConfig**: Configuración central del agente por usuario. Campos: `user_id`, `provider`, `provider_key_encrypted`, `strategy_id`, `execution_mode`, `is_active`, `updated_at`.
- **AIStrategyCatalog**: Estrategias predefinidas. Campos: `strategy_id`, `name`, `category`, `description`, `prompt_template`, `is_active`.
- **AIDecision**: Resultado de análisis por ciclo. Campos: `decision_id`, `user_id`, `action`, `confidence`, `reason_summary`, `input_snapshot_ref`, `is_executable`, `created_at`.
- **AIExecutionLink**: Relación decisión-ejecución. Campos: `decision_id`, `trade_request_id`, `execution_status`, `notification_status`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% de configuraciones de agente (proveedor + estrategia) quedan activas en menos de 20 segundos.
- **SC-002**: 90% de ciclos de análisis generan salida estructurada válida sin intervención manual.
- **SC-003**: 100% de usuarios Free reciben sugerencias (no ejecución automática directa).
- **SC-004**: 99% de decisiones del agente quedan trazadas en historial con contexto mínimo requerido.
- **SC-005**: 99% de eventos de ejecución/fallo disparan notificación al usuario en menos de 10 segundos.
- **SC-006**: 0 exposiciones de API keys de proveedores IA en logs, respuestas o UI.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** Yes
  - Datos: API keys de proveedores IA, snapshot de inputs de mercado, razonamiento resumido de decisiones.
  - **Encryption strategy**: API keys cifradas en backend; acceso restringido solo al servicio de agente.
  - **Storage**: Backend only; frontend nunca recibe secretos de proveedor.
  - **Logging**: no registrar prompts completos con secretos ni API keys completas.

### Input Validation

- **Backend validation rules**: proveedor permitido, estrategia activa, parámetros de riesgo en rangos válidos, activos permitidos válidos.
- **SQL injection prevention**: validación de entrada + ORM.
- **Payload limits**: máximo de configuración y frecuencia de actualización limitada por usuario.

### Authentication & Authorization

- **Auth required?** Yes
- **Roles/plans that can access**: todos los usuarios autenticados configuran agente; modo automático solo Plus/Premium.
- **Plan validation**: enforcement en backend antes de convertir decisión en ejecución.

### Audit Trail

- **What must be logged**: activación/desactivación agente, cambio de proveedor, cambio de estrategia, cada decisión, fallas de proveedor, transición manual/automático.
- **Log level**: INFO para flujo normal, WARNING para degradaciones, ERROR para fallas críticas.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** Yes
  - Check: usuario Free nunca ejecuta automáticamente; Plus/Premium condicionados por preferencia y límites vigentes.

- **Does this feature execute real monetary operations?** Indirectamente (a través de módulo trading)
  - Check: cada decisión ejecutable debe pasar validación previa de trading (suscripción, límites, balance, riesgo).

- **Capital limits**: heredados del módulo de trading por plan; el agente no puede proponer ejecución fuera de límites definidos.

### Frontend Behavior

- **Frontend role**: configurar agente, visualizar decisiones, aprobar/rechazar sugerencias en modo manual.
- **How frontend gets validation state**: endpoint de estado del agente y endpoint de elegibilidad de ejecución.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **ai.config.updated_total**: Counter - Configuraciones de agente actualizadas.
- **ai.decision.generated_total**: Counter - Decisiones generadas.
- **ai.decision.hold_total**: Counter - Decisiones HOLD.
- **ai.decision.executable_total**: Counter - Decisiones marcadas como ejecutables.
- **ai.provider.error_total**: Counter - Errores por proveedor IA.
- **ai.cycle.latency_seconds**: Histogram - Latencia por ciclo de análisis.
- **ai.notification.sent_total**: Counter - Notificaciones enviadas por eventos del agente.

### Alerts

- **Alert 1**: `ai.provider.error_total` > 5% de ciclos en 10 minutos.
- **Alert 2**: caída de `ai.decision.generated_total` a 0 durante ventana operativa esperada.

### Logging

- **Key events to log**: agent_enabled, agent_disabled, provider_changed, strategy_changed, decision_generated, decision_degraded_to_hold, decision_sent_to_execution, provider_timeout.
- **Log level**: INFO para eventos normales, WARNING para degradación/fallback, ERROR para fallos de infraestructura.

