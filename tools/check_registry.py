"""Internal-consistency checks over a claim registry and its manuscript.

Five checks, all of them *internal consistency* — comparisons between two
artifacts the author controls. None of them touches the question a rule
cannot decide: whether a registered tier is the right tier given the
evidence. That is Step Z, and it stays a human-and-agent pass.

The distinction is what makes these safe to mechanise, and it is worth
stating precisely because the two halves are easy to conflate:

    registered tier vs. evidence   -> judgment.      Not here.
    prose / graph vs. registered   -> consistency.   Here.

Checks:

  anchors    Every `% S#-#` anchor in the manuscript has a registry row,
             and every registry row has an anchor. A row with no anchor
             claims coverage the paper may not have; an anchor with no
             row is prose nothing tracks.

  tiers      Every copy of an ID's confidence tier agrees: registry
             sub-table rows, manuscript anchors `% S1-1: text (TYPE, P0,
             TIER)`, and a LaTeX table whose header has a Confidence
             column. A disagreement says two copies differ — never which
             one is right. The copies have drifted apart before: eight
             registry tiers were raised without touching their anchors,
             and the two disagreed for six months (#37).

  schema     Type-conditional column completeness. ARGUMENT rows need
             Grounds, Warrant and Rebuttal; PROPOSITION rows need
             Constructs, Relationship, Boundary conditions and
             Alternatives engaged. Presence only — never quality.

  premises   The premise graph resolves: every referenced ID exists, is
             itself verified, and the graph is acyclic. Then the property
             worth having — **a conclusion may not sit at a higher
             confidence tier than its weakest premise.** That is
             tier-monotonicity on the argument graph rather than on prose,
             and unlike the prose form it is fully decidable.

  budget     Word count against a declared budget (a Hard Constraint that
             has until now been checked by eye).

Every check reports a count rather than a bare pass, per the rule in
`docs/verification-hooks.md`: a check that cannot be told apart from an
absent check is not a check. Zero rows is a failure, not a clean run.

Public API:
    check_registry(registry_path, *, manuscript_path=None, budget=None)
        -> RegistryReport

CLI:
    python -m tools.check_registry <registry.md>
        [--manuscript <file.tex>] [--budget N] [--json]

Exit codes:
    0  all enabled checks passed
    1  at least one finding
    2  tooling error (file missing, no entries parsed)
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Reused rather than reimplemented: `_split_row` carries the escaped-pipe
# fix from v2.2.4, and duplicating that here would mean duplicating the bug
# it fixed. Same package, same file format, one parser.
from tools.coverage import _MARKER_REGEX, _SEPARATOR_REGEX, _split_row

ANCHOR_REGEX = re.compile(r"^%\s*(S\d+-\d+)\s*:", re.MULTILINE)
_ANCHOR_LINE_REGEX = re.compile(r"^%\s*(S\d+-\d+)\s*:(.*)$")
_TRAILING_PAREN_REGEX = re.compile(r"\(([^()]*)\)\s*$")
# `%` starts a comment unless escaped as `\%`; `\\%` is a row break then a comment.
_TEX_COMMENT_REGEX = re.compile(r"(?<!(?<!\\)\\)%.*$", re.M)
_TEX_VERBATIM_REGEX = re.compile(r"\\begin\{(verbatim|lstlisting|minted|comment)\*?\}.*?\\end\{\1\*?\}", re.S)
# tabular, tabular*, tabularx and longtable. Nested tables are not supported:
# the lazy match stops at the first matching \end.
_TABULAR_REGEX = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable\*?)\}(.*?)\\end\{\1\}", re.S)
# `\\`, `\\*`, `\\[2pt]` and `\tabularnewline` all end a row.
_TEX_ROW_END_REGEX = re.compile(r"\\\\\*?(?:\s*\[[^\]]*\])?|\\tabularnewline\b")
_TEX_CELL_SPLIT_REGEX = re.compile(r"(?<!\\)&")
_TEX_MULTICOLUMN_REGEX = re.compile(r"\\multicolumn\{(\d+)\}")
# Macros whose argument is not cell text: footnotes, references, and the
# rule/colour commands that can lead a row (`\cmidrule(lr){2-3}`).
_TEX_DROP_REGEX = re.compile(
    r"\\(footnote(?:mark|text)?|tnote|cite[a-zA-Z]*|ref|label|cline|cmidrule|rowcolor|cellcolor|addlinespace)"
    r"(?![a-zA-Z])\*?"
    r"(?:\([^)]*\))?(?:\[[^\]]*\])*(?:\{[^{}]*\})*"
)
_TEX_MATH_REGEX = re.compile(r"\$[^$]*\$")
# `\multirow{2}{*}{EMERGING}`: the first two arguments are layout, the third is text.
_TEX_MULTIROW_REGEX = re.compile(r"\\multirow\*?(?:\[[^\]]*\])?\{[^{}]*\}(?:\[[^\]]*\])?\{[^{}]*\}")
# LaTeX-typed ID dashes: `S2--1` (en-dash), a pasted – or —, `S1\-1`, `S1$-$1`, `S1{-}1`.
_ID_DASH_REGEX = re.compile(r"(S\d+)[ \t]*(?:--|–|—|\\-|\$-\$|\{-\})[ \t]*(\d+)")
_NESTED_TABLE_REGEX = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable\*?)\}")
_ANCHOR_PAREN_REGEX = re.compile(r"\(([^()]*)\)")
_AFTER_ANCHOR_PAREN_REGEX = re.compile(r"\s*(%.*)?$")
_TEX_MACRO_REGEX = re.compile(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?")
_ID_TOKEN_REGEX = re.compile(r"(?<![\w-])S\d+-\d+(?![\w-])")
ENTRY_ID_REGEX = re.compile(r"^S\d+-\d+$")
_PREMISE_ID_REGEX = re.compile(r"S\d+-\d+")
_VERIFIED_REGEX = re.compile(r"^\s*\[\s*x\s*\]", re.IGNORECASE)

# Strongest first. A conclusion may not outrank its weakest premise.
TIER_ORDER = ("ESTABLISHED", "SUPPORTED", "EMERGING", "SPECULATIVE")
_TIER_RANK = {tier: rank for rank, tier in enumerate(TIER_ORDER)}

# DR-010's PROVOCATION axis. These are NOT confidence tiers and are not
# rankable against them; naming them lets the report say so instead of
# reporting a real unit type as an unrecognised string.
PROVOCATION_TIERS = ("GROUNDED", "EXTRAPOLATED", "PROVOCATIVE", "CRITICAL")


def _normalise_tier(raw: str) -> str:
    """Strip cell decoration before ranking a tier.

    Registries legitimately write `**SPECULATIVE**`, `` `EMERGING` `` or
    `SUPPORTED ⚠`, and an exact dict lookup on the raw cell silently returned
    None for every one of them — which skipped the comparison with no finding
    and no change to the Examined count, so a broken check and a clean run
    printed the same thing. Measured 2026-09-14.
    """
    out = raw.strip()
    for ch in ("*", "`", "_", "⚠", "~"):
        out = out.replace(ch, "")
    # a parenthetical qualifier: "SPECULATIVE (provisional)"
    if "(" in out:
        out = out.split("(", 1)[0]
    return out.strip().upper()


REQUIRED_COLUMNS = {
    "ARGUMENT": ("grounds", "warrant", "rebuttal"),
    "PROPOSITION": (
        "constructs",
        "relationship",
        "premises",
        "reasoning",
        "boundary conditions",
        "alternatives engaged",
    ),
}

_SEVERITY_ORDER = {"finding": 0, "note": 1}


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str  # "finding" | "note"
    entry_id: str
    message: str


@dataclass(frozen=True)
class Entry:
    entry_id: str
    unit_type: str
    tier: str
    verified: bool
    line_number: int
    columns: dict
    premises: tuple[str, ...]


@dataclass(frozen=True)
class RegistryReport:
    registry_path: Path
    entries: tuple[Entry, ...]
    findings: tuple[Finding, ...]
    checks_run: tuple[str, ...]
    counts: dict

    @property
    def ok(self) -> bool:
        return not any(f.severity == "finding" for f in self.findings)

    def to_dict(self) -> dict:
        return {
            "registry_path": self.registry_path.name,
            "checks_run": list(self.checks_run),
            "counts": self.counts,
            "findings": [asdict(f) for f in self.findings],
            "count_entries": len(self.entries),
            "count_findings": sum(1 for f in self.findings if f.severity == "finding"),
            "count_notes": sum(1 for f in self.findings if f.severity == "note"),
            "ok": self.ok,
        }

    def to_markdown(self) -> str:
        lines = [f"# Registry consistency — {self.registry_path.name}", ""]
        # Counts first: a bare "passed" is indistinguishable from a check
        # that examined nothing, so the numbers lead.
        lines.append("| Check | Examined | Findings |")
        lines.append("|-------|----------|----------|")
        for check in self.checks_run:
            found = sum(1 for f in self.findings if f.check == check and f.severity == "finding")
            lines.append(f"| {check} | {self.counts.get(check, 0)} | {found} |")
        lines.append("")

        if not self.findings:
            lines.append(f"No findings across {len(self.entries)} registry entries.")
            return "\n".join(lines) + "\n"

        for severity, heading in (("finding", "Findings"), ("note", "Notes")):
            group = [f for f in self.findings if f.severity == severity]
            if not group:
                continue
            lines.append(f"## {heading} ({len(group)})")
            lines.append("")
            for f in group:
                who = f"`{f.entry_id}` " if f.entry_id else ""
                lines.append(f"- **{f.check}** — {who}{f.message}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------
# registry parsing
# --------------------------------------------------------------------------


def _parse_entries(content: str) -> tuple[Entry, ...]:
    """Parse per-type sub-tables into one entry per registry row.

    `tools.coverage` aggregates these to counts; this keeps the row, since
    every check here is about an individual entry's relationships.
    """
    entries: list[Entry] = []
    unit_type: str | None = None
    header: list[str] | None = None

    for lineno, line in enumerate(content.splitlines(), start=1):
        marker = _MARKER_REGEX.match(line)
        if marker:
            unit_type = marker.group(1).upper()
            header = None
            continue
        if unit_type is None:
            continue
        if _SEPARATOR_REGEX.match(line):
            continue

        cells = _split_row(line)
        if cells is None:
            # A blank line ends a sub-table; prose between tables does too.
            if not line.strip():
                header = None
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if not cells or not ENTRY_ID_REGEX.match(cells[0]):
            continue

        # strict=False deliberately: a row with fewer cells than its header
        # is a truncated row, and the right response is for the schema check
        # to report the missing columns, not for the tool to raise.
        columns = dict(zip(header, cells, strict=False))
        premise_text = columns.get("premises", "") or columns.get("grounds", "")
        entries.append(
            Entry(
                entry_id=cells[0],
                unit_type=unit_type,
                tier=(columns.get("confidence", "") or "").strip().upper(),
                verified=bool(_VERIFIED_REGEX.match(columns.get("status", ""))),
                line_number=lineno,
                columns=columns,
                premises=tuple(dict.fromkeys(_PREMISE_ID_REGEX.findall(premise_text))),
            )
        )
    return tuple(entries)


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def _check_anchors(entries: tuple[Entry, ...], manuscript: str) -> tuple[list[Finding], int]:
    anchored = set(ANCHOR_REGEX.findall(manuscript))
    registered = {e.entry_id for e in entries}
    findings: list[Finding] = []

    for entry_id in sorted(registered - anchored):
        findings.append(
            Finding(
                "anchors",
                "finding",
                entry_id,
                "registered but no `% "
                f"{entry_id}:` anchor in the manuscript — the registry counts it "
                "as covered; confirm the prose exists and anchor it, or drop the row",
            )
        )
    for entry_id in sorted(anchored - registered):
        findings.append(
            Finding(
                "anchors",
                "finding",
                entry_id,
                "anchored in the manuscript but absent from the registry — prose nothing tracks",
            )
        )
    return findings, len(anchored | registered)


def _anchor_tiers(manuscript: str) -> tuple[list[tuple[str, str, str]], list[Finding]]:
    """Return ([(id, where, raw_tier)], notes) for every `% S#-#:` anchor.

    The tier is the last element of the trailing parenthesis, which the
    convention writes as `(TYPE, PRIORITY, TIER)`. An anchor without all
    three is a note rather than a silent skip: it is a copy of the tier
    that this check could not read, and the Examined count would
    otherwise hide it.
    """
    copies: list[tuple[str, str, str]] = []
    notes: list[Finding] = []
    for lineno, line in enumerate(manuscript.splitlines(), start=1):
        match = _ANCHOR_LINE_REGEX.match(line)
        if not match:
            continue
        entry_id, rest = match.groups()
        # The tier is the first parenthesis followed only by whitespace or a
        # `% comment`. First, not last: in `(…, SUPPORTED) % raised from
        # (…, EMERGING)` the tail is history, and reading it would hide the
        # very disagreement this check exists for. A `%` before the
        # parenthesis is prose ("100% of …"), since the anchor is already a
        # comment.
        parts: list[str] = []
        for paren in _ANCHOR_PAREN_REGEX.finditer(rest):
            candidate = [p.strip() for p in paren.group(1).split(",")]
            if len(candidate) >= 3 and _AFTER_ANCHOR_PAREN_REGEX.match(rest, paren.end()):
                parts = candidate
                break
        if len(parts) < 3 or not parts[-1]:
            notes.append(
                Finding(
                    "tiers",
                    "note",
                    entry_id,
                    f"manuscript anchor at line {lineno} has no parseable tier — expected a "
                    "trailing `(TYPE, PRIORITY, TIER)`, so this copy was NOT compared",
                )
            )
            continue
        copies.append((entry_id, f"manuscript anchor line {lineno}", parts[-1]))
    return copies, notes


def _blank(match: re.Match) -> str:
    """Replace a match with spaces, keeping newlines so line numbers survive."""
    return re.sub(r"[^\n]", " ", match.group(0))


def _tex_cell(raw: str) -> str:
    """Reduce a LaTeX cell to its text: `\\texttt{S1-2}` -> `S1-2`, `\\textsc{Emerging}$^a$` -> `Emerging`."""
    out = _TEX_MULTIROW_REGEX.sub(" ", raw)
    out = _TEX_DROP_REGEX.sub(" ", out)
    out = _TEX_MATH_REGEX.sub(" ", out)
    out = _TEX_MACRO_REGEX.sub(" ", out)
    for ch in "{}":
        out = out.replace(ch, " ")
    return " ".join(out.split())


def _tex_cells(row: str) -> list[tuple[str, int]]:
    """Split a row on unescaped `&` into (text, span); `\\multicolumn{n}` spans n columns."""
    cells: list[tuple[str, int]] = []
    for raw in _TEX_CELL_SPLIT_REGEX.split(row):
        span = _TEX_MULTICOLUMN_REGEX.search(raw)
        cells.append((_tex_cell(raw), int(span.group(1)) if span else 1))
    return cells


def _table_tiers(manuscript: str) -> tuple[list[tuple[str, str, str]], list[Finding]]:
    """Return ([(id, where, raw_tier)], notes) from LaTeX tables with a Confidence column.

    Rows are split on the row terminators, not on newlines, so a row wrapped
    across lines or two rows on one line both parse. The header is the first
    row with at least two cells, one containing "Confidence"; rows above it
    (a caption, a group header) are passed over. A header whose Confidence
    cell spans several columns is ambiguous and the table is noted, not read.

    Backstop for the whole class of silent drops: every entry ID that occurs
    in a Confidence table's body must yield either a copy or a note. Two
    review rounds found seven separate ways to lose a row; this is what makes
    an eighth visible.
    """
    # Comments first: a `% \\begin{verbatim}` must not open a verbatim block
    # that swallows every table up to the next real `\\end{verbatim}`.
    text = _TEX_COMMENT_REGEX.sub(_blank, manuscript)
    text = _TEX_VERBATIM_REGEX.sub(_blank, text)
    # Same length is not needed; only newlines are, and the dash forms have none.
    text = _ID_DASH_REGEX.sub(r"\1-\2", text)
    copies: list[tuple[str, str, str]] = []
    notes: list[Finding] = []

    newlines = [i for i, ch in enumerate(text) if ch == "\n"]

    def line_at(pos: int) -> int:
        return bisect.bisect_left(newlines, pos) + 1

    for block in _TABULAR_REGEX.finditer(text):
        body_start, body = block.start(2), block.group(2)
        column: int | None = None
        accounted: set[str] = set()
        rows = []
        pos = 0
        for end in [*(m for m in _TEX_ROW_END_REGEX.finditer(body)), None]:
            stop = len(body) if end is None else end.start()
            rows.append((pos, body[pos:stop]))
            pos = len(body) if end is None else end.end()

        for row_start, row in rows:
            cells = _tex_cells(row)
            if column is None:
                if len(cells) < 2:
                    continue
                col = 0
                for text_, span in cells:
                    if "confidence" in text_.lower():
                        column = col if span == 1 else -1
                        break
                    col += span
                if column == -1:
                    notes.append(
                        Finding(
                            "tiers",
                            "note",
                            "",
                            f"table at line {line_at(block.start())} has a Confidence header spanning "
                            "several columns, so which column holds the tier is ambiguous; its "
                            "tier copies were NOT compared",
                        )
                    )
                    break
                continue
            id_match = _ID_TOKEN_REGEX.search(cells[0][0]) if cells else None
            if id_match is None:
                continue
            entry_id = id_match.group(0)
            accounted.add(entry_id)
            lineno = line_at(body_start + row_start + row.find(entry_id))
            flat = [c for c, span in cells for c in [c] + [""] * (span - 1)]
            if len(flat) <= column or not flat[column]:
                notes.append(
                    Finding(
                        "tiers",
                        "note",
                        entry_id,
                        f"manuscript table row at line {lineno} has no cell in the Confidence "
                        "column, so this copy was NOT compared",
                    )
                )
                continue
            copies.append((entry_id, f"manuscript table line {lineno}", flat[column]))

        if column is None or column == -1:
            continue
        nested = _NESTED_TABLE_REGEX.search(body)
        if nested:
            notes.append(
                Finding(
                    "tiers",
                    "note",
                    "",
                    f"the Confidence table at line {line_at(block.start())} contains a nested table "
                    f"(line {line_at(body_start + nested.start())}); nested tables are not supported, "
                    "and rows after the nested table's end were NOT read",
                )
            )
        for token in _ID_TOKEN_REGEX.finditer(body):
            if token.group(0) not in accounted:
                accounted.add(token.group(0))
                notes.append(
                    Finding(
                        "tiers",
                        "note",
                        token.group(0),
                        f"appears in the Confidence table at line {line_at(body_start + token.start())} "
                        "but no tier copy was read from it — the row did not parse as an entry row",
                    )
                )
    return copies, notes


def _check_tiers(entries: tuple[Entry, ...], manuscript: str) -> tuple[list[Finding], int]:
    """Compare every parseable copy of each ID's tier; one finding per disagreeing ID.

    Consistency only: which copy is right is Step Z's question, and the
    remediation that made Paper 1's copies agree first did so in the wrong
    direction (#37).
    """
    copies: dict[str, list[tuple[str, str]]] = {}
    for entry in entries:
        copies.setdefault(entry.entry_id, []).append((f"registry line {entry.line_number}", entry.tier))
    anchor_copies, findings = _anchor_tiers(manuscript)
    table_copies, table_notes = _table_tiers(manuscript)
    findings += table_notes
    for entry_id, where, raw in anchor_copies + table_copies:
        copies.setdefault(entry_id, []).append((where, raw))

    examined = 0
    for entry_id in sorted(copies):
        found = copies[entry_id]
        if len(found) < 2:
            continue
        examined += 1
        if len({_normalise_tier(raw) for _, raw in found}) > 1:
            listed = "; ".join(f"{where} `{raw.strip() or '(blank)'}`" for where, raw in found)
            findings.append(
                Finding(
                    "tiers",
                    "finding",
                    entry_id,
                    f"tier copies disagree — {listed}. This says the copies differ, not which one is right",
                )
            )
    if examined == 0:
        findings.append(
            Finding(
                "tiers",
                "note",
                "",
                "no entry had two readable tier copies, so the tier check compared NOTHING — "
                "anchors need a trailing `(TYPE, PRIORITY, TIER)`, or print a table with a "
                "Confidence column",
            )
        )
    return findings, examined


def _check_schema(entries: tuple[Entry, ...]) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    examined = 0
    for entry in entries:
        required = REQUIRED_COLUMNS.get(entry.unit_type)
        if not required:
            continue
        examined += 1
        for column in required:
            value = (entry.columns.get(column) or "").strip()
            if not value or value in {"-", "--", "—", "TBD", "N/A"}:
                findings.append(
                    Finding(
                        "schema",
                        "finding",
                        entry.entry_id,
                        f"{entry.unit_type} row has no **{column}** — the "
                        "type-conditional Gate 2 expectation is unmet "
                        "(presence only; this says nothing about quality)",
                    )
                )
    return findings, examined


def _uncomparable(raw: str, subject: str) -> str:
    """Say WHY a tier could not be ranked, rather than skipping in silence."""
    norm = _normalise_tier(raw)
    if not norm:
        return (
            f"{subject} records no confidence tier, so tier-monotonicity could NOT be "
            "checked for this entry — an absent check is not a passing one. If the "
            "column exists under another name, the parser did not find it."
        )
    if norm in PROVOCATION_TIERS:
        return (
            f"{subject} is on the PROVOCATION axis (`{norm}`, DR-010), which is not "
            "rankable against the confidence tiers, so tier-monotonicity could NOT be "
            "checked here. This tool does not yet support the PROVOCATION axis."
        )
    return (
        f"{subject} has tier `{raw.strip()}`, which is not one of "
        f"{', '.join(TIER_ORDER)}, so tier-monotonicity could NOT be checked for it."
    )


def _check_premises(entries: tuple[Entry, ...]) -> tuple[list[Finding], int]:
    by_id = {e.entry_id: e for e in entries}
    findings: list[Finding] = []
    examined = 0

    for entry in entries:
        if not entry.premises:
            continue
        examined += 1
        weakest_rank = -1
        weakest_id = ""
        for premise_id in entry.premises:
            premise = by_id.get(premise_id)
            if premise is None:
                findings.append(
                    Finding(
                        "premises",
                        "finding",
                        entry.entry_id,
                        f"cites premise `{premise_id}`, which is not in the registry",
                    )
                )
                continue
            if not premise.verified:
                findings.append(
                    Finding("premises", "finding", entry.entry_id, f"rests on `{premise_id}`, which is not verified")
                )
            rank = _TIER_RANK.get(_normalise_tier(premise.tier))
            if rank is None:
                findings.append(
                    Finding(
                        "premises",
                        "finding",
                        entry.entry_id,
                        _uncomparable(premise.tier, f"premise `{premise_id}`"),
                    )
                )
                continue
            if rank > weakest_rank:
                weakest_rank, weakest_id = rank, premise_id

        own_rank = _TIER_RANK.get(_normalise_tier(entry.tier))
        if own_rank is None:
            findings.append(
                Finding("premises", "finding", entry.entry_id, _uncomparable(entry.tier, "this entry")),
            )
        if own_rank is not None and weakest_rank >= 0 and own_rank < weakest_rank:
            findings.append(
                Finding(
                    "premises",
                    "finding",
                    entry.entry_id,
                    f"is {entry.tier} but its weakest premise `{weakest_id}` is "
                    f"{TIER_ORDER[weakest_rank]} — a conclusion may not outrank "
                    "the evidence it is built from",
                )
            )

    for cycle in _find_cycles({e.entry_id: e.premises for e in entries}):
        findings.append(Finding("premises", "finding", cycle[0], "premise cycle: " + " -> ".join(cycle + (cycle[0],))))
    return findings, examined


def _find_cycles(graph: dict) -> list[tuple[str, ...]]:
    """Return one representative cycle per strongly-connected component."""
    visiting: set[str] = set()
    done: set[str] = set()
    cycles: list[tuple[str, ...]] = []

    def walk(node: str, path: list[str]) -> None:
        if node in done:
            return
        if node in visiting:
            # path already ends with the repeat of `node` that closed the
            # cycle; trim it, or the rendered message reads "a -> b -> a -> a".
            start = path.index(node)
            cycles.append(tuple(path[start:-1]))
            return
        visiting.add(node)
        for nxt in graph.get(node, ()):  # missing IDs are the premises check's job
            if nxt in graph:
                walk(nxt, path + [nxt])
        visiting.discard(node)
        done.add(node)

    for node in sorted(graph):
        walk(node, [node])
    return cycles


_TEX_STRIP = (
    (re.compile(r"(?m)^\s*%.*$"), ""),  # comment lines
    (
        re.compile(
            r"\\begin\{(equation|align|figure|table|tabular|verbatim)\*?\}"
            r".*?\\end\{\1\*?\}",
            re.S,
        ),
        " ",
    ),
    (re.compile(r"\\(cite|ref|label|citep|citet)\w*\{[^}]*\}"), " "),
    (re.compile(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?"), " "),  # remaining macros
    (re.compile(r"[{}$&~^_\\]"), " "),
)


def count_words(tex: str) -> int:
    """Approximate body word count for a LaTeX manuscript.

    Deliberately approximate and documented as such: comments, math
    environments, floats and macros are stripped, everything else counts.
    The budget constraint is a threshold with slack, not an exact figure,
    so a stable approximation is worth more than a precise one that
    disagrees with whatever the target venue counts.
    """
    for pattern, replacement in _TEX_STRIP:
        tex = pattern.sub(replacement, tex)
    return len(tex.split())


def _check_budget(manuscript: str, budget: int) -> tuple[list[Finding], int]:
    words = count_words(manuscript)
    if words > budget:
        return [
            Finding(
                "budget",
                "finding",
                "",
                f"manuscript is ~{words} words against a budget of {budget} "
                f"(~{words - budget} over) — a Hard Constraint; exceeding it "
                "needs a decision record",
            )
        ], words
    if words > budget * 0.95:
        return [Finding("budget", "note", "", f"manuscript is ~{words} words, within 5% of the {budget} budget")], words
    return [], words


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


def check_registry(
    registry_path: Path,
    *,
    manuscript_path: Path | None = None,
    budget: int | None = None,
) -> RegistryReport:
    """Run every applicable internal-consistency check.

    Args:
        registry_path: path to claim_registry.md
        manuscript_path: optional manuscript; enables the anchor and tier
            checks (and the budget check, which needs a word count)
        budget: optional word budget; requires manuscript_path

    Raises:
        FileNotFoundError: if a given path does not exist
        ValueError: if the registry parses to zero entries — a legitimate
            registry is never empty, so that is a failure, not a clean run
    """
    if not registry_path.is_file():
        raise FileNotFoundError(registry_path)
    entries = _parse_entries(registry_path.read_text(encoding="utf-8"))
    if not entries:
        raise ValueError(
            f"no registry entries parsed from {registry_path} — a registry is never "
            "legitimately empty, so this is a parse failure rather than a clean run"
        )

    findings: list[Finding] = []
    counts: dict = {}
    checks: list[str] = []

    schema_findings, schema_count = _check_schema(entries)
    findings += schema_findings
    counts["schema"] = schema_count
    checks.append("schema")

    premise_findings, premise_count = _check_premises(entries)
    findings += premise_findings
    counts["premises"] = premise_count
    checks.append("premises")

    if manuscript_path is not None:
        if not manuscript_path.is_file():
            raise FileNotFoundError(manuscript_path)
        manuscript = manuscript_path.read_text(encoding="utf-8")

        anchor_findings, anchor_count = _check_anchors(entries, manuscript)
        findings += anchor_findings
        counts["anchors"] = anchor_count
        checks.append("anchors")

        tier_findings, tier_count = _check_tiers(entries, manuscript)
        findings += tier_findings
        counts["tiers"] = tier_count
        checks.append("tiers")

        if budget is not None:
            budget_findings, words = _check_budget(manuscript, budget)
            findings += budget_findings
            counts["budget"] = words
            checks.append("budget")

    findings.sort(key=lambda f: (_SEVERITY_ORDER[f.severity], f.check, f.entry_id))
    return RegistryReport(
        registry_path=registry_path,
        entries=entries,
        findings=tuple(findings),
        checks_run=tuple(checks),
        counts=counts,
    )


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.check_registry",
        description="Internal-consistency checks over a claim registry and its "
        "manuscript. Checks consistency, never correctness — whether a tier is "
        "the right tier stays a human pass.",
    )
    p.add_argument("registry", type=Path, help="Path to claim_registry.md")
    p.add_argument(
        "--manuscript", type=Path, default=None, help="Manuscript source; enables the anchor, tier and budget checks"
    )
    p.add_argument("--budget", type=int, default=None, help="Word budget; requires --manuscript")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    if args.budget is not None and args.manuscript is None:
        print("error: --budget requires --manuscript", file=sys.stderr)
        return 2
    try:
        report = check_registry(args.registry, manuscript_path=args.manuscript, budget=args.budget)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(report.to_markdown())
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
