# Tasks: Runtime Deprecation Cleanup Baseline

**Input**: Design docs from `/specs/010-runtime-deprecation-cleanup/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/runtime-deprecation-continuity.md`, `checklists/requirements.md`

**Tests**: TDD mandatory (RED -> GREEN -> REFACTOR). Contract, integration, and unit validation are required by Constitution Principle II and this feature spec.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare runtime-warning governance artifacts and baseline scaffolding.

- [ ] T001 Create runtime cleanup QA evidence report scaffold in `docs/qa/runtime-deprecation-cleanup.md`
- [ ] T002 Create runtime warning policy document scaffold in `docs/methodology/runtime-warning-policy.md`
- [ ] T003 [P] Create runtime warning capture helper scaffold in `backend/tests/fixtures/runtime_warnings.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared warning/lifecycle validation primitives required before user stories.

**CRITICAL**: No user story can start until this phase is complete.

- [ ] T004 Implement reusable runtime warning decision primitives in `backend/src/services/validation/runtime_warning_policy.py`
- [ ] T005 [P] Implement reusable warning assertion utilities for tests in `backend/tests/fixtures/runtime_warnings.py`
- [ ] T006 [P] Wire runtime warning fixtures and hooks into test bootstrap in `backend/tests/conftest.py`
- [ ] T007 Configure pytest markers/options for runtime warning baseline validation in `backend/pyproject.toml`

**Checkpoint**: Foundation ready. User stories can begin.

---

## Phase 3: User Story 1 - Remove Startup Deprecations (Priority: P1) 🎯 MVP

**Goal**: Migrate deprecated startup wiring to lifespan while preserving bootstrap behavior and existing API contracts.

**Independent Test**: Start app and run contract/integration lifecycle tests with zero deprecated lifecycle warnings.

### Tests for User Story 1 (MANDATORY)

- [ ] T008 [P] [US1] Add runtime continuity contract test for existing API invariants in `backend/tests/contract/runtime/test_runtime_continuity_contract.py`
- [ ] T009 [P] [US1] Add integration test ensuring no lifecycle deprecation warning during startup/shutdown in `backend/tests/integration/runtime/test_lifespan_no_deprecation.py`
- [ ] T010 [P] [US1] Add integration test for bootstrap equivalence before/after lifespan migration in `backend/tests/integration/runtime/test_bootstrap_compatibility.py`

### Implementation for User Story 1

- [ ] T011 [US1] Replace deprecated startup event wiring with FastAPI lifespan context in `backend/src/main.py`
- [ ] T012 [US1] Preserve and validate startup/shutdown observability events in `backend/src/main.py`
- [ ] T013 [US1] Update shared test client bootstrap for lifespan-compliant app execution in `backend/tests/conftest.py`

**Checkpoint**: US1 is independently testable and MVP-ready.

---

## Phase 4: User Story 2 - Stabilize Dependency Warning Surface (Priority: P2)

**Goal**: Reduce recurrent dependency warning noise with explicit treatment actions and no global suppression.

**Independent Test**: Run targeted suite in container and verify warning reduction plus explicit decision mapping for recurrent warnings.

### Tests for User Story 2 (MANDATORY)

- [ ] T014 [P] [US2] Add integration test for recurrent dependency warning classification and action mapping in `backend/tests/integration/runtime/test_dependency_warning_matrix.py`
- [ ] T015 [P] [US2] Add unit tests for runtime warning decision taxonomy in `backend/tests/unit/validation/test_runtime_warning_policy.py`

### Implementation for User Story 2

- [ ] T016 [US2] Implement explicit warning treatment matrix (REMEDIATE, PIN_VERSION, DOCUMENT_EXCEPTION) in `backend/src/services/validation/runtime_warning_policy.py`
- [ ] T017 [US2] Apply scoped warning handling rules without global ignore in `backend/tests/conftest.py`
- [ ] T018 [US2] Update dependency constraints for approved warning treatment actions in `backend/pyproject.toml`
- [ ] T019 [US2] Record baseline pre/post warning comparison evidence in `docs/qa/runtime-deprecation-cleanup.md`

**Checkpoint**: US2 is independently testable with warning-surface evidence.

---

## Phase 5: User Story 3 - Document Runtime Baseline Policy (Priority: P3)

**Goal**: Publish a clear runtime warning policy for PR quality gates and long-term maintenance discipline.

**Independent Test**: Validate documentation completeness and traceability of blocking/non-blocking rules and exception governance.

### Tests for User Story 3 (MANDATORY)

- [ ] T020 [P] [US3] Add documentation contract test for required runtime policy sections and references in `backend/tests/contract/runtime/test_warning_policy_contract.py`

### Implementation for User Story 3

- [ ] T021 [US3] Author runtime warning governance policy with blocking rules and ownership in `docs/methodology/runtime-warning-policy.md`
- [ ] T022 [US3] Add policy validation and PR review flow to feature quickstart in `specs/010-runtime-deprecation-cleanup/quickstart.md`
- [ ] T023 [US3] Align runtime continuity contract evidence references with final policy in `specs/010-runtime-deprecation-cleanup/contracts/runtime-deprecation-continuity.md`

**Checkpoint**: US3 policy is independently reviewable and enforceable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final evidence consolidation, regression verification, and implementation readiness.

- [ ] T024 [P] Run full contract/integration/unit runtime regression and capture final evidence in `docs/qa/runtime-deprecation-cleanup.md`
- [ ] T025 [P] Capture SC-001..SC-004 traceability matrix and closure notes in `docs/qa/runtime-deprecation-cleanup.md`
- [ ] T026 Validate final quickstart execution path and go/no-go checklist in `specs/010-runtime-deprecation-cleanup/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): starts immediately.
- Foundational (Phase 2): depends on Setup completion and blocks all user stories.
- User Stories (Phases 3-5): depend on Phase 2 completion and can run in parallel if capacity exists.
- Polish (Phase 6): depends on all in-scope stories being complete.

