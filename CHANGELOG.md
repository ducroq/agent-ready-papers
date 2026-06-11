# Changelog

All notable changes to `agent-ready-papers`. Adopters can check their paper project's framework version against this log to see what has changed.

<!-- Maintainer release process:
     When promoting a `vX.Y.Z (candidate, unreleased)` block to a dated release:

     1. Tag the release commit:

         git tag vX.Y.Z <commit>
         git push --tags

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
     - PATCH — docs-only changes, clarifications, cross-reference adds

     Adopter-notes convention:
     - Every release entry below MUST include an "Adopter notes" or
       "Adopter action" subsection listing what action (if any) pinned
       consumers need to take. UPGRADING.md aggregates these per version
       for quick lookup. If an entry has no adopter action, say so explicitly
       ("No adopter action required.") rather than omitting the subsection.
-->

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