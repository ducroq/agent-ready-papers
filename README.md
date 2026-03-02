# Working With AI Agents: Academic & Technical Writing

Verification infrastructure for AI-augmented academic writing — templates, quality gates, and session continuity that catch the failure modes automated tools miss. Patterns extracted from three real paper projects across two journals (IEEE TIM, MST), pressure-tested over 50+ agent sessions.

Automated citation checkers (RefChecker, scite.ai) and model-level solutions (RAG, grounded generation) address part of the problem. This guide operates at the **process level** — the workflow templates, decision records, and verification systems that make the difference between an agent that hallucinates citations and one that produces submission-ready prose.

Companion to [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code).

> **Want to get started fast?** Grab templates from [`templates/`](templates/) and adapt them to your paper project.

## The Core Problem

AI agents are remarkably useful for academic writing — literature synthesis, argument structuring, statistical interpretation, formatting. But they have failure modes that are *different* from coding:

- **Hallucinated citations.** Agents invent plausible-sounding papers, authors, and DOIs. A citation that looks correct but doesn't exist can survive multiple review rounds undetected.
- **Confidence inflation.** Agents state speculative claims with the same certainty as verified facts. "Demonstrates" and "suggests" carry very different weight in academic writing — agents don't naturally distinguish.
- **Scope creep.** Without architectural constraints, agents expand arguments beyond what the evidence supports, add sections that dilute focus, and exceed page budgets.
- **Terminology drift.** In interdisciplinary work, the same word means different things across fields. Agents mix terminology freely unless constrained by a reference document.
- **Invisible verification gaps.** Agents produce fluent prose that *reads* like it's well-sourced. Without a systematic verification system, gaps in evidence are invisible until a reviewer finds them.

The fix isn't avoiding AI assistance. It's building **verification infrastructure** — systematic processes that catch these failure modes before submission.

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

## Verification Registry: The Foundation

The registry tracks three unit types:

| Type | What it is | Where it appears | Verification |
|------|-----------|-----------------|--------------|
| **CLAIM** (default) | Factual statement with a source | All sections | Does the source exist and say this? |
| **ARGUMENT** | Reasoning chain combining evidence + inference | Discussion, Conclusion | Warrant valid? Evidence sufficient? Counter-arguments addressed? |
| **PROPOSITION** | Novel recommendation or contribution | Conclusion, Recommendations | Premises verified? Reasoning valid? Boundaries stated? |

Most entries are CLAIMs. ARGUMENTs and PROPOSITIONs appear in Discussion and Conclusion sections — the parts reviewers scrutinize most. All three share the same priority, confidence, and language calibration system.

### Priority (what breaks if this is wrong?)

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

Without this mapping, agents default to confident language for everything. A SPECULATIVE claim stated as "demonstrates" is a credibility risk that reviewers will catch. The writing guide template maps every claim to its section, confidence tier, and appropriate language. See [`templates/writing-guide.md`](templates/writing-guide.md).

**Own work under review** requires special framing: "we observed" (not "it was found"), with explicit status ("under review at IEEE TIM"). Don't let agents present under-review work as established.

## Anti-Hallucination Checklist

Before accepting any literature claim from an AI agent:

1. **Is the paper real?** (Google Scholar / DOI check)
2. **Is the author real?** (institutional affiliation page)
3. **Is the journal real?** (publisher website, not a predatory clone)
4. **Does the claim match the paper's scope?** (abstract check)
5. **Is the exact location cited?** (page / table / figure number)
6. **Have I read the relevant section?** (not just the abstract)

This is non-negotiable. Run it for every new citation the agent introduces. Agents can and will invent plausible-sounding papers with real-sounding author names. The checklist takes 2 minutes per citation. Catching a hallucinated citation in review takes 2 weeks.

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

This prevents scope creep — the most common failure mode when agents draft sections. Without a page budget, an introduction that should be half a page becomes two pages of background the reader doesn't need. The blueprint is a specification; the writing is implementation.

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

**Critical**: Run the review in a fresh session, not the one that helped write the paper. An agent reviewing its own work has sunk-cost bias in its context — it's unlikely to catch its own mistakes.

See [`templates/review-prompt.md`](templates/review-prompt.md) for a structured review prompt template.

## Terminology References

For interdisciplinary papers, create a **glossary** that serves as the single source of truth for terminology:

- Group terms by domain (metrology, simulation science, medical education, etc.)
- Include plain-language equivalents alongside formal definitions
- Note where terms overlap or conflict across fields
- Reference the standard each term comes from (VIM, GUM, ISO, APA)

This prevents terminology drift — agents using "accuracy" when they mean "trueness" (a VIM distinction), or mixing "fidelity" across its simulation and measurement meanings. Point the agent to the glossary in your project file (CLAUDE.md) so it's consulted before writing.

See [`templates/glossary.md`](templates/glossary.md).

## Quality Gates

Each gate must pass before proceeding:

### Gate 1: Draft Complete
- [ ] All sections drafted to page budget
- [ ] Claim registry populated with all factual statements
- [ ] P0 claims identified and prioritized

### Gate 2: Verification Complete
- [ ] P0 claims 100% verified
- [ ] P1 claims 90% verified
- [ ] Overall coverage ≥85%
- [ ] Static checks pass (LaTeX compiles, BibTeX valid, DOIs resolve)
- [ ] Anti-hallucination checklist run on all AI-introduced citations

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
# DR-001: Focus on infant ventilation (exclude adult compression)

