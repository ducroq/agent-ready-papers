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
        ValueError: if the file is not a parseable registry
    """
    if not registry_path.is_file():
        raise FileNotFoundError(registry_path)

    # TODO(#17): implement per-type sub-table parser.
    #   Walk the file, identify "**CLAIMs:**" / "**ARGUMENTs**" / "**PROPOSITIONs**" /
    #   "**PROVOCATIONs**" markers, parse the markdown table that follows each,
    #   count rows by Priority column (axis=PRIORITY_AXIS) or Tier column
    #   (axis=PROVOCATION_TIER_AXIS for PROVOCATION sub-tables),
    #   count Status == [x] as verified.
    #   Honour the `types` filter: skip sub-tables whose unit_type is not
    #   in the filter when one is provided.
    raise NotImplementedError("Sub-table parser not yet implemented — see TODO(#17)")


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
    except (ValueError, NotImplementedError) as exc:
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
