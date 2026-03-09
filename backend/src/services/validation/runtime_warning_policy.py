from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WarningDecision(str, Enum):
    REMEDIATE = "REMEDIATE"
    PIN_VERSION = "PIN_VERSION"
    DOCUMENT_EXCEPTION = "DOCUMENT_EXCEPTION"


class WarningSeverity(str, Enum):
    BLOCKING = "BLOCKING"
    NON_BLOCKING = "NON_BLOCKING"


@dataclass(frozen=True)
class RuntimeWarningDecision:
    decision: WarningDecision
    severity: WarningSeverity
    rationale: str


@dataclass(frozen=True)
class RuntimeWarningRecord:
    category: str
    message: str
    module: str = ""


def classify_runtime_warning(record: RuntimeWarningRecord) -> RuntimeWarningDecision:
    message = record.message.lower()
    category = record.category.lower()
    module = record.module.lower()

    if "on_event is deprecated" in message or "lifespan event handlers are deprecated" in message:
        return RuntimeWarningDecision(
            decision=WarningDecision.REMEDIATE,
            severity=WarningSeverity.BLOCKING,
            rationale="Deprecated lifecycle APIs must be migrated to lifespan.",
        )

    if "passlib" in module or ("deprecationwarning" in category and "crypt" in message):
        return RuntimeWarningDecision(
            decision=WarningDecision.DOCUMENT_EXCEPTION,
            severity=WarningSeverity.NON_BLOCKING,
            rationale="Known upstream warning; track with owner and review date.",
        )

    if "httpx" in module and "deprecated" in message:
        return RuntimeWarningDecision(
            decision=WarningDecision.PIN_VERSION,
            severity=WarningSeverity.NON_BLOCKING,
            rationale="Pin dependency range while upstream compatibility stabilizes.",
        )

    return RuntimeWarningDecision(
        decision=WarningDecision.REMEDIATE,
        severity=WarningSeverity.BLOCKING,
        rationale="Unknown runtime warning defaults to blocking until triaged.",
    )


def is_lifecycle_deprecation(record: RuntimeWarningRecord) -> bool:
    message = record.message.lower()
    return "on_event is deprecated" in message or "lifespan event handlers are deprecated" in message
