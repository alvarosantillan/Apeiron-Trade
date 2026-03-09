from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]


def test_runtime_warning_policy_document_contract_sections_exist():
    policy_path = REPO_ROOT / "docs/methodology/runtime-warning-policy.md"
    content = policy_path.read_text(encoding="utf-8")

    required_sections = [
        "# Runtime Warning Policy",
        "## Blocking Rules",
        "## Non-Blocking Rules",
        "## Treatment Matrix",
        "## Prohibited Practices",
        "## Required Evidence for PR Approval",
    ]

    for section in required_sections:
        assert section in content


def test_runtime_policy_is_referenced_by_feature_quickstart_and_contract():
    quickstart = (REPO_ROOT / "specs/010-runtime-deprecation-cleanup/quickstart.md").read_text(
        encoding="utf-8"
    )
    contract = (
        REPO_ROOT / "specs/010-runtime-deprecation-cleanup/contracts/runtime-deprecation-continuity.md"
    ).read_text(encoding="utf-8")

    assert "docs/methodology/runtime-warning-policy.md" in quickstart
    assert "docs/methodology/runtime-warning-policy.md" in contract
