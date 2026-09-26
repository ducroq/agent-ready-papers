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
    main,
)


def test_dataclass_shape_is_stable():
    """Dataclass field set is part of the public API contract."""
    row = CoverageRow(unit_type="CLAIM", axis=PRIORITY_AXIS, bucket="P0", total=8, verified=8)
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

    # Non-emptiness first: every all()/any() below is vacuously true over an
    # empty report, so a parser that silently matched nothing would satisfy
    # them all. Zero rows is never a legitimate state for this fixture.
    assert report.rows, "parsed zero rows — the parser matched nothing"

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
        "ID",
        "Statement",
        "Priority",
        "Confidence",
        "Grounds",
        "Warrant",
        "Rebuttal",
        "Source",
        "Source Tier",
        "Status",
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
        "ID",
        "Statement",
        "Source Tier",
        "Priority",
        "Tier (PROVOCATION axis)",
        "Plausibility evidence",
        "Status",
    ]
    # Must pick column 4 (Tier (PROVOCATION axis)), NOT column 2 (Source Tier).
    assert _find_bucket_and_status_columns(header, "PROVOCATION") == (
        4,
        PROVOCATION_TIER_AXIS,
        6,
    )


def test_find_columns_provocation_canonical_template():
    """Matches the column order in templates/claim-registry.md."""
    header = [
        "ID",
        "Statement",
        "Priority",
        "Tier (PROVOCATION axis)",
        "Plausibility evidence",
        "Generative move",
        "Reflexive marker",
        "Ethics commitment",
        "Status",
    ]
    assert _find_bucket_and_status_columns(header, "PROVOCATION") == (
        3,
        PROVOCATION_TIER_AXIS,
        8,
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
    content = "\n".join(
        [
            "**CLAIMs:**",
            "",
            "| ID | Statement | Priority | Confidence | Source | Source Tier | Status |",
            "|----|-----------|----------|------------|--------|-------------|--------|",
            r"| S1-1 | \|H(z)\| is the magnitude response | P0 | ESTABLISHED | textbook | C | [x] |",
            r"| S1-2 | \|z\|=1 is the unit circle | P0 | ESTABLISHED | textbook | C | [x] |",
            "| S1-3 | A plain claim with no pipes | P0 | ESTABLISHED | textbook | C | [ ] |",
        ]
    )
    counts = _parse_registry(content)
    assert counts[("CLAIM", PRIORITY_AXIS, "P0")] == (3, 2)


def test_parse_registry_refuses_a_row_with_excess_cells():
    """An UNESCAPED pipe (including inside backticks) gives the row more cells
    than the header. GFM discards the excess, so the row loses data AND every
    column index read from it shifts.

    Seeded 2026-09-14 from a measured failure: the row below parsed with Tier
    reading "IS FLAT" and Status reading "P0", the P0 claim landed in an
    invented bucket "H(z)" with target "-", and `coverage --strict` exited 0
    reporting 100% P0 over nothing. Refusing is the only safe outcome — a
    shifted read is silent.

    Note GFM splits a row into cells BEFORE parsing inline content, so
    backticks do not protect a pipe. Escape it as \\|.
    """
    content = "\n".join(
        [
            "**CLAIMs:**",
            "",
            "| ID | Statement | Priority | Confidence | Source | Tier | Status |",
            "|----|-----------|----------|------------|--------|------|--------|",
            "| S1-1 | transfer `|H(z)|` is flat | P0 | SPECULATIVE | guess | C | [x] |",
        ]
    )
    with pytest.raises(ValueError, match="excess is discarded"):
        _parse_registry(content)


def test_parse_registry_tolerates_a_short_divider_row_without_truncating():
    """A one-cell section divider is idiomatic markdown, not corruption: GFM
    pads a short row and renders it as intended.

    Seeded 2026-09-14: the loop used to `break` on any row shorter than the
    highest column index it needed, which ended the table at the first divider
    and silently dropped every row after it. A P0 claim could leave the
    denominator entirely and `--strict` would pass over the remainder. The
    divider itself must not be counted (empty bucket/status), and the rows
    after it must be.
    """
    content = "\n".join(
        [
            "**CLAIMs:**",
            "",
            "| ID | Statement | Priority | Confidence | Source | Tier | Status |",
            "|----|-----------|----------|------------|--------|------|--------|",
            "| S1-1 | before the divider | P0 | ESTABLISHED | s | A | [x] |",
            "| **PART TWO** |",
            "| S1-2 | after the divider | P0 | ESTABLISHED | s | A | [x] |",
            "| S1-3 | also after | P0 | ESTABLISHED | s | A | [ ] |",
        ]
    )
    counts = _parse_registry(content)
    assert counts[("CLAIM", PRIORITY_AXIS, "P0")] == (3, 2)


# --------------------------------------------------------------------------
# P0 tier floor (DR-002) — reported separately from coverage (#37)
# --------------------------------------------------------------------------


def _floor_registry(tmp_path, *tiers, header_confidence="Confidence"):
    rows = "\n".join(f"| S1-{n} | claim {n} | P0 | {tier} | s | A | [x] |" for n, tier in enumerate(tiers, start=1))
    path = tmp_path / "r.md"
    path.write_text(
        "**CLAIMs:**\n\n"
        f"| ID | Statement | Priority | {header_confidence} | Source | Source Tier | Status |\n"
        "|----|-----------|----------|------------|--------|-------------|--------|\n"
        + (f"{rows}\n" if rows else "")  # an empty line here would END the table
        + "| S1-99 | a P1 below the floor is not P0 | P1 | SPECULATIVE | s | A | [x] |\n",
        encoding="utf-8",
    )
    return path


def test_tier_floor_passes_when_every_p0_is_supported_or_established(tmp_path):
    report = check_coverage(_floor_registry(tmp_path, "SUPPORTED", "**ESTABLISHED**", "SUPPORTED ⚠"))
    assert report.meets_tier_floor is True
    assert report.p0_below_floor == ()
    assert len(report.p0_tiers) == 3
    assert "P0 tier floor (SUPPORTED or ESTABLISHED, DR-002): 3 of 3 meet it — meets" in report.to_markdown()
    assert main([str(report.registry_path), "--strict"]) == 0


def test_tier_floor_fails_on_a_p0_below_supported_even_at_full_coverage(tmp_path):
    report = check_coverage(_floor_registry(tmp_path, "SUPPORTED", "EMERGING", "Speculative"))
    assert report.meets_targets is True  # coverage is untouched by the floor
    assert report.meets_tier_floor is False
    assert report.p0_below_floor == ("S1-2", "S1-3")
    assert "1 of 3 meet it — FAILS; below the floor: S1-2, S1-3" in report.to_markdown()
    floor = report.to_dict()["p0_tier_floor"]
    assert floor["meets"] is False and floor["below_floor"] == ["S1-2", "S1-3"]
    assert main([str(report.registry_path), "--strict"]) == 1
    assert main([str(report.registry_path)]) == 0  # the floor gates --strict only


def test_tier_floor_counts_an_unreadable_tier_as_failing(tmp_path):
    """No Confidence column at all: every P0 row fails the floor, not passes it."""
    report = check_coverage(_floor_registry(tmp_path, "SUPPORTED", header_confidence="Notes"))
    assert report.meets_tier_floor is False
    assert report.p0_below_floor == ("S1-1",)


def test_paper1_p0_tier_floor_fails(paper1_registry):
    """Paper 1's P0 gate genuinely fails after the 828f9cd re-derivation (#38)."""
    report = check_coverage(paper1_registry)
    assert len(report.p0_tiers) == 8
    assert report.meets_tier_floor is False
    assert set(report.p0_below_floor) == {"S1-1", "S1-2", "S1-4", "S2-2", "S3-4", "S4-1", "S5-1"}


def test_tier_floor_sees_a_decorated_or_unticked_p0(tmp_path):
    """Seeded from review 2026-09-25: `**P0**` and a blank Status each dropped an
    EMERGING P0 out of the floor, which then printed "meets"."""
    path = tmp_path / "r.md"
    path.write_text(
        "**CLAIMs:**\n\n"
        "| ID | Statement | Priority | Confidence | Status |\n"
        "|----|-----------|----------|------------|--------|\n"
        "| S1-1 | ok | P0 | SUPPORTED | [x] |\n"
        "| S1-2 | decorated | **P0** | EMERGING | [x] |\n"
        "| S1-3 | unticked | P0 | EMERGING |  |\n",
        encoding="utf-8",
    )
    report = check_coverage(path)
    assert report.p0_below_floor == ("S1-2", "S1-3")
    # and coverage counts the unticked row as unverified, not as absent
    assert sum(r.total for r in report.rows) == 3
    assert sum(r.verified for r in report.rows) == 2


def test_tier_floor_counts_entries_not_rows(tmp_path):
    path = tmp_path / "r.md"
    table = "| ID | Statement | Priority | Confidence | Status |\n|----|----|----|----|----|\n"
    path.write_text(
        "**CLAIMs:**\n\n" + table + "| S1-1 | a | P0 | EMERGING | [x] |\n| S1-2 | b | P0 | SUPPORTED | [x] |\n\n"
        "**ARGUMENTs:**\n\n" + table + "| S1-1 | a | P0 | EMERGING | [x] |\n",
        encoding="utf-8",
    )
    report = check_coverage(path)
    assert report.p0_ids == ("S1-1", "S1-2")
    assert report.p0_below_floor == ("S1-1",)
    assert "1 of 2 meet it — FAILS; below the floor: S1-1." in report.to_markdown()


def test_tier_floor_with_no_p0_says_not_evaluated(tmp_path):
    """ "0 of 0 meet it — meets" reads as a pass; it must say nothing was checked."""
    report = check_coverage(_floor_registry(tmp_path))  # only the P1 row
    assert report.p0_ids == ()
    assert "NOT evaluated" in report.to_markdown()
    assert "meets" not in report._tier_floor_line()
    assert report.to_dict()["p0_tier_floor"]["evaluated"] is False


# --------------------------------------------------------------------------
# a marker whose table cannot be read is a parse failure, not an empty table
# --------------------------------------------------------------------------

_HEADER = "| ID | Statement | Priority | Confidence | Status |\n|----|----|----|----|----|\n"
_ROW = "| S1-1 | a | P0 | EMERGING | [x] |\n"


@pytest.mark.parametrize(
    "content",
    [
        pytest.param("**CLAIMs:**\n\nSome prose first.\n\n" + _HEADER + _ROW, id="prose-between-marker-and-table"),
        pytest.param("**CLAIMs:**\n\n", id="marker-at-end-of-file"),
        pytest.param("**CLAIMs:**\n\n" + _HEADER.replace("Priority", "Prio") + _ROW, id="renamed-priority-header"),
        pytest.param("**CLAIMs:**\n\n" + _HEADER.replace("Status", "State") + _ROW, id="renamed-status-header"),
    ],
)
def test_unreadable_sub_table_raises_instead_of_dropping_its_rows(tmp_path, content):
    path = tmp_path / "r.md"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError, match="dropped from coverage and the P0 tier floor"):
        check_coverage(path)
    assert main([str(path), "--strict"]) == 2


