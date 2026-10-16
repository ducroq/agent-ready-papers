"""Tests for the DR-027 (v5) registry schema in tools.coverage and tools.check_registry.

Every rule gets a seeded positive that fails without the v5 change, plus a
clean case, so a check that stopped firing cannot pass as a clean run. The
hand-migrated Paper 1 registry (tests/fixtures/v5/) pins the end-to-end result.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import check_registry as cr
from tools.check_registry import _anchor_tiers, _check_anchors, _parse_entries, check_registry
from tools.coverage import check_coverage
from tools.coverage import main as coverage_main

V5_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "v5" / "paper1-registry-v5.md"

CLAIMS_HEADER = (
    "| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged "
    "| Priority | Confidence tier | Source Tier | Status |\n"
    "|----|-----------|------|---------|---------|---------|----------|--------------------"
    "|----------|-----------------|-------------|--------|\n"
)
CONTRIB_HEADER = (
    "| ID | Contribution | Says | Rests on | What | How | Why | Who/Where/When | Objections engaged "
    "| Priority | Confidence tier | Status |\n"
    "|----|--------------|------|----------|------|-----|-----|----------------|--------------------"
    "|----------|-----------------|--------|\n"
)
DECL_HEADER = "| ID | Statement | Kind | Contestedness | Status |\n|----|-----------|------|---------------|--------|\n"


def claim_row(
    eid="S1-1",
    says="descriptive",
    grounds="src: Smith 2020",
    warrant="",
    rebuttal="",
    priority="P1",
    tier="SUPPORTED",
    status="[x]",
):
    return f"| {eid} | A statement | {says} | {grounds} | {warrant} | | {rebuttal} | | {priority} | {tier} | A | {status} |\n"


def contrib_row(eid="C1", says="descriptive", rests="claim: S1-1", www="", priority="P0", tier="SUPPORTED"):
    return f"| {eid} | A contribution | {says} | {rests} | w | h | y | {www} | | {priority} | {tier} | [x] |\n"


def decl_row(eid="D1", kind="value", contested="accepted in the field", status="[x]"):
    return f"| {eid} | A starting point | {kind} | {contested} | {status} |\n"


def registry(claims="", contribs="", decls=""):
    out = ""
    if contribs:
        out += "**Contributions:**\n\n" + CONTRIB_HEADER + contribs + "\n"
    if decls:
        out += "**Declared starting points:**\n\n" + DECL_HEADER + decls + "\n"
    if claims:
        out += "**Claims:**\n\n" + CLAIMS_HEADER + claims + "\n"
    return out


def write(tmp_path, text, name="r.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def schema_messages(tmp_path, text, entry_id=None):
    report = check_registry(write(tmp_path, text))
    return [
        f.message
        for f in report.findings
        if f.severity == "finding" and f.check in ("schema", "premises") and (entry_id is None or f.entry_id == entry_id)
    ]


# --------------------------------------------------------------------------
# markers and IDs
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "marker",
    ["**Claims:**", "**Claims**:", "**Claims** (DR-027):", "**Claim:**"],
)
def test_new_claims_marker_parses(tmp_path, marker):
    text = marker + "\n\n" + CLAIMS_HEADER + claim_row()
    report = check_coverage(write(tmp_path, text))
    assert [(r.unit_type, r.bucket, r.total) for r in report.rows] == [("DESCRIPTIVE", "P1", 1)]
    assert [e.entry_id for e in _parse_entries(text)] == ["S1-1"]


def test_contributions_and_declared_markers_parse(tmp_path):
    text = registry(claims=claim_row(), contribs=contrib_row(), decls=decl_row())
    entries = _parse_entries(text)
    assert [(e.entry_id, e.unit_type, e.schema) for e in entries] == [
        ("C1", "CONTRIBUTION", "DR-027"),
        ("D1", "DECLARED", "DR-027"),
        ("S1-1", "DESCRIPTIVE", "DR-027"),
    ]


def test_suffixed_and_new_ids_parse(tmp_path):
    text = registry(
        claims=claim_row("S2-3a", tier="ESTABLISHED") + claim_row("S2-3b", grounds="claim: S2-3a", warrant="w"),
        contribs=contrib_row("C1", rests="claim: S2-3b"),
        decls=decl_row("D1"),
    )
    entries = {e.entry_id: e for e in _parse_entries(text)}
    assert set(entries) == {"S2-3a", "S2-3b", "C1", "D1"}
    assert entries["S2-3b"].premises == ("S2-3a",)
    assert entries["C1"].premises == ("S2-3b",)


def test_old_premise_regex_reads_suffixed_ids():
    table = (
        "**ARGUMENTs** (Toulmin):\n\n| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Status |\n"
        "|---|---|---|---|---|---|---|---|\n| S2-1 | x | P0 | EMERGING | S1-1a; S1-2 | w | r | [x] |\n"
    )
    (entry,) = _parse_entries(table)
    assert entry.premises == ("S1-1a", "S1-2")


@pytest.mark.parametrize(
    "first_cell",
    ["S1.2", "**S1-1**", "X9", ""],
)
def test_a_row_whose_id_matches_no_pattern_is_reported_not_dropped(tmp_path, first_cell):
    old = (
        "**CLAIMs:**\n\n| ID | Statement | Priority | Confidence | Source | Source Tier | Status |\n"
        "|---|---|---|---|---|---|---|\n| S1-1 | a | P1 | EMERGING | s | A | [x] |\n"
        f"| {first_cell} | b | P1 | EMERGING | s | A | [x] |\n"
    )
    report = check_registry(write(tmp_path, old))
    hits = [f for f in report.findings if "matches no entry-ID pattern" in f.message]
    # A DR-004 table: reported as a note, so an unmigrated registry keeps master's exit code.
    assert len(hits) == 1 and hits[0].severity == "note"
    assert report.ok is True


def test_unmatched_id_is_reported_in_new_tables_too(tmp_path):
    text = registry(claims=claim_row() + claim_row("Claim-2"))
    assert any("matches no entry-ID pattern" in m for m in schema_messages(tmp_path, text))


def test_a_section_divider_is_not_an_unmatched_row(tmp_path):
    old = (
        "**CLAIMs:**\n\n| ID | Statement | Priority | Confidence | Source | Source Tier | Status |\n"
        "|---|---|---|---|---|---|---|\n| **PART ONE** |\n| S1-1 | a | P1 | EMERGING | s | A | [x] |\n"
    )
    assert check_registry(write(tmp_path, old)).ok


# --------------------------------------------------------------------------
# deprecation (alias path)
# --------------------------------------------------------------------------

OLD_REGISTRY = (
    "**CLAIMs:**\n\n| ID | Statement | Priority | Confidence | Source | Source Tier | Status |\n"
    "|---|---|---|---|---|---|---|\n| S1-1 | a | P0 | SUPPORTED | s | A | [x] |\n\n"
    "**ARGUMENTs** (Toulmin):\n\n| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Status |\n"
    "|---|---|---|---|---|---|---|---|\n| S2-1 | x | P1 | EMERGING | S1-1 | w | r | [x] |\n"
)


def test_deprecation_note_appears_once_and_exit_codes_are_unchanged(tmp_path, capsys):
    path = write(tmp_path, OLD_REGISTRY)
    assert coverage_main([str(path), "--strict"]) == 0
    out = capsys.readouterr().out
    assert out.count("deprecated in v5.0.0") == 1
    assert cr.main([str(path)]) == 0
    out = capsys.readouterr().out
    assert out.count("deprecated in v5.0.0") == 1
    report = check_registry(path)
    assert report.ok and not report.findings  # a note in the report, never a Finding
    assert len(report.to_dict()["deprecations"]) == 1
    assert len(check_coverage(path).to_dict()["deprecations"]) == 1


def test_old_rows_keep_old_labels_and_rules(tmp_path):
    report = check_coverage(write(tmp_path, OLD_REGISTRY))
    assert {r.unit_type for r in report.rows} == {"CLAIM", "ARGUMENT"}


def test_no_deprecation_note_for_new_or_provocation_markers(tmp_path):
    prov = (
        "**PROVOCATIONs** (Auger):\n\n| ID | Provocation | Tier | Status |\n|---|---|---|---|\n"
        "| S9-1 | p | GROUNDED | [x] |\n\n"
    )
    path = write(tmp_path, prov + registry(claims=claim_row()))
    assert check_coverage(path).deprecations == ()
    assert check_registry(path).deprecations == ()
    assert "Deprecation" not in check_registry(path).to_markdown()


def test_a_failing_old_registry_still_exits_one(tmp_path):
    path = write(tmp_path, OLD_REGISTRY.replace("| P0 | SUPPORTED |", "| P0 | EMERGING |"))
    assert coverage_main([str(path), "--strict"]) == 1


# --------------------------------------------------------------------------
# Claims schema
# --------------------------------------------------------------------------


def test_clean_new_schema_registry_has_no_findings(tmp_path):
    text = registry(
        claims=claim_row("S1-1", tier="ESTABLISHED")
        + claim_row("S1-2", says="normative", grounds="claim: S1-1; decl: D1", warrant="w", rebuttal="only in X"),
        contribs=contrib_row("C1", rests="claim: S1-2; decl: D1", tier="SUPPORTED"),
        decls=decl_row("D1"),
    )
    report = check_registry(write(tmp_path, text))
    assert report.ok, report.findings
    assert report.counts["schema"] == 4


@pytest.mark.parametrize("says", ["prescriptive", "", "Descriptive-ish"])
def test_invalid_says_is_a_finding(tmp_path, says):
    msgs = schema_messages(tmp_path, registry(claims=claim_row(says=says)))
    assert any("Says is" in m for m in msgs)


def test_says_is_case_insensitive(tmp_path):
    assert schema_messages(tmp_path, registry(claims=claim_row(says="Descriptive"))) == []


def test_invalid_says_reports_as_unclassified_in_coverage(tmp_path):
    report = check_coverage(write(tmp_path, registry(claims=claim_row(says="maybe"))))
    assert [r.unit_type for r in report.rows] == ["UNCLASSIFIED"]


def test_untyped_grounds_item_is_a_finding(tmp_path):
    msgs = schema_messages(tmp_path, registry(claims=claim_row(grounds="src: A 2020; Smith 2021")))
    assert any("untyped" in m and "Smith 2021" in m for m in msgs)


def test_empty_grounds_is_a_finding(tmp_path):
    msgs = schema_messages(tmp_path, registry(claims=claim_row(grounds="")))
    assert any("records no **grounds**" in m for m in msgs)


def test_claim_grounds_without_warrant_is_a_finding(tmp_path):
    text = registry(claims=claim_row("S1-1") + claim_row("S1-2", grounds="claim: S1-1", tier="EMERGING"))
    msgs = schema_messages(tmp_path, text, "S1-2")
    assert any("no **warrant**" in m for m in msgs)
    fixed = text.replace("| claim: S1-1 |  |", "| claim: S1-1 | because |")
    assert schema_messages(tmp_path, fixed, "S1-2") == []


def test_src_only_grounds_need_no_warrant(tmp_path):
    msgs = schema_messages(tmp_path, registry(claims=claim_row(grounds="src: A 2020; src: B 2021")))
    assert msgs == []


def test_normative_claim_without_declared_value_is_a_finding(tmp_path):
    text = registry(
        claims=claim_row(says="normative", grounds="src: A; decl: D1", rebuttal="bounds"),
        decls=decl_row("D1", kind="definition"),
    )
    msgs = schema_messages(tmp_path, text, "S1-1")
    assert any("names no declared value" in m for m in msgs)
    ok = text.replace("| definition |", "| value |")
    assert schema_messages(tmp_path, ok, "S1-1") == []


def test_normative_claim_without_rebuttal_is_a_finding(tmp_path):
    text = registry(claims=claim_row(says="normative", grounds="src: A; decl: D1", rebuttal="—"), decls=decl_row())
    msgs = schema_messages(tmp_path, text, "S1-1")
    assert any("no **rebuttal**" in m for m in msgs)


@pytest.mark.parametrize(
    "grounds, needle",
    [
        ("claim: S9-9", "cites premise `S9-9`"),
        ("decl: D7", "cites declared starting point `D7`"),
        ("claim: D1", "is a declared starting point"),
        ("decl: S1-2", "not a declared starting point"),
        ("claim: S1-2, S1-3", "does not name a single entry ID"),
    ],
)
def test_unresolved_or_mistyped_references_are_findings(tmp_path, grounds, needle):
    text = registry(
        claims=claim_row("S1-1", grounds=grounds, warrant="w", tier="SPECULATIVE") + claim_row("S1-2"),
        decls=decl_row("D1"),
    )
    msgs = schema_messages(tmp_path, text, "S1-1")
    assert any(needle in m for m in msgs), msgs


def test_referenced_claim_must_be_verified(tmp_path):
    text = registry(
        claims=claim_row("S1-1", status="[ ]") + claim_row("S1-2", grounds="claim: S1-1", warrant="w", tier="EMERGING")
    )
    assert any("not verified" in m for m in schema_messages(tmp_path, text, "S1-2"))


def test_tier_monotonicity_over_claim_edges(tmp_path):
    text = registry(
        claims=claim_row("S1-1", tier="EMERGING")
        + claim_row("S1-2", grounds="claim: S1-1; src: X", warrant="w", tier="SUPPORTED")
    )
    msgs = schema_messages(tmp_path, text, "S1-2")
    assert any("weakest premise `S1-1` is EMERGING" in m for m in msgs)


def test_src_and_decl_items_are_not_monotonicity_edges(tmp_path):
    text = registry(
        claims=claim_row("S1-1", grounds="src: Weak 2020; decl: D1", tier="ESTABLISHED"),
        decls=decl_row("D1"),
    )
    entry = next(e for e in _parse_entries(text) if e.entry_id == "S1-1")
    assert entry.premises == ()
    assert schema_messages(tmp_path, text, "S1-1") == []


def test_cycle_over_claim_edges_is_found(tmp_path):
    text = registry(
        claims=claim_row("S1-1", grounds="claim: S1-2", warrant="w", tier="EMERGING")
        + claim_row("S1-2", grounds="claim: S1-1", warrant="w", tier="EMERGING")
    )
    assert any("premise cycle" in m for m in schema_messages(tmp_path, text))


# --------------------------------------------------------------------------
# own: items (second trial migration; renamed from data:, which is Toulmin's term for all grounds)
# --------------------------------------------------------------------------


def test_bare_own_item_is_a_finding(tmp_path):
    msgs = schema_messages(tmp_path, registry(claims=claim_row(grounds="own:")))
    assert any("bare `own:`" in m for m in msgs)


def test_own_item_with_method_passes_and_is_not_an_edge(tmp_path):
    text = registry(claims=claim_row(grounds="own: corpus count, query Q1 (2026-03-01)"))
    assert schema_messages(tmp_path, text) == []
    (entry,) = _parse_entries(text)
    assert entry.premises == () and entry.decls == ()
    assert entry.items == (("own", "corpus count, query Q1 (2026-03-01)"),)


def test_data_prefix_is_not_a_grounds_type(tmp_path):
    """`data:` was renamed `own:` (Toulmin's "data" means all grounds); it now reads as untyped."""
    msgs = schema_messages(tmp_path, registry(claims=claim_row(grounds="data: corpus count, query Q1")))
    assert any("untyped" in m for m in msgs)


# --------------------------------------------------------------------------
# Contributions and declared starting points
# --------------------------------------------------------------------------


def test_contribution_with_non_p0_priority_is_a_finding(tmp_path):
    text = registry(claims=claim_row(), contribs=contrib_row(priority="P1"))
    msgs = schema_messages(tmp_path, text, "C1")
    assert any("P0 by definition" in m for m in msgs)


def test_contribution_counts_in_the_p0_floor(tmp_path):
    text = registry(claims=claim_row(priority="P0", tier="SUPPORTED"), contribs=contrib_row(tier="EMERGING"))
    path = write(tmp_path, text)
    report = check_coverage(path)
    assert report.p0_below_floor == ("C1",)
    assert report.meets_tier_floor is False
    assert coverage_main([str(path), "--strict"]) == 1


def test_contribution_with_mistyped_priority_still_enters_the_floor(tmp_path):
    report = check_coverage(write(tmp_path, registry(claims=claim_row(), contribs=contrib_row(priority="P1", tier="EMERGING"))))
    assert "C1" in report.p0_below_floor


def test_normative_contribution_needs_who_where_when_and_a_value(tmp_path):
    text = registry(claims=claim_row(), contribs=contrib_row(says="normative", rests="claim: S1-1"))
    msgs = schema_messages(tmp_path, text, "C1")
    assert any("no **who/where/when**" in m for m in msgs)
    assert any("names no declared value" in m for m in msgs)


def test_contribution_tier_may_not_exceed_its_weakest_claim(tmp_path):
    text = registry(claims=claim_row(tier="EMERGING"), contribs=contrib_row(tier="SUPPORTED"))
    assert any("weakest premise" in m for m in schema_messages(tmp_path, text, "C1"))


def test_declared_rows_are_excluded_from_coverage_and_reported_apart(tmp_path):
    text = registry(
        claims=claim_row(priority="P0", tier="SUPPORTED"),
        decls=decl_row("D1") + decl_row("D2", status="[ ]"),
    )
    path = write(tmp_path, text)
    report = check_coverage(path)
    assert sum(r.total for r in report.rows) == 1
    assert report.p0_ids == ("S1-1",)
    assert (report.declared_total, report.declared_verified) == (2, 1)
    assert "Declared starting points (DR-027): 2, of which 1 marked [x]" in report.to_markdown()
    assert report.to_dict()["declared_starting_points"] == {"total": 2, "verified": 1}


@pytest.mark.parametrize("kind, contested, needle", [("belief", "own", "Kind is"), ("value", "disputed", "Contestedness is")])
def test_declared_kind_and_contestedness_are_checked(tmp_path, kind, contested, needle):
    msgs = schema_messages(tmp_path, registry(decls=decl_row(kind=kind, contested=contested)), "D1")
    assert any(needle in m for m in msgs)


# --------------------------------------------------------------------------
# anchors
# --------------------------------------------------------------------------


def test_contribution_and_declared_anchors_are_matched():
    entries = _parse_entries(registry(claims=claim_row(), contribs=contrib_row(), decls=decl_row()))
    tex = "% S1-1: a (descriptive, P1, SUPPORTED)\n% C1: c (contribution, P0, SUPPORTED)\n% D1: d (value, accepted)\n"
    findings, examined = _check_anchors(entries, tex)
    assert findings == [] and examined == 3
    findings, _ = _check_anchors(entries, "% S1-1: a\n")
    assert sorted(f.entry_id for f in findings) == ["C1", "D1"]


def test_declared_anchor_without_tier_gives_no_note():
    copies, notes = _anchor_tiers("% D1: label (value, contested)\n% C1: c (contribution, P0, EMERGING)\n")
    assert notes == []
    assert copies == [("C1", "manuscript anchor line 2", "EMERGING")]


def test_contribution_anchor_tier_disagreement_is_found(tmp_path):
    reg = write(tmp_path, registry(claims=claim_row(), contribs=contrib_row(tier="SUPPORTED")))
    tex = write(
        tmp_path,
        "% S1-1: a (descriptive, P1, SUPPORTED)\n% C1: c (contribution, P0, EMERGING)\n",
        "m.tex",
    )
    report = check_registry(reg, manuscript_path=tex)
    assert [f.entry_id for f in report.findings if f.check == "tiers" and f.severity == "finding"] == ["C1"]


# --------------------------------------------------------------------------
# glossary (DR-028)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "content, needle",
    [
        (None, "not found"),
        ("  \n\n", "empty"),
        ("# Glossary\n\n**Paper:** [Title]\n", "template's placeholders"),
    ],
)
def test_glossary_missing_empty_or_template_is_a_finding(tmp_path, content, needle):
    reg = write(tmp_path, registry(claims=claim_row()))
    gloss = tmp_path / "glossary.md"
    if content is not None:
        gloss.write_text(content, encoding="utf-8")
    report = check_registry(reg, glossary_path=gloss)
    hits = [f for f in report.findings if f.check == "glossary"]
    assert len(hits) == 1 and needle in hits[0].message
    assert report.ok is False
    assert cr.main([str(reg), "--glossary", str(gloss)]) == 1


