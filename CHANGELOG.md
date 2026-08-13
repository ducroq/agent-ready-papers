# Changelog

All notable changes to `agent-ready-papers`. Adopters can check their paper project's framework version against this log to see what has changed.

<!-- Maintainer release process:
     When promoting a `vX.Y.Z (candidate, unreleased)` block to a dated release:

     1. Tag the release commit:

         git tag -a vX.Y.Z <commit> -m "vX.Y.Z"
         git push origin vX.Y.Z

        `-a` because a lightweight tag carries no tagger, date or message, and
        `git describe` and release tooling treat the two differently. Push the
        SINGLE ref, never `git push --tags`: that publishes every local tag,
        including wip-* and private scratch tags, permanently. (This block said
        `git tag` + `git push --tags` through v2.5.0, contradicting the
        /release skill's Step 6 — which is the copy that actually gets
        followed. Corrected during the v1.19.0-v1.25.0 companion adoption.)

        Tags let adopters `git checkout vX.Y.Z` to inspect a pinned version and
        `git diff vX.Y.Z..vX.Y+1.0 -- templates/` to preview an upgrade.

     2. Cut a GitHub Release from the tag (gh release create vX.Y.Z ...) with a
        short summary + link back to this CHANGELOG entry.

     3. Add a row to UPGRADING.md under the new version section: one table row
        per change that requires pinned-consumer action, paired with the
        from-version it applies from. Adopters read UPGRADING.md sequentially
        from their pin down to latest.

     Versioning convention (mirrors agent-ready-projects):
     - MAJOR — breaking changes to template surfaces or DR semantics
     - MINOR — new templates, patterns, application classes, or behaviours
     - PATCH — docs-only changes, clarifications, cross-reference adds, and
       backward-compatible bug fixes (e.g. a tooling fix that changes no
       public interface and adds no capability — it makes the tool honor a
       contract it already documented). Per semver, which this convention mirrors.

     Adopter-notes convention:
     - Every release entry below MUST include an "Adopter notes" or
       "Adopter action" subsection listing what action (if any) pinned
       consumers need to take. UPGRADING.md aggregates these per version
       for quick lookup. If an entry has no adopter action, say so explicitly
       ("No adopter action required.") rather than omitting the subsection.
-->

## v3.0.0 (2026-08-13)

Repo-wide sweep of the shipped surface and the literature layer, and remediation of what it found. Three adopter-installed templates now oblige action, so **MAJOR** — the first MAJOR triggered by tightening rather than removal.

The sweep ran 10 reviewers over `templates/`, `agents/`, the README's normative sections and `literature/sources/`, with an independent adjudicator over the judgement calls and a full `/review-changes` battery over the remediation itself. The classification rubric was pre-registered before any file was read.

### Templates

- **`anti-hallucination.md` — the worked example was wrong, and is now a *failing* example.** It shipped as the demonstration of a *successfully verified* citation and failed its own check twice: a DOI that returns 404 marked `resolves | PASS`, and the CPR-manikin **device's** stiffness range (5.34–13.59 N/mm) attributed to **human chests**, marked PASS on Steps 4, 5 and 6. The paper's human figure is 4–10 N/mm, cited from its own reference [16]. Rewritten to score those steps FAIL and reject the citation as an attribution error — the failure mode the same file tabulates and previously demonstrated passing.
- **`anti-hallucination.md` — Step 0's decision rule replaced.** It required **both** Google Scholar *and* DOI resolution, which classified every source without a DOI as HIGH RISK — including Toulmin (1958), which underpins the ARGUMENT unit type; 12 of 25 entries in this repo's own `literature/sources/` carry no resolvable DOI. It now gates on DOI **presence**: a cited DOI must resolve, an absent one is not a failure. An interim fix made it a plain "either" and was refuted during review by a seeded positive built from this file's own worked example.
- **`vv-framework.md` — Gate 2 gains `P2 entries 70% verified`**, which `docs/THRESHOLDS.md` and the README already required. The P1 tier floor is split out as an explicit **manual** check: `tools/coverage.py` reads only the Status checkbox and never the Confidence column, so `--strict` reports that gate met for a registry whose P1 rows are all verified and all SPECULATIVE.
- **`CLAUDE.md` and `writing-guide.md` — the confident-language floor moves to below ESTABLISHED.** Four surfaces said "below SUPPORTED", permitting "demonstrates" *at* SUPPORTED — the exact drift a 2026-03 retrofit audit found in 6 of 22 entries, and contrary to the DR-002 mapping the same guide ships. The pre-submission checklist had the same hole, so it certified the violation it exists to prevent.
- **`claim-registry.md` — the PROVOCATION sub-table was invisible to `tools/coverage.py`.** A prose paragraph between the sub-table marker and its header made the parser abandon the table, so a speculative-design adopter's PROVOCATION rows were silently uncounted. Paragraph moved above the marker; a comment records why it must stay there.
- **`decision-record.md`** — the `status:` vocabulary gains `Partially superseded`, which DR-001 has used all along.

### Decisions

- **`DR-009` (Accepted, binding) — Key Insight corrected.** It read "the prompt matters more than the model … the *same* model prompted to reproduce", which is false against the record: vendor, prompt and inference mode all varied together (Gemini reviewing vs Claude Sonnet with extended thinking). Now states the observation with the confound disclosed. The decision itself — calculation verification as a distinct procedure — is unchanged.
- **`DR-019` (Proposed) — Step Z surface scope.** Names framework prose as an unstated axis in Step Z's scope. Carries an explicit `Implementation status: nothing implemented` section and a probe that fails if that changes silently, because a Proposed DR must not read as shipped.

### Agents

- **`equation-checker.md`** — the KEY INSIGHT block asserted a causal result the underlying N=1 observation cannot isolate. Reworded with the confound named; the operating instructions are unchanged and do not depend on resolving it.
- **`review-prompt.md`** — recommendation bands were `≥4.0` / `3.5–3.9` / `2.5–3.4`, leaving 3.4–3.5 and 3.9–4.0 unclassifiable. Paper 1 scored 3.95, landing in the second gap. Now `3.5–<4.0` and `2.5–<3.5`.

### Tooling

- **`check_dois.py`** — `_clean_doi` did not strip a trailing `}`, so every BibTeX `doi = {…}` field produced a false 404. Twelve of twelve DOIs in `papers/perspective/references.bib` reported as failures; all twelve resolve. Regression test added and mutation-tested against the unfixed implementation.
- **`tools/README.md`** — a dead DR link, and a roadmap item listing a feature that shipped.

### Docs

- **`THRESHOLDS.md`** — the 85% envelope's stated design property ("a project hitting its per-tier targets clears the overall threshold automatically") is arithmetically false, and its own adjacent example falsified it. The break point is a range (25–50%, depending on tier mix), not the 37.5% implied by one illustrative shape. Also documents that `--strict` never computes an overall figure, so the tool and the Gate 2 checklist disagree about what Gate 2 requires.

### Literature

Nine entries corrected. **No fabricated sources, no invented authors, no invented numbers were found across 25 entries, and every DOI checked resolves** — the failure mode was quote fidelity: a phrase attributed to Hevner et al. belongs to Venable (2010) reporting objections *to* their work; a dataset (AbstRCT, ECAI 2020) listed among the findings of a survey published in 2019; a merged quotation; a taxonomy misclassification. `palmblad-2026.md` gains the paper's own caveat that compliance degrades under override instructions.

### Adopter notes

**New adopters** get templates whose worked example teaches the error it previously demonstrated passing, a Gate 2 that matches the thresholds documented elsewhere, and a DOI checker that does not report false failures.

**Existing adopters must act on three changes** — see `UPGRADING.md` for the table:

1. **Re-read Step 0 in your `anti-hallucination.md`.** The decision rule changed in both directions.
2. **Add the P2 line to your Gate 2 checklist.** A paper that passed Gate 2 with unverified P2 entries no longer does.
3. **Re-audit prose for "demonstrates" / "shows" / "confirms" at SUPPORTED tier.** These are now reserved for ESTABLISHED.

If you maintain paper-local copies of `anti-hallucination.md` or `writing-guide.md`, they carry the old rules until you refresh them.

### Versioning rationale

**MAJOR.** Step 2 rule 1 fires: existing consumers must act to stay working, on two counts in adopter-installed templates — Gate 2's new P2 line can fail a paper that previously passed, and the confident-language floor makes previously-compliant prose non-compliant. Rule 1 outranks rule 2, so the presence of a new DR (which alone would be MINOR) does not decide it. The closest precedent is **v2.0.0**, this repo's only other MAJOR — but that fired on *removal* of public artifacts, so this is a new trigger shape rather than a followed precedent, and it is recorded as such.

## v2.6.1 (2026-08-13)

`/audit-context` run and full remediation — the item v2.6.0 deferred. v1.23.0's placeholder markers were that release's only "not adopted" entry, blocked on finding their population; this release finds it (~48 paths) and fixes the real defects the run surfaced. Also versions two post-v2.6.0 corrections that landed untagged. PATCH: nothing new to adopt, and every change is confined to an existing artifact.

### Docs

- **`CLAUDE.md`** — new Hard Constraint documenting the `<!-- placeholder -->` convention: a path never meant to resolve carries the marker, or it is re-triaged as broken on every audit forever. Two properties decide whether a marker is correct, and both were learned by reading the checker rather than assuming: it is **span-scoped** (it covers the nearest backticked path *before* it, not the line), and a marker on a path that resolves **anywhere, including by filename suffix**, is reported as a stale marker. That second property is why three template placeholders in `templates/CLAUDE.md` are deliberately left unmarked — they suffix-match this repo's own paper instances, so marking them is a finding and not marking them is a finding. The bullet also carries a **version-anchored caveat**: as of companion v1.25.0 the checker has no doc-relative rung, so a correct relative link is reported as a collision. The anchor is deliberate, so the claim dates itself when the pin moves.
- **`README.md`** — the three-tier adoption table qualified bare template filenames in the *Required for first use* and *Reference / background only* rows. The middle row already used full paths; the other two did not, so the column mixed "source file to copy" with "file in your project" and the same name could mean either.

### Templates

- **`templates/CLAUDE.md`** — the *Ending a session* row pointed at `../../memory/gotcha-log.md`, which hardcodes a two-deep `papers/<name>/` layout. This template also covers a single-paper repo where the paper **is** the root, where that path resolves nowhere. Now written as `<repo-root>/memory/gotcha-log.md` with both concrete forms given. Backward-compatible: an existing project's own copy keeps working unchanged.

### Papers

