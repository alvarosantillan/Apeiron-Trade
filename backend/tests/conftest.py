import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth.login_protection import login_protection
from services.auth.user_store import store
from services.ai_agent.config_store import ai_agent_config_store
from services.ai_agent.decision_repository import ai_decision_repository
from services.audit.trade_detail_audit import trade_detail_audit_store
from services.persistence.database import get_engine, initialize_database, reset_database_engine
from services.persistence.models.base import Base
from services.notifications.dedup_service import notification_dedup_service
from services.notifications.history_store import notification_history_store
from services.notifications.preference_store import notification_preference_store
from services.notifications.token_service import notification_token_service
from services.payments.event_idempotency import idempotency_store
from services.binance.credential_service import credential_store
from services.execution.execution_repository import execution_repository
from services.execution.execute_order_service import balance_store
from services.execution.idempotency_service import idempotency_service
from services.subscriptions.store import subscription_store
from services.validation.plan_limit_validator import plan_limit_validator


@pytest.fixture(scope="session", autouse=True)
def _configure_test_database(tmp_path_factory: pytest.TempPathFactory) -> None:
    db_dir = tmp_path_factory.mktemp("db")
    db_path = Path(db_dir) / "trdia-tests.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"
    reset_database_engine()
    initialize_database()


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_store() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    store.reset_for_tests()
    login_protection._failed_by_email.clear()
    ai_decision_repository._by_user.clear()
    trade_detail_audit_store._events.clear()
    notification_token_service._by_user.clear()
    notification_preference_store._by_user.clear()
    notification_dedup_service._seen.clear()
    idempotency_store._seen_event_ids.clear()
    subscription_store._status_by_user.clear()
    credential_store._by_user.clear()
    idempotency_service._seen.clear()
    balance_store._balance.clear()
    plan_limit_validator._weekly_usage.clear()
