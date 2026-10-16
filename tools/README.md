# tools/

Registry-verification tooling for agent-ready-papers. Closes [#17](https://github.com/ducroq/agent-ready-papers/issues/17).

**Seven tools**, all stdlib-only (`check_quotes` calls `pdftotext` for PDFs, `check_experiments` calls `git`), all deterministic, all designed to run in CI. ⚠️ This
section said *"Two tools"* until 2026-09-14, two releases after the third and fourth
were released — re-derive with `ls tools/*.py` rather than trusting the count here.

| Tool | Purpose |
|------|---------|
| `coverage.py` | Parse a claim registry's tables (DR-027 Claims / Contributions / Declared starting points, or DR-004's deprecated per-type sub-tables); report P0/P1/P2 coverage, and separately the DR-002 P0 tier floor. |
| `check_dois.py` | Extract DOI patterns from a registry; verify each resolves via `https://doi.org/`. |
| `check_metadata.py` | Compare the bibliographic FIELDS against Crossref/DataCite — a resolving DOI is not a correct entry. |
| `check_registry.py` | Registry/manuscript internal consistency: anchors, tier agreement across copies, schema (DR-027 rules, or DR-004's type-conditional columns), premise graph, word budget, and with `--glossary` the paper's glossary (DR-028). |
| `check_quotes.py` | Does a quoted phrase occur in a source's full text, in order? PDF (three readings, including column by column from word positions), epub (printed page markers), text. Numbers keep their marks (decimal, thousands, ratio), exponents are tokens, and every Unicode maths symbol plus `~ % °` must match, with LaTeX's overlaid "≠" recomposed and a minus read from context; so "p < 0.05" is not found against "p > 0.05". A match needing a lenient reading (`:` as `.`, a glued footnote marker, "11, 000") is CHECK, not FOUND, as is every match in pdf2htmlEX HTML, whose spans split words; there a quote is also retried with spaces ignored ([#57](https://github.com/ducroq/agent-ready-papers/issues/57)). Reports NO TEXT LAYER when two thirds of pages are near-empty. A FOUND means the words occur in order, not that they support the citing sentence. Sources are usually gitignored, so it runs locally, not in CI. Closes [#48](https://github.com/ducroq/agent-ready-papers/issues/48). |
| `check_experiments.py` | The experiment registry (`vv/experiments/registry.jsonl`, DR-024): schema, id order, artifacts tracked and inside `vv/evidence/`, and each metric found standing alone in its evidence, with dates removed. Exit 0 / 1 / 2 (pass / a failure / registry unreadable, no git, not a work tree). Its docstring lists what it cannot see. Run by `make check`. |
| `registry_edit.py` | Edit one claim-table row by ID (append to the statement, set Status, replace text), refusing unless exactly one claim-table row (`\| ID \| statement \| P0-P3 \|`) matches; Priority Guide rows, which have no priority column, and rows in code fences are not matched. Refuses `\|` or line breaks in new text and keeps line endings. |

## Status

**Implemented and tested.** Both parsers landed and verified against the Paper 1 fixture (19 entries, 9 DOIs); pytest suite is green; live HEAD-against-`doi.org` confirms all 9 DOIs resolve. Two DR-011 review batteries applied (one for the scaffold, one for the parser). Closes [#17](https://github.com/ducroq/agent-ready-papers/issues/17).

## Registry tables (DR-027, Proposed) and the DR-004 aliases

Both parsers read a table only directly under a bold marker on its own line:

| Marker | Rows | Unit type in reports |
|--------|------|----------------------|
| `**Claims:**` | `S<n>-<n>` or `S<n>-<n>a` | DESCRIPTIVE or NORMATIVE from the Says cell; anything else is UNCLASSIFIED |
| `**Contributions:**` | `C<n>` | CONTRIBUTION, always in the P0 bucket |
| `**Declared starting points:**` | `D<n>` | not counted: excluded from coverage and the P0 floor, reported apart (count, and how many are `[x]`) |
| `**PROVOCATIONs**` (DR-010) | as before | PROVOCATION, unchanged |
| `**CLAIMs:**`, `**ARGUMENTs**`, `**PROPOSITIONs**` | as before | **deprecated aliases** (v5.0.0, read until v6.0.0): checked under DR-004's rules, reported under their old labels, and the report carries one `Deprecation:` line. It changes no number and no exit code |

The DR-027 names are case-sensitive as written. A line in marker shape with a known name in another case or form (`**CONTRIBUTIONS:**`, `### **CLAIMs:**`, `**claims**`) is a **near-miss marker**: `coverage.py` exits 2 and `check_registry.py` reports a finding, because its table would be read by nothing. Lines inside a code fence or an HTML comment are examples and are not near-misses.

DR-027 Grounds (Claims) and Rests on (Contributions) cells hold semicolon-separated typed items: `src: Author Year` (a source), `claim: S1-2` (another claim), `decl: D1` (a declared starting point), `own: <method>` (the author's own observation, experiment or measurement, e.g. `own: corpus count, query Q1 (2026-03-01)`). A contribution's Rests on lists only `claim:` and `decl:` items.

## Usage (once parsing lands)

```bash
# Markdown report to stdout
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md

# JSON for CI consumption
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --json
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md --json

# CI-friendly: exit 1 if a configured target is missed or the P0 tier floor fails
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --strict

# Quote check against a saved full text (exit 0 all found, 1 a miss, 2 unreadable or no text layer)
python -m tools.check_quotes literature/pdfs/<file>.pdf "first quoted phrase" "second quoted phrase"

# Registry consistency, with the manuscript and the paper's glossary (DR-028)
python -m tools.check_registry papers/<name>/vv/claims/claim_registry.md --manuscript papers/<name>/manuscript.tex --glossary papers/<name>/glossary.md

# Edit one registry row safely (exactly-one-match guard)
python -m tools.registry_edit papers/<name>/vv/claims/claim_registry.md S5-18 --append "Full text read 2026-10-08." --dry-run

# Offline DOI parse-check (no network)
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md --offline
```

Or via the project Makefile:

```bash
make coverage      # report against Paper 1
make check-dois    # DOI verification against Paper 1
make check         # lint + tests
```

Repo-maintenance checks are shell scripts in `scripts/`, not `tools/`: `make drift` (framework stamps, 0/1/2), `make dr-status`, `make gotcha-stats`, `make check-counts` (CHANGELOG counts, 0/1/2), `make read-surface` (`*.md` in maintainer-local `memory/` and `docs/work-items/` outside `archive/` vs a 100k-character budget, 0/1/2), `make check-profile` (the gitignored review profile's invariants, 0/1/2).

## Exit codes

All seven tools share a code-space (0 / 1 / 2 = success / failure / tooling error) but **default behavior differs**: `coverage.py` only fails the build under `--strict`; `check_dois.py` fails by default whenever a DOI does not resolve. The asymmetry is intentional — coverage targets are policy-configurable and may legitimately be missed mid-draft, while a DOI that fails to resolve is unambiguous.

| Code | `coverage.py` | `check_dois.py` |
|------|---------------|-----------------|
| 0 | Report emitted (always, unless `--strict` fails) | All DOIs resolved (or, with `--offline`, all DOIs parseable) |
| 1 | `--strict` and at least one target missed, the P0 tier floor failed, a row is UNCLASSIFIED or has an ID no pattern accepts, or only declared starting points were found (nothing evaluated) | At least one DOI failed to resolve (or, with `--offline`, failed to parse) |
| 2 | Tooling error (file missing, parse failure, near-miss marker) | Tooling error (file missing, parse failure) |

| Code | `check_quotes.py` | `registry_edit.py` | `check_experiments.py` |
|------|-------------------|--------------------|------------------------|
| 0 | Every quote found | Row edited (or, with `--dry-run`, would be) | Every entry passes |
| 1 | At least one quote not found, or found only as CHECK (a lenient reading) | Refused: no match or several, OLD not in the statement, or `\|` / a line break in new text | At least one FAIL: schema, artifact, or a metric not found in its evidence |
| 2 | Tooling error: source or quotes file unreadable, unsupported type, no text layer, a quote under three words | Registry unreadable or unwritable | Registry unreadable, git cannot run, or not a git work tree |

**The P0 tier floor is reported separately from coverage.** DR-002 requires every P0 entry
to be SUPPORTED or ESTABLISHED. The coverage table counts the Status column only, so a
registry can be 100% verified while most of its P0 entries sit below the floor — Paper 1 is
exactly that case (7 of 8 below, [#38](https://github.com/ducroq/agent-ready-papers/issues/38)).
The floor gets its own line under the table (`P0 tier floor … N of M meet it — FAILS`, naming
the failing IDs) and its own `p0_tier_floor` object in JSON, and `meets_targets` stays
coverage-only; `--strict` fails if either does. N and M count **entries, not rows**: an ID
registered in two sub-tables is one entry, and fails if any copy is below the floor. Three
cases are deliberately *not* skipped: a P0 row whose Confidence cell is empty or absent
**fails** the floor; a decorated `**P0**` priority is still P0; and a P0 row with a blank
Status is still on the floor, and coverage counts it as unverified. A registry with no P0 entry
at all prints `NOT evaluated` (JSON `evaluated: false`) rather than `0 of 0 … meets`. **DR-027:** every contribution is P0
whatever its Priority cell says, and enters the floor at its **effective tier**: its own tier capped by the weakest
`claim:` item in its Rests on (direct items only), so `--strict` alone fails a contribution resting on an EMERGING claim;
a referenced claim that is missing or has no readable tier fails the floor too. Declared starting points are excluded
and counted apart. A DR-027 registry with no contribution rows gets a `Note: no contributions registered` line.
JSON gains `declared_starting_points` (`total`, `verified`), `deprecations`, `unclassified`, `unmatched_ids`, `notes`
and `evaluated_nothing`; existing fields are unchanged. Like everything here this checks
**consistency, not correctness**: it compares the registered tier to the floor, never whether
the registered tier is right.

**`--offline` note.** ⚠️ This said *"check_dois only"* until 2026-09-14 and was wrong:
`check_metadata.py` has `--offline` too. Both print a stderr banner so an inherited flag
is visible.

- **`check_dois.py`** — offline does *not* mark DOIs as resolved. It checks parseability
  only and gates exit on `all_parseable` instead of `all_resolved`, so a CI gate over
  `all_resolved` cannot silently pass if the flag is inherited unintentionally.
- **`check_metadata.py`** — offline compares **no fields at all**, so there is nothing for
  `--strict` to be strict about. The two flags together are **refused** (exit 2) rather
  than returning 0. Until 2026-09-14 `--offline` returned before `--strict` was consulted,
  so a CI step inheriting it could never fail — the exact hazard the `check_dois` half of
  this note was written to prevent, reproduced in the sibling tool.

`check_metadata.py` also accepts `--json`, `--timeout` and `--mailto` (opt-in; no default).

## `check_metadata.py` — field-level verification

`check_dois.py` asks *does this DOI resolve*. `check_metadata.py` asks the question that one cannot: **does the entry attached to that DOI describe the paper it resolves to.**

The gap is measured, not hypothetical. Rao & Callison-Burch (COLM 2026, arXiv:2604.03159) benchmarked search-enabled frontier models generating BibTeX across 931 papers: **83.6% field-level accuracy, but only 50.9% of entries fully correct**, with accuracy falling 27.7 points on recent post-cutoff papers. The dominant failure is a *real* paper carrying corrupted metadata — wrong authors, year, or venue — which passes a resolution check cleanly every time. A green `make check-dois` is therefore weaker evidence than it reads as, and always was.

```bash
python -m tools.check_metadata papers/perspective/references.bib      # or: make verify-bib
python -m tools.check_metadata <registry.md>                          # or: make check-metadata
```

**Two input modes, chosen by suffix.** A `.bib` file gets strict field-by-field comparison (title, year, author, venue). A `.md` registry gets a looser proximity check: the year and author surnames in the prose captioning a DOI must match the record. Registry mode deliberately does **not** check titles — see Known limits.

**Three verdicts, mapped to the two failure shapes Rao & Callison-Burch identify.** *Wholesale substitution* (the DOI belongs to a different paper) trips title, year and author together. *Isolated field error* (right paper, one field wrong) trips exactly one. `WARN` covers differences that are normal rather than wrong — venue abbreviation, a missing co-author, a title whose subtitle is truncated.

| Exit | Meaning |
|------|---------|
| 0 | no MISMATCH (WARN allowed, unless `--strict`) |
| 1 | at least one MISMATCH, any WARN under `--strict`, or a DOI with no record at either agency |
| 2 | tooling error (file missing, no DOIs found) |

**Registration agencies.** Crossref first, DataCite on a 404. Not incidental: arXiv registers under the `10.48550` prefix with DataCite, so a Crossref-only lookup reports every preprint as unverifiable — exactly the entries most worth checking in an arXiv-first literature. DataCite records carry a *publisher* (`arXiv`) rather than a venue, so venue scores there are near zero by construction and the report says so inline.

**`--mailto` is opt-in.** Crossref asks consumers to identify themselves for priority routing. Nothing is sent unless you pass the flag: an email address is the caller's to disclose, not the tool's to send.

## `check_registry.py` — internal consistency

Five checks over a registry and its manuscript. All five are **internal consistency** — comparisons between two artifacts the author controls. None touches the question a rule cannot decide.

That line is the whole design, and it is worth stating precisely because the two halves are easy to conflate:

| Question | Decidable? | Where it lives |
|----------|-----------|----------------|
| Is the registered tier right, given the evidence? | No — judgment | Step Z, a human-and-agent pass |
| Given the registered tier, is the premise graph consistent with it? | Yes | Here |
| Given the registered tier, is the prose consistent with it? | Locatable, not decidable (span attribution is unsound) | Step Z, by hand. A locator was proposed in DR-021 and withdrawn 2026-10-12, never built |

`docs/framework-summary.md` states tier-monotonicity as *"prose language tier ≤ the registered confidence tier for the same entry"* — the form in the last row. This tool implements its graph analogue (the middle row), not the prose rule itself.

```bash
python -m tools.check_registry <registry.md> [--manuscript <file.tex>] [--budget N] [--glossary <glossary.md>]
# or: make check-registry
```

With `--manuscript`, files pulled in by `\input` and `\include` are read as part of it, resolved from the manuscript's directory and any `\input@path` it sets with `\def` ([#58](https://github.com/ducroq/agent-ready-papers/issues/58)). An input that does not resolve, or that would loop, is a note. Findings name the file and line inside an input. `\subfile`, `\import` and `\InputIfFileExists` are not followed, and an `\input` inside `\iffalse` is still read. A sub-table marker covers only the table directly under it, as in `coverage.py`; an unmarked table further down (the template's `## Out of Scope`) is not read ([#50](https://github.com/ducroq/agent-ready-papers/issues/50)). An entry row cut off from its table by a blank or comment line, with no heading between, is a `schema` finding, since neither tool reads it.

| Check | What it decides | Needs |
|-------|-----------------|-------|
| `anchors` | Every `% S#-#:`, `% S#-#a:`, `% C#:` and `% D#:` anchor has a registry row, and every row has an anchor. A `% D1: label (KIND, CONTESTEDNESS)` anchor must agree with the D row's Kind and Contestedness (first word, case-insensitive); D anchors carry no tier, so they get no tier comparison and no "no parseable tier" note | `--manuscript` |
| `tiers` | Every copy of an ID's confidence tier agrees — registry sub-table rows (an ID may appear in more than one), manuscript anchors `% S1-1: text (TYPE, P0, TIER)`, and a LaTeX `tabular` whose header row has a Confidence column. Case-insensitive, so a printed "Emerging" matches "EMERGING". One finding per disagreeing ID, naming each copy and its line. **A disagreement says the copies differ, never which one is right** | `--manuscript` |
| `schema` | DR-027 tables: Says is descriptive or normative; every Grounds / Rests-on item is typed and non-empty (`own:` names its method); `claim:` grounds need a Warrant; a normative claim needs a Rebuttal (boundary conditions), a normative contribution a Who/Where/When, and both a `decl:` item whose D row's Kind is `value`; a contribution's Priority is P0 and its Rests on holds no `src:`/`own:`; a D row's Kind is assumption/definition/value and its Contestedness accepted/contested/own; each table holds its own ID prefix. Any table: a duplicate ID, a row with more cells than its header (an unescaped `\|`), a near-miss marker, and a DR-027-shaped table under a DR-004 marker are findings; a row with content whose ID matches no pattern is a finding in a DR-027 table and a note in a DR-004 table. DR-004 tables keep their type-conditional columns: ARGUMENT rows carry Grounds/Warrant/Rebuttal, PROPOSITION rows carry Constructs/Relationship/Premises/Reasoning/Boundary conditions/Alternatives. **Presence only, never quality** | registry |
| `premises` | Every referenced premise exists and is verified; the graph is acyclic; and **no conclusion sits at a higher tier than its weakest premise**. In DR-027 tables the edges are `claim:` items (Grounds, and a contribution's Rests on, so a contribution's tier may not exceed its weakest claim); `decl:` items must resolve to a D row and are not edges; `src:` and `own:` items are not references. In DR-004 tables only `S#-#` IDs in Grounds / Premises are read | registry |
| `budget` | Word count against a declared budget — a Hard Constraint previously checked by eye | `--manuscript` + `--budget` |
| `glossary` | DR-028: the paper's glossary exists, is readable, is not empty or whitespace, and contains none of `templates/glossary.md`'s placeholders (`[Title]`, `[term]`, `[definition]`, `[Domain …]`, …). Without the flag the report says `glossary: not checked`, which is not a finding | `--glossary` |

The premise tier check is the one worth having. It is tier-monotonicity applied to the argument graph rather than to prose, and unlike the prose form it is fully decidable: if `S5-1` is registered ESTABLISHED while a premise it names is EMERGING, that is a defect no reading of the sentence will reveal.

**Counts lead the report, deliberately.** Per `docs/verification-hooks.md`, a check that cannot be told apart from an absent check is not a check, so every run prints what each check examined before what it found. A file with no recognised sub-table marker raises rather than passing, since nothing was parsed and a vacuous clean run would be indistinguishable from a parse failure. Recognised markers over empty tables — a freshly started registry — are not an error: the registry-only checks (`schema`, `premises`) examine 0, while `--manuscript` checks still run against the manuscript.

| Exit | Meaning |
|------|---------|
| 0 | no findings (notes allowed) |
| 1 | at least one finding (including a glossary finding) |
| 2 | tooling error (registry or manuscript missing, no recognised sub-table marker) |

## Known limits

Documented here so adopters hit informed surfaces rather than silent miscounts. None are blockers for the current Paper 1 fixture or the canonical templates; each is captured for the next adopter.

- ~~**Escaped pipes in cells (`\|`) are not supported.**~~ **Fixed 2026-06-12.** `_split_row` in `coverage.py` now honors backslash-escaped pipes (`\|`) — common in magnitude notation like `|H(z)|` — restoring them as literal `|` in the cell value instead of splitting the row into spurious columns. Regression tests in `tests/test_coverage.py` (`test_split_row_honors_escaped_pipes`, `test_parse_registry_counts_correctly_with_escaped_pipes`). Found by dog-fooding the tool on the math-heavy dsp-workshop z-domain registry, where the old behavior silently miscounted coverage (read 5/7 where the data was 8/8).
- **No HTTP proxy support.** `check_dois.py` uses `http.client.HTTPSConnection` directly and does not honor `https_proxy` / `HTTPS_PROXY`. This is fine for CI runners and most direct connections; fails opaquely for adopters behind a corporate proxy. If this matters, switch the HEAD path to `urllib.request` (which respects proxy env vars).
- **Sequential, single-retry HTTP.** No concurrency, no backoff. ≤20 DOIs runs in single-digit seconds; ~50 DOIs takes ~30s; 200+ DOIs becomes minute-scale. Concurrency is a follow-up, not a current need.
- **A marker whose table cannot be read is an error (exit 2), not an empty sub-table.** Since 2026-09-26, `coverage.py` raises when a `**CLAIMs:**`-style marker is followed by prose or end of file, or by a table with no Priority (or, for PROVOCATION, Tier) column or no Status column. A file in which **no marker is recognised at all** is an error too, in both `coverage.py` and `check_registry.py`. For that test only, a marker inside a fenced code block or an HTML comment is an example and does not count; quoting never affects which rows are parsed, so a stray `<!--` in a cell cannot hide a sub-table. Recognised markers over empty tables — a freshly started registry — report zero rows cleanly, and `--strict` then exits 0 with the P0 floor `NOT evaluated`. Until then an unreadable sub-table was skipped in silence, dropping its rows from coverage **and** the P0 tier floor: renaming every `Priority` header turned `--strict` green on Paper 1, whose floor genuinely fails. A marker the regex does not recognise (`**CLAIMS:**`, `### **CLAIMs:**`; `**Claims:**` is a DR-027 marker since v5.0.0) used to drop *its* sub-table silently while the others parsed; since v5.0.0 such a near-miss is an error in `coverage.py` and a finding in `check_registry.py`. The DR-027 names are case-sensitive, but a near-miss of any known name is caught. Still open: deleting a row, which no parser can see. Closed the same day: a row with content but a blank Priority is an error too — only a section divider may lack one, meaning nothing after its first cell and that cell not an `S#-#` entry ID, so `| S2-1 |` is not a divider at any width (an ID the pattern misses, like `S2-1 (dup)`, still is); a blank Status counts as unverified instead of leaving the denominator; priority buckets normalise (`p0`, `**P0**` → `P0`), and a bucket that is neither P0/P1/P2 nor a configured target (`-`, `TBD`) fails `meets_targets` and shows `NO — not a priority`. See `docs/verification-hooks.md`.
- **Marker recognition is line-anchored.** `_MARKER_REGEX` requires the sub-table marker on its own line. A heading-form marker like `### **CLAIMs:**` is not recognised; since v5.0.0 it is reported as a near-miss marker (exit 2 in `coverage.py`, a finding in `check_registry.py`) rather than skipped. Keep markers on their own line per the templates, and put a marker above every table: a `## Claims` heading alone does not open one.
- **`check_metadata.py` registry mode does not check titles.** A registry cell cites a source; it does not quote its title. Comparing the two warned on 8 of 9 correct rows in this repo's own registry on first run, and a check that fires on almost everything teaches people to ignore warnings. Titles are checked in `.bib` mode, where a title field exists to be wrong.
- **`check_metadata.py` reads years off the line with the DOI removed first.** Many DOIs embed their year (`10.5465/amr.1989.4308371`), so a cell misciting Whetten 1989 as 1991 still contains "1989" inside the DOI. Stripping the DOI before the year scan is what makes the registry-mode year check work at all; caught by `test_registry_mode_flags_a_wrong_year_in_prose`.
- **`check_metadata.py` trusts the registration agency.** Crossref and DataCite records are themselves occasionally wrong (Crossref stores Gregor 2006's title with a trailing footnote marker, `...Information Systems1`). The tool reports the disagreement; deciding who is right stays with the human. WARN rather than MISMATCH exists for exactly this.
- **Sequential HTTP, no concurrency** in `check_metadata.py` too, and each entry costs one or two requests rather than one. A 14-entry bibliography takes a few seconds; a 200-entry one is minute-scale.
- **`check_registry.py` word counting is approximate.** It counts `\input` files too, so an input macro or table file adds to it. Comments, math environments, floats and macros are stripped; everything else counts. It reports ~3,322 words for Paper 1 where `CLAUDE.md` says ~3,450. The budget is a threshold with slack, so a stable approximation is worth more than a precise figure that disagrees with whatever the target venue counts — but do not quote the tool's number as the submission word count.
- **`check_registry.py` schema checks presence, not quality.** A Warrant column containing the word "because" passes, as do an `own:` item naming any method and a Rebuttal holding any boundary condition. Whether the warrant licenses the inference is the ARGUMENT verification procedure's job and stays with a human. The check is worth having anyway: an empty Warrant is a defect the eye skips over in a wide table.
- **`check_registry.py` tiers reads only what it can parse.** Registry rows, anchors, and a LaTeX `tabular`, `tabular*`, `tabularx` or `longtable` whose header — the first row with two or more cells, one containing "Confidence" — names the column. Other table environments (`tblr`, `tabu`, `array`, `NiceTabular`) are ignored, and prose tables in files the manuscript does not `\input` (a writing guide's tier table, say) are not copies it sees. Within a table: rows end at `\\`, `\\*`, `\\[len]` or `\tabularnewline`, so wrapped rows and two rows on one line parse; wrapping macros (`\texttt{S1-2}`, `\textsc{Emerging}`), `\footnote`/`\cite`/`\ref` arguments, inline math, `\multirow`'s layout arguments, row-leading `\hline`/`\cline`/`\cmidrule`/`\rowcolor`, `\multicolumn` spans, escaped `\&` and `\%`, and LaTeX-typed ID dashes (`S2--1`, a pasted en-dash, `S1\-1`, `S1$-$1`) are handled. A caption or group header above the real header is passed over **unless** it has two or more cells and one contains "Confidence" — so a *data* row mentioning "confidence" in a table with no Confidence header is misread as the header, and the false findings that follow are loud, not silent. A Confidence header spanning several columns is ambiguous and the table is noted, not read. **Nested tables are not supported**: the table is noted and rows after the nested table's end are not read. Tables inside comments or `verbatim`/`lstlisting`/`minted` are ignored. The backstop is that every entry ID occurring in a Confidence table's body yields a copy or a note, so a row form none of the above anticipates is reported rather than lost; its cost is a note for an ID mentioned in passing (`\footnote{formerly S1-3}`). Tier-cell residue it does not strip (`\(n=3\)`, a trailing `\%`) shows up as a false disagreement, again loud. Pathological input (hundreds of thousands of `%` on one anchor line, an unclosed `\\[` repeated through megabytes) is quadratic; a 5 MB manuscript of ordinary text takes well under a second. **Anchors:** the tier is the last element of the *first* parenthesis followed only by whitespace or a `% comment` — so `(CLAIM, P0, SUPPORTED) % raised from (…, EMERGING)` reads SUPPORTED, and a `%` before the parenthesis (`100% of …`) is prose. `(CLAIM, P0, SUPPORTED, see §3)` reads `see §3` and reports a disagreement. An anchor with fewer than three elements, or a table row too short to reach the Confidence column, is a note, not a skip. `Examined` counts only IDs with at least two copies compared, and when it is 0 a note says the check compared nothing — a note rather than a finding, because the templates do not yet prescribe the tier in anchors. It exists because the copies drifted before: eight Paper 1 registry tiers were raised without touching their anchors, and the two disagreed for six months ([#37](https://github.com/ducroq/agent-ready-papers/issues/37)). The first remediation made them agree **in the wrong direction**, which is exactly what a consistency check cannot see.
- **`check_registry.py` anchors require the `% S#-#:` colon form.** A section header comment like `% Registry entries: S4-1, S4-2` is deliberately *not* counted as an anchor — counting it would have concealed the finding the check was written to surface.
- **`_clean_doi` is heuristic.** For DOIs whose authoritative form ends with unbalanced punctuation (vanishingly rare in real Crossref data), the cleaner may strip too much. Run a spot-check against the publisher's canonical citation if a DOI fails to resolve unexpectedly.

## Design constraints

- **Stdlib only.** No `requests`, no third-party YAML / Markdown libs. Keeps the toolchain trivial to install and free to vendor.
- **Deterministic.** Same registry input → byte-identical report. Result types use `frozen=True` dataclasses; ordering is stable.
- **No LLM step.** Registry format is author-controlled markdown; a regex parser suffices. (Pattern borrowed from the ADR-016 floor-check discipline in a sibling project, private.)
- **Importable and runnable.** Both modules expose a `check_*` function in addition to the CLI, so tests can call them directly.

## File-naming note

The issue title uses `check-dois.py` <!-- placeholder --> (hyphenated). The actual file is `check_dois.py` (underscored) so Python can import it as `tools.check_dois`. The CLI is invoked via `python -m tools.check_dois` either way.

## Licensing

Tools live inside the agent-ready-papers repo and inherit its licence (CC BY 4.0). If `tools/` grows substantially, [DR-013](../decisions/DR-013_license-choice.md) carries a "Revisit If" condition for re-examining a dual CC BY 4.0 + MIT split.

## Roadmap (post-scaffold)

1. Implement `coverage.py` sub-table parser. Tests against `papers/perspective/vv/claims/claim_registry.md` (19 entries, 100% verified — known-good fixture).
2. Implement `check_dois.py` extractor + resolver. Tests against the same fixture; offline mode verified against a hand-curated DOI/non-DOI fixture file.
3. ~~PROVOCATION axis support in `coverage.py`~~ — **done.** `axis="provocation_tier"` buckets GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL (see [DR-010](../decisions/DR-010_provocation-unit-type.md), [DR-014](../decisions/DR-014_provocation-layered-as-opt-in-extension.md)). Note the rows are *reported but not gated* unless `provocation_targets` is supplied, so `--strict` gates them on neither axis by default.
4. Add `tools/` to repo CI once a real fixture suite exists.
