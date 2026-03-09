import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth.login_protection import login_protection
from services.auth.user_store import store
from services.ai_agent.config_store import ai_agent_config_store
from services.ai_agent.decision_repository import ai_decision_repository
from services.payments.event_idempotency import idempotency_store
from services.binance.credential_service import credential_store
from services.execution.execution_repository import execution_repository
from services.execution.execute_order_service import balance_store
from services.execution.idempotency_service import idempotency_service
from services.subscriptions.store import subscription_store
from services.validation.plan_limit_validator import plan_limit_validator


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_store() -> None:
    store._users_by_email.clear()
    store._users_by_oauth.clear()
    store._refresh_tokens.clear()
    login_protection._failed_by_email.clear()
    ai_agent_config_store._by_user.clear()
    ai_decision_repository._by_user.clear()
    idempotency_store._seen_event_ids.clear()
    subscription_store._status_by_user.clear()
    credential_store._by_user.clear()
    idempotency_service._seen.clear()
    execution_repository._executions.clear()
    execution_repository._by_user.clear()
    execution_repository._by_id.clear()
    balance_store._balance.clear()
    plan_limit_validator._weekly_usage.clear()
