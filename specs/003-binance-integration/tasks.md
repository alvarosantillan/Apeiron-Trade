# Tasks: TRDIA - Binance Integration

**Input**: Design docs from `/specs/003-binance-integration/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/trading.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [ ] T001 Create Binance integration module in `backend/src/services/binance/`
- [ ] T002 [P] Create trading schemas in `backend/src/schemas/trading/`
- [ ] T003 [P] Create tests structure under `backend/tests/*/trading/`

## Phase 2: Foundational

- [ ] T004 Implement credential encryption/decryption adapter in `backend/src/services/binance/credential_service.py`
- [ ] T005 [P] Implement exchange client abstraction in `backend/src/services/binance/client.py`
- [ ] T006 [P] Implement symbol/precision validator in `backend/src/services/binance/market_rules.py`
- [ ] T007 Implement idempotency guard in `backend/src/services/execution/idempotency_service.py`

## Phase 3: US1 - Store and Validate Credentials (P1)

### Tests

- [ ] T008 [P] [US1] Contract test credentials endpoint in `backend/tests/contract/trading/test_credentials_contract.py`
- [ ] T009 [P] [US1] Integration test credential validation in `backend/tests/integration/trading/test_credentials_validation.py`

### Implementation

- [ ] T010 [US1] Implement credentials upsert endpoint in `backend/src/api/trading/credentials.py`
- [ ] T011 [US1] Implement active-credentials status endpoint in `backend/src/api/trading/credentials_status.py`

## Phase 4: US2 - Execute Spot Orders (P2)

### Tests

- [ ] T012 [P] [US2] Contract test execute endpoint in `backend/tests/contract/trading/test_execution_contract.py`
- [ ] T013 [P] [US2] Integration test successful execution in `backend/tests/integration/trading/test_execute_success.py`
- [ ] T014 [P] [US2] Integration test insufficient balance in `backend/tests/integration/trading/test_execute_balance_fail.py`

### Implementation

- [ ] T015 [US2] Implement execute order service in `backend/src/services/execution/execute_order_service.py`
- [ ] T016 [US2] Implement execute endpoint in `backend/src/api/trading/executions.py`
- [ ] T017 [US2] Persist execution results in `backend/src/services/execution/execution_repository.py`

## Phase 5: US3 - Paper Trading and Limits (P3)

### Tests

- [ ] T018 [P] [US3] Integration test paper execution non-consumption in `backend/tests/integration/trading/test_paper_mode.py`
- [ ] T019 [P] [US3] Unit test weekly counter rule in `backend/tests/unit/trading/test_weekly_counter.py`

### Implementation

- [ ] T020 [US3] Implement paper execution adapter in `backend/src/services/execution/paper_execution_service.py`
- [ ] T021 [US3] Integrate plan-limit validation in `backend/src/services/validation/plan_limit_validator.py`

## Phase 6: Polish

- [ ] T022 Run trading integration test suite and baseline report in `docs/qa/binance-integration.md`
- [ ] T023 Validate quickstart scenarios in `specs/003-binance-integration/quickstart.md`