@pytest.mark.parametrize("marker", ["**Claims:**", "### **CLAIMs:**", "**CLAIM (Toulmin):**"])
def test_a_registry_whose_only_marker_is_unrecognised_is_an_error(tmp_path, marker):
    """Review 2026-09-26: an unrecognised marker silently dropped its sub-table,
    and with nothing else parsed --strict exited 0 with the floor NOT evaluated."""
    path = tmp_path / "r.md"
    path.write_text(marker + "\n\n" + _HEADER + _ROW.replace("[x]", "[ ]"), encoding="utf-8")
    with pytest.raises(ValueError, match="never legitimately empty"):
        check_coverage(path)
    assert main([str(path), "--strict"]) == 2


def test_renaming_a_priority_header_no_longer_turns_strict_green(tmp_path, paper1_registry):
    """The measured route (2026-09-26): on Paper 1, whose P0 floor genuinely
    fails, renaming the Priority headers dropped every row from coverage and
    the floor, which then printed NOT evaluated while --strict exited 0."""
    content = paper1_registry.read_text(encoding="utf-8")
    renamed = content.replace("| ID | Statement | Priority |", "| ID | Statement | Prio |")
    assert renamed != content, "fixture no longer has the header this test renames"
    path = tmp_path / "r.md"
    path.write_text(renamed, encoding="utf-8")
    assert main([str(paper1_registry), "--strict"]) == 1
    assert main([str(path), "--strict"]) == 2


