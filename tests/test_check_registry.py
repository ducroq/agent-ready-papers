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
    _check_tiers,
    _find_cycles,
    _normalise_tier,
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
# tiers — every copy of an ID's tier agrees (#37)
# --------------------------------------------------------------------------

REGISTRY_TABLE_TEX = r"""\begin{tabular}{@{}lllll@{}}
\toprule
\textbf{ID} & \textbf{Type} & \textbf{Priority} & \textbf{Confidence} & \textbf{Status} \\
\midrule
S1-1 & Claim & P0 & Established & Verified \\
S1-2 & Claim & P1 & Emerging    & Verified \\
\bottomrule
\end{tabular}
"""


def test_tiers_pass_when_every_copy_agrees():
    """Registry, anchor and printed table agree; the table's title case
    ("Emerging") must match the registry's "EMERGING"."""
    entries = (_entry("S1-1", tier="ESTABLISHED"), _entry("S1-2", tier="EMERGING"))
    manuscript = "% S1-1: a (CLAIM, P0, ESTABLISHED)\n% S1-2: b (CLAIM, P1, EMERGING)\n" + REGISTRY_TABLE_TEX
    findings, examined = _check_tiers(entries, manuscript)
    assert findings == []
    assert examined == 2


def test_tiers_flag_an_anchor_disagreeing_with_the_registry():
    """The live case at 828f9cd^: registry raised to SUPPORTED, anchor left at EMERGING."""
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    findings, examined = _check_tiers(entries, "text\n% S1-1: a (CLAIM, P0, EMERGING)\n")
    assert [(f.entry_id, f.severity) for f in findings] == [("S1-1", "finding")]
    assert "registry line 1 `SUPPORTED`" in findings[0].message
    assert "manuscript anchor line 2 `EMERGING`" in findings[0].message
    assert examined == 1


def test_tiers_flag_a_printed_table_disagreeing_with_the_registry():
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="EMERGING"))
    findings, _ = _check_tiers(entries, REGISTRY_TABLE_TEX)
    assert [f.entry_id for f in findings] == ["S1-1"]
    assert "manuscript table line 5 `Established`" in findings[0].message


def test_tiers_flag_an_id_whose_registry_rows_disagree():
    """An ID may appear in more than one registry sub-table."""
    content = CLAIM_TABLE + "\n" + ARGUMENT_TABLE.replace("S2-1", "S1-1")
    findings, _ = _check_tiers(_parse_entries(content), "")
    assert [f.entry_id for f in findings] == ["S1-1"]


def test_tiers_note_an_anchor_with_no_parseable_tier():
    """A copy the check cannot read is reported, never skipped in silence."""
    entries = (_entry("S1-1"),)
    findings, examined = _check_tiers(entries, "% S1-1: no parenthesis\n% S1-1: short (CLAIM, P0)\n")
    assert [(f.severity, f.check, f.entry_id) for f in findings] == [
        ("note", "tiers", "S1-1"),
        ("note", "tiers", "S1-1"),
        ("note", "tiers", ""),  # and the check says it compared nothing
    ]
    assert examined == 0


def test_tiers_ignore_a_tabular_without_a_confidence_column():
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = REGISTRY_TABLE_TEX.replace(r"\textbf{Confidence}", r"\textbf{Notes}")
    findings, examined = _check_tiers(entries, tex)
    assert [f.severity for f in findings] == ["note"]  # "compared NOTHING", never a silent zero
    assert examined == 0


def test_tiers_examined_counts_only_ids_with_two_copies():
    entries = (_entry("S1-1"), _entry("S1-2"))
    _, examined = _check_tiers(entries, "% S1-1: a (CLAIM, P0, EMERGING)\n")
    assert examined == 1


