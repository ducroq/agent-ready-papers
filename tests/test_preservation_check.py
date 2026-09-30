"""Tests for extensions/preservation_check.py (PROPOSED under DR-023).

Each signal is exercised against a seeded change it must flag and against a
faithful rewrite it must not. A signal that only ever sees clean input cannot
be told apart from an absent one (docs/verification-hooks.md). One test pins a
known blind spot, so the reason Prompt C exists stays visible.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "preservation_check", Path(__file__).resolve().parent.parent / "extensions" / "preservation_check.py"
)
pc = importlib.util.module_from_spec(_SPEC)
sys.modules["preservation_check"] = pc  # dataclasses resolve types through sys.modules
_SPEC.loader.exec_module(pc)

BANDS = pc.read_bands(pc.DEFAULT_GUIDE)


def _kinds(src: str, trn: str, **kw) -> list[str]:
    return [f.kind for f in pc.check(src, trn, BANDS, **kw).flags]


# --- the guide -------------------------------------------------------------


def test_bands_are_read_from_the_writing_guide():
    assert list(BANDS) == list(pc.TIER_ORDER)
    assert "shows" in BANDS["ESTABLISHED"] and "may" in BANDS["EMERGING"]


def test_a_guide_without_the_table_fails_closed(tmp_path):
    g = tmp_path / "guide.md"
    g.write_text("# Guide\n\n## Language Calibration\n\nNo table here.\n\n## Next\n")
    with pytest.raises(pc.GuideError):
        pc.read_bands(g)


def test_a_tier_row_without_phrases_fails_closed(tmp_path):
    text = pc.DEFAULT_GUIDE.read_text().replace('"may", ', "").replace('"preliminary evidence", ', "")
    text = text.replace('"initial findings suggest"', "initial findings suggest")
    g = tmp_path / "guide.md"
    g.write_text(text)
    with pytest.raises(pc.GuideError, match="EMERGING"):
        pc.read_bands(g)


def test_cli_exits_2_on_an_unreadable_guide(tmp_path, capsys):
    s = tmp_path / "s.md"
    s.write_text("x")
    assert pc.main([str(s), str(s), "--guide", str(tmp_path / "missing.md")]) == 2


# --- numbers ---------------------------------------------------------------


def test_a_dropped_number_is_flagged():
    assert "number-missing" in _kinds("The log went from 85k to 33k.", "The log got much shorter.")


def test_reformatted_numbers_are_not_flagged():
    src = "It is 34,521 characters, 7% of the total, and three raters agreed."
    trn = "Three raters agreed. It is 34521 characters, which is 7 % of the total."
    assert _kinds(src, trn) == []


def test_digits_inside_identifiers_do_not_count():
    src = "DR-022, L86, #41, S2-2, v4.0.0 and commit 7059cac are cited; see `archive/p-2026-09-30.md`."
    trn = "The decision record and the issue are cited."
    assert [k for k in _kinds(src, trn) if k.startswith("number")] == []


def test_a_new_number_in_the_translation_is_flagged():
    assert "number-new" in _kinds("Most reviewers agreed.", "Nine of ten reviewers agreed, 90%.")


def test_a_dropped_date_is_reported_separately():
    assert _kinds("Decided on 2026-09-30.", "Decided recently.") == ["date-missing"]


def test_sample_size_counts_as_a_number():
    assert "number-missing" in _kinds("Evidence so far (n=4).", "Evidence so far.")


# --- tiers -----------------------------------------------------------------


def test_certainty_moving_up_a_band_is_flagged():
    src = "The pilot may reduce review time for new students."
    trn = "The pilot shows reduced review time for new students."
    kinds = _kinds(src, trn)
    assert "tier-up" in kinds and "tier-missing" in kinds and "band-count" in kinds


def test_certainty_moving_down_is_not_tier_up():
    src = "The pilot shows reduced review time for new students."
    trn = "The pilot may reduce review time for new students."
    kinds = _kinds(src, trn)
    assert "tier-up" not in kinds and "band-count" not in kinds
    assert "tier-missing" in kinds  # "shows" went missing: reported, the author decides


def test_inflected_tier_words_match():
    assert "tier-up" in _kinds("Results indicate a gap in coverage.", "Results demonstrated a gap in coverage.")


def test_a_negated_tier_word_is_not_a_claim():
    src = "The audit may find gaps in the registry."
    trn = "The audit does not show gaps in the registry yet; it may find them."
    assert "tier-up" not in _kinds(src, trn)


def test_tier_labels_in_capitals_are_not_language():
    src = "S2-2 stays EMERGING."
    trn = "S2-2 stays EMERGING, not ESTABLISHED."
    assert [k for k in _kinds(src, trn) if k.startswith(("tier", "band"))] == []


def test_a_confident_sentence_with_no_source_is_flagged():
    src = "The registry has six entries at P0."
    trn = "The registry has six entries at P0. Mechanisation demonstrates clear savings everywhere."
    assert "tier-unmatched" in _kinds(src, trn)


# --- hedges, absolutes, link -------------------------------------------------


def test_a_dropped_hedge_is_flagged():
    # The 2026-09-30 memory rewrite: "may be" made flat, "unverified" dropped.
    src = "The gap may be only in the scope statements. Two sources remain unverified."
    trn = "The gap is in the scope statements. Two sources remain."
    kinds = _kinds(src, trn)
    assert "hedge-missing" in kinds and "tier-missing" in kinds


def test_an_added_absolute_is_flagged():
    src = "The instances on record were caught by review."
    trn = "Every instance was caught by review, never by the rule."
    assert "absolute-added" in _kinds(src, trn)


def test_the_link_to_the_source_is_checked_only_when_asked():
    assert "link-missing" not in _kinds("A.", "A.")
    assert "link-missing" in _kinds("A.", "A.", link="docs/work-items/reports/r1.md")
    assert "link-missing" not in _kinds(
        "A.", "A. Source: docs/work-items/reports/r1.md", link="docs/work-items/reports/r1.md"
    )


# --- whole reports ---------------------------------------------------------


def test_a_faithful_translation_is_clean():
    src = (
        "| # | Severity | Finding |\n|---|---|---|\n"
        "| 1 | WARNING | 2 pointers still say *Resolved*; the entry may confuse readers |\n\n"
        "Verdict: 0 blockers, 1 warning, 5 files checked on 2026-09-30.\n"
    )
    trn = (
        "Nothing blocks the commit. There is 1 warning, from 5 files checked on 2026-09-30.\n\n"
        "The warning: 2 pointers still send readers to the old *Resolved* section, which may confuse them.\n"
    )
    assert _kinds(src, trn) == []


def test_a_source_with_nothing_to_check_says_so():
    rep = pc.check("The review found problems with the wording.", "The wording has problems.", BANDS)
    assert rep.examined_nothing
    assert "examined nothing" in pc.to_markdown(rep)


def test_every_report_names_the_claim_comparison():
    rep = pc.check("It shows 3 gaps.", "It shows 3 gaps.", BANDS)
    assert rep.flags == [] and "Prompt C" in pc.to_markdown(rep)


def test_known_blind_spot_an_added_claim_without_tier_words():
    # The #41 case: a claim added with no number and no tier word. The script
    # cannot see it; Prompt C exists for this. If this ever starts failing,
    # update the docstring and DR-023's description of the two halves.
    src = "It gives feedback that fits the course as it is taught."
    trn = "It gives feedback that works like an instructor would."
    assert _kinds(src, trn) == []


def test_json_output(tmp_path, capsys):
    s, t = tmp_path / "s.md", tmp_path / "t.md"
    s.write_text("It may take 3 days.")
    t.write_text("It takes days.")
    assert pc.main([str(s), str(t), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert {f["kind"] for f in data["flags"]} >= {"number-missing", "tier-missing"}


def test_all_and_every_count_as_one_class():
    # From the 2026-09-30 pilot: "All references carry" -> "Every reference carries".
    src = "All references carry the prefix. Ran every probe: all exit 0."
    trn = "Every reference carries the prefix. Every probe exits 0."
    assert "absolute-added" not in _kinds(src, trn)
    assert "absolute-added" in _kinds("Most references carry the prefix.", "Every reference carries the prefix.")


# --- round-1 review findings, each seeded --------------------------------------


def test_units_stay_attached_and_without_is_not_a_negation():
    # The review's blocker: zero flags before the fix.
    src = "The cache cut latency to 5ms on the 12GB box."
    trn = "Without doubt, this confirms the cache cut latency to 50ms on the 16GB box."
    kinds = _kinds(src, trn)
    assert {"number-missing", "number-new", "band-count"} <= set(kinds)
    assert "tier-up" in kinds or "tier-unmatched" in kinds


def test_a_hedge_after_a_negation_still_counts():
    assert "tier-missing" in _kinds("It is not proven; it may help.", "It helps.")


def test_not_only_does_not_hide_a_confident_word():
    assert "band-count" in _kinds("The pilot helped students.", "The pilot not only shows gains, it helps students.")


def test_a_minus_sign_is_kept():
    assert "number-missing" in _kinds("Loss was -5 points.", "Loss was 5 points.")


def test_a_new_number_written_as_a_word_is_flagged():
    assert "number-new" in _kinds("We found an issue.", "We found five issues.")


def test_zero_survives_only_as_no_of_the_same_thing():
    assert "number-missing" not in _kinds("0 blockers remain.", "Nothing blocks the commit.")
    assert "number-missing" in _kinds("0 checks failed.", "No reviewer has seen it; the checks ran.")


def test_a_new_date_is_flagged():
    assert "date-new" in _kinds("Released on 2026-09-30.", "Released on 2026-09-30 and patched 2026-10-02.")


def test_a_rise_to_emerging_is_seen_without_sentence_matching():
    src = "We hypothesize the cache helps in the lab setting overall today."
    assert "band-count" in _kinds(src, "Caching may help.")


def test_adding_a_hedge_to_a_bare_sentence_is_not_a_rise():
    kinds = _kinds("The cache helps in the lab.", "The cache may help in the lab.")
    assert "tier-up" not in kinds and "band-count" not in kinds


def test_may_the_month_is_not_a_hedge():
    assert [k for k in _kinds("It shipped in May.", "It shipped last spring.") if k.startswith("tier")] == []


def test_flags_are_not_hidden_by_the_examined_nothing_note():
    rep = pc.check("The review found problems.", "The review demonstrates that all files always fail.", BANDS)
    md = pc.to_markdown(rep)
    assert rep.examined_nothing and rep.flags
    assert md.index("item(s) to check") < md.index("examined nothing")


def test_cli_exits_2_on_an_unreadable_source(tmp_path):
    t = tmp_path / "t.md"
    t.write_text("x")
    assert pc.main([str(tmp_path / "missing.md"), str(t)]) == 2


def test_the_guide_table_reads_only_the_language_column(tmp_path):
    text = pc.DEFAULT_GUIDE.read_text().replace(
        '| ESTABLISHED | "demonstrates", "shows", "confirms", "established" |',
        '| ESTABLISHED | "demonstrates", "shows", "confirms", "established" | "note" |',
    )
    g = tmp_path / "guide.md"
    g.write_text(text)
    assert "note" not in pc.read_bands(g)["ESTABLISHED"]


def test_the_guide_section_may_be_the_last_one(tmp_path):
    g = tmp_path / "guide.md"
    body = pc.DEFAULT_GUIDE.read_text()
    section = body[body.index("## Language Calibration") :]
    section = section[: section.index("\n#", 5)]
    g.write_text("# Guide\n\n" + section.rstrip() + "\n")
    assert list(pc.read_bands(g)) == list(pc.TIER_ORDER)


def test_dates_and_digits_inside_paths_are_identifiers():
    # From the 2026-09-30 pilot: a plain-text source link read as a new date.
    src = "The review found 2 warnings."
    trn = "The review found 2 warnings.\n\nSource: docs/work-items/reports/2026-09-30-review-memory-lens.md"
    assert _kinds(src, trn) == []
    assert _kinds("See 2026-09-30-notes.md.", "See the notes.") == []


# --- round-2 findings: every site of each class, enumerated -------------------


@pytest.mark.parametrize(
    "opener",
    [
        "No doubt it",
        "Without doubt this",
        "No question it",
        "Not only it",
        "Not just it",
        "It cannot deny it",
        "It never fails to",
    ],
)
def test_idioms_that_open_with_a_negation_word_still_assert(opener):
    assert "band-count" in _kinds("The fix may help.", f"{opener} demonstrates the fix helps.")


def test_a_real_negation_still_suppresses():
    assert "band-count" not in _kinds("The fix may help.", "It does not demonstrate that the fix helps; it may.")


@pytest.mark.parametrize("marker", ["- ", "* ", "1. ", "> ", "**", "| x | "])
def test_may_after_line_markup_is_the_hedge(marker):
    assert "tier-missing" in _kinds(f"{marker}May be slow.", f"{marker}Is slow.")


@pytest.mark.parametrize(
    ("src", "trn"),
    [("Latency was 5ms.", "Latency was 5 ms."), ("It is 5 kg.", "It is 5kg."), ("It took 10mins.", "It took 10 mins.")],
)
def test_a_multi_letter_unit_may_follow_a_space(src, trn):
    assert _kinds(src, trn) == []


def test_a_changed_rate_is_not_hidden_as_a_path():
    assert "number-new" in _kinds("Throughput 12GB/s.", "Throughput 16GB/s.")


def test_an_ordinal_survives_as_a_word_but_a_leading_first_is_not_new():
    assert _kinds("The 1st run failed.", "The first run failed.") == []
    assert "number-new" not in _kinds("The run failed.", "First, the run failed.")
