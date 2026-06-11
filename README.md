# Working With AI Agents: Academic & Technical Writing

Verification infrastructure for AI-augmented academic and structured non-fiction writing — templates, quality gates, and session continuity addressing the failure modes automated tools miss. Covers conventional academic papers plus speculative-design work (see [DR-010](decisions/DR-010_provocation-unit-type.md)).

Automated citation checkers (RefChecker, scite.ai) and model-level solutions (RAG, [grounded generation](docs/framework-summary.md#terminology-note-grounding--grounded)) address part of the problem. This guide operates at the **process level** — the workflow templates, decision records, and verification systems that sit between an AI agent and a submission-ready manuscript.

Companion to [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code).

**Status:** A working framework we use on our own papers. Broader empirical validation across other authors and domains is an open question — adopt it as a structured starting point, not as a tested method.

**Current release:** v2.2.3 (2026-06-11) — see [`CHANGELOG.md`](CHANGELOG.md). Pin your project with `agent-ready-papers: v2.2.3` in your CLAUDE.md and surface drift at session start.

## The Core Problem

AI agents are remarkably useful for academic writing — literature synthesis, argument structuring, statistical interpretation, formatting. But they have failure modes that are *different* from coding:

- **Hallucinated citations.** Agents invent plausible-sounding papers, authors, and DOIs. A citation that looks correct but doesn't exist can survive multiple review rounds undetected.
- **Confidence inflation.** Agents state speculative claims with the same certainty as verified facts. "Demonstrates" and "suggests" carry very different weight in academic writing — agents don't naturally distinguish.
- **Scope creep.** Without architectural constraints, agents expand arguments beyond what the evidence supports, add sections that dilute focus, and exceed page budgets.
- **Terminology drift.** In interdisciplinary work, the same word means different things across fields. Agents mix terminology freely unless constrained by a reference document.
- **Invisible verification gaps.** Agents produce fluent prose that *reads* like it's well-sourced. Without a systematic verification system, gaps in evidence are invisible until a reviewer finds them.

The fix isn't avoiding AI assistance. It's building **verification infrastructure** — systematic processes designed to catch these failure modes before submission.

## The Approach

The fix borrows a vocabulary from systems engineering: if claims are the paper's components, then sources are tests, coverage is measurable, and quality gates can prevent defective work from shipping.

<details>
<summary><strong>Mental model: the SE mapping</strong></summary>

| Engineered System | Paper |
|-------------------|-------|
| System requirements | Paper goals (what must the paper demonstrate?) |
| Components | Claims (individual statements of fact or data) |
| Unit tests | Claim verification (source exists, data supports claim) |
| Test coverage | % of claims with verified sources |
| SIL classification | Claim priority (P0 / P1 / P2) |
| Static analysis | Build checks (LaTeX compile, word count, DOI validation) |
| Integration tests | Argument flow (claims connect logically, no contradictions) |
| HIL testing | Expert review (co-author, domain expert) |
| Digital twin oracle | Reference documents (author guidelines, exemplar papers) |
| Stakeholder validation | Peer review simulation |
| Traceability matrix | Claim → Evidence → Audit trail |

Every concept on the right maps to a concrete artifact in the project — a template, a checklist, a registry entry. The rest of this guide explains each one.

</details>

## The Argument, Structurally

Stating the case in [Toulmin form](literature/sources/toulmin-1958.md) — *Claim / Grounds / Warrant / Qualifier / Rebuttal*, from Toulmin's *The Uses of Argument* (1958) — makes it inspectable rather than persuasive:

| Component | Statement |
|-----------|-----------|
| **Claim** | AI-augmented academic and structured non-fiction writing benefits from process-level verification infrastructure. |
| **Grounds** | The five failure modes in [The Core Problem](#the-core-problem) — hallucinated citations, confidence inflation, scope creep, terminology drift, invisible verification gaps. Each is observable in agent output today. |
| **Warrant** | Tool-level checkers (RefChecker, scite.ai) verify already-written citations; model-level techniques (RAG, [grounded generation](docs/framework-summary.md#terminology-note-grounding--grounded)) constrain what gets generated. Neither reaches the process layer where the failure modes originate — the templates, decision records, and registry discipline a writer brings *to* the session. |
| **Qualifier** | **EMERGING.** We use this framework on our own papers; broader empirical validation across other authors and domains is an open question. |
| **Rebuttal** | The framework is overhead with no return in the cases listed in *[When It Is Overkill](#when-it-is-overkill)* below — one-shot prose, throwaway code, internal notes, and domains with their own established compliance audit conventions. |

This Toulmin block decomposes the **argument** the framework rests on; R-1 in [*This README, registered*](#this-readme-registered) below states the **proposition** the argument supports — registered with its own boundary conditions, per the framework's [Whetten checklist](literature/sources/whetten-1989.md) (*Constructs / Premises / Reasoning / Boundary conditions / Alternatives engaged*, from Whetten's *What Constitutes a Theoretical Contribution?*, AMR 1989). The two views coexist by design: argument verifies the reasoning chain; proposition verifies the recommendation; same case, two checklists. Six further entries (R-2…R-7) cover supporting CLAIMs / ARGUMENTs / PROPOSITIONs from the rest of this file.

**Dynamic counter to the Warrant.** A reasonable objection: "tool-level + model-level techniques are improving fast; RAG with citation-grounded generation plus reasoning-step verification could close most of the gap as capability rises." The Warrant above claims a **structural** distinction (process layer is the locus of the failure modes), not a **static** one (today's tools don't reach it). The structural claim is empirically open — registered as a falsifiable position in [`vv/hypothesis-log.md`](vv/hypothesis-log.md) with a Method (apply the framework's apparatus to a frontier-model-RAG-produced manuscript and count residual process-level findings) and a Revisit trigger (frontier-model RAG pipeline with reasoning-step verification becomes available, applied to a ≥5,000-word manuscript with ≥10 citations). Reading this and disagreeing? File an issue or contact the maintainer; "the position fails if residual process-level findings drop below 3" is concrete enough to test.

## When This Framework Is Worth The Overhead

Each test can be answered yes / no for your specific project — they're meant as boundary conditions, not aspirational filters:

- **Hallucination cost exceeds review cost.** A hallucinated citation surviving into your output would cost more than an hour of your time to retract or correct downstream.
- **Context cannot fit in a single session.** The work spans multiple sessions (a paper, a grant, a long-form decision) — no one conversation holds it all, so handoff state has to live in files.
- **At least one claim is load-bearing.** You have an argument or proposition the reader will scrutinise — being wrong about it would cost a co-author conversation or a reviewer round.
- **Confidence language is read as a signal.** "Demonstrates" vs. "suggests" will be parsed by your reader (reviewer, regulator, decision-maker) as a calibrated weighting, not interchangeable hedging.

## When It Is Overkill

Each test is similarly yes / no — if the description fits, the framework is overhead with no return:

- **No citation surface.** One-shot prose that introduces no external references — no hallucination possible.
- **Correctness verified by execution.** Throwaway code or scripts — running them is the verification.
- **Audience of one.** Internal scratch notes that only you will read.
- **Established audit conventions already cover it.** Domains with their own conventions (FDA 21 CFR 820, IEC 62304, ISO 17025, GDPR DPIA, regulated clinical trial reporting) — use those instead.

## Common Questions

**Doesn't this add overhead?** Yes — roughly 10 minutes of setup plus ongoing claim logging as you draft. The trade is overhead against the cost of being wrong. If a hallucinated citation or a confidence-inflated claim could survive to submission, the overhead pays back the first time it catches one.

**What if my paper has only a few claims?** Then the registry is short. The point is verification discipline, not registry size. Even 5–10 entries benefit from typed verification — type-checking each entry forces you to articulate what kind of statement it is and what would falsify it.

**How is this different from a reference manager (Zotero, Mendeley)?** Reference managers track *citations*; this tracks the *structure of your argument*. A claim has a confidence tier; an argument has a warrant; a proposition has boundary conditions. Reference managers don't model those, and they don't enforce confidence-to-language calibration.

**Can I use this without an AI agent?** Yes. The framework was designed for AI-augmented writing — that's where hallucination and confidence inflation are most acute — but registry discipline, decision records, and quality gates work fine for any structured non-fiction. The anti-hallucination checklist is most useful when an agent is introducing claims; the rest applies regardless.

**Has this been peer-reviewed?** Not yet. We use it on our own work; Paper 1 (in this repo) is the perspective article that argues for the gap this framework addresses. Adopt as a structured starting point, not as a tested method.

## Quickstart

Adopt the framework on a new paper in five steps (~10 minutes to set up):

1. **Bootstrap session continuity.** Copy [`templates/CLAUDE.md`](templates/CLAUDE.md) into your paper project as `CLAUDE.md`. Fill in the paper identity, target journal, deadline.
2. **Copy the minimum-viable adoption files.** [`templates/claim-registry.md`](templates/claim-registry.md), [`templates/anti-hallucination.md`](templates/anti-hallucination.md), and [`templates/writing-guide.md`](templates/writing-guide.md). These three plus CLAUDE.md are enough to start.
3. **Register your first claims.** In `claim-registry.md`, list 5–10 of your paper's load-bearing factual statements. Assign each a priority (P0 / P1 / P2), confidence tier (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE), and a source.
4. **Verify each citation.** Run the Step 0 + 6-step checklist in `anti-hallucination.md` on every AI-introduced citation. Step 0 (Scholar + DOI) catches fabrications in seconds.
5. **Run one review pass.** Before sharing the draft, ask a *fresh session* of a smaller model in the same family (e.g., Haiku, GPT-4o-mini, Gemini-Flash) to review the manuscript against your review prompt. A fresh session escapes the sunk-cost bias of the session that wrote the draft. See [`agents/review-prompt.md`](agents/review-prompt.md) for the prompt template and [DR-011](decisions/DR-011_multi-model-review-pattern.md) for the full three-pass pattern (intra-family small → intra-family large → cross-vendor).

### Three tiers of adoption

| Tier | Files | When |
|------|-------|------|
| **Required for first use** | `CLAUDE.md`, `claim-registry.md`, `anti-hallucination.md`, `writing-guide.md` | From day one |
| **Useful once the paper grows** | `agents/review-prompt.md`, `agents/equation-checker.md`, `templates/decision-record.md`, `templates/glossary.md`, `templates/vv-framework.md`, `templates/cost-log.md`, `templates/hypothesis-log.md` | After ~20 registry entries, or once you hit a decision / cost-tracking / pre-registered bet worth recording |
| **Reference / background only** | `key-quotes.md` | When you want context, not before |

### Driving it with your agent

The five steps above describe *what* gets set up. In practice you delegate four of the five steps to the agent — the framework is for AI-augmented writing, not for the human applying a checklist on their own. (Step 3's *initial selection* of which 5–10 claims are load-bearing remains a human-judgement call the prompts don't claim; the agent registers what you point at, doesn't decide what's load-bearing.) Four common operations as one-shot prompts you can copy and adapt; replace `<framework>` with the path to your `agent-ready-papers` checkout and `<paper>` with your paper's directory.

**Bootstrap a new paper project** (once, at project start):

> Start a paper project using the agent-ready-papers framework at `<framework>` (currently v2.1.2). Topic: [X]. Target journal: [Y]. Deadline: [Z]. Do this: (1) Create `papers/<name>/`. (2) Copy `<framework>/templates/CLAUDE.md`, `claim-registry.md`, `anti-hallucination.md`, `writing-guide.md` into it. (3) Fill `CLAUDE.md` with the paper identity. (4) Initialise the registry with empty per-type sub-tables for each anticipated section. (5) Commit. From now on, read `papers/<name>/CLAUDE.md` at the start of every session.

**Register claims as I draft** (background companion mode for every writing session):

> As I draft, when I make a factual claim, argument, or proposition, register it in `<paper>/vv/claims/claim_registry.md` using the per-type sub-tables and the priority / tier conventions in CLAUDE.md. Don't ask permission for routine entries — just register them and report a running coverage summary at section end. Flag anything you're unsure about: CLAIMs that look like ARGUMENTs, PROPOSITIONs missing boundary conditions, SPECULATIVE claims phrased as ESTABLISHED. When I introduce a citation, run Step 0 of `<framework>/templates/anti-hallucination.md` immediately and tell me if it's verifiable or likely fabricated.

**Verify a single citation** (one-shot lookup):

> Walk the Step 0 + 6-step anti-hallucination checklist in `<framework>/templates/anti-hallucination.md` for [citation]. Re-read the checklist from the source file at this invocation — don't rely on memorised steps from a prior session. For each step report PASS / FAIL / NEEDS-CONTENT-CHECK with the evidence (Scholar result, DOI resolution, publisher URL, abstract excerpt, page number). If Step 0 fails, stop and tell me — the citation is likely fabricated.

**Run a peer-review pass** (in a *fresh session of a different model* — see [DR-011](decisions/DR-011_multi-model-review-pattern.md)):

> You are a peer reviewer. Read `<framework>/agents/review-prompt.md` and apply it as your system prompt to `<paper>/manuscript.tex`. This is Pass [1 intra-family small / 2 intra-family large / 3 cross-vendor]; the style/voice filter is [target journal's style guide / project's voice rules]. Use the scoring rubric in the role prompt and report scored assessments per dimension plus load-bearing findings. Do not propose rewrites — only flag findings I can act on.

For non-Claude-Code agents (GitHub Copilot CLI, Cursor, Continue, web chat), see [`docs/non-claude-setup.md`](docs/non-claude-setup.md) for the universal four-step pattern and tool-specific entry points — the prompts above work as-is across vendors.

The full template index is in the [Templates](#templates) section near the bottom.

---

> **From here down: implementation detail.** The sections below explain how each piece works for adopters actually setting up.

## Verification Registry: The Foundation

The registry tracks three unit types:

| Type | What it is | Where it appears | Verification |
|------|-----------|-----------------|--------------|
| **CLAIM** (default) | Factual statement with a source | All sections | Does the source exist and say this? |
| **ARGUMENT** | Reasoning chain combining evidence + inference | Discussion, Conclusion | Warrant valid? Evidence sufficient? Counter-arguments addressed? |
| **PROPOSITION** | Novel recommendation or contribution | Conclusion, Recommendations | Premises verified? Reasoning valid? Boundaries stated? |

Most entries are CLAIMs. ARGUMENTs and PROPOSITIONs appear in Discussion and Conclusion sections — the parts reviewers scrutinize most. All three share the same priority, confidence, and language calibration system.

For papers with quantitative content (equations, derived values, numerical tables), a fourth verification procedure applies:

| Type | What it is | Where it appears | Verification |
|------|-----------|-----------------|--------------|
| **CALCULATION** | Derived numerical value from a stated formula | Methods, Results, technical appendices | Does the stated result follow from stated inputs? |

Calculation verification uses **mechanical reproduction** — substituting values into formulas and computing step by step — rather than plausibility assessment. The rationale: a formula with correct units, reasonable magnitude, and coherent surrounding prose will pass plausibility review even when the arithmetic is wrong. Reproducing the calculation is designed to surface what assessment misses. See [DR-009](decisions/DR-009_calculation-verification.md) for the verification procedure.

For speculative-design / design-fiction / diegetic-prototype work, an opt-in fifth unit type applies:

| Type | What it is | Where it appears | Verification |
|------|-----------|-----------------|--------------|
| **PROVOCATION** | Designed artefact making no truth claim — diegetic prototype, reflexive Ask, paradox box, fictional category | Speculative-design works only | Plausible? Generative? Reflexive marker present? Ethically held? (Auger 2013) |

PROVOCATIONs use a separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) measuring quality of speculation rather than strength of evidence, with required prose markers binding for each tier. See [DR-010](decisions/DR-010_provocation-unit-type.md) for the activation rationale.

### Priority (what breaks if this is wrong?)

| Priority | Meaning | Coverage Target |
|----------|---------|-----------------|
| **P0** | Core argument — paper fails without it | 100% verified |
| **P1** | Supporting — strengthens argument | 90% verified |
| **P2** | Context — nice to have | 70% verified |

### Confidence (how sure are we?)

| Tier | Assign when... |
|------|---------------|
| **ESTABLISHED** | Multiple independent sources confirm; no credible dispute; textbook-level |
| **SUPPORTED** | At least 2–3 peer-reviewed sources agree; some open questions remain |
| **EMERGING** | 1–2 sources, or preliminary/pilot data; plausible but not yet replicated |
| **SPECULATIVE** | Logical inference, hypothesis, single non-peer-reviewed source, or extrapolation |

### Source tier (how trustworthy is the evidence?)

| Tier | Type | Weight |
|------|------|--------|
| A | Peer-reviewed primary research | 1.0 |
| B | Peer-reviewed review article | 0.8 |
| C | Textbook / established reference | 0.9 |
| D | Guidelines / industry standards | 0.7 |
| E | Own unpublished work (under review) | 0.6 |
| F | Logical inference | 0.2 |

The **registry** tracks all of this in one place — a living table of every claim, argument, and proposition with its type, priority, confidence tier, source, and verification status. See [`templates/claim-registry.md`](templates/claim-registry.md).

### One row, concretely

A populated CLAIM entry looks like this:

| ID | Type | Priority | Confidence | Source | Source Tier | Status |
|----|------|----------|------------|--------|-------------|--------|
| S1-1 | CLAIM | P0 | SUPPORTED | Mugaanyi et al. 2024 (JMIR, DOI: 10.2196/52935): 62–89% DOI fabrication rates across disciplines | A | [x] |

The same row for an ARGUMENT carries additional fields (Grounds / Warrant / Rebuttal); a PROPOSITION carries Constructs / Relationship / Premises / Reasoning / Boundary conditions / Alternatives engaged. The per-type sub-table layout in [`templates/claim-registry.md`](templates/claim-registry.md) makes the type-specific fields explicit.

### Cross-reference rules

- No claim accepted on a single non-textbook source
- Contradictory sources must be acknowledged
- Claims >10 years old need a recency check

## Confidence-to-Language Mapping

This is the bridge between verification and writing. The confidence tier determines what language is appropriate:

| Tier | Language |
|------|----------|
| ESTABLISHED | "demonstrates", "shows", "confirms", "established" |
| SUPPORTED | "indicates", "supports", "evidence suggests" |
| EMERGING | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | "warrants investigation", "remains unclear", "we hypothesize" |

Without this mapping, agents default to confident language regardless of tier. A SPECULATIVE claim stated as "demonstrates" is a credibility risk that reviewers will catch. The writing guide template maps every claim to its section, confidence tier, and appropriate language. See [`templates/writing-guide.md`](templates/writing-guide.md).

**PROVOCATIONs use a separate axis.** When the registry contains PROVOCATION entries, the table above does not apply to them — they take GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL with their own required prose markers (see [DR-010](decisions/DR-010_provocation-unit-type.md) and [`templates/claim-registry.md`](templates/claim-registry.md) → "PROVOCATION Confidence — Separate Axis").

**Own work under review** requires special framing: "we observed" (not "it was found"), with explicit status ("under review at [journal name]"). Don't let agents present under-review work as established.

## Anti-Hallucination Checklist

Before accepting any literature claim from an AI agent:

0. **Quick web verification** — search Google Scholar + resolve DOI; if neither confirms the source, it's high risk
1. **Confirm the canonical citation** — pin down exact DOI, title, year before checking content
2. **Is the author real?** (institutional affiliation page)
3. **Is the journal real?** (publisher website, not a predatory clone)
4. **Does the claim match the paper's scope?** (abstract check)
5. **Is the exact location cited?** (page / table / figure number)
6. **Have I read the relevant section?** (not just the abstract)

This is non-negotiable. Run it for every new citation the agent introduces. Agents can and will invent plausible-sounding papers with real-sounding author names. Step 0 catches fabrications in seconds; the full checklist takes 2 minutes per citation. Catching a hallucinated citation in review takes 2 weeks.

**Automated companion (since v1.5.0):** for whole-registry verification, `python -m tools.check_dois <registry.md>` extracts every DOI from your claim registry, HEADs against `doi.org`, and reports the unresolved ones. It does Step 0 at scale — useful before phase gates and in CI. Pair it with the manual checklist for the content-level steps (4, 5, 6) where machine verification cannot substitute for reading the source. See [Tools](#tools) below.

**Inverse hallucination — Step Z.** For projects with PROVOCATION entries (speculative-design, design-fiction, diegetic-prototype work), an agent can present a *speculation* as if it had a citable source — the inverse of standard fabrication. Steps 0–6 will fail to catch this because no source exists to verify. Step Z reclassifies such entries as PROVOCATIONs rather than chasing missing sources. See [`templates/anti-hallucination.md`](templates/anti-hallucination.md) → Step Z and [DR-010](decisions/DR-010_provocation-unit-type.md).

See [`templates/anti-hallucination.md`](templates/anti-hallucination.md) for the full checklist with worked examples.

## Architecture Blueprints

Before writing begins, define the paper's structure with **page budgets**:

```
Section                         Pages
────────────────────────────────────────
Title, Authors, Abstract        0.50
Introduction                    0.50
Materials and Methods           1.50
Results                         2.00
Discussion                      1.50
Limitations & Conclusion        0.80
References                      1.00
────────────────────────────────────────
TOTAL                           7.80 / 8.00
```

Each section gets:
- A paragraph-level outline (what each paragraph argues)
- The claims it uses (by registry ID)
- What was cut and where it went (supplement, future work, or deleted)
- Explicit "content moved" and "content cut" annotations

This constrains scope creep — a common failure mode when agents draft sections. Without a page budget, an introduction that should be half a page becomes two pages of background the reader doesn't need. The blueprint is a specification; the writing is implementation.

## Peer Review Simulation

Before submission, run the paper through a structured AI review that simulates the target journal's standards. This isn't a substitute for real peer review — it's a pre-flight check that catches the obvious problems.

A good review prompt evaluates along multiple dimensions:

| Dimension | What it checks |
|-----------|---------------|
| Scientific rigor | Statistics, experimental design, claims vs. evidence |
| Terminology compliance | Domain-specific standards (VIM, GUM, IEEE, APA) |
| Structure and clarity | Logical flow, balance, redundancy |
| Journal style | Formatting, tone, prohibited patterns |
| Completeness | Self-contained narrative, supplement references |
| Technical accuracy | Statistical tests match design, citations correct |

The review produces **scored assessments** — not just prose feedback. A weighted rubric (e.g., contribution 15%, methodology 15%, uncertainty quantification 15%, clarity 10%) gives you a concrete quality signal. If the simulated review scores below your threshold (e.g., 3.5/5.0), address the weaknesses before submitting.

**Critical**: Never review in the building session — an agent reviewing its own work has sunk-cost bias in its context and is unlikely to catch its own mistakes. For the strongest version, use the three-pass pattern that escapes distinct biases at each pass: Pass 1 (intra-family small, sunk-cost-from-session escape, every publish), Pass 2 (intra-family large, different review character, every major revision), Pass 3 (cross-vendor, training/stylistic-prior escape, high-stakes only with mandatory style filter). See [`decisions/DR-011_multi-model-review-pattern.md`](decisions/DR-011_multi-model-review-pattern.md) and Step 7 in [`templates/anti-hallucination.md`](templates/anti-hallucination.md).

See [`agents/review-prompt.md`](agents/review-prompt.md) for a structured review prompt template.

## Terminology References

For interdisciplinary papers, create a **glossary** that serves as the single source of truth for terminology:

- Group terms by the domain they come from
- Include plain-language equivalents alongside formal definitions
- Note where terms overlap or conflict across fields
- Reference the standard each term comes from (VIM, GUM, ISO, APA, etc.)

This guards against terminology drift — for instance, agents using "accuracy" when they mean "trueness" (a VIM distinction), or using a domain-specific term with its colloquial meaning where the formal meaning is required. Point the agent to the glossary in your project file (CLAUDE.md) so it's consulted before writing.

See [`templates/glossary.md`](templates/glossary.md).

## Quality Gates

Each gate must pass before proceeding.

> The numerical thresholds in Gate 2 (100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage) and Gate 3 (≥3.5/5.0 simulated peer review) are **SPECULATIVE-tier heuristics** chosen on internal reasoning, not on a calibration dataset. See [`docs/THRESHOLDS.md`](docs/THRESHOLDS.md) for the rationale per threshold and what would harden them.

### Gate 1: Draft Complete
- [ ] All sections drafted to page budget
- [ ] Claim registry populated with all factual statements
- [ ] P0 claims identified and prioritized

### Gate 2: Verification Complete
- [ ] P0 claims 100% verified
- [ ] P1 claims 90% verified
- [ ] Overall coverage ≥85%
- [ ] Coverage checked by section type (Factual sections vs Discussion/Conclusion) — Discussion sections typically have lower coverage and need ARGUMENTs/PROPOSITIONs, not just CLAIMs
- [ ] Entry types re-checked (see `templates/claim-registry.md` — Detecting Mistyped Entries)
- [ ] Coverage report generated (timestamped snapshot for co-author review)
- [ ] Static checks pass (LaTeX compiles, BibTeX valid, DOIs resolve)
- [ ] Anti-hallucination checklist run on all AI-introduced citations

### Gate 2.5: Internal Consistency
- [ ] All statistics in appendices cross-checked against main text values
- [ ] Date citations consistent (same year for same source throughout)
- [ ] Numerical values in tables match claims in prose
- [ ] No data present only in appendix without main text reference (or vice versa)

These are manual cross-checks not covered by the automated static checks in Gate 2.

### Gate 2.6: Reflexivity *(conditional — only when PROVOCATIONs are present)*

For projects with PROVOCATION entries (see [DR-010](decisions/DR-010_provocation-unit-type.md)). Walk every PROVOCATION; confirm the required prose marker for its tier (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) is visible in the manuscript itself, at every load-bearing moment — not only in the registry. Without the marker, authoritative-toned speculation can be misread as a claim. Entries failing this audit are rewritten or downgraded to EMERGING CLAIM with additional sources.

### Gate 2.7: Ethical Review *(conditional — only for contested topics)*

For projects engaging actively contested ethical territory. No real-world group is pathologised in the author's voice; harm consideration is documented in a DR; treatment is symmetric across the contested traditions in the work; reviewer composition matches those traditions; project-specific operational rules from the contested-topic DR are applied chapter by chapter.

### Gate 2.8: Voice Consistency *(conditional — only for voice-driven work)*

For voice-driven work where the manuscript's register is part of the contribution. The project has a voice manifest binding for every chapter; no drift into excluded modes (academic hedging, snark, righteousness); a read-aloud test passes; drift is logged and resolved before Gate 3.

### Gate 3: Review Complete
- [ ] Simulated peer review scored ≥3.5/5.0
- [ ] Co-author signoff
- [ ] Language matches confidence levels (writing guide applied)

### Gate 4: Submission Ready
- [ ] All previous gates passed
- [ ] Journal requirements met (word count, format, data availability)
- [ ] Final proofread complete
- [ ] Author agreement signed

## Decision Records

Academic papers involve many consequential choices — scope decisions, methodology pivots, journal selection, what to include vs. exclude. Document these as lightweight decision records:

```markdown
# DR-001: Restrict scope to single mechanism (exclude broader survey)

## Context
The paper could cover one mechanism in depth or survey three related
mechanisms at a shallower level. Page budget forces a choice.

## Decision
Single-mechanism deep treatment; the other two mechanisms appear only
as related-work pointers.

## Rationale
- The single mechanism has the strongest empirical anchor in the literature.
- A survey at the available page budget would underspecify each mechanism,
  weakening the contribution.
- Deep treatment lets us defend boundary conditions explicitly.

## Revisit If
- Page budget increases (journal offers extended format).
- Reviewer feedback specifically requests the survey framing.
- A new result makes one of the excluded mechanisms load-bearing.
```

Without DRs, agents repeatedly re-propose excluded approaches across sessions. "Should we widen the scope to all three mechanisms?" gets answered once in DR-001, not every session.

See [`templates/decision-record.md`](templates/decision-record.md).

## Workflow Phases

A structured workflow prevents the common failure of jumping straight to writing. Phases group *what you're doing*; gates group *what must be true before moving on*. The mapping:

| Phase | What you're doing | Exits at |
|-------|-------------------|----------|
| 0 — Problem Framing | Research questions, target audience, initial decisions (DR-000, DR-001) | Paper identity set |
| 1 — Requirements | Goals, success criteria, key claims, evidence mapping | Claims listed in registry |
| 2 — Literature Audit | Find source → verify → extract citation → tag confidence | Registry coverage acceptable |
| 3 — Writing | Architecture blueprint + writing guide + anti-hallucination checklist | **Gate 1** (Draft Complete) |
| 4 — Validation | Simulated peer review, co-author review, full coverage report | **Gate 2** + **2.5** + **3** (Review Complete) |
| 5 — Submission | Journal requirements, final citation check, data availability | **Gate 4** (Submission Ready) |

Sessions within a phase span days to months. Session continuity rides on `CLAUDE.md` as the handoff document: read it at the start, update it at the end, commit everything. No reliance on conversation memory — all context recoverable from committed files. See [`templates/CLAUDE.md`](templates/CLAUDE.md) for the structure.

## What Doesn't Work

Common anti-patterns, in priority order. Each links back to the section that explains the fix:

- **Trusting agent citations without verification.** Agents hallucinate citations routinely. Every citation goes through the [Anti-Hallucination Checklist](#anti-hallucination-checklist) — non-negotiable.
- **Writing before the claim registry.** Prose written without a registry will need to be rewritten. The [Verification Registry](#verification-registry-the-foundation) forces you to name what you're claiming before you invest in sentences.
- **Reviewing in the building session.** An agent that spent an hour helping write Section 3 carries sunk-cost bias into its own review. Use the three-pass pattern in [Peer Review Simulation](#peer-review-simulation) — at minimum, a fresh session of the same model.
- **Skipping the architecture blueprint.** Without page budgets, agents expand every section. See [Architecture Blueprints](#architecture-blueprints).
- **Mixing terminology across domains.** In interdisciplinary work, freely-used terms confuse every reviewer. See [Terminology References](#terminology-references).
- **Reviewing equations for "soundness" instead of reproducing them.** Plausibility assessment misses arithmetic errors that mechanical reproduction catches. See [`agents/equation-checker.md`](agents/equation-checker.md).
- **Confident language for weak claims.** "Our results demonstrate" for a SPECULATIVE inference is a credibility risk. See [Confidence-to-Language Mapping](#confidence-to-language-mapping).
- **Skipping verification for informal technical communication.** The same error classes (unit confusion, property overestimates, wrong formulas) appear in WhatsApp messages, emails, and Slack discussions with quantitative claims — without the review trigger a paper would attract. If numbers or technical terminology go to a stakeholder, run the relevant checks before sending.

## Measuring Success

You know the system is working when:
- The claim registry hits its per-tier coverage targets before submission (P0 / P1 / P2; current targets in Gate 2 — see [`docs/THRESHOLDS.md`](docs/THRESHOLDS.md) for why)
- The simulated peer review clears the project's submission threshold
- No hallucinated citations survive to co-author review
- Language consistently matches evidence strength
- Agents don't re-propose excluded scope (because DRs exist)
- Sessions resume productively without re-explaining context

You know it's failing when:
- You find unverified claims in "final" drafts
- Co-authors catch hallucinated references
- The paper exceeds page limits despite having a blueprint
- Agents use "demonstrates" for speculative claims
- You're re-explaining the paper's scope every session
- Terminology is inconsistent across sections

The specific numbers behind the success signals (85% overall coverage, 100% P0, 3.5/5.0 peer-review) are SPECULATIVE-tier heuristics — defensible defaults, not calibrated constants. Adjust them per project as you accrue evidence.

## Templates

Fill-in templates in [`templates/`](templates/) — the files you copy, populate, and keep iterating on as the paper grows. (For single-shot agent system prompts, see [Agent-Role Prompts](#agent-role-prompts) below.)

- **[`CLAUDE.md`](templates/CLAUDE.md)** — Paper project identity, session continuity, Before You Start table
- **[`claim-registry.md`](templates/claim-registry.md)** — Claim tracking with priority, confidence, source tiers
- **[`vv-framework.md`](templates/vv-framework.md)** — Verification and validation framework
- **[`writing-guide.md`](templates/writing-guide.md)** — Confidence-to-language mapping, section-claim assignment
- **[`decision-record.md`](templates/decision-record.md)** — Lightweight ADR for scope and methodology decisions
- **[`anti-hallucination.md`](templates/anti-hallucination.md)** — Citation verification checklist
- **[`glossary.md`](templates/glossary.md)** — Cross-domain terminology reference
- **[`cost-log.md`](templates/cost-log.md)** — Per-operation token-cost log; copy to your paper's `vv/cost-log.md` (since v1.6.0)
- **[`hypothesis-log.md`](templates/hypothesis-log.md)** — Provisional positions whose evidence lives in the future (`Position` / `Method` / `Revisit trigger` / `Review by`); resolves to closed or promoted to DR (since v1.7.0; adopted from agent-ready-projects v1.10.0)

Copy what you need, delete the comments, fill in your specifics.

## Agent-Role Prompts

Portable agent-role prompts in [`agents/`](agents/) — copy each as a system prompt into any agent (Claude Code, GitHub Copilot CLI, Cursor, ChatGPT, Gemini) and pair with the artefact to be processed. Vendor-neutral by design.

| Prompt | Role | When to run |
|--------|------|-------------|
| [`equation-checker.md`](agents/equation-checker.md) | Mechanical equation & numerical verifier — substitute values, compute, flag discrepancies (not plausibility review) | When any equation or derived value is load-bearing; paired with the source equations for cross-reference |
| [`review-prompt.md`](agents/review-prompt.md) | Peer-review simulator with multi-pass bias-escape semantics ([DR-011](decisions/DR-011_multi-model-review-pattern.md)) | Before submission; once per pass — Pass 1 intra-family small, Pass 2 intra-family large, Pass 3 cross-vendor (high-stakes only, with style/voice filter) |

See [`agents/README.md`](agents/README.md) for the directory's purpose and the line between agent-role prompts (here) and fill-in templates (in [`templates/`](templates/)). Convention mirrored from [agent-ready-assessment](https://github.com/ducroq/agent-ready-assessment)'s `agents/` directory; new here in v2.1.0. For practical setup with a non-Claude-Code agent (Copilot CLI, Cursor, Continue, web chat), see [`docs/non-claude-setup.md`](docs/non-claude-setup.md).

## Tools

Optional Python CLIs in [`tools/`](tools/) — stdlib only, deterministic, CI-friendly. Pair with the manual workflows above; replace nothing.

| Tool | Purpose | When to run |
|------|---------|-------------|
| [`coverage.py`](tools/coverage.py) | Parse a `claim_registry.md`; report P0/P1/P2 coverage by unit type | Before phase gates; in CI with `--strict` to fail the build on missed thresholds |
| [`check_dois.py`](tools/check_dois.py) | Extract DOIs; HEAD against `doi.org`; report unresolved | After any AI-assisted citation introduction; in CI; pair with the [Anti-Hallucination Checklist](#anti-hallucination-checklist) Step 0 |

Invoke as `python -m tools.coverage <registry.md>` or via Makefile (`make coverage` / `make check-dois`) from the repo root. Known limits (no HTTPS proxy support, sequential HEAD scaling, no escaped-pipe support in cells) are documented in [`tools/README.md`](tools/README.md).

### Self-applied cost data (N=2, code-tooling scale)

We ran the DR-011 two-pass review on this repo's own `tools/` code (`coverage.py` + `check_dois.py`, ~620 LOC) and logged the token cost. Treat as a back-of-envelope reference, not as a published benchmark — it covers one type of artefact (Python code) at one scale, reviewed within one model family (Claude):

| Operation | N | Mean total tokens | Findings that would have shipped broken |
|-----------|---|-------------------|------------------------------------------|
| Pass 1 (Haiku) | 2 | 36,812 | 0 / 2 rounds |
| Pass 2 (Opus) | 2 | 52,540 (~1.4× Pass 1) | 2 / 2 rounds |

Per-paper cost logging via the [`cost-log.md`](templates/cost-log.md) template. See [DR-011 Open Questions](decisions/DR-011_multi-model-review-pattern.md) for what's still unmeasured (paper-scale prose, cross-family generality, Pass 3 yield).

## Paper Projects

Papers written using this framework live in [`papers/`](papers/). Each paper project has its own CLAUDE.md, claim registry, writing guide, and verification infrastructure — instantiated from the templates above.

| Paper | Directory | Status | Target |
|-------|-----------|--------|--------|
| Paper 1: The Verification Gap (Perspective) | [`papers/perspective/`](papers/perspective/) | Phase 3 — Draft complete, Gate 3 (co-author review) | Learned Publishing |
| Paper 2: Verification Infrastructure (DSR) | — | Not yet started | JAIS |
| Paper 3: SE-Inspired Verification Pipeline | — | Not yet started (equation-checker is proof of concept) | TBD |

See [`decisions/DR-006_publication-roadmap.md`](decisions/DR-006_publication-roadmap.md) for the publication strategy and sequencing.

## This README, registered

Applying the framework to its own home document. The seven entries below are the README's load-bearing claims, arguments, and propositions — registered with priority, type, confidence tier, and source. Coverage is not 100%: a README is a guide, not a paper, and not every sentence is registered. The load-bearing ones are.

Tier vocabulary matches the [Confidence-to-Language Mapping](#confidence-to-language-mapping) above; type vocabulary matches the [Verification Registry](#verification-registry-the-foundation).

**Format note.** Simplified columns for README brevity: every row uses the CLAIM-style header (ID / Type / Priority / Confidence / Statement / Source / Anchor), with ARGUMENT- and PROPOSITION-specific fields (Toulmin Grounds / Warrant / Rebuttal; Whetten Constructs / Premises / Reasoning / Boundary conditions / Alternatives engaged) inlined into the Statement cell as "Warrant: …", "Boundary: …", and so on. Adopters maintaining actual paper registries should use the per-type sub-tables from [`templates/claim-registry.md`](templates/claim-registry.md); the single-table layout here is a compression for README readability, not the framework's normative form.

| ID | Type | Priority | Confidence | Statement | Source / Anchor | Where it appears |
|----|------|----------|------------|-----------|------------------|------------------|
| R-1 | PROPOSITION | P0 | EMERGING | Process-level verification infrastructure (templates + gates + decision records + registry) catches a class of AI-augmented-writing failure modes that tool-level checkers and model-level techniques do not fully address. Boundary: the four When-Worth-It tests; reduces to overhead for the When-Overkill cases. | Own use on three application classes (academic-paper, speculative-design, decision-support); Paper 1 (this repo) is the perspective article arguing the gap | [The Approach](#the-approach), [The Argument, Structurally](#the-argument-structurally) |
| R-2 | ARGUMENT | P0 | SUPPORTED | The systems-engineering identity (claims-as-components, sources-as-tests, coverage-as-measurable) operationalises verification rather than just metaphorising it. Warrant: typed registry + tier-monotonic language calibration + per-priority coverage targets are each independently tractable. Rebuttal addressed: the mapping is most natural for argumentative/empirical non-fiction and stretches for purely literary or oral genres. | [DR-007](decisions/DR-007_se-inspired-claim-verification.md) | [The Approach → SE mapping](#the-approach) |
| R-3 | CLAIM | P1 | SUPPORTED | LLMs introduce plausible-but-fabricated citations at rates high enough that unverified citations can survive into submission-ready drafts. | Hallucination literature as cited in [`templates/anti-hallucination.md`](templates/anti-hallucination.md) | [The Core Problem → Hallucinated citations](#the-core-problem), [Anti-Hallucination Checklist](#anti-hallucination-checklist) |
| R-4 | CLAIM | P1 | SUPPORTED | Plausibility-based review of calculations misses arithmetic errors that mechanical reproduction catches. | [DR-009](decisions/DR-009_calculation-verification.md) (calculation-verification rationale); [`agents/equation-checker.md`](agents/equation-checker.md) (designed implementation) | [Verification Registry → CALCULATION](#verification-registry-the-foundation), [`agents/equation-checker.md`](agents/equation-checker.md) |
| R-5 | PROPOSITION | P1 | EMERGING | A three-pass review pattern (intra-family small → intra-family large → cross-vendor) escapes biases a single pass cannot — sunk-cost-from-session, review-character convergence, training-prior alignment. Boundary: demonstrated at code-tooling scale within one model family (N=2 within Claude); paper-scale prose and cross-family generality remain untested. | [DR-011](decisions/DR-011_multi-model-review-pattern.md) (Status: Proposed) | [Peer Review Simulation](#peer-review-simulation), [Tools → cost data](#tools) |
| R-6 | CLAIM | P1 | SPECULATIVE | The numerical thresholds in Gate 2 (100% P0 / 90% P1 / 70% P2 / ≥85% overall) and Gate 3 (≥3.5/5.0 simulated peer review) are defensible defaults, not calibrated constants. | [`docs/THRESHOLDS.md`](docs/THRESHOLDS.md) (self-declared SPECULATIVE at top of file) | [Quality Gates](#quality-gates), [Measuring Success](#measuring-success) |
| R-7 | PROPOSITION | P2 | EMERGING | Speculative-design / design-fiction work creates an "inverse hallucination" risk — designed speculation presented as if it had a citable source — which Steps 0–6 of the standard anti-hallucination checklist will not catch. Boundary: opt-in extension for PROVOCATION-using projects only; standard academic papers can ignore. | [DR-010](decisions/DR-010_provocation-unit-type.md) | [Verification Registry → PROVOCATION](#verification-registry-the-foundation), [Anti-Hallucination Checklist → Step Z](#anti-hallucination-checklist) |

**Coverage note.** Type cut: 3 CLAIMs / 1 ARGUMENT / 3 PROPOSITIONs. Tier cut: 0 ESTABLISHED / 3 SUPPORTED / 3 EMERGING / 1 SPECULATIVE. The absence of an ESTABLISHED tier is intentional — the README does not yet have validated claims about its own efficacy, and forcing one would be the exact confidence-inflation failure the framework is supposed to catch.

**Why this section exists.** Two reasons. (1) The framework's strongest credibility move available post-scope-tightening is applying itself to its own home document — readers can audit the README's load-bearing claims using the apparatus the README proposes. (2) The exercise forces honest tiers: R-1 reads as EMERGING (not SUPPORTED), R-6 reads as SPECULATIVE (not SUPPORTED), and the README's earlier undifferentiated confidence tone hid that.

## Further Reading

- **[agent-ready-projects](https://github.com/ducroq/agent-ready-projects)** — The companion guide for AI-assisted coding (layered documentation model, auto-loading cliff, progressive disclosure)

## Contributing & Support

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guidance. Short version:

- **Adopters** — copy templates, pin a version in your project's CLAUDE.md, you're not expected to upstream changes.
- **Collaborators** — open an issue describing the proposed change before investing in a PR; most framework changes land as Decision Records.

Licence: CC BY 4.0 — see [`LICENSE`](LICENSE) and [`decisions/DR-013_license-choice.md`](decisions/DR-013_license-choice.md).

Upgrading a pinned version? See [`UPGRADING.md`](UPGRADING.md) — per-release adopter notes aggregated for quick lookup.
