"""Paper 1's live registry on the DR-027 schema (migrated 2026-10-16).

Pins the P0 floor and the registry/manuscript consistency, so a change to the
registry or the draft that breaks either shows up here. The only findings
expected are premises resting on rows written in the migration session and not
yet checked by a later one; when those rows are verified, update this list.
"""

from __future__ import annotations

from tools.check_registry import check_registry
from tools.coverage import check_coverage

from .conftest import REPO_ROOT

MANUSCRIPT = REPO_ROOT / "papers" / "perspective" / "manuscript.tex"
GLOSSARY = REPO_ROOT / "papers" / "perspective" / "glossary.md"


def test_paper1_v5_p0_floor(paper1_v5_registry):
    report = check_coverage(paper1_v5_registry)
    assert set(report.p0_ids) == {"S1-1", "S1-2", "S2-1", "S2-2", "S3-4", "C1"}
    assert set(report.p0_below_floor) == {"C1", "S2-2", "S3-4"}
    assert not report.deprecations


def test_paper1_v5_consistency(paper1_v5_registry):
    report = check_registry(paper1_v5_registry, manuscript_path=MANUSCRIPT, budget=4000, glossary_path=GLOSSARY)
    by_check = {}
    for f in report.findings:
        if f.check == "budget" and f.severity == "note":  # near the word budget: a heads-up; over budget is a finding
            continue
        by_check.setdefault(f.check, []).append(f.message)
    assert set(by_check) == {"premises"}, by_check
    assert len(by_check["premises"]) == 23  # rows awaiting the blind re-rating (2026-11-04: C1 also rests on S4-9; 2026-10-19: S1-7 rests on S1-8 and S1-9, new, and on S1-1 and S1-2, reworded; draft 4, 2026-10-30: S3-4 rests on S1-9)
    assert all("which is not verified" in m for m in by_check["premises"])



# The paper states register counts in prose ("this paper's has 39 entries", "the six P0
# entries", "three reach the Supported tier"); after a cut or a new row they went stale
# unnoticed (37 vs 39, 2026-11-10). Each stated count must equal the parser's.
# Convention: "entries" are all register rows (claims S*, declarations D*, contribution C1),
# counted as distinct IDs; P0 counts come from coverage's P0 floor (Emerging = below it);
# C1's grounds are its claim premises and its declarations by kind.
# Read: the manuscript and the abstract (arXiv build). Only digits and the number words
# below match; a shape that stops matching altogether fails the shape guard. A count in a shape not listed
# here is not seen: extend COUNT_SHAPES when the prose gains one.
PAPER_TEXTS = (MANUSCRIPT, MANUSCRIPT.with_name("abstract.tex"))
_NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
_N = r"(\d+|" + "|".join(_NUMBER_WORDS) + r")\b"  # a number only: "all P0 entries" is no count
COUNT_SHAPES = {
    "entries": (rf"this paper's has {_N} entries",),
    "p0": (rf"{_N} P0 entries", rf"of its {_N} central claims"),
    "p0_supported": (rf"P0 entries, {_N} reach the Supported tier",),
    "p0_emerging": (rf"leaves {_N} of its \w+ central claims at the Emerging tier",),
    # Table 2's grounds cell for C1: "five claims, three declared values, three declared definitions"
    "c1_claims": (rf"{_N} claims, \w+ declared values",),
    "c1_values": (rf"claims, {_N} declared values",),
    "c1_definitions": (rf"declared values, {_N} declared definitions",),
}


def _stated_counts(text: str) -> dict[str, list[int]]:
    import re

    text = re.sub(r"(?m)(?<!\\)%.*$", "", text)  # LaTeX comments are not prose
    text = text.replace("~", " ").replace("\u2019", "'")
    text = re.sub(r"\s+", " ", text)
    out: dict[str, list[int]] = {}
    for key, pats in COUNT_SHAPES.items():
        for pat in pats:
            for m in re.finditer(pat, text, flags=re.I):
                w = m.group(1).lower()
                n = int(w) if w.isdigit() else _NUMBER_WORDS.get(w)
                assert n is not None, f"unreadable count {m.group(0)!r}: add the word or reword"
                out.setdefault(key, []).append(n)
    return out


def _stale(stated: dict[str, list[int]], actual: dict[str, int]) -> list[str]:
    return [f"{k}: prose says {n}, register has {actual[k]}"
            for k, ns in stated.items() for n in ns if n != actual[k]]


def test_paper1_stated_register_counts(paper1_v5_registry):
    cov = check_coverage(paper1_v5_registry)
    p0, below = set(cov.p0_ids), set(cov.p0_below_floor)
    entries = {e.entry_id: e for e in check_registry(paper1_v5_registry).entries}
    c1 = entries["C1"]
    kinds = [entries[d].columns.get("kind") for d in c1.decls]
    actual = {
        "entries": len(entries),
        "c1_claims": len(c1.premises),
        "c1_values": kinds.count("value"),
        "c1_definitions": kinds.count("definition"),
        "p0": len(p0),
        "p0_supported": len(p0 - below),
        "p0_emerging": len(below),
    }
    stated: dict[str, list[int]] = {}
    for path in PAPER_TEXTS:
        for k, ns in _stated_counts(path.read_text(encoding="utf-8")).items():
            stated.setdefault(k, []).extend(ns)
    assert set(stated) == set(COUNT_SHAPES), f"a count shape no longer matches the prose: {stated}"
    assert not _stale(stated, actual)


def test_stated_count_check_catches_a_stale_number():
    # Seeded positive: the 2026-11-10 defect (37 stated, 39 in the register).
    stated = _stated_counts("The register asks work of authors; this paper\u2019s has~37\nentries. % 39 entries\n"
                            "Of the six P0 entries, three reach the Supported tier.")
    assert stated == {"entries": [37], "p0": [6], "p0_supported": [3]}
    assert _stale(stated, {"entries": 39, "p0": 6, "p0_supported": 3}) == ["entries: prose says 37, register has 39"]


def test_stated_count_check_ignores_non_numbers():
    # Outside the number table: not matched at all, so the shape guard in the live test
    # fails if this is the only occurrence; "all P0 entries" is not a count and is ignored.
    assert _stated_counts("this paper's has forty entries. all P0 entries") == {}
