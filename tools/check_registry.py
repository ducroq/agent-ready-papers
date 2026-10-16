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
             Alternatives engaged (DR-004 tables, deprecated, read through
             v5.x). DR-027 tables: Says is descriptive/normative; every
             Grounds / Rests-on item is typed (`src:`, `claim:`, `decl:`,
             `own:` with its method); `claim:` grounds need a Warrant; a
             normative claim or contribution needs boundary conditions and
             a `decl:` value; a contribution is P0; a declared starting
             point has a valid Kind and Contestedness. A row with content
             whose ID matches no pattern is a finding. Presence only —
             never quality.

  premises   The premise graph resolves: every referenced ID exists, is
             itself verified, and the graph is acyclic. Then the property
             worth having — **a conclusion may not sit at a higher
             confidence tier than its weakest premise.** That is
             tier-monotonicity on the argument graph rather than on prose,
             and unlike the prose form it is fully decidable.

  budget     Word count against a declared budget (a Hard Constraint that
             has until now been checked by eye).

  glossary   With --glossary (DR-028): the file exists, is not empty and no
             longer carries the template's `**Paper:** [Title]`. Without the
             flag the report says "glossary: not checked".

IDs: `S<n>-<n>` (optionally `S2-3a`), `C<n>` (contribution), `D<n>` (declared
starting point; anchored as `% D1: label (kind, contestedness)`, no tier).
In DR-027 tables the premise graph is the `claim:` items; `decl:` items must
resolve to D rows; `src:` and `own:` items are not edges.

Every check reports a count rather than a bare pass, per the rule in
`docs/verification-hooks.md`: a check that cannot be told apart from an
absent check is not a check. A file with no recognised sub-table marker is a
failure, not a clean run; a freshly started registry (markers over empty
tables) reports zero examined.

Public API:
    check_registry(registry_path, *, manuscript_path=None, budget=None,
                   glossary_path=None)
        -> RegistryReport

CLI:
    python -m tools.check_registry <registry.md>
        [--manuscript <file.tex>] [--budget N] [--glossary <glossary.md>] [--json]

Exit codes:
    0  all enabled checks passed
    1  at least one finding
    2  tooling error (file missing, no recognised sub-table marker)
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
from tools.coverage import (
    _MARKER_REGEX,
    _SEPARATOR_REGEX,
    CLAIMS_TABLE,
    CONTRIBUTION,
    CONTRIBUTIONS_TABLE,
    DECLARED,
    DECLARED_TABLE,
    _has_marker,
    _split_row,
    deprecation_notes,
    marker_kind,
    near_miss_markers,
    says_unit_type,
)

