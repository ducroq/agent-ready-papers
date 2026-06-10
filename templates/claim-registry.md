# Claim Registry

<!-- The paper's verification registry. Every factual claim, argument,
     and proposition tracked here. Most entries are CLAIMs (default).
     Use ARGUMENT for Discussion/Conclusion reasoning chains.
     Use PROPOSITION for novel contributions and recommendations.
     Update this living document throughout the writing process. -->

**Paper:** [Title]
**Last Updated:** [date]
**Thesis:** [One-line thesis]

---

## Coverage Summary

Two cuts of the same row set. Both should be filled when a registry contains more than one unit type; CLAIM-only registries can omit the by-type table.

**Coverage by Priority**

| Priority | Total | Verified | Needs Evidence | Coverage |
|----------|-------|----------|----------------|----------|
| P0 | 0 | 0 | 0 | 0% |
| P1 | 0 | 0 | 0 | 0% |
| P2 | 0 | 0 | 0 | 0% |
| **Total** | **0** | **0** | **0** | **0%** |

**Coverage by Type**

| Type | Total | Verified | Coverage |
|------|-------|----------|----------|
| CLAIM | 0 | 0 | 0% |
| ARGUMENT | 0 | 0 | 0% |
| PROPOSITION | 0 | 0 | 0% |
| PROVOCATION | 0 | 0 | 0% |
| **Total** | **0** | **0** | **0%** |

A combined Priority × Type matrix is optional for papers with many of both axes.

**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2. Type-level targets are project-conditional — for example, every registered ARGUMENT and PROPOSITION should be `[x]` before Gate 2, because each is load-bearing for the contribution.

---

## Priority Guide

### P0 (Critical) — paper fails without these
<!-- Claims that, if wrong, break the core argument -->

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| [ID] | [claim] | [consequence] |

### P1 (Important) — target 90%
<!-- Claims that strengthen but don't break the argument -->

### P2 (Supporting) — target 70%
<!-- Context and background claims -->

---

## Registry by Section

Each section may contain up to four sub-tables — one per unit type — and includes only the ones it needs. Most sections are CLAIM-only; Discussion / Conclusion sections typically add ARGUMENT and PROPOSITION sub-tables; speculative-design work adds PROVOCATION (see DR-010). Each sub-table's columns match its verification checklist, so every required field has a structural home (no orbiting prose blocks below the table).

**ID convention.** IDs are `S<section>-<number>` (e.g. `S3-2`) and are **unique within a section across all four sub-tables** — `S3-2` exists in at most one of the CLAIM / ARGUMENT / PROPOSITION / PROVOCATION sub-tables for Section 3. A `Grounds`/`Premises` reference like `S3-2` is therefore resolvable by `Ctrl-F` within the section; the sub-table header (`**ARGUMENTs**`, etc.) tells the verifier what type the target is.

**List delimiter convention (`;`).** The semicolon is the **list delimiter throughout the registry**, used wherever a cell carries more than one value:

- `Source` + `Source Tier` — sources and their tiers in **parallel order** (position *i* in `Source Tier` corresponds to position *i* in `Source`). Example: `Author1 Year; Author2 Year` → `A; C`.
- `Grounds`, `Premises`, `Rebuttal`, `Alternatives engaged` — lists of registry IDs or short phrases. Example: `S1-2; S2-1`.

Edge cases:
- **Source with no tier yet** (e.g. own work in preparation, status unclear): use `[TBD]` in the corresponding `Source Tier` position and mark the row `[~]` (in progress) until tier is assigned.
- **`;` collision with markdown tables**: safe inside `|`-delimited cells in CommonMark, GFM, and pandoc. The real hazard is `|` itself inside cells — escape as `\|` if needed.

### Section 1: [Section Name]

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S1-1 | [factual statement] | P0 | ESTABLISHED | [Author Year] | A | [ ] |
| S1-2 | [factual statement] | P1 | EMERGING | [OWN WORK] | E | [ ] |
| S1-3 | [factual statement supported by two sources] | P1 | SUPPORTED | [Author1 Year]; [Author2 Year] | A; A | [ ] |

<!-- Repeat for each section. Add ARGUMENT / PROPOSITION / PROVOCATION sub-tables
     below when the section contains those unit types. -->

### Section N: Discussion

<!-- Discussion and Conclusion sections typically contain ARGUMENTs and PROPOSITIONs
     alongside standard CLAIMs. Each unit type has its own sub-table matching its
     verification checklist — Toulmin for ARGUMENT, Whetten for PROPOSITION,
     Auger for PROVOCATION. -->

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| SN-3 | [factual comparison] | P1 | SUPPORTED | [Author Year] | A | [ ] |

