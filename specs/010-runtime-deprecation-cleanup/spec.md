# Feature Specification: Runtime Deprecation Cleanup

**Feature Branch**: `010-runtime-deprecation-cleanup`  
**Created**: 2026-03-09  
**Status**: Draft  
**Input**: User description: "Runtime deprecation cleanup for FastAPI lifespan and runtime warnings"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove Startup Deprecations (Priority: P1)

Como equipo técnico, queremos eliminar deprecaciones de ciclo de vida de la API para mantener compatibilidad y evitar deuda operativa en siguientes upgrades.

**Why this priority**: Esta deprecación está en el arranque del servicio y afecta todo el runtime.

**Independent Test**: Iniciar la app y ejecutar test suite sin warnings deprecados de ciclo de vida.

**Acceptance Scenarios**:

1. **Given** el backend iniciado, **When** se levanta la aplicación, **Then** no aparece warning por eventos de startup obsoletos.
2. **Given** la suite de pruebas, **When** se ejecuta en contenedor, **Then** los flujos existentes mantienen comportamiento funcional.

---

### User Story 2 - Stabilize Dependency Warning Surface (Priority: P2)

Como mantenedor del proyecto, quiero reducir warnings de dependencias conocidas para que los reportes de ejecución muestren solo señales relevantes.

**Why this priority**: Mejora observabilidad de calidad y evita normalizar warnings en CI.

**Independent Test**: Ejecutar pruebas y validar reducción de warnings conocidos sin afectar resultados.

**Acceptance Scenarios**:

1. **Given** pruebas de autenticación y seguridad, **When** se ejecutan, **Then** no aparecen warnings esperados como "ruido" sin acción definida.

---

### User Story 3 - Document Runtime Baseline Policy (Priority: P3)

Como equipo, queremos una política explícita de manejo de warnings para mantener disciplina de mantenimiento en nuevas features.

**Why this priority**: Evita regresión silenciosa en deuda técnica y facilita revisiones futuras.

**Independent Test**: Revisar documentación de metodología y confirmar criterios para aceptar/rechazar warnings.

**Acceptance Scenarios**:

1. **Given** una nueva PR, **When** se evalúa calidad runtime, **Then** existe criterio documentado para warnings bloqueantes vs no bloqueantes.

### Edge Cases

- El reemplazo de ciclo de vida rompe inicialización de componentes existentes.
- Diferencias de comportamiento entre ejecución local y contenedor.
- Warnings suprimidos sin remediación real.
- Dependencia externa introduce warning nuevo en parche menor.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (P1)**: El sistema MUST migrar el manejo de inicialización de aplicación al patrón de ciclo de vida recomendado.
- **FR-002 (P1)**: El sistema MUST mantener el comportamiento actual de bootstrap tras la migración.
- **FR-003 (P1)**: El sistema MUST ejecutar test suite en contenedor sin warnings deprecados del ciclo de vida reemplazado.
- **FR-004 (P2)**: El sistema MUST identificar y tratar warnings de dependencias recurrentes con acción explícita (remediar, fijar versión o documentar excepción).
- **FR-005 (P2)**: El sistema MUST evitar suprimir warnings globalmente sin justificación específica.
- **FR-006 (P3)**: El sistema MUST documentar política de runtime warnings para revisiones futuras.

### Key Entities *(include if feature involves data)*

- **RuntimeWarningRecord**: registro conceptual de warning detectado, origen, severidad y decisión de tratamiento.
- **LifecycleBootstrapPolicy**: definición de responsabilidades en startup/shutdown y criterios de compatibilidad.

## Assumptions & Dependencies

- Base branch oficial del repositorio: `master`.
- El entorno de validación principal sigue siendo el contenedor `Apeiron-Trade`.
- El alcance de esta feature no incluye refactor funcional de negocio.

## Sprint Scope (Closed)

### In Scope (Sprint 010)

- Limpieza de deprecación de ciclo de vida en backend.
- Reducción/control de warnings runtime conocidos con evidencia de test.
- Documentación de política de warnings.

### Out of Scope (Future Feature)

- Refactor profundo de módulos no relacionados con lifecycle.
- Reescritura completa de dependencias externas.
- Cambios de producto o contratos API de negocio.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 warnings por patrón de ciclo de vida obsoleto durante arranque y ejecución de pruebas.
- **SC-002**: 100% de pruebas existentes continúan pasando tras la limpieza de deprecaciones.
- **SC-003**: Reducción observable de warnings totales en ejecución de suite respecto a baseline actual.
- **SC-004**: Política de warnings documentada y referenciable en revisiones de PR.

## Security Requirements *(mandatory for TRDIA - Constitution Principle III)*

### Credentials & Sensitive Data

- **Does this feature handle sensitive data?** No cambio de manejo de datos sensibles.
  - **Encryption strategy**: Sin cambios.
  - **Storage**: Sin cambios.
  - **Logging**: Mantener exclusión estricta de secretos/tokens.

### Input Validation

- **Backend validation rules**: Sin cambios funcionales en validaciones de payload de negocio.
- **SQL injection prevention**: Sin cambios.
- **Payload limits**: Sin cambios.

### Authentication & Authorization

- **Auth required?** Sin cambios.
- **Roles/plans that can access**: Sin cambios.
- **Plan validation**: Sin cambios.

### Audit Trail

- **What must be logged**: eventos de inicio/cierre de aplicación relevantes para diagnóstico.
- **Log level**: INFO para flujo normal, WARNING para degradaciones.
- **Sensitive data exclusion**: confirmado.

## Validation Strategy *(mandatory for trading/subscription features - Constitution Principle V)*

### Backend Validation (NON-NEGOTIABLE)

- **Does this feature require plan limit validation?** No cambio.
- **Does this feature execute real monetary operations?** No.
- **Capital limits**: Sin cambios.

### Frontend Behavior

- **Frontend role**: Sin cambios.
- **How frontend gets validation state**: Sin cambios.

## Observability *(mandatory - Constitution Principle VI)*

### Metrics

- **runtime.warnings.total**: Counter - total de warnings detectados durante tests.
- **runtime.lifecycle.deprecation.total**: Counter - warnings deprecados de ciclo de vida.

### Alerts

- **Alert 1**: `runtime.lifecycle.deprecation.total > 0` en pipeline de validación.
- **Alert 2**: incremento sostenido de `runtime.warnings.total` respecto a baseline acordado.

### Logging

- **Key events to log**: startup initialized, startup failed, shutdown completed.
- **Log level**: INFO para eventos esperados, ERROR para fallos de inicialización.
