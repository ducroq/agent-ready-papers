"""DR-027 tools prototype, review round 1: a seeded positive per defect.

Each test fails on the round-0 prototype (commit f0b5d30) and passes with the
fix. Helpers come from `test_v5_registry` so both files build rows one way.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.test_v5_registry import (
    CLAIMS_HEADER,
    CONTRIB_HEADER,
    OLD_REGISTRY,
    claim_row,
    contrib_row,
    decl_row,
    registry,
    schema_messages,
    write,
)
from tools.check_registry import _check_anchors, _parse_entries, check_registry
from tools.coverage import check_coverage
from tools.coverage import main as coverage_main

REPO_ROOT = Path(__file__).resolve().parents[1]


# 1. near-miss markers -------------------------------------------------------


def test_near_miss_marker_after_a_heading_is_an_error_not_a_silent_drop(tmp_path):
    """`**CONTRIBUTIONS:**` under `## Contributions` dropped its table while
    `**Claims:**` parsed, so --strict passed over a SPECULATIVE contribution."""
    text = (
        "## Claims\n\n"
        + registry(claims=claim_row(priority="P0"))
        + "## Contributions\n\n**CONTRIBUTIONS:**\n\n"
        + CONTRIB_HEADER
        + contrib_row(tier="SPECULATIVE")
    )
    path = write(tmp_path, text)
    with pytest.raises(ValueError, match="near-miss marker"):
        check_coverage(path)
    assert coverage_main([str(path), "--strict"]) == 2
    report = check_registry(path)
    assert any("near-miss marker `**CONTRIBUTIONS:**`" in f.message and f.severity == "finding" for f in report.findings)


@pytest.mark.parametrize(
    "line", ["**claims:**", "### **CLAIMs:**", "**Declared Starting Points:**", "**ARGUMENT (Toulmin):**"]
)
def test_near_miss_forms_are_caught_beside_a_valid_marker(tmp_path, line):
    path = write(tmp_path, registry(claims=claim_row()) + line + "\n\n" + CLAIMS_HEADER + claim_row("S2-1"))
    with pytest.raises(ValueError, match="near-miss marker"):
        check_coverage(path)


@pytest.mark.parametrize(
    "line",
    [
        "**Claims with a Warrant**",
        "```\n**claims:**\n```",
        "    **claims:**",
        "**Arguments**\n\nProse follows, no table.",
        "**Claim (S1-1):**\n\nThe statement in prose.",
    ],
)
def test_bold_prose_and_quoted_examples_are_not_near_misses(tmp_path, line):
    path = write(tmp_path, line + "\n\n" + registry(claims=claim_row()))
    assert check_coverage(path).rows
    assert not any("near-miss" in f.message for f in check_registry(path).findings)


# 2. contributions: P0 bucket, effective tier -------------------------------


def test_contribution_is_in_the_p0_bucket_whatever_its_cell(tmp_path):
    report = check_coverage(write(tmp_path, registry(claims=claim_row(), contribs=contrib_row(priority="P2"))))
    assert ("CONTRIBUTION", "P0", 1) in [(r.unit_type, r.bucket, r.total) for r in report.rows]


def test_contribution_effective_tier_fails_the_floor_under_strict_alone(tmp_path):
    """A SUPPORTED contribution resting on an EMERGING claim: coverage alone must fail."""
    text = registry(claims=claim_row(priority="P1", tier="EMERGING"), contribs=contrib_row(tier="SUPPORTED"))
    path = write(tmp_path, text)
    report = check_coverage(path)
    assert report.p0_below_floor == ("C1",)
    assert "weakest claim S1-1" in dict(report.p0_tiers)["C1"]
    assert coverage_main([str(path), "--strict"]) == 1


def test_contribution_on_an_unregistered_claim_fails_the_floor(tmp_path):
    text = registry(claims=claim_row(priority="P1"), contribs=contrib_row(rests="claim: S9-9", tier="SUPPORTED"))
    assert check_coverage(write(tmp_path, text)).p0_below_floor == ("C1",)


def test_contribution_resting_on_supported_claims_meets_the_floor(tmp_path):
    text = registry(claims=claim_row(priority="P1", tier="ESTABLISHED"), contribs=contrib_row(tier="SUPPORTED"))
    assert check_coverage(write(tmp_path, text)).meets_tier_floor


# 3. unclassified and unmatched rows in coverage -----------------------------


def test_unclassified_rows_are_counted_and_fail_strict(tmp_path):
    path = write(tmp_path, registry(claims=claim_row(says="maybe"), contribs=contrib_row()))
    report = check_coverage(path)
    assert report.unclassified == ("S1-1",)
    assert "Unclassified rows: 1 (S1-1)" in report.to_markdown()
    assert coverage_main([str(path)]) == 0
    assert coverage_main([str(path), "--strict"]) == 1


def test_unmatched_ids_in_dr027_tables_are_counted_and_fail_strict(tmp_path):
    path = write(tmp_path, registry(claims=claim_row() + claim_row("SN-1"), contribs=contrib_row()))
    report = check_coverage(path)
    assert report.unmatched_ids == ("SN-1",)
    assert report.meets_targets and report.meets_tier_floor
    assert coverage_main([str(path), "--strict"]) == 1


def test_unmatched_ids_in_dr004_tables_are_a_note_and_do_not_fail_strict(tmp_path):
    """Round 2, item 1: the template's SN-1…SN-4 must not fail --strict."""
    path = write(tmp_path, OLD_REGISTRY.replace("| S2-1 | x |", "| SN-1 | x |"))
    report = check_coverage(path)
    assert report.unmatched_ids == ()
    assert any("SN-1" in n for n in report.notes)
    assert coverage_main([str(path), "--strict"]) == 0