# Entry IDs: `S2-3` or `S2-3a` (a claim, by manuscript section), `C1` (a
# contribution), `D1` (a declared starting point; DR-027).
_ID = r"(?:S\d+-\d+[a-z]?|[CD]\d+)"
ANCHOR_REGEX = re.compile(rf"^%\s*({_ID})\s*:", re.MULTILINE)
_ANCHOR_LINE_REGEX = re.compile(rf"^%\s*({_ID})\s*:(.*)$")
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
# Tier-carrying IDs only: a declared starting point has no tier to print.
_ID_TOKEN_REGEX = re.compile(r"(?<![\w-])(?:S\d+-\d+[a-z]?|C\d+)(?![\w-])")
ENTRY_ID_REGEX = re.compile(rf"^{_ID}$")
DR004_KINDS = ("CLAIM", "ARGUMENT", "PROPOSITION")
_INPUT_REGEX = re.compile(r"\\(input|include)(?:\s*\{([^{}]+)\}|\s+([^\s{}\\]+))")
_INPUT_PATH_REGEX = re.compile(r"\\def\s*\\input@path\s*\{((?:\{[^{}]*\})+)\}")
# DR-004 Grounds / Premises are free text: only S-IDs are references there, as
# before v5.0.0 (`Smith's model C2` is not a premise). A suffix (`S2-3a`) is read
# only when it ends the token, so every master match still matches.
_PREMISE_ID_REGEX = re.compile(r"S\d+-\d+(?:[a-z](?!\w))?")
# A DR-027 grounds / Rests-on item: `src: Author Year`, `claim: S1-2`, `decl: D1`,
# or `own: <method or query>` (the author's own observation, experiment or measurement;
# not a reference, not a graph edge, not a source).
_GROUNDS_ITEM_REGEX = re.compile(r"^(src|claim|decl|own)\s*:\s*(.*)$", re.IGNORECASE | re.S)
_MISSING_VALUES = {"", "-", "--", "—", "TBD", "N/A"}
_TYPED_ITEM_START = re.compile(r"^\s*(src|claim|decl|own)\s*:", re.IGNORECASE)
DR027 = "DR-027"
DR004 = "DR-004"
DECLARED_KINDS = ("assumption", "definition", "value")
CONTESTEDNESS = ("accepted", "contested", "own")
# The ID prefix each DR-027 table holds.
_TABLE_ID_PREFIX = {CLAIMS_TABLE: "S", CONTRIBUTIONS_TABLE: "C", DECLARED_TABLE: "D"}
# Placeholder tokens of templates/glossary.md (DR-028: a glossary that still
# contains any of them was copied, not filled in). Prefixes where the template's
# bracket carries an example (`[Domain 1]`, `[meaning in field A]`).
GLOSSARY_PLACEHOLDERS = (
    "[Title]",
    "[e.g., metrology",
    "[Domain ",
    "[term]",
    "[formal definition]",
    "[VIM",
    "[accessible explanation]",
    "[definition]",
    "[field]",
    "[disambiguation",
    "[notes]",
    "[meaning in field",
    "[which meaning",
    "[abbr]",
    "[full form]",
    "[date]",
    "[N]",
)
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
    premises: tuple[str, ...]  # `claim:` references (DR-004: IDs in Grounds / Premises)
    schema: str = DR004  # DR004 or DR027: which rules check this row
    decls: tuple[str, ...] = ()  # DR-027 `decl:` references
    # DR-027 grounds / Rests-on items as (kind, value); kind "" when untyped.
    items: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class RegistryReport:
    registry_path: Path
    entries: tuple[Entry, ...]
    findings: tuple[Finding, ...]
    checks_run: tuple[str, ...]
    counts: dict
    deprecations: tuple[str, ...] = ()
    glossary_checked: bool = False

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
            "deprecations": list(self.deprecations),
            "glossary": "checked" if self.glossary_checked else "not checked",
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
        # Not findings: neither changes the exit code.
        extra = [f"Deprecation: this registry {note}." for note in self.deprecations]
        if not self.glossary_checked:
            extra.append("glossary: not checked (pass --glossary to check the paper's glossary, DR-028)")
        if extra:
            lines += extra + [""]

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


def _missing(value: str | None) -> bool:
    """The missing-value convention: empty, `-`, `--`, `—`, `TBD`, `N/A`."""
    return (value or "").strip() in _MISSING_VALUES


def _clean_id(raw: str) -> str:
    """`` `S1-2` `` or `**S1-2**` -> `S1-2`: strip cell decoration around a referenced ID."""
    return raw.strip().strip("*`_ ").strip()


def _first_word(raw: str) -> str:
    """`accepted in the field` -> `accepted`; decoration stripped, lower-cased."""
    words = raw.strip().strip("*`_ ").lower().split()
    return words[0].strip(".,;:()") if words else ""


def _grounds_items(text: str) -> tuple[tuple[str, str], ...]:
    """Split a DR-027 Grounds / Rests-on cell into (kind, value) items; kind "" when untyped."""
    if _missing(text):
        return ()
    items: list[tuple[str, str]] = []
    for raw in text.split(";"):
        item = raw.strip()
        if not item:
            continue
        typed = _GROUNDS_ITEM_REGEX.match(item)
        items.append((typed.group(1).lower(), typed.group(2).strip()) if typed else ("", item))
    return tuple(items)


def _new_schema_entry(entry_id: str, table: str, columns: dict, lineno: int) -> Entry:
    """Build an entry from a DR-027 Claims, Contributions or Declared starting points row."""
    if table == CLAIMS_TABLE:
        unit_type = says_unit_type(columns.get("says", ""))
        items = _grounds_items(columns.get("grounds", ""))
    elif table == CONTRIBUTIONS_TABLE:
        unit_type = CONTRIBUTION
        items = _grounds_items(columns.get("rests on", ""))
    else:
        unit_type = DECLARED
        items = ()
    # Only a well-formed single ID becomes an edge; anything else is a schema finding.
    claims = [_clean_id(v) for k, v in items if k == "claim" and ENTRY_ID_REGEX.match(_clean_id(v))]
    decls = [_clean_id(v) for k, v in items if k == "decl" and ENTRY_ID_REGEX.match(_clean_id(v))]
    tier = "" if table == DECLARED_TABLE else (columns.get("confidence tier") or columns.get("confidence") or "")
    return Entry(
        entry_id=entry_id,
        unit_type=unit_type,
        tier=tier.strip().upper(),
        verified=bool(_VERIFIED_REGEX.match(columns.get("status", ""))),
        line_number=lineno,
        columns=columns,
        premises=tuple(dict.fromkeys(claims)),
        schema=DR027,
        decls=tuple(dict.fromkeys(decls)),
        items=items,
    )