### User Story Dependencies

- US1 (P1): starts after Phase 2; no dependency on US2 or US3.
- US2 (P2): starts after Phase 2; independent of US1 behaviorally but sequenced after MVP by priority.
- US3 (P3): starts after Phase 2; depends on US2 warning taxonomy outputs for final policy wording.

### Dependency Graph (Story Completion Order)

- Foundation -> US1 -> US2 -> US3 -> Polish

### Within Each User Story

- Tests must be authored first and fail before implementation.
- Lifecycle/warning primitives before runtime wiring changes.
- Runtime wiring and policy docs before final regression evidence.

---

## Parallel Execution Examples

## Parallel Example: User Story 1

```bash
Task T008 + T009 + T010
Task T011 + T012
```

## Parallel Example: User Story 2

```bash
Task T014 + T015
Task T018 + T019
```

## Parallel Example: User Story 3

```bash
Task T020 + T021
Task T022 + T023
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2.
2. Deliver Phase 3 (US1).
3. Run US1 independent test gate for lifecycle deprecation removal.
4. Demo/deploy MVP baseline cleanup.

### Incremental Delivery

1. Setup + Foundational complete shared runtime governance baseline.
2. US1 (P1): remove lifecycle deprecation with compatibility checks.
3. US2 (P2): reduce dependency warning noise with explicit decisions.
4. US3 (P3): publish policy governance and PR-review enforceability.
5. Polish: consolidate evidence and readiness for implementation handoff.

### Parallel Team Strategy

1. Team completes Phases 1-2 together.
2. After foundation:
   - Dev A: US1 lifecycle migration + compatibility tests.
   - Dev B: US2 warning taxonomy + dependency treatment.
   - Dev C: US3 policy docs + documentation contract checks.
3. Merge each story after independent gate passes.

---

## Notes

- All tasks follow checklist format: `- [ ] T### [P?] [US?] Description with file path`.
- Priority and scope are locked to Sprint 010 (P1 -> P2 -> P3).
- Out-of-scope refactors and product/API contract changes are explicitly excluded.
