# Tasks: Cryptocurrency UI Kit Integration (Iteracion 1)

**Input**: Design docs from `/specs/012-cryptocurrency-ui-kit/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/frontend-ui-kit-integration.md`

**Tests**: TDD mandatory (RED -> GREEN -> REFACTOR) per Constitution Principle II and this feature plan.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar scaffolding de trabajo y evidencia de QA para la integracion visual cerrada de Sprint 012.

- [x] T001 Crear documento de evidencia QA para Sprint 012 en `docs/qa/cryptocurrency-ui-kit.md`
- [x] T002 Definir checklist de alcance cerrado y no-regresion en `specs/012-cryptocurrency-ui-kit/quickstart.md`
- [x] T003 [P] Registrar baseline visual y funcional de rutas privadas para comparativa en `docs/qa/cryptocurrency-ui-kit.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Bloqueadores obligatorios antes de implementar historias de usuario.

**CRITICAL**: Ninguna historia puede comenzar hasta completar esta fase.

- [x] T004 Registrar y aprobar revalidacion de governance de stack web para Sprint 012 en `docs/methodology/constitution-exceptions.md`
- [x] T005 Actualizar gate de readiness de governance como requisito de implementacion en `specs/012-cryptocurrency-ui-kit/quickstart.md`
- [x] T006 [P] Definir contrato de tokens y pautas del UI Kit para layout/dashboard/trading en `frontend/src/app/content/ui-kit-theme.ts`
- [x] T007 [P] Definir mapa de eventos de observabilidad UI Kit sin datos sensibles en `frontend/src/services/observability/events.ts`
- [x] T008 Asegurar compatibilidad de router privado y layout shell para cambios visuales sin alterar guardas en `frontend/src/app/router.tsx`
- [x] T009 Documentar matriz de trazabilidad FR/SC -> pruebas para la feature 012 en `docs/qa/cryptocurrency-ui-kit.md`

**Checkpoint**: Foundation lista. Se habilita implementacion por historia.

---

## Phase 3: User Story 1 - Layout Autenticado con UI Kit (Priority: P1) MVP

**Goal**: Aplicar el UI Kit al layout autenticado preservando autenticacion, guardas y navegacion privada.

**Independent Test**: Con sesion valida, el usuario ve layout privado redisenado y navega Dashboard/Trading; sin sesion, redirige a login.

### Tests for User Story 1 (MANDATORY)

- [x] T010 [P] [US1] Agregar pruebas unitarias de render y estados de navegacion del layout privado en `frontend/tests/unit/ui/private-layout.test.tsx`
- [x] T011 [P] [US1] Extender prueba de integracion de rutas privadas y redireccion post-login en `frontend/tests/integration/auth/private-routes.test.tsx`
- [x] T012 [P] [US1] Actualizar smoke E2E de acceso y navegacion autenticada con nuevo layout en `frontend/tests/e2e/us1-access-navigation.spec.ts`

### Implementation for User Story 1

- [x] T013 [P] [US1] Crear componentes estructurales del shell autenticado (header/sidebar/topbar) en `frontend/src/app/components/AuthenticatedShell.tsx`
- [x] T014 [P] [US1] Crear componente de item de navegacion con estado activo y accesibilidad de teclado en `frontend/src/app/components/NavigationItem.tsx`
- [x] T015 [P] [US1] Implementar estilos/tokens del shell autenticado basados en UI Kit en `frontend/src/app/content/ui-kit-theme.ts`
- [x] T016 [US1] Integrar shell UI Kit dentro del layout privado manteniendo logout y guardas actuales en `frontend/src/app/layouts/PrivateLayout.tsx`
- [x] T017 [US1] Ajustar definicion de rutas para mantener consistencia de estado activo en navegacion privada en `frontend/src/app/routes.tsx`
- [x] T018 [US1] Emitir eventos de observabilidad de render y redireccion en layout privado en `frontend/src/services/observability/events.ts`

**Checkpoint**: US1 funcional y validable de forma independiente (MVP).

---

## Phase 4: User Story 2 - Dashboard con Estilo del UI Kit (Priority: P2)

**Goal**: Redisenar Dashboard con UI Kit manteniendo datos/contratos actuales y estados UX completos.

**Independent Test**: Dashboard renderiza estados loading/success/empty/error con datos reales existentes sin cambiar APIs.

### Tests for User Story 2 (MANDATORY)

- [x] T019 [P] [US2] Extender pruebas unitarias del renderer de estados para variantes visuales de Dashboard en `frontend/tests/unit/ui/view-state-renderer.test.tsx`
- [x] T020 [P] [US2] Extender prueba de integracion de carga e historial en Dashboard con assertions de estados UX en `frontend/tests/integration/dashboard/history-flow.test.tsx`
- [x] T021 [P] [US2] Crear smoke E2E de Dashboard redisenado con escenarios de datos y fallback en `frontend/tests/e2e/us2-dashboard-ui-kit.spec.ts`

### Implementation for User Story 2

- [x] T022 [P] [US2] Crear componentes de cards y paneles de resumen para Dashboard UI Kit en `frontend/src/features/dashboard/DashboardSummaryCards.tsx`
- [x] T023 [P] [US2] Crear componente de tabla/listado de historial para Dashboard UI Kit en `frontend/src/features/dashboard/DashboardHistoryPanel.tsx`
- [x] T024 [P] [US2] Ajustar mapeo de datos del dashboard para necesidades de presentacion sin alterar contrato backend en `frontend/src/features/dashboard/dashboard.viewmodel.ts`
- [x] T025 [US2] Integrar componentes UI Kit y estados UX en pagina Dashboard en `frontend/src/pages/DashboardPage.tsx`
- [x] T026 [US2] Ajustar mensajes de empty/error para Dashboard manteniendo acciones de retry en `frontend/src/app/content/error-messages.ts`
- [x] T027 [US2] Emitir eventos de observabilidad de transicion de estado de Dashboard en `frontend/src/services/observability/events.ts`

**Checkpoint**: US2 funcional e independiente con estado visual consistente.

---

## Phase 5: User Story 3 - Trading con Estilo del UI Kit (Priority: P3)

**Goal**: Redisenar Trading con UI Kit preservando submit, feedback y validaciones backend existentes.

**Independent Test**: Usuario ejecuta flujo de trading (submit exitoso y error) con feedback claro y sin cambio de logica backend.

### Tests for User Story 3 (MANDATORY)

- [x] T028 [P] [US3] Extender pruebas unitarias de control de submit y feedback visual de Trading en `frontend/tests/unit/ui/trading-form-state.test.tsx`
- [x] T029 [P] [US3] Extender prueba de integracion del flujo de trading con assertions de submitting/success/error en `frontend/tests/integration/trading/trading-flow.test.tsx`
- [x] T030 [P] [US3] Extender smoke E2E de confiabilidad UX para submit y recuperacion en Trading en `frontend/tests/e2e/us3-ux-reliability.spec.ts`

### Implementation for User Story 3

- [x] T031 [P] [US3] Crear componentes visuales del formulario y panel de resultado para Trading UI Kit en `frontend/src/features/trading/TradingFormPanel.tsx`
- [x] T032 [P] [US3] Ajustar proyeccion de estado de trading (idle/submitting/success/error) en `frontend/src/features/trading/trading.viewmodel.ts`
- [x] T033 [P] [US3] Integrar componente de guardado de submit para evitar doble envio en `frontend/src/app/components/SubmitGuardButton.tsx`
- [x] T034 [US3] Integrar componentes UI Kit y feedback de estado en pagina Trading en `frontend/src/pages/TradingPage.tsx`
- [x] T035 [US3] Ajustar mensajes accionables de error/success de Trading sin exponer detalles sensibles en `frontend/src/app/content/error-messages.ts`
- [x] T036 [US3] Emitir eventos de observabilidad de submit y resultado de Trading en `frontend/src/services/observability/events.ts`

**Checkpoint**: US3 funcional e independiente con submit y recuperacion confiables.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de calidad, regresion completa y evidencia final de cumplimiento.

- [x] T037 [P] Ejecutar suite de regresion frontend (unit + integration + e2e smoke) y registrar resultados en `docs/qa/cryptocurrency-ui-kit.md`
- [x] T038 [P] Ejecutar validacion responsive (mobile/desktop) y accesibilidad basica (focus/teclado/contraste) en layout/dashboard/trading en `docs/qa/cryptocurrency-ui-kit.md`
- [x] T039 Validar que no hubo cambios de contratos backend ni endpoints durante la implementacion en `docs/qa/cryptocurrency-ui-kit.md`
- [x] T040 Actualizar checklist final de readiness para `/speckit.implement` en `specs/012-cryptocurrency-ui-kit/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): inicia inmediatamente.
- Foundational (Phase 2): depende de Setup y bloquea todas las historias.
- User Stories (Phases 3-5): dependen de Foundational y se ejecutan en orden de prioridad P1 -> P2 -> P3 para alcance cerrado.
- Polish (Phase 6): depende de completar historias en alcance.

