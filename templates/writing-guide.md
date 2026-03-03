# Writing Guide: Registry-to-Section Mapping

<!-- Maps verified registry entries (CLAIMs, ARGUMENTs, PROPOSITIONs) to
     paper sections with language calibration. Consult before writing or
     editing any section. -->

**Paper:** [Title]
**Last Updated:** [date]

---

## How to Use This Guide

1. **Before writing a section:** Check which registry entries apply (CLAIMs, ARGUMENTs, PROPOSITIONs)
2. **For each entry:** Use the confidence tier to calibrate language
3. **For CLAIMs:** Source details are in `claim_registry.md`
4. **For ARGUMENTs:** Check that the warrant is explicit and grounds are verified CLAIMs
5. **For PROPOSITIONs:** Check that reasoning is explicit and boundary conditions are stated
6. **For quotes:** Keep a key quotes file for verbatim text

---

## Language Calibration

| Confidence Tier | Language |
|-----------------|----------|
| ESTABLISHED | "demonstrates", "shows", "confirms", "established" |
| SUPPORTED | "indicates", "supports", "evidence suggests" |
| EMERGING | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | "warrants investigation", "remains unclear", "we hypothesize" |

### Writing by Unit Type

| Type | How to write it | Watch for |
|------|----------------|-----------|
| CLAIM | State the fact, cite the source, match language to tier | Overclaiming (confident language for EMERGING/SPECULATIVE) |
| ARGUMENT | State the conclusion, present the evidence (grounds), make the warrant explicit | Implicit warrants that the reader won't share; missing counter-arguments |
| PROPOSITION | State the recommendation, give the reasoning, specify where it applies | Overgeneralization; missing boundary conditions |

**ARGUMENT prose pattern:**
> [Grounds — the evidence, citing verified CLAIMs]. [Warrant — why this evidence leads to the conclusion]. [Qualifier — hedging per confidence tier]. [Therefore, conclusion]. [Rebuttal — acknowledging the strongest counter-argument].

Example: "Manikin A produced force errors exceeding 15% across all test conditions (Table 2). Since clinical guidelines require feedback accuracy within 10% to support skill transfer [Author, Year], these errors are clinically significant. This **suggests** that current compression feedback in Manikin A is insufficient for competency-based training, although performance may differ under instructor-guided conditions."