def _parse_entries(content: str) -> tuple[Entry, ...]:
    """Parse per-type sub-tables into one entry per registry row.

    `tools.coverage` aggregates these to counts; this keeps the row, since
    every check here is about an individual entry's relationships.
    """
    return _walk_registry(content)[0]


def _walk_registry(content: str) -> tuple[tuple[Entry, ...], list[Finding]]:
    """Return (entries, findings for rows with content whose ID matches no pattern).

    Until v5.0.0 a row whose first cell was not `S<n>-<n>` was skipped in
    silence (a `C1` contribution, a `**S1-1**` ID, an `S1.2` typo): it left
    every check while still sitting visibly in the registry. A section divider
    (`| **PART TWO** |`, nothing after its first cell) is the only row skipped.
    """
    entries: list[Entry] = []
    unmatched: list[Finding] = [
        Finding(
            "schema",
            "finding",
            "",
            f"registry line {n}: near-miss marker `{text}` — a known table name in marker shape that is not "
            "a recognised marker, so its table is read by nothing",
        )
        for n, text in near_miss_markers(content)
    ]
    unit_type: str | None = None
    header: list[str] | None = None
    mixed_flagged = False

    def dr027_under_dr004(lineno: int, why: str) -> None:
        nonlocal mixed_flagged
        if not mixed_flagged:
            mixed_flagged = True
            unmatched.append(
                Finding(
                    "schema",
                    "finding",
                    "",
                    f"registry line {lineno}: DR-027 table under a DR-004 marker ({why}) — it is checked under "
                    "DR-004's rules, so none of the DR-027 rules run; use `**Claims:**`",
                )
            )

    for lineno, line in enumerate(content.splitlines(), start=1):
        marker = _MARKER_REGEX.match(line)
        if marker:
            unit_type = marker_kind(marker)
            header = None
            mixed_flagged = False
            continue
        if unit_type is None:
            continue
        if _SEPARATOR_REGEX.match(line):
            continue

        cells = _split_row(line)
        if cells is None:
            # The first line after the marker's table that is not a row ends
            # the marker's reach, as in `tools.coverage`, which reads only the
            # table under a marker. Carrying it on read the template's unmarked
            # `## Out of Scope` / `## Parked` tables as the last marker's type:
            # 19 parked CLAIM rows as ARGUMENTs, 57 schema findings (#50).
            if header is not None:
                unit_type = header = None
            continue
        if header is None:
            header = [c.lower() for c in cells]
            if unit_type in DR004_KINDS:
                dr027_cols = [c for c in ("says", "rests on", "contestedness") if c in header]
                if dr027_cols:
                    dr027_under_dr004(lineno, f"its header has {', '.join(dr027_cols)}")
            continue
        if len(cells) > len(header):
            # As in tools.coverage: GFM discards the excess cells and every
            # column read from this row would shift. Report, never mis-read.
            unmatched.append(
                Finding(
                    "schema",
                    "finding",
                    cells[0][:40],
                    f"registry line {lineno}: row has {len(cells)} cells but the header defines {len(header)} — "
                    "an unescaped `|` (escape it as `\\|`, also inside backticks) shifts every column, so this "
                    "row was NOT checked",
                )
            )
            continue
        if not cells or not ENTRY_ID_REGEX.match(cells[0]):
            if any(cells[1:]):
                # DR-004 tables: a note, so an unmigrated registry keeps its exit
                # code; DR-027 tables: a finding.
                new_table = unit_type in _TABLE_ID_PREFIX
                unmatched.append(
                    Finding(
                        "schema",
                        "finding" if new_table else "note",
                        cells[0][:40],
                        f"registry line {lineno}: row has content but its ID `{cells[0][:40] or '(blank)'}` "
                        "matches no entry-ID pattern (S<n>-<n>, S<n>-<n>a, C<n>, D<n>), so no check reads it",
                    )
                )
            continue

        # strict=False deliberately: a row with fewer cells than its header
        # is a truncated row, and the right response is for the schema check
        # to report the missing columns, not for the tool to raise.
        columns = dict(zip(header, cells, strict=False))
        if unit_type in _TABLE_ID_PREFIX:
            entries.append(_new_schema_entry(cells[0], unit_type, columns, lineno))
            continue
        premise_text = columns.get("premises", "") or columns.get("grounds", "")
        if unit_type in DR004_KINDS and any(_TYPED_ITEM_START.match(i) for i in premise_text.split(";")):
            dr027_under_dr004(lineno, "its Grounds hold typed `src:` / `claim:` / `decl:` / `own:` items")
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
    return tuple(entries), unmatched


