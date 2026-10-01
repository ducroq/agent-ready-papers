# Changelog

All notable changes to `agent-ready-papers`. Adopters can check their paper project's framework version against this log to see what has changed. Releases before v4.0.0 are in [`CHANGELOG-archive.md`](CHANGELOG-archive.md).

<!-- Maintainer release process. Full steps: the project-local /release skill (Step 6 hands
     over the tag commands; Step 7 runs after the push). It cites step 2 by number:
     1. Tag annotated (`git tag -a vX.Y.Z <commit> -m "vX.Y.Z"`; a lightweight tag has no tagger,
        date or message) and push the single ref
        (`git push origin vX.Y.Z`), never `git push --tags`, which publishes every local tag.
     2. Cut a GitHub Release from the tag (`gh release create vX.Y.Z ...`) linking back here.
     3. Add the adopter-action rows to UPGRADING.md under the new version.
     Versioning (semver, mirrors agent-ready-projects): MAJOR breaks template surfaces or DR
     semantics; MINOR adds templates, patterns or behaviours; PATCH is docs, clarifications or a
     backward-compatible fix. Every entry has an "Adopter notes" or "Adopter action" subsection,
     saying "No adopter action required." when there is none. -->

## Unreleased

### Tooling (this repo's maintenance)

- **New `make check-counts`** (`scripts/check-counts.sh`): checks the counts stated in the top CHANGELOG section against the repo. A `` `path` A → B characters `` claim must match the file now; "N tests" must match the collected tests of the one module the item names; "the suite went from A to N" must match the whole suite. Exit 0 all match, 1 stale, 2 cannot verify. A count in a near-miss shape (an ASCII arrow, "chars", a "k" abbreviation, "added N tests") is reported UNPARSED and exits 2, and so does a section with no counts. It narrows stale counts; it does not close them: a count spelled out, or in a table cell, can still pass. Three review rounds. The shapes seeded in review are now `tests/test_check_counts.py`, one case per shape with its expected exit; removing either fail-closed branch turns cases red. The test suite now takes seconds rather than under one, since each case runs the script. `/release` Step 4 runs it on the new entry (project-local skill, gitignored).
- **New `make read-surface`** (`scripts/read-surface.sh`): characters in every `*.md` under `memory/` and `docs/work-items/` outside `archive/`, the set `/curate` Step 0 measures, against a budget (`READ_SURFACE_BUDGET`, default 100,000). It lists each file over 10,000, largest first. Only regular files count, as with `find -type f`: symlinks, FIFOs and sockets are skipped. Exit 0 within budget, 1 over, 2 cannot verify (no surface or no files, an unreadable directory or file, a non-UTF-8 file, a bad budget, a crash, `python3` missing). `tests/test_read_surface.py` seeds each exit, and removing any one guard in the script turns a case red (each ablated in review). Across this section the test suite went from 274 to 364.
- DR-023's proposed path for kept report sources is now `docs/work-items/archive/reports/` (in the DR, `extensions/translation-prompts.md` and `tests/test_preservation_check.py`), so test data stays out of session reading.
- **New `make check-profile`** (`scripts/check-profile.sh`): checks the gitignored review profile (`.claude/review-profile.md`) four ways. Every guarantee's winning tier (the most specific matching pattern, as the profile states) is HIGH, every HIGH pattern has a guarantee, a tier pattern whose base path is gitignored is listed in the profile's *Ignored paths* table, and every Makefile target and script is named in backticks in the guarantee section. A guarantee glob is tested as a sample path, so one broader than its HIGH pattern is caught. A bare directory pattern is asked about both as a file and as `dir/`, because a rule like `audits/` misses a bare `audits` that does not exist. Limits, stated in the script header: a pattern whose files are only partly ignored is not flagged, and one starting with `*` is reported as unchecked. Exits 0 / 1 / 2; each guard has a case in `tests/test_check_profile.py` that a 2026-10-01 ablation turned red. It settles three of the gotcha log's proposed Mechanized rows; three others were rejected (caveat anchors, literal versions in probes, a general `ablate.sh`).
- All six scripts find the repo root from their own path, so they work from inside `memory/` (its own git repo, where `git rev-parse` returned the wrong root) and with `CDPATH` set. `make gotcha-stats` also exits 2 on a crash or a non-UTF-8 log.

### Docs

