"""Bibliographic metadata verifier for .bib files and claim registries.

`check_dois.py` answers *does this DOI resolve*. This module answers the
question that one cannot: *does the entry attached to that DOI actually
describe the paper it resolves to*.

The distinction is not academic. Rao & Callison-Burch (COLM 2026,
arXiv:2604.03159) benchmarked search-enabled frontier models generating
BibTeX and found 83.6% field-level accuracy but only **50.9% of entries
fully correct** — the dominant failure being a real paper carrying
corrupted metadata (wrong authors, year, venue) rather than an invented
one. Every such entry passes a resolution check cleanly. They identify
two failure shapes, and this tool is built to separate them:

    wholesale substitution  -> the DOI belongs to a different paper
                               (first-author surname absent, title
                               unrelated) -> MISMATCH
    isolated field error    -> right paper, one field wrong
                               (year off by one, venue garbled) -> MISMATCH
                               or WARN depending on the field

Authority is the DOI's registration agency: Crossref first, falling back
to DataCite on a 404. The fallback is not incidental — arXiv registers
under the 10.48550 prefix with DataCite, so a Crossref-only lookup
reports every preprint in a bibliography as unverifiable, which for an
arXiv-first literature is precisely the wrong place to go blind.

Public API:
    check_metadata(path, *, offline=False, timeout=10.0, mailto=None)
        -> MetadataReport

CLI:
    python -m tools.check_metadata <file.bib|registry.md>
        [--json] [--offline] [--strict] [--timeout=10] [--mailto=EMAIL]

Exit codes:
    0  success — no MISMATCH results (WARN allowed unless --strict)
    1  failure — at least one MISMATCH, or any WARN under --strict,
                 or a DOI with no record at either agency
    2  tooling error (file missing, unreadable, no DOIs found)

Input modes, chosen by file suffix:
    .bib  strict  — structured fields compared field by field
    .md   loose   — DOI plus its surrounding prose; checks that the year
                    and an author surname on that line match the record.
                    Catches a real DOI captioned with the wrong author or
                    year, which is the shape this failure takes in a
                    claim registry.

On `--mailto`: Crossref asks API consumers to identify themselves for
priority routing. It is opt-in and off by default, deliberately — an
email address is the caller's to disclose, not this tool's to send.

Design constraints inherited from the rest of tools/: stdlib only,
deterministic ordering, polite sequential client with a single retry.
"""

from __future__ import annotations

import argparse
import http.client
import json
import re
import sys
import unicodedata
import urllib.parse
from dataclasses import asdict, dataclass
from pathlib import Path

DOI_REGEX = re.compile(r'10\.\d{4,9}/[^\s"<>|\]]+')
CROSSREF_HOST = "api.crossref.org"
DATACITE_HOST = "api.datacite.org"
DEFAULT_TIMEOUT = 10.0
_USER_AGENT = "agent-ready-papers/tools.check_metadata"

# Containment thresholds for fuzzy string fields. Titles are compared
# strictly because Crossref stores them verbatim; venues loosely because
# abbreviation ("J. Mark." vs "Journal of Marketing") is normal and not
# an error worth failing a build over.
_TITLE_MATCH = 0.90
_TITLE_WARN = 0.50
_VENUE_MATCH = 0.60

_VERDICT_ORDER = {"ok": 0, "warn": 1, "unchecked": 2, "mismatch": 3, "unresolved": 4, "error": 5}


# --------------------------------------------------------------------------
# normalisation helpers
# --------------------------------------------------------------------------


def _strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


# LaTeX letter-commands that ARE letters rather than markup. Accent forms
# like \"u or \'e are handled by rule; these have no non-backslash form.
_LATEX_LETTERS = {
    r"\\ss": "ss",
    r"\\aa": "aa",
    r"\\AA": "AA",
    r"\\ae": "ae",
    r"\\AE": "AE",
    r"\\oe": "oe",
    r"\\OE": "OE",
    r"\\o": "o",
    r"\\O": "O",
    r"\\l": "l",
    r"\\L": "L",
    r"\\i": "i",
    r"\\j": "j",
}