def _stray_rows(content: str) -> list[Finding]:
    """Entry rows cut off from their marker's table, which neither this tool nor coverage reads.

    A blank or comment line inside a table ends it, so the rows below are read by
    nothing, and a P0 there drops out of the tier floor in silence. Rows under a
    heading are a deliberately unmarked section (`## Out of Scope`) and are left alone.
    """
    findings: list[Finding] = []
    state = "none"  # "table": inside a marker's table · "after": that table ended, no heading yet
    for lineno, line in enumerate(content.splitlines(), start=1):
        if _MARKER_REGEX.match(line):
            state = "marker"
            continue
        if re.match(r"^ {0,3}#{1,6}(\s|$)", line):
            state = "none"
            continue
        cells = _split_row(line)
        if state == "marker" and cells is not None:
            state = "table"
        elif state == "table" and cells is None:
            state = "after"
        elif state == "after" and cells and ENTRY_ID_REGEX.match(cells[0]):
            findings.append(
                Finding(
                    "schema",
                    "finding",
                    cells[0],
                    f"registry line {lineno}: entry row outside its marker's table (a blank or comment "
                    "line above ends the table), so neither this check nor coverage reads it",
                )
            )
    return findings


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def _read_manuscript(path: Path) -> tuple[str, list[tuple[str, int]], list[str]]:
    r"""Read a manuscript with its `\input` and `\include` files inlined.

    Reading only the main file reported every entry of a multi-file manuscript
    as unanchored: 131 findings for a registry whose anchors were all present
    (#58). Paths resolve against the main file's directory, as LaTeX run there
    resolves them, then against each `\input@path` directory the main file sets
    with `\def` (`\def\input@path{{drafts/}}`); `.tex` is added when the name
    has no suffix. A commented-out command is left alone; one inside `\iffalse`
    or a `comment` environment is not. Not followed: `\subfile`, `\import`,
    `\InputIfFileExists`.

    Returns the expanded text, the (file, line) each of its lines came from,
    and every input that could not be resolved (missing, or a cycle).
    """
    root = path.parent
    found = _INPUT_PATH_REGEX.search(_TEX_COMMENT_REGEX.sub("", path.read_text(encoding="utf-8")))
    dirs = (root, *(root / d for d in re.findall(r"\{([^{}]*)\}", found.group(1)))) if found else (root,)
    lines: list[str] = []
    origins: list[tuple[str, int]] = []
    unresolved: list[str] = []

    def _resolve(name: str) -> Path | None:
        for base in dirs:
            target = base / name
            if not target.suffix:
                target = target.with_suffix(".tex")
            if target.is_file():
                return target
        return None

    def _expand(file: Path, seen: frozenset[Path]) -> None:
        label = file.relative_to(root).as_posix() if file.is_relative_to(root) else str(file)
        for lineno, line in enumerate(file.read_text(encoding="utf-8").split("\n"), start=1):
            cut = _TEX_COMMENT_REGEX.search(line)
            code, comment = (line[: cut.start()], line[cut.start() :]) if cut else (line, "")
            pos = 0
            for m in _INPUT_REGEX.finditer(code):
                name = (m.group(2) or m.group(3)).strip()
                target = _resolve(name)
                if target is None or target.resolve() in seen:
                    why = "not found" if target is None else "a cycle"
                    unresolved.append(f"{label}:{lineno}: \\{m.group(1)}{{{name}}} ({why})")
                    continue
                lines.append(code[pos : m.start()])
                origins.append((label, lineno))
                _expand(target, seen | {target.resolve()})
                pos = m.end()
            # After an `\input`, a lone space keeps a trailing comment off the
            # start of its line, where it would read as an anchor.
            lines.append((code[pos:] or (" " if pos else "")) + comment)
            origins.append((label, lineno))

    _expand(path, frozenset({path.resolve()}))
    return "\n".join(lines), origins, unresolved


