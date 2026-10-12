"""Tests for tools/check_experiments.py (DR-024).

Every guard is exercised with a planted defect it must fail on, and the
committed registry must pass. DR-024's Acceptance Condition 1 names the seeded
positives: a gitignored artifact, a metric 4 whose only occurrence is a date,
and each accidental match in rule 4 (#41, DR-041, +0.350). Each runs in a
throwaway git repo, never against the tracked registry.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("check_experiments", ROOT / "tools" / "check_experiments.py")
ce = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ce)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


@pytest.fixture
def repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.org")
    _git(tmp_path, "config", "user.name", "t")
    ev = tmp_path / "vv" / "evidence" / "2026-10-12-x"
    ev.mkdir(parents=True)
    (ev / "PREREGISTRATION.md").write_text("Confirmed if at least two findings hold up.\n")
    (ev / "result.md").write_text("Method-level findings that held up: 3. Rate 0.35, kappa 0.712.\n")
    (tmp_path / ".gitignore").write_text("private/\n")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "evidence for EXP-001, n = 17")
    return tmp_path


def _entry(**over) -> dict:
    e = {
        "id": "EXP-001",
        "date": "2026-10-12",
        "title": "t",
        "hypothesis": "h",
        "subject": "s",
        "judge": None,
        "branch": "master",
        "commits": [],
        "spend_usd": 0,
        "cost_ref": None,
        "population": {},
        "metrics": {"held_up": 3},
        "decision": "kept",
        "decision_rationale": "r",
        "artifacts": ["vv/evidence/2026-10-12-x"],
        "references": [],
        "review": None,
    }
    e.update(over)
    return e


def _run(repo: Path, *entries: dict) -> tuple[int, str]:
    reg = repo / "planted.jsonl"
    reg.write_text("".join(json.dumps(e) + "\n" for e in entries))
    fails, _ = ce.check(reg, repo)
    return len(fails), "\n".join(fails)


# --- the committed registry ---------------------------------------------------


def test_the_committed_registry_passes(capsys):
    assert ce.main([]) == 0, capsys.readouterr().out


def test_a_clean_entry_passes(repo):
    assert _run(repo, _entry()) == (0, "")


# --- DR-024 Acceptance Condition 1: the seeded positives ---------------------


def test_a_gitignored_artifact_FAILS_although_it_exists_on_disk(repo):
    (repo / "vv" / "evidence" / "private").mkdir()
    (repo / "vv" / "evidence" / "private" / "notes.md").write_text("held up: 3\n")
    n, out = _run(repo, _entry(artifacts=["vv/evidence/private/notes.md"]))
    assert n and "exists on disk but is not tracked by git" in out


def test_an_untracked_file_inside_a_tracked_folder_is_not_searched(repo):
    (repo / "vv" / "evidence" / "2026-10-12-x" / "draft.md").write_text("figure 99\n")
    n, out = _run(repo, _entry(metrics={"figure": 99}))
    assert n and "NOT traceable" in out


def _evidence(repo: Path, text: str, name: str = "result.md") -> None:
    (repo / "vv" / "evidence" / "2026-10-12-x" / name).write_text(text + "\n")
    _git(repo, "add", ".")


@pytest.mark.parametrize(
    "text, metric",
    [
        ("Run on 4 October 2026.", 4),
        ("Run on 4th Oct. 2026.", 4),
        ("Run on October 4, 2026.", 4),
        ("See Oct. 4 meeting.", 4),
        ("Met 4-Oct-2026.", 4),
        ("Held 4\u20136 October.", 4),
        ("Run on 2026-10-04.", 4),
        ("Run on 2026-10-04.", 2026),
        ("At 2026-10-04T09:00Z.", 9),
        ("Since October 2026.", 2026),
        ("At 12:30 sharp.", 30),
        ("See #41 for the guard.", 41),
        ("Follows DR-041.", 41),
        ("Score moved +0.350 overall.", 0.35),
        ("Score moved +0.35 overall.", 0.35),
        ("Score was 0.350 overall.", "0.35"),
        ("Value 4.5 seen.", 4),
        ("Rows 34,521 in all.", 521),
        ("Rows 34,521 in all.", 34),
        ("Ratio 1:2 held.", 2),
        ("Grew 10^4 times.", 4),
        ("Share %4 odd.", 4),
        ("Agreement 76/83 rows.", 76),
        ("Paper 1 at v4.2.0.", "4.2"),
        ("Row S2-2 failed.", 2),
        ("Commit 4a1b2c3 holds it.", 4),
        ("Up 12% this run.", 12),
    ],
)
def test_an_accidental_match_FAILS(repo, text, metric):
    _evidence(repo, text)
    n, out = _run(repo, _entry(metrics={"m": metric}))
    assert n and "NOT traceable" in out, f"{metric!r} matched by accident in {text!r}"


@pytest.mark.parametrize(
    "text, metric",
    [
        ("Findings that held up: 3.", 3),
        ("Rate 0.35, then.", 0.35),
        ("Agreement 76/83 rows.", "76/83"),
        ("12% of rows.", "12%"),
        ("Rows: 34,521 in all.", 34521),
        ("(4) cases", 4),
        ("Shift of -0.2 seen.", -0.2),
        ("a,b\nx,923", 923),
        ("acc,0.35,0.40", 0.35),
        ("run1,12,30", 12),
        ("[1,2,3]", 2),
        ('{"f1":0.35}', 0.35),
        ("Rows 34,521 in all.", "34,521"),
        ("Octopus count 4 here.", 4),
    ],
)
def test_a_genuine_occurrence_passes(repo, text, metric):
    _evidence(repo, text)
    assert _run(repo, _entry(metrics={"m": metric})) == (0, "")


# --- what is never evidence --------------------------------------------------


def test_the_checkers_own_saved_output_is_not_evidence(repo):
    _evidence(repo, "  FAIL  EXP-001: metric `m` = 7 is NOT traceable", "check-2026-10-12.txt")
    n, out = _run(repo, _entry(metrics={"m": 7}))
    assert n and "NOT traceable" in out


def test_a_preregistrations_predictions_are_not_evidence(repo):
    _evidence(repo, "Expected 1 to 5.", "PREREGISTRATION.md")
    n, out = _run(repo, _entry(metrics={"m": 5}))
    assert n and "NOT traceable" in out


def test_a_commit_message_is_not_evidence(repo):
    head = _git(repo, "rev-parse", "--short", "HEAD").strip()
    n, out = _run(repo, _entry(commits=[head], metrics={"n": 17}))
    assert n and "NOT traceable" in out


# --- artifacts --------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        "",
        ".",
        "./",
        "*",
        "*.md",
        ":/",
        ":(glob)**",
        "/etc/hosts",
        "vv/../x.md",
        " vv",
        "vv",
        "vv/evidence",
        "vv/experiments/registry.jsonl",
        "decisions",
        "vv/evidence/x\x00",
        "vv/evidence/\ud800",
    ],
)
def test_an_artifact_path_that_is_not_one_place_FAILS(repo, path):
    n, out = _run(repo, _entry(artifacts=[path]))
    assert n and "artifact path" in out, path


def test_a_tracked_symlink_FAILS_and_is_not_read(repo, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside") / "o.md"
    outside.write_text("value 99\n")
    (repo / "vv" / "evidence" / "2026-10-12-x" / "link.md").symlink_to(outside)
    _git(repo, "add", ".")
    n, out = _run(repo, _entry(metrics={"m": 99}))
    assert n and "symlink or missing on disk" in out and "NOT traceable" in out


def test_a_tracked_file_deleted_from_disk_FAILS(repo):
    (repo / "vv" / "evidence" / "2026-10-12-x" / "result.md").unlink()
    n, out = _run(repo, _entry(metrics={"m": None, "k": 0.712}))
    assert n and "missing on disk" in out


def test_a_directly_cited_file_is_read_whatever_its_suffix(repo):
    _evidence(repo, "value 313", "out.log")
    assert _run(repo, _entry(artifacts=["vv/evidence/2026-10-12-x/out.log"], metrics={"m": 313})) == (0, "")


def test_folder_suffixes_ignore_case_and_skip_others(repo):
    _evidence(repo, "value 811", "t.tex")
    _evidence(repo, "value 923", "T.MD")
    _evidence(repo, "value 555", "t.log")
    assert _run(repo, _entry(metrics={"a": 811, "b": 923}))[0] == 0
    assert _run(repo, _entry(metrics={"c": 555}))[0] == 1


# --- the rest of the schema ---------------------------------------------------


def test_an_invented_or_one_digit_off_number_FAILS(repo):
    n, out = _run(repo, _entry(metrics={"kappa": 0.722}))
    assert n and "`kappa` = 0.722 is NOT traceable" in out


@pytest.mark.parametrize("value", [True, "", {"a": 1}, [3], float("nan")])
def test_a_metric_of_the_wrong_kind_FAILS(repo, value):
    n, out = _run(repo, _entry(metrics={"held_up": 3, "m": value}))
    assert n and "must be a number, a non-empty string or null" in out


def test_null_passes_beside_a_real_metric_but_not_alone(repo):
    assert _run(repo, _entry(metrics={"held_up": 3, "lost": None})) == (0, "")
    for metrics in ({}, {"lost": None}):
        n, out = _run(repo, _entry(metrics=metrics))
        assert n and "nothing would be checked" in out


@pytest.mark.parametrize(
    "over, needle",
    [
        ({"decision": "probably-fine"}, "not in"),
        ({"decision": ["kept"]}, "field `decision` has the wrong type"),
        ({"id": "EXP-1"}, "id is not EXP-NNN"),
        ({"date": "12 Oct 2026"}, "not a real ISO date"),
        ({"date": "2026-13-45"}, "not a real ISO date"),
        ({"spend_usd": "0"}, "field `spend_usd` has the wrong type"),
        ({"spend_usd": True}, "field `spend_usd` has the wrong type"),
        ({"spend_usd": -50}, "finite number of zero or more"),
        ({"spend_usd": float("inf")}, "finite number of zero or more"),
        ({"oracle": "x"}, "unknown field `oracle`"),
        ({"commits": ["deadbee"]}, "commit not found"),
        ({"commits": ["HEAD"]}, "is not a hash"),
        ({"commits": [123]}, "must be a list of strings"),
        ({"artifacts": [None]}, "must be a list of strings"),
        ({"references": [{"a": 1}]}, "must be a list of strings"),
        ({"references": "EXP-001"}, "field `references` has the wrong type"),
        ({"references": ["EXP-999"]}, "not in the registry"),
        ({"artifacts": ["vv/evidence/missing"]}, "is not tracked by git"),
    ],
)
def test_a_schema_defect_FAILS_without_a_crash(repo, over, needle):
    n, out = _run(repo, _entry(**over))
    assert n and needle in out


def test_a_missing_field_FAILS(repo):
    e = _entry()
    del e["cost_ref"]
    n, out = _run(repo, e)
    assert n and "missing required field `cost_ref`" in out


def test_a_duplicate_json_key_FAILS(repo):
    reg = repo / "planted.jsonl"
    reg.write_text(json.dumps(_entry()).replace('"held_up": 3', '"held_up": 999, "held_up": 3') + "\n")
    fails, _ = ce.check(reg, repo)
    assert any("duplicate key" in f for f in fails)


def test_an_empty_registry_FAILS(repo):
    reg = repo / "planted.jsonl"
    reg.write_text("\n")
    assert "the registry holds no entries" in ce.check(reg, repo)[0]


def test_order_and_duplicates_are_both_reported(repo):
    a, b = _entry(), _entry(id="EXP-002")
    assert "ascending order" in _run(repo, b, a)[1]
    out = _run(repo, b, a, _entry())[1]
    assert "duplicate ids" in out and "ascending order" in out


# --- preregistrations -------------------------------------------------------


def test_a_preregistration_has_no_results_and_cites_its_tracked_file(repo):
    pre = _entry(decision="preregistered", metrics={"held_up": None})
    assert _run(repo, pre) == (0, "")
    assert "has a metric value" in _run(repo, _entry(decision="preregistered"))[1]
    bare = _entry(decision="preregistered", metrics={}, artifacts=["vv/evidence/2026-10-12-x/result.md"])
    assert "cites no tracked PREREGISTRATION.md" in _run(repo, bare)[1]


def test_a_gitignored_preregistration_does_not_count(repo):
    (repo / ".gitignore").write_text("private/\nPREREGISTRATION.md\n")
    _git(repo, "rm", "-q", "--cached", "vv/evidence/2026-10-12-x/PREREGISTRATION.md")
    n, out = _run(repo, _entry(decision="preregistered", metrics={}))
    assert n and "cites no tracked PREREGISTRATION.md" in out


def test_only_a_later_concluded_entry_closes_a_preregistration(repo):
    reg = repo / "planted.jsonl"
    pre = _entry(id="EXP-002", decision="preregistered", metrics={})
    early = _entry(id="EXP-001", references=["EXP-002"])
    later = _entry(id="EXP-003", references=["EXP-002"])
    another_pre = _entry(id="EXP-003", decision="preregistered", metrics={}, references=["EXP-002"])
    for lines, expected in (
        ([early, pre], ["EXP-002"]),
        ([pre, another_pre], ["EXP-002", "EXP-003"]),
        ([pre, later], []),
    ):
        reg.write_text("".join(json.dumps(x) + "\n" for x in lines))
        assert ce.check(reg, repo)[1]["open"] == expected


# --- exit codes and banner ----------------------------------------------------


def test_exit_codes(repo, tmp_path_factory):
    reg = repo / "planted.jsonl"
    reg.write_text(json.dumps(_entry()) + "\n")
    assert ce.main(["--repo", str(repo), "--registry", str(reg)]) == 0
    reg.write_text(json.dumps(_entry(metrics={"x": 404})) + "\n")
    assert ce.main(["--repo", str(repo), "--registry", str(reg)]) == 1
    assert ce.main(["--repo", str(repo), "--registry", str(repo / "absent.jsonl")]) == 2
    reg.write_bytes(b"\xff\xfe not utf-8\n")
    assert ce.main(["--repo", str(repo), "--registry", str(reg)]) == 2
    bare = tmp_path_factory.mktemp("bare")
    (bare / "r.jsonl").write_text(json.dumps(_entry()) + "\n")
    assert ce.main(["--repo", str(bare), "--registry", str(bare / "r.jsonl")]) == 2


def test_help_names_the_dr(capsys):
    with pytest.raises(SystemExit):
        ce.main(["--help"])
    assert "(DR-024)" in capsys.readouterr().out


def test_git_missing_exits_2_not_a_traceback(repo, monkeypatch):
    reg = repo / "planted.jsonl"
    reg.write_text(json.dumps(_entry()) + "\n")
    monkeypatch.setenv("PATH", "")
    assert ce.main(["--repo", str(repo), "--registry", str(reg)]) == 2


def test_the_registry_is_never_its_own_evidence(repo):
    reg = repo / "vv" / "experiments" / "registry.jsonl"
    reg.parent.mkdir(parents=True)
    reg.write_text(json.dumps(_entry(metrics={"x": 987654}, artifacts=["vv/evidence/2026-10-12-x"])) + "\n")
    _git(repo, "add", ".")
    fails, _ = ce.check(reg, repo)
    assert any("987654 is NOT traceable" in f for f in fails)


def test_a_bad_id_prints_without_a_traceback(repo, capsys):
    reg = repo / "planted.jsonl"
    reg.write_text(json.dumps(_entry(id="EXP-\ud800")) + "\n")
    assert ce.main(["--repo", str(repo), "--registry", str(reg)]) == 1
    assert "id is not EXP-NNN" in capsys.readouterr().out
