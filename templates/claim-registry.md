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

| Priority | Total | Verified | Needs Evidence | Coverage |
|----------|-------|----------|----------------|----------|
| P0 | 0 | 0 | 0 | 0% |
| P1 | 0 | 0 | 0 | 0% |
| P2 | 0 | 0 | 0 | 0% |
| **Total** | **0** | **0** | **0** | **0%** |

**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2

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

### Section 1: [Section Name]

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S1-1 | [factual statement] | CLAIM | P0 | ESTABLISHED | [Author Year] | A | [ ] |
| S1-2 | [factual statement] | CLAIM | P1 | EMERGING | [OWN WORK] | E | [ ] |

<!-- Repeat for each section -->

### Section N: Discussion

<!-- Discussion and Conclusion sections typically contain ARGUMENTs and PROPOSITIONs
     alongside standard CLAIMs. Use the verification guides below. -->

| ID | Statement | Type | Priority | Confidence | Source / Warrant | Source Tier | Status |
|----|-----------|------|----------|------------|-----------------|-------------|--------|
| SN-1 | [interpretive conclusion] | ARGUMENT | P0 | SUPPORTED | Warrant: [inferential bridge] | -- | [ ] |
| SN-2 | [recommendation] | PROPOSITION | P1 | EMERGING | Reasoning: [logical basis] | -- | [ ] |
| SN-3 | [factual comparison] | CLAIM | P1 | SUPPORTED | [Author Year] | A | [ ] |

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

### Verifying ARGUMENTs (Toulmin checklist)

1. Is the claim clearly stated?
2. Are the grounds (evidence) verified? (These should be CLAIMs in this registry)
3. Is the warrant (inferential bridge) explicit and valid for the target audience?
4. Is the qualifier calibrated to evidence strength? (Maps to confidence tiers)
5. Are the strongest counter-arguments addressed? (Not strawmen)

### Verifying PROPOSITIONs (Whetten checklist)

1. Are all key constructs defined?
2. Is the relationship clearly stated?
3. Is the reasoning (warrant) explicit and valid?
4. Are boundary conditions specified?
5. Does it engage with alternative explanations?

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
| PROPOSITION | 5/5 Whetten, tested in practice | 4/5 Whetten, premises verified | 3/5 Whetten, reasoning valid but untested | <3/5 Whetten, or missing boundary conditions |

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