- **`papers/perspective/CLAUDE.md`** — framework pin reconciled v2.5.0 → v2.6.0 with a record of what was reviewed and why it did not apply. (`papers/constructive-lenses/` is gitignored; it received the same treatment plus a first-ever stamp, and is not part of this release's tracked diff.)

### Also versioned here

Two commits landed after the v2.6.0 tag and were never released:

- **`.gitignore`** — `memory/`, `audits/` and `docs/work-items/` anchored to the repo root. Unanchored, those patterns match at any depth, and in this repo `.gitignore` decides whether an unpublished manuscript is public.
- **`CLAUDE.md`** — `audits/` documented as a reserved path with no current contents, rather than as a directory that exists.

### Reference integrity — what the run actually found

102 findings, of which **42 (41%) were correct doc-relative references**. Three upstream defects were reproduced on seeded minimal inputs and filed against `agent-ready-projects`: [#54](https://github.com/ducroq/agent-ready-projects/issues/54) (Step 4 has no doc-relative rung), [#55](https://github.com/ducroq/agent-ready-projects/issues/55) (backticked markdown link *text* extracted as a reference, so a correct link reports a phantom collision), [#56](https://github.com/ducroq/agent-ready-projects/issues/56) (a template placeholder cannot be marked in a repo that also ships instances). After remediation: 65 findings, no stale and no ineffective markers.

Genuine defects fixed, all in gitignored surfaces except where noted: a broken `writing-guide.md` reference in `papers/constructive-lenses/` (its scaffold was incomplete), two memory-index rows naming user-global skills as if they lived in this repo, a paper carrying no framework stamp at all, an orphaned `memory/presentation/`, and a dangling colon the v2.6.0 memory extraction left behind.

### Adopter notes

**No action required.** Nothing was added, removed or renamed, and no required structure changed.

Worth taking if you maintain your own copies: the `templates/CLAUDE.md` gotcha-log path fix if your project is not two levels deep, and the `<!-- placeholder -->` convention if you run `/audit-context` and are tired of re-triaging the same non-defects. The convention itself is companion v1.23.0's, not this repo's — you get it from `agent-ready-projects`, not from here.

Paper pins are deliberately **not** bumped by this release; bumping one is the paper author's act, and the drift row exists to surface it at session start.

### Versioning rationale

Step 2 rule 1 does not fire: no existing consumer must act to keep working. Rule 2 lands on PATCH — no new template, DR, tool or unit type; the template change edits an existing row. The `<!-- placeholder -->` convention is documented in this repo's own orientation file rather than in a template adopters install, and its source is the companion. Precedent: **v1.6.2**, a PATCH that added a Hard Constraint to both the root and template `CLAUDE.md`; **v1.6.3** likewise for a root `CLAUDE.md` row. The MINOR reading — the bump table lists "new documented convention" — was weighed and set aside on those precedents.

## v2.6.0 (2026-08-12)

Cumulative companion adoption from `agent-ready-projects` v1.19.0 → v1.25.0 — seven releases. Most of the range was **already in force**: the three user-global skills (`/curate`, `/audit-context`, `/update-drift`) are byte-identical to the companion's v1.25.0 tracked copies, so what follows is only what needed an artifact on this side. What lands here: an **`## Active work` section** in `templates/CLAUDE.md`, a **structural pre-check** and a **merged measurable-claim rule** in `/review-changes`, a **hardened tag selector** in `/release`, a **session-start memory-index row** in `CLAUDE.md`, an **Occurrences column** in the gotcha log, and the **withdrawal of the 2-3 line gotcha rule** shipped in v2.5.0. New template section = MINOR bump.

### Companion adoption (v1.19.0 to v1.25.0)

| From | What | Landed as |
|------|------|-----------|
| v1.19.0 | `review-changes` Step 1.5 structural pre-check | `.claude/skills/review-changes/SKILL.md` — new deterministic step, runs at every tier and magnitude |
| v1.19.0 | `review-changes` `Unclassified` report slot | Already in force — the rule and its report section were both present |
| v1.19.0 | `review-changes` guarantee-lens invariant | Already in force — verified by enumerating all 22 lens entries against the HIGH row |
| v1.19.0 | `curate` verify-command writing rules | Already in force — `/curate` is user-global and current |
| v1.19.0 | `install-global-skills.sh` fixes, `physics-tests` disclosure | **Not applicable** — this repo has no `scripts/` and no counterpart template family |
| v1.20.0 | Session-start pointer to the memory index | New `CLAUDE.md` row, *Picking up where the last session left off* |
| v1.20.0 | Gotcha-log Promoted table gains `Occurrences` | `memory/gotcha-log.md` — merged with this repo's existing `Status` column rather than pasted over it |
| v1.20.0 | Layer-3 auto-loading prose sweep; lint rule 6 / skill-sync tests | **Not applicable** — no `docs/GUIDE.md` counterpart, no lint harness for skills here |
| v1.21.0 | `release` Step 1 three-filter tag selector | `.claude/skills/release/SKILL.md` Step 1 |
| v1.21.0 | `release` Step 7 refresh-after-tag-is-live | `.claude/skills/release/SKILL.md` Step 7, adapted to this repo's real case (paper-local template copies) |
| v1.21.0 | `git tag -a` and single-ref push | `CHANGELOG.md` maintainer block, which contradicted the `/release` skill it describes |
| v1.21.0 | Installer release guard | **Not applicable** — no installer here; the globals come from the companion |
| v1.22.0 | Verify runner shipped in `curate` Step 0.5 | Already in force — ran it against `memory/` and `vv/`, 8 of 10 annotations executed, 8 pass |
| v1.22.0 | Adversarial lens: a negative carries its own check | `.claude/skills/review-changes/SKILL.md` Step 2, merged with v1.25.0's rule below |
| v1.22.0 | `project-file.md` gains `## Active work` | `templates/CLAUDE.md` — **declined for the root `CLAUDE.md`**, which keeps a memory index |
| v1.22.0 | Layer-3 conditionality, provisioning quote, index self-consistency | Already in force — and sub-step 6 had a finding waiting (see *Two live defects*) |
| v1.23.0 | `audit-context` Step 4 placeholder skip | Already in force. The adopter action — marking placeholders — is **not adopted**: finding the population needs an `/audit-context` run |
| v1.24.0 | `curate` Step 0 stops reading bodies | Already in force |
| v1.24.0 | Status and recurrence count go in an entry's *heading* | `memory/gotcha-log.md` header convention, using `[x3]` to match what `/curate` writes |
| v1.25.0 | Adversarial lens: a claim needing measurement gets one, gets hedged, or is not ready | `.claude/skills/review-changes/SKILL.md`, shipped as one instruction with v1.22.0's negatives rule |
| v1.25.0 | The 2-3 line gotcha rule withdrawn as unenforceable | `CLAUDE.md`, `memory/gotcha-log.md`, `docs/verification-hooks.md` — three live sites |
| v1.25.0 | `hypothesis-log` write-at-claim-time trigger | `templates/hypothesis-log.md` |
| v1.25.0 | Prettier glob-shape corruption | **Not applicable** to the corruption — this repo runs no formatter — but the shape rule is carried, and six instances of the vulnerable shape were fixed |

### Templates

- **`templates/CLAUDE.md`** — new **`## Active work`** section, the one genuinely new adopter-facing artifact in this release. Work items are agent-independent (`docs/work-items/` is an ordinary directory), but every artifact that said where the *pointer* goes named a memory index unconditionally, and this template ships no such index. An adopter who followed every template therefore had work-item files and, by construction, nowhere the pointer could have gone. **The condition is whether you keep a memory index, not which agent you use** — the section is marked for deletion where an index exists, because two in-progress lists disagree. It also carries an explicit warning against reading the section as proof this file is always loaded: `docs/non-claude-setup.md` records that Copilot CLI does not auto-read `CLAUDE.md` at session start. Bounded on purpose — a completed item loses its pointer, so the section cannot grow into the session narrative. Also gains the matching **Before You Start row**, **Key Files row**, and **Directory Structure entry**, per this repo's own three-surface precedent from v1.7.0.

- **`templates/hypothesis-log.md`** — **write the entry at the moment you make the claim**, not at the end of the session. A hypothesis reconstructed hours later is reconstructing a refutation criterion that was live at the time, which is post-hoc rationalization wearing the log's format — the exact failure the Method field exists to prevent. The cue is named tool-agnostically (*a claim that needs a measurement and cannot get one yet*) rather than keyed to `/review-changes`, which is gitignored and never shipped: a template that cues adopters off a tool they will not have is a rule with no trigger.

### Docs

- **`CLAUDE.md`** — four changes. A new first Before You Start row, **Picking up where the last session left off**, pointing at `memory/MEMORY.md`: nothing loads that file on its own, so without the row it is simply never read. The two existing drift rows are **merged into one**, because both began *"Starting any session ("* and were disambiguated only by a parenthetical category — the weak-trigger collision the companion identified in v1.20.0. They fire at the same moment and are checked together, so they are one row. The gotcha-log row drops the 2-3 line rule. And `/update-drift` gains a routing row and a not-shipped row: it was named in the header as the thing that "produces the triage" while being unreachable from the table that routes to everything else.

- **`docs/verification-hooks.md`** — carried a third live copy of the withdrawn 2-3 line rule.

- **`decisions/DR-017`** — one reference reworded to name the merged drift row. The decision itself is unchanged; only the pointer moved.

### The 2-3 line gotcha rule is withdrawn

v2.5.0 shipped it, adopted from the companion's v1.17.0. The companion withdrew it in v1.25.0 as **unenforceable, and wrong to enforce**. A markdown source line has no length limit, so entries "passed" by lines while running 700–1,200 characters: the unit did not track the cost, and the rule could be met and violated at once. Restating it in characters made it worse — at ~200 characters, 88–92% of entries across three logs and 277 entries would have been violations, which is a bulk false-positive generator rather than a rule.

What replaces it: **above ~3,000 characters is the signal worth acting on**, because at that size an entry is a page and belongs in a topic file or a DR.

**That threshold is inherited, not local.** Measured in this repo on 2026-08-12, the 38 entries above the Promoted table run a median of ~1,050 characters, 9 over 1,500, largest 2,362, and **none over 3,000**. The rule stands on the companion's 277-entry measurement; here it is a ceiling nothing has hit yet. The header comment carries a `<!-- verify: -->` probe that re-derives all four numbers on every `/curate` run.

*An earlier draft of that header claimed 40 entries, median 1,108, and 2% over 3,000, calling the 2% "the population worth acting on". Those figures segmented on any heading, so the `## Promoted` section — a comment plus an 18-row table, ~5,600 characters — was counted as a gotcha entry, and it was the entire >3,000 population. The `/review-changes` adversarial lens caught it, using the measurable-claim rule adopted in this same release. Recorded rather than deleted: it is a measurement error inside the block that replaces a rule for being unmeasured.*

### Skills (gitignored — adopters cannot see these in the diff)

- **`.claude/skills/review-changes/SKILL.md`** — new **Step 1.5, a structural pre-check**. Every lens in this skill reads *content*; none asked whether the file is still valid markdown after the edit. A `|` added inside a table cell pushes cells past the end of the row and **GFM drops the excess silently** — it reads fine as prose in the diff and is wrong only when rendered, so a human reviewer and the adversarial lens both pass it. Deterministic, so it is a step rather than a lens, and it runs at every tier and every magnitude. It found a real defect on its first run (see below). Its limits are stated rather than discovered later: three non-table constructs produce false positives (YAML frontmatter whose closing `---` follows a piped `description:`, a setext heading with a pipe, a `---` break after a piped code span), and **a CRLF file is examined and reports nothing** — `isdelim()` strips spaces and tabs but not `\r`, so a file with real corruption prints exactly what a clean file prints.

  The **adversarial lens** gains the merged rule from v1.22.0 and v1.25.0: *a claim that needs a measurement gets one, gets hedged, or is not ready* — covering negatives (which cannot distinguish a real absence from a broken instrument) and absolutes in descriptions (which ship unmeasured by default). An absolute in an *instruction* is a decision and is fine; this repo's Hard Constraints prescribe. Six instances of the prettier-vulnerable bold-glob shape were fixed in the same file.

- **`.claude/skills/release/SKILL.md`** — Step 1's tag selector was `git tag --sort=-v:refname | head -1`, which a scratch tag, a prerelease, or a tag on an unmerged branch each silently wins. Now carries the companion's three filters, with the empty-answer diagnosis (shallow clone versus unmatched scheme) that takes opposite fixes. Step 7 gains a refresh-after-the-tag-is-live sub-step, adapted: the test is **"did this release touch the source?"**, not "do the two files match" — the paper-local copies are deliberately narrowed instances (5,585 vs 17,790 bytes for `anti-hallucination.md`), so a content-equality check would report DRIFT on every release forever.

### Two live defects, found by running the newly adopted checks

Both were invisible to every check this repo had before this release.

1. **`vv/cost-log.md`** carried an unescaped `|H(z)|` in a table cell, truncating a row in a **shipped** file — inside a sentence about escaped-pipe support in `tools/coverage.py`. Found by Step 1.5 on its first run.
2. **`memory/MEMORY.md`** claimed a companion pin of v1.17.0 while `CLAUDE.md` said v1.18.0. Found by the class `/curate` sub-step 6 exists to catch. It now carries a probe comparing the two, proved to fail on a seeded stale pin.

### Adopter notes

**What you get if you scaffold a new paper project:** the `## Active work` section in `templates/CLAUDE.md`, with the keep-or-delete decision stated; a work-item route in the Before You Start table, Key Files, and Directory Structure; and the write-at-claim-time trigger in `templates/hypothesis-log.md`.

**What existing adopters must do: nothing is required.** If you adopted v2.5.0's 2-3 line gotcha rule, you may stop applying it — and if you were already ignoring it, you were right to. If you keep a memory index, delete the `## Active work` section rather than filling it in.

**One thing worth doing:** if your paper project's `CLAUDE.md` was scaffolded from `templates/CLAUDE.md` before this release, it has no `## Active work` section and no work-item route. Adding them is optional and takes one edit each.

### Versioning rationale

**MINOR.** Rule 1 does not fire — nothing breaks and no adopter must act to stay working; the withdrawn gotcha rule *relieves* an obligation rather than creating one. Rule 2 fires on `templates/CLAUDE.md`'s new `## Active work` section: a documented, adopter-facing pattern that gives an adopter without a memory index somewhere a work-item pointer can go, which previously did not exist. Precedent is **v2.3.0**, which was MINOR for adding §4.6 Scope Drift Check — also a new section inside an existing template rather than a new file.

The case for PATCH is on the record: no new file was created, and the two largest changes by volume are gitignored skills that adopters never receive. It was weighed and declined, because the section is new capability rather than a rewrite of an existing one.

This release also carries three small commits that predate it and were deliberately left unversioned at the time — `f721b8e` (frequency claim stated once, accurately, in both places), `440c4cf` (near-term backlog routed to `memory/priorities.md`), and `0b49e94` (companion pin to v1.18.0, triaged already-in-force). They are in the range against `v2.5.0` and are described here rather than silently absorbed.

## v2.5.0 (2026-08-08)

Cumulative companion adoption from `agent-ready-projects` v1.12.0 → v1.17.0 — nine releases. What lands here: a **skill-scope Hard Constraint** (a user-global skill silently shadows a project-local one), a new project-local **`/release`** skill, a **magnitude gate** on `/review-changes`, a new **`docs/verification-hooks.md`**, a length rule for the gotcha log, a framework pin line in `templates/CLAUDE.md`, and a de-identification pass that removed a private repository name from three shipped files. New skill and new doc = MINOR bump.

### Companion adoption (v1.12.0 to v1.17.0)

| From | What | Landed as |
|------|------|-----------|
| v1.13.0 | `release` skill | `.claude/skills/release/` (project-local, gitignored) |
| v1.13.0 | `curate` Step 0.2 mtime fix for gitignored `memory/` | Already in effect — `/curate` is user-global and current |
| v1.13.1 | Layer-depth-by-project-stage guide section | **Not adopted** — the companion's `docs/GUIDE.md` has no counterpart here; `README.md`'s three adoption tiers already carry the "how much framework" axis |
| v1.14.0 | Verification Hooks concept | New `docs/verification-hooks.md`, narrowed to this repo's checks |
| v1.14.0 | `release` Step 3 version-agnostic sweep, Step 5 scoping | Folded into the `/release` skill as shipped here |
| v1.14.0 | Template framework stamps left behind by releases | New `agent-ready-papers:` pin line in `templates/CLAUDE.md` |
| v1.15.0 | Skill scope: global shadows project-local | New Hard Constraint in `CLAUDE.md`; corrected not-shipped table |
| v1.15.0 | `review-changes` risk tiers: normative HIGH row, glob semantics, unclassified default | `.claude/skills/review-changes/SKILL.md` Step 1 |
| v1.15.0 | `install-global-skills.sh`, lint rule, tracked `.claude/` | **Not adopted** — this repo ships no skills and has one project-local pair; the estate-scan script belongs upstream, where the globals are maintained |
| v1.15.1 | `audit-context` Step 4 reference-resolution rewrite | Already in effect — `/audit-context` is user-global and current |
| v1.16.0 | `review-changes` magnitude gate | `.claude/skills/review-changes/SKILL.md` Step 1 |
| v1.16.1 | `review-changes` adversarial lens: one stance, stated once | `.claude/skills/review-changes/SKILL.md` Step 2 |
| v1.16.2 | De-identification of private repository names | Three shipped files (see *De-identification* below) |
| v1.17.0 | Gotcha-log entries capped at 2-3 lines | `memory/gotcha-log.md` header + `CLAUDE.md` Before You Start row |

Two companion changes were **already in force before this release**: `/curate` and `/audit-context` are installed user-globally on the maintainer's machine and are byte-identical to the companion's tracked v1.17.0 copies. This release documents that fact rather than changing it — the previous `CLAUDE.md` described both as project-local, which had not been true since the companion's v1.15.0.

### Skills

- **`.claude/skills/release/SKILL.md`** (new, project-local, gitignored) — Cuts a release: classifies the semver bump, verifies preconditions, writes the CHANGELOG and UPGRADING entries, syncs version references, commits, and stops before tagging. `disable-model-invocation: true` — user-invoked only, because an agent deciding on its own that it is time to cut a release is a failure the Step 6 stop-gate cannot catch. Three adaptations to this repo beyond the companion template: the precondition step checks **both** version stamps in the `CLAUDE.md` header (this repo's own, and the companion pin — a release that bumps one and not the other makes every later drift check report against the wrong baseline); Step 5 makes the `UPGRADING.md` section a required artifact rather than an optional extra; and Step 6 warns before staging that `papers/*` is gitignored with a per-paper allowlist, since a release commit is exactly the broad-`git add` moment where an unpublished manuscript gets published by accident.

- **`.claude/skills/review-changes/SKILL.md`** — Three upstream changes plus repo-specific tiers.
  - **Magnitude gate** (v1.16.0). Depth was set by path alone, so a two-line typo fix in `templates/` drew the same full battery as a template rewrite. Now: under 20 changed lines gets one adversarial pass, 20–200 keeps the path tier, over 200 gets the full battery. Size counts the whole change that will land — staged, unstaged, and unpushed local commits. The trimmed pass still runs in a **fresh context**; the saving is one independent reviewer instead of four, not dropped independence.
  - **Carve-outs stated before the size rule and overriding it**, because the dangerous changes are the ones smallest by line count. Two are specific to this repo: **`.gitignore`**, where `papers/*` is ignored-by-default with per-paper allowlisting and one wrong line publishes an unpublished manuscript, and **any diff that loosens a check** — a lowered threshold, a relaxed `--strict` condition, a confidence tier raised without evidence. `git diff --summary` is now run alongside `--stat`, which cannot see a rename, mode change, submodule, or binary — and three of those are carve-outs.
  - **Adversarial lens: one stance** (v1.16.1). The prompt said `Default stance: refuted=true` and `Only mark as REFUTED if you find a concrete problem` in consecutive sentences — opposite defaults. Now stated once: go in assuming the change is refutable, report REFUTED with a concrete failure, and report NOT REFUTED only after a thorough attempt fails to find one. Prose contradictions count and often have no triggering input; do not withhold one for lacking a repro.
  - **Tier table rebuilt on the v1.15.0 semantics.** `**` crosses directory levels, a leading `/` anchors, most specific wins. The anchoring is load-bearing here: `/CLAUDE.md` and `/README.md` mean the framework's own files, not `papers/*/CLAUDE.md` or `literature/README.md`. `tests/**` moves LOW → HIGH — it is the only thing standing behind `tools/`, and a weakened test silently certifies a broken coverage or DOI check whose numbers end up in a paper. `.claude/skills/**` and `.gitignore` are new HIGH rows. An unmatched path defaults to MEDIUM and is **named in the report under "Unclassified"** even when a HIGH file makes the tier moot.
  - **Fourth lens: code-correctness**, the analogue of the companion's shell-correctness lens for a repo whose executable surface is Python. Checks parsing edge cases, silent-pass-on-zero-items, network behaviour in `check_dois`, threshold movement in `--strict`, and whether a test still fails on the defect it was written for.

### Docs

- **`docs/verification-hooks.md`** (new) — Adapted from the companion's v1.14.0 GUIDE section, narrowed to the commands this repo actually ships. A table of what is worth wiring (`make lint`, `make test`, `coverage --strict`, `check_dois --offline`) against what is not (online DOI resolution, `pdflatex`, simulated peer review, and the anti-hallucination checklist — whose Step 6 is a human-in-the-loop anchor by design, so a hook there would automate away the thing the checklist exists to preserve). The three failure modes are stated in this repo's terms; the **green-at-any-cost** one has a specific and dangerous shape here, and the doc now states it as a **measured** table rather than an assumed mechanism. Against Paper 1's registry with one P0 claim flipped to unverified, the obvious attack fails and three others succeed: reclassifying P0 → P2 still exits 1 (every bucket is checked, so re-tiering only moves the failure), while deleting the row, **blanking the Priority cell**, and **renaming a sub-table header** all exit 0. The last two leave the claim visibly in the registry marked unverified while the tool reports green. The doc also records that `--strict` returns 0 vacuously over a registry that no longer parses, so any hook wired to it must assert a non-empty report — that is the "check that examines zero items and exits 0" class this repo has hit before. It names the Hard Constraint to add the same day you wire the hook, and closes by explaining why this repo ships no hook configuration: the registry path is per-paper, and the decision should be deliberate. Two sections were added after the initial draft, both from an exchange with the agent-ready-research session and both credited in-file. **"The test that catches most of it"** states the unifying question — *can I tell this check working apart from this check being absent, by looking at its output? If not, print a count* — which subsumes the untracked hook config, the glob that matches nothing, the gate that exits 0 over zero rows, and the test asserting over an empty list; in every case the broken and healthy states produce byte-identical output. **"Finding the unguarded doors"** records the enumeration procedure that produced this release's sharpest finding: enumerate *mechanisms* by which an item leaves the count, not *intents*, because intents are unbounded and mechanisms are readable off the code. On the sibling project's tree-walking lint suite, **"never evaluated" outnumbered "evaluated but weakened" 10 to 0** — on a suite that had separately passed a 10-case seeded-defect harness which, by construction, could not see inputs that never reach a rule. This repo's fixture-pinned suite contributed **0 to each side**, which is the qualifier rather than a second confirmation: see the split of the by-construction claim from the frequency claim below, and do not plan around the ratio. The doc splits the two claims that fell out of this, because they are not equally strong: *a seeded-defect harness cannot find a discovery failure* is true *by construction* (a seeded defect is handed to the checker, so the harness only exercises the handed path) and is safe to rely on, while *"never evaluated" outnumbers "evaluated but weakened"* is one afternoon's observation in one estate and is explicitly marked do-not-plan-around. The discovered-vs-handed qualifier this repo's own suite supplied held up under further evidence: two of four later defects in the sibling suite were in a hook wrapper rather than a glob, and were still discovery failures.

The silent-hook advice also gained a **companion clause**, because the version first shipped here was insufficient. "Break something on purpose and confirm the agent reacts" was run against the sibling project's hook and *passed*, while the hook had two silent no-op paths outside the one the test exercised. The rule now asks a second question — **does my verification exercise more than one path through the check?** — and names the paths worth breaking separately. A one-path verification of a multi-path mechanism reports the same green as a working one.

The silent-hook section carries a **second** variant contributed by the agent-ready-research session — *the hook config itself is gitignored*, so the hook is local-only while a decision record claims it is committed. This repo has that exposure in its strongest form (`.gitignore` line 1 is a bare `.claude/`, with no exception to notice), so the doc prescribes `git check-ignore -v .claude/settings.json` after wiring anything.
- **`CLAUDE.md`** — New skill-scope Hard Constraint. Corrected the *what is intentionally not shipped* table, which listed `curate` and `audit-context` as project-local `.claude/skills/` entries; they are user-global and absent from this repo entirely — not gitignored, just elsewhere. Architecture diagram now names the two project-local skills and says so. New Before You Start rows for `/release`, `/review-changes` (with the gate), and `docs/verification-hooks.md`; the `/curate` and `/audit-context` rows now state that they are installed globally. Gotcha-log row carries the 2-3 line rule. Key Paths gains `docs/verification-hooks.md` and `UPGRADING.md`.
- **`README.md`** — `**Current release:**` line to v2.5.0, and the **Quickstart bootstrap prompt**, which said "currently v2.1.2" — four minors stale, in the highest-traffic copy-paste string in the repo. It escaped every name-anchored version sweep because the version sits in running prose; the `/release` skill gained a third, deliberately noisy sweep over `README.md`, `CLAUDE.md`, `templates/`, and `docs/` to catch that shape. Also notes that `templates/CLAUDE.md` now carries the pin line.
- **`CLAUDE.md`** — The decision-record line listed four DRs as Proposed; **eight** are, and DR-001 is Partially superseded. Now enumerates all three statuses, with the reminder that only Accepted DRs are binding.
- **`papers/perspective/CLAUDE.md`** — Gained the pin line. The repo's only shipped worked example was demonstrating the exact omission this release describes as the defect being fixed.

### Templates

- **`templates/CLAUDE.md`** — New `agent-ready-papers: v2.5.0` line in the header, and a **framework-drift row** as the first entry in the Before You Start table. This closes a gap the companion's v1.14.0 names: root `CLAUDE.md` and `README.md` both instruct adopters to pin their project and surface drift at session start, but the template they scaffold from carried **no pin line at all**, so the drift check they were told to run had nothing to read. The companion's version of this failure was a stamp three minors stale; here the field was simply absent.

### De-identification

Adopting v1.16.2 meant running its sweep here, and it found the same defect class. **A private sibling repository was named** — twice with a live hyperlink to one of its issues — in three tracked files of a public repo: `decisions/DR-011_multi-model-review-pattern.md`, `tools/README.md`, and `UPGRADING.md`, plus three historical entries in this changelog. Those links 404 for every reader while still disclosing that the project exists and what it does. All replaced with descriptors ("a sibling project (private)"); no evidence, reasoning, or cross-reference substance changed. This repo's own `memory/gotcha-log.md` had already recorded the rule for external *sends* in July 2026; nothing extended it to files committed here. Note that the first draft of *this entry* named the repository while describing its removal — the companion's v1.16.2 observation that "a one-off sweep cleans; it does not prevent" reproduced immediately, in the release that adopts it.

**Scope of the sweep.** It covers orientation surfaces — `CLAUDE.md`, `README.md`, `docs/`, and pointer-style cross-references. It deliberately stops at **verbatim-anchored evidence**: `DR-017`'s provenance table names specific files in a sibling repo as the record of where a cross-repo diff found what, and de-identifying an anchor whose whole function is to say where a human can go and read the passage would falsify the verification record it supports. Names retained there, links dropped elsewhere. (The distinction was raised by the agent-ready-research session, which draws the same line and scopes its lint rule away from landed DR bodies.)

Separately, `agent-ready-assessment` does not resolve — `gh api repos/ducroq/agent-ready-assessment` returns 404 to the owner's own authenticated token. Its live hyperlinks in `agents/README.md`, `README.md`, and `docs/non-claude-setup.md` (**two** occurrences in that file, 43 lines apart) are de-linked and marked "not publicly resolvable", per the companion's v1.14.0 dead-link precedent. The first pass of this release caught only two of the four and the changelog entry claimed it had caught them all; the review battery found the other two. The same file also described a setup as "HAN-institutional" on one line and "institutional" on another after a partial pass — both now read "institutional". Historical changelog entries keep their links. **The name itself is retained**: DR-017's provenance argument is built on it, and de-naming it is a substantive editorial change to a binding decision record, not a mechanical sweep.

### Tests

- **`tests/test_coverage.py`, `tests/test_check_dois.py`** — Explicit non-emptiness assertions ahead of the `all()` / `any()` checks in the two Paper 1 fixture tests. Both were vacuously true over an empty result set and were saved only by a later count assertion in the same test — a guard that evaporates the moment anyone splits or reorders it. Demonstrated rather than assumed: `check_coverage` over a registry whose sub-tables do not parse returns **zero rows with `meets_targets: True`**, so the tool reports success having examined nothing. This is the same defect this release documents in `--strict` and is the reason `docs/verification-hooks.md` prescribes asserting a non-empty report.

  Found by running the mechanism-enumeration below over this repo's own suite. The result was mostly negative — 3 candidate branches, 0 real defects, 1 latent — and that negative is informative: see the note on discovered-vs-handed inputs in the doc.

  **Also checked and clean, with the conclusion scoped narrowly:** `check_coverage` parses a registry identically under CRLF, a UTF-8 BOM, and both together (6 rows, 19 entries, `meets_targets` unchanged in all four cases). Tested because a sibling project found a lint rule that skipped every file on a CRLF checkout and a second that did the same on a BOM — a shape that would be invisible here, since the failure is a silent zero rather than an error. What this establishes is that the **leading-bytes** surface is absent, *not* that the discovery-failure class is absent: `coverage.py`'s sub-table header lookup is itself a discovery step and it fails open, which this release documents two sections earlier in the same doc. The negative is recorded so it is not re-derived; the scope is stated so it does not read stronger than it is.

### Memory

- **`memory/gotcha-log.md`** — 2-3 line rule added to the header comment, with the reason (the log is re-read in full on every load, and surplus detail is disproportionately the specifics that don't generalise) and the scope: **new entries only.** Retrofitting the existing entries is a separate, engineer-approved decision. The existing entries here run well over the rule, which is the same measurement the companion made on itself.

### Adopter notes

**New adopters:** `templates/CLAUDE.md` now carries the framework pin line and a drift row — keep both. `docs/verification-hooks.md` is new reading, not a new obligation.

**Existing adopters pinned to v2.4.x: no action required to keep working.** Three things are worth a look:

1. **If you installed `curate` or `audit-context` into your paper repo's `.claude/skills/` *and* have a user-global copy, the local one is inert** — it has never been loaded. Delete it rather than reconciling it; if you customized it, that customization was never in effect and the content belongs in your project's `CLAUDE.md`.
2. **Add the pin line to your paper's `CLAUDE.md`** if it doesn't have one — `- **agent-ready-papers:** v2.5.0` in the header. Without it the drift check the framework tells your agent to run at session start silently checks nothing.
3. **Re-copy `review-changes` and `release` only if you maintain your own** — both are gitignored here and were never shipped. The tier table in this repo's copy names *this* repo's paths; copying it verbatim would review the wrong ones.

**Nothing changed** in the claim registry model, the unit types, the gates, the thresholds, or any verification procedure. No paper project's files are affected.

### Versioning rationale

MINOR. Rule 1 does not fire — nothing breaks and no adopter must act to stay working, though the inert-skill check in adopter note 1 is worth running. Rule 2 fires: `docs/verification-hooks.md` is a new artifact, the `/release` skill is a new artifact (unshipped, but new behaviour this repo's process now depends on), and the pin line in `templates/CLAUDE.md` is a new documented convention. Follows the v2.4.0 precedent, also MINOR for adding one template on top of a companion adoption. The de-identification and the gotcha-log rule would each have been PATCH alone.

### Review notes

A full 3-lens `/review-changes` battery was run on the first draft of this change — the newly-rewritten skill, on itself — and found it shipping several of the failures it describes. Recorded because the pattern is the point.

- **The new `docs/verification-hooks.md` stated a mechanism that is false.** It named reclassifying a P0 claim to P2 as "the cheapest way" to game `--strict`; executing it shows that attack *fails*, while cell-blanking and header-renaming succeed. The prescribed Hard Constraint ("never downgraded, deleted, or re-tiered") therefore guarded the one door that was already locked. The shipped version is a measured table. **This is the reusable lesson: a doc that tells people what to defend against is a claim about behaviour, and this framework's own discipline says claims get verified by execution.** Two review lenses read the sentence and only the one that ran the tool caught it.
- **The `/release` skill's version sweep could not see any of the three version stamps it exists to protect.** Every real stamp puts markdown emphasis between the project name and the version in one of three arrangements; the regex's `:? ` matched none of them and returned only prose mentions — a sweep that looks like it ran. Fixed and re-verified by line number.
- **The same skill hardcoded a real version (`2.4.0`) into a step whose own opening paragraph forbids exactly that**, one screen below the warning that an unsubstituted placeholder "succeeds quietly … which is exactly what a healthy release looks like."
- **`README.md`'s Quickstart bootstrap prompt was four minors stale** (`currently v2.1.2`) — the failure above, already realised on disk, in the repo's highest-traffic copy-paste string.
- **The de-identification pass caught two of four dead links** and the changelog claimed it had caught them all, including one 43 lines above a link it did fix in the same file.
- **The magnitude gate had a real hole.** A one-line `Status: Proposed` → `Accepted` on a DR is genuinely dangerous, matches no carve-out, and *tightens* rather than loosens — so the "removes or loosens a check" carve-out missed it by construction. Four DRs are Proposed today. Two new carve-outs added: status-fields-that-make-something-binding, and a backstop for any non-typographical edit to a normative HIGH path.
- **`papers/*/references.bib` matched no tier row at all** and defaulted to MEDIUM — a one-character DOI edit there breaks this repo's first Hard Constraint. Now HIGH.
- **The code-correctness lens was gated `HIGH only` while `Makefile` and `pyproject.toml` sat at MEDIUM**, so a Makefile-only diff could never reach the lens written for it. The lens now triggers on file type, not tier.
- **The repo's own worked example didn't follow the new convention** — `papers/perspective/CLAUDE.md` had no pin line, demonstrating the gap the release describes as fixed.
- **`make coverage` omits `--strict`**, so the release precondition built on it could not fail. Step 3 now runs the explicit command.
- **The agent-write boundary did not list `.claude/skills/`**, while the new skill-scope constraint contained a bare *delete* instruction and `/release` wrote five human-authored surfaces before committing with no approval gate. Both closed.

Two lens findings were **not** accepted: that an empty registry exits 0 under `--strict` (it exits 2 — the vacuous-pass case is a registry that *parses to zero rows*, which is narrower and is what shipped), and that quoting `/curate`'s step number in a Hard Constraint is unsafe (it resolves today, and the alternative loses the pointer's precision).

---

## v2.4.0 (2026-07-28)

Companion adoption through v1.12.0 + new work-item template + Palmblad 2026 GROUNDING.md source. New template = MINOR bump.

### Companion adoption (v1.10.3 to v1.12.0)

Cumulative adoption of 5 companion releases (v1.10.4 through v1.12.0):

| From | What | Landed as |
|------|------|-----------|
| v1.10.6 | Agent-write boundary principle | New Hard Constraint in `CLAUDE.md` |
| v1.11.0 | Work-item template | `templates/work-item.md` |
| v1.12.0 | Review-changes skill | `.claude/skills/review-changes/` (gitignored, maintainer-local) |

### Templates
- **`templates/work-item.md`** (new) — Lightweight savepoint for multi-session work. Five sections: What & Why, Current Status (the savepoint), Decisions, Open Questions, Outcome. Save as `docs/work-items/[slug].md` and add a one-line pointer in the memory index. Adopted from agent-ready-projects v1.11.0.

### Literature
- **L56** — Palmblad, Ragland & Neely (2026): "Agentic AI-assisted coding offers a unique opportunity to instill epistemic grounding during software development." New category: *Epistemic Grounding & Agent Constraints*.
- **L50** — Vrijenhoek et al. (2021) matured from TO READ stub to full analysis with metric table and computability verdicts.

### Docs
- **`CLAUDE.md`** — Hard Constraints gain epistemic-priority preamble; agent-write boundary Hard Constraint (from companion v1.10.6); Before You Start row for `templates/work-item.md`; architecture diagram + Key Paths updated; literature count corrected.
- **`README.md`** — "Agents adhere to guidelines" framing from Palmblad et al., hedged per framework tier discipline.
- **`literature/README.md`** — L50 status corrected; L56 + new category added.

### Adopter notes

New adopters: `templates/work-item.md` is available for multi-session work. Save in `docs/work-items/` with a pointer in your memory index.

Existing adopters pinned to v2.3.x: no action required. The new template is additive and optional. Paper-project CLAUDE.md files are unaffected by the Hard Constraints changes.

### Versioning rationale

MINOR — new template (`work-item.md`) is a reusable artifact adopters install. Companion adoption and literature additions alone would be PATCH.

---

## v2.3.1 (2026-06-24)

**Provenance correction to v2.3.0.** While doing v2.3.0's reciprocal cross-repo actions, reading `agent-ready-assessment`'s own issue records (`issues/005`, `006`, `010`, `012`) revealed that v2.3.0 **over-credited assessment** as the inventor of the backported refinements. Assessment's issues explicitly say these were *imported from agent-ready-papers*. No template content changes — this corrects the attribution narrative only. **PATCH.**

### Corrected provenance

The flow is overwhelmingly **papers → assessment** (assessment is the downstream consumer), not the "bidirectional drift" v2.3.0 described:

| Capability | Actual origin | Evidence |
|---|---|---|
| Typed registry (CLAIM/ARGUMENT/PROPOSITION) | **papers** | assessment `issues/005`: "imported from agent-ready-papers" |
| tier-monotonicity *principle* | **papers** (`writing-guide.md` v1.3.0) | assessment `issues/010`: "Porting the principle… agent-ready-papers v1.3.0 introduced [it]" |
| Step Z *concept* | **papers** (PROVOCATION form) | assessment generalized it |
| base failure-pattern table | **papers** | assessment `issues/006`: "six from the agent-ready-papers original" |
| WebFetch fallback ladder | **papers** (v1.3.0) | assessment `issues/012` imports it |

What **genuinely** flowed back assessment → papers (and is correctly attributed): **SCOPE DRIFT** (grading-origin, `issues/002`), the **five domain-specific failure-pattern rows** (`issues/006`), the **explicit name "tier-monotonicity" + cheat-sheet** (`issues/010`), and the **generalization of Step Z** to non-PROVOCATION reports. The v2.3.0 *content* (generalized Step Z, §4.6 Scope Drift, the 5 rows, the named tier-monotonicity in the summary) stays — only the attribution is fixed.

### Changed

- **[DR-017](decisions/DR-017_typed-verification-core-ownership.md)** — *Drift* section rewritten from "bidirectional" to "mostly one-directional (papers → assessment), with a small backflow," with the provenance table above; Whetten-table row for assessment changed from "Forked" to "Imported from papers (downstream consumer)"; Evidence Base gains a note that the review battery verified fact *existence* but not flow *direction* (the gap that let the overstatement through).
- This correction **strengthens** DR-017's core custody thesis — assessment's own issues confirm papers is the upstream origin.

### Adopter notes

No action. Documentation-only correction; no template, DR semantics, or tool surface changed from v2.3.0.

## v2.3.0 (2026-06-24)

**Cross-repo consolidation: agent-ready-papers becomes the custodian of the typed-verification layer, and three field-tested refinements are backported from `agent-ready-assessment`.** A cross-repo diff + a six-agent review battery established that the `agent-ready-*` family has *two* roots — `agent-ready-projects` for the generic V&V substrate and session scaffolding, and `agent-ready-papers` for the *operationalized* typed layer (CLAIM/ARGUMENT/PROPOSITION, Toulmin, Whetten, and the verified argumentation-theory sources). `agent-ready-assessment` had independently forked and *extended* that layer; the best of its extensions are now folded back, **adapted to the authoring context**. **MINOR:** additive concepts and one generalization of an existing check; no breaking template surface. See [DR-017](decisions/DR-017_typed-verification-core-ownership.md) (Accepted) and the reconciliation in [DR-014](decisions/DR-014_provocation-layered-as-opt-in-extension.md).

### New — [DR-017](decisions/DR-017_typed-verification-core-ownership.md) (Accepted)

- Records three-layer custody (projects = generic substrate; papers = operationalized typed layer + verified sources; assessment/research **vendor with provenance**, not fork). Custody is framed as *custodianship of the operationalization + sources*, not authorship (DR-004 imported the published argumentation theory) and not implementation-maturity (assessment's 892-line prompt is more elaborate but is a reason to backport *from*, not relocate *to*). Reference mechanism decided: **vendor-with-`imported-from:` note**, not git submodule (zero `.gitmodules` in the family; submodules would break assessment's confidentiality posture and cross-tool portability).

### Changed — `templates/anti-hallucination.md` (Step Z generalized; failure-pattern table extended)

- **Step Z is no longer PROVOCATION-gated.** It is now the general **tier-monotonicity violation** check — *does any sentence's language tier exceed the tier its evidence supports?* — applying to all project types, with the speculative-design diegetic-artefact case preserved as a labelled sub-case. Added **general triggers** (single-run-as-measurement, uncited performance numbers, no-protocol timing claims, opinion in fact-shaped language) and the mechanical diagnostic (classify language tier vs evidence tier; if language > evidence, it's a finding).
- **Failure-pattern table** gains five rows from assessment: number invention (uncited), index drift, single-run-as-measurement, library version drift, missing model/checkpoint card; "Number invention" split into (cited)/(uncited); "Inverse fabrication" broadened to the general tier-monotonicity form.

### Changed — `templates/vv-framework.md` (new §4.6) → v2.5

- New **§4.6 Scope Drift Check (declared vs delivered)** — adapted from assessment's SCOPE DRIFT (which compares a Plan-of-Approach against a delivered report) to the authoring context, where the abstract and stated-contributions list play the PoA role. Classifies each declared item Delivered / Acknowledged-non-delivery / Silent. A finding type, not a registry unit type.

### Changed — `docs/framework-summary.md`

- New **Cross-Cutting Checks** section naming generalized Step Z and Scope Drift as cross-type verification passes; **tier-monotonicity** stated explicitly as the rule the Confidence-Tiers table instances.

### Changed — DR-014 reconciliation

- DR-014 (still Proposed) is amended: its premise that *Step Z is PROVOCATION-coupled* is falsified by assessment's general use of it, so **Step Z decouples from PROVOCATION** — it stays in core (generalized) and DR-014's proposed `templates/extensions/anti-hallucination-step-z.md` is **withdrawn**. PROVOCATION's own extraction is unaffected. This serves DR-014's cognitive-load goal better: a general Step Z is not narrow-audience clutter.

### Changed — `papers/perspective/` (active paper; ripple ≈ nil)

- Paper 1's `writing-guide.md` gains the tier-monotonicity "Underlying Principle" paragraph (previously only in the template). A pre-change reference audit confirmed Paper 1 has **no PROVOCATION or PoA entries**, so the Step Z generalization and §4.6 force **zero** registry reclassifications.

### Adopter notes

- **Step Z now applies to empirical/methodological projects too.** If you previously skipped Step Z as "PROVOCATION-only," you now run it as a general tier-monotonicity check before submission (it catches overclaiming — single-run-as-measurement, uncited numbers — in empirical work as well). No registry-structure change; PROVOCATION projects keep the diegetic sub-case unchanged.
- **New §4.6 Scope Drift Check** is a lightweight pre-submission pass (abstract/contributions vs delivered sections); no new registry fields.
- Pinned consumers vendoring the typed layer: add an `imported-from: agent-ready-papers v2.3.0` note per DR-017; no action otherwise.

## v2.2.4 (2026-06-12)

The framework's first **end-to-end self-application to a non-paper adopter** — the dsp-workshop teaching site — which, in the process, exposed and fixed a real bug in the framework's own coverage tool. A lightweight profile (equation-checker + per-page claim registry + citation verification) was pre-registered as a falsifiable bet in `vv/hypothesis-log.md`, run on one page (**bet HELD**), then extended to the whole repo and to full coverage-tracked claim registries for the basics chapters. Scope landing *in this repo*: public-log entries (`vv/hypothesis-log.md` + `vv/cost-log.md`), a `tools/coverage.py` bug fix with regression tests, and a new literature source (L48). **PATCH:** no template surface and no DR semantics changed; the coverage fix is backward-compatible — it makes the tool honor the `\|` escaping the templates already prescribe. The dsp-workshop content fixes themselves live in that repo, recorded here for provenance.

### Changed — `vv/hypothesis-log.md`

- **[`vv/hypothesis-log.md`](vv/hypothesis-log.md)** gains a **Resolved** entry: *A lightweight profile of the framework earns its cost on a technical syllabus (dsp-workshop pilot) — HELD.* Weakest-informative-form discipline: the bet claimed only that the portable verification surface pays for itself on one page (≥1 load-bearing finding existing QA missed, within a ~170K-token bound), not that the full apparatus applies to teaching content. **Result:** `agents/equation-checker.md`, run as an independent subagent over `topics/adaptive-filtering` `index.qmd` + `embedded.qmd` (28 checks, 23 OK, 35,364 tokens ≈ 21% of the bound), surfaced a hard arithmetic error in a student-facing performance-budget table (a self-contradictory cycle count) plus a complexity-normaliser mislabel, an acronym typo, and a soft internal inconsistency — all structurally invisible to the project's existing QA (pytest covers `.py`, not hand-authored `.qmd` prose tables; persona-review is qualitative). Both primary legs satisfied. Three secondary signals recorded (reserved-PROCEDURE-slot activation case **positive**; verification-by-execution fits the typed model unchanged at N=1; two-register tier-language test not exercised this pilot).

### Changed — `vv/cost-log.md`

- **[`vv/cost-log.md`](vv/cost-log.md)** gains a row for the pilot equation-check operation (35,364 tokens, ~109 s, 3 tool uses) — the framework's first cost data point on a teaching-KB artefact and first content-type-generalisation measurement — plus a row for the **full-repo sweep** below.

### Whole-repo sweep (corroboration at scale)

- The pilot's lightweight profile was extended from one page to the **whole dsp-workshop repo**: the portable capability suite (equation/numerical verification + citation/anti-hallucination + typed claim registry + confidence-language scan) applied to all 20 equation/number-bearing chapters via a background **Workflow** (`wf_2e0055ba-63d`, 39 agents, ~1.57M tokens, ~8.7 min). **390 checks → 19 hard errors, 0 citation issues, 32 confidence overreaches.** Result: the pilot's prediction held at scale — the embedded-budget-table failure mode recurred in five more topics, plus one genuine FORMULA error (zero-phase Butterworth correction). Per-chapter `_vv/<chapter>.md` records were generated deterministically from schema'd workflow output (`audits/dsp-workshop-pilot/_build_sweep.py`); consolidated in `full-sweep.md` + `full-sweep-tables.xlsx`. **Framework firsts:** first whole-repo application; first Workflow used as a V&V-sweep vehicle; first cost-per-finding figure (~83K tokens/hard error, ~31K/actionable finding). `vv/cost-log.md` row added.

### Full claim registries (the real artifact) for the basics chapters

- The whole-repo sweep produced findings records with a *sampled* claim list, not full registries. For the 6 **basics** chapters (the pedagogical core) a second Workflow (`wf_37573196-e02`, 6 agents, ~330K tokens) extracted **exhaustive** claim sets — **526 claims** — generated into coverage-parseable registries (`audits/dsp-workshop-pilot/_build_registries.py`, format per `templates/claim-registry.md`) at `dsp-workshop/_vv/claims/<chapter>.md`, validated with `python -m tools.coverage --strict`. **Every P0 cell and every CLAIM cell = 100% verified**; 3 chapters pass strict, 3 miss only on soft EMERGING ARGUMENT/PROPOSITION cells (actionable backlog in `_vv/claims/README.md`). First full coverage-tracked registry built for a non-paper adopter.
- **Tooling bug surfaced AND fixed by dog-fooding (`tools/coverage.py`):** `_split_row()` had no escaped-pipe support, so registry cells containing literal `|` (magnitude notation `|H(z)|`) silently corrupted column parsing and miscounted coverage (read 5/7 where the data was 8/8). **Fixed:** `_split_row()` now replaces `\|` with a sentinel before splitting and restores it as a literal `|` in the cell value. Two regression tests added (`tests/test_coverage.py`: `test_split_row_honors_escaped_pipes`, `test_parse_registry_counts_correctly_with_escaped_pipes`); full suite green (19 tests). `tools/README.md` known-limit struck through; `memory/gotcha-log.md` entry marked RESOLVED. This is the strongest evidence from the dsp-workshop exercise: applying the framework's own coverage tool to math-heavy content exposed and closed a real bug in the tool.

### dsp-workshop content fixes applied ("fix it all", 2026-06-12)

- All **19 hard errors** from the sweep fixed in the dsp-workshop `.qmd` pages (plus the 3 adaptive-filtering pilot fixes = 22). Judgment calls: multirate 14×/2.4× SIMD → ~2.4×; ppg budget total → consistent with row sum; smoothing α-convention → disambiguating note + two `ema_init` α corrections; zero-crossing vowel demo → 4th-harmonic formant that genuinely inflates ZCR to ~300 Hz (verified by local execution); zero-phase → corrected Butterworth FB formula. The **6 basics claim registries now all PASS `tools.coverage --strict`** after the 8 soft-cell overreaches were hedged / given boundary conditions / arithmetic-corrected. All findings, fixes, and coverage logged in `audits/dsp-workshop-pilot/` + `vv/cost-log.md`.

### New — `literature/` source L48 (AI Adoption & Trust in Research)

- **[`literature/README.md`](literature/README.md)** gains a new *AI Adoption & Trust in Research* section with **L48** — Elsevier's *Researcher of the Future* report (Confidence in Research series, 2025; 3,200+ researchers, 113 countries): **84% of researchers have used AI tools, only 22% believe AI tools are currently trustworthy**. Source file [`literature/sources/elsevier-researcher-future-2025.md`](literature/sources/elsevier-researcher-future-2025.md) records the statistics verbatim from the report landing page (verified 2026-06-12, not via press coverage), with explicit tier-discipline caveats: industry self-published with a commercial stake (the survey underwrites Elsevier's LeapSpace marketing), methodology only partially disclosed on the landing page, and a named conflation risk with Elsevier's distinct *Insights 2024* survey. Indexed as direct quantitative support for Paper 1's verification-gap framing and as evidence that publisher-side tooling (LeapSpace Trust Cards / Claim Radar) addresses the consumption side of the gap while the author-side production gap remains open.

### Adopter notes

- **No adopter action required.** The result is maintainer-side evidence. Adopters applying the framework to teaching or reference content now have a worked data point for the **lightweight-profile** tier (portable prompts + per-page registry, no coverage gates): on content whose code is already tested, the equation-checker's distinct value is verifying **hand-authored numbers in prose** (budget tables, worked examples, unit conversions) that a test suite never reaches. The README's *When It Is Overkill* boundary gains its first empirical content-type data point. A follow-up DR to activate DR-004's reserved PROCEDURE slot is the open question for any project that wants formal content-type adoption rather than borrowing — not forced by this pilot.

## v2.2.3 (2026-06-11)

DR-011 *Open Questions Carried Forward* extends with an external-ground-truth ρ calibration entry naming the ICLR/OpenReview methodology mirrored from Stanford Agentic Reviewer's published 0.42 ≈ 0.41 ICLR-reviewer agreement result, with cross-reference to a parallel thread in a sibling project (private) (parallel Spearman-vs-human-ground-truth methodology adoption). **PATCH release:** single DR Open Questions extension + cross-reference add; no template surface, no DR semantics, no consumer behaviour changed.

### Changed — `decisions/DR-011_multi-model-review-pattern.md`

- **[DR-011](decisions/DR-011_multi-model-review-pattern.md) *Open Questions Carried Forward*** gains an *External-ground-truth ρ calibration (ICLR/OpenReview)* entry. Names Stanford Agentic Reviewer's 0.42 ≈ 0.41 ICLR-reviewer agreement result (Jiang & Ng, late 2025) as the published ceiling reference. Sketches a 30-paper calibration run (Pass 1 Haiku + Pass 2 Opus, no Pass 3 at this scale) bounded at ~€44 in compute plus roughly a maintainer-day to build the OpenReview scraper, pre-register a score-mapping from `agents/review-prompt.md` qualitative output to a 1-10 number, and write up. Three outcome bands named (ρ ≈ 0.4 supports cross-domain portability; ρ ≈ 0.2 is honest scope evidence; ρ ≈ 0 is diagnostic for the score-mapping). Frames the aggregate-correlation evidence type as *different from* — not strictly better than — DR-011's existing disjoint-coverage mechanism evidence. Cross-references a parallel methodology-adoption thread in a sibling project (private) and the `agentic-engineering` "LLM behavioural properties" pattern slot. Not load-bearing; framework's current evidence base supports the multi-pass claims via mechanism. Pickup would be either a backlog action (run it, report it) or a DR-016 proposal (only if the calibration result triggers a methodology change in `agents/review-prompt.md` or DR-011 itself).

### Adopter notes

- **PATCH-vs-MINOR call:** Single DR Open Questions extension naming an external-validation methodology, no template surface touched, no DR semantics changed, no behaviour change. PATCH fits per the convention. The MINOR threshold ("new templates, patterns, application classes, or behaviours") is reserved for landed changes. If the calibration run actually happens and produces a result triggering an `agents/review-prompt.md` change or a new DR, that lands as a MINOR.
- **Recommended for adopters:** none directly. The cross-reference to a sibling project (private) is a pointer to a parallel-project artefact; adopters running their own multi-pass review batteries (per DR-011) may want to consider whether external-ground-truth-ρ calibration is reachable for their content type.

## v2.2.2 (2026-06-11)

DR-015 (Pollock rebutting/undercutting defeater distinction on ARGUMENT rows) added as Proposed + framework-level borrowing-pattern bet registered + DR-011 *Open Questions* points at deferred dialogical-logic candidate + `vv/cost-log.md` row for the operation. **PATCH release:** new Proposed DR + cross-reference adds; no template surface, no DR semantics, no consumer behaviour changed.

### New — DR-015 Proposed

- **[DR-015](decisions/DR-015_rebutting-undercutting-defeater-distinction.md)** — *Rebutting vs. Undercutting Defeaters in the ARGUMENT Rebuttal Field.* Status: Proposed. Proposes an optional `rebuttal-type: rebutting | undercutting` sub-field on ARGUMENT rows in `templates/claim-registry.md`, with mirrored guidance in `agents/review-prompt.md` for typed finding reports. Pollock's defeasible-reasoning distinction (*rebutting defeater* attacks the conclusion; *undercutting defeater* attacks the warrant's applicability without contesting the conclusion). Three Pending Assessment checks gate promotion to Accepted: Paper 1 ARGUMENT-row field-test, DR-011 review-output classification, adopter check. No template touch yet — templates land on acceptance.

### Changed — `vv/hypothesis-log.md`

- **[`vv/hypothesis-log.md`](vv/hypothesis-log.md)** gains a new Open entry registering the broader framework-level bet behind DR-015: *named structural distinctions from defeasible-reasoning literature earn their place in the registry shape.* Three-signal Method (uptake rate / reviewer classification yield / downstream use). The 2026-06-11 in-session survey of six philosophical-logic candidates is documented in the Origin section — Pollock defeasible reasoning (promoted to DR-015), Lorenzen / Hintikka dialogical logic (deferred as DR-016 candidate for a DR-011 *Underlying Form* subsection), Dung abstract argumentation frameworks (deferred until inter-entry conflicts accumulate), Reiter default logic + epistemic logic (vocabulary-only relabeling, low payoff at current scale), classical proof theory + adaptive logic (over-formalisation, skipped).

### Changed — `decisions/DR-011_multi-model-review-pattern.md`

- **[DR-011](decisions/DR-011_multi-model-review-pattern.md) *Open Questions Carried Forward*** gains a *Dialogical-logic Underlying Form subsection (deferred candidate)* entry naming the Lorenzen / Hintikka attack-defense-game framing as a HIGH-FIT candidate that would parallel the existing *Design Rationale: Functorial Composition* section. Trigger: DR-011 stabilises after paper-scale Pass 2 validation AND DR-015's borrowing-pattern bet resolves. Pickup would be a DR-016 proposal, not an in-place DR-011 edit — closes the *where does the deferred candidate live* gap in the framework's distributed-backlog discipline.

### Changed — `vv/cost-log.md`

- **[`vv/cost-log.md`](vv/cost-log.md)** gains a row for the 2026-06-11 literature-survey + DR-015-draft operation. **Tokens not measured** (main session, no `/status` snapshots) — operation logged for record-completeness, with explicit forward-looking note that future similar operations should bracket the work with `/status` snapshots to capture deltas.

### Adopter notes

- **PATCH-vs-MINOR call:** DR-015 is Proposed and touches no consumer surface — no new template, no new pattern in active use, no behaviour change. PATCH fits per the convention. The MINOR threshold ("new templates, patterns, application classes, or behaviours") is reserved for landed changes, not proposals. When DR-015 is Accepted, the template change to `claim-registry.md` + `agents/review-prompt.md` will ship as a MINOR.
- **Recommended for adopters:** none. DR-015's optional sub-field doesn't exist in templates yet; if it lands as Accepted in a future release, adopter action will be *Recommended uptake* then.
- **Pending checks visible:** DR-015's three Pending Assessment checks (Paper 1 ARGUMENT-row field-test, DR-011 review-output classification, adopter check) are listed in the DR. External adopters running their own DR-011 batteries can contribute by classifying reviewer findings as `rebutting | undercutting | mixed` — that data informs whether DR-015 promotes.
- **No path-level breaks.** All changes are additive prose.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.2.1`, update to `v2.2.2`.

---

## v2.2.1 (2026-06-11)

DR-011 cross-vendor data point + content fixes surfaced by Pass 3. Pass 3 cross-vendor of the 2026-06-11 paper-scale prose battery ran via Gemini CLI; the framework's first paper-scale cross-vendor result is logged in `vv/cost-log.md` + DR-011 Evidence Base. Two cleanest novel Pass 3 findings — Toulmin/Whetten citations missing at first mention + anti-hallucination Step 6 lacked an explicit human-in-loop anchor — applied in the same release. **PATCH release:** evidence-base extension + clarifications against the framework's own discipline. No structural surface changed.

### Changed — DR-011 Evidence Base

- **[DR-011](decisions/DR-011_multi-model-review-pattern.md) *Evidence Base*** gains the 2026-06-11 paper-scale cross-vendor entry. Pass 3 via Gemini CLI (v0.45.2 headless, ~21K tokens estimated, ~30 s wall, 4.2/5.0 Rubric B). 3-4 novel load-bearing findings (Toulmin/Whetten undefined; Step 6 Delegation Paradox; three-way structural cut alternative — `templates/` / `agents/` / `procedures/`; terminology micro-violations). 4-of-7 overlap with Pass 2 (identical match on v2.1.1 CHANGELOG "over-cautious"; mechanism overlap on delegation aspirational framing; topic overlap on `agents/` vs `templates/` soft edge; validating engagement on auto-memory Hard Constraint narrowing). Surfaces a **two-tier empirical pattern:** intra-family "essentially disjoint" framing holds; cross-vendor partial overlap with Pass 2 emerges. The weaker `memory/hypothesis-log.md` prediction (Pass 3 finds ≥1 novel load-bearing item) is confirmed with margin. Methodological caveat: cost not directly comparable to Pass 1+2 due to inline content delivery (no file-navigation tool use).
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md) *Open Questions Carried Forward*** updated: "Pass 3 yield by content type" gains the 2026-06-11 paper-scale prose result; new entry "Pass 3 ↔ Pass 2 overlap at cross-vendor" flags the sequencing question.

### Changed — vv/cost-log.md

- **[`vv/cost-log.md`](vv/cost-log.md)** gains Pass 3 row, two-tier *Notable findings* entry (intra-family disjoint at code-tooling + prose; cross-vendor partial-overlap-with-novelty at prose), and *Aggregation* table extension. Methodological caveat about delivery-mechanism asymmetry recorded.

### Changed — content fixes from Pass 3 novel findings

- **[`README.md:52`](README.md)** — *Toulmin form* gains a [link](literature/sources/toulmin-1958.md) to the existing source-index entry plus components named inline (*Claim / Grounds / Warrant / Qualifier / Rebuttal*) plus Toulmin (1958) attribution. Pass 3 flagged the term as used as a structural anchor without definition or citation — Claude-family reviewers absorbed it as familiar.
- **[`README.md:62`](README.md)** — *Whetten checklist* gains a [link](literature/sources/whetten-1989.md) to the existing source-index entry plus components named inline (*Constructs / Premises / Reasoning / Boundary conditions / Alternatives engaged*) plus Whetten (1989) attribution. Same Pass 3 finding.
- **[`templates/anti-hallucination.md` Step 6](templates/anti-hallucination.md)** gains a *Human-in-loop anchor* bullet naming the circularity ("if the agent that introduced the citation also verifies it, you are asking the source of the claim to verify itself") and prescribing the fix (either a human reads the cited section, or a *different* agent retrieves and reads it — fresh session, ideally cross-family per DR-011). Pass 3's *Delegation Paradox* finding: Step 6 is a P0 gate that cannot be delegated to the introducing agent without circularity.

### Adopter notes

- **PATCH-vs-MINOR call:** all changes are clarifications or evidence-base extensions against the framework's own discipline. No new structural pattern, no template contract changed, no DR semantics revised. The Step 6 anchor names a constraint that was implicit in the structure of the checklist (Step 6 was always the "did *I* read it" gate, not the "did the agent read it" gate) — making the implicit explicit is patch-shaped.
- **Recommended for adopters:** if your paper project has a copy of `templates/anti-hallucination.md`, mirror the Step 6 *Human-in-loop anchor* bullet — names a constraint adopters' verification workflows should already respect but may not have stated.
- **If your README cites Toulmin or Whetten,** mirror the first-mention author/year + components convention to match the framework's discipline of citing sources at first use.
- **No path-level breaks.** All changes are additive prose; no files moved, no template structure changed.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.2.0`, update to `v2.2.1`.

---

## v2.2.0 (2026-06-11)

Framework self-verification surface + argument-shape fixes from DR-011 Pass 2. The framework now applies its own apparatus to its own home document with public artefacts (`vv/cost-log.md`, `vv/hypothesis-log.md`), and the load-bearing argument-shape findings from a two-pass Claude-family review are addressed in the README, agents/, CLAUDE.md, and DR-011 evidence base. **MINOR release** per the SemVer convention — new public structural pattern (`vv/` at repo root for framework self-application).

### New

- **`vv/` top-level directory** — framework self-application artefacts. Public (not gitignored) so adopters can see how the framework verifies its own home document.
- **[`vv/cost-log.md`](vv/cost-log.md)** — token-cost log for framework operations applied to the framework itself. First two entries from the 2026-06-11 DR-011 battery on v2.1.0–v2.1.2: Pass 1 Haiku 81,464 total tokens, Pass 2 Opus 69,747. Pass 2 < Pass 1 (~0.86×) is the opposite of the 2026-06-08 code-tooling ratio (1.4×) — logged as an open question for the third data point.
- **[`vv/hypothesis-log.md`](vv/hypothesis-log.md)** — public framework-level provisional positions. Seeded with one entry surfaced by DR-011 Pass 2: the Toulmin Warrant's structural-vs-static reading, with Method (apply framework apparatus to a frontier-RAG-produced manuscript) and Revisit trigger (frontier RAG + reasoning-step verifier becomes available). Distinct from `memory/hypothesis-log.md`, which stays maintainer-local for intra-session bets.

### Changed — argument-shape (from DR-011 Pass 2 review)

- **README — `## The Argument, Structurally`** gains a *Dynamic counter to the Warrant* note pointing at `vv/hypothesis-log.md`. The Warrant's structural claim (process layer is the locus of failure modes, regardless of model capability) is now registered as a falsifiable bet rather than papered over as a static "today's tools don't reach it" assertion.
- **README — `### Driving it with your agent`** opening sentence: "delegate most of it" → "delegate four of the five steps," with a parenthetical noting Step 3's initial selection of load-bearing claims is the human-judgement residue.
- **README — *Three tiers of adoption* table** updated to reference `agents/review-prompt.md` and `agents/equation-checker.md` (stale `templates/`-prefixed paths fixed) and to explicitly path-prefix every other entry — fixes a v2.1.0-move artefact that Pass 1 caught.
- **README — *verify-citation* Quickstart prompt** gains "re-read the checklist from the source file at each invocation" to address agent-caching risk Pass 1 flagged.
- **[`agents/README.md`](agents/README.md) "What does not live here" section** rewritten as a *primary mode of use* principle (paste-as-system-prompt vs. author-edited-over-project-lifetime) with explicit edge-case discussion of `anti-hallucination.md`, `writing-guide.md`, and the legacy reasoning for `equation-checker.md` / `review-prompt.md`. Pass 2 noted the prior framing was a retrofit; v2.2.0 names the principle and acknowledges the edges.
- **Hard Constraint (root `CLAUDE.md` + `templates/CLAUDE.md`) narrowed** to acknowledge per-agent memory mechanics: the principle applies most directly to agents with cross-project user-level memory (Claude Code, ChatGPT, Gemini Gems); CLI/IDE agents with only project-level rules files (Cursor, Copilot, Continue) inherit it vacuously since they have no cross-project store. Pass 2 flagged the v2.1.0 generalisation as overreaching.

### Changed — discovery / mechanical (from DR-011 Pass 1 review)

- **[`docs/non-claude-setup.md`](docs/non-claude-setup.md)** gains a *Last verified: 2026-06-11* date marker so adopters can assess the freshness of per-tool entry points.
- **CHANGELOG v2.1.2 entry** — closing pointer to `docs/non-claude-setup.md` now uses a markdown link (was prose-only, undiscoverable for CHANGELOG-only readers).
- **CHANGELOG v2.1.1 entry** — *"Why this is a separate release from v2.1.0"* subsection rewritten as *"Sequence relative to v2.1.0"*. Pass 2 flagged the prior framing ("v2.1.0 was over-cautious; v2.1.1 corrects it") as motivated retrospection. The new wording describes the sequence factually: v2.1.0 scoped narrowly; v2.1.1 added the doc the next day.

### Changed — DRs

- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** *Evidence Base* gains the 2026-06-11 paper-scale prose entry: first paper-scale prose replication of the disjoint-coverage prediction; zero overlap between Pass 1 (Haiku, 5 findings) and Pass 2 (Opus, 5 findings) load-bearing findings; opposite token-cost ratio to the 2026-06-08 code-tooling baseline. Strengthens the within-family disjoint-coverage claim.

### Adopter notes

- **PATCH-vs-MINOR call:** this release adds a new public structural pattern (the `vv/` directory) and renames the `agents/` vs `templates/` principle. Both are minor additions, not breaking changes — no existing template contracts changed, no DR semantics revised. Per the convention, MINOR fits.
- **Recommended for adopters:** if your paper project has its own load-bearing arguments whose validity depends on future evidence, mirror the `vv/hypothesis-log.md` pattern at your paper's root (or wherever your `vv/` lives). If you run named framework-scale operations (audits, batch verifications), mirror `vv/cost-log.md` as a framework-level companion to your paper-level cost log.
- **No path-level breaks.** Files moved in v2.1.0 (`agents/equation-checker.md`, `agents/review-prompt.md`) stay where they are.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.1.2`, update to `v2.2.0`.

---

## v2.1.2 (2026-06-11)

Agent-driven Quickstart. The README's Quickstart described *what* gets set up but read as a checklist a human applies. The framework is for *AI-augmented* writing — most of the steps are things you delegate. **PATCH release:** README-only edit adding a new `### Driving it with your agent` subsection, no template / DR / tool surface changed.

### Changed

- **`README.md`** — new `### Driving it with your agent` subsection inserted under Quickstart, between *Three tiers of adoption* and the implementation-detail divider. Four copy-paste prompts cover the most common operations:
  1. **Bootstrap a new paper project** — one-shot prompt that creates `papers/<name>/`, copies the minimum-viable adoption files, fills CLAUDE.md identity, initialises the registry, commits, and sets up session continuity.
  2. **Register claims as I draft** — background companion mode the agent runs while the human writes; entries flagged as the human types, coverage summary at section end, citations auto-verified at Step 0.
  3. **Verify a single citation** — one-shot lookup walking Step 0 + 6 of the anti-hallucination checklist with PASS / FAIL / NEEDS-CONTENT-CHECK output per step.
  4. **Run a peer-review pass** — in a fresh session of a different model, applying `agents/review-prompt.md` per DR-011's three-pass pattern (intra-family small / intra-family large / cross-vendor).
- Closing pointer at [`docs/non-claude-setup.md`](docs/non-claude-setup.md) for non-Claude-Code adopters — the prompts work as-is across vendors; the setup doc covers per-tool entry points for how to load them.

### Adopter notes

- **No template / DR / tool surface changed.** Pinned consumers bumping v2.1.1 → v2.1.2 inherit only the new Quickstart subsection.
- **Recommended:** if you maintain your own paper project, consider mirroring the four-prompts pattern in your own README. The prompts are deliberately generic — replace `<framework>` and `<paper>` placeholders and they work for any paper.
- **The prompts are not new templates.** They are README-level documentation of how to delegate operations the agent could already perform — the framework's `agents/` directory and `templates/` checklists were always agent-runnable; v2.1.2 just makes that explicit in the Quickstart instead of implicit.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.1.1`, update to `v2.1.2`.

---

## v2.1.1 (2026-06-11)

Practical-setup doc for non-Claude-Code agents. v2.1.0 made the framework agent-agnostic in convention (the `agents/` directory + generalised Hard Constraint), but a fresh Cursor / Copilot CLI / Continue user still had no clear "where do I start" landing. This release adds [`docs/non-claude-setup.md`](docs/non-claude-setup.md). **PATCH release:** new doc + discoverability fixes, no template / DR / tool surface changed.

### New

- **`docs/non-claude-setup.md`** — covers the framework's agent-facing surface (`CLAUDE.md`, `agents/<role>.md`, in-repo `memory/`), the universal four-step pattern (orient → load role prompt → provide artefact → persist state), tool-specific entry points for GitHub Copilot CLI / Cursor / Continue / Aider / web chat (ChatGPT, Gemini, Claude.ai), an explicit *"things to verify per tool"* checklist, and a *"what you do not need to do"* section (no renaming `CLAUDE.md` → `AGENTS.md`; no parallel `agents/` copies per vendor; no per-agent Hard Constraint set). Vendor-specific syntax notes are flagged as point-in-time correct; adopters are pointed at each tool's own current docs for authoritative install / auth steps.

### Changed

- **Root `CLAUDE.md`** — new Before You Start row pointing at `docs/non-claude-setup.md` ("Using the framework with an agent other than Claude Code").
- **`README.md`** — *Agent-Role Prompts* section's closing paragraph gains a pointer at `docs/non-claude-setup.md` for practical setup.

### Sequence relative to v2.1.0

v2.1.0 made the structural move (`agents/` directory + Hard Constraint generalisation) and deliberately scoped out the non-Claude setup doc, citing inability to genericise the source pattern in `agent-ready-assessment` (which is HAN-institutional). v2.1.1 ships the doc the next day, written from scratch against the framework's own agent-facing surface rather than copied from the source pattern. The release is additive, not corrective: v2.1.0's choice to ship the structural move first and the setup doc second is preserved in history rather than rewritten.

### Adopter notes

- **No template / DR / tool surface changed.** Pinned consumers bumping v2.1.0 → v2.1.1 inherit only the new doc and two discoverability fixes.
- **Recommended:** if you maintain your own paper-project `CLAUDE.md` and have non-Claude collaborators, mirror the Before You Start row pointing at the framework's `docs/non-claude-setup.md`.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.1.0`, update to `v2.1.1` to surface drift cleanly.

---

## v2.1.0 (2026-06-11)

Agent-agnostic move. The framework's portable agent-role prompts are split out from `templates/` into a new top-level `agents/` directory, and the Hard Constraint about in-repo memory is generalised so it speaks of "any agent's user-level auto-memory" rather than naming Claude Code as the only case. Convention mirrored from [`agent-ready-assessment`](https://github.com/ducroq/agent-ready-assessment)'s `agents/` directory pattern.

The principle being made explicit: **templates are files you copy and populate over time; agent-role prompts are files you paste once into any agent's system-prompt slot.** Two kinds of artefact, two locations. Adopters and reviewers reading the framework for the first time now see the distinction structurally instead of having to infer it from the contents of each file.

### New

- **`agents/`** — new top-level directory with portable agent-role prompts. Each file is a complete "you are X" system prompt that runs in Claude Code, GitHub Copilot CLI, Cursor, ChatGPT, Gemini, or any other agent harness.
- **`agents/README.md`** — directory purpose; the line between agent-role prompts (here) and fill-in templates (in `templates/`). Documents the vendor-neutrality convention.
- **`agents/equation-checker.md`** — moved from `templates/equation-checker.md` via `git mv` (history preserved). Mechanical equation & numerical verifier — substitute values, compute, flag discrepancies.
- **`agents/review-prompt.md`** — moved from `templates/review-prompt.md` via `git mv`. Peer-review simulator with multi-pass bias-escape semantics per DR-011 (Pass 1 intra-family small / Pass 2 intra-family large / Pass 3 cross-vendor with style filter).

### Changed

- **README.md** — Templates section trimmed (review-prompt + equation-checker rows removed); new `## Agent-Role Prompts` section added between *Templates* and *Tools*; intro sentence to *Templates* clarifies the fill-in vs single-shot distinction. All inline references to the two moved files updated to point at `agents/`.
- **Root `CLAUDE.md`** — Architecture diagram gains an `agents/` block above `templates/` and the two moved entries are removed from `templates/`. New Before You Start row pointing at `agents/`. Hard Constraint about in-repo memory generalised to "any agent's user-level auto-memory"; Claude Code's path retained as the named instance; Cursor and Copilot CLI named as other agents the same separation principle applies to.
- **`templates/CLAUDE.md`** (adopter paper template) — Before You Start row about reviewing now mentions both paper-local copy *and* the framework's `agents/review-prompt.md` as valid paths; new row for `agents/equation-checker.md`. Hard Constraint generalised in parallel with root CLAUDE.md. Directory Structure no longer shows `review-prompt.md` as a paper-local file — adopters reference the framework's `agents/` directly unless they explicitly choose to keep a paper-local copy.
- **`templates/anti-hallucination.md`** — inline reference to `templates/review-prompt.md` updated to `agents/review-prompt.md`.
- **DRs** — DR-009, DR-011, DR-013 inline references updated to the new `agents/` paths. DR-013's "Markdown templates" list split into "Markdown templates" + "Agent-role prompts" sub-bullets to reflect the new structure; license scope unchanged (everything stays CC BY 4.0).
- **`docs/THRESHOLDS.md`** — two inline references to `templates/review-prompt.md` updated.

### Convention origin

`agent-ready-assessment` has shipped an `agents/` directory at its repo root since at least its v1.2.0 era — used there for *quality-gate* agents that operate on assessment outputs (audit, calibrate, check-rubric-design, review-prompt-design). The pattern translates cleanly: portable agent-role prompts that work across modules / papers belong at the repo root, not inside a per-module / per-paper subdirectory. This release adopts that pattern for agent-ready-papers.

### Adopter notes

- **Path-level breaking change for pinned consumers who reference the two moved files by path.** If your project's `CLAUDE.md`, build scripts, or paper-local docs reference `templates/equation-checker.md` or `templates/review-prompt.md`, update to `agents/equation-checker.md` and `agents/review-prompt.md`. The files' *contents* are unchanged — only their location.
- **Why this is MINOR despite the path change:** the surface affected is two files out of ~20 templates/agents combined; the move is mechanical (`git mv` preserved history); and both files were already framed as standalone agent system prompts (i.e., their internal contract was always "copy and paste into an agent", not "edit in place over the project's lifetime"). The MAJOR threshold is reserved for breaking changes to *template contracts* or *DR semantics* — neither happened here.
- **No change for adopters who don't reference these paths directly.** If your paper's verification workflow runs the prompts via copy-and-paste rather than path reference, you don't need to do anything.
- **The generalised Hard Constraint is documentation-level only.** No agent enforcement changes; the principle (in-repo `memory/` is canonical for project state) was already correct for any agent.
- **Self-pin bump:** if your `CLAUDE.md` pins `agent-ready-papers: v2.0.2`, update to `v2.1.0` to surface drift cleanly at session start.

---

## v2.0.2 (2026-06-11)

README self-audit fixes. Applying the framework's verification checklist to the `## This README, registered` section shipped in v2.0.1 surfaced three small failures against the framework's own rigor. **PATCH release:** README-only edits, no template/DR/tool surface changed.

### README — three fixes

- **Type-consistency note in `## The Argument, Structurally`.** R-1 is registered as a PROPOSITION, but the section presents the same statement via Toulmin (which the framework reserves for ARGUMENT verification). The closing sentence now clarifies the two views coexist by design: the Toulmin block decomposes the *argument* the framework rests on; R-1 below states the *proposition* the argument supports, with Whetten-style boundary conditions. Argument verifies the reasoning chain; proposition verifies the recommendation; same case, two checklists.
- **Source tightening on R-3 and R-4.** Both rows previously cited maintainer-local sources public readers couldn't verify. R-3's "replicated in own audits" pointed at `audits/`, which was scrubbed from the public repo in v2.0.0 and is gitignored. R-4's "Gemini missed 3/3 errors that Sonnet caught" lives in gitignored `memory/gotcha-log.md`. Sources are now constrained to publicly-verifiable halves: R-3 cites the hallucination literature within `templates/anti-hallucination.md`; R-4 cites DR-009 (calculation-verification rationale) and `templates/equation-checker.md` (designed implementation).
- **Format note above the registered table.** The single-table layout (CLAIM-style columns with ARGUMENT/PROPOSITION fields inlined into the Statement cell) is a README-brevity compression, not the framework's normative per-type-sub-table layout. New paragraph above the table acknowledges this and points adopters at `templates/claim-registry.md` for actual paper registries.

### Adopter notes

- **No template / DR / tool surface changed.** Pinned consumers bumping v2.0.1 → v2.0.2 inherit only README clarifications.
- **Self-pin bump only:** if your `CLAUDE.md` pins `agent-ready-papers: v2.0.1`, update to `v2.0.2`; no functional change.
- **Pattern worth carrying back to your own README:** applying the framework to its own home document on the first pass (v2.0.1) produced three rigor-check violations, surfaced by an explicit self-audit prompt. The self-audit is itself a productive framework output — expect ~2-4 type / source / format gaps to surface on the first audit of any document the framework wasn't originally drafted around.

---

## v2.0.1 (2026-06-10)

README logic-application pass. The framework is applied to its own home document — a four-move coordinated edit using the same discipline the README proposes for adopters' papers. **PATCH release:** README-only edits, no template/DR/tool surface changed.

### README — four moves

- **`## The Argument, Structurally`** — new section inserted between *The Approach* and *When-Worth-It*. Five-row Toulmin table making the central argument inspectable: Claim (process-level verification infrastructure benefits AI-augmented writing) / Grounds (the five failure modes) / Warrant (tool-level and model-level techniques don't reach the process layer) / Qualifier (EMERGING — own use, not externally validated) / Rebuttal (the four When-Overkill cases).
- **Confidence-language calibration sweep** across seven load-bearing spots. ESTABLISHED-tier language ("catches", "prevents", "surfaces", "for everything", "will re-propose", "the most common") downshifted where the underlying claim is EMERGING or SPECULATIVE. Examples: `catches these failure modes` → `designed to catch these failure modes`; `Reproducing the calculation surfaces what assessment misses` → `…is designed to surface…`; `default to confident language for everything` → `default to confident language regardless of tier`; `prevents scope creep — the most common failure mode` → `constrains scope creep — a common failure mode`; `prevents terminology drift` → `guards against terminology drift`; `agents will re-propose excluded approaches` → `agents repeatedly re-propose excluded approaches across sessions`.
- **`## When This Framework Is Worth The Overhead`** and **`## When It Is Overkill`** — rewritten as **testable boundary conditions**. Each bullet is now yes/no-answerable for a specific project. When-Worth-It: hallucination cost exceeds review cost / context cannot fit in a single session / at least one claim is load-bearing / confidence language is read as a signal. When-Overkill: no citation surface / correctness verified by execution / audience of one / established audit conventions already cover it (FDA 21 CFR 820, IEC 62304, ISO 17025, GDPR DPIA, regulated clinical trial reporting).
- **`## This README, registered`** — new section near the bottom. Seven entries R-1…R-7 (3 CLAIMs / 1 ARGUMENT / 3 PROPOSITIONs; 0 ESTABLISHED / 3 SUPPORTED / 3 EMERGING / 1 SPECULATIVE) registering the README's load-bearing claims with priority, type, confidence tier, source, and section anchors. Coverage note explains the deliberate absence of ESTABLISHED tier (no validated efficacy claims about the framework itself); *Why this section exists* documents the rationale.

### Adopter notes

- **No template / DR / tool surface changed.** Pinned consumers bumping v2.0.0 → v2.0.1 inherit only README clarifications.
- **Recommended for adopters:** mirror the *This README, registered* pattern in your own paper project's README — applying the framework to the document that describes the framework is a low-cost credibility move.
- **Self-pin bump only:** if your `CLAUDE.md` pins `agent-ready-papers: v2.0.0`, update to `v2.0.1` to surface drift cleanly at session start; no functional change.

---

## v2.0.0 (2026-06-10)

Repository scope-tightening + README reflection pass. This release is a **MAJOR bump** because two public artifacts have been removed entirely:

- `templates/physics-verification/` — nine-file physics-paper verification template family removed. The methodology lives on conceptually but the template files are no longer shipped.
- `docs/METHODOLOGY.md` — methodology-derivation narrative removed.

In addition, all in-text references to specific source projects and audit findings have been replaced with generic phrasing throughout templates, DRs, and Paper 1 supporting files. The framework now stands on its own design rationale rather than enumerating which projects it was derived from.

### Removed
- **`templates/physics-verification/`** — all nine templates (`cross-document-consistency.md`, `dimensional-checker.md`, `estimation-checker.md`, `lean-as-optional-tier.md`, `limiting-case-checker.md`, `scope-domain-registry.md`, `two-paths-consistency.md`, `verification-tier-hierarchy.md`, `README.md`). Adopters who pinned to v1.7.x and depended on this family must either freeze on v1.7.x or replace with their own equivalents.
- **`docs/METHODOLOGY.md`** — derivation narrative. No replacement; the framework is now described entirely by README + templates + DRs.
- **`audits/`** — directory and its contents are gitignored and no longer published. Adopters do not need this directory.

### Changed — README restructure (front-of-file)
- **Order:** Problem → Approach → When-Worth-It → When-Overkill → Common Questions → Quickstart → (divider) → details. The case is made before the action is asked for.
- **Status hedge:** A new line near the top declares the framework as "a working framework we use on our own papers" with broader empirical validation as an open question. The README's previous confident framing is calibrated.
- **Common Questions** section added: overhead, small-paper applicability, vs. reference managers, non-AI use, peer-review status.
- **One row, concretely** worked-example added to the Verification Registry section so adopters see a populated CLAIM entry inline rather than via a click-through.
- **What Doesn't Work** tightened from eight paragraphs to eight one-liners with backlinks to the explanatory sections.
- **Workflow Phases** consolidated with the former Session Continuity and Project File sections; now includes an explicit Phase→Gate mapping table.
- **Tools cost-log** reframed from "empirical operation costs from Paper 1" to "self-applied cost data (N=2, code-tooling scale)" with honest scope caveats.

### Changed — Paper 1
- **`papers/perspective/manuscript.tex`** — Section 4 (Preliminary Evidence) collapsed from a two-audit case-study presentation into a shorter "Related Work and Design Rationale" section. Appendix A's worked examples are rewritten to use generic illustrations. The paper is publishable as a pure proposal/perspective; the empirical anchors from the source-project audits are removed.
- **Supporting files** (`CLAUDE.md`, `backlog.md`, `backlog-paper2.md`, `writing-guide.md`, `vv/claims/claim_registry.md`) — all audit references removed; sources column reset to "own design rationale" or generic phrasing where source-project citations were used.

### Changed — templates
- **`templates/anti-hallucination.md`** — Step Z worked example uses a generic DSM-form imitation rather than naming a specific speculative-design book.
- **`templates/equation-checker.md`** — origin comment removed (referenced source project).
- **`templates/claim-registry.md`** — inverse-hallucination note genericised.
- **`templates/hypothesis-log.md`** — example tags genericised.
- **`templates/vv-framework.md`** — Gate 2.7 source-pattern pointer removed.

### Changed — DRs
All DRs that referenced audits or specific source projects (DR-004, 006, 007, 008, 009, 010, 011, 012, 013, 014) have had their evidence-base sections, triggering-observation blocks, and audit pointers rewritten. The decisions themselves are unchanged; their evidence narratives are genericised.

### Adopter notes
- **Pinned consumers on v1.7.x using `templates/physics-verification/`**: this is a breaking change. Freeze on v1.7.1 (`git checkout v1.7.1 -- templates/physics-verification/`) or replace with your own family.
- **Pinned consumers on v1.7.x using `docs/METHODOLOGY.md`**: same — freeze or write your own.
- **Pinned consumers using only the core templates** (`CLAUDE.md`, `claim-registry.md`, `vv-framework.md`, `writing-guide.md`, `review-prompt.md`, `decision-record.md`, `anti-hallucination.md`, `glossary.md`, `equation-checker.md`, `cost-log.md`, `hypothesis-log.md`, `key-quotes.md`): templates' contracts are unchanged. Migrate by bumping your pin to `agent-ready-papers: v2.0.0`. The minor template edits (Step Z example, etc.) do not affect the surface adopters consume.

### Origin

This release reflects a deliberate scope-tightening decision. The framework's public artifact is now intentionally smaller and self-contained: it does not point at evidence outside its own files, and it does not enumerate source projects. The README reflection pass that produced the restructure is documented in this session's curate output.

---

## v1.7.1 (2026-06-09)

Companion pin bump: `agent-ready-projects` advanced from v1.10.2 → v1.10.3. Upstream v1.10.3 added structural-lint self-tests at `tests/lint/` — maintainer-only infrastructure with no template-surface change.

### Documentation
- **Root `CLAUDE.md`** — Companion pin: `agent-ready-projects: v1.10.2` → `v1.10.3`. Self-pin: `v1.7.0` → `v1.7.1`.
- **`README.md`** — Current release line bumped to v1.7.1.

### Adopter notes

No action required. PATCH release, metadata-only.

---

## v1.7.0 (2026-06-09)

Full adoption of agent-ready-projects v1.10.0 features. Two upstream additions land here: the **hypothesis log** (provisional positions with pre-registered falsification criteria) and the **self-verifying memory posture** (verify-comments embedded in state claims, audited by `/curate` Step 0 sub-step 5). Companion pin advances to v1.10.2.

The two additions answer different questions. Decision records freeze rationale at decision time; the gotcha log captures problems with known root causes. Neither has a home for *bets* — provisional positions whose evidence lives in the future. Self-verifying memory addresses a different failure mode: state claims in `memory/` decay immediately after the session that writes them.

### Templates
- **`templates/hypothesis-log.md`** — new template, adapted from agent-ready-projects v1.10.0. Lifecycle: open → dormant → revisit → resolved (close or promote to DR). Adopters: copy to your paper project's root and populate.
- **`templates/CLAUDE.md`** — three edits to surface hypothesis-log: new Before You Start row, Key Files row, Directory Structure entry.

### Documentation
- **Root `CLAUDE.md`** — companion pin bumped, self-pin bumped, new Before You Start row for the hypothesis-log, new Hard Constraint for self-verifying memory.

### Adopter notes
- **Recommended migration for pinned consumers on v1.6.3:**
  1. Copy `templates/hypothesis-log.md` to your paper project root.
  2. Add the new Before You Start row in your paper project's `CLAUDE.md` — see updated `templates/CLAUDE.md` for the exact phrasing.
  3. Self-verifying memory: optional and incremental. Add `<!-- verify: cmd -->` comments to new state claims going forward.
- **No template-content breaking changes.**

---

## v1.6.3 (2026-06-08)

Backlog discoverability. Framework backlog is distributed by velocity — `memory/MEMORY.md` "Next session priorities" for volatile near-term items, DR *Open Questions* sections for decision-specific long-burn items. No single `BACKLOG.md` file by design.

### Documentation
- **Root `CLAUDE.md`** — new Before You Start row pointing at the backlog locations with their velocity semantics named.

### Adopter notes
- **No template content changes.** PATCH release.

---

## v1.6.2 (2026-06-08)

Framework convention codification: in-repo memory is canonical for project state.

The conflict: a *global* "you have this memory system" instruction (framed as agent capability, loaded early in the system prompt) versus a *project-level* routing instruction (framed as task trigger). The global one wins by default unless the project explicitly tells the agent otherwise.

### Documentation
- **Root `CLAUDE.md`** — new Hard Constraint: project state goes in `memory/` (in-repo, gitignored), not in user-level Claude Code auto-memory.
- **`templates/CLAUDE.md`** — same constraint, phrased for adopters.

### Adopter notes
- **PATCH release.** No template content changes.
- **Recommended for adopters using Claude Code:** mirror the constraint in your own paper project's `CLAUDE.md`.

---

## v1.6.1 (2026-06-08)

README discoverability fix. v1.5.0 shipped `tools/`, v1.6.0 shipped `templates/cost-log.md` — neither was threaded through the public-facing README.

### Documentation
- **`README.md`** — current-release line bumped; *Anti-Hallucination Checklist* gains an automated-companion note pointing at `python -m tools.check_dois`; new *## Tools* section between *Templates* and *Paper Projects*; *Templates* index gains a row for `cost-log.md`.

### Adopter notes
- **No template content changes.** README-only edits.

---

## v1.6.0 (2026-06-08)

Operation cost logging. New `templates/cost-log.md` template + per-paper `vv/cost-log.md` convention for tracking token cost of major framework operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps).

### New template
- **`templates/cost-log.md`** — column structure for per-paper operation cost log: date, operation, total tokens, input/output deltas, cache read, wall clock, notes. Top-of-file convention paragraph documents how to use `/status` for the deltas.
- **`papers/perspective/vv/cost-log.md`** — Paper 1 bootstrap data.

### CLAUDE.md updates
- **`templates/CLAUDE.md`** — Before You Start row added: *"Logging token cost of an operation"* → `vv/cost-log.md`.
- **`papers/perspective/CLAUDE.md`** — same row added.

### Adopter notes
- **Optional.** The cost-log is a convention, not a required surface.
- **Recommended** if you want to make decision-record cost-vs-value claims quantitative or if you want to budget framework overhead per paper.

---

## v1.5.1 (2026-06-08)

CLAUDE.md discoverability fix. v1.5.0 shipped the `tools/` directory but did not update any of the three CLAUDE.md files (root, Paper 1, paper template) to point future agent sessions at the tools.

### Documentation
- **Root `CLAUDE.md`:**
  - Architecture diagram — `tools/`, `tests/`, `Makefile`, `pyproject.toml` rows added.
  - Before You Start — two new rows: *"Checking coverage or DOIs in a registry"* and *"Asking what a coverage or peer-review threshold means"*.
  - How to Work Here — replaced the manual percentages comment with `python -m tools.coverage` and `python -m tools.check_dois` commands.
- **`papers/perspective/CLAUDE.md`** — Before You Start gains a row pointing at the tools with the correct registry path.
- **`templates/CLAUDE.md`** — Before You Start gains the same row with adopter-facing path placeholders.

### Adopter notes
- **No template content changes.** Only the agent-orientation tables.

---

## v1.5.0 (2026-06-08)

Registry-verification tooling. The `tools/` directory introduces the first Python footprint in the repo: two zero-dep CLIs that read a `claim_registry.md` and answer two operational questions — *what is my coverage* and *do all my DOIs resolve*.

### New tooling
- **`tools/coverage.py`** — per-type sub-table parser. Walks a claim registry, identifies `**CLAIMs:**` / `**ARGUMENTs**` / `**PROPOSITIONs**` / `**PROVOCATIONs**` sub-tables by marker, counts verified entries. Markdown and JSON output. Exit codes 0 (success) / 1 (with `--strict`, target missed) / 2 (tooling error).
- **`tools/check_dois.py`** — DOI extractor and resolver. Regex-extracts DOIs, HEAD against `https://doi.org/` without redirect-following. `--offline` mode verifies parseability only.
- **`tools/README.md`** — usage, exit codes, design constraints, known limits.
- **`Makefile`, `pyproject.toml`, `.gitignore`** — first Python footprint in the repo: ruff config, pytest config, py3.10 target.
- **`tests/`** — shape-pin tests against the Paper 1 fixture.

### Adopter notes
- **No template changes.** All additions are opt-in tooling.
- **Optional adoption.** If you maintain a `claim_registry.md`, you can run `python -m tools.coverage <your-registry.md>` and `python -m tools.check_dois <your-registry.md>`.
- **Known limits documented in `tools/README.md`.**

---

## v1.4.0 (2026-06-08)

The framework gains a LICENSE (CC BY 4.0), three new top-level docs (`CONTRIBUTING.md`, `UPGRADING.md`, `docs/THRESHOLDS.md`), two new DRs (DR-013 Accepted, DR-014 Proposed), substantially restructured README front-of-file (Quickstart + adoption tiers), and the maintainer release process is codified in this CHANGELOG's header.

### New decisions
- **[DR-013](decisions/DR-013_license-choice.md)** — *License Choice — CC BY 4.0.* Status: Accepted.
- **[DR-014](decisions/DR-014_provocation-layered-as-opt-in-extension.md)** — *PROVOCATION as Explicit Opt-In Extension Over Core Unit Types.* Status: Proposed.

### New top-level files
- **`LICENSE`** — CC BY 4.0 deed + canonical legal-code URL + citation block.
- **`CONTRIBUTING.md`** — contribution guide.
- **`UPGRADING.md`** — per-version adopter-notes aggregation for pinned consumers.

### New docs
- **`docs/THRESHOLDS.md`** — rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds. Top-of-file **SPECULATIVE** label per the framework's own confidence-tier discipline.

### README restructure (front-of-file)
- **## Quickstart + Three tiers of adoption** — 5-step ~10-minute path with the minimum-viable-adoption file table.

### CLAUDE.md changes
- **`.claude/skills/` and `memory/`** in the architecture diagram now labelled as gitignored.
- **New ## What is intentionally not shipped section** — table covering `/curate`, `/audit-context`, `MEMORY.md`, `gotcha-log.md`, `dead-ends.md`.

### Adopter notes
- **No breaking changes.** All adopter-facing changes are additive.
- **DR-013 licence:** new contributions are CC BY 4.0 from v1.4.0 forward.

---

## v1.3.0 (2026-06-01)

DR-012 names decision-support as a third opt-in application class; DR-011 evidence base extended; anti-hallucination gains WebFetch fallback discipline; claim-registry adds Coverage-by-Type cut; Paper 1 registry migrated to per-type sub-tables.

### New decisions
- **[DR-012](decisions/DR-012_decision-support-artefacts.md)** — *Decision-Support Artefacts as Third Non-Paper Application Class.* Status: Proposed.

### New templates / pattern additions
- **`templates/claim-registry.md`** — Coverage Summary now cuts both by Priority and by Type. Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating.
- **`templates/anti-hallucination.md`** — adds *Verifying Web Sources: WebFetch Fallback Discipline* between *Verifying Negative Claims* and Step Z. Names two failure modes (subpage blindspot; transport failure) and prescribes a fallback ladder.

### Paper 1
- **`papers/perspective/vv/claims/claim_registry.md`** — migrated from legacy single-mixed-type table per section to per-type sub-tables (CLAIMs / ARGUMENTs / PROPOSITIONs). List delimiter normalised to `;`. Coverage Summary gains by-type cut.

### Versioning
This is the framework's first explicitly-versioned release. Prior versions (v1.0.0 through v1.2.0 below) are reconstructed retroactively from the git history.

---

## v1.2.0 (2026-05-29)

Multi-pass review pattern + structural rationale + per-type registry surface.

### New decisions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** — *Multi-Model Review Pattern.* Three-pass review with explicit bias-escape semantics: Pass 1 (intra-family small), Pass 2 (intra-family large), Pass 3 (cross-vendor) requires a mandatory style/voice filter. Status: Proposed.

### Template / pattern additions
- **`templates/claim-registry.md`** — per-type sub-tables (one each for CLAIMs / ARGUMENTs / PROPOSITIONs / PROVOCATIONs) with checklist-aligned columns.
- **`templates/writing-guide.md`** — tier-monotonicity principle added: manuscript language must sit at or below the registered confidence tier.
- **`templates/review-prompt.md`** — *Style/voice rules to filter against* added as a required-with-default field per DR-011 Pass 3 requirement.
- **`templates/anti-hallucination.md`** — Step 7 (Multi-Pass Review Across Model Families) added per DR-011.

### Docs / structural rationale
- **`docs/category-theory-as-design-lens.md`** — names the structural lens implicit across DR-004 (typed registry), DR-011 (multi-pass functors), and the layered memory system.

### Adopter notes
- Pre-existing registries with the legacy single-mixed-type table still work; migration to per-type sub-tables is mechanical and recommended at next major revision.

---

## v1.1.0 (2026-05-10)

Speculative-design extension. DR-010 activates DR-004's reserved non-empirical slot with PROVOCATION as a fifth opt-in unit type.

### New decisions
- **[DR-010](decisions/DR-010_provocation-unit-type.md)** — *PROVOCATION as Fifth Unit Type for Speculative-Design Work.* Status: Accepted. Separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL), each tier carrying a required prose marker. Opt-in: default registry type remains CLAIM.

