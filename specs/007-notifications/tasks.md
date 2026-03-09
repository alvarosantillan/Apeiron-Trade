# Tasks: TRDIA - Notifications and Alerts

**Input**: Design docs from `/specs/007-notifications/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/notifications.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [x] T001 Create notifications module in `backend/src/services/notifications/`
- [x] T002 [P] Create notification schemas in `backend/src/schemas/notifications/`
- [x] T003 [P] Create notification tests in `backend/tests/*/notifications/`

## Phase 2: Foundational

- [x] T004 Implement push provider abstraction in `backend/src/services/notifications/push_provider.py`
- [x] T005 [P] Implement deduplication service in `backend/src/services/notifications/dedup_service.py`
- [x] T006 [P] Implement retry policy service in `backend/src/services/notifications/retry_policy.py`
- [x] T007 Implement token lifecycle manager in `backend/src/services/notifications/token_service.py`

## Phase 3: US1 - Register Devices and Send Trading Alerts (P1)

### Tests

- [x] T008 [P] [US1] Contract test device token upsert in `backend/tests/contract/notifications/test_device_tokens_contract.py`
- [x] T009 [P] [US1] Integration test trading event push delivery in `backend/tests/integration/notifications/test_trading_push_delivery.py`

### Implementation

- [x] T010 [US1] Implement device token endpoints in `backend/src/api/notifications/device_tokens.py`
- [x] T011 [US1] Implement event-to-delivery pipeline in `backend/src/services/notifications/delivery_service.py`

## Phase 4: US2 - Preferences and Critical Priority (P2)

### Tests

- [x] T012 [P] [US2] Contract test preferences update in `backend/tests/contract/notifications/test_preferences_contract.py`
- [x] T013 [P] [US2] Integration test preference filtering in `backend/tests/integration/notifications/test_preference_filtering.py`

### Implementation

- [x] T014 [US2] Implement preference endpoints in `backend/src/api/notifications/preferences.py`
- [x] T015 [US2] Implement critical-priority override policy in `backend/src/services/notifications/priority_policy.py`

## Phase 5: US3 - Delivery Tracking and Retries (P3)

### Tests

- [x] T016 [P] [US3] Integration test transient failure retry in `backend/tests/integration/notifications/test_retry_flow.py`
- [x] T017 [P] [US3] Integration test invalid token drop in `backend/tests/integration/notifications/test_invalid_token_drop.py`

### Implementation

- [x] T018 [US3] Implement delivery status transitions in `backend/src/services/notifications/delivery_status_service.py`
- [x] T019 [US3] Implement history endpoint in `backend/src/api/notifications/history.py`

## Phase 6: Polish

- [x] T020 Validate quickstart scenarios in `specs/007-notifications/quickstart.md`
- [x] T021 Run notifications test baseline in `docs/qa/notifications.md`