def test_filled_glossary_passes(tmp_path):
    reg = write(tmp_path, registry(claims=claim_row()))
    gloss = write(tmp_path, "# Glossary\n\n**Paper:** The Verification Gap\n\nclaim: ...\n", "glossary.md")
    report = check_registry(reg, glossary_path=gloss)
    assert report.ok and "glossary" in report.checks_run
    assert "| glossary | 1 | 0 |" in report.to_markdown()
    assert "not checked" not in report.to_markdown()


def test_absent_glossary_flag_says_not_checked(tmp_path, capsys):
    reg = write(tmp_path, registry(claims=claim_row()))
    report = check_registry(reg)
    assert report.ok and "glossary" not in report.checks_run
    assert "glossary: not checked" in report.to_markdown()
    assert cr.main([str(reg), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["glossary"] == "not checked"


# --------------------------------------------------------------------------
# the hand-migrated Paper 1 registry
# --------------------------------------------------------------------------


def test_v5_fixture_p0_floor_is_three_of_six_failing():
    report = check_coverage(V5_FIXTURE)
    assert len(report.p0_ids) == 6
    assert sorted(report.p0_below_floor) == ["C1", "S2-2", "S3-4"]
    assert report.deprecations == ()
    assert (report.declared_total, report.declared_verified) == (6, 4)
    assert {r.unit_type for r in report.rows} == {"CONTRIBUTION", "DESCRIPTIVE", "NORMATIVE"}
    assert coverage_main([str(V5_FIXTURE)]) == 0  # runs without error


def test_v5_fixture_reports_s5_2_as_underspecified_normative():
    report = check_registry(V5_FIXTURE)
    s52 = [f.message for f in report.findings if f.entry_id == "S5-2" and f.severity == "finding"]
    assert any("no **rebuttal**" in m for m in s52)
    assert any("names no declared value" in m for m in s52)
    assert len(report.entries) == 24
    assert report.counts["schema"] == 24