- `README.md` loses its inline edit histories (version provenance notes, the 2026-09-14 "whole-registry verification" correction, and R-4's dated retier note: R-4 went SUPPORTED → EMERGING on 2026-08-13) and a restated thresholds paragraph; the per-project adjustment advice moves to the *Quality Gates* note. R-5's boundary says "observed" instead of "demonstrated", which an EMERGING row may not use.
- **Release history split at the current MAJOR (P23, #40).** v3.0.0 and earlier moved word for word to `CHANGELOG-archive.md` and `UPGRADING-archive.md`. `UPGRADING.md` 61,512 → 7,281 characters; `CHANGELOG.md` shrank from ~149k to ~27k (it grows with each entry). The release-process header comment is shorter; the steps `/release` cites by number keep their numbers. Adopters pinned before v4.0.0 read the archive from their pin up to v3.0.0. Two links in `agents/README.md` now point into the archive.
- P16 leftovers from the 2026-09-14 review battery. DR-021 no longer contradicts itself: its Context and Option A's con name the *prose* half as unsupported (the graph half has `check_registry.py`); the `S4-*` line no longer says all rest on tier F (three were withdrawn, S4-3 cites PeerArg and Gupta); the prediction that acceptance would break the DR-count probe is replaced, since the probe counts files. `tools/README.md` splits the decidability row: the premise graph is checked here; the prose is locatable but not decidable, and only proposed (DR-021). `literature/sources/equator-gap.md` hedges two claims about four unread guidelines. `literature/README.md` names GhostCite's authors (Xu et al.). `topaz-2026.md` adds the ratios the stated rates give (6.2×, 10.2×) beside the press figure of ~12-fold.
- `docs/verification-hooks.md`, *The adjacent measurement*: adds the follow-up count (adjacency in 4 of 64 findings over three review batteries, about 6%, or 5 with a borderline case). The shape stays EMERGING; the count is a share of findings, not a recurrence rate.
- New `docs/adopter-feedback/argument-project-2026-09-14.md`: feedback from an argument-shaped adopter (v3.0.0), in a generic form. Four findings: PROVOCATION scoped to one device with an abuse tripwire, a deliberative gate turned into a search, **internal evidential contradiction** as a possible sibling of §4.6 scope drift, and a rule-versus-prose ledger. Not yet filed as issues.

### Adopter notes

No adopter action required. `check-counts.sh` and `read-surface.sh` read this repo's own layout.

## v4.1.0 (2026-09-30)

Readability joins verification. A new optional template gives two prompts against compressed, hard-to-read AI prose. Two Proposed decisions stage tools for it: DR-022 (formula repetition as a readability lens, never a detector) and DR-023 (a translation step where agent text reaches a person, with a check that the rewrite kept its numbers and certainty). A token-economy pass cuts what a session reads at start from ~107k characters to ~19k. **MINOR**: new template and DRs, nothing an adopter must do.

Fourteen commits since v4.0.0: the readability template, two Proposed DRs with staged tools in `extensions/`, 25 literature IDs (L67–L91), three maintenance scripts, a companion adoption (pin v1.42.0 → v1.49.2), and Paper 1 P0 work. The test suite went from 173 to 274.

### Templates

- **New `templates/readability.md`** (optional). *Explain like I'm 18* states problem, findings, conclusions and next steps in full sentences, with how sure each conclusion is. *Write for a reader* sets rules for manuscript prose: one idea per sentence, a concrete subject, the point stated outright at the strength its registry tier allows, and a tier guard that overrides every other rule. A three-step workflow and two worked before/after examples.
- **`templates/CLAUDE.md`**: one tree line for `readability.md`.
- **`templates/hypothesis-log.md`**: once the log grows long, resolved entries may move to a separate `hypothesis-log-resolved.md`, leaving a pointer under `## Resolved`. Optional.

### Decisions

- **DR-022 (Proposed): formula repetition as a readability lens, not a detector.** It records, for adopters, the decision to keep AI-text detectors out of every gate. Revised on the readability literature: H1 is narrowed to expert or repeat-exposed readers from the intended audience; a multi-file mode (not yet built) is required before acceptance; engagement-marker density is proposed (not built) for the academic profile; the Evidence Base records that triads, "not X but Y" and rhythm rest on one source (L72).
- **DR-023 (Proposed): two registers, and a translation step where text reaches a person.** Files an agent reads stay compact. Generated text a person reads (reports, CHANGELOG entries, issue bodies) is rewritten in a fresh context, with what the reader must decide first; a translation of a DR or paper is a proposal the author approves. A two-part check reports and never gates. Acceptance test: 10 real reports, two raters, partly blind (#42).

### Extensions (staged, not accepted)

Staged in `extensions/` under the DR-018 precedent; each file carries a PROPOSED banner.

- **DR-022**: `formula_scan.py`, an advisory locator for rhythm, paragraph uniformity, negation-contrast turns, triad share, stock style words with per-item provenance, recurring phrases and openers, and section-template features. It exits 0 whenever it reports (2 on a tooling error), is English-only and says so, and handles LaTeX only for `.tex` files. `formula-review.md` is a judgement pass that never judges authorship or truth; `effect-profiles.md` a voice layer with a device register and five effect profiles. `make formula-scan`. 42 tests, each signal seeded both ways. First run on Paper 1: "to our knowledge" recurs in 8 paragraphs.
- **DR-023**: `preservation_check.py` compares a source text with its rewrite. It reports numbers and ISO dates that went missing or appeared, and tier words that went missing or moved up a band (read at run time from the Language Calibration table in `templates/writing-guide.md`; exit 2 if the table cannot be read). Beyond the DR, it also reports dropped hedges and added absolutes, and says so. Numbers are checked for presence only: two numbers that swap places pass. `translation-prompts.md` holds Prompt T (rewrite for a person, decision first, only if the source asks for one) and Prompt C (list the assertions a rewrite adds or drops, which the script cannot see). `make preservation-check SRC=… TRN=… [LINK=…]`. 59 tests, including one that pins the blind spot Prompt C covers. A one-report pilot: the script raised 1 flag; Prompt C found 5 items, two of them errors the script cannot see ("not refuted" rendered "passed", and a miscount).

### Docs and README

- **README, Common Questions: "Will an AI-text detector flag my paper?"** Detector accuracy is condition-dependent and was biased against non-native writers in a 2023 pilot; the policies read judge disclosure; keep the verification record as the answer to a flag.
- **`CLAUDE.md` 34,670 → 11,570 characters.** Edit histories and restated counts are removed; instructions, Key Paths and every Hard Constraint's operative clause stay (a review lens checked them clause by clause, and restored five it found weakened). New Hard Constraint, *Token economy*: cut at least as much as you add, and keep no edit histories in per-session files.
- **`vv/hypothesis-log.md` 34,521 → 19,199 characters**: its two resolved entries move word for word to `vv/hypothesis-log-resolved.md`; `docs/THRESHOLDS.md` points there.
- `tools/README.md` notes that repo-maintenance checks live in `scripts/`.

### Tooling (this repo's maintenance)

- **New `scripts/`**, replacing prose that went stale by hand; each exit path was exercised on a seeded fixture:
  - `make drift`: 0 no drift, 1 drift, 2 cannot verify. Checks the companion pin against the latest release, the global skills byte for byte against the reference install at the pinned tag, this repo's stamp against this file, and paper pins. A failed fetch, a missing pin tag or no clone gives 2, never 0. A tracked paper pinned behind counts as drift.
  - `make dr-status`: DRs grouped by the `status:` in their frontmatter.
  - `make gotcha-stats`: entry count and sizes.
- **`/release`** (project-local, gitignored): adopts the companion's `tagfree` check, and its coverage precondition now runs `tools.coverage --strict` instead of `make coverage`, which never enforced the thresholds.

### Literature

- **AI-text detection, L67–L82**: independent accuracy and bias evaluations, detector mechanisms, one vendor report (tier D), ICMJE/COPE/publisher policy, and the word-list provenance for `formula_scan.py` (L81 Kobak et al. 2025; L82 Wikipedia "Signs of AI writing", tier D). Step 0 passed for all; key figures re-checked against the PDFs.
- **Readability, engagement and homogenisation, L83–L91.** Lay readers preferred AI poems (L85); the formula penalty so far appears to come from expert readers (L72, L86, L88); AI assistance made texts by different authors more alike (L83, L84). Hyland 2005 and Sword 2012 are read only in part.

### Paper 1

- **P0 tier floor: 1 of 8 → 3 of 6** (#38). S4-1, S4-2 and S4-4 are withdrawn (no manuscript text); S5-1 is re-grounded on S2-1, S2-2 and S3-4. S1-4 is reworded against prior art and demoted to P1. S1-1 and S1-2 are now SUPPORTED, with new sources read in full. S2-2 is narrowed to "no published consensus-based guideline" and stays EMERGING. S3-4 and S5-1 are capped by tier-monotonicity, because their premises are EMERGING. **`coverage --strict` still fails on the floor** (S2-2, S3-4, S5-1), as disclosed at v4.0.0; this release ships over it.
- Framework pin v2.6.0 → v4.0.0; the v3.0.0 Required items were already in force.

### Companion adoption

| From | What | Landed as |
|------|------|-----------|
| agent-ready-projects v1.43.0 | `tagfree`: offline, no argument or an unsubstituted `vX.Y.Z` gives 2, never "free" | Project-local `/release` |
| agent-ready-projects v1.47.0 | Size signals: project file above ~15k characters, memory archive pass above ~300k | In force through the global `/curate` and `/audit-context` |
| agent-ready-projects v1.45.1 | Cheaper HIGH review tier | **Declined**: offered upstream as not the default (n=2), and it drops lenses this repo's tool guarantees rely on |
| agent-ready-projects v1.44.0–v1.49.2, other tags | Already in force, or PATCH with nothing to adopt | Pin only; the four global skills are byte-identical to v1.49.2 |

### Adopter notes

No adopter action required. Everything new is optional: `templates/readability.md` can be copied into a paper project, and the `extensions/` files stay staged until their DRs are accepted. If you copy the hypothesis-log template, the separate resolved file is an option, not a change you must make. The scripts in `scripts/` read this repo's own layout.

### Versioning rationale

Step 2 rule 1 does not fire: no existing consumer must act. Rule 2 fires on a new template (`templates/readability.md`) and two new DRs, so MINOR, following v2.6.0 and v2.5.0.

## v4.0.0 (2026-09-26)

The claim-registry tools stop trusting what they cannot read. `coverage --strict` now enforces DR-002's P0 confidence floor, and `coverage` fails closed on a registry it cannot parse instead of miscounting it. Two new tools check citation *fields* and registry/manuscript *consistency*. **MAJOR**, because a registry that passed `--strict` under v3.0.0 can now fail it with no change on the adopter's side.

Twenty commits since v3.0.0: a companion adoption (pin v1.25.0 → v1.42.0), two new tools, two Proposed DRs, nine literature sources, and three rounds of fail-closed work on `coverage.py` — from a review battery on the new tools, from #37, and from re-measuring the green-at-any-cost routes. #32 lands an agent rule. All tooling changes carry seeded-fail tests; the suite went from 20 tests at v3.0.0 to 173.

### Tooling

- **`tools/coverage.py` — DR-002 P0 tier floor** ([#37](https://github.com/ducroq/agent-ready-papers/issues/37)). Every P0 entry must be SUPPORTED or ESTABLISHED. Reported *separately* from coverage — a `P0 tier floor: N of M meet it` line under the table, a `p0_tier_floor` JSON object, `meets_tier_floor` on the report — because a registry can be 100% verified while its P0 entries sit below the floor, and Paper 1 is exactly that case (1 of 8 meets it, [#38](https://github.com/ducroq/agent-ready-papers/issues/38)). `meets_targets` stays coverage-only; `--strict` fails if either fails. A P0 row with no readable tier fails the floor; the count is entries, not rows.
- **`tools/coverage.py` — fails closed instead of miscounting.** Each of these used to be skipped in silence, dropping a row or a whole sub-table from the counts, and each was measured turning `--strict` green over an unverified claim. Now:
  - a row with **more cells than its header** (an unescaped `|`, including inside backticks) → exit 2;
  - a sub-table marker followed by prose, end of file, or a table with no Priority/Status column → exit 2;
  - a file with **no recognised sub-table marker** at all (e.g. only `**Claims:**`) → exit 2. A freshly started registry — recognised markers over empty tables — reports zero rows cleanly;
  - a row with content but a **blank Priority** (including one blanked down to its ID) → exit 2;
  - a **blank Status** → counted as unverified, where it used to leave the denominator;
  - a Priority that is not P0/P1/P2 or a configured target (`-`, `TBD`) → fails `meets_targets` (`NO — not a priority`); `p0` and `**P0**` normalise to `P0`;
  - a **short** row (a one-cell section divider) is padded as GFM renders it, where it used to end the table.

  Routes still open are measured and listed in `docs/verification-hooks.md`: deleting a row, P0→P1 into a bucket with slack, an ID the `S#-#` pattern misses, a miscased marker.
- **New: `tools/check_metadata.py`** — a resolving DOI is not a correct entry. Compares title, authors, year and venue against Crossref, falling back to DataCite (arXiv DOIs are not Crossref). Distinguishes a DOI that does not exist from one that could not be *reached*, and an entry where nothing could be compared from a passing one. Runs on `.bib` files (`make verify-bib`) and on registries (`make check-metadata`).
- **New: `tools/check_registry.py`** — internal consistency between a registry and its manuscript, never whether a tier is right: `anchors` (every `% S#-#:` anchor has a row and vice versa), `tiers` (every copy of an ID's tier — registry rows, anchors, a LaTeX table with a Confidence column — agrees; #37), `schema` (type-conditional columns present), `premises` (the premise graph resolves, is acyclic, and no conclusion outranks its weakest premise), `budget`. Unreadable copies are notes, never silent skips. Like `coverage`, it exits 2 on a file with no recognised sub-table marker and accepts a freshly started registry. `make check-registry`.

### Agents

- **`equation-checker.md` — derived op-counts, complexity and budgets are reproduced from the procedure, not the reported number** ([#32](https://github.com/ducroq/agent-ready-papers/issues/32)). Step 3 confirms a figure follows from its stated formula; a new Rule, a Step 3 pointer and a widened `FORMULA` description require that, for a *derived* operation-count / complexity / runtime / cost figure, the formula itself be rebuilt from the algorithm, pseudocode or experimental setup the document describes, within its stated counting convention. Measured figures are excluded. Motivated by an adopter pilot where the lens passed a self-consistent compute budget that counted a feature suite the real-time path never ran (true load 3x lower). Framed as correctness — a wrong-model figure is *false* — on the argument in #32's 2026-08-16 comment that this keeps it clear of the Option-B objection (DR-018, applied to circularity in DR-020). Deliberately limited to that case: entailed or circular results, and comparisons that are true but unfair, are out of scope.

### Templates

- **`templates/CLAUDE.md`** — the framework pin is "a number, not a status" (companion v1.34.0), and a *Before committing* row points at `/review-changes` or its paste-in prompt.
- **`templates/vv-framework.md`** — Gate 2's P1-tier-floor note now says `coverage.py` reads the Confidence column for the **P0** floor only; the P1 floor is still a manual check.
- **`templates/claim-registry.md`** — a comment now says prose between a marker and its table is an error, not a silent skip.

### Decisions

- **DR-020 (Proposed)** — circular evidence as a Step Z limb: a result entailed by its own inputs carries no evidential weight. Both the gap and the remedy are declared EMERGING.
- **DR-021 (Proposed)** — prose tier-floor scanning as a *locator*, not a gate.
- DR-015 and DR-019 carry notes (a mechanization argument; a probe that measured a CHANGELOG mention instead of an implementation). No status changes; only Accepted DRs bind.

### Docs

- **`docs/verification-hooks.md`** — a fourth failure mode, *the adjacent measurement*; the green-at-any-cost routes table re-measured against the new `coverage.py`, with open routes marked open.
- **`docs/THRESHOLDS.md`** — `--strict` also gates the P0 floor; a new scope section: the thresholds assume a self-authored project, and on a document the project did not write, what governs coverage is whether a claim can be closed without its author.
- **`docs/non-claude-setup.md`** — AGENTS.md as the cross-tool standard (companion v1.37.0); the *symlink or duplicate* advice withdrawn.
- **README** tools table names the new tools and checks.

### Also in this release

- **`vv/hypothesis-log.md`** (public) — the third-party-audit ceiling bet, registered and resolved **SPLIT** within three days by a second audit (headline prediction refuted; one mechanism held), with its successor positions registered.
- **`.gitignore`** — third-party full texts under `literature/pdfs/` are not tracked; and a publishing rule for `papers/*`: never allowlist a paper that critiques third-party work.
- **README** — `check_dois` is described as DOI resolution, not whole-registry verification.
- **Paper 1** (the repo's own demonstration paper) — eight claim tiers re-derived from DR-002 and lowered to EMERGING, with the manuscript's appendix table and the writing guide's Quick Reference rebuilt to match; a P0 summary cell that asserted an audit its row does not contain was corrected. The resulting P0-floor failure is #38.

### Literature

L57–L65 ingested (65 sources). They re-verify Paper 1's gap claim (EQUATOR now lists 704 guidelines, still no non-empirical category) and **falsify S1-4 as written**: L60 and L61 are process-level verification infrastructure for AI-assisted writing. The rewording is staged, not applied, because a P0 rewording is a human call. Third-party full texts are gitignored under `literature/pdfs/`.

### Companion adoption (agent-ready-projects pin v1.25.0 → v1.42.0)

| From | What | Landed as |
|------|------|-----------|
| v1.25.1 | Step 1.5's awk lacked CRLF handling: no table was examined on a CRLF checkout | Ported into the then-local `/review-changes` — a copy later found inert (shadowed by the global install) and deleted under v1.40.0. In effect only through the user-global install |
| v1.26.1 | Review baseline computed from `@{u}`, empty on a pushed unmerged branch | Same as v1.25.1 |
| v1.28.0 | Reference checker gains a doc-relative rung | Retired a standing caveat in `CLAUDE.md` |
| v1.31.0 | Adopter notes name marker strings, never only "re-copy it" (#94) | `/release` Step 4 (maintainer-local); applied in this entry |
| v1.34.0 | A version stamp is a number, not an adjective | `templates/CLAUDE.md`, `CLAUDE.md` stamps |
| v1.37.0 | AGENTS.md as a standard; symlink-or-duplicate withdrawn | `docs/non-claude-setup.md` |
| v1.40.0 | `/review-changes` user-global, with a per-repo `.claude/review-profile.md` | Profile written; inert local copy removed; skill-scope Hard Constraint rewritten |
| v1.41.0 | Gotcha log gains a `## Mechanized` table | Maintainer-local memory (no commit in this repo records it) |
| v1.27.0–v1.42.0 (whole range, including the rows above) | 19 releases triaged: 8 adopt, 0 decline, 2 not applicable, 9 already in force | Full record maintainer-local |

### Adopter notes

**New adopters** get tools that fail loudly on a registry they cannot read, a P0 floor that `--strict` enforces, and two checkers — field-level citation metadata and registry/manuscript consistency — that did not exist in v3.0.0.

**Existing adopters who run `coverage --strict` in CI must expect it to go red** in two ways — see `UPGRADING.md`:

1. **Any P0 entry below SUPPORTED now fails.** DR-002 always required this; nothing enforced it. Remedies are stronger sources, re-prioritisation, or an explicit decision record — not a waiver.
2. **A malformed registry now exits 2, with or without `--strict`.** Every case listed under *Tooling* was already a miscount; the error message names the line. One shape was harmless before and is now an error too: a section divider with a second cell, or a totals row inside a marked sub-table — move it outside. A blank Status now lowers coverage instead of vanishing. A freshly started registry is unaffected.

A copied or adapted `equation-checker.md` can take this surgically — add the Rule beginning `Reproduce op-counts, complexity and budgets from the procedure`, the Step 3 bullet beginning `For a derived operation-count`, and the `FORMULA` row's added clause `or counts work the described procedure does not perform`. Those three strings are the markers a current copy contains. No other adopter action.

The paper-local copies under `papers/*/` are not refreshed by this release; `templates/vv-framework.md` and `agents/equation-checker.md` changed.

**Known at release:** this repo's own Paper 1 fails the new floor (1 of 8 P0 entries at SUPPORTED or above; #38), so `/release`'s own `coverage --strict` precondition is red for a content reason, not a tooling one. That is the floor working. `check_registry` also exits 1 on Paper 1 for three unanchored entries (S4-1, S4-2, S4-4), whose prose was removed deliberately in an earlier revision; whether they remain in the registry is an open decision.

### Versioning rationale

**MAJOR.** Step 2 rule 1 fires: an adopter's `coverage --strict` can fail where it passed under v3.0.0, and a registry `coverage` used to read now exits 2 — both without any change on the adopter's side. Rule 1 outranks rule 2, so the new tools and DRs (MINOR on their own) do not decide it. Precedent is **v3.0.0**, which went MAJOR because "Gate 2's new P2 line can fail a paper that previously passed" — a requirement also already documented elsewhere, as DR-002's floor was here. The case for MINOR is on the record: every newly-red input was already non-compliant with DR-002 or already miscounted, so no *correct* registry changes result. It was weighed and declined, because rule 1 asks whether consumers must act to keep working, not whether they were right before.