_LINE_REF_REGEX = re.compile(r"(?<!registry )\bline (\d+)")


def _relocate(message: str, origins: list[tuple[str, int]]) -> str:
    """Turn "line N" of the expanded text into "line M of file" when inputs were inlined.

    Backticked spans quote the manuscript and are left alone."""

    def _sub(m: re.Match) -> str:
        n = int(m.group(1))
        if not 1 <= n <= len(origins):
            return m.group(0)
        file, line = origins[n - 1]
        return f"line {line} of {file}"

    parts = message.split("`")
    return "`".join(_LINE_REF_REGEX.sub(_sub, p) if k % 2 == 0 else p for k, p in enumerate(parts))


def _decl_anchor_findings(entries: tuple[Entry, ...], manuscript: str) -> list[Finding]:
    """`% D1: label (KIND, CONTESTEDNESS)` must agree with the D row's Kind and Contestedness.

    Compared by first word, case-insensitive, as the schema check reads them
    (`accepted in the field` is `accepted`). An anchor without a two-part
    trailing parenthesis is not compared, and not noted: D anchors carry no tier.
    """
    rows = {e.entry_id: e for e in entries if e.unit_type == DECLARED}
    findings: list[Finding] = []
    for lineno, line in enumerate(manuscript.split("\n"), start=1):
        match = _ANCHOR_LINE_REGEX.match(line)
        if not match or not match.group(1).startswith("D") or match.group(1) not in rows:
            continue
        entry_id, rest = match.groups()
        parts: list[str] = []
        for paren in _ANCHOR_PAREN_REGEX.finditer(rest):
            candidate = [x.strip() for x in paren.group(1).split(",")]
            if len(candidate) == 2 and _AFTER_ANCHOR_PAREN_REGEX.match(rest, paren.end()):
                parts = candidate
                break
        if not parts:
            continue
        row = rows[entry_id]
        for label, column, anchored_value in (("Kind", "kind", parts[0]), ("Contestedness", "contestedness", parts[1])):
            registered_value = row.columns.get(column, "")
            if _first_word(anchored_value) != _first_word(registered_value):
                findings.append(
                    Finding(
                        "anchors",
                        "finding",
                        entry_id,
                        f"manuscript anchor at line {lineno} gives {label} `{anchored_value}`, the registry row "
                        f"`{registered_value.strip() or '(blank)'}` — the copies differ",
                    )
                )
    return findings


def _check_anchors(entries: tuple[Entry, ...], manuscript: str) -> tuple[list[Finding], int]:
    anchored = set(ANCHOR_REGEX.findall(manuscript))
    registered = {e.entry_id for e in entries}
    findings: list[Finding] = _decl_anchor_findings(entries, manuscript)

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
    for lineno, line in enumerate(manuscript.split("\n"), start=1):  # as `_read_manuscript` counts lines
        match = _ANCHOR_LINE_REGEX.match(line)
        if not match:
            continue
        entry_id, rest = match.groups()
        if entry_id.startswith("D"):
            # `% D1: label (value, contested)`: a declared starting point has
            # no tier (DR-027), so there is nothing to compare and nothing to note.
            continue
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


