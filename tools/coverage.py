"""Coverage reporter for typed claim registries.

Parses a claim_registry.md and computes verification coverage per
(unit_type, axis, bucket). Two axes are supported:

- axis="priority"  — for the DR-027 Claims and Contributions tables, and
                     for DR-004's CLAIM / ARGUMENT / PROPOSITION sub-tables
                     (read through v5.x, deprecated); buckets are P0 / P1 / P2.
                     A Claims row reports as DESCRIPTIVE or NORMATIVE (its
                     Says cell; anything else as UNCLASSIFIED), a Contributions
                     row as CONTRIBUTION.
- axis="provocation_tier" — for PROVOCATION sub-tables; buckets are
                     GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL
                     per DR-010 and DR-014.

Targets apply per axis: `priority_targets` gate P0/P1/P2 coverage;
`provocation_targets` (default None — no numeric targets) optionally
gate the tier axis. Rows whose axis has no configured target are
included in the report but excluded from `meets_targets`.

Separately from coverage, the DR-002 P0 tier floor: every P0 entry must be
SUPPORTED or ESTABLISHED. It is reported apart from the coverage table
(`meets_tier_floor`, not `meets_targets`) because the two answer different
questions — a registry can be 100% verified while most of its P0 entries
sit below the floor, and one combined verdict would hide which failed.
A P0 row with no readable tier fails the floor rather than being skipped.
Every CONTRIBUTION row is in the P0 bucket whatever its Priority cell says: a
contribution is P0 by definition (DR-027), so a mistyped `P1` cannot take it
out of the floor (check_registry reports the non-P0 cell). It enters the
floor at its effective tier: its own, capped by its weakest `claim:` item.

DR-027's Declared starting points table carries no priority and no tier: its
rows are excluded from coverage and the floor and reported apart (count, and
how many are `[x]`). A registry that still uses DR-004's markers gets one
deprecation line in the report; it changes no number and no exit code.

Public API:
    check_coverage(registry_path, *, types=None,
                   priority_targets=None,
                   provocation_targets=None) -> CoverageReport

CLI:
    python -m tools.coverage <registry.md> [--json] [--strict]

Exit codes:
    0  success (and, with --strict, all applicable targets met and the
       P0 tier floor met)
    1  failure (with --strict: a target missed, the P0 tier floor failed,
       an UNCLASSIFIED row or an ID no pattern accepts, or only declared
       starting points found)
    2  tooling error (file missing, parse failure, near-miss marker)

Design notes:
    - Deterministic: same input file → byte-identical report.
    - Zero-dep: stdlib only.
    - No LLM step: registry format is author-controlled markdown.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

PRIORITY_AXIS = "priority"
PROVOCATION_TIER_AXIS = "provocation_tier"

DEFAULT_PRIORITY_TARGETS: dict[str, float] = {
    "P0": 100.0,
    "P1": 90.0,
    "P2": 70.0,
}

# Matches a sub-table marker line. DR-004 (deprecated, read through v5.x):
# **CLAIMs:**, **ARGUMENTs** (Toulmin):, **PROPOSITIONs** (Whetten):.
# DR-010: **PROVOCATIONs** (Auger ...):. DR-027: **Claims:**,
# **Contributions:**, **Declared starting points:**. The DR-027 names are
# case-sensitive as written, so `**CLAIMS:**` stays unrecognised rather than
# being read as a new-schema table.
_MARKER_REGEX = re.compile(
    r"^\s*\*\*\s*"
    r"(CLAIM|ARGUMENT|PROPOSITION|PROVOCATION|Claim|Contribution|Declared starting point)s?"
    r"\s*:?\s*\*\*"
    r"(?:\s+\([^)]+\))?"
    r"\s*:?\s*$"
)

# Table kinds a marker opens. The DR-004 kinds are their own unit types.
CLAIMS_TABLE = "CLAIMS"
CONTRIBUTIONS_TABLE = "CONTRIBUTIONS"
DECLARED_TABLE = "DECLARED_TABLE"
_NEW_MARKERS = {
    "Claim": CLAIMS_TABLE,
    "Contribution": CONTRIBUTIONS_TABLE,
    "Declared starting point": DECLARED_TABLE,
}
DEPRECATED_KINDS = ("CLAIM", "ARGUMENT", "PROPOSITION")
DEPRECATION_NOTE = (
    "uses DR-004 markers (CLAIMs / ARGUMENTs / PROPOSITIONs; deprecated in v5.0.0, "
    "still read until v6.0.0): these rows are checked under DR-004's rules and "
    "reported under their old labels"
)

# Unit types of new-schema rows.
SAYS_VALUES = ("descriptive", "normative")
UNCLASSIFIED = "UNCLASSIFIED"
CONTRIBUTION = "CONTRIBUTION"
DECLARED = "DECLARED"
DECLARED_AXIS = "declared"


def marker_kind(match: re.Match) -> str:
    """The table kind a `_MARKER_REGEX` match opens: a DR-004/DR-010 unit type
    (`CLAIM`, `ARGUMENT`, `PROPOSITION`, `PROVOCATION`) or a DR-027 table kind."""
    raw = match.group(1)
    return _NEW_MARKERS.get(raw, raw.upper())


def says_unit_type(raw: str) -> str:
    """DESCRIPTIVE / NORMATIVE from a Says cell; UNCLASSIFIED for anything else."""
    value = raw.strip().strip("*`_ ").lower()
    return value.upper() if value in SAYS_VALUES else UNCLASSIFIED


# A marker-shaped line with a known name in the wrong case or form
# (`**CONTRIBUTIONS:**`, `### **CLAIMs:**`, `**claims**`). Until v5.0.0 such a
# line dropped its table in silence whenever another marker in the file was
# recognised. Shape only: bold prose like `**Claims with a Warrant**` is not one,
# and neither is a marker-shaped label with no table under it (`near_miss_markers`).
_NEAR_MISS_REGEX = re.compile(
    r"^ {0,3}(?:#{1,6}\s*)?\*\*\s*"
    r"(?:claims?|arguments?|propositions?|provocations?|contributions?|declared\s+starting\s+points?)"
    r"\s*(?:\([^)]*\))?\s*:?\s*\*\*"
    r"(?:\s*\([^)]*\))?"
    r"\s*:?\s*$",
    re.IGNORECASE,
)


_NEAR_MISS_LOOKAHEAD = 3


def near_miss_markers(content: str) -> list[tuple[int, str]]:
    """(line number, line) for every unquoted near-miss marker: a known table name
    in marker shape that `_MARKER_REGEX` does not accept, with a table row (`|`)
    within the next three non-blank lines. That table would be read by nothing.
    A label with no table under it (`**Arguments**`, `**Claim (S1-1):**`) is prose.
    Quoted lines (fences, HTML comments) and 4-space-indented code are examples."""
    lines = content.splitlines()
    quoted = _quoted_lines(lines)
    found: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if quoted[i] or not _NEAR_MISS_REGEX.match(line) or _MARKER_REGEX.match(line):
            continue
        following = [nxt for nxt in lines[i + 1 :] if nxt.strip()][:_NEAR_MISS_LOOKAHEAD]
        for nxt in following:
            if _MARKER_REGEX.match(nxt):
                break  # the table below belongs to that recognised marker
            if nxt.lstrip().startswith("|"):
                found.append((i + 1, line.strip()))
                break
    return found


def has_dr027_marker(content: str) -> bool:
    """Whether any line opens a DR-027 table (Claims, Contributions, Declared)."""
    return any(
        m and marker_kind(m) in (CLAIMS_TABLE, CONTRIBUTIONS_TABLE, DECLARED_TABLE)
        for m in map(_MARKER_REGEX.match, content.splitlines())
    )


def deprecation_notes(content: str) -> tuple[str, ...]:
    """One note if any marker the parser reads is a deprecated DR-004 marker.

    Every marker line counts, as the parser reads every one (quoting only
    informs the zero-rows guard). The note never changes a number or an exit code.
    """
    for line in content.splitlines():
        m = _MARKER_REGEX.match(line)
        if m and marker_kind(m) in DEPRECATED_KINDS:
            return (DEPRECATION_NOTE,)
    return ()


_FENCE_REGEX = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def _quoted_lines(lines: list[str]) -> list[bool]:
    """True for each line inside a fenced code block or an HTML comment.

    Used ONLY by `_has_marker`, i.e. only to decide whether a file that parsed
    to zero rows had any real marker at all. It deliberately does not affect
    row parsing: a heuristic that decided what counts would, on a `<!--`
    inside a table cell, hide every marker below it and drop real rows
    (measured in review 2026-09-26). Here the worst a misreading can do is
    change the wording of an error on a file that counted nothing.
    """
    quoted: list[bool] = []
    fence: str | None = None
    in_comment = False
    for line in lines:
        if fence is not None:
            quoted.append(True)
            close = _FENCE_REGEX.match(line)
            # CommonMark: a closing fence uses the same character, is at least
            # as long as the opener, and carries no info string.
            if (
                close
                and close.group(1)[0] == fence[0]
                and len(close.group(1)) >= len(fence)
                and not close.group(2).strip()
            ):
                fence = None
            continue
        if in_comment:
            quoted.append(True)
            in_comment = "-->" not in line
            continue
        opener = _FENCE_REGEX.match(line)
        if opener and not (opener.group(1)[0] == "`" and "`" in opener.group(2)):
            fence = opener.group(1)
            quoted.append(True)
            continue
        # The comment state at the end of the line decides the next one:
        # `--> ... <!--` reopens, `<!-- ... -->` closes.
        opens, closes = line.rfind("<!--"), line.rfind("-->")
        in_comment = opens != -1 and opens > closes
        quoted.append(in_comment)
    return quoted


def _has_marker(content: str) -> bool:
    """Whether any unquoted line is a sub-table marker."""
    lines = content.splitlines()
    return any(not q and _MARKER_REGEX.match(line) for line, q in zip(lines, _quoted_lines(lines), strict=True))


_SEPARATOR_REGEX = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
_STATUS_VERIFIED_REGEX = re.compile(r"^\s*\[\s*x\s*\]", re.IGNORECASE)
_ENTRY_ID_REGEX = re.compile(r"^\W*(?:S\d+-\d+[a-z]?|[CD]\d+)\W*$")
# DR-004 and PROVOCATION tables keep master's patterns exactly (alias parity).
_DR004_ENTRY_ID_REGEX = re.compile(r"^\W*S\d+-\d+\W*$")
DR004_STRICT_ID_REGEX = re.compile(r"^S\d+-\d+$")
DR027_UNIT_TYPES = ("DESCRIPTIVE", "NORMATIVE", "UNCLASSIFIED", "CONTRIBUTION", "DECLARED")
# An entry ID exactly as both tools accept it (no decoration): S2-3, S2-3a, C1, D1.
STRICT_ID_REGEX = re.compile(r"^(?:S\d+-\d+[a-z]?|[CD]\d+)$")
# A `claim:` item naming one ID, in a Rests-on cell.
_CLAIM_ITEM_REGEX = re.compile(r"^\s*claim\s*:\s*[*`_ ]*(S\d+-\d+[a-z]?|C\d+)[*`_ ]*\s*$", re.IGNORECASE)
_CLAIM_PREFIX_REGEX = re.compile(r"^\s*claim\s*:\s*(.*)$", re.IGNORECASE)
_TIER_ORDER = ("ESTABLISHED", "SUPPORTED", "EMERGING", "SPECULATIVE")

# DR-002: "all SUPPORTED or ESTABLISHED (no EMERGING/SPECULATIVE)".
P0_TIER_FLOOR = ("ESTABLISHED", "SUPPORTED")


def _normalise_tier(raw: str) -> str:
    """Strip cell decoration (`**`, backticks, `⚠`, a parenthetical) and upper-case.

    Kept equivalent to `tools.check_registry._normalise_tier` by hand rather
    than imported: check_registry already imports from this module, and the
    reverse import would make the two modules circular.
    """
    out = raw.strip()
    for ch in ("*", "`", "_", "⚠", "~"):
        out = out.replace(ch, "")
    if "(" in out:
        out = out.split("(", 1)[0]
    return out.strip().upper()


@dataclass(frozen=True)
class _RegistryRow:
    unit_type: str
    axis: str
    bucket: str
    status: str
    entry_id: str
    tier: str
    refs: tuple[str, ...] = ()  # a contribution's `claim:` Rests-on IDs
    bad_refs: tuple[str, ...] = ()  # `claim:` items that are not exactly one S/C ID


@dataclass(frozen=True)
class CoverageRow:
    # DESCRIPTIVE | NORMATIVE | UNCLASSIFIED | CONTRIBUTION (DR-027);
    # CLAIM | ARGUMENT | PROPOSITION (DR-004, deprecated) | PROVOCATION
    unit_type: str
    axis: str  # PRIORITY_AXIS | PROVOCATION_TIER_AXIS
    bucket: str  # P0/P1/P2 or GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL
    total: int
    verified: int

    @property
    def percent(self) -> float:
        return 100.0 * self.verified / self.total if self.total else 0.0


@dataclass(frozen=True)
class CoverageReport:
    registry_path: Path
    rows: tuple[CoverageRow, ...]
    priority_targets: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_PRIORITY_TARGETS))
    provocation_targets: dict[str, float] | None = None
    # (entry_id, raw Confidence cell) for every priority-axis P0 row.
    p0_tiers: tuple[tuple[str, str], ...] = ()
    # DR-027 Declared starting points: rows, and rows marked [x]. Not coverage.
    declared_total: int = 0
    declared_verified: int = 0
    deprecations: tuple[str, ...] = ()
    # Rows --strict refuses to pass over: a Says that is neither descriptive
    # nor normative, and an ID no pattern accepts.
    unclassified: tuple[str, ...] = ()
    unmatched_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    # Only Declared rows were found: nothing coverage or the floor could evaluate.
    evaluated_nothing: bool = False
    # (contribution ID, effective-tier text) — why each contribution sits where it does.
    effective_tiers: tuple[tuple[str, str], ...] = ()

    @property
    def passes_strict(self) -> bool:
        """What --strict requires: targets met, floor met, every row classifiable."""
        return (
            self.meets_targets
            and self.meets_tier_floor
            and not self.unclassified
            and not self.unmatched_ids
            and not self.evaluated_nothing
        )

    @property
    def p0_ids(self) -> tuple[str, ...]:
        """Distinct P0 entry IDs. The floor counts entries, not rows — an ID
        registered in two sub-tables is one entry."""
        return tuple(dict.fromkeys(eid for eid, _ in self.p0_tiers))

    @property
    def p0_below_floor(self) -> tuple[str, ...]:
        """P0 IDs with any copy not SUPPORTED/ESTABLISHED, including unreadable ones."""
        return tuple(dict.fromkeys(eid for eid, tier in self.p0_tiers if _normalise_tier(tier) not in P0_TIER_FLOOR))

    @property
    def meets_tier_floor(self) -> bool:
        """True iff every P0 entry is SUPPORTED or ESTABLISHED.

        Vacuously True when no P0 entry was parsed (a PROVOCATION-only registry
        legitimately has none); the report then says NOT evaluated rather than
        "meets", and the JSON carries `evaluated: false`.
        """
        return not self.p0_below_floor

    def _unknown_priority_bucket(self, row: CoverageRow) -> bool:
        """A priority bucket that is neither P0/P1/P2 nor a configured target.

        `-`, `TBD` or `P9` in a Priority cell used to become its own untargeted
        bucket, so overwriting a claim's `P0` passed --strict exactly as
        blanking it did (review 2026-09-26). Custom targets stay valid.
        """
        return (
            row.axis == PRIORITY_AXIS
            and row.bucket not in DEFAULT_PRIORITY_TARGETS
            and row.bucket not in self.priority_targets
        )

    def _target_for(self, row: CoverageRow) -> float | None:
        if row.axis == PRIORITY_AXIS:
            return self.priority_targets.get(row.bucket)
        if row.axis == PROVOCATION_TIER_AXIS:
            if self.provocation_targets is None:
                return None
            return self.provocation_targets.get(row.bucket)
        return None

    def to_dict(self) -> dict:
        return {
            "registry_path": self.registry_path.name,
            "rows": [asdict(r) | {"percent": r.percent, "target": self._target_for(r)} for r in self.rows],
            "priority_targets": dict(self.priority_targets),
            "provocation_targets": (None if self.provocation_targets is None else dict(self.provocation_targets)),
            "meets_targets": self.meets_targets,
            "p0_tier_floor": {
                "floor": list(P0_TIER_FLOOR),
                "evaluated": bool(self.p0_ids),
                "total": len(self.p0_ids),
                "meeting": len(self.p0_ids) - len(self.p0_below_floor),
                "below_floor": list(self.p0_below_floor),
                "meets": self.meets_tier_floor,
            },
            "declared_starting_points": {
                "total": self.declared_total,
                "verified": self.declared_verified,
            },
            "deprecations": list(self.deprecations),
            "unclassified": list(self.unclassified),
            "unmatched_ids": list(self.unmatched_ids),
            "notes": list(self.notes),
            "evaluated_nothing": self.evaluated_nothing,
            "contribution_effective_tiers": {eid: text for eid, text in self.effective_tiers},
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Coverage report — {self.registry_path.name}",
            "",
            "| Unit Type | Axis | Bucket | Total | Verified | % | Target | Meets |",
            "|-----------|------|--------|-------|----------|---|--------|-------|",
        ]
        for row in self.rows:
            target = self._target_for(row)
            if self._unknown_priority_bucket(row):
                meets = "NO — not a priority"
            else:
                meets = "—" if target is None else ("yes" if row.percent >= target else "NO")
            target_str = "—" if target is None else f"{target:.0f}%"
            lines.append(
                f"| {row.unit_type} | {row.axis} | {row.bucket} | {row.total} "
                f"| {row.verified} | {row.percent:.0f}% | {target_str} | {meets} |"
            )
        lines.append("")
        lines.append(self._tier_floor_line())
        for eid, text in self.effective_tiers:
            lines.append("")
            lines.append(f"{eid}: effective {text}")
        if self.declared_total:
            lines.append("")
            lines.append(
                f"Declared starting points (DR-027): {self.declared_total}, of which "
                f"{self.declared_verified} marked [x]. Excluded from coverage and the P0 tier floor."
            )
        if self.unclassified:
            lines.append("")
            lines.append(
                f"Unclassified rows: {len(self.unclassified)} ({', '.join(self.unclassified)}) — Says is "
                "neither descriptive nor normative; --strict fails."
            )
        if self.unmatched_ids:
            lines.append("")
            lines.append(
                f"Rows whose ID matches no pattern (S<n>-<n>, S<n>-<n>a, C<n>, D<n>): {len(self.unmatched_ids)} "
                f"({', '.join(self.unmatched_ids)}); --strict fails."
            )
        if self.evaluated_nothing:
            lines.append("")
            lines.append(
                "Nothing evaluated: the registry holds only declared starting points, which coverage and "
                "the P0 tier floor exclude; --strict fails."
            )
        for note in self.notes:
            lines.append("")
            lines.append(f"Note: {note}.")
        for note in self.deprecations:
            lines.append("")
            lines.append(f"Deprecation: this registry {note}.")
        return "\n".join(lines) + "\n"

    def _tier_floor_line(self) -> str:
        if not self.p0_ids:
            # Vacuously met, and said so: "0 of 0 meet it — meets" reads as a pass.
            return (
                "P0 tier floor (SUPPORTED or ESTABLISHED, DR-002): NOT evaluated — no P0 entries were "
                "parsed. If this registry has P0 entries, the parser did not find them."
            )
        total = len(self.p0_ids)
        below = self.p0_below_floor
        line = (
            f"P0 tier floor (SUPPORTED or ESTABLISHED, DR-002): {total - len(below)} of {total} "
            f"meet it — {'meets' if not below else 'FAILS'}"
        )
        if below:
            line += f"; below the floor: {', '.join(below)}"
        return line + ". Reported separately from the coverage table above, which counts Status only."

    @property
    def meets_targets(self) -> bool:
        """True iff no row with a configured target falls below it.

        Rows whose axis has no configured target are excluded from the
        check (not treated as silent pass — they are reported and
        skipped). Configure `provocation_targets` to gate the
        PROVOCATION tier axis. A priority-axis row in an unrecognised
        bucket is the exception: it FAILS, because on that axis an
        untargeted bucket is a mistyped or overwritten Priority cell.
        """
        for row in self.rows:
            if self._unknown_priority_bucket(row):
                return False
            target = self._target_for(row)
            if target is not None and row.percent < target:
                return False
        return True


def _split_row(line: str) -> list[str] | None:
    """Split a markdown table row into stripped cell values.

    Returns None when the line is not a table row (no leading `|`).
    Tolerates trailing whitespace and missing trailing `|`.

    Honors backslash-escaped pipes (``\\|``) inside cells — common in
    magnitude notation like ``|H(z)|`` — so they do not split the row into
    spurious columns (which silently shifts the bucket/status columns and
    corrupts coverage counts). The escaped pipe is restored as a literal
    ``|`` in the returned cell value.
    """
    stripped = line.rstrip()
    if not stripped.lstrip().startswith("|"):
        return None
    inner = stripped.lstrip()[1:]
    sentinel = "\x00"
    inner = inner.replace("\\|", sentinel)
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip().replace(sentinel, "|") for c in inner.split("|")]


def _find_bucket_and_status_columns(header: list[str], unit_type: str) -> tuple[int, str, int] | None:
    """Return (bucket_col_index, axis, status_col_index) or None if not found.

    PROVOCATION sub-tables prefer the Tier-axis column. The match must
    be tight because PROVOCATION rows may also carry a `Source Tier`
    column inherited from the CLAIM / ARGUMENT / PROPOSITION sub-tables;
    a naive substring match on "tier" would silently bucket against the
    wrong column. We require the column name to start with "tier" (so
    "Source Tier" — which starts with "source" — is excluded), then one
    containing both "provocation" and "tier", and fall back to a name
    containing "provocation" only when neither exists: a
    `| ID | Provocation | Tier |` or `| ID | Provocation | Provocation tier |`
    header holds the text in "Provocation" (#39).
    """
    bucket_col: int | None = None
    bucket_axis: str | None = None
    status_col: int | None = None

    if unit_type == "PROVOCATION":
        names = [name.lower().strip() for name in header]
        for match in (
            lambda n: n.startswith("tier"),
            lambda n: "provocation" in n and "tier" in n,
            lambda n: "provocation" in n,
        ):
            idx = next((i for i, n in enumerate(names) if match(n)), None)
            if idx is not None:
                bucket_col, bucket_axis = idx, PROVOCATION_TIER_AXIS
                break

    if bucket_col is None:
        for idx, name in enumerate(header):
            if name.lower().strip() == "priority":
                bucket_col, bucket_axis = idx, PRIORITY_AXIS
                break

    for idx, name in enumerate(header):
        if name.lower().strip() == "status":
            status_col = idx
            break

    if bucket_col is None or status_col is None or bucket_axis is None:
        return None
    return bucket_col, bucket_axis, status_col


def _parse_registry(content: str) -> dict[tuple[str, str, str], tuple[int, int]]:
    """Walk the registry; return {(unit_type, axis, bucket): (total, verified)}."""
    counts: dict[tuple[str, str, str], list[int]] = {}
    for row in _iter_registry_rows(content):
        if row.axis == DECLARED_AXIS:
            continue  # reported apart, never coverage (DR-027)
        # A blank Status is an entry nobody has verified: it stays in the
        # denominator. Until 2026-09-26 it was skipped, so blanking a Status
        # cell raised coverage.
        slot = counts.setdefault((row.unit_type, row.axis, row.bucket), [0, 0])
        slot[0] += 1
        if _STATUS_VERIFIED_REGEX.match(row.status):
            slot[1] += 1
    return {k: (v[0], v[1]) for k, v in counts.items()}


def _find_column(header: list[str], name: str) -> int | None:
    return next((idx for idx, cell in enumerate(header) if cell.lower().strip() == name), None)


def _iter_registry_rows(content: str) -> Iterator[_RegistryRow]:
    """Walk the registry's typed sub-tables, yielding one record per counted row."""

    def registry_line_no(idx: int) -> str:
        return f"line {idx + 1}"

    lines = content.splitlines()
    i = 0
    while i < len(lines):
        marker = _MARKER_REGEX.match(lines[i])
        if not marker:
            i += 1
            continue

        unit_type = marker_kind(marker)
        marker_line = i
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1

        # A marker whose table cannot be read used to be skipped in silence,
        # dropping every row under it from coverage AND the P0 tier floor —
        # so renaming one `Priority` header made `--strict` exit 0 on a
        # registry whose floor genuinely fails (measured 2026-09-26). A
        # marker promises a sub-table; one that is not there is a parse
        # failure, not an empty sub-table.
        header = _split_row(lines[i]) if i < len(lines) else None
        if header is None:
            raise ValueError(
                f"{registry_line_no(marker_line)}: sub-table marker "
                f"{lines[marker_line].strip()!r} is not followed by a table — its rows "
                "would be dropped from coverage and the P0 tier floor. Put the table "
                "directly under the marker (prose goes above it)."
            )

        cols: tuple[int, str, int] | None
        if unit_type == DECLARED_TABLE:
            status_col = _find_column(header, "status")
            if status_col is None:
                raise ValueError(
                    f"{registry_line_no(i)}: the Declared starting points table's header has no "
                    "Status column, so its rows cannot be reported. Header: "
                    f"{lines[i].strip()[:120]}"
                )
            cols = (status_col, DECLARED_AXIS, status_col)
        else:
            cols = _find_bucket_and_status_columns(header, unit_type)
        if cols is None:
            raise ValueError(
                f"{registry_line_no(i)}: the {unit_type} sub-table's header has no "
                f"{'Tier or ' if unit_type == 'PROVOCATION' else ''}Priority column or no "
                "Status column, so none of its rows can be counted — they would be dropped "
                f"from coverage and the P0 tier floor. Header: {lines[i].strip()[:120]}"
            )
        bucket_col, axis, status_col = cols
        id_col = _find_column(header, "id")
        tier_col = _find_column(header, "confidence")
        says_col = _find_column(header, "says")
        rests_col = _find_column(header, "rests on")
        if unit_type in (CLAIMS_TABLE, CONTRIBUTIONS_TABLE) and tier_col is None:
            tier_col = _find_column(header, "confidence tier")

        i += 1
        if i < len(lines) and _SEPARATOR_REGEX.match(lines[i]):
            i += 1

        while i < len(lines):
            row = _split_row(lines[i])
            if row is None:
                break
            if len(row) > len(header):
                # GFM DISCARDS the excess cells, so this row loses data when
                # rendered AND shifts every column index we read below. The
                # usual cause is an unescaped `|` inside a cell — including
                # inside backticks, because GFM splits a row into cells BEFORE
                # it parses inline content. Refuse rather than mis-parse: a
                # shifted read is silent, and it has been measured to move a
                # P0 claim into an invented bucket where `--strict` then
                # reports 100% P0 over nothing. Escape it as `\|`.
                raise ValueError(
                    f"{registry_line_no(i)}: table row has {len(row)} cells but "
                    f"the header defines {len(header)} — the excess is discarded "
                    f"when rendered and shifts every column read from this row. "
                    f"An unescaped '|' inside a cell is the usual cause "
                    f"(escape it as '\\|'), including inside backticks. Row: "
                    f"{lines[i].strip()[:120]}"
                )
            if len(row) < len(header):
                # GFM PADS a short row with empty cells and renders it as
                # intended, so this is not corruption — a section divider like
                # `| **PART ONE** |` inside a wide table is idiomatic. Pad to
                # match, and let the empty-bucket test below skip it.
                # Breaking here instead (the behaviour until 2026-09-14) ended
                # the table at the first divider and silently dropped every
                # row after it from the counts, so a P0 claim could leave the
                # denominator and `--strict` pass over what remained.
                row = row + [""] * (len(header) - len(row))
            if axis == DECLARED_AXIS:
                # A divider (first cell only, not an ID) or an empty row is not
                # a starting point; anything else is counted, never dropped.
                first = row[0 if id_col is None else id_col]
                if any(row[1:]) or (first and _ENTRY_ID_REGEX.match(first)):
                    yield _RegistryRow(DECLARED, DECLARED_AXIS, "", row[status_col], first, "")
                i += 1
                continue
            if unit_type == CONTRIBUTIONS_TABLE:
                # P0 by definition (DR-027): the written cell does not move it out
                # of the P0 bucket (check_registry reports a cell that is not P0).
                first = row[0 if id_col is None else id_col]
                if not any(row[1:]) and not _ENTRY_ID_REGEX.match(first):
                    i += 1
                    continue
                refs: list[str] = []
                bad: list[str] = []
                for item in [] if rests_col is None else row[rests_col].split(";"):
                    if not _CLAIM_PREFIX_REGEX.match(item):
                        continue
                    good = _CLAIM_ITEM_REGEX.match(item)
                    (refs if good else bad).append(good.group(1) if good else _CLAIM_PREFIX_REGEX.match(item).group(1))
                yield _RegistryRow(
                    CONTRIBUTION,
                    axis,
                    "P0",
                    row[status_col],
                    first,
                    "" if tier_col is None else row[tier_col],
                    tuple(dict.fromkeys(refs)),
                    tuple(bad),
                )
                i += 1
                continue
            bucket = row[bucket_col]
            if axis == PRIORITY_AXIS:
                # `p0` and `**P0**` are P0 — the same reading the P0 tier floor
                # uses, so coverage and the floor cannot disagree about a cell.
                bucket = _normalise_tier(bucket)
            status = row[status_col]
            # A section divider (`| **PART TWO** |`) is the only row allowed to
            # lack a bucket: nothing after its first cell, and that cell not an
            # entry ID. Any other row without one is an entry whose Priority
            # was blanked — including one blanked down to its ID, at any width
            # (`| S2-1 |`, `| S2-1 | | | |`) — and skipping it took an unverified
            # claim out of the count while it still sat visibly in the registry
            # (docs/verification-hooks.md, measured 2026-09-26). A blank Status
            # is not skipped either: `_parse_registry` counts it as unverified.
            if not bucket:
                first = row[0 if id_col is None else id_col]
                id_regex = _ENTRY_ID_REGEX if unit_type == CLAIMS_TABLE else _DR004_ENTRY_ID_REGEX
                is_divider = not any(row[1:]) and not id_regex.match(first)
                if not is_divider:
                    raise ValueError(
                        f"{registry_line_no(i)}: row has content but no "
                        f"{'Tier' if axis == PROVOCATION_TIER_AXIS else 'Priority'} — it cannot be "
                        "counted, and skipping it would drop an entry from coverage and the P0 "
                        f"tier floor. Row: {lines[i].strip()[:120]}"
                    )
                i += 1
                continue
            if unit_type == CLAIMS_TABLE:
                row_type = says_unit_type("" if says_col is None else row[says_col])
            else:
                row_type = unit_type
            yield _RegistryRow(
                unit_type=row_type,
                axis=axis,
                bucket=bucket,
                status=status,
                entry_id=row[0 if id_col is None else id_col],
                tier="" if tier_col is None else row[tier_col],
            )
            i += 1


def check_coverage(
    registry_path: Path,
    *,
    types: tuple[str, ...] | None = None,
    priority_targets: dict[str, float] | None = None,
    provocation_targets: dict[str, float] | None = None,
) -> CoverageReport:
    """Parse a claim registry and return a CoverageReport.

    Args:
        registry_path: path to claim_registry.md
        types: optional filter, e.g. ("CLAIM", "ARGUMENT"). When set, only
            sub-tables whose unit_type appears in the tuple are counted.
            None (default) includes all sub-table types found.
        priority_targets: override default P0/P1/P2 targets
        provocation_targets: per-tier targets for PROVOCATION rows; None
            (default) means PROVOCATION rows are reported but not gated

    Raises:
        FileNotFoundError: if registry_path does not exist
    """
    if not registry_path.is_file():
        raise FileNotFoundError(registry_path)

    content = registry_path.read_text(encoding="utf-8")
    counts = _parse_registry(content)
    if not counts and not _has_marker(content):
        # No recognised marker at all is what an unrecognised one reduces to
        # (`**CLAIMS:**`, `### **CLAIMs:**`): before this, --strict passed over
        # it with the P0 floor "NOT evaluated". Recognised markers over empty
        # tables are different — a freshly started registry, which the README
        # bootstrap creates — and report zero rows without error. (A marker
        # whose table is missing or malformed already raised above.)
        raise ValueError(
            f"no sub-table marker recognised in {registry_path}, so nothing was counted — "
            "this is a parse failure rather than a clean run. Sub-table markers must read "
            "exactly like `**Claims:**` (or DR-004's `**CLAIMs:**`) on their own line."
        )
    near = near_miss_markers(content)
    listed = "; ".join(f"line {n}: `{text}`" for n, text in near)
    dr027 = has_dr027_marker(content)
    if near and dr027:
        raise ValueError(
            f"near-miss marker {listed} — a known table name in marker shape that is not a recognised "
            "marker, so its table would be dropped from coverage and the P0 tier floor. Write it exactly "
            "as `**Claims:**`, `**Contributions:**`, `**Declared starting points:**` (or DR-004's `**CLAIMs:**`)."
        )
    all_rows = tuple(_iter_registry_rows(content))
    effective = {r.entry_id: _effective_tier(r, all_rows) for r in all_rows if r.unit_type == CONTRIBUTION}
    p0_tiers = tuple(
        (row.entry_id, effective[row.entry_id] if row.unit_type == CONTRIBUTION else row.tier)
        for row in all_rows
        if row.axis == PRIORITY_AXIS
        # `**P0**` is still P0: an undecorated compare would drop it from the floor.
        # A contribution is always in the P0 bucket (DR-027).
        and _normalise_tier(row.bucket) == "P0"
        and (types is None or row.unit_type in {t.upper() for t in types})
    )
    declared = [row for row in all_rows if row.axis == DECLARED_AXIS]
    unclassified = tuple(dict.fromkeys(r.entry_id for r in all_rows if r.unit_type == UNCLASSIFIED))
    # DR-027 tables: an ID no pattern accepts is counted and fails --strict.
    # DR-004 and PROVOCATION tables: a note only, so their exit code stays master's.
    unmatched = tuple(
        dict.fromkeys(
            r.entry_id or "(blank)"
            for r in all_rows
            if r.unit_type in DR027_UNIT_TYPES and not STRICT_ID_REGEX.match(r.entry_id)
        )
    )
    old_unmatched = tuple(
        dict.fromkeys(
            r.entry_id or "(blank)"
            for r in all_rows
            if r.unit_type not in DR027_UNIT_TYPES and not DR004_STRICT_ID_REGEX.match(r.entry_id)
        )
    )
    notes: list[str] = []
    if near:
        # Only reached in a registry with no DR-027 marker: a note, never an exit code.
        notes.append(f"near-miss marker {listed} — its table is read by nothing")
    if old_unmatched:
        notes.append(
            f"DR-004/PROVOCATION rows whose ID is not S<n>-<n>: {len(old_unmatched)} "
            f"({', '.join(old_unmatched)}); counted above, never read by check_registry"
        )
    if dr027 and not any(r.unit_type == CONTRIBUTION for r in all_rows):
        notes.append(
            "no contributions registered — a DR-027 registry names its contribution (C1…) as a P0 root "
            "claim, and the P0 tier floor covers it"
        )
    evaluated_nothing = bool(declared) and not any(r.axis != DECLARED_AXIS for r in all_rows)

    if types is not None:
        wanted = tuple(t.upper() for t in types)
        counts = {k: v for k, v in counts.items() if k[0] in wanted}

    rows = tuple(
        CoverageRow(unit_type=k[0], axis=k[1], bucket=k[2], total=v[0], verified=v[1])
        for k, v in sorted(counts.items())
    )

    return CoverageReport(
        registry_path=registry_path,
        rows=rows,
        priority_targets=(dict(DEFAULT_PRIORITY_TARGETS) if priority_targets is None else dict(priority_targets)),
        provocation_targets=(None if provocation_targets is None else dict(provocation_targets)),
        p0_tiers=p0_tiers,
        declared_total=len(declared),
        declared_verified=sum(1 for row in declared if _STATUS_VERIFIED_REGEX.match(row.status)),
        deprecations=deprecation_notes(content),
        unclassified=unclassified,
        unmatched_ids=unmatched,
        notes=tuple(notes),
        evaluated_nothing=evaluated_nothing,
        effective_tiers=tuple(
            (eid, text) for eid, text in effective.items() if types is None or CONTRIBUTION in {t.upper() for t in types}
        ),
    )


def _effective_tier(row: _RegistryRow, all_rows: tuple[_RegistryRow, ...]) -> str:
    """A contribution's tier for the P0 floor: its own, capped by its weakest `claim:` item.

    DR-027: a contribution's tier is no higher than its weakest supporting claim,
    so `--strict` alone fails a contribution resting on an EMERGING claim. A
    referenced claim that is missing or has no readable tier makes the result
    unreadable, which fails the floor rather than being skipped. Direct items
    only; check_registry runs monotonicity over the whole graph.
    """
    tiers: dict[str, list[str]] = {}
    for other in all_rows:
        if other.axis == PRIORITY_AXIS:
            tiers.setdefault(other.entry_id, []).append(_normalise_tier(other.tier))
    own = _normalise_tier(row.tier)
    if own not in _TIER_ORDER:
        return f"UNREADABLE (own tier `{row.tier.strip() or 'blank'}` is not a confidence tier)"
    if row.bad_refs:
        return f"UNREADABLE (Rests-on item `claim: {row.bad_refs[0]}` is not exactly one S/C ID)"
    worst, worst_id = _TIER_ORDER.index(own), ""
    for ref in row.refs:
        copies = tiers.get(ref)
        if not copies:
            return f"UNREADABLE (rests on {ref}, which is not a registered claim)"
        for tier in copies:
            if tier not in _TIER_ORDER:
                return f"UNREADABLE (rests on {ref}, whose tier is unreadable)"
            if _TIER_ORDER.index(tier) > worst:
                worst, worst_id = _TIER_ORDER.index(tier), ref
    if not worst_id:
        return f"{own} (own; no weaker claim)"
    return f"{_TIER_ORDER[worst]} (weakest claim {worst_id}; own {own})"


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.coverage",
        description="Coverage reporter for typed claim registries.",
    )
    p.add_argument("registry", type=Path, help="Path to claim_registry.md")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any configured target is missed, the P0 tier floor fails, a row is "
        "unclassified or has an unmatched ID, or only declared starting points were found",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    try:
        report = check_coverage(args.registry)
    except FileNotFoundError as exc:
        print(f"error: registry file not found: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(report.to_markdown())

    if args.strict and not report.passes_strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