**ARGUMENTs** (Toulmin — see verification checklist below):

| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Source | Source Tier | Status |
|----|-----------|----------|------------|---------|---------|----------|--------|-------------|--------|
| SN-1 | [interpretive conclusion] | P0 | SUPPORTED | S1-2; S2-1 | [inferential bridge] | [strongest counter-arguments addressed] | [optional Toulmin "backing" citation] | A | [ ] |

<!-- Grounds: list registry IDs (semicolon-separated) of **CLAIMs or verified ARGUMENTs**
     this argument builds on. Each must be marked [x] verified in its own row.
     SPECULATIVE grounds cannot support SUPPORTED or ESTABLISHED arguments.
     Source / Source Tier are optional and used only for Toulmin "backing" — an external
     citation that supports the warrant itself, distinct from the registry-internal grounds. -->

**PROPOSITIONs** (Whetten — see verification checklist below):

| ID | Statement | Priority | Confidence | Constructs | Relationship | Premises | Reasoning | Boundary conditions | Alternatives engaged | Source | Source Tier | Status |
|----|-----------|----------|------------|------------|--------------|----------|-----------|---------------------|----------------------|--------|-------------|--------|
| SN-2 | [recommendation] | P1 | EMERGING | [X, Y, Z defined] | [X enables Y under Z] | S1-2; S2-3 | [logical basis] | [where applies / where doesn't] | [alt explanations engaged] | [optional framework-provenance citation] | C | [ ] |

<!-- Whetten 5-item coverage: Constructs (What), Relationship (How), Reasoning (Why),
     Boundary conditions (Who-Where-When), Alternatives engaged.
     Premises: list registry IDs (semicolon-separated) of CLAIMs / ARGUMENTs this
     proposition rests on.
     Boundary conditions must be specific, falsifiable, and bounded — see anti-pattern
     checks below.
     Source / Source Tier are optional and used only for external framework provenance. -->

**PROVOCATIONs** (Auger — opt-in, speculative-design only; see DR-010):

Column semantics differ from the other sub-tables: Auger's four criteria are *evaluative questions*, so each column records the **evidence or move that answers the question**, not a yes/no judgment. The column headers below name the content the cell should carry.

| ID | Statement | Priority | Tier (PROVOCATION axis) | Plausibility evidence | Generative move | Reflexive marker | Ethics commitment | Status |
|----|-----------|----------|--------------------------|------------------------|------------------|-------------------|--------------------|--------|
| SN-4 | [diegetic prototype / reflexive Ask / paradox box] | P1 | GROUNDED | [why a reader could hold this seriously inside the fiction] | [how the surrounding prose develops the artefact as material] | "[exact prose phrasing — required, verbatim]" | [potential harm considered + DR-level pre-commitment binding for writing] | [ ] |

<!-- Tier uses the PROVOCATION axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL),
     not the evidence-strength axis.
     Reflexive marker must quote the prose phrasing verbatim — without it the entry is
     indefensible (see Step Z in anti-hallucination.md and DR-010).
     Each Auger criterion is recorded as the *substance* of the answer, not "yes/no".
     An empty cell means the criterion has not been addressed; the entry is then not yet
     verifiable as a PROVOCATION and should remain `[ ]` or be marked `[!]`. -->

**Empty-cell convention.** A blank cell in any optional column (e.g. `Source` for an ARGUMENT, `Alternatives engaged` for a low-stakes PROPOSITION) is acceptable. A blank cell in a **required** column for that unit type signals the entry is not yet verifiable — keep the row `[ ]` or mark `[!]` and address before promoting confidence.

---

## Source Verification Checklist

### Literature Sources

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| [Author Year] | [IDs] | [specific values/statements to verify] | [ ] |

### Own Data

| Data Source | Claims | What to Check |
|-------------|--------|---------------|
| [dataset/experiment] | [IDs] | [data files exist, analysis reproducible] |

### Own Work (Under Review)

| Paper | Claims | Venue | Status |
|-------|--------|-------|--------|
| [paper title] | [IDs] | [journal] | [under review / accepted / published] |

---

## Out of Scope

<!-- Claims verified but excluded (preserve for future reference) -->

| ID | Claim | Source | Why Excluded |
|----|-------|--------|-------------|
| [ID] | [claim] | [source] | [reason — link to DR if applicable] |

---

## Unit Type Reference

