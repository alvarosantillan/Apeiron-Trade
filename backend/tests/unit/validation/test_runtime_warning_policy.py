from services.validation.runtime_warning_policy import (
    RuntimeWarningRecord,
    WarningDecision,
    WarningSeverity,
    classify_runtime_warning,
    is_lifecycle_deprecation,
)


def test_runtime_warning_policy_lifecycle_is_blocking_and_remediate():
    decision = classify_runtime_warning(
        RuntimeWarningRecord(
            category="DeprecationWarning",
            message="on_event is deprecated, use lifespan event handlers instead",
            module="fastapi.applications",
        )
    )

    assert decision.decision == WarningDecision.REMEDIATE
    assert decision.severity == WarningSeverity.BLOCKING


def test_runtime_warning_policy_known_dependency_warnings_are_non_blocking_with_action():
    passlib_decision = classify_runtime_warning(
        RuntimeWarningRecord(
            category="DeprecationWarning",
            message="'crypt' is deprecated and slated for removal",
            module="passlib.handlers",
        )
    )
    httpx_decision = classify_runtime_warning(
        RuntimeWarningRecord(
            category="DeprecationWarning",
            message="Deprecated transport behavior in httpx",
            module="httpx._client",
        )
    )

    assert passlib_decision.decision == WarningDecision.DOCUMENT_EXCEPTION
    assert passlib_decision.severity == WarningSeverity.NON_BLOCKING

    assert httpx_decision.decision == WarningDecision.PIN_VERSION
    assert httpx_decision.severity == WarningSeverity.NON_BLOCKING


def test_runtime_warning_policy_unknown_warning_defaults_to_blocking():
    decision = classify_runtime_warning(
        RuntimeWarningRecord(
            category="UserWarning",
            message="Unexpected runtime warning",
            module="custom.module",
        )
    )

    assert decision.decision == WarningDecision.REMEDIATE
    assert decision.severity == WarningSeverity.BLOCKING


def test_lifecycle_deprecation_detector():
    lifecycle = RuntimeWarningRecord(
        category="DeprecationWarning",
        message="Lifespan event handlers are deprecated",
        module="fastapi.applications",
    )
    non_lifecycle = RuntimeWarningRecord(
        category="DeprecationWarning",
        message="'crypt' is deprecated",
        module="passlib.handlers",
    )

    assert is_lifecycle_deprecation(lifecycle)
    assert not is_lifecycle_deprecation(non_lifecycle)
