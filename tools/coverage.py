"""Coverage reporter for typed claim registries.

Parses a claim_registry.md and computes verification coverage per
(unit_type, axis, bucket). Two axes are supported:

- axis="priority"  — for CLAIM / ARGUMENT / PROPOSITION sub-tables;
                     buckets are P0 / P1 / P2.
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

Public API:
    check_coverage(registry_path, *, types=None,
                   priority_targets=None,
                   provocation_targets=None) -> CoverageReport

CLI:
    python -m tools.coverage <registry.md> [--json] [--strict]

Exit codes:
    0  success (and, with --strict, all applicable targets met and the
       P0 tier floor met)
    1  failure (with --strict, a target missed or the P0 tier floor failed)
    2  tooling error (file missing, parse failure)

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

# Matches a sub-table marker line: **CLAIMs:**, **ARGUMENTs** (Toulmin):,
# **PROPOSITIONs** (Whetten):, **PROVOCATIONs** (Auger ...):
_MARKER_REGEX = re.compile(
    r"^\s*\*\*\s*"
    r"(CLAIM|ARGUMENT|PROPOSITION|PROVOCATION)s?"
    r"\s*:?\s*\*\*"
    r"(?:\s+\([^)]+\))?"
    r"\s*:?\s*$"
)

_SEPARATOR_REGEX = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
_STATUS_VERIFIED_REGEX = re.compile(r"^\s*\[\s*x\s*\]", re.IGNORECASE)

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


@dataclass(frozen=True)
class CoverageRow:
    unit_type: str  # CLAIM | ARGUMENT | PROPOSITION | PROVOCATION
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
            meets = "—" if target is None else ("yes" if row.percent >= target else "NO")
            target_str = "—" if target is None else f"{target:.0f}%"
            lines.append(
                f"| {row.unit_type} | {row.axis} | {row.bucket} | {row.total} "
                f"| {row.verified} | {row.percent:.0f}% | {target_str} | {meets} |"
            )
        lines.append("")
        lines.append(self._tier_floor_line())
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
        PROVOCATION tier axis.
        """
        for row in self.rows:
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
    "Source Tier" — which starts with "source" — is excluded) or to
    contain "provocation".
    """
    bucket_col: int | None = None
    bucket_axis: str | None = None
    status_col: int | None = None

    if unit_type == "PROVOCATION":
        for idx, name in enumerate(header):
            normalized = name.lower().strip()
            if normalized.startswith("tier") or "provocation" in normalized:
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
        if not row.status:
            continue
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

        unit_type = marker.group(1).upper()
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
                # match, and let the empty bucket/status test below skip it.
                # Breaking here instead (the behaviour until 2026-09-14) ended
                # the table at the first divider and silently dropped every
                # row after it from the counts, so a P0 claim could leave the
                # denominator and `--strict` pass over what remained.
                row = row + [""] * (len(header) - len(row))
            bucket = row[bucket_col]
            status = row[status_col]
            # A blank Status still yields the row: the P0 tier floor must see a
            # P0 entry whether or not anyone has ticked it. Coverage skips it
            # in `_parse_registry`, exactly as before.
            if not bucket:
                i += 1
                continue
            yield _RegistryRow(
                unit_type=unit_type,
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
    if not counts:
        # Zero rows is never a legitimate registry, and it is what every
        # unrecognised marker reduces to (`**Claims:**`, `### **CLAIMs:**`):
        # before this, --strict passed over it with the P0 floor "NOT
        # evaluated". Same rule as `tools.check_registry`.
        raise ValueError(
            f"no registry rows parsed from {registry_path} — a registry is never "
            "legitimately empty, so this is a parse failure rather than a clean run. "
            "Sub-table markers must read exactly like `**CLAIMs:**` on their own line."
        )
    p0_tiers = tuple(
        (row.entry_id, row.tier)
        for row in _iter_registry_rows(content)
        if row.axis == PRIORITY_AXIS
        # `**P0**` is still P0: an undecorated compare would drop it from the floor.
        and _normalise_tier(row.bucket) == "P0"
        and (types is None or row.unit_type in {t.upper() for t in types})
    )

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
    )


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
        help="Exit 1 if any configured target is missed or the P0 tier floor fails",
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

    if args.strict and not (report.meets_targets and report.meets_tier_floor):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