def _de_latex(text: str) -> str:
    r"""Reduce LaTeX name/title markup to plain letters.

    Order matters. `Schl{\"u}ssel` and `Hr{\o}bjartsson` are the real
    cases from this repo's own bibliography: a naive `\\[a-zA-Z]+ -> space`
    rule turns them into `schl ussel` and `hr objartsson`, which then read
    as author mismatches against Crossref. Accents are stripped to their
    base letter, letter-commands are mapped, and only then is anything
    that remains treated as markup and dropped.
    """
    # \"u, \'e, \`a, \^o, \~n, \=a, \.z — backslash, non-letter, letter
    text = re.sub(r'\\[\'"`^~=.]\s*\{?([a-zA-Z])\}?', r"\1", text)
    # \c{c}, \v{s}, \u{a}, \H{o}, \r{a}, \k{a}, \d{s}, \b{o}
    text = re.sub(r"\\[cvuHrkdb]\{([a-zA-Z])\}", r"\1", text)
    for cmd, letter in _LATEX_LETTERS.items():
        text = re.sub(cmd + r"(?![a-zA-Z])", letter, text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)  # \emph, \textbf, ...
    return text


def _normalise(text: str) -> str:
    """Fold to comparable form: de-LaTeX, de-accent, alphanumeric only."""
    text = _de_latex(text)
    text = text.replace("{", "").replace("}", "")
    text = _strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _tokens(text: str) -> set[str]:
    return set(_normalise(text).split())


def _containment(a: str, b: str) -> float:
    """Overlap relative to the shorter token set.

    Containment rather than Jaccard because a local entry legitimately
    truncates a subtitle; that should not read as a different paper.
    """
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def _surname(author: str) -> str:
    """Extract a comparable surname from one BibTeX author string.

    Handles both `Last, First` and `First Last`. Drops common suffixes
    and any `{...}` protection braces.
    """
    author = _de_latex(author).replace("{", "").replace("}", "").strip()
    if not author:
        return ""
    if "," in author:
        surname = author.split(",", 1)[0]
    else:
        parts = author.split()
        surname = parts[-1] if parts else ""
        if surname.lower().rstrip(".") in {"jr", "sr", "ii", "iii"} and len(parts) > 1:
            surname = parts[-2]
    return _normalise(surname)


def _split_authors(raw: str) -> tuple[str, ...]:
    raw = " ".join(raw.split())
    parts = re.split(r"\s+and\s+", raw)
    return tuple(s for s in (_surname(p) for p in parts) if s)


def _clean_doi(raw: str) -> str:
    """Trim trailing punctuation and balance closing parens.

    Mirrors `tools.check_dois._clean_doi` — some real DOIs carry parens
    (Lancet `10.1016/S0140-6736(13)62228-X`) while prose wraps them in
    parens of its own. Kept as a local copy rather than imported so the
    two modules stay independently vendorable.
    """
    doi = raw.rstrip(".,:;}")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1].rstrip(".,:;}")
    return doi


# --------------------------------------------------------------------------
# result types
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldCheck:
    field_name: str
    local: str
    remote: str
    verdict: str  # "ok" | "warn" | "mismatch" | "absent"
    note: str = ""


@dataclass(frozen=True)
class MetadataResult:
    doi: str
    line_number: int
    entry_key: str  # bib key, or "" in registry mode
    verdict: str  # worst field verdict, or unresolved/error
    checks: tuple[FieldCheck, ...] = ()
    note: str = ""

    @property
    def failed_fields(self) -> tuple[str, ...]:
        return tuple(c.field_name for c in self.checks if c.verdict == "mismatch")


