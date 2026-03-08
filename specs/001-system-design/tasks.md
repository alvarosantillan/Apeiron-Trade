# Tasks: TRDIA - System Design Foundation

**Input**: Design documents from `/specs/001-system-design/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/platform-core.openapi.yaml

**Tests**: Mandatory by constitution (TDD). Every implementation task must be preceded by failing tests.

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create backend module skeleton in `backend/src/{api,trading,agents,strategies,analytics,payments,workers}/`
- [ ] T002 [P] Create frontend module skeleton in `frontend/src/{screens,features,services,state}/`
- [ ] T003 [P] Add base environment templates in `backend/.env.example` and `frontend/.env.example`
- [ ] T004 Add architecture README in `docs/architecture/overview.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**CRITICAL**: No feature implementation starts before these are complete.

- [ ] T005 Setup DB migration baseline for core entities in `backend/src/models/` and migration scripts
- [ ] T006 [P] Implement auth middleware and request identity context in `backend/src/api/middleware/`
- [ ] T007 [P] Implement centralized validation/error handling in `backend/src/api/errors/` and `backend/src/schemas/common/`
- [ ] T008 [P] Implement encryption service for external credentials in `backend/src/services/security/crypto_service.py`
- [ ] T009 Implement audit logging foundation in `backend/src/services/audit/`
- [ ] T010 [P] Implement metrics/logging bootstrap in `backend/src/services/observability/`
- [ ] T011 Define async worker base config in `backend/src/workers/`

**Checkpoint**: Foundation ready for story work.

---

## Phase 3: User Story 1 - Onboarding Foundation (Priority: P1) 🎯 MVP

**Goal**: Base flow for new user onboarding context (auth, plan free default, profile summary capability).

**Independent Test**: Authenticated user can retrieve platform profile summary with defaults.

### Tests (TDD First)

- [ ] T012 [P] [US1] Contract test for `GET /v1/platform/profile-summary` in `backend/tests/contract/test_platform_profile_summary.py`
- [ ] T013 [P] [US1] Integration test for new user default plan and counters in `backend/tests/integration/test_onboarding_defaults.py`

### Implementation

- [ ] T014 [US1] Implement profile summary endpoint in `backend/src/api/platform/profile_summary.py`
- [ ] T015 [US1] Implement default plan/counter initialization service in `backend/src/services/users/bootstrap_service.py`
- [ ] T016 [US1] Add audit event on first summary access in `backend/src/services/audit/`

---

## Phase 4: User Story 2 - Manual Suggestions Baseline (Priority: P2)

**Goal**: Definir el baseline técnico para flujo manual (free) con validación backend.

**Independent Test**: Capability matrix for Free user exposes manual-only execution mode.

### Tests (TDD First)

- [ ] T017 [P] [US2] Contract test for `GET /v1/platform/capabilities` in `backend/tests/contract/test_platform_capabilities.py`
- [ ] T018 [P] [US2] Integration test for free plan capability enforcement in `backend/tests/integration/test_free_capabilities.py`

### Implementation

- [ ] T019 [US2] Implement capabilities endpoint in `backend/src/api/platform/capabilities.py`
- [ ] T020 [US2] Implement plan-to-capability mapper in `backend/src/services/plans/capability_mapper.py`
- [ ] T021 [US2] Add validation policy for manual-only Free mode in `backend/src/services/validation/plan_policy.py`

---

## Phase 5: User Story 3 - Automatic Mode Eligibility Baseline (Priority: P3)

**Goal**: Establecer base de elegibilidad para ejecución automática en Plus/Premium.

**Independent Test**: Plus/Premium capability responses include automatic mode; Free does not.

### Tests (TDD First)

- [ ] T022 [P] [US3] Integration test for plus/premium automatic eligibility in `backend/tests/integration/test_paid_plan_capabilities.py`
- [ ] T023 [P] [US3] Unit test for eligibility rules in `backend/tests/unit/test_plan_policy.py`

### Implementation

- [ ] T024 [US3] Extend `plan_policy` for automatic mode checks in `backend/src/services/validation/plan_policy.py`
- [ ] T025 [US3] Add policy errors/messages contract in `backend/src/schemas/platform/policy_errors.py`

---

## Phase 6: User Story 4 - Subscription Backbone (Priority: P4)

**Goal**: Definir infraestructura base para lifecycle de suscripciones y sincronización de estado.

**Independent Test**: Subscription state transitions reflect in profile summary and capabilities.

### Tests (TDD First)

- [ ] T026 [P] [US4] Integration test for subscription state transitions in `backend/tests/integration/test_subscription_state_baseline.py`
- [ ] T027 [P] [US4] Unit test for transition rules in `backend/tests/unit/test_subscription_rules.py`

### Implementation

- [ ] T028 [US4] Implement subscription domain model baseline in `backend/src/models/subscription.py`
- [ ] T029 [US4] Implement subscription status service in `backend/src/services/subscriptions/status_service.py`
- [ ] T030 [US4] Wire profile summary with subscription status in `backend/src/api/platform/profile_summary.py`

---

## Phase 7: User Story 5 - Paper Trading Baseline (Priority: P5)

**Goal**: Definir reglas base de simulación sin consumo de límite semanal.

**Independent Test**: Simulated operation does not increment weekly operation counter.

### Tests (TDD First)

- [ ] T031 [P] [US5] Integration test for paper mode non-consumption in `backend/tests/integration/test_paper_counter_behavior.py`
- [ ] T032 [P] [US5] Unit test for counter increment policy in `backend/tests/unit/test_operation_counter_policy.py`

### Implementation

- [ ] T033 [US5] Implement operation counter policy service in `backend/src/services/counters/operation_counter_policy.py`
- [ ] T034 [US5] Add simulation flag validation schema in `backend/src/schemas/trading/execution_mode.py`
- [ ] T035 [US5] Add audit event for simulation execution path in `backend/src/services/audit/`

---

## Phase 8: Polish & Cross-Cutting

- [ ] T036 [P] Validate quickstart architecture checklist in `specs/001-system-design/quickstart.md`
- [ ] T037 [P] Add/update runbooks in `docs/runbooks/{security,observability}.md`
- [ ] T038 Execute full test suite and capture baseline report in `docs/qa/system-design-baseline.md`
- [ ] T039 Review constitution compliance and document deviations (if any) in `specs/001-system-design/plan.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Stories (Phase 3-7) -> Phase 8.
- Stories can run in parallel after Phase 2 if staffed, but recommended order is P1 -> P5.
- Within each story: tests first (RED), then implementation (GREEN), then refactor.

## Implementation Strategy

- Complete this feature as architectural baseline before deep implementation of feature-specific stories.
- After baseline completion, execute `/speckit.tasks` in order for `002` to `008`.
