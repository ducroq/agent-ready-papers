"""Tests for tools.check_registry.

Every check here is exercised twice: once against input it should pass,
once against seeded input it must fail. A check that only ever sees clean
input cannot be told apart from a check that is absent — the rule
`docs/verification-hooks.md` states, applied to the suite rather than the
output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.check_registry import (
    Entry,
    _check_anchors,
    _check_budget,
    _check_premises,
    _check_schema,
    _find_cycles,
    _parse_entries,
    check_registry,
    count_words,
)

CLAIM_TABLE = """**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S1-1 | A claim | P0 | ESTABLISHED | Somewhere | A | [x] |
| S1-2 | Another | P1 | EMERGING | Elsewhere | F | [x] |
"""

ARGUMENT_TABLE = """**ARGUMENTs** (Toulmin):

| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Source | Source Tier | Status |
|----|-----------|----------|------------|---------|---------|----------|--------|-------------|--------|
| S2-1 | An argument | P0 | EMERGING | S1-1; S1-2 | Because X licenses Y | Unless Z | Own | F | [x] |
"""


def _entry(entry_id, unit_type="CLAIM", tier="EMERGING", verified=True, premises=(), **cols):
    return Entry(
        entry_id=entry_id,
        unit_type=unit_type,
        tier=tier,
        verified=verified,
        line_number=1,
        columns=dict(cols),
        premises=tuple(premises),
    )


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


def test_parse_entries_reads_id_type_tier_and_status():
    entries = _parse_entries(CLAIM_TABLE + "\n" + ARGUMENT_TABLE)
    assert [e.entry_id for e in entries] == ["S1-1", "S1-2", "S2-1"]
    assert [e.unit_type for e in entries] == ["CLAIM", "CLAIM", "ARGUMENT"]
    assert entries[0].tier == "ESTABLISHED"
    assert all(e.verified for e in entries)


def test_parse_entries_reads_premises_from_grounds_for_arguments():
    (argument,) = [e for e in _parse_entries(ARGUMENT_TABLE) if e.unit_type == "ARGUMENT"]
    assert argument.premises == ("S1-1", "S1-2")


def test_parse_entries_marks_unverified_status():
    table = CLAIM_TABLE.replace(
        "| S1-2 | Another | P1 | EMERGING | Elsewhere | F | [x] |",
        "| S1-2 | Another | P1 | EMERGING | Elsewhere | F | [ ] |",
    )
    entries = _parse_entries(table)
    assert entries[1].verified is False


def test_parse_entries_ignores_non_entry_rows():
    noise = "| Priority | Total | Verified |\n|---|---|---|\n| P0 | 8 | 8 |\n\n"
    assert len(_parse_entries(noise + CLAIM_TABLE)) == 2


# --------------------------------------------------------------------------
# anchors — must fire in both directions
# --------------------------------------------------------------------------


def test_anchors_pass_when_manuscript_and_registry_agree():
    entries = (_entry("S1-1"), _entry("S1-2"))
    findings, examined = _check_anchors(entries, "% S1-1: blah\ntext\n% S1-2: blah\n")
    assert findings == []
    assert examined == 2


def test_anchors_flag_a_registered_entry_with_no_prose_anchor():
    """The live case: S4-1/S4-2/S4-4 in Paper 1."""
    entries = (_entry("S1-1"), _entry("S1-2"))
    findings, _ = _check_anchors(entries, "% S1-1: only this one\n")
    assert [f.entry_id for f in findings] == ["S1-2"]
    assert findings[0].severity == "finding"


def test_anchors_flag_prose_the_registry_does_not_track():
    findings, _ = _check_anchors((_entry("S1-1"),), "% S1-1: ok\n% S9-9: untracked\n")
    assert [f.entry_id for f in findings] == ["S9-9"]


def test_anchor_regex_requires_the_colon_form():
    """`% Registry entries: S4-1, S4-2` is a section header, not an anchor —
    counting it would have hidden the very finding this check exists for."""
    findings, _ = _check_anchors((_entry("S4-1"),), "% Registry entries: S4-1, S4-2\n")
    assert [f.entry_id for f in findings] == ["S4-1"]


# --------------------------------------------------------------------------
# schema — presence only, never quality
# --------------------------------------------------------------------------


def test_schema_passes_a_complete_argument_row():
    findings, examined = _check_schema(_parse_entries(ARGUMENT_TABLE))
    assert findings == []
    assert examined == 1


def test_schema_flags_a_missing_warrant():
    table = ARGUMENT_TABLE.replace("| Because X licenses Y ", "|  ")
    findings, _ = _check_schema(_parse_entries(table))
    assert [f.entry_id for f in findings] == ["S2-1"]
    assert "warrant" in findings[0].message


@pytest.mark.parametrize("placeholder", ["-", "--", "—", "TBD", "N/A"])
def test_schema_treats_placeholders_as_absent(placeholder):
    table = ARGUMENT_TABLE.replace("| Unless Z ", f"| {placeholder} ")
    findings, _ = _check_schema(_parse_entries(table))
    assert any("rebuttal" in f.message for f in findings)


def test_schema_ignores_claim_rows_entirely():
    findings, examined = _check_schema(_parse_entries(CLAIM_TABLE))
    assert findings == []
    assert examined == 0


# --------------------------------------------------------------------------
# premises — resolution, verification, tier monotonicity, cycles
# --------------------------------------------------------------------------


def test_premises_pass_when_conclusion_does_not_outrank_its_weakest():
    entries = (
        _entry("S1-1", tier="ESTABLISHED"),
        _entry("S1-2", tier="EMERGING"),
        _entry("S2-1", tier="EMERGING", premises=("S1-1", "S1-2")),
    )
    findings, examined = _check_premises(entries)
    assert findings == []
    assert examined == 1


def test_premises_flag_a_conclusion_outranking_its_weakest_premise():
    entries = (
        _entry("S1-1", tier="ESTABLISHED"),
        _entry("S1-2", tier="EMERGING"),
        _entry("S2-1", tier="ESTABLISHED", premises=("S1-1", "S1-2")),
    )
    findings, _ = _check_premises(entries)
    assert len(findings) == 1
    assert "may not outrank" in findings[0].message
    assert "S1-2" in findings[0].message


def test_premises_flag_a_missing_referenced_id():
    entries = (_entry("S2-1", premises=("S9-9",)),)
    findings, _ = _check_premises(entries)
    assert "not in the registry" in findings[0].message


def test_premises_flag_resting_on_an_unverified_entry():
    entries = (
        _entry("S1-1", verified=False),
        _entry("S2-1", premises=("S1-1",)),
    )
    findings, _ = _check_premises(entries)
    assert any("not verified" in f.message for f in findings)


def test_premises_detect_a_cycle():
    entries = (
        _entry("S1-1", premises=("S1-2",)),
        _entry("S1-2", premises=("S1-1",)),
    )
    findings, _ = _check_premises(entries)
    assert any("premise cycle" in f.message for f in findings)


def test_find_cycles_returns_nothing_for_a_dag():
    assert _find_cycles({"a": ("b",), "b": ("c",), "c": ()}) == []


def test_find_cycles_handles_self_reference():
    assert _find_cycles({"a": ("a",)}) == [("a",)]


# --------------------------------------------------------------------------
# budget
# --------------------------------------------------------------------------


def test_count_words_strips_comments_math_and_macros():
    tex = (
        "% a comment line that should not count\n"
        "\\section{Heading}\n"
        "One two three four five.\n"
        "\\begin{equation}E = mc^2\\end{equation}\n"
        "\\cite{someone2020}\n"
    )
    # "Heading" survives as a word; the comment, equation and citation do not.
    assert 5 <= count_words(tex) <= 7


def test_budget_passes_under_the_limit():
    findings, words = _check_budget("one two three", 100)
    assert findings == []
    assert words == 3


def test_budget_flags_going_over():
    findings, _ = _check_budget("one two three four five", 3)
    assert findings[0].severity == "finding"
    assert "over" in findings[0].message


def test_budget_notes_approaching_the_limit_without_failing():
    findings, _ = _check_budget(" ".join(["w"] * 98), 100)
    assert [f.severity for f in findings] == ["note"]


# --------------------------------------------------------------------------
# contract
# --------------------------------------------------------------------------


def test_check_registry_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        check_registry(Path("no/such/registry.md"))


def test_empty_registry_is_an_error_not_a_clean_run(tmp_path):
    """A registry is never legitimately empty, so a vacuous pass would be
    indistinguishable from a parse failure."""
    path = tmp_path / "empty.md"
    path.write_text("# Registry\n\nNo tables here.\n", encoding="utf-8")
    with pytest.raises(ValueError):
        check_registry(path)


def test_report_leads_with_counts(tmp_path):
    path = tmp_path / "r.md"
    path.write_text(CLAIM_TABLE + "\n" + ARGUMENT_TABLE, encoding="utf-8")
    markdown = check_registry(path).to_markdown()
    assert "| Check | Examined | Findings |" in markdown
    assert "| schema | 1 | 0 |" in markdown


def test_anchor_check_is_skipped_without_a_manuscript(tmp_path):
    path = tmp_path / "r.md"
    path.write_text(CLAIM_TABLE, encoding="utf-8")
    report = check_registry(path)
    assert "anchors" not in report.checks_run
    assert report.ok is True


def test_notes_alone_do_not_fail_the_run(tmp_path):
    reg = tmp_path / "r.md"
    reg.write_text(CLAIM_TABLE, encoding="utf-8")
    man = tmp_path / "m.tex"
    man.write_text("% S1-1: x\n% S1-2: y\n" + " ".join(["w"] * 96), encoding="utf-8")
    report = check_registry(reg, manuscript_path=man, budget=100)
    assert [f.severity for f in report.findings] == ["note"]
    assert report.ok is True