def test_a_row_with_a_blanked_priority_is_an_error_not_a_skip(tmp_path):
    """Measured route (docs/verification-hooks.md): deleting the two characters
    of `P0` took an unverified claim out of the count while it stayed visibly in
    the registry, and --strict exited 0."""
    path = tmp_path / "r.md"
    path.write_text(
        "**CLAIMs:**\n\n" + _HEADER + _ROW + _ROW.replace("S1-1", "S1-2").replace("| P0 |", "|  |"), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="no Priority"):
        check_coverage(path)
    assert main([str(path), "--strict"]) == 2


def test_a_blank_status_counts_as_unverified(tmp_path):
    """Blanking a Status cell used to remove the row from the denominator, which
    RAISED coverage. It is an entry nobody has verified."""
    path = tmp_path / "r.md"
    path.write_text(
        "**CLAIMs:**\n\n" + _HEADER + _ROW + _ROW.replace("S1-1", "S1-2").replace("[x]", ""), encoding="utf-8"
    )
    report = check_coverage(path)
    assert [(r.bucket, r.total, r.verified) for r in report.rows] == [("P0", 2, 1)]
    assert report.meets_targets is False
    assert main([str(path), "--strict"]) == 1


@pytest.mark.parametrize("overwrite", ["-", "TBD", "N/A", "P9"])
def test_an_overwritten_priority_fails_instead_of_hiding_in_its_own_bucket(tmp_path, overwrite):
    """Review 2026-09-26: replacing `P0` with anything unrecognised moved an
    unverified claim into an untargeted bucket, and --strict exited 0."""
    path = tmp_path / "r.md"
    unverified = _ROW.replace("S1-1", "S1-2").replace("[x]", "[ ]").replace("| P0 |", f"| {overwrite} |")
    path.write_text("**CLAIMs:**\n\n" + _HEADER + _ROW + unverified, encoding="utf-8")
    report = check_coverage(path)
    assert report.meets_targets is False
    assert "NO — not a priority" in report.to_markdown()
    assert main([str(path), "--strict"]) == 1