# 4. zero cases ---------------------------------------------------------------


def test_contributions_marker_with_no_rows_is_noted(tmp_path):
    text = "**Contributions:**\n\n" + CONTRIB_HEADER + "\n" + registry(claims=claim_row())
    report = check_coverage(write(tmp_path, text))
    assert any("no contributions registered" in n for n in report.notes)


def test_new_schema_claims_without_a_contributions_table_are_noted(tmp_path):
    assert any("no contributions" in n for n in check_coverage(write(tmp_path, registry(claims=claim_row()))).notes)


def test_no_contribution_note_for_an_old_registry(tmp_path):
    assert check_coverage(write(tmp_path, OLD_REGISTRY)).notes == ()


def test_declared_only_registry_evaluates_nothing(tmp_path):
    path = write(tmp_path, registry(decls=decl_row()))
    report = check_coverage(path)
    assert report.evaluated_nothing
    assert "Nothing evaluated" in report.to_markdown()
    assert coverage_main([str(path)]) == 0
    assert coverage_main([str(path), "--strict"]) == 1


# 5. alias regression -----------------------------------------------------------


def test_dr004_grounds_read_only_s_ids_as_premises():
    """`Smith's model C2 and phase D1` in DR-004 free text is not a reference."""
    table = (
        "**ARGUMENTs** (Toulmin):\n\n| ID | Claim | Grounds | Warrant | Rebuttal | Priority | Confidence | Status |\n"
        "|---|---|---|---|---|---|---|---|\n| S2-1 | y | S1-1; Smith's model C2 and phase D1 | w | r | P0 | SUPPORTED | [x] |\n"
    )
    (entry,) = _parse_entries(table)
    assert entry.premises == ("S1-1",)


def test_unmatched_id_in_a_dr004_table_keeps_the_exit_code(tmp_path):
    path = write(tmp_path, OLD_REGISTRY.replace("| S2-1 | x |", "| SN-1 | x |"))
    report = check_registry(path)
    assert [f.severity for f in report.findings if "so no check reads it" in f.message] == ["note"]
    assert report.ok


# 6. DR-027 table under a DR-004 marker --------------------------------------


