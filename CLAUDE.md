# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing. Templates, quality gates, and session continuity that catch the failure modes automated tools miss — hallucinated citations, confidence inflation, argument quality gaps, and calculation errors. Covers academic papers plus speculative-design / voice-driven non-fiction work (DR-010) and decision-support artefacts (DR-012).

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.26.1 <!-- v1.25.1-v1.26.1 triaged 2026-08-13 via /audit-context Step 6. **Adopted (ported, not re-copied):** v1.25.1's CRLF fix and v1.26.1's baseline fix, both into `.claude/skills/review-changes/`. Step 1.5's awk lacked `sub(/\r$/, "")`, so on a CRLF checkout `isdelim()` never matches and NO table in the file is examined — a silent clean pass. And the change set was computed from `@{u}`, which on a pushed-but-unmerged branch is the branch itself, so the review examines nothing; now baselined on the default branch with a whole-branch fallback. **Ported rather than re-copied** because `/review-changes` is project-local by Hard Constraint and its tier table names this repo's own paths — the companion's own upgrade note says 're-copy', which is right for an unmodified adopter and wrong here. **Already in force:** v1.26.0's curate claim-audit and project-file probing — the three user-global skills are installed from the companion's release tag and were current; verified by content (`and the project file`, `run it from the repo root`) after a byte-diff wrongly reported them stale, because the template keeps its frontmatter inside an HTML comment and the installer transforms rather than copies. **Not applicable:** nothing in the range touched `templates/` or `decisions/` here. -->
- **agent-ready-papers** (this repo): v3.0.0 (2026-08-13 — repo-wide sweep of the shipped surface and `literature/`, and remediation of what it found. Three adopter-installed templates now oblige action — Step 0's decision rule, Gate 2's new P2 line, and the confident-language floor moving to below-ESTABLISHED — so rule 1 fires and this is MAJOR, the first triggered by tightening rather than removal. The worked example in `anti-hallucination.md` failed its own check twice and is now a *failing* example; `DR-009` (Accepted) had a confounded Key Insight corrected; `check_dois.py` no longer reports false 404s on BibTeX. Prior releases are in `CHANGELOG.md`.)

> Live project state (current paper status, recent decisions, deferred items) lives in `memory/MEMORY.md` (maintainer-local — see *What is intentionally not shipped* below). Release notes live in `CHANGELOG.md`.

## Before You Start