def test_a_lowercase_or_decorated_priority_is_the_same_bucket_the_floor_reads(tmp_path):
    path = tmp_path / "r.md"
    path.write_text(
        "**CLAIMs:**\n\n"
        + _HEADER
        + _ROW
        + _ROW.replace("S1-1", "S1-2").replace("| P0 |", "| p0 |")
        + _ROW.replace("S1-1", "S1-3").replace("| P0 |", "| **P0** |"),
        encoding="utf-8",
    )
    report = check_coverage(path)
    assert [(r.bucket, r.total) for r in report.rows] == [("P0", 3)]
    assert len(report.p0_ids) == 3


def test_custom_priority_targets_are_not_unknown_buckets(tmp_path):
    path = tmp_path / "r.md"
    path.write_text("**CLAIMs:**\n\n" + _HEADER + _ROW.replace("| P0 |", "| P3 |"), encoding="utf-8")
    assert check_coverage(path).meets_targets is False
    assert check_coverage(path, priority_targets={"P3": 50.0}).meets_targets is True


@pytest.mark.parametrize("row", ["| S1-2 |  |  |  |  |\n", "| S1-2 |\n", "| **S1-2** | |\n"])
def test_a_row_blanked_down_to_its_id_is_not_a_divider(tmp_path, row):
    """A divider's shape but an entry's ID, at any width (round 2: the short
    form `| S1-2 |` was still skipped)."""
    path = tmp_path / "r.md"
    path.write_text("**CLAIMs:**\n\n" + _HEADER + _ROW + row, encoding="utf-8")
    with pytest.raises(ValueError, match="no Priority"):
        check_coverage(path)