@pytest.mark.parametrize(
    "header_extra, grounds",
    [
        pytest.param(" Says |", "S1-2", id="says-column"),
        pytest.param(" Note |", "src: A 2020; claim: S1-2", id="typed-grounds"),
    ],
)
def test_dr027_table_under_a_dr004_marker_is_a_finding(tmp_path, header_extra, grounds):
    """One finding per table (two triggering rows: deduped), and the flag resets at
    the next marker (a second triggering table: a second finding)."""

    def table(marker, a, b):
        return (
            f"{marker}\n\n"
            f"| ID | Statement |{header_extra} Grounds | Warrant | Rebuttal | Priority | Confidence | Status |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            f"| {a} | x | descriptive | {grounds} | w | r | P1 | EMERGING | [x] |\n"
            f"| {b} | x | descriptive | {grounds} | w | r | P1 | EMERGING | [x] |\n\n"
        )

    text = table("**ARGUMENTs** (Toulmin):", "S1-1", "S1-2") + table("**CLAIMs:**", "S2-1", "S2-2")
    report = check_registry(write(tmp_path, text))
    hits = [f for f in report.findings if "DR-027 table under a DR-004 marker" in f.message]
    assert [f.severity for f in hits] == ["finding", "finding"]
    assert "registry line 3" in hits[0].message or "registry line 5" in hits[0].message


# 7. excess cells ----------------------------------------------------------------


def test_excess_cells_are_a_finding_not_a_column_shift(tmp_path):
    report = check_registry(write(tmp_path, registry(claims=claim_row(grounds="src: `a|b` 2020"))))
    assert any("cells but the header defines" in f.message and f.severity == "finding" for f in report.findings)
    assert report.entries == ()


# 8. duplicate IDs -----------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(registry(claims=claim_row() + claim_row()), id="claims"),
        pytest.param(registry(decls=decl_row() + decl_row(kind="definition")), id="declared"),
    ],
)
def test_duplicate_ids_are_a_finding(tmp_path, text):
    assert any("duplicate ID" in m for m in schema_messages(tmp_path, text))


def test_an_id_in_two_dr004_sub_tables_is_one_entry_not_a_duplicate(tmp_path):
    """Round 2, item 2: DR-004 keeps master's rule (tools/README.md)."""
    report = check_registry(write(tmp_path, OLD_REGISTRY.replace("| S2-1 | x |", "| S1-1 | x |")))
    assert not any("duplicate ID" in f.message for f in report.findings)


# 9 / 12. Rests-on item types -------------------------------------------------------


def test_own_item_in_rests_on_is_a_finding(tmp_path):
    text = registry(claims=claim_row(), contribs=contrib_row(rests="claim: S1-1; own: survey of 10 labs"))
    assert any("Rests on lists `own:" in m for m in schema_messages(tmp_path, text, "C1"))


def test_src_item_in_rests_on_is_a_finding(tmp_path):
    text = registry(claims=claim_row(), contribs=contrib_row(rests="claim: S1-1; src: Smith 2020"))
    assert any("Rests on lists `src:" in m for m in schema_messages(tmp_path, text, "C1"))


# 10 / 12. glossary ------------------------------------------------------------------


def test_glossary_template_with_only_the_paper_line_edited_fails(tmp_path):
    template = (REPO_ROOT / "templates" / "glossary.md").read_text(encoding="utf-8")
    assert "**Paper:** [Title]" in template
    gloss = write(tmp_path, template.replace("**Paper:** [Title]", "**Paper:** The Verification Gap"), "glossary.md")
    reg = write(tmp_path, registry(claims=claim_row()))
    hits = [f for f in check_registry(reg, glossary_path=gloss).findings if f.check == "glossary"]
    assert len(hits) == 1 and "`| [term] |`" in hits[0].message and "[Title]" not in hits[0].message


