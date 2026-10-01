"""Tests for scripts/check-profile.sh (repo maintenance, not an adopter tool).

Exits: 0 all invariants hold, 1 a finding, 2 cannot verify. Each case seeds a
minimal git repo in tmp_path and mutates one thing from a clean baseline. The
cases were written against the guards a 2026-10-01 review found unpinned; the
bash exit clamp (> 2 becomes 2) has no case.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-profile.sh"
BASH = shutil.which("bash") or "bash"

PROFILE = """# Review Profile

## Risk tiers

| Tier | File patterns | Depth |
|------|-------------|-------|
| **HIGH** | `tools/**`, `/CLAUDE.md`, `papers/*/references.bib`, `memory/**`, `Makefile`, `scripts/**` | Full |
| **MEDIUM** | `docs/**` | Two |
| **LOW** | `CHANGELOG.md` | One |

## Ignored paths

| Pattern | Want reviewed? |
|---------|----------------|
| `memory/**` | yes |

## Guarantee surfaces

- `tools/a.py`: a guarantee
- `CLAUDE.md`: stamps
- `papers/*/references.bib`: entries resolve
- `memory/**`: kept local
- `Makefile`: targets `test`, `drift`
- `scripts/**`: `drift.sh` exits 0 / 1 / 2
"""

MAKEFILE = ".PHONY: test drift\n\ntest:  ## t\n\tpytest\n\ndrift:  ## d\n\tbash scripts/drift.sh\n"


def _seed(root: Path, profile: str = PROFILE, makefile: str | None = MAKEFILE, gitignore: str = "memory/\n") -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(gitignore)
    (root / ".claude").mkdir()
    (root / ".claude" / "review-profile.md").write_text(profile)
    if makefile is not None:
        (root / "Makefile").write_text(makefile)
    (root / "scripts").mkdir()
    (root / "scripts" / "drift.sh").write_text("")
    return root


def _run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([BASH, str(SCRIPT), str(root)], capture_output=True, text=True, timeout=30)


def test_clean_baseline_passes(tmp_path):
    r = _run(_seed(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "6 HIGH patterns, 6 guarantees, 1 ignored patterns, 2 targets, 1 scripts" in r.stdout


def test_guarantee_outside_high_is_a_finding(tmp_path):
    r = _run(_seed(tmp_path, PROFILE + "- `docs/guide.md`: MEDIUM only\n"))
    assert r.returncode == 1
    assert "guarantee `docs/guide.md` is tiered MEDIUM, not HIGH" in r.stdout


def test_high_pattern_without_guarantee_is_a_finding(tmp_path):
    r = _run(_seed(tmp_path, PROFILE.replace("- `tools/a.py`: a guarantee\n", "")))
    assert r.returncode == 1
    assert "HIGH pattern `tools/**` has no guarantee" in r.stdout


def test_single_star_does_not_cross_directories(tmp_path):
    prof = PROFILE.replace("`papers/*/references.bib`: entries", "`papers/a/b/references.bib`: entries")
    r = _run(_seed(tmp_path, prof))
    assert r.returncode == 1
    assert "guarantee `papers/a/b/references.bib` is tiered nowhere, not HIGH" in r.stdout


def test_ignored_pattern_missing_from_table_is_a_finding(tmp_path):
    r = _run(_seed(tmp_path, gitignore="memory/\ndocs/\n"))
    assert r.returncode == 1
    assert "MEDIUM pattern `docs/**` is gitignored and not in the Ignored paths table" in r.stdout


def test_ignored_pattern_listed_in_table_is_not_a_finding(tmp_path):
    prof = PROFILE.replace("| `memory/**` | yes |", "| `memory/**` | yes |\n| `docs/` | no |")
    assert _run(_seed(tmp_path, prof, gitignore="memory/\ndocs/\n")).returncode == 0


def test_unnamed_target_is_a_finding(tmp_path):
    r = _run(_seed(tmp_path, makefile=MAKEFILE + "\nlint:  ## l\n\truff\n"))
    assert r.returncode == 1
    assert "Makefile target `lint` is not named" in r.stdout


def test_unnamed_script_is_a_finding(tmp_path):
    root = _seed(tmp_path)
    (root / "scripts" / "new.sh").write_text("")
    r = _run(root)
    assert r.returncode == 1
    assert "scripts/new.sh is not named" in r.stdout


def _high(extra: str) -> str:
    return PROFILE.replace("`scripts/**` | Full", "`scripts/**`, " + extra + " | Full")


@pytest.mark.parametrize(
    ("profile", "finding"),
    [
        # most specific pattern wins: a LOW sub-tree under HIGH tools/** takes the guarantee out of HIGH
        (
            PROFILE.replace("`CHANGELOG.md` | One", "`CHANGELOG.md`, `tools/fixtures/**` | One")
            + "- `tools/fixtures/g.json`: golden\n",
            "guarantee `tools/fixtures/g.json` is tiered LOW",
        ),
        # a guarantee glob broader than its HIGH pattern
        (
            PROFILE.replace("`papers/*/references.bib`: entries", "`papers/**/references.bib`: entries"),
            "is tiered nowhere",
        ),
        # indented and `*` bullets are read
        (PROFILE + "  - `docs/a.md`: indented\n", "guarantee `docs/a.md` is tiered MEDIUM"),
        (PROFILE + "* `docs/b.md`: star\n", "guarantee `docs/b.md` is tiered MEDIUM"),
    ],
    ids=["most-specific-wins", "broader-glob", "indented-bullet", "star-bullet"],
)
def test_guarantee_tier_findings(tmp_path, profile, finding):
    r = _run(_seed(tmp_path, profile))
    assert r.returncode == 1, r.stdout + r.stderr
    assert finding in r.stdout


def test_double_star_crosses_directories(tmp_path):
    prof = PROFILE.replace("`tools/a.py`: a guarantee", "`tools/x/y/a.py`: a guarantee")
    assert _run(_seed(tmp_path, prof)).returncode == 0


def test_bare_directory_pattern_is_asked_as_a_directory(tmp_path):
    r = _run(
        _seed(
            tmp_path,
            PROFILE.replace("`CHANGELOG.md` | One", "`CHANGELOG.md`, `audits` | One"),
            gitignore="memory/\naudits/\n",
        )
    )
    assert r.returncode == 1
    assert "LOW pattern `audits` is gitignored" in r.stdout


def test_ignored_pattern_decided_under_its_base_key(tmp_path):
    prof = PROFILE.replace("`memory/**`, `Makefile`", "`memory/**`, `memory/*.md`, `Makefile`")
    assert _run(_seed(tmp_path, prof + "- `memory/x.md`: one\n")).returncode == 0


def test_leading_glob_pattern_is_reported_unchecked(tmp_path):
    r = _run(_seed(tmp_path, PROFILE.replace("`docs/**` | Two", "`docs/**`, `**/*.tmp` | Two")))
    assert r.returncode == 0
    assert "UNCHECKED: `**/*.tmp`" in r.stdout


def test_script_named_only_as_a_substring_is_a_finding(tmp_path):
    root = _seed(tmp_path)
    (root / "scripts" / "ift.sh").write_text("")  # a substring of `drift.sh`
    r = _run(root)
    assert r.returncode == 1
    assert "scripts/ift.sh is not named" in r.stdout


def test_dotfiles_in_scripts_are_skipped(tmp_path):
    root = _seed(tmp_path)
    (root / "scripts" / ".gitkeep").write_text("")
    assert _run(root).returncode == 0


@pytest.mark.parametrize(
    ("makefile", "code", "message"),
    [
        (MAKEFILE + "\nPY:=python\n", 0, ""),
        (MAKEFILE + "\nCC ::= gcc\n", 0, ""),
        (MAKEFILE + "\ndefine BODY\ninner: thing\nendef\n", 0, ""),
        (MAKEFILE + "\nmanuscript.pdf:  ## dotted\n\tlatex\n", 1, "Makefile target `manuscript.pdf` is not named"),
        (MAKEFILE + "\nlint fmt:  ## two\n\truff\n", 1, "Makefile target `fmt` is not named"),
    ],
    ids=["assignment-is-not-a-target", "double-colon-assignment", "define-body", "dotted-target", "multi-target-line"],
)
def test_target_parsing(tmp_path, makefile, code, message):
    r = _run(_seed(tmp_path, makefile=makefile))
    assert r.returncode == code, r.stdout + r.stderr
    assert message in r.stdout


def test_section_heading_inside_a_fence_does_not_cut_the_section(tmp_path):
    prof = (
        PROFILE.replace("- `tools/a.py`: a guarantee\n", "- `tools/a.py`: a guarantee\n```\n## not a heading\n```\n")
        + "- `docs/c.md`: late\n"
    )
    r = _run(_seed(tmp_path, prof))
    assert r.returncode == 1
    assert "guarantee `docs/c.md` is tiered MEDIUM" in r.stdout


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda r: (r / ".claude" / "review-profile.md").unlink(), "review-profile.md"),
        (lambda r: (r / "Makefile").unlink(), "Makefile"),
        (lambda r: (r / "Makefile").write_text("# no targets\n"), "no targets"),
        (lambda r: shutil.rmtree(r / "scripts"), "no scripts/ directory"),
        (lambda r: (r / ".claude" / "review-profile.md").write_bytes(b"\xff\xfe"), "review-profile.md"),
        (
            lambda r: (r / ".claude" / "review-profile.md").write_text(
                PROFILE.replace("`docs/**` | Two", "`docs/**`, `../out/x` | Two")
            ),
            "git check-ignore failed",
        ),
        (lambda r: shutil.rmtree(r / ".git"), "not a git work tree"),
        (
            lambda r: (r / ".claude" / "review-profile.md").write_text(PROFILE + "```\nunclosed\n"),
            "unclosed code fence",
        ),
        (
            lambda r: (r / ".claude" / "review-profile.md").write_text(PROFILE.replace("| **HIGH** |", "| HIGH |")),
            "no HIGH row",
        ),
        (
            lambda r: (r / ".claude" / "review-profile.md").write_text(PROFILE.split("## Guarantee")[0]),
            "no '## Guarantee surfaces' section",
        ),
        (
            lambda r: (r / ".claude" / "review-profile.md").write_text(PROFILE.split("- `tools/a.py`")[0]),
            "lists no",
        ),
    ],
    ids=[
        "no-profile",
        "no-makefile",
        "no-targets",
        "no-scripts-dir",
        "non-utf8-profile",
        "check-ignore-fails",
        "no-git",
        "unclosed-fence",
        "no-high-row",
        "no-guarantee-section",
        "empty-guarantees",
    ],
)
def test_cannot_verify_exits_2(tmp_path, mutate, message):
    root = _seed(tmp_path)
    mutate(root)
    r = _run(root)
    assert r.returncode == 2, r.stdout + r.stderr
    assert message in r.stderr
