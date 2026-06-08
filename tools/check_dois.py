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

Resolution policy: HEAD against `https://doi.org/<doi>` without
following redirects. A 2xx or 3xx response from doi.org means the DOI
is registered (3xx is the normal case — doi.org redirects to the
publisher landing page). A 404 from doi.org means the DOI is not
registered. Other failures are recorded with the HTTP status in the
result note.

Design notes:
    - Zero-dep: http.client + stdlib only.
    - Polite client: 10s default timeout, single retry on transient errors.
    - Trailing punctuation (.,:;) is stripped from regex matches; markdown
      prose often places DOIs against closing colons/periods.
"""

from __future__ import annotations

import argparse
import http.client
import json
import re
import sys
import urllib.parse
from dataclasses import asdict, dataclass
from pathlib import Path

DOI_REGEX = re.compile(r'10\.\d{4,9}/[^\s"<>|\]]+')
DOI_BASE = "https://doi.org/"
DEFAULT_TIMEOUT = 10.0
_USER_AGENT = "agent-ready-papers/tools.check_dois"


def _clean_doi(raw: str) -> str:
    """Trim trailing punctuation and balance closing parens.

    The DOI character class allows `(` and `)` because some real DOIs
    carry them (e.g., Lancet `10.1016/S0140-6736(13)62228-X`). Markdown
    prose then wraps DOIs in their own parens, which would otherwise
    bleed in: `(DOI: 10.xxx/abc)` matches `10.xxx/abc)`, leaving an
    unbalanced trailing `)`. We strip trailing `.,:;` first, then strip
    trailing `)` while it exceeds the count of `(`.
    """
    doi = raw.rstrip(".,:;")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1].rstrip(".,:;")
    return doi


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


def _extract_dois(content: str) -> tuple[tuple[str, int], ...]:
    """Extract DOIs with their first-seen line number, deduplicated.

    Applies `_clean_doi` to every match — markdown prose commonly
    wraps DOIs in parens and trails them with `.,:;` punctuation.
    """
    seen: dict[str, int] = {}
    for lineno, line in enumerate(content.splitlines(), start=1):
        for match in DOI_REGEX.finditer(line):
            doi = _clean_doi(match.group(0))
            if doi and doi not in seen:
                seen[doi] = lineno
    return tuple((doi, lineno) for doi, lineno in seen.items())


def _head_doi(doi: str, timeout: float) -> tuple[int | None, bool, str]:
    """HEAD https://doi.org/<doi> without following redirects.

    Returns (http_status, resolved, note). One retry on transient error.
    2xx or 3xx from doi.org → resolved. 404 → not resolved. Other
    statuses → not resolved, note carries the status.
    """
    target = DOI_BASE + urllib.parse.quote(doi, safe="/:")
    parsed = urllib.parse.urlparse(target)
    path = parsed.path + (f"?{parsed.query}" if parsed.query else "")

    last_error: str | None = None
    for attempt in range(2):
        try:
            conn = http.client.HTTPSConnection(parsed.netloc, timeout=timeout)
            try:
                conn.request("HEAD", path, headers={"User-Agent": _USER_AGENT})
                resp = conn.getresponse()
                status = resp.status
                resp.read()
                resolved = 200 <= status < 400
                note = "" if resolved else f"HTTP {status}"
                return status, resolved, note
            finally:
                conn.close()
        except (OSError, http.client.HTTPException) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt == 0:
                continue
    return None, False, last_error or "unreachable"


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

    content = registry_path.read_text(encoding="utf-8")
    extracted = _extract_dois(content)

    results: list[DOIResult] = []
    for doi, lineno in extracted:
        if offline:
            results.append(
                DOIResult(
                    doi=doi,
                    line_number=lineno,
                    http_status=None,
                    parseable=True,
                    resolved=False,
                    note="not checked (offline mode)",
                )
            )
        else:
            status, resolved, note = _head_doi(doi, timeout)
            results.append(
                DOIResult(
                    doi=doi,
                    line_number=lineno,
                    http_status=status,
                    parseable=True,
                    resolved=resolved,
                    note=note,
                )
            )

    return DOIReport(
        registry_path=registry_path,
        results=tuple(results),
        offline=offline,
    )


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
    except ValueError as exc:
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
