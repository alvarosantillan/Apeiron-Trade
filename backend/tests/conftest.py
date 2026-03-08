import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth.user_store import store


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_store() -> None:
    store._users_by_email.clear()
    store._refresh_tokens.clear()