def test_tiers_read_the_table_forms_a_manuscript_actually_uses():
    """Seeded from review 2026-09-25: each of these was skipped in silence, and
    the ID still counted as agreeing. longtable, tabularx, a macro-wrapped ID,
    a group-header row above the real header, a leading \\hline, an escaped
    \\& in an earlier cell, and a macro-wrapped tier."""
    entries = tuple(_entry(f"S1-{n}", tier="SUPPORTED") for n in range(1, 6))
    tex = r"""\begin{longtable}{lll}
ID & Type & Confidence \\
S1-1 & Claim & Speculative \\
\end{longtable}
\begin{tabularx}{\textwidth}{lXl}
 & \multicolumn{2}{c}{Registry} \\
ID & Statement & Confidence \\
\texttt{S1-2} & x & Speculative \\
\hline S1-3 & a \& b & Speculative \\
S1-4 & wrapped
  over two lines & \textsc{Speculative} \\ S1-5 & two rows on one line & Speculative \\
\end{tabularx}
"""
    findings, examined = _check_tiers(entries, tex)
    assert [f.entry_id for f in findings if f.severity == "finding"] == ["S1-1", "S1-2", "S1-3", "S1-4", "S1-5"]
    assert all("`Speculative`" in f.message for f in findings)
    assert examined == 5


def test_tiers_multicolumn_header_does_not_shift_the_confidence_index():
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = r"""\begin{tabular}{llll}
\multicolumn{2}{c}{Entry} & Priority & Confidence \\
S1-1 & Claim & P0 & Supported \\
\end{tabular}
"""
    findings, examined = _check_tiers(entries, tex)
    assert findings == [] and examined == 1


def test_tiers_note_a_table_row_too_short_to_reach_confidence():
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="EMERGING"))
    tex = REGISTRY_TABLE_TEX.replace(r"S1-2 & Claim & P1 & Emerging    & Verified", "S1-2 & Claim")
    findings, _ = _check_tiers(entries, tex)
    assert {(f.severity, f.entry_id) for f in findings} == {("finding", "S1-1"), ("note", "S1-2")}


def test_tiers_see_through_a_trailing_comment_on_an_anchor():
    """`% was SUPPORTED` after the parenthesis must not demote the #37 drift to a note."""
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    findings, _ = _check_tiers(entries, "% S1-1: a (CLAIM, P0, EMERGING) % was SUPPORTED\n")
    assert [(f.severity, f.entry_id) for f in findings] == [("finding", "S1-1")]


@pytest.mark.parametrize(
    "row_end",
    [r"\\", r"\\[2pt]", r"\\*", r"\tabularnewline", "\\\\ % trailing comment\n"],
)
def test_tiers_read_every_row_terminator(row_end):
    """Round 2 (2026-09-25): after `\\[2pt]`, `\\*` or `\tabularnewline` every
    later row was dropped in silence, and `\\%` swallowed the next row."""
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="SUPPORTED"))
    tex = (
        "\\begin{tabular}{ll}\nID & Confidence " + row_end + "\nS1-1 & Speculative " + row_end + "\n"
        "S1-2 & Speculative " + row_end + "\n\\end{tabular}\n"
    )
    findings, examined = _check_tiers(entries, tex)
    assert [f.entry_id for f in findings if f.severity == "finding"] == ["S1-1", "S1-2"]
    assert examined == 2


def test_tiers_strip_row_leading_rules_and_cell_decoration():
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="SUPPORTED"))
    tex = r"""\begin{tabular}{ll}
ID & Confidence \\
\cmidrule(lr){1-2} \rowcolor{gray} S1-1\footnote{see text} & Supported$^\dagger$ \\
\cline{1-2} S1-2 & \textsc{Supported}\footnote{x} \\
\end{tabular}
"""
    findings, examined = _check_tiers(entries, tex)
    assert findings == [] and examined == 2


def test_tiers_pass_over_a_caption_that_mentions_confidence():
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = r"""\begin{longtable}{ll}
\caption{Claims by confidence tier} \\
ID & Confidence \\ \endhead
S1-1 & Supported \\
\end{longtable}
"""
    findings, examined = _check_tiers(entries, tex)
    assert findings == [] and examined == 1