| Type | When to use | Verification | Typical sections |
|------|------------|--------------|-----------------|
| **CLAIM** (default) | Factual statement with a source | Does the source exist and say this? | All sections |
| **ARGUMENT** | Interpretive conclusion combining evidence + reasoning | Warrant valid? Evidence sufficient? Counter-arguments addressed? | Discussion, Conclusion |
| **PROPOSITION** | Novel recommendation or contribution | Premises verified? Reasoning valid? Boundary conditions stated? | Conclusion, Recommendations |
| **PROVOCATION** (opt-in) | Designed artefact making no truth claim — diegetic prototype, reflexive Ask, paradox box | Plausible? Generative? Reflexive marker present? Ethically held? | Speculative-design / design-fiction work only (see DR-010) |

### Detecting Mistyped Entries

Every audit found 3–6 entries initially typed as CLAIMs that were actually ARGUMENTs or PROPOSITIONs. Run this decision tree on each entry after initial registration:

1. **Does it cite a specific external source?** → Likely CLAIM
2. **Does it draw a conclusion from multiple pieces of evidence?** → Likely ARGUMENT
3. **Does it recommend, propose, or prescribe?** → Likely PROPOSITION
4. **Does it interpret data rather than report it?** → Likely ARGUMENT (even if it cites the data source)
5. **Does it state a relationship between constructs?** → Likely PROPOSITION if novel, CLAIM if citing existing work
6. **Does it make no truth claim — a designed/fictional artefact in a speculative-design work?** → PROVOCATION (opt-in; see DR-010)
7. **Does it look like a truth claim but is actually a design choice (e.g., a fictional category imitating an authoritative form)?** → PROVOCATION; require an explicit reflexive marker in the prose

**Red flags for mistyped CLAIMs:**
- Entry has no single source (it synthesizes multiple sources → ARGUMENT)
- Entry appears in Discussion/Conclusion (often ARGUMENT or PROPOSITION, not CLAIM)
- Entry was scored low on source verification but "feels" well-supported (may be a well-grounded ARGUMENT evaluated with the wrong procedure)
- Entry states "should", "needs", or "we propose" (→ PROPOSITION)
- Entry is a fictional category, diegetic prototype, or reflexive construction with no real source (→ PROVOCATION, not SPECULATIVE CLAIM — see DR-010). Marking such an entry as a CLAIM with a fabricated source is the inverse of standard hallucination and equally dangerous

**When to re-check types:** After initial registration (Gate 1), and again after verification (Gate 2) if any entries scored unexpectedly low.

### Verifying ARGUMENTs (Toulmin checklist)

1. Is the claim clearly stated?
2. Are the grounds (evidence) verified? (These should be CLAIMs in this registry)
   - **Grounds traceability:** List the registry IDs that serve as grounds (e.g., S1-5, S1-7, S1-8)
   - Each ground must be marked [x] verified in the registry
   - SPECULATIVE grounds cannot support SUPPORTED or ESTABLISHED arguments
3. Is the warrant (inferential bridge) explicit and valid for the target audience?
4. Is the qualifier calibrated to evidence strength? (Maps to confidence tiers)
5. Are the strongest counter-arguments addressed? (Not strawmen)

### Verifying PROPOSITIONs (Whetten checklist)

1. Are all key constructs defined?
2. Is the relationship clearly stated?
3. Is the reasoning (warrant) explicit and valid?
4. Are boundary conditions specified? (See quality criteria below)
5. Does it engage with alternative explanations?

**Boundary conditions** — required field for every PROPOSITION:

```markdown
Boundary conditions: [Where does this apply? Where doesn't it?]
```

Good boundary conditions are specific and testable:
- **Good:** "Applies to engineering domains requiring judgment; may not hold for routine, well-defined tasks"
- **Good:** "Holds when team size < 10 and iteration cycles are weekly or shorter"
- **Bad (tautological):** "Applies when applicable" / "Holds when conditions are met"
- **Bad (moving target):** "Applies unless future evidence suggests otherwise"
- **Bad (overgeneralized):** "Applies to all engineering domains" — no upper bound on scope
- **Bad (missing):** No boundary conditions stated — every proposition has limits

Anti-patterns to check:
- **Tautological** — boundary condition restates the proposition
- **Moving target** — boundary condition can never be falsified
- **Overgeneralized** — "applies to all X" without specifying where it breaks down

**Falsification criteria quality** (for each PROPOSITION):
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the proposition (not circular)
- [ ] Criterion is specific enough to be measurable
- [ ] Criterion is not a moving target

See `vv-framework.md` Section 4.1 for the full Whetten verification procedure.

### Verifying PROVOCATIONs (Auger checklist — opt-in, see DR-010)

