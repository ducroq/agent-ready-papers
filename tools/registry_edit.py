"""Edit one claim-registry row by its ID, refusing anything but exactly one match.

A row ID such as `S7-3` also opens rows in the Priority Guide and other summary tables, so a
substring or first-match edit can land in the wrong table. This tool matches only claim-table rows,
whose shape is `| ID | statement | P0-P3 | ...`, and refuses when it finds none or more than one.
Text containing an unescaped `|` or a line break is refused, since it would break the table, and
rows inside fenced code blocks are skipped. Line endings are kept as they are.

    python -m tools.registry_edit REGISTRY S5-18 --append "Full text read 2026-10-08: ..."
    python -m tools.registry_edit REGISTRY S5-18 --status x        # set the Status checkbox
    python -m tools.registry_edit REGISTRY S5-18 --replace OLD NEW # inside the statement cell
    ... --dry-run                                                  # print the new row, write nothing

Exit: 0 edited (or would edit); 1 refused (no match, several matches, OLD empty or not exactly once in the statement, or
an unescaped `|` or line break in new text); 2 the registry cannot be read or written.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\| (?P<id>[A-Z]+\d*-\d+) \| (?P<stmt>.*?) \| (?P<prio>P[0-3]) \|(?P<rest>.*)$")


def claim_rows(lines: list[str], row_id: str) -> list[int]:
    """Claim-table rows with this ID, skipping fenced code blocks (template examples)."""
    hits, fence = [], None  # fence: (character, length) of the open fence
    for i, line in enumerate(lines):
        bare = line.lstrip()
        m = re.match(r"(`{3,}|~{3,})(.*)", bare)
        if m:
            char, n, info = m.group(1)[0], len(m.group(1)), m.group(2).strip()
            if fence is None:
                fence = (char, n)
            elif char == fence[0] and n >= fence[1] and not info:
                fence = None  # only a bare closer of the same character, at least as long
            continue
        if fence is None and (m := ROW.match(line.rstrip("\r"))) and m.group("id") == row_id:
            hits.append(i)
    return hits


def edit_row(line: str, append: str | None, status: str | None, replace: tuple[str, str] | None) -> str:
    m = ROW.match(line)
    assert m
    stmt, rest = m.group("stmt"), m.group("rest")
    if replace:
        old, new = replace
        if not old or stmt.count(old) != 1:
            raise ValueError(f"{old!r} occurs {stmt.count(old) if old else 0} times in the statement of "
                             f"{m.group('id')}; it must occur exactly once")
        stmt = stmt.replace(old, new, 1)
    if append:
        stmt = stmt.rstrip()
        if stmt.endswith(".") and not stmt.endswith(".."):
            stmt = stmt[:-1]  # one full stop only; "..." and "…" stay
        stmt = stmt + ". " + append.strip()
    if status:
        rest, n = re.subn(r"\[[ x~]\] \|\s*$", f"[{status}] |", rest)
        if n != 1:
            raise ValueError(f"no Status checkbox at the end of {m.group('id')}")
    return f"| {m.group('id')} | {stmt} | {m.group('prio')} |{rest}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("registry", type=Path)
    ap.add_argument("row_id")
    ap.add_argument("--append", help="text appended to the statement cell")
    ap.add_argument("--status", choices=["x", " ", "~"], help="set the Status checkbox")
    ap.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"), help="replace text in the statement")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if not (a.append or a.status or a.replace):
        ap.error("nothing to do: give --append, --status or --replace")
    for t in (a.append, a.replace[1] if a.replace else None):
        if t and (re.search(r"(?<!\\)\|", t) or len(("x" + t + "x").splitlines()) > 1):
            print("REFUSED: new text contains an unescaped '|' or a line break, which would break the table;"
                  " write \\| and keep it on one line", file=sys.stderr)
            return 1
    try:
        with open(a.registry, encoding="utf-8", newline="") as f:  # keep CRLF as it is
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"CANNOT READ {a.registry}: {e}", file=sys.stderr)
        return 2
    lines = text.split("\n")
    hits = claim_rows(lines, a.row_id)
    if len(hits) != 1:
        where = ", ".join(f"line {i + 1}" for i in hits) or "none"
        print(f"REFUSED: {len(hits)} claim-table rows match {a.row_id} ({where}); expected exactly one",
              file=sys.stderr)
        return 1
    i = hits[0]
    cr = "\r" if lines[i].endswith("\r") else ""
    try:
        new = edit_row(lines[i].rstrip("\r"), a.append, a.status, tuple(a.replace) if a.replace else None)
    except ValueError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    unescaped = re.compile(r"(?<!\\)\|")
    if len(unescaped.findall(new)) != len(unescaped.findall(lines[i])) or not ROW.match(new):
        print("REFUSED: the edited row would have a different number of columns", file=sys.stderr)
        return 1
    print(f"line {i + 1}: {new}")
    if not a.dry_run:
        lines[i] = new + cr
        try:
            tmp = a.registry.with_name(a.registry.name + ".tmp")
            with open(tmp, "w", encoding="utf-8", newline="") as f:
                f.write("\n".join(lines))
            os.replace(tmp, a.registry)  # atomic: an interrupted write leaves the original
        except OSError as e:
            print(f"CANNOT WRITE {a.registry}: {e}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