**PROPOSITION prose pattern:**
> [Reasoning — why this recommendation follows from the arguments]. [Proposition — the recommendation itself]. [Boundary conditions — where it applies and where it doesn't].

Example: "Given the systematic feedback errors documented above, we propose that CPR training programs should prioritize manikin feedback accuracy over anatomical realism when selecting training equipment. This applies to competency-based programs targeting measurable skill outcomes; instructor-led demonstration contexts, where visual realism may support engagement, fall outside this recommendation."

### Special Cases

| Situation | Language |
|-----------|----------|
| Own work (under review) | "we observed", "our findings indicate" — never "it was found" |
| Own work (published) | "we previously demonstrated" with citation |
| Logical inference | "If [premises], then [conclusion]" — mark as inference |
| Single study | "In a study of N=X, [Author] found..." — note sample size |
| Contradictory evidence | "While [Author1] reported X, [Author2] found Y" — acknowledge both |

---

## Section → Registry Mapping

### Worked Example (from a Proposition paper's Introduction)

<!-- This shows what a completed section mapping looks like. The example uses
     real data from a CPR manikin fidelity paper to illustrate how registry
     entries, confidence tiers, calibrated language, and key quotes come
     together in a section mapping. Adapt the pattern; don't copy the content. -->

**Purpose:** Establish that manikin measurement fidelity is under-examined, setting up the paper's core argument.

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| H1 | 5.6% calibration shift in-phantoma | CLAIM | SUPPORTED | "we observed" (own work under review) |
| H2 | 120–130× datasheet deviation | CLAIM | SUPPORTED | "manufacturer specifications may not align" |
| H5 | Manikin chest compliance exceeds human tissue stiffness | CLAIM | SUPPORTED | "commercial manikins may not faithfully replicate" |
| F1 | Skill transfer depends on functional alignment, not visual resemblance | CLAIM | SUPPORTED | "Norman et al. argued" (attribution) |

**Key quotes ready:**
- Norman 2012: "nearly all the studies showed no significant advantage of HFS over LFS, with average differences ranging from 1% to 2%" (p. 636)
- Lim 2024: "no information on these properties is provided" (supporting H2)

**Caution:** H1 and H2 are N=1 findings from own work under review. Use "preliminary", "one device", and flag review status.

---

<!-- Now fill in the actual sections for your paper below -->

### 1. Introduction

**Purpose:** [What this section establishes]

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| [ID] | [statement] | CLAIM | [tier] | [calibrated phrasing] |

**Key quotes ready:**
- [Author Year]: "[exact quote]" (p. [N])

---

### 2. [Section Name]

**Purpose:** [What this section establishes]

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| [ID] | [statement] | CLAIM | [tier] | [calibrated phrasing] |

**Data to cite:**
```
[Key numbers, ranges, or statistics relevant to this section]
```

**Caution:** [Any nuances, caveats, or framing requirements]

---

### N. Discussion / Conclusion

<!-- This is where ARGUMENTs and PROPOSITIONs typically appear -->

**Purpose:** [What this section argues and recommends]

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| [ID] | [interpretive conclusion] | ARGUMENT | [tier] | [calibrated phrasing] |
| [ID] | [recommendation] | PROPOSITION | [tier] | [calibrated phrasing] |

**Warrant check:** For each ARGUMENT, state the warrant explicitly:
- [ID]: Warrant = [why the evidence supports this conclusion]

**Boundary check:** For each PROPOSITION, state the limits:
- [ID]: Applies to [context]; does NOT apply to [exclusions]

---

<!-- Repeat for each section -->

## Quick Reference: All Entries by Tier

### ESTABLISHED / SUPPORTED — Ready for Strong Statements

| ID | Statement | Type | Tier | Best Source |
|----|-----------|------|------|------------|
| [ID] | [statement] | CLAIM | [tier] | [Author Year] |

### EMERGING — Appropriately Hedged

| ID | Statement | Type | Tier | Hedging Language |
|----|-----------|------|------|------------------|
| [ID] | [statement] | CLAIM | EMERGING | [suggested phrasing] |

### SPECULATIVE — Requires Careful Framing

| ID | Statement | Type | Tier | How to Frame |
|----|-----------|------|------|--------------|
| [ID] | [statement] | CLAIM | SPECULATIVE | [framing approach] |

---

## Pre-Submission Checklist

### CLAIMs
- [ ] All P0 claims at SUPPORTED or ESTABLISHED (or explicitly framed as hypothesis)
- [ ] Language matches confidence tiers throughout
- [ ] All quotes verified against source
- [ ] "Own work" claims clearly marked with status
- [ ] Hypotheses distinguished from verified claims
- [ ] No "demonstrates" or "shows" for EMERGING or SPECULATIVE claims

### ARGUMENTs
- [ ] Each ARGUMENT has its warrant stated explicitly (not left implicit)
- [ ] Grounds are verified CLAIMs in the registry (not unregistered assertions)
- [ ] Qualifier matches the weakest evidence in the chain
- [ ] Strongest counter-arguments acknowledged (not strawmen)
- [ ] No ARGUMENT grounded solely in SPECULATIVE claims without flagging

### PROPOSITIONs
- [ ] Each PROPOSITION has boundary conditions stated
- [ ] Key constructs are defined (not assumed)
- [ ] Reasoning is explicit (not "it follows that..." without warrant)
- [ ] Alternative explanations engaged with
- [ ] Scope not overgeneralized beyond what the arguments support

### General
- [ ] Nuances and contradictions acknowledged
- [ ] Discussion/Conclusion entries use the prose patterns (grounds → warrant → qualifier → conclusion → rebuttal)
- [ ] All entries traceable to registry IDs

---

*Created: [date]*
