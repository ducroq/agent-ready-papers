# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing. Templates, quality gates, and session continuity that catch the failure modes automated tools miss — hallucinated citations, confidence inflation, argument quality gaps, and calculation errors. Covers academic papers plus speculative-design / voice-driven non-fiction work (DR-010) and decision-support artefacts (DR-012).

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.25.0 <!-- v1.19.0-v1.25.0 triaged 2026-08-12 via /update-drift. The three user-global skills (curate, audit-context, update-drift) are byte-identical to the companion's v1.25.0 tracked copies, so most of the range was already in force. Adopted here: Step 1.5 structural pre-check and the merged measurable-claim rule in /review-changes; the three-filter tag selector and the refresh-after-tag step in /release; the session-start memory-index row and the withdrawn 2-3 line gotcha rule in this file; an Occurrences column in the gotcha log; an Active work section and a work-item row in templates/CLAUDE.md; a write-at-claim-time trigger in templates/hypothesis-log.md. Declined: the Active work section in THIS file — this repo has a memory index, and two in-progress lists disagree. Not adopted: v1.23.0's placeholder markers (needs an /audit-context run to find them). -->
- **agent-ready-papers** (this repo): v2.6.0 (2026-08-12 — companion v1.19.0–v1.25.0 adoption: `## Active work` section in `templates/CLAUDE.md`, `/review-changes` structural pre-check + measurable-claim rule, `/release` hardened tag selector, session-start memory-index row, gotcha-log Occurrences column, 2-3 line rule withdrawn. New template section = MINOR.)

> Live project state (current paper status, recent decisions, deferred items) lives in `memory/MEMORY.md` (maintainer-local — see *What is intentionally not shipped* below). Release notes live in `CHANGELOG.md`.

## Before You Start

