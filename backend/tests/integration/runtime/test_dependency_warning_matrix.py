import pytest

from services.validation.runtime_warning_policy import WarningDecision, WarningSeverity
from tests.fixtures.runtime_warnings import CapturedRuntimeWarning, classify_warnings


@pytest.mark.runtime
@pytest.mark.runtime_warning_policy
def test_dependency_warning_matrix_maps_actions_explicitly():
    captured = [
        CapturedRuntimeWarning(
            category="DeprecationWarning",
            message="on_event is deprecated, use lifespan event handlers instead",
            module="fastapi.applications",
        ),
        CapturedRuntimeWarning(
            category="DeprecationWarning",
            message="'crypt' is deprecated and slated for removal",
            module="passlib.handlers",
        ),
        CapturedRuntimeWarning(
            category="DeprecationWarning",
            message="Deprecated transport behavior in httpx",
            module="httpx._client",
        ),
    ]

    decisions = classify_warnings(captured)

    assert decisions[0].decision == WarningDecision.REMEDIATE
    assert decisions[0].severity == WarningSeverity.BLOCKING

    assert decisions[1].decision == WarningDecision.DOCUMENT_EXCEPTION
    assert decisions[1].severity == WarningSeverity.NON_BLOCKING

    assert decisions[2].decision == WarningDecision.PIN_VERSION
    assert decisions[2].severity == WarningSeverity.NON_BLOCKING
