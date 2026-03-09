# Tasks: TRDIA - Persistence and Hardening Baseline

**Input**: Design docs from `/specs/009-persistence-hardening/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/persistence-hardening.openapi.yaml`

**Tests**: TDD mandatory (RED -> GREEN -> REFACTOR). Contract, integration, and unit coverage is required by spec and constitution.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Enable PostgreSQL persistence tooling and test scaffolding.

- [ ] T001 Add PostgreSQL persistence dependencies (`sqlalchemy`, `alembic`, `psycopg`) in `backend/pyproject.toml`
- [ ] T002 Create Alembic base config for backend service in `backend/alembic.ini`
- [ ] T003 [P] Create Alembic migration environment bootstrap in `backend/migrations/env.py`
- [ ] T004 [P] Create persistence package scaffold in `backend/src/services/persistence/__init__.py`
- [ ] T005 [P] Add reusable PostgreSQL test bootstrap fixture in `backend/tests/fixtures/postgres_bootstrap.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core persistence and hardening primitives required before user stories.

**CRITICAL**: No user story can start until this phase is complete.

- [ ] T006 Implement SQLAlchemy engine/session factory in `backend/src/services/persistence/database.py`
- [ ] T007 [P] Implement shared ORM metadata base in `backend/src/services/persistence/models/base.py`
- [ ] T008 [P] Implement controlled DB error taxonomy and mapping in `backend/src/services/persistence/errors.py`
- [ ] T009 Implement API-level persistence error handler in `backend/src/api/middleware/persistence_error_handler.py`
- [ ] T010 [P] Implement persistence audit logger with sensitive-data redaction in `backend/src/services/audit/persistence_audit.py`
- [ ] T011 Create baseline migration for auth/execution/notifications/ai_agent tables in `backend/migrations/versions/009_persistence_baseline.py`
- [ ] T012 Wire startup DB connectivity and migration gate in `backend/src/main.py`

**Checkpoint**: Foundation ready. User stories can begin.

---

## Phase 3: User Story 1 - Persistencia real de datos criticos (Priority: P1) 🎯 MVP

**Goal**: Persist auth, execution, notifications, and AI config in PostgreSQL while preserving API contracts.

**Independent Test**: Create records, restart backend, and verify state remains available with unchanged API behavior.

### Tests for User Story 1 (MANDATORY)

- [ ] T013 [P] [US1] Extend login/refresh contract coverage for persistence continuity in `backend/tests/contract/auth/test_login_contract.py`
- [ ] T014 [P] [US1] Extend execution contract coverage for persisted idempotent replay in `backend/tests/contract/trading_execution/test_create_execution_contract.py`
- [ ] T015 [P] [US1] Add notifications persistence contract coverage in `backend/tests/contract/notifications/test_history_persistence_contract.py`
- [ ] T016 [P] [US1] Extend AI config contract read-after-write persistence coverage in `backend/tests/contract/ai_agent/test_config_contract.py`
- [ ] T017 [P] [US1] Add integration restart survival scenario across critical domains in `backend/tests/integration/persistence/test_restart_data_survival.py`
- [ ] T018 [P] [US1] Add auth session persistence integration scenario in `backend/tests/integration/auth/test_session_persistence.py`

### Implementation for User Story 1

- [ ] T019 [P] [US1] Replace in-memory user persistence with PostgreSQL-backed store in `backend/src/services/auth/user_store.py`
- [ ] T020 [P] [US1] Replace in-memory auth session persistence with PostgreSQL-backed session service in `backend/src/services/auth/session_service.py`
- [ ] T021 [P] [US1] Replace in-memory execution repository with PostgreSQL repository in `backend/src/services/execution/execution_repository.py`
- [ ] T022 [P] [US1] Replace in-memory notification history store with PostgreSQL repository in `backend/src/services/notifications/history_store.py`
- [ ] T023 [P] [US1] Replace in-memory AI config store with PostgreSQL repository in `backend/src/services/ai_agent/config_store.py`
- [ ] T024 [US1] Preserve request-id idempotency with DB-backed checks in `backend/src/services/execution/idempotency_service.py`
- [ ] T025 [US1] Preserve trading endpoint contract semantics on persistent backend in `backend/src/api/trading/router.py`
- [ ] T026 [US1] Preserve auth endpoint contract semantics on persistent backend in `backend/src/api/auth/router.py`
- [ ] T027 [US1] Preserve notifications endpoint contract semantics on persistent backend in `backend/src/api/notifications/router.py`
- [ ] T028 [US1] Preserve AI agent endpoint contract semantics on persistent backend in `backend/src/api/ai_agent/router.py`

**Checkpoint**: US1 is independently testable and demo-ready (MVP).

---

## Phase 4: User Story 2 - Configuracion clara para DB host y contenedor (Priority: P2)

**Goal**: Provide reproducible host/container DB setup and smoke verification path.

**Independent Test**: Fresh environment can connect, apply migrations, and pass smoke CRUD checks.

### Tests for User Story 2 (MANDATORY by spec FR-010)

- [ ] T029 [P] [US2] Add integration test for host-container DB connectivity using host override in `backend/tests/integration/persistence/test_host_container_connectivity.py`
- [ ] T030 [P] [US2] Add smoke integration test for migration plus CRUD baseline in `backend/tests/integration/persistence/test_smoke_persistence_baseline.py`

### Implementation for User Story 2

- [ ] T031 [US2] Implement canonical DB environment settings loader in `backend/src/services/validation/db_settings.py`
- [ ] T032 [US2] Integrate DB settings loader into app bootstrap in `backend/src/main.py`
- [ ] T033 [US2] Document host and container DB setup and smoke flow in `specs/009-persistence-hardening/quickstart.md`
- [ ] T034 [US2] Add backend container DB environment wiring in `docker-compose.yml`
- [ ] T035 [US2] Add persistence QA runbook and execution commands in `docs/qa/persistence-hardening.md`
- [ ] T036 [US2] Add persistence smoke test marker/config in `backend/pyproject.toml`

**Checkpoint**: US2 can be executed independently on a clean environment.

---

## Phase 5: User Story 3 - Hardening operativo minimo para pre-produccion (Priority: P3)

**Goal**: Add controlled failure handling, auditability, and operational hardening for persistence flows.

**Independent Test**: Simulate transient DB failures and verify controlled API response plus audited event.

### Tests for User Story 3 (MANDATORY)

- [ ] T037 [P] [US3] Add controlled DB outage integration scenario in `backend/tests/integration/persistence/test_db_outage_controlled_error.py`
- [ ] T038 [P] [US3] Add unit tests for persistence error mapping and audit redaction in `backend/tests/unit/persistence/test_error_audit_mapping.py`

### Implementation for User Story 3

- [ ] T039 [US3] Implement transactional write wrapper for repository operations in `backend/src/services/persistence/transaction_manager.py`
- [ ] T040 [US3] Integrate audited controlled-failure behavior into execution orchestration in `backend/src/services/execution/execution_orchestrator.py`
- [ ] T041 [US3] Integrate audited controlled-failure behavior into notification delivery writes in `backend/src/services/notifications/delivery_service.py`
- [ ] T042 [US3] Implement persistence observability counters/histogram emitters in `backend/src/services/persistence/metrics.py`
- [ ] T043 [US3] Add hardening operations checklist and rollback notes in `docs/qa/persistence-hardening.md`

**Checkpoint**: US3 is independently testable for pre-production hardening baseline.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, performance baseline support, and release evidence.

- [ ] T044 [P] Run full contract/integration regression and record evidence in `docs/qa/persistence-hardening.md`
- [ ] T045 [P] Add query index migration for critical persistence paths in `backend/migrations/versions/009_persistence_indexes.py`
- [ ] T046 Validate complete quickstart on clean environment and capture final notes in `specs/009-persistence-hardening/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): starts immediately.
- Foundational (Phase 2): depends on Setup completion and blocks all user stories.
- User Stories (Phases 3-5): all depend on Phase 2 completion.
- Polish (Phase 6): depends on completed user stories in scope.

