# Tasks: TRDIA - Trading Execution

**Input**: Design docs from `/specs/006-trading-execution/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/trading-execution.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [ ] T001 Create execution module in `backend/src/services/execution/`
- [ ] T002 [P] Create risk module in `backend/src/services/risk/`
- [ ] T003 [P] Create execution tests in `backend/tests/*/trading_execution/`

## Phase 2: Foundational

- [ ] T004 Implement request idempotency service in `backend/src/services/execution/idempotency_service.py`
- [ ] T005 [P] Implement state-machine transition validator in `backend/src/services/execution/state_machine.py`
- [ ] T006 [P] Implement plan-limit validator integration in `backend/src/services/validation/plan_limit_validator.py`
- [ ] T007 Implement operation counter updater in `backend/src/services/counters/weekly_counter_service.py`

## Phase 3: US1 - Validated Spot Execution (P1)

### Tests

- [ ] T008 [P] [US1] Contract test create execution endpoint in `backend/tests/contract/trading_execution/test_create_execution_contract.py`
- [ ] T009 [P] [US1] Integration test successful real execution in `backend/tests/integration/trading_execution/test_real_execution_success.py`

### Implementation

- [ ] T010 [US1] Implement create execution endpoint in `backend/src/api/trading/executions_create.py`
- [ ] T011 [US1] Implement execution orchestration service in `backend/src/services/execution/execution_orchestrator.py`

## Phase 4: US2 - Enforcement and Blocking (P2)

### Tests

- [ ] T012 [P] [US2] Integration test weekly limit exceeded in `backend/tests/integration/trading_execution/test_limit_block.py`
- [ ] T013 [P] [US2] Integration test insufficient balance in `backend/tests/integration/trading_execution/test_balance_block.py`

### Implementation

- [ ] T014 [US2] Implement block reason mapper in `backend/src/services/execution/block_reason_mapper.py`
- [ ] T015 [US2] Persist blocked execution states in `backend/src/services/execution/execution_repository.py`

## Phase 5: US3 - Paper Mode and Reconciliation (P3)

### Tests

- [ ] T016 [P] [US3] Integration test paper mode no counter increment in `backend/tests/integration/trading_execution/test_paper_no_count.py`
- [ ] T017 [P] [US3] Integration test pending reconciliation flow in `backend/tests/integration/trading_execution/test_reconciliation_flow.py`

### Implementation

- [ ] T018 [US3] Implement paper execution path in `backend/src/services/execution/paper_execution_service.py`
- [ ] T019 [US3] Implement reconciliation worker in `backend/src/workers/execution_reconciliation_worker.py`

## Phase 6: Polish

- [ ] T020 Validate quickstart scenarios in `specs/006-trading-execution/quickstart.md`
- [ ] T021 Run execution test baseline in `docs/qa/trading-execution.md`
