"""Tests for scripts/check-counts.sh (repo maintenance, not an adopter tool).

Each case is a shape seeded by hand in the 2026-10-01 review, with the exit it
must give: 0 every claim matches, 1 a claim is stale, 2 cannot verify. Stale
and near-miss shapes sit beside one valid claim, so a pass cannot come from an
empty section. The script reads claimed paths relative to the repo root.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check-counts.sh"
CLAUDE_LEN = len((REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
VALID = f"- `CLAUDE.md` 34,670 → {CLAUDE_LEN:,} characters."


def _run(tmp_path: Path, body: str, env: dict | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    cl = tmp_path / "CHANGELOG.md"
    cl.write_text(f"# Changelog\n\n## Top\n\n{body}\n\n## v0\n\n- `CLAUDE.md` 1 → 2 characters\n", encoding="utf-8")
    return subprocess.run(["bash", str(SCRIPT), str(cl)], capture_output=True, text=True, env=env, cwd=cwd)


def _collected(module: str) -> int:
    p = subprocess.run(
        [sys.executable, "-m", "pytest", f"tests/{module}", "-q", "--collect-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    n = sum("::" in line for line in p.stdout.splitlines())
    assert p.returncode == 0 and n > 0, p.stdout + p.stderr
    return n


CASES = [
    # matching claims
    (VALID, 0),
    (f"{VALID}\n- The test suite went from 1 to {{total}}.", 0),
    # stale claims
    ("- `CLAUDE.md` 34,670 → 99 characters.", 1),
    (f"{VALID}\n- `CLAUDE.md` 1 → **99** characters", 1),
    (f"{VALID}\n- `CLAUDE.md` 1 → `99` characters", 1),
    (f"{VALID}\n- trimmed, see\n#37: `CLAUDE.md` 1 → 99 characters", 1),
    (f"{VALID}\n<!--\n## x -->\n- `CLAUDE.md` 1 → 99 characters", 1),
    (f"{VALID}\n```\n## not a heading\n```\n- `CLAUDE.md` 1 → 99 characters", 1),
    (f"{VALID}\n- `formula_scan.py` hardened; the suite went from 42 tests at v4.0.0 to 99999.", 1),
    ("- `formula_scan.py`: 99999 tests", 1),
    ("- `tests` 1 → 2 characters", 1),
    # near-miss shapes: unparsed, cannot verify
    (f"{VALID}\n- `CLAUDE.md` 1 -> 99 characters", 2),
    (f"{VALID}\n- `CLAUDE.md` shrank from 34,670 to 99 characters", 2),
    (f"{VALID}\n- `CLAUDE.md` 1 → 11 570 characters", 2),
    (f"{VALID}\n- `CLAUDE.md` 1 → 99 chars", 2),
    (f"{VALID}\n- `CLAUDE.md` is now 11.6k characters", 2),
    (f"{VALID}\n- `formula_scan.py`: 99 unit tests", 2),
    (f"{VALID}\n- `formula_scan.py`: 1 test", 2),
    (f"{VALID}\n- `formula_scan.py`: added 5 tests", 2),
    (f"{VALID}\n- `formula_scan.py`: a further 5 tests", 2),
    ("- `CLAUDE.md` 34,670 → 99 and `vv/hypothesis-log.md` 34,521 → {vv} characters", 2),
    # nothing to check: never success over nothing
    ("- Nothing here.", 2),
    ("- Ran lint, tests and coverage on `tools/coverage.py`.", 2),
    ("- Paper 1 floor: 1 of 8 → 3 of 6.", 2),
    ("- `tools/coverage.py` now has ~3 tests.", 2),
    # prose that must not be read as a claim
    (f"{VALID}\n- DR-021 tests the claim in `formula_scan.py`.", 0),
    (f"{VALID}\n- The two Paper 1 fixture tests pass.", 0),
    (f"{VALID}\n- `coverage.py` fixes; the suite went from 20 tests at v3.0.0 to {{total}}.", 0),
]


@pytest.mark.parametrize(("body", "want"), CASES, ids=[f"case{n:02d}" for n in range(len(CASES))])
def test_shape_gives_expected_exit(tmp_path, body, want):
    raw = body
    if "{total}" in body:
        body = body.replace("{total}", str(_collected("")))
    if "{vv}" in body:
        body = body.replace("{vv}", f"{len((REPO_ROOT / 'vv/hypothesis-log.md').read_text(encoding='utf-8')):,}")
    p = _run(tmp_path, body)
    assert p.returncode == want, p.stdout + p.stderr
    if "{total}" in raw:  # the suite claim itself was checked, not only VALID
        assert "ok     test suite" in p.stdout, p.stdout


def test_per_module_count_matches(tmp_path):
    n = _collected("test_formula_scan.py")
    p = _run(tmp_path, f"- `extensions/formula_scan.py` gained a check. {n} tests, seeded.")
    assert p.returncode == 0, p.stdout + p.stderr


def test_crlf_counts_as_wc_m(tmp_path):
    f = REPO_ROOT / "docs/work-items/zz_check_counts_crlf.txt"
    f.parent.mkdir(exist_ok=True)  # gitignored, created on demand
    f.write_bytes(b"a\r\nb\r\n")
    try:
        p = _run(tmp_path, "- `docs/work-items/zz_check_counts_crlf.txt` 1 → 6 characters")
    finally:
        f.unlink()
    assert p.returncode == 0, p.stdout + p.stderr


def test_non_utf8_claimed_file_cannot_verify(tmp_path):
    f = REPO_ROOT / "docs/work-items/zz_check_counts_bin.txt"
    f.parent.mkdir(exist_ok=True)  # gitignored, created on demand
    f.write_bytes(b"\xff\xfe")
    try:
        p = _run(tmp_path, "- `docs/work-items/zz_check_counts_bin.txt` 1 → 2 characters")
    finally:
        f.unlink()
    assert p.returncode == 2 and "UnicodeDecodeError" in p.stderr


def test_unreadable_changelog_cannot_verify(tmp_path):
    p = subprocess.run(["bash", str(SCRIPT), str(tmp_path / "missing.md")], capture_output=True, text=True)
    assert p.returncode == 2


def test_root_found_from_any_cwd_and_cdpath(tmp_path):
    env = {**os.environ, "CDPATH": "."}
    p = _run(tmp_path, VALID, env=env, cwd=REPO_ROOT / "tests")
    assert p.returncode == 0, p.stdout + p.stderr