def _schema_dr027(entry: Entry, by_id: dict[str, Entry]) -> list[str]:
    """DR-027 schema rules for one new-schema row; returns the finding messages.

    Presence and form only, never quality: that a Warrant exists, not that it
    licenses the step. Reference resolution is the premises check's job.
    """
    out: list[str] = []
    cols = entry.columns
    eid = entry.entry_id

    if entry.unit_type == DECLARED:
        if not eid.startswith("D"):
            out.append("row in the Declared starting points table has a non-D ID (expected D<n>)")
        kind = _first_word(cols.get("kind", ""))
        if kind not in DECLARED_KINDS:
            out.append(f"Kind is `{cols.get('kind', '').strip() or '(blank)'}`; expected one of {', '.join(DECLARED_KINDS)}")
        contested = _first_word(cols.get("contestedness", ""))
        if contested not in CONTESTEDNESS:
            out.append(
                f"Contestedness is `{cols.get('contestedness', '').strip() or '(blank)'}`; "
                f"expected one of {', '.join(CONTESTEDNESS)}"
            )
        return out

    is_contribution = entry.unit_type == CONTRIBUTION
    label = "contribution" if is_contribution else "claim"
    expected = "C" if is_contribution else "S"
    if not eid.startswith(expected):
        table = "Contributions" if is_contribution else "Claims"
        out.append(f"row in the {table} table has an ID that is not {expected}…")
    says = cols.get("says", "")
    if says_unit_type(says) not in ("DESCRIPTIVE", "NORMATIVE"):
        out.append(f"Says is `{says.strip() or '(blank)'}`; expected descriptive or normative")
    if is_contribution and (cols.get("priority", "") or "").strip().strip("*`_ ").upper() != "P0":
        out.append(
            f"Priority is `{(cols.get('priority') or '').strip() or '(blank)'}`; a contribution is P0 by "
            "definition (DR-027) and counts in the P0 tier floor whatever this cell says"
        )

    grounds_col = "rests on" if is_contribution else "grounds"
    if not entry.items:
        out.append(f"{label} records no **{grounds_col}** — every {label} rests on typed items (DR-027)")
    for kind, value in entry.items:
        if not kind:
            out.append(
                f"{grounds_col} item `{value[:60]}` is untyped — prefix it with `src:`, `claim:`, `decl:` or `own:`"
            )
        elif kind == "own" and not is_contribution:
            if not value:
                out.append("a bare `own:` item names no method or query — write e.g. `own: corpus count, query Q1`")
        elif kind in ("src", "own") and is_contribution:
            out.append(f"Rests on lists `{kind}: {value[:60]}`; a contribution rests on `claim:` and `decl:` items")
        elif kind == "src" and not value:
            out.append("a bare `src:` item names no source")
        elif kind in ("claim", "decl") and not ENTRY_ID_REGEX.match(_clean_id(value)):
            out.append(f"`{kind}: {value[:60]}` does not name a single entry ID")

    if not is_contribution and entry.premises and _missing(cols.get("warrant")):
        out.append("claim rests on other claims (`claim:` grounds) but has no **warrant** to join them")

    if entry.unit_type == "NORMATIVE" or (is_contribution and says_unit_type(says) == "NORMATIVE"):
        bounds = "who/where/when" if is_contribution else "rebuttal"
        if _missing(cols.get(bounds)):
            out.append(f"normative {label} has no **{bounds}** (its boundary conditions, DR-027)")
        values = [
            d
            for d in entry.decls
            if d in by_id and by_id[d].unit_type == DECLARED and _first_word(by_id[d].columns.get("kind", "")) == "value"
        ]
        if not values:
            out.append(f"normative {label} names no declared value — add a `decl:` item whose D-row Kind is value")
    return out