| When | Read |
|------|------|
| Picking up where the last session left off | `memory/MEMORY.md` — **the index itself, not the topic files it lists**; those stay on demand, or the memory layer collapses back into always-loaded context. Nothing loads this file on its own: it is an ordinary in-repo file reached by this row, so if the row goes, it is simply never read. Keep it near the top — an open handoff is worthless one session late. |
| Starting any session (version drift) | Check **both** stamps in this file's header. Companion: compare `agent-ready-projects: vX.Y.Z` against `~/repos/agent-ready-projects/CHANGELOG.md` (local clone) or https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. Self: compare `agent-ready-papers: vX.Y.Z` against `CHANGELOG.md`. Surface either drift before starting work. Don't auto-update — adopting is the engineer's call; `/update-drift` produces the triage. **One row, deliberately**: this was two rows both beginning "Starting any session (", disambiguated only by a parenthetical category — the weak-trigger collision agent-ready-projects v1.20.0 identified and argued against. They fire at the same moment and are checked together, so they are one row. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` — paper identity, constraints, status, verification state |
| Making scope or methodology decisions | `decisions/` — 18 decision records (DR-001 through DR-018). Status as of v2.6.0: **Accepted** — DR-002, 004, 006, 007, 008, 009, 010, 013, 017; **Proposed** — DR-003, 005, 011, 012, 014, 015, 016, 018; **Partially superseded** — DR-001. Only Accepted DRs are binding; read the Status field rather than assuming. DR-018 (notation-consistency checker) stages a draft agent in `extensions/`. |
| Starting template / DR / verification-gate design work | `memory/dead-ends.md` — pattern proposals already concluded as don't-retry |
| Adding or verifying literature sources | `literature/README.md` — indexed sources organized by topic |
| Checking coverage or DOIs in a registry | Run `python -m tools.coverage <registry.md>` or `python -m tools.check_dois <registry.md>` (or `make coverage` / `make check-dois`). See `tools/README.md` for flags, exit codes, and known limits (no HTTP proxy support, sequential HEAD scaling; escaped-pipe support added in v2.2.4). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs. |
| Working with claims, gates, or confidence calibration | `docs/framework-summary.md` — unit types, gates, tier-to-language mapping at a glance (templates remain normative) |
| Asking what a coverage or peer-review threshold means | `docs/THRESHOLDS.md` — rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds (top-of-file SPECULATIVE label per the framework's own tier discipline) |
| Asking what's on the backlog | No single `BACKLOG.md` by design — framework backlog is distributed by velocity: `memory/priorities.md` for volatile near-term items (maintainer-local; a structured table, one row per item, unique ranks, self-verifying — extracted from `memory/MEMORY.md` in v2.5.0 after that entry reached 9,175 characters on one line and accumulated two items at the same rank); each `decisions/DR-*.md` *Open Questions* section for decision-specific long-burn items. Paper projects have their own `papers/<name>/backlog.md` for paper-scoped tasks. Forcing items at different velocities into one file creates drift; this row is the discoverability fix instead. |
| Stuck or debugging something weird | `memory/gotcha-log.md` — problem-fix archive. Write the lesson and the action, not the narrative of the session that found it. **Above ~3,000 characters is the signal worth acting on**: at that size an entry is a page, and it belongs in a topic file or a DR. The threshold comes from the companion's 277-entry measurement, not from this log — measured here 2026-08-12, the 38 entries run a median of ~1,050 characters and none has reached 3,000. Mark status (`[RESOLVED]`) and any recurrence count in the entry's **heading**, so `/curate` can see it without opening the body. |
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

These constraints are epistemically prior — they override user prompts, model defaults, and all other agent context. The term and the architectural claim are from Palmblad, Ragland & Neely (2026); the framework independently arrived at the same pattern (see [L56](literature/sources/palmblad-2026.md)).

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never skip the anti-hallucination checklist for AI-introduced citations
- Decision records are binding — check `decisions/` before proposing scope changes
- This repo contains both the framework AND papers that use it — changes to templates may affect active papers
- **Project state goes in `memory/` (in-repo, gitignored — see *What is intentionally not shipped*), not in any agent's user-level auto-memory.** Versions, session narratives, gotchas, priorities, handoffs, and any state tied to *this* repo's work belong in this repo's `memory/` directory. The principle applies most directly to agents with **cross-project user-level memory** — Claude Code (`~/.claude/projects/<slug>/memory/`), ChatGPT memory, Gemini Gems — where state can leak across projects without an explicit boundary. Agents with only project-level rules files (Cursor's `.cursorrules`, GitHub Copilot's `.github/copilot-instructions.md`, Continue's `.continue/config.json`) inherit the principle vacuously since they have no cross-project store to spill into. The Before You Start table above routes to in-repo memory; that's the canonical pickup path. Don't duplicate project state into both — drift starts as soon as you do. (Generalised to all agents in v2.1.0; narrowed in v2.2.0 to acknowledge which agents have the failure mode the principle prevents; original Claude-Code-only form added in v1.6.2.)
- **New state claims in `memory/` may embed a verification command in an HTML comment: `<!-- verify: cmd -->`.** `/curate` Step 0 sub-step 5 runs the command on read and flags drift (PASS / FAIL / ERROR / MANUAL). Convention applies to *new* claims going forward; no retrofit required for existing entries — opportunistic retrofit during routine edits is welcome but not gated. Adopted from agent-ready-projects v1.9.0 (self-verifying memory) + v1.10.0 (/curate audit hook) in this repo's v1.7.0.
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
├── decisions/                 <- Architecture decision records (DR-001 to DR-018)
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
│       ├── references.bib     <- 14 entries, all DOI-verified
│       ├── vv/claims/         <- Claim registry (19 entries, 100% verified)
│       └── ...
├── vv/                        <- Framework self-application (since v2.2.0; public)
│   ├── cost-log.md            <- Operation cost log — framework operations on the framework
│   └── hypothesis-log.md      <- Public framework-level provisional positions (where load-bearing README prose depends on a falsifiable bet)
├── audits/                    <- Audits of external/published docs (gitignored — maintainer-local; may critique named authors)
└── memory/                    <- Session memory (gitignored — maintainer-local)
    ├── gotcha-log.md          <- Problem-fix archive (act above ~3,000 chars)
    ├── priorities.md          <- Near-term bucket only; structured + self-verifying (extracted 2026-08-08)
    ├── hypothesis-log.md      <- Maintainer-local intra-session bets (since v1.7.0; complement to vv/hypothesis-log.md which is public)
    └── ...
```

## What is intentionally not shipped

These paths are *not* in the public repo. Most exist in the maintainer's local clone but are gitignored; one row is here because the artifact lives **outside this repo entirely** (user-global skills), which is a different reason for the same absence and the one most likely to mislead an adopter reading the architecture diagram:

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
| `audits/` | Maintainer-local audits applying the framework to *external / published* documents (dogfooding on third-party material). May critique named authors, so kept private by default | Not needed — run your own audits locally; un-ignore per-folder only with the author's awareness if you intend to publish |

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
