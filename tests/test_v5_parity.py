"""Alias parity: on DR-004 (and PROVOCATION) registries the v5 tools give master's results.

The class rule from review round 2: DR-004 tables behave exactly as on master
for exit codes and findings; v5 may only add NOTE lines. The expected values
below were MEASURED by running master's `tools/coverage.py` and
`tools/check_registry.py` (v4.3.0, commit e89ffd4) on the same files — they
are not restated from the branch. Re-measure with master's tools if a fixture
here changes; never by running the branch.

`alias-edge-cases.md` holds one row for every way a DR-004 table can differ
from the v5 patterns: a near-miss marker, a decorated ID, a letter ID (the
template's SN-n), a suffixed ID, a C-ID, ID-only divider rows, an ID in two
sub-tables, C/D tokens in free-text Grounds, and a PROVOCATION row with a
non-S ID. `alias-excess-cell.md` has an unescaped pipe.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.check_registry import check_registry
from tools.coverage import check_coverage
from tools.coverage import main as coverage_main

ROOT = Path(__file__).resolve().parents[1]

# (registry, manuscript, coverage --strict exit, coverage rows, P0 floor (meeting, total),
#  check_registry exit, check_registry counts, findings as (check, entry_id))
MASTER = [
    (
        "tests/fixtures/dr004/template-v4-claim-registry.md",
        None,
        1,
        [("ARGUMENT", "P0", 1, 0), ("CLAIM", "P0", 1, 0), ("CLAIM", "P1", 3, 0), ("PROPOSITION", "P1", 1, 0),
         ("PROVOCATION", "GROUNDED", 1, 0)],
        (2, 2),
        0,
        {"premises": 0, "schema": 0},
        [],
    ),
    (
        "tests/fixtures/dr004/paper1-v4-registry.md",
        None,
        1,
        [("ARGUMENT", "P0", 1, 1), ("CLAIM", "P0", 4, 4), ("CLAIM", "P1", 9, 9), ("CLAIM", "P2", 2, 2),
         ("PROPOSITION", "P0", 1, 1)],
        (3, 6),
        0,
        {"premises": 2, "schema": 2},
        [],
    ),
    (
        "tests/fixtures/dr004/paper1-v4-registry.md",
        "tests/fixtures/dr004/paper1-v4-manuscript.tex",
        1,
        [("ARGUMENT", "P0", 1, 1), ("CLAIM", "P0", 4, 4), ("CLAIM", "P1", 9, 9), ("CLAIM", "P2", 2, 2),
         ("PROPOSITION", "P0", 1, 1)],
        (3, 6),
        0,
        {"anchors": 17, "budget": 3496, "premises": 2, "schema": 2, "tiers": 17},
        [],
    ),
    (
        "tests/fixtures/dr004/alias-edge-cases.md",
        None,
        0,
        [("ARGUMENT", "P0", 1, 1), ("ARGUMENT", "P1", 1, 1), ("CLAIM", "P0", 1, 1), ("CLAIM", "P1", 4, 4),
         ("PROVOCATION", "EXTRAPOLATED", 1, 0), ("PROVOCATION", "GROUNDED", 1, 1)],
        (1, 1),
        1,
        {"premises": 2, "schema": 2},
        [("premises", "S1-1")],
    ),
    (
        "tests/fixtures/dr004/alias-edge-cases.md",
        "tests/fixtures/dr004/alias-edge-cases.tex",
        0,
        [("ARGUMENT", "P0", 1, 1), ("ARGUMENT", "P1", 1, 1), ("CLAIM", "P0", 1, 1), ("CLAIM", "P1", 4, 4),
         ("PROVOCATION", "EXTRAPOLATED", 1, 0), ("PROVOCATION", "GROUNDED", 1, 1)],
        (1, 1),
        1,
        {"anchors": 3, "budget": 4, "premises": 2, "schema": 2, "tiers": 2},
        [("anchors", "S3-1"), ("premises", "S1-1")],
    ),
]


@pytest.mark.parametrize(
    "reg, ms, cov_exit, rows, floor, cr_exit, counts, findings",
    MASTER,
    ids=[f"{m[0].split('/')[-1]}{'+tex' if m[1] else ''}" for m in MASTER],
)
def test_dr004_registry_matches_master(reg, ms, cov_exit, rows, floor, cr_exit, counts, findings):
    path = ROOT / reg
    assert coverage_main([str(path), "--strict"]) == cov_exit
    report = check_coverage(path)
    assert sorted((r.unit_type, r.bucket, r.total, r.verified) for r in report.rows) == rows
    assert (len(report.p0_ids) - len(report.p0_below_floor), len(report.p0_ids)) == floor
    assert report.unmatched_ids == () and report.unclassified == () and not report.evaluated_nothing

    manuscript = None if ms is None else ROOT / ms
    cr = check_registry(path, manuscript_path=manuscript, budget=5000 if ms else None)
    assert (0 if cr.ok else 1) == cr_exit
    assert cr.counts == counts
    assert sorted((f.check, f.entry_id) for f in cr.findings if f.severity == "finding") == findings


def test_dr004_excess_cell_matches_master():
    """Master: coverage exits 2; check_registry reads the row shifted, 0 findings, exit 0."""
    path = ROOT / "tests/fixtures/dr004/alias-excess-cell.md"
    assert coverage_main([str(path), "--strict"]) == 2
    cr = check_registry(path)
    assert cr.ok and cr.counts == {"premises": 0, "schema": 0}
    assert [f.severity for f in cr.findings if "cells but the header defines" in f.message] == ["note"]
    assert [e.entry_id for e in cr.entries] == ["S1-1", "S1-4"]


def test_dr004_edge_cases_surface_only_as_notes():
    """What master dropped in silence is now visible — as notes, never findings."""
    path = ROOT / "tests/fixtures/dr004/alias-edge-cases.md"
    notes = [f.message for f in check_registry(path).findings if f.severity == "note"]
    for needle in ("near-miss marker `**claims:**`", "`**S1-2**`", "`SN-1`", "`S1-3a`", "`C1`", "`PV-1`"):
        assert any(needle in n for n in notes), needle
    cov_notes = " ".join(check_coverage(path).notes)
    assert "near-miss marker" in cov_notes and "SN-1" in cov_notes and "PV-1" in cov_notes