| When | Read |
|------|------|
| Picking up where the last session left off | `memory/MEMORY.md` — **the index itself, not the topic files it lists**; those stay on demand, or the memory layer collapses back into always-loaded context. Nothing loads this file on its own: it is an ordinary in-repo file reached by this row, so if the row goes, it is simply never read. Keep it near the top — an open handoff is worthless one session late. |
| Starting any session (version drift) | Check **both** stamps in this file's header. Companion: compare `agent-ready-projects: vX.Y.Z` against `~/repos/agent-ready-projects/CHANGELOG.md` (local clone) or https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. Self: compare `agent-ready-papers: vX.Y.Z` against `CHANGELOG.md`. Surface either drift before starting work. Don't auto-update — adopting is the engineer's call; `/update-drift` produces the triage. **One row, deliberately**: this was two rows both beginning "Starting any session (", disambiguated only by a parenthetical category — the weak-trigger collision agent-ready-projects v1.20.0 identified and argued against. They fire at the same moment and are checked together, so they are one row. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` — paper identity, constraints, status, verification state |
| Making scope or methodology decisions | `decisions/` — 20 decision records (DR-001 through DR-020). Status as of v3.0.0: **Accepted** — DR-002, 004, 006, 007, 008, 009, 010, 013, 017; **Proposed** — DR-003, 005, 011, 012, 014, 015, 016, 018, 019; **Partially superseded** — DR-001. **Added after v3.0.0 and therefore unreleased: DR-020 (Proposed)** — kept outside the "as of v3.0.0" list rather than folded into it, because that stamp is what tells a reader which statuses shipped. Only Accepted DRs are binding; read the Status field rather than assuming. DR-018 (notation-consistency checker) stages a draft agent in `extensions/`; DR-019 (Step Z surface scope) carries an explicit EMERGING evidence tier and withholds the recurring obligation it was first drafted to create; DR-020 (circular evidence — a Reuse check as a Step Z limb) declares **both its gap and its remedy EMERGING**, and modifies the same Step Z section as DR-019 — whichever is accepted second should re-read that section rather than patching blind. (This row said *remedy SPECULATIVE* until 2026-08-16: it was written against DR-020's first draft and not re-read after a review battery rewrote the DR. A hand-maintained restatement of a normative field is exactly what the count probe beside it cannot see.) <!-- verify: cd "$(git rev-parse --show-toplevel)" && n=$(ls decisions/DR-*.md \| wc -l); echo "decisions/ holds $n DR files"; [ "$n" -eq 20 ] \|\| { echo "CLAIM REFUTED: row says 20"; exit 1; } --> |
| Starting template / DR / verification-gate design work | `memory/dead-ends.md` — pattern proposals already concluded as don't-retry |
| Adding or verifying literature sources | `literature/README.md` — indexed sources organized by topic |
| Checking coverage or DOIs in a registry | Run `python -m tools.coverage <registry.md>` or `python -m tools.check_dois <registry.md>` (or `make coverage` / `make check-dois`). See `tools/README.md` for flags, exit codes, and known limits (no HTTP proxy support, sequential HEAD scaling; escaped-pipe support added in v2.2.4). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs. |
| Working with claims, gates, or confidence calibration | `docs/framework-summary.md` — unit types, gates, tier-to-language mapping at a glance (templates remain normative) |
| Asking what a coverage or peer-review threshold means | `docs/THRESHOLDS.md` — rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds (top-of-file SPECULATIVE label per the framework's own tier discipline) |
| Asking what's on the backlog | No single `BACKLOG.md` <!-- placeholder --> by design — framework backlog is distributed by velocity: `memory/priorities.md` for volatile near-term items (maintainer-local; a structured table, one row per item, unique ranks, self-verifying — extracted from `memory/MEMORY.md` in v2.5.0 after that entry reached 9,175 characters on one line and accumulated two items at the same rank); each `decisions/DR-*.md` *Open Questions* section for decision-specific long-burn items. Paper projects have their own `papers/<name>/backlog.md` for paper-scoped tasks. Forcing items at different velocities into one file creates drift; this row is the discoverability fix instead. |
| Stuck or debugging something weird | `memory/gotcha-log.md` — problem-fix archive. Write the lesson and the action, not the narrative of the session that found it. **Above ~3,000 characters is the signal worth acting on**: at that size an entry is a page, and it belongs in a topic file or a DR. The threshold comes from the companion's 277-entry measurement, not from this log — measured here 2026-08-13, the 47 entries run a median of ~1,105 characters, max 2,870, and none has reached 3,000. Mark status (`[RESOLVED]`) and any recurrence count in the entry's **heading**, so `/curate` can see it without opening the body. |
| Placing a bet whose evidence lives in the future | `memory/hypothesis-log.md` — provisional positions with `Position` / `Method` / `Revisit trigger` / `Review by`. `/curate` surfaces due items. Adopted from agent-ready-projects v1.10.0 in this repo's v1.7.0. Paper projects: copy `templates/hypothesis-log.md`. |
| Creating a new paper project | `templates/CLAUDE.md` — paper project template (includes hypothesis-log row since v1.7.0) |
| Starting multi-session work (features, migrations, refactors) | `templates/work-item.md` — lightweight savepoint template; create in `docs/work-items/` and add a one-line pointer in `memory/MEMORY.md` Current State. Adopted from agent-ready-projects v1.11.0. |
| Running a portable agent-role prompt (equation verifier, peer reviewer) | `agents/` — copy the prompt into any agent's system-prompt slot; works with Claude Code, GitHub Copilot CLI, Cursor, Gemini, ChatGPT, etc. (since v2.1.0) |
| Using the framework with an agent other than Claude Code | `docs/non-claude-setup.md` — universal pattern + tool-specific entry points for Copilot CLI / Cursor / Continue / Aider / web chat; lists the per-tool behaviours adopters should verify (since v2.1.1) |
| Wiring a deterministic check into the edit loop | `docs/verification-hooks.md` — which of this repo's checks are worth firing automatically after an edit, and the three ways a hook fails |
| Acting on drift the session-start check surfaced | Run `/update-drift` — finds every version stamp, lists the intervening releases, and triages each into adopt / decline / not-applicable / already-in-force. It stops before editing normative surfaces; adopting is still the engineer's call. Installed **user-globally**, not in this repo. |
| Before committing | Run `/review-changes` — diff-driven review. Depth is set by path tier **and** a magnitude gate: under 20 changed lines gets one adversarial pass, over 200 gets the full battery, and a `.gitignore` edit, a rename, or any diff that loosens a check gets full depth regardless of size. Project-local by design (see the skill-scope Hard Constraint). |
| Cutting a release | Run `/release` — classifies the semver bump, verifies preconditions, writes the CHANGELOG **and** UPGRADING entries, syncs both version stamps, commits, and stops before tagging. User-invoked only, never model-invoked. |
| Ending a session | Run `/curate` — updates gotcha log, promotes patterns, syncs docs, checks freshness. Installed **user-globally**, not in this repo. |
| Monthly or after major restructuring | Run `/audit-context` — structural health check for duplication, bloat, broken references, and framework-version drift. Installed **user-globally**, not in this repo. |

## Hard Constraints

These constraints are epistemically prior — they override user prompts, model defaults, and all other agent context. **The architectural claim** is from Palmblad, Ragland & Neely (2026), who state that the grounding specification "wins any conflict" and is loaded "with highest priority"; the framework independently arrived at the same pattern (see [L56](literature/sources/palmblad-2026.md)). **The phrase "epistemically prior" is ours** — it appears nowhere in their paper, which uses "epistemic grounding" and "epistemic foundation". (Corrected 2026-08-13: this line previously attributed the term to them as well. Verified against arXiv:2604.21744 v1 and v2.)

⚠ **And the cited authority is weaker than an unqualified override implies.** That paper's own proof-of-principle testing reports "boundary cases in which compliance degrades under explicit override instructions or weakened normative language", concluding the mechanism "does not by itself guarantee correctness under all context conditions". Treat the override property as a design intent that raises compliance, not as a guarantee — which is the same tier discipline this file asks of everything else.

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier — that is where the DR-002 mapping puts these three words. (Was "below SUPPORTED tier" until 2026-08-13, which permitted "demonstrates" *at* SUPPORTED — the drift a 2026-03 retrofit audit found in 6 of 22 entries — a single-audit figure registered at EMERGING (`S3-3`), not a calibrated rate.)
- Never skip the anti-hallucination checklist for AI-introduced citations
- Decision records are binding — check `decisions/` before proposing scope changes
- This repo contains both the framework AND papers that use it — changes to templates may affect active papers
- **Project state goes in `memory/` (in-repo, gitignored — see *What is intentionally not shipped*), not in any agent's user-level auto-memory.** Versions, session narratives, gotchas, priorities, handoffs, and any state tied to *this* repo's work belong in this repo's `memory/` directory. The principle applies most directly to agents with **cross-project user-level memory** — Claude Code (`~/.claude/projects/<slug>/memory/`), ChatGPT memory, Gemini Gems — where state can leak across projects without an explicit boundary. Agents with only project-level rules files (Cursor's `.cursorrules`, GitHub Copilot's `.github/copilot-instructions.md` <!-- placeholder -->, Continue's `.continue/config.json` <!-- placeholder -->) inherit the principle vacuously since they have no cross-project store to spill into. The Before You Start table above routes to in-repo memory; that's the canonical pickup path. Don't duplicate project state into both — drift starts as soon as you do. (Generalised to all agents in v2.1.0; narrowed in v2.2.0 to acknowledge which agents have the failure mode the principle prevents; original Claude-Code-only form added in v1.6.2.)
- **New state claims in `memory/` may embed a verification command in an HTML comment: `<!-- verify: cmd -->`.** `/curate` Step 0 sub-step 5 runs the command on read and flags drift (PASS / FAIL / ERROR / MANUAL). Convention applies to *new* claims going forward; no retrofit required for existing entries — opportunistic retrofit during routine edits is welcome but not gated. Adopted from agent-ready-projects v1.9.0 (self-verifying memory) + v1.10.0 (/curate audit hook) in this repo's v1.7.0.
- **A path that was never meant to resolve carries `<!-- placeholder -->` on the same line, immediately after it.** Instructional paths in `templates/`, other agents' config files (`.github/copilot-instructions.md`), deliberately-absent files (`BACKLOG.md`, which this repo does not have by design), and paths in another checkout. Without the marker they are re-triaged as broken on every `/audit-context` run, forever. Two properties decide whether a marker is correct, both learned by reading the checker rather than assuming: it is **span-scoped** — it covers the nearest backticked path *before* it, not the line — and a marker on a path that resolves **anywhere, including by filename suffix**, is reported as a stale marker. The second is why three template placeholders in `templates/CLAUDE.md` are deliberately left unmarked: they suffix-match this repo's own paper instances, so marking them is a finding and not marking them is a finding ([projects#56](https://github.com/ducroq/agent-ready-projects/issues/56)). An angle-bracket segment (`papers/<name>/backlog.md`) self-announces and needs no marker. Adopted from agent-ready-projects v1.23.0 in this repo's v2.6.1; the population was found by the `/audit-context` run that adoption was waiting on. **Caveat when reading a Step 4 report**: *as of companion v1.25.0* it has no doc-relative rung, so a correct relative link like `backlog.md` inside `papers/perspective/CLAUDE.md` is reported as a collision — 42 of 102 findings here were this ([projects#54](https://github.com/ducroq/agent-ready-projects/issues/54)). Check a finding against the referencing document's own directory before acting on it. The version anchor is deliberate: when the companion pin moves past v1.25.0, re-check whether this caveat still holds rather than trusting it.
- **A user-global skill silently shadows a project-local one of the same name.** It wins with no merge and no warning, so a local copy of a globally-installed skill is *inert* — it reads as authoritative while never being loaded, and is free to drift from the copy actually in use. Two consequences are normative here. **(1) Scope is decided per skill, not per repo:** `/curate` and `/audit-context` are generic and install user-globally (`~/.claude/skills/`); `/review-changes` and `/release` name this repo's own paths, tiers, and release process and must **never** be installed globally — one global copy would silently disable every other repo's version. **(2) Never leave an inert local copy.** If a global install exists, propose deleting the local one rather than reconciling it — **surface it, don't delete it yourself**; the deletion is a human call under the agent-write boundary above, and misjudging scope here destroys a project-local skill that was never shadowed. if you customized a local `/curate`, that customization was never in effect and the content belongs in this file instead. The question when choosing scope is not "is this generic today?" but "will any repo ever need its own version?" — installing globally forecloses per-repo variants. (Directory-scoped skills in a monorepo are namespaced, e.g. `papers/perspective:curate`, not shadowed.) Adopted from agent-ready-projects v1.15.0.
- **Agent-write boundary — agents may write the `memory/` layer autonomously (gotchas, session notes, work-item savepoints) but must not edit human-authored knowledge surfaces (`CLAUDE.md`, `README.md`, `templates/`, `decisions/`, `docs/`, `agents/`, `tools/`, `tests/`, `.claude/skills/`, paper manuscripts) or commit without in-session human approval.** This includes `/release`, which writes five of those surfaces before committing — its Step 6 carries the approval gate. `.claude/skills/` is on the list despite being gitignored: a defect there ships to every install derived from it, and the skill-scope constraint below contains a *delete* instruction, which is exactly the kind of destructive act that needs a human in the loop. A wrong edit to a template or decision record propagates silently to every future session and every adopter; a wrong edit to a memory file is cheap to correct at the next `/curate`. Decision rule: could a human reasonably need to disagree with this edit? If yes, it's human-authored — ask first. Adopted from agent-ready-projects v1.10.6.

## Architecture

```
agent-ready-papers/
├── .claude/skills/            <- Project-local slash commands (gitignored — not shipped)
│   ├── review-changes/        <- Diff-driven pre-commit review; project-local, never global
│   └── release/               <- Release cutter; project-local, never global; user-invoked only
│                                 (/curate, /audit-context, /update-drift are user-global — not here)
├── README.md                  <- The guide (public-facing)
├── CHANGELOG.md               <- Versioned release notes (v1.0.0 onwards)
├── CLAUDE.md                  <- This file (agent orientation)
├── LICENSE                    <- CC BY 4.0 (see DR-013)
├── CONTRIBUTING.md            <- Three-audience contribution guide
├── UPGRADING.md               <- Per-version adopter notes (pinned consumers)
├── Makefile                   <- Tooling targets: test / lint / format / coverage / check-dois (since v1.5.0)
├── pyproject.toml             <- Python tooling config: ruff + pytest, py3.10 target (since v1.5.0)
├── agents/                    <- Portable agent-role prompts (since v2.1.0; mirrors agent-ready-assessment)
│   ├── README.md              <- Directory purpose; line between role prompts and fill-in templates
│   ├── equation-checker.md    <- Mechanical equation & numerical verifier (was templates/equation-checker.md)
│   └── review-prompt.md       <- Peer-review simulator with multi-pass bias-escape (was templates/review-prompt.md)
├── templates/                 <- Fill-in templates for new paper projects
│   ├── CLAUDE.md              <- Paper project identity template
│   ├── claim-registry.md      <- Registry structure (P0/P1/P2, typed verification)
│   ├── vv-framework.md        <- Verification & validation framework
│   ├── writing-guide.md       <- Confidence tier to language mapping
│   ├── anti-hallucination.md  <- Step 0 + 6-step citation verification checklist
│   ├── glossary.md            <- Cross-domain terminology
│   ├── decision-record.md     <- DR template
│   ├── hypothesis-log.md      <- Provisional positions with future evidence (since v1.7.0)
│   ├── work-item.md           <- Multi-session work savepoint (from agent-ready-projects v1.11.0)
│   └── key-quotes.md          <- Reference quotes
├── decisions/                 <- Architecture decision records (DR-001 to DR-019)
├── extensions/                <- Staged, not-yet-accepted agent surfaces (DR-018 notation-checker)
├── literature/                <- Source registry
├── docs/                      <- Framework summary, threshold rationale, category-theory lens
│   ├── verification-hooks.md  <- Which checks to fire automatically after an edit (since v2.5.0)
│   └── work-items/            <- Multi-session work tracking (per `templates/work-item.md`; created on-demand)
├── tools/                     <- Registry tooling: coverage + DOI verification CLIs (since v1.5.0)
│   ├── coverage.py            <- Per-type sub-table parser; P0/P1/P2 + PROVOCATION tier coverage
│   ├── check_dois.py          <- DOI extractor + resolver (HEAD against doi.org, --offline mode)
│   └── README.md              <- Usage, exit codes, design constraints, known limits
├── tests/                     <- Shape-pin + edge-case tests for tools/ (since v1.5.0)
├── papers/
│   └── perspective/           <- Paper 1: "The Verification Gap" (active)
│       ├── CLAUDE.md          <- Paper-specific context (READ THIS for paper work)
│       ├── manuscript.tex     <- LaTeX source (~3,450 words)
│       ├── references.bib     <- 14 entries; the 12 carrying a DOI all resolve (2 cite ISBN/URL)
│       ├── vv/claims/         <- Claim registry (19 entries, 100% verified)
│       └── ...
├── vv/                        <- Framework self-application (since v2.2.0; public)
│   ├── cost-log.md            <- Operation cost log — framework operations on the framework
│   └── hypothesis-log.md      <- Public framework-level provisional positions (where load-bearing README prose depends on a falsifiable bet)
├── audits/                    <- RESERVED, absent today — external-doc audits if recreated (gitignored; may critique named authors)
└── memory/                    <- Session memory (gitignored — maintainer-local)
    ├── gotcha-log.md          <- Problem-fix archive (act above ~3,000 chars)
    ├── priorities.md          <- Near-term bucket only; structured + self-verifying (extracted 2026-08-08)
    ├── hypothesis-log.md      <- Maintainer-local intra-session bets (since v1.7.0; complement to vv/hypothesis-log.md which is public)
    └── ...
```

## What is intentionally not shipped

These paths are *not* in the public repo, for three different reasons — the distinction matters, because a row's reason tells you whether anything is there at all. **Most** exist in the maintainer's local clone and are gitignored. **One** lives outside this repo entirely (user-global skills), which is the row most likely to mislead an adopter reading the architecture diagram. **Two** — `audits/` and `docs/work-items/` — are conventions with a reserved path and no current contents: the policy is live, the directory is not. Each row says which case it is.

| Path | What it holds | For adopters |
|------|---------------|--------------|
| `.claude/skills/review-changes/` | `/review-changes` slash command (diff-driven pre-commit review). **Project-local, never global** — its risk tiers name this repo's own paths | Optional — the README and templates already document what the skill does. Build your own tier table; a copy of this one would review the wrong paths. Adopted from agent-ready-projects v1.12.0, gate from v1.16.0. |
| `.claude/skills/release/` | `/release` slash command (release cutter). **Project-local, never global** — it names this repo's CHANGELOG + UPGRADING process and its two version stamps | Optional — same. Adopted from agent-ready-projects v1.13.0. |
| *(not in this repo)* `~/.claude/skills/curate/`, `~/.claude/skills/audit-context/`, `~/.claude/skills/update-drift/` | `/curate`, `/audit-context` and `/update-drift` are installed **user-globally**, so they are absent from this repo entirely — not gitignored, just elsewhere. A local copy would be inert (see the skill-scope Hard Constraint) | Optional — install them globally from `agent-ready-projects`, which is their upstream. Do not copy them into your paper repo. |
| `docs/work-items/` | Multi-session work-item savepoints (per `templates/work-item.md`) | Optional — create per-project when work spans multiple sessions |
| `memory/MEMORY.md` | Maintainer's index of current project state and deferred items | Not needed — equivalent state for your paper lives in your paper's CLAUDE.md |
| `memory/priorities.md` | Maintainer's near-term priorities — structured table with a `<!-- verify: -->` asserting it parses and is non-empty | Not needed. If you build one, keep it to a **single velocity**: near-term only. The value came from splitting one bucket out of a prose blob, not from merging buckets into a tracker |
| `memory/gotcha-log.md` | Maintainer's problem-fix archive | Build your own per-project |
| `memory/dead-ends.md` | Maintainer's "don't retry" log | Build your own per-project |
| `memory/hypothesis-log.md` | Maintainer's intra-session framework bets (working positions) | Adopters maintain their own per `templates/hypothesis-log.md`; the *public* framework-level positions are at `vv/hypothesis-log.md`, which IS shipped |
| `audits/` | **Reserved path, no current contents** — the directory does not exist on the maintainer's clone today. The convention: audits applying the framework to *external / published* documents (dogfooding on third-party material). May critique named authors, so gitignored and private by default if recreated. The v2.0.0 scrub purged the earlier contents from git history; what remained on disk has since gone too | Not needed — run your own audits locally; un-ignore per-folder only with the author's awareness if you intend to publish |

The public framework — templates, DRs, README, CHANGELOG — is fully consumable without any of the above. Adopters maintain their own session state per the patterns in `templates/CLAUDE.md`, not by depending on the maintainer's `memory/`.

Listed here so the architecture diagram above is honest about what an adopter sees on `git clone` versus what the maintainer has on disk.

## Key Paths

| Path | What it is |
|------|-----------|
| `papers/perspective/CLAUDE.md` | Paper 1 project context — start here for paper work |
| `papers/perspective/manuscript.tex` | Paper 1 LaTeX source |
| `papers/perspective/vv/claims/claim_registry.md` | Paper 1 claim registry (19 entries) |
| `papers/perspective/backlog.md` | Paper 1 current tasks and priorities |
| `decisions/DR-004_registry-model-for-non-empirical-papers.md` | Most consequential DR — typed verification model |
| `decisions/DR-006_publication-roadmap.md` | Publication sequencing (Papers 1-3) |
| `literature/README.md` | Master source index (56 entries) |
| `templates/CLAUDE.md` | Template for new paper projects |
| `templates/work-item.md` | Multi-session work savepoint template (adopted from agent-ready-projects v1.11.0) |
| `docs/verification-hooks.md` | Which of this repo's checks are worth firing automatically after an edit (since v2.5.0) |
| `UPGRADING.md` | Per-version adopter action table — a required release artifact, not an optional extra |

## How to Work Here

```bash
# Compile Paper 1 (LaTeX)
cd papers/perspective && pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript

# Check claim registry coverage (since v1.5.0)
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md
# or: make coverage
# --strict makes the call fail if P0=100% / P1=90% / P2=70% thresholds are missed

# Verify DOIs in a registry resolve at doi.org (since v1.5.0)
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md
# or: make check-dois  (use --offline to skip network)

# Verify a citation (anti-hallucination)
# Follow the Step 0 + 6-step checklist in papers/perspective/anti-hallucination.md

# Run peer review simulation
# Use papers/perspective/review-prompt.md with the three-pass pattern (DR-011): Pass 1 intra-family small, Pass 2 intra-family large, Pass 3 cross-vendor (high-stakes only, with style filter)
```

## Cross-Repo Evidence

This project is a source project for [agentic-engineering](https://github.com/ducroq/agentic-engineering) — a proposition about what's new when engineers work with AI agents. When you discover evidence relevant to the four patterns (verification findings, context architecture lessons, reproduce-don't-assess examples, LLM behavioral properties), file an issue at `ducroq/agentic-engineering` with the pattern name, quantified results, and which claims it supports.
