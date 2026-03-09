from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import warnings

import pytest

from services.validation.runtime_warning_policy import (
    RuntimeWarningDecision,
    RuntimeWarningRecord,
    WarningSeverity,
    classify_runtime_warning,
    is_lifecycle_deprecation,
)


@dataclass(frozen=True)
class CapturedRuntimeWarning:
    category: str
    message: str
    module: str


@contextmanager
def capture_runtime_warnings() -> list[CapturedRuntimeWarning]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("default")
        captured: list[CapturedRuntimeWarning] = []
        yield captured

        for item in caught:
            module = getattr(item, "module", "") or ""
            captured.append(
                CapturedRuntimeWarning(
                    category=item.category.__name__,
                    message=str(item.message),
                    module=module,
                )
            )


def classify_warnings(captured: list[CapturedRuntimeWarning]) -> list[RuntimeWarningDecision]:
    return [
        classify_runtime_warning(
            RuntimeWarningRecord(category=item.category, message=item.message, module=item.module)
        )
        for item in captured
    ]


def assert_no_lifecycle_deprecations(captured: list[CapturedRuntimeWarning]) -> None:
    offenders = [
        item
        for item in captured
        if is_lifecycle_deprecation(
            RuntimeWarningRecord(category=item.category, message=item.message, module=item.module)
        )
    ]
    assert not offenders, f"Lifecycle deprecation warnings detected: {offenders}"


def assert_no_blocking_warnings(captured: list[CapturedRuntimeWarning]) -> None:
    decisions = classify_warnings(captured)
    blocking = [item for item in decisions if item.severity == WarningSeverity.BLOCKING]
    assert not blocking, f"Blocking runtime warnings detected: {blocking}"


@pytest.fixture
def runtime_warning_capture() -> list[CapturedRuntimeWarning]:
    with capture_runtime_warnings() as captured:
        yield captured