### Template / pattern additions
- **`templates/claim-registry.md`** — PROVOCATION row in the Unit Type Reference; PROVOCATION-tier confidence row in the Confidence Tiers table; reflexive-marker required field.
- **`templates/anti-hallucination.md`** — Step Z (Inverse Hallucination Check, PROVOCATION-specific) added. Catches the failure mode where speculation is presented as if sourced.
- **`templates/vv-framework.md` / quality gates** — three project-conditional gates added:
  - **Gate 2.6 — Reflexivity.** Every PROVOCATION carries a reflexive marker visible in the prose.
  - **Gate 2.7 — Ethical Review.** For projects engaging contested topics.
  - **Gate 2.8 — Voice Consistency.** For voice-driven work.

### Adopter notes
- PROVOCATION is opt-in. Projects without speculative-design content can ignore the new unit type, gates 2.6/2.7/2.8, and Step Z entirely.

---

## v1.0.0 (2026-05-09)

Baseline release of the framework. Captures the state reached through DR-001 through DR-009 plus DR-010 reserved, 47 indexed literature sources, and active development of Paper 1 (Verification Gap).

### Decisions in scope at v1.0.0
- **DR-001** through **DR-009** as documented in [`decisions/`](decisions/).
- Notable highlights:
  - **DR-002** — confidence tiers (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) and the language-calibration mapping.
  - **DR-004** — typed verification model (CLAIM / ARGUMENT / PROPOSITION); reserved slots for future non-empirical work (DR-010 activates one such slot in v1.1.0).
  - **DR-005** — nanoarguments / argument-layer peer concept (extended in v1.2.0).
  - **DR-006** — publication roadmap (Papers 1 / 2 / 3).
  - **DR-007** — SE-inspired verification identity.
  - **DR-008** — methodological-facts exception for own-data claims.
  - **DR-009** — calculation verification as distinct procedure.

### Templates in scope at v1.0.0
- `templates/CLAUDE.md` — paper project identity template.
- `templates/claim-registry.md` — registry structure with P0/P1/P2 priority, typed verification (legacy single-mixed-type table format; migrated to per-type sub-tables in v1.2.0).
- `templates/vv-framework.md` — verification & validation framework, quality gates.
- `templates/writing-guide.md` — confidence-tier to language mapping.
- `templates/review-prompt.md` — structured peer review simulation (single-shot pre-DR-011).
- `templates/anti-hallucination.md` — Step 0 + 6-step citation verification (pre-Step-Z, pre-Step-7).
- `templates/equation-checker.md` — mechanical equation verification (DR-009).
- `templates/decision-record.md` — DR template.
- `templates/glossary.md` — cross-domain terminology.
- `templates/key-quotes.md` — reference quotes.
- `templates/physics-verification/` — physics-verification template family.

### Adopter notes
- v1.0.0 is the baseline pin for adopters who started with this framework before the speculative-design extension. Upgrading to v1.1.0 is opt-in (PROVOCATION is opt-in); upgrading to v1.2.0 brings the multi-pass review pattern as a recommended-but-not-required workflow improvement.
</content>
</invoke>