Applies only to projects that contain designed artefacts making no truth claim (speculative-design, design-fiction, diegetic-prototype work). Standard empirical and methodological papers do not need this section.

Verification questions (adapted from Auger 2013, *Digital Creativity* 24:1):

1. **Plausible** — Could this exist in some adjacent world consistent enough that a reader holds it seriously inside the fiction?
2. **Generative** — Does the surrounding prose reach into the artefact (taking it as material to develop) rather than around it?
3. **Reflexive** — Is a marker visible *in the prose* (not only in the registry) at every load-bearing moment, signalling fictionality?
4. **Ethically held** — Has potential for harm been considered, with a DR-level pre-commitment binding for chapter writing?

**Reflexive marker** — required field for every PROVOCATION:

```markdown
Reflexive marker: [Quote the exact prose phrasing that signals fictionality]
```

If no marker is present in the prose: rewrite to add it, or downgrade the entry to EMERGING CLAIM with additional sources. PROVOCATIONs without reflexive markers are indistinguishable from authoritative-toned hallucinations and undermine the whole speculative-design contract with the reader.

**The inverse-hallucination risk:** a CLAIM hallucination invents a source for a real-sounding statement. A PROVOCATION risks the reverse — being read as a CLAIM with a citable source when no source applies. An agent presenting a fictional speculative-design criterion ending in `[Author, Year]` has hallucinated *into* fictional territory. See `anti-hallucination.md` Step Z.

---

## Confidence Tier Reference

| Tier | Assign when... | Language |
|------|---------------|----------|
| **ESTABLISHED** | CLAIM: multiple independent sources. ARGUMENT: complete Toulmin + fair engagement. PROPOSITION: premises verified + logic valid + tested | "demonstrates", "shows", "confirms" |
| **SUPPORTED** | CLAIM: 2-3 sources agree. ARGUMENT: warrant valid + evidence sufficient. PROPOSITION: premises verified + logic valid | "indicates", "supports", "evidence suggests" |
| **EMERGING** | CLAIM: 1-2 sources. ARGUMENT: evidence partial or warrant debatable. PROPOSITION: premises plausible + logic sound | "may", "preliminary evidence", "initial findings suggest" |
| **SPECULATIVE** | CLAIM: inference only. ARGUMENT: position stated, logic incomplete. PROPOSITION: conjectural | "warrants investigation", "remains unclear", "we hypothesize" |

### Typed Confidence Assessment

<!-- How many verification checks correspond to each tier, by unit type.
     For CLAIMs, confidence tracks source strength. For ARGUMENTs and
     PROPOSITIONs, confidence tracks checklist completeness + premise quality. -->

| Type | ESTABLISHED | SUPPORTED | EMERGING | SPECULATIVE |
|------|-------------|-----------|----------|-------------|
| CLAIM | 3+ independent sources, textbook consensus | 2–3 sources agree, open questions | 1–2 sources, not replicated | Logical inference, no data |
| ARGUMENT | 5/5 Toulmin, premises ESTABLISHED | 4/5 Toulmin, premises SUPPORTED+ | 3/5 Toulmin, premises verified but conclusion untested | <3/5 Toulmin, or premises unverified |
<!-- Note: "5/5 Toulmin" refers to the 5-item operationalized checklist (claim, grounds, warrant, qualifier, rebuttal),
     not Toulmin's original 6 components (which include backing as a separate element). See DR-004 for the operationalization rationale. -->
| PROPOSITION | 5/5 Whetten, tested in practice | 4/5 Whetten, premises verified | 3/5 Whetten, reasoning valid but untested | <3/5 Whetten, or missing boundary conditions |

### PROVOCATION Confidence — Separate Axis

PROVOCATIONs do not measure evidence strength; they measure quality of speculation. The tiers below replace ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE for PROVOCATION entries only. Each tier carries a *required prose marker* — a phrasing that must appear in the manuscript itself, not only in the registry. See DR-010.

| Tier | Assign when… | Required prose marker |
|------|--------------|------------------------|
| **GROUNDED** | Speculation explicitly anchored in cited research; mechanism named; warrant visible | *"If X (source Y), then a speculative manifestation might look like…"* |
| **EXTRAPOLATED** | Extension of an existing pattern (e.g., DSM dimensional approach) into fictional territory; warrant visible but underpinning partial | *"By analogy with X, we propose a fictional Y…"* |
| **PROVOCATIVE** | Deliberately uncomfortable, rhetorical; ethical hedge explicit; no empirical pretension | *"Deliberately uncomfortable: what if…"* |
| **CRITICAL** | The fiction itself critiques an existing system (e.g., DSM form imitated to surface diagnostic reification) | *"By imitating this DSM form we ask…"* |

