# Tasks: TRDIA - Dashboard and History

**Input**: Design docs from `/specs/008-dashboard-history/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/dashboard-history.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [ ] T001 Create dashboard/history modules in `backend/src/services/{dashboard,history,kpi}/`
- [ ] T002 [P] Create API schemas in `backend/src/schemas/dashboard/` and `backend/src/schemas/history/`
- [ ] T003 [P] Create tests structure in `backend/tests/*/dashboard_history/`

## Phase 2: Foundational

- [ ] T004 Implement dashboard snapshot composer in `backend/src/services/dashboard/snapshot_service.py`
- [ ] T005 [P] Implement history filter validator in `backend/src/services/history/filter_validator.py`
- [ ] T006 [P] Implement cursor pagination service in `backend/src/services/history/pagination_service.py`
- [ ] T007 Implement KPI aggregation service in `backend/src/services/kpi/kpi_service.py`

## Phase 3: US1 - Dashboard Summary (P1)

### Tests

- [ ] T008 [P] [US1] Contract test dashboard summary endpoint in `backend/tests/contract/dashboard_history/test_dashboard_summary_contract.py`
- [ ] T009 [P] [US1] Integration test dashboard load for active user in `backend/tests/integration/dashboard_history/test_dashboard_load.py`

### Implementation

- [ ] T010 [US1] Implement `GET /v1/dashboard/summary` in `backend/src/api/analytics/dashboard_summary.py`
- [ ] T011 [US1] Integrate plan/counter/bot status mapping in `backend/src/services/dashboard/snapshot_service.py`

## Phase 4: US2 - Filtered Trade History (P2)

### Tests

- [ ] T012 [P] [US2] Contract test history list endpoint in `backend/tests/contract/dashboard_history/test_history_contract.py`
- [ ] T013 [P] [US2] Integration test combined filters and pagination in `backend/tests/integration/dashboard_history/test_history_filters.py`

### Implementation

- [ ] T014 [US2] Implement `GET /v1/history/trades` in `backend/src/api/analytics/trade_history.py`
- [ ] T015 [US2] Implement history query service in `backend/src/services/history/history_query_service.py`

## Phase 5: US3 - Trade Detail and KPIs (P3)

### Tests

- [ ] T016 [P] [US3] Contract test trade detail endpoint in `backend/tests/contract/dashboard_history/test_trade_detail_contract.py`
- [ ] T017 [P] [US3] Contract test KPI endpoint in `backend/tests/contract/dashboard_history/test_kpi_contract.py`
- [ ] T018 [P] [US3] Integration test detail access audit in `backend/tests/integration/dashboard_history/test_detail_audit.py`

### Implementation

- [ ] T019 [US3] Implement `GET /v1/history/trades/{tradeId}` in `backend/src/api/analytics/trade_detail.py`
- [ ] T020 [US3] Implement `GET /v1/dashboard/kpis` in `backend/src/api/analytics/dashboard_kpis.py`
- [ ] T021 [US3] Implement detail-access audit logging in `backend/src/services/audit/trade_detail_audit.py`

## Phase 6: Polish

- [ ] T022 Validate quickstart scenarios in `specs/008-dashboard-history/quickstart.md`
- [ ] T023 Run dashboard/history test baseline in `docs/qa/dashboard-history.md`
