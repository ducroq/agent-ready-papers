"""Shape-pin tests for tools.coverage.

These tests assert the structural invariants the parser must guarantee
against the Paper 1 fixture. They are marked xfail while the parser is
stubbed (TODO(#17)) and become PASS once the parser lands. Removing the
xfail marker is the gate that closes #17.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.coverage import (
    PRIORITY_AXIS,
    PROVOCATION_TIER_AXIS,
    CoverageReport,
    CoverageRow,
    _find_bucket_and_status_columns,
    _parse_registry,
    _split_row,
    check_coverage,
)


def test_dataclass_shape_is_stable():
    """Dataclass field set is part of the public API contract."""
    row = CoverageRow(
        unit_type="CLAIM", axis=PRIORITY_AXIS, bucket="P0", total=8, verified=8
    )
    assert row.percent == 100.0
    # frozen invariant
    with pytest.raises((AttributeError, TypeError)):
        row.total = 99  # type: ignore[misc]


def test_check_coverage_raises_filenotfound_on_missing_path():
    with pytest.raises(FileNotFoundError):
        check_coverage(Path("does-not-exist.md"))


def test_paper1_registry_coverage_shape(paper1_registry):
    """The Paper 1 fixture must produce the documented shape."""
    report = check_coverage(paper1_registry)

    assert isinstance(report, CoverageReport)
    assert report.registry_path == paper1_registry

    # Every row in Paper 1 is on the priority axis (no PROVOCATION entries).
    assert all(row.axis == PRIORITY_AXIS for row in report.rows)

    # Total entries across the registry: 19.
    assert sum(r.total for r in report.rows) == 19
    assert sum(r.verified for r in report.rows) == 19

    unit_types = {r.unit_type for r in report.rows}
    assert unit_types == {"CLAIM", "ARGUMENT", "PROPOSITION"}

    buckets = {r.bucket for r in report.rows}
    assert buckets == {"P0", "P1", "P2"}

    # 100% verified everywhere → meets the default targets.
    assert report.meets_targets is True


def test_paper1_coverage_is_deterministic(paper1_registry):
    """Same input → byte-identical output across runs (DR-011 review finding)."""
    r1 = check_coverage(paper1_registry)
    r2 = check_coverage(paper1_registry)
    assert r1.to_markdown() == r2.to_markdown()
    assert r1.to_dict() == r2.to_dict()


def test_find_columns_claim_table():
    header = ["ID", "Statement", "Priority", "Confidence", "Source", "Source Tier", "Status"]
    assert _find_bucket_and_status_columns(header, "CLAIM") == (2, PRIORITY_AXIS, 6)


def test_find_columns_argument_table_with_source_tier():
    """ARGUMENT tables carry a 'Source Tier' column but bucket on Priority."""
    header = [
        "ID", "Statement", "Priority", "Confidence", "Grounds", "Warrant",
        "Rebuttal", "Source", "Source Tier", "Status",
    ]
    assert _find_bucket_and_status_columns(header, "ARGUMENT") == (2, PRIORITY_AXIS, 9)


def test_find_columns_provocation_prefers_tier_axis_over_source_tier():
    """Regression for DR-011 Pass 2 finding #1.

    A naive substring match on 'tier' would silently bucket against
    'Source Tier' when both columns are present. The canonical
    PROVOCATION header has both, and 'Source Tier' precedes
    'Tier (PROVOCATION axis)' in some adopter orderings.
    """
    header = [
        "ID", "Statement", "Source Tier", "Priority",
        "Tier (PROVOCATION axis)", "Plausibility evidence", "Status",
    ]
    # Must pick column 4 (Tier (PROVOCATION axis)), NOT column 2 (Source Tier).
    assert _find_bucket_and_status_columns(header, "PROVOCATION") == (
        4, PROVOCATION_TIER_AXIS, 6,
    )


def test_find_columns_provocation_canonical_template():
    """Matches the column order in templates/claim-registry.md."""
    header = [
        "ID", "Statement", "Priority", "Tier (PROVOCATION axis)",
        "Plausibility evidence", "Generative move", "Reflexive marker",
        "Ethics commitment", "Status",
    ]
    assert _find_bucket_and_status_columns(header, "PROVOCATION") == (
        3, PROVOCATION_TIER_AXIS, 8,
    )


def test_find_columns_returns_none_when_required_missing():
    header = ["ID", "Statement", "Confidence", "Source"]  # no Priority, no Status
    assert _find_bucket_and_status_columns(header, "CLAIM") is None


def test_split_row_honors_escaped_pipes():
    """Escaped pipes (\\|) in cells — e.g. magnitude notation |H(z)| — must not
    split the row into spurious columns. Regression for the dsp-workshop
    dog-fooding finding (2026-06-12): unescaped handling shifted the Status
    column and miscounted coverage (read 5/7 where the data was 8/8)."""
    row = r"| S4-1 | The magnitude \|H(z)\| peaks at \|z\|=1 | P0 | [x] |"
    cells = _split_row(row)
    assert cells == ["S4-1", "The magnitude |H(z)| peaks at |z|=1", "P0", "[x]"]


def test_parse_registry_counts_correctly_with_escaped_pipes():
    """End-to-end: a sub-table whose statements contain \\| must still bucket
    every row against the right Priority/Status columns."""
    content = "\n".join([
        "**CLAIMs:**",
        "",
        "| ID | Statement | Priority | Confidence | Source | Source Tier | Status |",
        "|----|-----------|----------|------------|--------|-------------|--------|",
        r"| S1-1 | \|H(z)\| is the magnitude response | P0 | ESTABLISHED | textbook | C | [x] |",
        r"| S1-2 | \|z\|=1 is the unit circle | P0 | ESTABLISHED | textbook | C | [x] |",
        "| S1-3 | A plain claim with no pipes | P0 | ESTABLISHED | textbook | C | [ ] |",
    ])
    counts = _parse_registry(content)
    assert counts[("CLAIM", PRIORITY_AXIS, "P0")] == (3, 2)
