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
    assert len(by_check["premises"]) == 22  # rows awaiting the blind re-rating (2026-10-19: S1-7 rests on S1-8 and S1-9, new, and on S1-1 and S1-2, reworded; draft 4, 2026-10-30: S3-4 rests on S1-9)
    assert all("which is not verified" in m for m in by_check["premises"])