@dataclass(frozen=True)
class MetadataReport:
    source_path: Path
    mode: str  # "bib" | "registry"
    results: tuple[MetadataResult, ...]
    offline: bool

    @property
    def count_mismatch(self) -> int:
        return sum(1 for r in self.results if r.verdict in ("mismatch", "unresolved", "error"))

    @property
    def count_warn(self) -> int:
        return sum(1 for r in self.results if r.verdict == "warn")

    @property
    def all_ok(self) -> bool:
        return bool(self.results) and self.count_mismatch == 0 and self.count_unchecked == 0

    @property
    def count_unchecked(self) -> int:
        """Entries where the record resolved but NO field could be compared."""
        return sum(1 for r in self.results if r.verdict == "unchecked")

    @property
    def all_clean(self) -> bool:
        """No mismatches AND no warnings — the --strict bar."""
        return self.all_ok and self.count_warn == 0

    def to_dict(self) -> dict:
        return {
            "source_path": self.source_path.name,
            "mode": self.mode,
            "offline": self.offline,
            "results": [{**asdict(r), "failed_fields": list(r.failed_fields)} for r in self.results],
            "count_total": len(self.results),
            "count_ok": sum(1 for r in self.results if r.verdict == "ok"),
            "count_unchecked": self.count_unchecked,
            "count_warn": self.count_warn,
            "count_mismatch": self.count_mismatch,
            "all_ok": self.all_ok,
            "all_clean": self.all_clean,
        }

    def to_markdown(self) -> str:
        header = f"# Metadata report — {self.source_path.name} ({self.mode} mode)"
        if self.offline:
            header += " (offline — parse only)"
        lines = [
            header,
            "",
            "| Line | Key | DOI | Verdict | Fields at fault | Note |",
            "|------|-----|-----|---------|-----------------|------|",
        ]
        symbol = {
            "ok": "OK",
            "warn": "WARN",
            "mismatch": "MISMATCH",
            "unchecked": "NOTHING COMPARED",
            "unresolved": "NO RECORD",
            "error": "ERROR",
            "skipped": "—",
        }
        for r in self.results:
            bad = ", ".join(r.failed_fields) or "—"
            key = f"`{r.entry_key}`" if r.entry_key else "—"
            lines.append(
                f"| {r.line_number} | {key} | `{r.doi}` | {symbol.get(r.verdict, r.verdict)} | {bad} | {r.note} |"
            )
        lines.append("")
        lines.append(
            f"**{len(self.results)} checked** — "
            f"{sum(1 for r in self.results if r.verdict == 'ok')} ok, "
            f"{self.count_warn} warn, {self.count_unchecked} nothing-compared, "
            f"{self.count_mismatch} failing."
        )
        # Detail only for entries that need a human; a clean run stays short.
        for r in self.results:
            if r.verdict in ("ok", "skipped"):
                continue
            lines.append("")
            lines.append(f"### {r.entry_key or r.doi} — {symbol.get(r.verdict, r.verdict)}")
            if r.note:
                lines.append(f"{r.note}")
            for c in r.checks:
                if c.verdict == "ok":
                    continue
                lines.append(
                    f"- **{c.field_name}** ({c.verdict}): "
                    f"local `{c.local or '—'}` vs Crossref `{c.remote or '—'}`" + (f" — {c.note}" if c.note else "")
                )
        return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# input parsing
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class _LocalEntry:
    key: str
    line_number: int
    doi: str
    fields: dict


