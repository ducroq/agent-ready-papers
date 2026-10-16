"""The shipped claim-registry template parses with both tools (DR-027).

Restores the guard the v4 template carried in its PROVOCATION placement note:
run the tools on the template instead of reading it. Until 2026-08-13 the
released template's PROVOCATION rows were invisible to the released tool. If a
template edit changes an ID, a table shape or a tier, this test says so.
"""

from __future__ import annotations

from pathlib import Path

from tools.check_registry import check_registry
from tools.coverage import check_coverage
from tools.coverage import main as coverage_main

TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "claim-registry.md"


def test_template_ids_parse_in_check_registry():
    report = check_registry(TEMPLATE)
    ids = sorted(e.entry_id for e in report.entries)
    assert ids == ["C1", "D1", "D2", "S1-1", "S1-2", "S4-1", "S4-2", "S4-3"]


def test_template_has_no_schema_findings_and_no_notes():
    report = check_registry(TEMPLATE)
    assert report.counts == {"premises": 3, "schema": 7}
    assert [f for f in report.findings if f.check == "schema"] == []
    assert [f for f in report.findings if f.severity == "note"] == []
    # The only findings: example rows are `[ ]`, so their `claim:` premises are unverified.
    assert sorted((f.check, f.entry_id) for f in report.findings) == [
        ("premises", "C1"),
        ("premises", "C1"),
        ("premises", "S4-1"),
        ("premises", "S4-1"),
        ("premises", "S4-2"),
    ]


def test_template_coverage_rows_and_p0_floor():
    report = check_coverage(TEMPLATE)
    assert not report.evaluated_nothing
    assert report.unmatched_ids == () and report.unclassified == ()
    assert sorted((r.unit_type, r.bucket, r.total, r.verified) for r in report.rows) == [
        ("CONTRIBUTION", "P0", 1, 0),
        ("DESCRIPTIVE", "P0", 1, 0),
        ("DESCRIPTIVE", "P1", 2, 0),
        ("NORMATIVE", "P1", 1, 0),
        ("PROVOCATION", "GROUNDED", 1, 0),
    ]
    # The template's note says the example fails the floor: C1 is EMERGING.
    assert sorted(report.p0_ids) == ["C1", "S1-1"]
    assert list(report.p0_below_floor) == ["C1"]
    assert coverage_main([str(TEMPLATE)]) == 0
    assert coverage_main([str(TEMPLATE), "--strict"]) == 1
