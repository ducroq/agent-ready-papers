"""DOI extractor and resolver for claim registries.

Extracts DOI patterns from a claim_registry.md and verifies each one
resolves via HTTP HEAD against https://doi.org/. Designed for CI use:
deterministic ordering, JSON output, stable exit codes.

Public API:
    check_dois(registry_path, *, offline=False, timeout=10.0) -> DOIReport

CLI:
    python -m tools.check_dois <registry.md> [--json] [--offline] [--timeout=10]

Exit codes:
    0  success — all DOIs resolved (or, with --offline, all DOIs parseable)
    1  failure — at least one DOI failed to resolve (or, with --offline,
                 at least one DOI failed to parse)
    2  tooling error (file missing, parse failure)

Note on `--offline`: offline mode does *not* mark DOIs as resolved. It
checks parseability only. `all_resolved` is False under --offline by
design; CI gates that depend on resolution still fail if the offline
flag is inherited unintentionally. The check is over `all_parseable`
instead, and a stderr banner makes the mode explicit.

Design notes:
    - Zero-dep: urllib + stdlib only.
    - Polite client: 10s default timeout, single retry on transient errors.
    - HEAD against https://doi.org/<doi> resolves to the registered URL;
      2xx and 3xx are both treated as "resolves".
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

DOI_REGEX = r"10\.\d{4,9}/[^\s\]\)\"<>]+"
DOI_BASE = "https://doi.org/"
DEFAULT_TIMEOUT = 10.0


@dataclass(frozen=True)
class DOIResult:
    doi: str
    line_number: int
    http_status: int | None       # None if offline / not checked
    parseable: bool               # regex matched a well-formed DOI
    resolved: bool                # True if 2xx or 3xx; always False under --offline
    note: str                     # diagnostic (empty when resolved cleanly)


@dataclass(frozen=True)
class DOIReport:
    registry_path: Path
    results: tuple[DOIResult, ...]
    offline: bool

    def to_dict(self) -> dict:
        return {
            "registry_path": self.registry_path.name,
            "offline": self.offline,
            "results": [asdict(r) for r in self.results],
            "all_resolved": self.all_resolved,
            "all_parseable": self.all_parseable,
            "count_total": len(self.results),
            "count_resolved": sum(1 for r in self.results if r.resolved),
            "count_parseable": sum(1 for r in self.results if r.parseable),
            "count_failed": sum(1 for r in self.results if not r.resolved),
        }

    def to_markdown(self) -> str:
        header = f"# DOI report — {self.registry_path.name}"
        if self.offline:
            header += " (offline — parseability only)"
        lines = [
            header,
            "",
            "| Line | DOI | HTTP | Parseable | Resolved | Note |",
            "|------|-----|------|-----------|----------|------|",
        ]
        for r in self.results:
            status = "—" if r.http_status is None else str(r.http_status)
            parseable = "yes" if r.parseable else "NO"
            resolved = "yes" if r.resolved else "NO"
            lines.append(
                f"| {r.line_number} | `{r.doi}` | {status} | {parseable} | {resolved} | {r.note} |"
            )
        return "\n".join(lines) + "\n"

    @property
    def all_resolved(self) -> bool:
        return bool(self.results) and all(r.resolved for r in self.results)

    @property
    def all_parseable(self) -> bool:
        return all(r.parseable for r in self.results)


def check_dois(
    registry_path: Path,
    *,
    offline: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> DOIReport:
    """Extract and verify all DOIs in a claim registry.

    Args:
        registry_path: path to claim_registry.md
        offline: skip HTTP HEAD calls; record parseability only.
            `resolved` is False for all results under offline mode by
            design (so CI gates over `all_resolved` cannot silently
            pass if the flag is inherited unintentionally).
        timeout: per-request timeout in seconds

    Raises:
        FileNotFoundError: if registry_path does not exist
    """
    if not registry_path.is_file():
        raise FileNotFoundError(registry_path)

    # TODO(#17): implement.
    #   1. Read file lines, regex-extract DOIs with their line numbers.
    #      After matching, strip trailing punctuation `.,:;` (markdown
    #      prose context often follows the DOI with a closing colon or
    #      period; the regex character class does not exclude these).
    #   2. Deduplicate while preserving first-seen order.
    #   3. If offline: build DOIResult(http_status=None, parseable=True,
    #      resolved=False, note="not checked (offline mode)").
    #   4. Else: urllib HEAD against https://doi.org/<doi>, 10s timeout,
    #      follow redirects. Treat 2xx/3xx as resolved; record final status code.
    #      One retry on URLError; subsequent failure → resolved=False
    #      with the error string in `note`. `parseable=True` for any
    #      DOI that survived the regex (parse failures should not reach
    #      this branch).
    raise NotImplementedError("DOI extraction + resolution not yet implemented — see TODO(#17)")


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.check_dois",
        description="Extract and verify DOIs in a claim registry.",
    )
    p.add_argument("registry", type=Path, help="Path to claim_registry.md")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    p.add_argument(
        "--offline",
        action="store_true",
        help="Skip network calls; verify DOI pattern parseability only",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Per-request HEAD timeout in seconds (default {DEFAULT_TIMEOUT:g})",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    try:
        report = check_dois(args.registry, offline=args.offline, timeout=args.timeout)
    except FileNotFoundError as exc:
        print(f"error: registry file not found: {exc}", file=sys.stderr)
        return 2
    except (ValueError, NotImplementedError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.offline:
        print(
            "OFFLINE MODE: no network verification performed; "
            "checking DOI parseability only.",
            file=sys.stderr,
        )

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(report.to_markdown())

    if args.offline:
        return 0 if report.all_parseable else 1
    return 0 if report.all_resolved else 1


if __name__ == "__main__":
    sys.exit(main())
