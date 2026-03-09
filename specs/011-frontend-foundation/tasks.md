# Tasks: Frontend Foundation MVP

**Input**: Design docs from `/specs/011-frontend-foundation/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/frontend-backend-integration.md`, `checklists/requirements.md`

**Tests**: TDD mandatory (RED -> GREEN -> REFACTOR) per Constitution Principle II and this feature plan.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Bootstrap frontend workspace and testing/documentation scaffolding for Sprint 011.

- [ ] T001 Create frontend web workspace skeleton in `frontend/src/app/.gitkeep`
- [ ] T002 Initialize frontend package and scripts for app/test/lint/build in `frontend/package.json`
- [ ] T003 [P] Configure TypeScript compiler options for frontend app and tests in `frontend/tsconfig.json`
- [ ] T004 [P] Configure test runner and browser test environment in `frontend/vitest.config.ts`
- [ ] T005 [P] Create frontend QA evidence document scaffold for Sprint 011 in `docs/qa/frontend-foundation.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement governance and shared primitives required before any user-story coding.

**CRITICAL**: No user story work can start until this phase is complete.

- [ ] T006 Document and approve constitution stack exception/amendment for web MVP implementation in `docs/methodology/constitution-exceptions.md`
- [ ] T007 Add Sprint 011 governance gate and approver record to feature quickstart in `specs/011-frontend-foundation/quickstart.md`
- [ ] T008 [P] Implement shared frontend HTTP client with auth/session interceptors and typed error mapping in `frontend/src/services/http/client.ts`
- [ ] T009 [P] Define shared UX state contract (`loading/empty/error/success`) and reusable state helpers in `frontend/src/app/state/view-state.ts`
- [ ] T010 [P] Implement shared observability event logger with sensitive-field redaction in `frontend/src/services/observability/events.ts`
- [ ] T011 Implement router shell with private-route guard and session-expiration redirect support in `frontend/src/app/router.tsx`
- [ ] T012 Wire app root providers (router, session context, query/cache layer) in `frontend/src/app/main.tsx`

**Checkpoint**: Foundation ready. User-story work can begin.

---

## Phase 3: User Story 1 - Access and Core Navigation (Priority: P1) MVP

**Goal**: Deliver login/logout, protected navigation, and baseline private sections (Dashboard, Trading, Notifications, AI Agent).

**Independent Test**: Login with valid credentials, verify protected routing, navigate all core sections without losing session.

### Tests for User Story 1 (MANDATORY)

- [ ] T013 [P] [US1] Add unit tests for session state transitions and expiry handling in `frontend/tests/unit/auth/session-store.test.ts`
- [ ] T014 [P] [US1] Add integration test for private-route redirection and post-login routing in `frontend/tests/integration/auth/private-routes.test.tsx`
- [ ] T015 [P] [US1] Add E2E smoke test for login and core navigation journey in `frontend/tests/e2e/us1-access-navigation.spec.ts`

### Implementation for User Story 1

- [ ] T016 [P] [US1] Implement auth API adapter for login/logout/session refresh using existing backend contracts in `frontend/src/features/auth/auth.api.ts`
- [ ] T017 [P] [US1] Implement session store/context and auth guard hooks in `frontend/src/features/auth/session-store.ts`
- [ ] T018 [US1] Implement login page with actionable validation and error messages in `frontend/src/pages/LoginPage.tsx`
- [ ] T019 [US1] Implement authenticated app shell and primary navigation layout in `frontend/src/app/layouts/PrivateLayout.tsx`
- [ ] T020 [P] [US1] Create base dashboard page placeholder with shared state rendering in `frontend/src/pages/DashboardPage.tsx`
- [ ] T021 [P] [US1] Create base trading page placeholder with shared state rendering in `frontend/src/pages/TradingPage.tsx`
- [ ] T022 [P] [US1] Create base notifications page placeholder with shared state rendering in `frontend/src/pages/NotificationsPage.tsx`
- [ ] T023 [P] [US1] Create base AI agent page placeholder with shared state rendering in `frontend/src/pages/AIAgentPage.tsx`
- [ ] T024 [US1] Register auth and section routes with guard enforcement in `frontend/src/app/routes.tsx`

**Checkpoint**: US1 is independently functional and MVP-releasable.

---

## Phase 4: User Story 2 - End-to-End Core User Flows (Priority: P2)

**Goal**: Enable full MVP business journeys for trading credentials/order execution, history view, notifications, and AI configuration using existing backend APIs.

**Independent Test**: From authenticated session, complete each core flow and observe success/failure states matching backend responses.

### Tests for User Story 2 (MANDATORY)

- [ ] T025 [P] [US2] Add integration test for trading credential save and order execution workflow in `frontend/tests/integration/trading/trading-flow.test.tsx`
- [ ] T026 [P] [US2] Add integration test for dashboard/history loading with basic filters in `frontend/tests/integration/dashboard/history-flow.test.tsx`
- [ ] T027 [P] [US2] Add integration test for notification device register and emit workflow in `frontend/tests/integration/notifications/notifications-flow.test.tsx`
- [ ] T028 [P] [US2] Add integration test for AI agent config load/edit/save workflow in `frontend/tests/integration/ai-agent/ai-config-flow.test.tsx`
- [ ] T029 [P] [US2] Add E2E smoke test that covers all P2 core flows end-to-end in `frontend/tests/e2e/us2-core-flows.spec.ts`

### Implementation for User Story 2

- [ ] T030 [P] [US2] Implement dashboard summary/history API adapter and mappers in `frontend/src/features/dashboard/dashboard.api.ts`
- [ ] T031 [P] [US2] Implement trading API adapter for credential verify/save and order execution in `frontend/src/features/trading/trading.api.ts`
- [ ] T032 [P] [US2] Implement notifications API adapter for device register and event emit in `frontend/src/features/notifications/notifications.api.ts`
- [ ] T033 [P] [US2] Implement AI agent configuration API adapter for load/update operations in `frontend/src/features/ai-agent/ai-agent.api.ts`
- [ ] T034 [US2] Implement dashboard view model and filters for metrics/recent operations rendering in `frontend/src/features/dashboard/dashboard.viewmodel.ts`
- [ ] T035 [US2] Implement trading flow view model with submit lock and backend-validation projection in `frontend/src/features/trading/trading.viewmodel.ts`
- [ ] T036 [US2] Implement notifications flow view model with registered-device precondition in `frontend/src/features/notifications/notifications.viewmodel.ts`
- [ ] T037 [US2] Implement AI agent config view model with basic form validation and save state in `frontend/src/features/ai-agent/ai-agent.viewmodel.ts`
- [ ] T038 [US2] Connect P2 view models to pages and complete end-to-end UI actions in `frontend/src/app/routes.tsx`

**Checkpoint**: US2 is independently testable against existing backend contracts.

---

## Phase 5: User Story 3 - UX Reliability and Error Handling (Priority: P3)

**Goal**: Standardize resilient UX for loading, empty, error, retry, and recovery behavior across all core frontend flows.

**Independent Test**: Simulate session expiration, transient network failures, and empty datasets; verify actionable messaging and successful recovery without context loss.

### Tests for User Story 3 (MANDATORY)

- [ ] T039 [P] [US3] Add unit tests for shared view-state renderer and actionable message mapping in `frontend/tests/unit/ui/view-state-renderer.test.tsx`
- [ ] T040 [P] [US3] Add integration test for session-expired recovery across private routes in `frontend/tests/integration/auth/session-expiry-recovery.test.tsx`
- [ ] T041 [P] [US3] Add integration test for transient network retry behavior in trading and notifications flows in `frontend/tests/integration/resilience/network-retry.test.tsx`
- [ ] T042 [P] [US3] Add E2E smoke test for empty/error/loading recovery journey in `frontend/tests/e2e/us3-ux-reliability.spec.ts`

### Implementation for User Story 3

- [ ] T043 [P] [US3] Implement reusable state panel components for loading, empty, error, and success variants in `frontend/src/app/components/StatePanel.tsx`
- [ ] T044 [P] [US3] Implement reusable retry and error-normalization utility for HTTP/domain failures in `frontend/src/services/http/error-normalizer.ts`
- [ ] T045 [US3] Integrate state panel and retry actions into dashboard/trading/notifications/ai pages in `frontend/src/app/routes.tsx`
- [ ] T046 [US3] Implement duplicate-submit protection and visual feedback for critical form actions in `frontend/src/app/components/SubmitGuardButton.tsx`
- [ ] T047 [US3] Add actionable copy guidelines and message catalog for known MVP failures in `frontend/src/app/content/error-messages.ts`

**Checkpoint**: US3 resilience behavior is consistent and independently verifiable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, evidence capture, and implementation handoff readiness.

- [ ] T048 [P] Run full frontend unit/integration/E2E regression suite and capture results in `docs/qa/frontend-foundation.md`
- [ ] T049 [P] Document SC-001..SC-004 traceability and measured outcomes in `docs/qa/frontend-foundation.md`
- [ ] T050 Validate quickstart readiness steps for `/speckit.implement` and update final go/no-go checklist in `specs/011-frontend-foundation/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): starts immediately.
- Foundational (Phase 2): depends on Setup completion and blocks all user stories.
- User Stories (Phases 3-5): depend on Phase 2 completion; execute in priority order for closed MVP scope (P1 -> P2 -> P3).
- Polish (Phase 6): depends on all in-scope stories completion.

