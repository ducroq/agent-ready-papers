"""Experiment registry check: schema, id order, and that every number traces to its evidence.

DR-024 (Accepted 2026-10-12). Run by `make check-experiments` and `make check`.

Checks vv/experiments/registry.jsonl, one JSON object per line (schema:
vv/experiments/README.md). Ported from llm-distillery's
check_experiment_registry.py, with the three changes DR-024 rule 4 asks for
and some of this port's own:

  tracked     (rule 4) Each artifact must be tracked by git (staged counts),
              exist on disk, and not be a symlink. Inside a folder, only
              tracked files are searched.
  inside      (rule 1) Each artifact must sit inside vv/evidence/<date>-<name>,
              so the registry, DRs and hypothesis logs are never evidence. No
              "..", absolute path, glob character, leading ":" or control
              character.
  boundaries  (rule 4) A metric matches only where it stands alone. Before it
              there may be no letter, digit, "_", "#", "+", "-", minus sign,
              "/", "%", "^" or ".", and no ":" that follows a digit. After it
              there may be no letter, digit, "_" or "%", no ".", "/", ":" or
              "-" followed by a digit, and no "-" followed by a letter. A comma
              between digits blocks a match only where it reads as a thousands
              separator (a group of exactly three digits follows it). So 41 does not match "#41" or "DR-041", 0.35 does not
              match "+0.350", 521 does not match "34,521", and 76 does not
              match "76/83" (write the metric as "76/83" instead). Dates and
              times are removed first: ISO dates and timestamps, "4 October",
              "4th Oct. 2026", "October 4", "Oct. 4, 2026", "4-Oct-2026",
              "4-6 October", "October 2026", and "12:30".
  suffixes    (rule 4) Folders are searched in .md, .txt, .json, .jsonl, .py,
              .tex and .csv files, in any letter case.
  not evidence  A PREREGISTRATION.md and the checker's own saved output
              (check-*.txt) are never searched, by file name: one holds predictions, the
              other the failing numbers it printed. Commit messages are not
              searched either (llm-distillery searched them); the entry's
              author writes them too.
  as written  A number matches only as Python prints it (and, for an integer,
              with thousands commas). A metric that a script prints with other
              rounding is written as a string.

Also: `judge` replaces `oracle`, `cost_ref` is new (DR-024 rule 3), and
`preregistered` is a sixth decision value, for an entry written before any
result is seen. Such an entry has no metric values, cites a tracked
PREREGISTRATION.md, and is concluded by a later entry whose `references` name
its id. The report lists preregistrations no later entry concludes. Any other
entry must state at least one metric that is not null, so the check never
passes over nothing.

What it cannot see:
  - Whether a number is the right one. A metric that appears in its artifact
    passes even if the artifact is a summary written to contain it (DR-024
    rule 6: such an entry says so in `notes`).
  - Whether a stand-alone number is the quantity meant: 4 matches "[4]",
    "Fig. 4" or "exit 4". Name the metric so a reader can find it.
  - "May" followed by a number is read as a date, so "May 3" never matches 3.
  - A comma next to a group of exactly three digits reads as a thousands
    separator, so in a CSV row "1,923" the cell 923 does not match.
  - Month names are matched in English and with a capital only.
  - A string metric shaped like a date or a time ("2026-10-04", "1:10") is
    removed with the dates, so it can never pass; record it in `notes`.
  - Predictions saved under another file name than PREREGISTRATION.md are
    searched like any evidence.
  - Whether a commit has been pushed: a commit that exists only locally passes
    here and fails in a clone.

Exit codes: 0 all checks pass; 1 at least one FAIL; 2 the registry cannot be
read, or git cannot be run, or the repo is not a git work tree.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
REGISTRY = Path("vv/experiments/registry.jsonl")
EVIDENCE = "vv/evidence/"
NONE = type(None)
FIELDS = {
    "id": str,
    "date": str,
    "title": str,
    "hypothesis": str,
    "subject": str,
    "judge": (str, NONE),
    "branch": str,
    "commits": list,
    "spend_usd": (int, float, NONE),
    "cost_ref": (str, NONE),
    "population": dict,
    "metrics": dict,
    "decision": str,
    "decision_rationale": str,
    "artifacts": list,
    "references": list,
    "review": (str, NONE),
}
OPTIONAL = {"notes": str}
LISTS_OF_STR = ("commits", "artifacts", "references")
DECISIONS = {"kept", "parked", "rejected", "rolled_back", "superseded", "preregistered"}
SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".py", ".tex", ".csv"}
ID_RE = re.compile(r"^EXP-\d{3}$")
HASH_RE = re.compile(r"^[0-9a-f]{7,40}$")
NOT_EVIDENCE = re.compile(r"^(?:PREREGISTRATION\.md|check-.*\.txt)$", re.I)
MONTH = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?"
    r"|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b\.?"
)
DAY = r"\d{1,2}(?:st|nd|rd|th)?"
DATES = re.compile(
    r"\d{4}-\d{2}-\d{2}(?:T[\d:.]+(?:Z|[+-]\d{2}:?\d{2})?)?"
    rf"|\b{DAY}(?:\s*[-–]\s*{DAY})?[\s-]+{MONTH}(?:,?[\s-]+\d{{4}})?"
    rf"|\b{MONTH}\s+(?:{DAY}\b(?:,?\s+\d{{4}})?|\d{{4}}\b)"
    r"|\b\d{1,2}:\d{2}(?::\d{2})?\b"
)
# A comma counts as a thousands separator only before a group of exactly three digits.
BEFORE = r"(?<![\w#+\-/%^.−])(?<!\d:)(?:(?<!\d,)|(?!\d{3}(?!\d)))"
AFTER = r"(?![\w%]|[./:\-]\d|,\d{3}(?!\d)|-[A-Za-z])"


class GitError(Exception):
    pass


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", "--literal-pathspecs", "-C", str(repo), *args], capture_output=True, text=True)  # noqa: S603, S607
    except OSError as ex:
        raise GitError(f"cannot run git: {ex.strerror}") from ex


def bad_path(a: str) -> str | None:
    """Why `a` cannot name one place in the repo, or None."""
    p = PurePosixPath(a)
    if not a or a.strip() != a:
        return "empty or padded"
    try:
        a.encode("utf-8")
    except UnicodeEncodeError:
        return "not valid text"
    if re.search(r"[\x00-\x1f\x7f]", a):
        return "holding a control character"
    if p.is_absolute() or a.startswith(("~", ":")) or re.search(r"[*?\[\\]", a):
        return "absolute, a pattern or magic"
    if p.parts in ((), (".",)) or ".." in p.parts:
        return "the repo root or outside it"
    if not (a + "/").startswith(EVIDENCE) or len(p.parts) < 3:
        return f"not inside {EVIDENCE}<date>-<name>"
    return None


def tracked_files(repo: Path, path: str) -> list[str]:
    """Tracked paths at or under `path`."""
    r = git(repo, "ls-files", "-z", "--", path)
    if r.returncode != 0:
        raise GitError(f"git ls-files failed on {path!r}: {r.stderr.strip()}")
    return [p for p in r.stdout.split("\0") if p]


def evidence_text(repo: Path, entry: dict) -> str:
    blobs = []
    for a in entry["artifacts"]:
        if bad_path(a):
            continue  # reported by check_entry
        for rel in tracked_files(repo, a):
            f = repo / rel
            if NOT_EVIDENCE.match(f.name) or f.is_symlink() or not f.is_file():
                continue
            if f.suffix.lower() in SUFFIXES or rel == a:
                blobs.append(f.read_text(encoding="utf-8", errors="replace"))
    return DATES.sub(" ", "\n".join(blobs))


def forms(value) -> list[str]:
    if isinstance(value, int):
        return sorted({str(value), f"{value:,}"})
    return [str(value)]


def traceable(value, text: str) -> bool:
    """True when the metric stands alone somewhere in the text (module docstring, `boundaries`)."""
    if value is None:
        return True
    return any(re.search(BEFORE + re.escape(f) + AFTER, text) for f in forms(value))


def no_duplicate_keys(pairs):
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise ValueError(f"duplicate key {dup[0]!r}")
    return dict(pairs)


def schema_fails(e: dict, label: str) -> list[str]:
    """Missing, unknown and wrongly typed fields. The other checks run only when this is empty."""
    fails = []
    for name, kind in {**FIELDS, **OPTIONAL}.items():
        if name not in e:
            if name in FIELDS:
                fails.append(f"{label}: missing required field `{name}`")
        elif not isinstance(e[name], kind) or isinstance(e[name], bool):
            fails.append(f"{label}: field `{name}` has the wrong type ({type(e[name]).__name__})")
        elif name in LISTS_OF_STR and not all(isinstance(x, str) for x in e[name]):
            fails.append(f"{label}: field `{name}` must be a list of strings")
    for name in sorted(set(e) - set(FIELDS) - set(OPTIONAL)):
        fails.append(f"{label}: unknown field `{name}`")
    return fails


def check_entry(repo: Path, e: dict, label: str) -> list[str]:
    fails = []
    if not ID_RE.match(e["id"]):
        fails.append(f"{label}: id is not EXP-NNN")
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["date"]):
            raise ValueError
        date.fromisoformat(e["date"])
    except ValueError:
        fails.append(f"{label}: date is not a real ISO date (YYYY-MM-DD)")
    s = e["spend_usd"]
    if s is not None and not (0 <= s < float("inf")):
        fails.append(f"{label}: spend_usd must be a finite number of zero or more")
    if e["decision"] not in DECISIONS:
        fails.append(f"{label}: decision {e['decision']!r} not in {sorted(DECISIONS)}")
    for c in e["commits"]:
        if not HASH_RE.match(c):
            fails.append(f"{label}: commit {c!r} is not a hash (a branch or HEAD moves)")
        elif git(repo, "cat-file", "-e", f"{c}^{{commit}}").returncode != 0:
            fails.append(f"{label}: commit not found: {c}")
    prereg = False
    for a in e["artifacts"]:
        why = bad_path(a)
        if why:
            fails.append(f"{label}: artifact path {a!r} is {why}")
            continue
        files = tracked_files(repo, a)
        if not files:
            where = "exists on disk but " if (repo / a).exists() else ""
            fails.append(f"{label}: artifact {where}is not tracked by git: {a}")
        for rel in files:
            f = repo / rel
            if f.is_symlink() or not f.is_file():
                fails.append(f"{label}: tracked file is a symlink or missing on disk: {rel}")
            prereg |= f.name == "PREREGISTRATION.md"
    metrics = e["metrics"]
    for k, v in metrics.items():
        if not (v is None or isinstance(v, (str, int, float)) and not isinstance(v, bool)) or v == "" or v != v:
            fails.append(f"{label}: metric `{k}` must be a number, a non-empty string or null")
    if e["decision"] == "preregistered":
        if any(v is not None for v in metrics.values()):
            fails.append(f"{label}: a preregistered entry has a metric value; results come in a later entry")
        if not prereg:
            fails.append(f"{label}: a preregistered entry cites no tracked PREREGISTRATION.md")
    elif all(v is None for v in metrics.values()):
        fails.append(f"{label}: states no metric that is not null, so nothing would be checked")
    return fails


def check(registry: Path, repo: Path) -> tuple[list[str], dict]:
    fails, entries, good = [], [], []
    for n, line in enumerate(registry.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line, object_pairs_hook=no_duplicate_keys)
        except ValueError as ex:
            fails.append(f"line {n}: not valid JSON ({ex})")
            continue
        if not isinstance(e, dict):
            fails.append(f"line {n}: not a JSON object")
            continue
        entries.append(e)
        label = e["id"] if isinstance(e.get("id"), str) else f"line {n}"
        schema = schema_fails(e, label)
        fails += schema or check_entry(repo, e, label)
        if not schema:
            good.append(e)
    if not entries:
        fails.append("the registry holds no entries")
    ids = [e["id"] for e in entries if isinstance(e.get("id"), str)]
    if len(set(ids)) != len(ids):
        fails.append("duplicate ids")
    if ids != sorted(ids):
        fails.append("ids are not in ascending order")

    checked = untraceable = 0
    for e in good:
        text = evidence_text(repo, e)
        for k, v in e["metrics"].items():
            if v is None or v == "" or v != v or isinstance(v, (bool, dict, list)):  # reported by check_entry
                continue
            checked += 1
            if not traceable(v, text):
                untraceable += 1
                fails.append(f"{e['id']}: metric `{k}` = {v} is NOT traceable to a tracked artifact")

    known, open_ = set(ids), []
    for i, e in enumerate(good):
        for r in e.get("references", []):
            if ID_RE.match(r) and r not in known:
                fails.append(f"{e['id']}: references {r}, which is not in the registry")
        if e.get("decision") == "preregistered":
            later = good[i + 1 :]
            if not any(e["id"] in x.get("references", []) and x.get("decision") != "preregistered" for x in later):
                open_.append(e["id"])
    spend = sum(e["spend_usd"] for e in good if isinstance(e.get("spend_usd"), (int, float)))
    return fails, {
        "entries": len(entries),
        "checked": checked,
        "untraceable": untraceable,
        "open": open_,
        "spend": spend,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Check the experiment registry (DR-024): schema, id order, "
        "tracked artifacts, and that every metric traces to its evidence."
    )
    ap.add_argument("--repo", type=Path, default=REPO, help="git work tree that artifact paths resolve against")
    ap.add_argument("--registry", type=Path, help=f"registry to check (default: <repo>/{REGISTRY})")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")  # an id with a lone surrogate must not crash the report
    repo = args.repo.resolve()
    registry = args.registry or repo / REGISTRY
    try:
        if git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
            print(f"ERROR: {repo} is not a git work tree")
            return 2
        fails, s = check(registry, repo)
    except GitError as ex:
        print(f"ERROR: {ex}")
        return 2
    except (OSError, UnicodeDecodeError) as ex:
        print(f"ERROR: cannot read {registry}: {ex}")
        return 2
    print(f"entries {s['entries']}   metrics checked {s['checked']}   untraceable {s['untraceable']}")
    print(f"spend recorded: ${s['spend']:.2f}")
    print(f"open preregistrations: {', '.join(s['open']) or 'none'}")
    for f in fails:
        print(f"  FAIL  {f}")
    print("PASS" if not fails else f"{len(fails)} FAILURE(S)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
