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
    CoverageReport,
    CoverageRow,
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


@pytest.mark.xfail(reason="parser stubbed — see TODO(#17) in tools/coverage.py", strict=True)
def test_paper1_registry_coverage_shape(paper1_registry):
    """Once the parser lands, the Paper 1 fixture must produce this shape."""
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