### User Story Dependencies

- US1 (P1): inicia tras Phase 2; no depende de US2/US3.
- US2 (P2): inicia tras validacion MVP de US1 para preservar estabilidad de layout/routing.
- US3 (P3): inicia tras US2, reutilizando patrones visuales y de estados UX ya consolidados.

### Dependency Graph (Story Completion Order)

- Foundation -> US1 -> US2 -> US3 -> Polish

### Within Each User Story

- Tests primero y en fallo esperado (RED) antes de implementar.
- Componentes base/estado antes de integrar en pagina.
- Integracion en pagina antes de eventos de observabilidad finales.
- Criterio independiente de la historia debe pasar antes de avanzar.

---

## Parallel Execution Examples

## Parallel Example: User Story 1

```bash
Task T010 + T011 + T012
Task T013 + T014 + T015
```

## Parallel Example: User Story 2

```bash
Task T019 + T020 + T021
Task T022 + T023 + T024
```

## Parallel Example: User Story 3

```bash
Task T028 + T029 + T030
Task T031 + T032 + T033
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Completar Phases 1 y 2 (incluyendo gate de governance).
2. Completar US1 y validar prueba independiente.
3. Congelar baseline MVP de layout autenticado antes de continuar.

### Incremental Delivery

1. Foundation completa.
2. Entregar US1 (layout autenticado).
3. Entregar US2 (Dashboard UI Kit).
4. Entregar US3 (Trading UI Kit).
5. Ejecutar polish y evidencia final.

### Parallel Team Strategy

1. Equipo completo en Setup + Foundational.
2. Luego del gate:
   - Dev A: US1 layout/routing.
   - Dev B: US2 dashboard.
   - Dev C: US3 trading.
3. Integracion por prioridad con evidencia de pruebas por historia.

---

## Notes

- Todas las tareas cumplen formato checklist: `- [ ] T### [P?] [US?] Descripcion con ruta de archivo`.
- Alcance cerrado forzado: solo layout autenticado + Dashboard + Trading.
- No se permiten cambios de backend, endpoints o reglas de negocio en esta feature.
