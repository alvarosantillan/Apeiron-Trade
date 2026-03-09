# Runtime Warning Policy

## Purpose

Define a stable policy for runtime warning governance in backend reviews, with explicit treatment and ownership.

## Scope

- Applies to backend runtime and test execution.
- Applies in local runs and container validation for `Apeiron-Trade`.
- Excludes business-feature behavior changes.

## Blocking Rules

- Any lifecycle deprecation warning related to deprecated FastAPI startup/shutdown APIs is blocking.
- Any unknown warning class is blocking until triaged with explicit decision.

## Non-Blocking Rules

- Known upstream dependency warnings may be non-blocking only with explicit decision.
- Non-blocking status requires owner, rationale, and next review date.

## Treatment Matrix

- `REMEDIATE`: fix code usage or integration to eliminate warning at source.
- `PIN_VERSION`: constrain dependency version range while waiting for upstream compatibility.
- `DOCUMENT_EXCEPTION`: temporary accepted warning with owner and review date.

## Prohibited Practices

- Global warning suppression in pytest or runtime bootstrap without issue-specific rationale.
- Silent acceptance of new warnings without taxonomy classification.

## Ownership and Review

- Runtime warning decisions are owned by backend maintainers.
- Every `DOCUMENT_EXCEPTION` entry must be re-reviewed in a subsequent sprint.
- PR review must verify evidence references in `docs/qa/runtime-deprecation-cleanup.md`.

## Required Evidence for PR Approval

- Runtime warning test results for contract/integration/unit scope.
- Confirmation that lifecycle deprecation count is zero.
- Updated QA traceability for SC-001..SC-004.