def test_tiers_note_a_confidence_header_spanning_columns():
    """Which of Before/After is "the" tier is ambiguous; say so, don't guess."""
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = r"""\begin{tabular}{llll}
\multicolumn{2}{c}{Claim} & \multicolumn{2}{c}{Confidence} \\
ID & Claim & Before & After \\
S1-1 & a & Emerging & Supported \\
\end{tabular}
"""
    findings, _ = _check_tiers(entries, tex)
    assert any(f.severity == "note" and "ambiguous" in f.message for f in findings)
    assert not any(f.severity == "finding" for f in findings)


def test_tiers_backstop_notes_an_id_no_row_accounted_for():
    """The net under the whole silent-drop class: an ID in a Confidence table's
    body that yields neither a copy nor a note is itself a note."""
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = r"""\begin{tabular}{ll}
ID & Confidence \\
S1-1 & Supported \\
Merged into & S1-9 \\
\end{tabular}
"""
    findings, _ = _check_tiers(entries, tex)
    assert [(f.severity, f.entry_id) for f in findings] == [("note", "S1-9")]


def test_tiers_ignore_tables_in_verbatim_and_comments():
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    table = "\\begin{tabular}{ll}\nID & Confidence \\\\\nS1-1 & Speculative \\\\\n\\end{tabular}\n"
    tex = "\\begin{verbatim}\n" + table + "\\end{verbatim}\n" + "".join("% " + ln + "\n" for ln in table.splitlines())
    findings, examined = _check_tiers(entries, tex)
    assert not any(f.severity == "finding" for f in findings)
    assert examined == 0


def test_tiers_anchor_prose_may_contain_a_percent_sign():
    """The anchor is already a comment, so `100%` is prose, not a second comment."""
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    findings, examined = _check_tiers(entries, "% S1-1: 100% of them (CLAIM, P0, SUPPORTED)\n")
    assert findings == [] and examined == 1


def test_tiers_anchor_reads_the_tier_not_the_history_in_its_comment_tail():
    """Round 3: `% raised from (…, EMERGING)` after the real tier used to be
    read instead of it, masking a disagreement."""
    entries = (_entry("S1-1", tier="EMERGING"),)
    anchor = "% S1-1: a (CLAIM, P0, SUPPORTED) % raised from (CLAIM, P0, EMERGING)\n"
    findings, _ = _check_tiers(entries, anchor)
    assert [(f.severity, f.entry_id) for f in findings] == [("finding", "S1-1")]
    assert "`SUPPORTED`" in findings[0].message


@pytest.mark.parametrize("typed_id", ["S1--1", "S1–1", "S1 -- 1", r"S1\-1", "S1$-$1", "S1{-}1"])
def test_tiers_read_latex_typed_id_dashes(typed_id):
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = "\\begin{tabular}{ll}\nID & Confidence \\\\\n" + typed_id + " & Emerging \\\\\n\\end{tabular}\n"
    findings, _ = _check_tiers(entries, tex)
    assert [(f.severity, f.entry_id) for f in findings] == [("finding", "S1-1")]


def test_tiers_note_a_nested_table():
    """Nested tables are unsupported; the rows after one must not vanish unannounced."""
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="SUPPORTED"))
    tex = r"""\begin{tabular}{ll}
ID & Confidence \\
S1-1 & \begin{tabular}{@{}l@{}}Supported\\x\end{tabular} \\
S1-2 & Emerging \\
\end{tabular}
"""
    findings, _ = _check_tiers(entries, tex)
    assert any(f.severity == "note" and "nested table" in f.message for f in findings)


def test_tiers_commented_verbatim_opener_does_not_swallow_tables():
    entries = (_entry("S1-1", tier="SUPPORTED"),)
    tex = (
        "% \\begin{verbatim}\n\\begin{tabular}{ll}\nID & Confidence \\\\\nS1-1 & Emerging \\\\\n\\end{tabular}\n"
        "\\begin{verbatim}\nx\n\\end{verbatim}\n"
    )
    findings, _ = _check_tiers(entries, tex)
    assert [(f.severity, f.entry_id) for f in findings] == [("finding", "S1-1")]


