"""Tests for scripts/read-surface.sh (repo maintenance, not an adopter tool).

Exits: 0 at or under budget, 1 over, 2 cannot verify. Each tree is seeded in
tmp_path, so the counts are known and the real memory/ is never read.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "read-surface.sh"
BASH = shutil.which("bash") or "bash"  # absolute, so a stripped PATH still finds it


def _run(root: Path, budget: str | None = None, **extra: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, **extra)
    env.pop("READ_SURFACE_BUDGET", None)
    if budget is not None:
        env["READ_SURFACE_BUDGET"] = budget
    return subprocess.run([BASH, str(SCRIPT), str(root)], capture_output=True, text=True, env=env, timeout=30)


def _seed(root: Path, files: dict[str, str]) -> Path:
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body.encode("utf-8"))
    return root


def test_counts_characters_not_bytes_and_keeps_crlf(tmp_path):
    _seed(tmp_path, {"memory/a.md": "é\r\n", "docs/work-items/b.md": "xyz"})
    r = _run(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "6 characters in 2 files" in r.stdout


def test_archive_and_non_markdown_are_excluded(tmp_path):
    _seed(
        tmp_path,
        {
            "memory/a.md": "ab",
            "memory/archive/old.md": "x" * 500,
            "docs/work-items/archive/reports/r.md": "x" * 500,
            "memory/notes.txt": "x" * 500,
            "docs/other.md": "x" * 500,
        },
    )
    assert "2 characters in 1 files" in _run(tmp_path).stdout


def test_files_over_10k_are_listed_largest_first(tmp_path):
    _seed(tmp_path, {"memory/big.md": "x" * 10001, "memory/bigger.md": "x" * 12000, "memory/small.md": "x" * 10000})
    out = _run(tmp_path, "1000000").stdout
    assert "small.md" not in out
    assert out.index("bigger.md") < out.index("big.md")


@pytest.mark.parametrize(("budget", "code"), [("100", 0), ("99", 1)])
def test_budget_boundary(tmp_path, budget, code):
    _seed(tmp_path, {"memory/a.md": "x" * 100})
    r = _run(tmp_path, budget)
    assert r.returncode == code
    assert ("OVER BUDGET by 1" in r.stdout) == (code == 1)


@pytest.mark.parametrize(("n", "code"), [(100000, 0), (100001, 1)])
def test_default_budget_is_100k(tmp_path, n, code):
    _seed(tmp_path, {"memory/a.md": "x" * n})
    assert _run(tmp_path).returncode == code


def test_nested_archive_is_excluded_and_either_root_suffices(tmp_path):
    _seed(tmp_path, {"docs/work-items/a.md": "ab", "docs/work-items/x/archive/old.md": "x" * 500})
    r = _run(tmp_path)
    assert r.returncode == 0 and "2 characters in 1 files" in r.stdout


def test_symlinks_are_skipped_as_find_type_f_does(tmp_path):
    _seed(tmp_path, {"memory/a.md": "ab", "elsewhere/big.md": "x" * 500})
    (tmp_path / "memory" / "link.md").symlink_to(tmp_path / "elsewhere" / "big.md")
    assert "2 characters in 1 files" in _run(tmp_path).stdout


@pytest.mark.parametrize("budget", ["1e5", "100,000", "-1"])
def test_bad_budget_cannot_verify(tmp_path, budget):
    _seed(tmp_path, {"memory/a.md": "x"})
    assert _run(tmp_path, budget).returncode == 2


def test_no_surface_cannot_verify(tmp_path):
    r = _run(tmp_path)
    assert r.returncode == 2 and "CANNOT VERIFY" in r.stderr


def test_empty_surface_cannot_verify(tmp_path):
    _seed(tmp_path, {"memory/archive/old.md": "x", "docs/work-items/notes.txt": "x"})
    r = _run(tmp_path)
    assert r.returncode == 2 and "nothing was measured" in r.stderr


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 directory")
def test_unreadable_directory_cannot_verify(tmp_path):
    _seed(tmp_path, {"memory/a.md": "ab", "memory/sub/b.md": "x" * 50})
    sub = tmp_path / "memory" / "sub"
    sub.chmod(0)
    try:
        r = _run(tmp_path)
        assert r.returncode == 2 and "Permission denied" in r.stderr
    finally:
        sub.chmod(0o755)


def test_undecodable_filename_is_listed_not_a_crash(tmp_path):
    # It crashed print() with exit 1, read as "over budget"; a crash now exits 2.
    _seed(tmp_path, {"memory/a.md": "ab"})
    (tmp_path / "memory" / os.fsdecode(b"\xff.md")).write_text("x" * 10001)
    r = _run(tmp_path)
    assert r.returncode == 0 and "10,001" in r.stdout, r.stderr


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 file")
def test_unreadable_file_cannot_verify(tmp_path):
    _seed(tmp_path, {"memory/a.md": "ab"})
    f = tmp_path / "memory" / "a.md"
    f.chmod(0)
    try:
        r = _run(tmp_path)
        assert r.returncode == 2 and "Permission denied" in r.stderr and "crash:" not in r.stderr
    finally:
        f.chmod(0o644)


def test_non_utf8_file_cannot_verify(tmp_path):
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "a.md").write_bytes(b"\xff\xfe")
    r = _run(tmp_path)
    assert r.returncode == 2 and "decode" in r.stderr and "crash:" not in r.stderr


def test_symlinked_top_level_dir_is_not_descended(tmp_path):
    _seed(tmp_path, {"real/a.md": "x" * 500, "docs/work-items/c.md": "c"})
    (tmp_path / "memory").symlink_to(tmp_path / "real")
    assert "1 characters in 1 files" in _run(tmp_path).stdout


def test_fifo_is_skipped_not_opened(tmp_path):
    _seed(tmp_path, {"memory/a.md": "ab"})
    os.mkfifo(tmp_path / "memory" / "p.md")
    assert "2 characters in 1 files" in _run(tmp_path).stdout


def test_crash_is_cannot_verify_not_over_budget(tmp_path):
    _seed(tmp_path, {"memory/\u00e9.md": "x" * 10001})
    r = _run(tmp_path, PYTHONIOENCODING="ascii")
    assert r.returncode == 2 and "crash:" in r.stderr


def test_missing_python_cannot_verify(tmp_path):
    _seed(tmp_path, {"memory/a.md": "ab"})
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    (bin_ / "dirname").symlink_to(shutil.which("dirname"))
    r = _run(tmp_path, PATH=str(bin_))
    assert r.returncode == 2