def _check_schema(entries: tuple[Entry, ...]) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    examined = 0
    by_id = {e.entry_id: e for e in entries}
    seen: dict[str, int] = {}
    for entry in entries:
        if entry.entry_id in seen:
            findings.append(
                Finding(
                    "schema",
                    "finding",
                    entry.entry_id,
                    f"duplicate ID: registry lines {seen[entry.entry_id]} and {entry.line_number} — every "
                    "reference to it, and every tier copy, is ambiguous",
                )
            )
        else:
            seen[entry.entry_id] = entry.line_number
    for entry in entries:
        if entry.schema == DR027:
            examined += 1
            findings += [Finding("schema", "finding", entry.entry_id, m) for m in _schema_dr027(entry, by_id)]
            continue
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
        if not entry.premises and not entry.decls:
            continue
        examined += 1
        # DR-027 `decl:` references resolve to a declared starting point; they
        # are not premise-graph edges (a starting point has no tier).
        for decl_id in entry.decls:
            target = by_id.get(decl_id)
            if target is None:
                findings.append(
                    Finding(
                        "premises",
                        "finding",
                        entry.entry_id,
                        f"cites declared starting point `{decl_id}`, which is not in the registry",
                    )
                )
            elif target.unit_type != DECLARED:
                findings.append(
                    Finding(
                        "premises",
                        "finding",
                        entry.entry_id,
                        f"`decl: {decl_id}` names a row that is not a declared starting point — use `claim:`",
                    )
                )
        if not entry.premises:
            continue
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
            if premise.unit_type == DECLARED:
                findings.append(
                    Finding(
                        "premises",
                        "finding",
                        entry.entry_id,
                        f"rests on `{premise_id}` as a claim, but it is a declared starting point — use `decl:`",
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


def _check_glossary(path: Path) -> list[Finding]:
    """DR-028: the paper's glossary exists, is not empty, and is no longer the template.

    Presence only: whether its definitions are right is a reading pass. An
    unreadable file is a finding, not a tooling error, as a missing one is.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [Finding("glossary", "finding", "", f"glossary file not found: {path}")]
    except (OSError, UnicodeDecodeError) as exc:
        return [Finding("glossary", "finding", "", f"glossary file could not be read ({exc.__class__.__name__}): {path}")]
    if not text.strip():
        return [Finding("glossary", "finding", "", f"glossary file is empty: {path}")]
    left = [token for token in GLOSSARY_PLACEHOLDERS if token in text]
    if left:
        return [
            Finding(
                "glossary",
                "finding",
                "",
                "glossary still contains the template's placeholders ("
                + ", ".join(f"`{t}`" for t in left)
                + ") — copied, not filled in",
            )
        ]
    return []


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
    glossary_path: Path | None = None,
) -> RegistryReport:
    """Run every applicable internal-consistency check.

    Args:
        registry_path: path to claim_registry.md
        manuscript_path: optional manuscript; enables the anchor and tier
            checks (and the budget check, which needs a word count)
        budget: optional word budget; requires manuscript_path
        glossary_path: optional paper glossary (DR-028); missing, empty or
            still-template is a finding. Absent, the report says "glossary:
            not checked".

    Raises:
        FileNotFoundError: if a given path does not exist
        ValueError: if the file has no recognised sub-table marker at all —
            nothing was parsed, so that is a failure, not a clean run. A
            freshly started registry (markers over empty tables) is not an
            error; the report says it examined zero entries.
    """
    if not registry_path.is_file():
        raise FileNotFoundError(registry_path)
    content = registry_path.read_text(encoding="utf-8")
    entries, unmatched = _walk_registry(content)
    if not entries and not _has_marker(content):
        # Same rule as tools.coverage, so a freshly started registry passes
        # both tools and a file whose markers are all unrecognised fails both.
        raise ValueError(
            f"no sub-table marker recognised in {registry_path}, so nothing was parsed — "
            "this is a parse failure rather than a clean run"
        )

    findings: list[Finding] = []
    counts: dict = {}
    checks: list[str] = []

    schema_findings, schema_count = _check_schema(entries)
    schema_findings += _stray_rows(content)
    schema_findings += unmatched
    findings += schema_findings
    counts["schema"] = schema_count
    checks.append("schema")

    premise_findings, premise_count = _check_premises(entries)
    findings += premise_findings
    counts["premises"] = premise_count
    checks.append("premises")

    if glossary_path is not None:
        findings += _check_glossary(glossary_path)
        counts["glossary"] = 1
        checks.append("glossary")

    if manuscript_path is not None:
        if not manuscript_path.is_file():
            raise FileNotFoundError(manuscript_path)
        manuscript, origins, unresolved = _read_manuscript(manuscript_path)
        multi_file = len({file for file, _ in origins}) > 1

        anchor_findings, anchor_count = _check_anchors(entries, manuscript)
        # An input that did not resolve hides its anchors: say so, or its rows
        # read as unanchored for the wrong reason.
        anchor_findings += [
            Finding("anchors", "note", "", f"input not read, so its anchors were not seen: {u}") for u in unresolved
        ]
        findings += anchor_findings
        counts["anchors"] = anchor_count
        checks.append("anchors")

        tier_findings, tier_count = _check_tiers(entries, manuscript)
        if multi_file:
            tier_findings = [
                Finding(f.check, f.severity, f.entry_id, _relocate(f.message, origins)) for f in tier_findings
            ]
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
        deprecations=deprecation_notes(content),
        glossary_checked=glossary_path is not None,
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
    p.add_argument(
        "--glossary",
        type=Path,
        default=None,
        help="The paper's glossary (DR-028); missing, empty or still the template is a finding",
    )
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    if args.budget is not None and args.manuscript is None:
        print("error: --budget requires --manuscript", file=sys.stderr)
        return 2
    try:
        report = check_registry(
            args.registry, manuscript_path=args.manuscript, budget=args.budget, glossary_path=args.glossary
        )
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