def test_tiers_read_the_text_argument_of_multirow_and_not_a_prefix_macro():
    entries = (_entry("S1-1", tier="SUPPORTED"), _entry("S1-2", tier="SUPPORTED"))
    tex = r"""\begin{tabular}{ll}
ID & Confidence \\
S1-1 & \multirow{2}{*}{Supported} \\
S1-2 & \reflectbox{Supported} \\
\end{tabular}
"""
    findings, examined = _check_tiers(entries, tex)
    assert findings == [] and examined == 2


def test_normalise_tier_matches_coverage_copy():
    """The two copies are kept equivalent by hand (importing would be circular);
    this is what keeps the tiers check and the P0 floor reading a cell alike."""
    from tools.coverage import _normalise_tier as coverage_normalise

    for raw in ("**SUPPORTED**", "`EMERGING`", "SUPPORTED ⚠", "Emerging", "SPECULATIVE (provisional)", "~~X~~", ""):
        assert _normalise_tier(raw) == coverage_normalise(raw)


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
    assert "tiers" not in report.checks_run
    assert report.ok is True


def test_notes_alone_do_not_fail_the_run(tmp_path):
    reg = tmp_path / "r.md"
    reg.write_text(CLAIM_TABLE, encoding="utf-8")
    man = tmp_path / "m.tex"
    # Anchors carry tiers matching the registry, so the budget note is the only one.
    man.write_text(
        "% S1-1: x (CLAIM, P0, ESTABLISHED)\n% S1-2: y (CLAIM, P1, EMERGING)\n" + " ".join(["w"] * 96),
        encoding="utf-8",
    )
    report = check_registry(reg, manuscript_path=man, budget=100)
    assert [f.severity for f in report.findings] == ["note"]
    assert report.ok is True


# --- tier-monotonicity must never skip in silence (seeded 2026-09-14) ---------
#
# `_TIER_RANK.get(raw)` returned None for anything it did not recognise and the
# comparison was then skipped with NO finding and NO change to the Examined
# count — so a registry where the check was inert printed exactly what a clean
# registry prints. Three reachable paths, all measured, all seeded below.


def _arg(entry_id: str, tier: str, premises: tuple[str, ...] = ()) -> Entry:
    return Entry(
        entry_id=entry_id,
        unit_type="ARGUMENT",
        tier=tier,
        verified=True,
        line_number=1,
        columns={},
        premises=premises,
    )


def test_normalise_tier_strips_cell_decoration():
    """Registries legitimately bold or quote a tier cell."""
    for raw in ("**SPECULATIVE**", " `SPECULATIVE` ", "SPECULATIVE ⚠", "speculative"):
        assert _normalise_tier(raw) == "SPECULATIVE", raw
    assert _normalise_tier("SUPPORTED (provisional)") == "SUPPORTED"


def test_decorated_premise_tier_is_ranked_not_skipped():
    """A bold premise tier must produce the REAL monotonicity finding."""
    entries = (_arg("S1-2", "ESTABLISHED", ("S1-1",)), _arg("S1-1", "**SPECULATIVE**"))
    findings, _ = _check_premises(entries)
    assert any("may not outrank" in f.message for f in findings)


def test_unrankable_premise_tier_is_reported_not_skipped():
    """An absent tier, a PROVOCATION-axis tier and a bogus string must each be
    REPORTED. Silence here is indistinguishable from a clean pass."""
    for tier, needle in (
        ("", "records no confidence tier"),
        ("PROVOCATIVE", "PROVOCATION axis"),
        ("PROBABLY-FINE", "not one of"),
    ):
        entries = (_arg("S1-2", "ESTABLISHED", ("S1-1",)), _arg("S1-1", tier))
        findings, _ = _check_premises(entries)
        assert any(needle in f.message for f in findings), f"{tier!r} skipped silently"
        assert any("could NOT be checked" in f.message for f in findings), tier


def test_unrankable_own_tier_is_reported_not_skipped():
    """The conclusion's own tier has the same hole: unrecognised meant no
    comparison at all, silently."""
    entries = (_arg("S1-2", "", ("S1-1",)), _arg("S1-1", "SPECULATIVE"))
    findings, _ = _check_premises(entries)
    assert any("could NOT be checked" in f.message for f in findings)
