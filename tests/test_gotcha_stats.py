"""Tests for scripts/gotcha-stats.sh (repo maintenance, not an adopter tool).

Exits: 0 counted, 1 no entries and no `## Promoted` anchor, 2 unreadable log.
Each log is seeded in tmp_path; the real memory/ is never read.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gotcha-stats.sh"
BASH = shutil.which("bash") or "bash"


def _run(tmp_path: Path, body: str) -> subprocess.CompletedProcess:
    f = tmp_path / "gotcha-log.md"
    f.write_text(body, encoding="utf-8")
    return subprocess.run([BASH, str(SCRIPT), str(f)], capture_output=True, text=True, timeout=30)


def test_counts_entries_and_missing_problem_lines(tmp_path):
    r = _run(tmp_path, "# Gotcha Log\n\n### A (2026-11-11)\n**Problem**: x\n\n### B\nno problem line\n\n## Promoted\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("2 entries") and "1 without a **Problem** line" in r.stdout


def test_zero_entries_with_promoted_heading_is_clean(tmp_path):
    r = _run(tmp_path, "# Gotcha Log\n\n## Lessons kept\n\n- one line\n\n## Promoted\n\n| a |\n\n## Mechanized\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("0 entries")


def test_zero_entries_without_anchor_fails(tmp_path):
    # Seeded positive: entries written as `#### ` (a shape change) must not read as a clean log.
    r = _run(tmp_path, "# Gotcha Log\n\n#### A\n**Problem**: x\n")
    assert r.returncode == 1
    assert "NO ENTRIES" in r.stderr


def test_promoted_inside_code_fence_is_not_an_anchor(tmp_path):
    r = _run(tmp_path, "# Gotcha Log\n\n```\n## Promoted\n```\n")
    assert r.returncode == 1


def test_unreadable_log_exits_2(tmp_path):
    r = subprocess.run([BASH, str(SCRIPT), str(tmp_path / "missing.md")], capture_output=True, text=True, timeout=30)
    assert r.returncode == 2


def test_zero_entries_with_anchor_but_deeper_headings_fails(tmp_path):
    # Seeded positive (review 2026-11-11): the live log always has `## Promoted`, so a
    # shape change there must still fail, not read as a clean log.
    r = _run(tmp_path, "# Gotcha Log\n\n#### A new-shape entry\n**Problem**: x\n\n## Promoted\n")
    assert r.returncode == 1
    assert "NO ENTRIES" in r.stderr


def test_zero_entries_with_anchor_but_bold_titled_entry_fails(tmp_path):
    r = _run(tmp_path, "# Gotcha Log\n\n**A bold-titled entry**\n**Problem**: x\n\n## Promoted\n")
    assert r.returncode == 1


def test_promoted_inside_html_comment_is_not_an_anchor(tmp_path):
    r = _run(tmp_path, "# Gotcha Log\n\n<!--\n## Promoted\n-->\n")
    assert r.returncode == 1


def test_heading_and_problem_inside_html_comment_are_not_content(tmp_path):
    body = "# Gotcha Log\n\n<!-- Format:\n### Title (date)\n**Problem**: what broke\n-->\n\n## Promoted\n"
    r = _run(tmp_path, body)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("0 entries")


def test_zero_entries_with_anchor_but_level2_dated_entries_fails(tmp_path):
    # Seeded positive (review round 2): a real log format, `## [date]` entries with `**Problem.**`.
    r = _run(tmp_path, "# Gotcha Log\n\n## Promoted\n\n## [2026-08-16] Bug\n**Problem.** x\n")
    assert r.returncode == 1


def test_problem_variants_count_as_stray(tmp_path):
    for p in ("**Problem:** x", "**problem** x", "**Problem.** x"):
        r = _run(tmp_path, f"# Gotcha Log\n\n{p}\n\n## Promoted\n")
        assert r.returncode == 1, p


def test_fence_inside_comment_does_not_swallow_entries(tmp_path):
    # Seeded positive (review round 2): a comment closed on a fence line hid a real entry.
    body = "# Log\n## Promoted\n<!-- example:\n```bash\ncmd\n``` -->\n\n### Real entry (2026-11-01)\n**Problem**: x\n"
    r = _run(tmp_path, body)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("1 entries")


def test_known_sections_and_inline_comment_on_anchor_are_clean(tmp_path):
    body = "# Gotcha Log\n\n## Lessons kept from retired entries\n\n- x\n\n## Promoted <!-- note -->\n\n## Mechanized\n"
    r = _run(tmp_path, body)
    assert r.returncode == 0, r.stderr
