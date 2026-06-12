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

Public API:
    check_coverage(registry_path, *, types=None,
                   priority_targets=None,
                   provocation_targets=None) -> CoverageReport

CLI:
    python -m tools.coverage <registry.md> [--json] [--strict]

Exit codes:
    0  success (and, with --strict, all applicable targets met)
    1  failure (with --strict, at least one target missed)
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


@dataclass(frozen=True)
class CoverageRow:
    unit_type: str   # CLAIM | ARGUMENT | PROPOSITION | PROVOCATION
    axis: str        # PRIORITY_AXIS | PROVOCATION_TIER_AXIS
    bucket: str      # P0/P1/P2 or GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL
    total: int
    verified: int

    @property
    def percent(self) -> float:
        return 100.0 * self.verified / self.total if self.total else 0.0


@dataclass(frozen=True)
class CoverageReport:
    registry_path: Path
    rows: tuple[CoverageRow, ...]
    priority_targets: dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_PRIORITY_TARGETS)
    )
    provocation_targets: dict[str, float] | None = None

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
            "rows": [
                asdict(r) | {"percent": r.percent, "target": self._target_for(r)}
                for r in self.rows
            ],
            "priority_targets": dict(self.priority_targets),
            "provocation_targets": (
                None if self.provocation_targets is None
                else dict(self.provocation_targets)
            ),
            "meets_targets": self.meets_targets,
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
        return "\n".join(lines) + "\n"

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


def _find_bucket_and_status_columns(
    header: list[str], unit_type: str
) -> tuple[int, str, int] | None:
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
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        marker = _MARKER_REGEX.match(lines[i])
        if not marker:
            i += 1
            continue

        unit_type = marker.group(1).upper()
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines):
            break

        header = _split_row(lines[i])
        if header is None:
            continue

        cols = _find_bucket_and_status_columns(header, unit_type)
        if cols is None:
            i += 1
            continue
        bucket_col, axis, status_col = cols

        i += 1
        if i < len(lines) and _SEPARATOR_REGEX.match(lines[i]):
            i += 1

        while i < len(lines):
            row = _split_row(lines[i])
            if row is None:
                break
            if len(row) <= max(bucket_col, status_col):
                break
            bucket = row[bucket_col]
            status = row[status_col]
            if not bucket or not status:
                i += 1
                continue
            key = (unit_type, axis, bucket)
            slot = counts.setdefault(key, [0, 0])
            slot[0] += 1
            if _STATUS_VERIFIED_REGEX.match(status):
                slot[1] += 1
            i += 1

    return {k: (v[0], v[1]) for k, v in counts.items()}


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
        priority_targets=(
            dict(DEFAULT_PRIORITY_TARGETS) if priority_targets is None
            else dict(priority_targets)
        ),
        provocation_targets=(
            None if provocation_targets is None else dict(provocation_targets)
        ),
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
        help="Exit 1 if any configured target is missed",
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

    if args.strict and not report.meets_targets:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