### User Story Dependencies

- US1 (P1): starts after Phase 2; no dependency on US2 or US3.
- US2 (P2): starts after Phase 2; can run in parallel with US1 if capacity exists, but MVP sequence is US1 first.
- US3 (P3): starts after Phase 2; should consume persistence primitives from US1/Phase 2.

### Dependency Graph (Story Completion Order)

- Foundation -> US1 -> US2 -> US3 -> Polish

### Within Each User Story

- Tests must be authored first and fail before implementation.
- Persistence/repository changes before API adaptation.
- API adaptation before regression verification.

---

## Parallel Execution Examples

## Parallel Example: User Story 1

```bash
Task T013 + T014 + T015 + T016 + T017 + T018
Task T019 + T020 + T021 + T022 + T023
```

## Parallel Example: User Story 2

```bash
Task T029 + T030
Task T033 + T034 + T035 + T036
```

## Parallel Example: User Story 3

```bash
Task T037 + T038
Task T040 + T041
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2.
2. Deliver Phase 3 (US1).
3. Run US1 independent tests and restart-survival checks.
4. Demo/deploy MVP persistence baseline.

### Incremental Delivery

1. Foundation (Phases 1-2).
2. US1 (P1) for durable critical state.
3. US2 (P2) for reproducible environment setup/smoke.
4. US3 (P3) for hardening and controlled failures.
5. Polish for regression evidence and release readiness.

### Parallel Team Strategy

1. Team completes Phases 1-2 together.
2. After foundation:
   - Dev A: US1 repositories + API compatibility
   - Dev B: US2 environment/smoke path
   - Dev C: US3 hardening and audit/error flows
3. Merge each story after independent test gate passes.

---

## Notes

- All tasks follow checklist format: `- [ ] T### [P?] [US?] Description with file path`.
- Scope is closed to Sprint 009 requirements only.
- Out-of-scope items from spec remain excluded by design.
