import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth.login_protection import login_protection
from services.auth.user_store import store


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_store() -> None:
    store._users_by_email.clear()
    store._users_by_oauth.clear()
    store._refresh_tokens.clear()
    login_protection._failed_by_email.clear()