### User Story Dependencies

- US1 (P1): starts after Phase 2; no dependency on US2/US3.
- US2 (P2): starts after US1 MVP validation gate in closed-scope sequencing.
- US3 (P3): starts after US2 baseline core-flow completion.

### Dependency Graph (Story Completion Order)

- Foundation -> US1 -> US2 -> US3 -> Polish

### Within Each User Story

- Tests must be authored first and fail before implementation.
- API adapters before view models.
- View models before page/route integration.
- Story acceptance gate must pass before next priority story starts.

---

## Parallel Execution Examples

## Parallel Example: User Story 1

```bash
Task T013 + T014 + T015
Task T020 + T021 + T022 + T023
```

## Parallel Example: User Story 2

```bash
Task T025 + T026 + T027 + T028 + T029
Task T030 + T031 + T032 + T033
```

## Parallel Example: User Story 3

```bash
Task T039 + T040 + T041 + T042
Task T043 + T044
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2, including constitution exception/amendment approval tasks.
2. Deliver Phase 3 (US1) and pass independent acceptance tests.
3. Stop and validate MVP usability (auth + private navigation).

### Incremental Delivery

1. Foundation complete (Phases 1-2).
2. Deliver US1 (P1) and validate SC-001 and SC-003 coverage.
3. Deliver US2 (P2) and validate SC-002 coverage.
4. Deliver US3 (P3) and validate SC-004 coverage.
5. Run Phase 6 polish and readiness checks.

### Parallel Team Strategy

1. Team completes Setup and Foundational phases together.
2. After Foundation:
   - Dev A: US1 auth/navigation implementation and tests.
   - Dev B: US2 API adapters/view models.
   - Dev C: US3 shared resilience components and messaging.
3. Merge stories in priority order with independent test evidence.

---

## Notes

- All tasks follow checklist format: `- [ ] T### [P?] [US?] Description with file path`.
- Closed sprint scope enforced: no new backend endpoints, no mobile-native implementation, no production hardening.
- Task T006 and T007 are mandatory governance blockers before coding story tasks.