def _parse_bib(content: str) -> tuple[_LocalEntry, ...]:
    """Extract entries from a .bib file.

    Deliberately small: scans for `@type{key,` then brace-matches to the
    entry's close, splitting top-level `field = value` pairs. Values may
    be `{...}` (nested braces honoured), `"..."`, or bare.
    """
    entries: list[_LocalEntry] = []
    for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", content):
        start = match.end()
        depth = 1
        i = start
        while i < len(content) and depth:
            ch = content[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
        body = content[start : i - 1]
        line_number = content.count("\n", 0, match.start()) + 1
        fields = _parse_bib_fields(body)
        doi = _clean_doi(fields.get("doi", "").strip())
        if not doi:
            # A DOI may also be buried in a url/note field.
            for candidate in (fields.get("url", ""), fields.get("note", "")):
                found = DOI_REGEX.search(candidate)
                if found:
                    doi = _clean_doi(found.group(0))
                    break
        entries.append(_LocalEntry(key=match.group(2), line_number=line_number, doi=doi, fields=fields))
    return tuple(entries)


def _parse_bib_fields(body: str) -> dict:
    fields: dict = {}
    i = 0
    n = len(body)
    while i < n:
        eq = body.find("=", i)
        if eq == -1:
            break
        name = body[i:eq].strip().strip(",").strip().lower()
        j = eq + 1
        while j < n and body[j].isspace():
            j += 1
        if j >= n:
            break
        if body[j] == "{":
            depth = 1
            k = j + 1
            while k < n and depth:
                if body[k] == "{":
                    depth += 1
                elif body[k] == "}":
                    depth -= 1
                k += 1
            value = body[j + 1 : k - 1]
            i = k
        elif body[j] == '"':
            k = body.find('"', j + 1)
            k = n if k == -1 else k
            value = body[j + 1 : k]
            i = k + 1
        else:
            k = body.find(",", j)
            k = n if k == -1 else k
            value = body[j:k]
            i = k
        if name and re.fullmatch(r"[a-z][a-z0-9_-]*", name):
            fields[name] = " ".join(value.split())
        while i < n and body[i] in ", \t\r\n":
            i += 1
    return fields


def _parse_registry(content: str) -> tuple[_LocalEntry, ...]:
    """Extract DOIs from markdown with the prose on their own line.

    The line is the local claim: a registry cell reads
    `Mugaanyi et al. 2024 (JMIR, DOI: 10.2196/52935): ...`. The year and
    surname on that line are what we check the record against.

    ⚠️ EVERY occurrence is returned, not the first per DOI. A file-global
    dedup (the behaviour until 2026-09-14) silently discarded later citations
    of the same DOI — so a source cited correctly on one line and MISCAPTIONED
    on another was never checked on the second line, and whether the
    miscaption was caught depended on row order. That is precisely the failure
    this mode exists to catch. The network cost is deduplicated in the caller
    instead, by caching the fetch per DOI.
    """
    entries: list[_LocalEntry] = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        for match in DOI_REGEX.finditer(line):
            doi = _clean_doi(match.group(0))
            if not doi:
                continue
            entries.append(_LocalEntry(key="", line_number=lineno, doi=doi, fields={"_context": line}))
    return tuple(entries)


# --------------------------------------------------------------------------
# Crossref
# --------------------------------------------------------------------------


def _get_json(host: str, path: str, timeout: float) -> tuple[dict | None, int | None, str]:
    """GET a JSON endpoint, following same-host redirects up to 3 hops.

    Crossref answers some DOIs with a 301 to a canonicalised path
    (`10.5465/amr.1989.4308371` is one in this repo's own bibliography).
    Treating that as an error reports a perfectly good entry as
    unverifiable, so redirects are followed rather than surfaced.
    """
    last_error: str | None = None
    for _hop in range(3):
        for attempt in range(2):
            try:
                conn = http.client.HTTPSConnection(host, timeout=timeout)
                try:
                    conn.request(
                        "GET",
                        path,
                        headers={"User-Agent": _USER_AGENT, "Accept": "application/json"},
                    )
                    resp = conn.getresponse()
                    payload = resp.read()
                    if resp.status in (301, 302, 303, 307, 308):
                        location = resp.getheader("Location") or ""
                        parsed = urllib.parse.urlparse(location)
                        if parsed.netloc and parsed.netloc != host:
                            return None, resp.status, f"redirect off-host to {parsed.netloc}"
                        if not parsed.path:
                            return None, resp.status, f"HTTP {resp.status} without Location"
                        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
                        break  # next hop
                    if resp.status != 200:
                        return None, resp.status, f"HTTP {resp.status}"
                    return json.loads(payload), 200, ""
                finally:
                    conn.close()
            except (OSError, http.client.HTTPException, ValueError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt == 0:
                    continue
                return None, None, last_error
        else:
            return None, None, last_error or "unreachable"
    return None, None, "too many redirects"


def _record_from_crossref(message: dict) -> dict:
    years: set[int] = set()
    for key in ("issued", "published-online", "published-print", "published", "created"):
        for part in (message.get(key) or {}).get("date-parts") or []:
            if part and isinstance(part[0], int):
                years.add(part[0])
    surnames = tuple(
        _normalise(a.get("family") or a.get("name") or "")
        for a in (message.get("author") or [])
        if (a.get("family") or a.get("name"))
    )
    return {
        "title": _first(message.get("title")),
        "years": years,
        "surnames": surnames,
        "venue": _first(message.get("container-title")),
        "agency": "Crossref",
    }


def _record_from_datacite(data: dict) -> dict:
    attrs = data.get("data", {}).get("attributes", {}) or {}
    titles = attrs.get("titles") or []
    years: set[int] = set()
    if isinstance(attrs.get("publicationYear"), int):
        years.add(attrs["publicationYear"])
    for date in attrs.get("dates") or []:
        found = re.match(r"(\d{4})", str(date.get("date", "")))
        if found:
            years.add(int(found.group(1)))
    surnames: list[str] = []
    for creator in attrs.get("creators") or []:
        family = creator.get("familyName")
        if not family:
            name = creator.get("name") or ""
            family = name.split(",")[0] if "," in name else name.split(" ")[-1]
        if family:
            surnames.append(_normalise(family))
    return {
        "title": (titles[0] or {}).get("title", "") if titles else "",
        "years": years,
        "surnames": tuple(surnames),
        "venue": attrs.get("publisher") or "",
        "agency": "DataCite",
    }


def _fetch_record(doi: str, timeout: float, mailto: str | None) -> tuple[dict | None, str, str]:
    """Resolve a DOI's registered metadata, Crossref first then DataCite.

    Returns ``(record, note, outcome)``. ``outcome`` is ``"found"``,
    ``"absent"`` (both agencies answered and neither has this DOI) or
    ``"unreachable"`` (we could not get an answer).

    ⚠️ The outcome is RETURNED, never inferred from the note. The caller used
    to decide with ``"404" in note``, which matches the string
    ``"Crossref 404; DataCite: gaierror"`` — a DOI we could not check at all.
    Every arXiv DOI then rendered as **NO RECORD** on any DataCite outage or
    proxied network, i.e. a real paper reported as fabricated. In an
    anti-hallucination workflow that is the expensive direction. Measured
    2026-09-14.

    Not every DOI is a Crossref DOI. arXiv registers under the 10.48550
    prefix with **DataCite**, so a Crossref-only lookup reports every
    preprint in a bibliography as having no record — which for this repo,
    whose literature is increasingly arXiv-first, would have made the tool
    useless on exactly the entries most likely to be wrong.
    """
    quoted = urllib.parse.quote(doi, safe="/:")
    path = "/works/" + quoted
    if mailto:
        path += "?" + urllib.parse.urlencode({"mailto": mailto})
    data, status, note = _get_json(CROSSREF_HOST, path, timeout)
    if data is not None:
        return _record_from_crossref(data.get("message", {})), "Crossref", "found"

    if status == 404:
        dc, dc_status, dc_note = _get_json(DATACITE_HOST, "/dois/" + quoted, timeout)
        if dc is not None:
            return _record_from_datacite(dc), "DataCite", "found"
        if dc_status == 404:
            # Both agencies answered and neither holds it. This is the ONLY
            # path that licenses "NO RECORD".
            return None, "no record at Crossref or DataCite (404)", "absent"
        return None, f"Crossref 404; DataCite unreachable: {dc_note}", "unreachable"

    return None, note, "unreachable"


def _first(value) -> str:
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


# --------------------------------------------------------------------------
# comparison
# --------------------------------------------------------------------------


def _compare_bib(entry: _LocalEntry, record: dict) -> tuple[FieldCheck, ...]:
    checks: list[FieldCheck] = []
    f = entry.fields

    remote_title = record["title"]
    local_title = f.get("title", "")
    if local_title:
        score = _containment(local_title, remote_title)
        verdict = "ok" if score >= _TITLE_MATCH else "warn" if score >= _TITLE_WARN else "mismatch"
        checks.append(FieldCheck("title", local_title, remote_title, verdict, f"containment {score:.2f}"))
    else:
        checks.append(FieldCheck("title", "", remote_title, "absent", "no local title"))

    remote_years = record["years"]
    local_year = f.get("year", "").strip()
    if local_year.isdigit():
        verdict = "ok" if int(local_year) in remote_years else "mismatch"
        checks.append(FieldCheck("year", local_year, "/".join(str(y) for y in sorted(remote_years)) or "—", verdict))
    elif local_year:
        checks.append(FieldCheck("year", local_year, "—", "warn", "unparseable local year"))

    remote_surnames = record["surnames"]
    local_authors = _split_authors(f.get("author", "") or f.get("editor", ""))
    if local_authors and remote_surnames:
        if local_authors[0] not in remote_surnames:
            checks.append(
                FieldCheck(
                    "author",
                    local_authors[0],
                    remote_surnames[0],
                    "mismatch",
                    "first-author surname absent from record — possible wholesale substitution",
                )
            )
        else:
            missing = [a for a in local_authors if a not in remote_surnames]
            if missing:
                checks.append(
                    FieldCheck(
                        "author",
                        ", ".join(local_authors),
                        ", ".join(remote_surnames),
                        "warn",
                        f"not in record: {', '.join(missing)}",
                    )
                )
            elif len(local_authors) != len(remote_surnames):
                checks.append(
                    FieldCheck(
                        "author",
                        f"{len(local_authors)} authors",
                        f"{len(remote_surnames)} authors",
                        "warn",
                        "author count differs",
                    )
                )
            else:
                checks.append(FieldCheck("author", ", ".join(local_authors), ", ".join(remote_surnames), "ok"))
    elif not local_authors:
        checks.append(FieldCheck("author", "", ", ".join(remote_surnames), "absent", "no local author field"))

    remote_venue = record["venue"]
    local_venue = f.get("journal", "") or f.get("booktitle", "") or f.get("publisher", "")
    if local_venue and remote_venue:
        score = _containment(local_venue, remote_venue)
        verdict = "ok" if score >= _VENUE_MATCH else "warn"
        detail = f"containment {score:.2f}; abbreviation is normal"
        if record.get("agency") == "DataCite":
            # DataCite stores a publisher ("arXiv"), never a venue, so a
            # preprint cited by its workshop proceedings always scores 0.00
            # here. Say so, or every arXiv entry looks like a finding.
            detail += " — DataCite records a publisher, not a venue; expect a low score"
        checks.append(FieldCheck("venue", local_venue, remote_venue, verdict, detail))

    return tuple(checks)


def _compare_registry(entry: _LocalEntry, record: dict) -> tuple[FieldCheck, ...]:
    """Loose check of the prose captioning a DOI in a registry."""
    # Strip the DOI itself before reading years off the line. Many DOIs
    # embed their publication year (`10.5465/amr.1989.4308371`), so a cell
    # that miscites Whetten 1989 as 1991 still contains "1989" — inside the
    # DOI — and the check passes on the very error it exists to catch.
    context = entry.fields.get("_context", "").replace(entry.doi, " ")
    checks: list[FieldCheck] = []

    remote_years = record["years"]
    cited_years = {int(m.group(0)) for m in re.finditer(r"\b(?:19|20)\d{2}\b", context)}
    if cited_years:
        verdict = "ok" if cited_years & remote_years else "mismatch"
        checks.append(
            FieldCheck(
                "year",
                "/".join(str(y) for y in sorted(cited_years)),
                "/".join(str(y) for y in sorted(remote_years)) or "—",
                verdict,
                "" if verdict == "ok" else "no year on this line matches the record",
            )
        )

    remote_surnames = record["surnames"]
    if remote_surnames:
        context_tokens = _tokens(context)
        verdict = "ok" if any(s in context_tokens for s in remote_surnames) else "warn"
        checks.append(
            FieldCheck(
                "author",
                "(prose)",
                ", ".join(remote_surnames[:4]),
                verdict,
                "" if verdict == "ok" else "no author surname from the record appears on this line",
            )
        )

    # No title check here, deliberately. A registry cell cites a source, it
    # does not quote its title, so comparing the two warned on 8 of 9 correct
    # rows in this repo's own registry on first run. A check that fires on
    # almost everything teaches people to ignore warnings, which costs more
    # than the rare case it would catch. Titles are checked in .bib mode,
    # where a title field is actually present to be wrong.

    return tuple(checks)


def _worst(checks: tuple[FieldCheck, ...]) -> str:
    """Worst field verdict, with "compared nothing" kept distinct from "ok".

    ⚠️ "absent" means the LOCAL entry had no such field, so nothing was
    compared. Folding it into "ok" made an entry with zero comparable fields —
    a bare `@article{k, doi = {...}}`, which is exactly the AI-generated stub
    shape this tool cites Rao & Callison-Burch for — report OK and pass
    `--strict`. The detail block is also suppressed for "ok", so the word
    "absent" never reached the reader. Measured 2026-09-14.
    """
    worst = "ok"
    comparable = 0
    for c in checks:
        if c.verdict in ("ok", "warn", "mismatch"):
            comparable += 1
        if c.verdict == "mismatch":
            return "mismatch"
        if c.verdict == "warn":
            worst = "warn"
    if comparable == 0:
        return "unchecked"
    return worst


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


def check_metadata(
    source_path: Path,
    *,
    offline: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
    mailto: str | None = None,
) -> MetadataReport:
    """Verify local bibliographic metadata against Crossref.

    Args:
        source_path: a `.bib` file (strict field comparison) or a
            markdown registry (loose prose comparison)
        offline: parse and report what would be checked; contacts nothing
        timeout: per-request timeout in seconds
        mailto: optional address for Crossref's polite pool. Opt-in.

    Raises:
        FileNotFoundError: if source_path does not exist
        ValueError: if no DOI-bearing entries are found
    """
    if not source_path.is_file():
        raise FileNotFoundError(source_path)

    content = source_path.read_text(encoding="utf-8")
    mode = "bib" if source_path.suffix.lower() == ".bib" else "registry"
    entries = _parse_bib(content) if mode == "bib" else _parse_registry(content)

    if not entries:
        raise ValueError(f"no entries found in {source_path}")
    if not any(e.doi for e in entries):
        raise ValueError(f"no DOIs found in {source_path}")

    # One network call per DOI even though every OCCURRENCE is checked.
    _fetch_cache: dict[str, tuple[dict | None, str, str]] = {}
    results: list[MetadataResult] = []
    for entry in entries:
        if not entry.doi:
            results.append(
                MetadataResult(
                    doi="",
                    line_number=entry.line_number,
                    entry_key=entry.key,
                    verdict="skipped",
                    note="entry carries no DOI — not checkable here",
                )
            )
            continue
        if offline:
            results.append(
                MetadataResult(
                    doi=entry.doi,
                    line_number=entry.line_number,
                    entry_key=entry.key,
                    verdict="skipped",
                    note="not checked (offline mode)",
                )
            )
            continue

        if entry.doi in _fetch_cache:
            record, note, outcome = _fetch_cache[entry.doi]
        else:
            record, note, outcome = _fetch_record(entry.doi, timeout, mailto)
            _fetch_cache[entry.doi] = (record, note, outcome)
        if record is None:
            # "unresolved" renders as NO RECORD and is a claim that the DOI
            # does not exist. Only an "absent" outcome supports it.
            verdict = "unresolved" if outcome == "absent" else "error"
            results.append(
                MetadataResult(
                    doi=entry.doi, line_number=entry.line_number, entry_key=entry.key, verdict=verdict, note=note
                )
            )
            continue

        checks = _compare_bib(entry, record) if mode == "bib" else _compare_registry(entry, record)
        results.append(
            MetadataResult(
                doi=entry.doi,
                line_number=entry.line_number,
                entry_key=entry.key,
                verdict=_worst(checks),
                checks=checks,
                note="" if record.get("agency") == "Crossref" else f"via {record.get('agency')}",
            )
        )

    return MetadataReport(source_path=source_path, mode=mode, results=tuple(results), offline=offline)


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.check_metadata",
        description="Verify local bibliographic metadata against Crossref. "
        "Complements check_dois, which verifies resolution only.",
    )
    p.add_argument("source", type=Path, help="Path to a .bib file or claim_registry.md")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    p.add_argument("--offline", action="store_true", help="Parse entries and report what would be checked; no network")
    p.add_argument("--strict", action="store_true", help="Treat WARN as failure (exit 1), not only MISMATCH")
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Per-request timeout in seconds (default {DEFAULT_TIMEOUT:g})",
    )
    p.add_argument(
        "--mailto",
        default=None,
        help="Optional address for Crossref's polite pool (opt-in; nothing is sent unless you pass it)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    try:
        report = check_metadata(args.source, offline=args.offline, timeout=args.timeout, mailto=args.mailto)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.offline:
        print("OFFLINE MODE: entries parsed but not verified against Crossref.", file=sys.stderr)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(report.to_markdown())

    if args.offline:
        # --strict asserts "every field matched". Offline compares no fields at
        # all, so the combination asserts cleanliness over nothing. Returning 0
        # here (the behaviour until 2026-09-14) meant a CI step that inherited
        # --offline could never fail, which is the exact hazard the --offline
        # note in tools/README.md was written about — for the sibling tool.
        # Refuse the combination rather than pass it.
        if args.strict:
            print(
                "error: --strict with --offline asserts every field matched while "
                "comparing no fields at all. Drop one of them.",
                file=sys.stderr,
            )
            return 2
        return 0
    if args.strict:
        return 0 if report.all_clean else 1
    return 0 if report.all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