No marker = indefensible PROVOCATION. Remediation: rewrite to add the marker, or downgrade the entry to EMERGING CLAIM with additional sources.

## Source Tier Reference

| Tier | Type | Weight |
|------|------|--------|
| A | Peer-reviewed primary research | 1.0 |
| B | Peer-reviewed review article | 0.8 |
| C | Textbook / established reference | 0.9 |
| D | Guidelines / industry standards | 0.7 |
| E | Own unpublished work (under review) | 0.6* |
| F | Logical inference | 0.2 |

\* **Own data vs. own work (DR-008):** The 0.6 weight applies to own work cited from
papers under review elsewhere. For **own-data claims** — results from experiments reported
in the current paper — confidence should reflect methodological rigor (sample size,
statistical power, reproducibility, calibration), not source count. Assign confidence
based on the evidence quality:
- Large sample, adequate power, validated method → ESTABLISHED or SUPPORTED
- Small sample, exploratory, single-site → EMERGING
- Pilot data, proof-of-concept → SPECULATIVE

### Special Cases: Reference Claims

CLAIMs that are verifiable facts about external documents — e.g., "AHA recommends X
with Class I evidence" or "ISO 17025 requires Y" — should use **ESTABLISHED** when the
source is publicly accessible and the statement is a direct, verifiable reference. These
are not evidence-dependent claims requiring confidence assessment; they are facts about
what a document says. If the document exists and says this, the claim is verified.

Use ESTABLISHED for reference claims when:
- The source document is publicly accessible (published guideline, standard, or regulation)
- The statement is a direct reference to what the document says (not an interpretation)
- Verification requires only checking the document, not evaluating evidence strength

### Special Cases: Framework Components

<!-- DR-004: Novel frameworks get written in ESTABLISHED language when they're
     actually EMERGING/SPECULATIVE. This is the most common language calibration error.
     See also writing-guide.md — Framework Component Language special case. -->

When a paper proposes a new framework, the framework components start at EMERGING or lower
regardless of the evidence that motivated them. The framework is an interpretation of
evidence, not the evidence itself.

| Stage | Confidence | Example |
|-------|-----------|---------|
| Conjectural, no supporting evidence | SPECULATIVE | "We hypothesize a multiplicative relationship" |
| Novel contribution, supporting evidence but no validation | EMERGING | "We propose a multiplicative relationship" |
| Initial validation (pilot, case study) | SUPPORTED | "Pilot data supports the multiplicative model" |
| Independent replication | ESTABLISHED | "Multiple studies confirm the multiplicative relationship" |

This applies even when the evidence *supporting* the framework is strong — the evidence
supports the framework's premises, but the framework's structure and claims are untested
interpretations until validated.

### Special Cases: Methodological Facts

<!-- DR-008: Results from applying a published standard method (e.g., GUM uncertainty
     budgets, ISO statistical tests, validated analytical procedures) are not
     evidence-strength claims — they are calculations with documented inputs. -->

Results from applying a published standard method are **ESTABLISHED** when:
- The calculation follows a published standard (e.g., GUM, ISO 5725, ASTM method)
- All inputs are documented (raw data, parameters, assumptions)
- The result is reproducible (another analyst with the same inputs gets the same answer)

These are methodological facts — the confidence comes from the method's validity, not from
independent replication of the result itself.

**Key distinction:**
| Statement | Type | Why |
|-----------|------|-----|
| "Expanded uncertainty is ±2.29% (k=2, GUM)" | Methodological fact → ESTABLISHED | Calculation follows published standard with documented inputs |
| "This uncertainty is acceptable for clinical use" | ARGUMENT → needs Toulmin | Interprets the result against a threshold — warrant can be challenged |
| "GUM requires combining Type A and Type B uncertainties" | Reference claim → ESTABLISHED | Direct statement about what the standard says |

## Status Legend

| Status | Meaning |
|--------|---------|
| [ ] | Not yet verified |
| [~] | In progress |
| [x] | Verified |
| [!] | Problem — needs attention |

---

## Cross-Reference Rules

- No claim accepted on a single non-textbook source
  - **Exception (DR-008):** Own-data claims with documented methodology (data files, analysis scripts, reproducible pipeline) are accepted on the strength of the methodology, not source count
- Contradictory sources must be acknowledged in the text
- Claims >10 years old need a recency check
- Own work under review must be explicitly flagged

---

*Registry created: [date]*