def test_glossary_that_is_a_directory_is_a_finding(tmp_path):
    reg = write(tmp_path, registry(claims=claim_row()))
    report = check_registry(reg, glossary_path=tmp_path)
    assert any(f.check == "glossary" and "could not be read" in f.message for f in report.findings)


def test_whitespace_only_glossary_is_empty(tmp_path):
    reg = write(tmp_path, registry(claims=claim_row()))
    gloss = write(tmp_path, " \t\n \n", "glossary.md")
    hits = [f for f in check_registry(reg, glossary_path=gloss).findings if f.check == "glossary"]
    assert len(hits) == 1 and "empty" in hits[0].message


# 11. D anchors -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "anchor, expected",
    [
        ("% D1: d (value, accepted)", []),
        ("% D1: d (definition, accepted)", ["Kind"]),
        ("% D1: d (value, own)", ["Contestedness"]),
        ("% D1: d", []),
    ],
)
def test_declared_anchor_must_agree_with_kind_and_contestedness(anchor, expected):
    entries = _parse_entries(registry(decls=decl_row("D1", kind="value", contested="accepted in the field")))
    findings, _ = _check_anchors(entries, anchor + "\n")
    assert [f.message.split(" gives ")[1].split(" ")[0] for f in findings] == expected
    assert all(f.severity == "finding" for f in findings)


# 12. rules a mutation run found untested ----------------------------------------------


@pytest.mark.parametrize(
    "eid, table, needle",
    [
        ("C5", "claims", "Claims table has an ID that is not S"),
        ("S1-9", "contribs", "Contributions table has an ID that is not C"),
        ("S1-8", "decls", "non-D ID"),
    ],
)
def test_wrong_prefix_ids_are_findings(tmp_path, eid, table, needle):
    texts = {
        "claims": registry(claims=claim_row(eid)),
        "contribs": registry(claims=claim_row(), contribs=contrib_row(eid)),
        "decls": registry(decls=decl_row(eid)),
    }
    assert any(needle in m for m in schema_messages(tmp_path, texts[table], eid))


def test_bare_src_item_is_a_finding(tmp_path):
    assert any("bare `src:`" in m for m in schema_messages(tmp_path, registry(claims=claim_row(grounds="src:"))))


def test_declared_table_without_status_is_a_parse_error(tmp_path):
    text = (
        "**Declared starting points:**\n\n| ID | Statement | Kind | Contestedness |\n|---|---|---|---|\n"
        "| D1 | v | value | own |\n"
    )
    with pytest.raises(ValueError, match="no Status column"):
        check_coverage(write(tmp_path, text))


def test_id_only_declared_row_is_counted(tmp_path):
    text = registry(claims=claim_row(), decls=decl_row() + "| D2 |\n")
    assert check_coverage(write(tmp_path, text)).declared_total == 2


def test_contribution_ids_are_read_from_manuscript_confidence_tables(tmp_path):
    reg = write(tmp_path, registry(claims=claim_row(), contribs=contrib_row(tier="SUPPORTED")))
    tex = write(
        tmp_path,
        "% S1-1: a (descriptive, P1, SUPPORTED)\n% C1: c (contribution, P0, SUPPORTED)\n"
        "\\begin{tabular}{ll}\nID & Confidence \\\\\nC1 & EMERGING \\\\\n\\end{tabular}\n",
        "m.tex",
    )
    report = check_registry(reg, manuscript_path=tex)
    hits = [f for f in report.findings if f.check == "tiers" and f.severity == "finding"]
    assert [f.entry_id for f in hits] == ["C1"] and "manuscript table" in hits[0].message


# 13. fixture ------------------------------------------------------------------------------


def test_v5_fixture_types_own_observations_as_own_with_no_source_tier():
    from tests.test_v5_registry import V5_FIXTURE

    entries = {e.entry_id: e for e in _parse_entries(V5_FIXTURE.read_text(encoding="utf-8"))}
    for eid in ("S1-3", "S1-5"):
        ((kind, method),) = entries[eid].items
        assert kind == "own" and method
        assert entries[eid].columns["source tier"] == ""