## Context
Paper could cover adult + infant, both compression + ventilation.
Page budget forces a choice.

## Decision
Infant ventilation primary, infant compression secondary (descriptive only).

## Rationale
- Infant ventilation has the clearest human reference data (Huang 2016)
- No human reference exists for infant compression (Kent 2010)
- This gives us a clean fidelity gap analysis for ventilation

## Revisit If
- Human infant compression data becomes available
- Page budget increases (e.g., journal offers extended format)
```

Without DRs, agents will re-propose excluded approaches. "Should we add adult compression data?" gets answered once in DR-001, not every session.

See [`templates/decision-record.md`](templates/decision-record.md).

## Project File for Paper Projects

Your CLAUDE.md (or equivalent) for a paper project should include:

1. **Paper identity** — what it argues, target journal, deadline
2. **Core concept** — the key insight in 2-3 sentences
3. **Session continuity** — what to read on session start, what to update on session end
4. **Key files table** — where everything lives
5. **Methodology summary** — confidence tagging, claim audits, anti-hallucination
6. **Before You Start** table — task-triggered pointers:

```markdown
| When | Read |
|------|------|
| Writing or editing prose | `writing-guide.md` — claim-to-section mapping with language calibration |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with status |
| Making scope or methodology decisions | `DR-*.md` — decision records index |
| Checking terminology | `glossary.md` — cross-domain term definitions |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
```

See [`templates/CLAUDE.md`](templates/CLAUDE.md).

## Workflow Phases

A structured workflow prevents the common failure of jumping straight to writing:

### Phase 0: Problem Framing
- Define research questions clearly
- Identify target audience and outlet format
- Document initial decisions (DR-000, DR-001)

### Phase 1: Requirements
- Define paper goals (what must the paper demonstrate?)
- Specify success criteria
- Identify key claims that need support
- Map claims to required evidence

### Phase 2: Literature Audit
- Register all claims in the claim registry
- For each: find source → verify it exists → extract exact citation → tag confidence
- Flag unsupported claims for resolution

### Phase 3: Writing
- Follow the architecture blueprint (page budgets)
- Use the writing guide (confidence → language)
- Run anti-hallucination checklist on new citations
- Pass quality gates per section

### Phase 4: Validation
- Simulated peer review (fresh session)
- Co-author review
- Full claim audit (coverage report)

### Phase 5: Submission
- Format to journal requirements
- Final citation check
- Data availability statement
- Author agreement

## Session Continuity

Paper projects span many sessions — often months. Session continuity is critical.

### Starting a session
1. Read CLAUDE.md (project identity and current state)
2. Read the backlog (current tasks and priorities)
3. Check recent decision records (any pending decisions?)
4. Resume from last state (don't restart completed work)

### Ending a session
1. Update the backlog with progress
2. Commit all changes
3. Update CLAUDE.md if a major milestone was reached

### AI handoff
If switching AI systems or starting a fresh session:
- CLAUDE.md is the primary handoff document
- All context should be recoverable from committed files
- No reliance on conversation memory

## What Doesn't Work

### Trusting agent citations without verification
Agents hallucinate citations. Not occasionally — routinely. Every citation needs the anti-hallucination checklist. This is the single most important practice in this guide.

### Writing before the claim registry
Prose written without a claim registry is prose that will need to be rewritten. The registry forces you to identify what you're claiming and whether you can support it *before* you invest in beautiful sentences.

### Reviewing in the building session
An agent that spent an hour helping write Section 3 will not catch its own errors in Section 3. Use a fresh session for review — or a different model entirely.

### Skipping the architecture blueprint
Without page budgets, agents expand every section. A 4-page paper becomes 8 pages. A focused argument becomes a literature review. The blueprint is constraint that enables quality.

### Mixing terminology across domains
In interdisciplinary work, letting agents use terms freely creates a paper that confuses every reviewer. A glossary isn't overhead — it's a prerequisite for clarity.

### Confident language for weak claims
"Our results demonstrate" for a SPECULATIVE inference is a credibility risk. The confidence-to-language mapping is mechanical but essential — it prevents the most subtle form of academic dishonesty.

## Measuring Success

You know the system is working when:
- Claim registry coverage is above 85% before submission
- All P0 claims are at 100% verification
- Simulated peer review scores above 3.5/5.0
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

## Templates

Ready-to-use starter files in [`templates/`](templates/):

- **[`CLAUDE.md`](templates/CLAUDE.md)** — Paper project identity, session continuity, Before You Start table
- **[`claim-registry.md`](templates/claim-registry.md)** — Claim tracking with priority, confidence, source tiers
- **[`vv-framework.md`](templates/vv-framework.md)** — Verification and validation framework
- **[`writing-guide.md`](templates/writing-guide.md)** — Confidence-to-language mapping, section-claim assignment
- **[`review-prompt.md`](templates/review-prompt.md)** — Structured AI peer review with scoring rubric
- **[`decision-record.md`](templates/decision-record.md)** — Lightweight ADR for scope and methodology decisions
- **[`anti-hallucination.md`](templates/anti-hallucination.md)** — Citation verification checklist
- **[`glossary.md`](templates/glossary.md)** — Cross-domain terminology reference

Copy what you need, delete the comments, fill in your specifics.

## Further Reading

- **[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)** — How these patterns were developed from three real paper projects, including the concrete failures that shaped them
- **[agent-ready-projects](https://github.com/ducroq/agent-ready-projects)** — The companion guide for AI-assisted coding (layered documentation model, auto-loading cliff, progressive disclosure)
