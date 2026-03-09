from fastapi.testclient import TestClient
import pytest

from main import app
from tests.fixtures.runtime_warnings import (
    assert_no_lifecycle_deprecations,
    capture_runtime_warnings,
)


@pytest.mark.runtime
@pytest.mark.runtime_warning_policy
def test_lifespan_startup_shutdown_emits_no_lifecycle_deprecation():
    with capture_runtime_warnings() as captured:
        with TestClient(app) as client:
            response = client.get("/openapi.json")
            assert response.status_code == 200

    assert_no_lifecycle_deprecations(captured)
