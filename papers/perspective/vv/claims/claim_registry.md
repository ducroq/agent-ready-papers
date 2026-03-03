# Claim Registry

<!-- The paper's verification registry. Every factual claim, argument,
     and proposition tracked here. Most entries are CLAIMs (default).
     Use ARGUMENT for reasoning chains combining evidence + inference.
     Use PROPOSITION for novel contributions and recommendations.
     Update this living document throughout the writing process. -->

**Paper:** The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines Beyond Citation Checking
**Last Updated:** 2026-03-03 (all 18 entries drafted into manuscript.tex)
**Thesis:** The scholarly community lacks verification infrastructure for non-empirical papers written with AI assistance; we propose typed verification (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists.

---

## Coverage Summary

| Priority | Total | Drafted | Verified | Needs Evidence | Coverage |
|----------|-------|---------|----------|----------------|----------|
| P0 | 8 | 8 | 0 | 8 | 0% |
| P1 | 9 | 9 | 0 | 9 | 0% |
| P2 | 1 | 1 | 0 | 1 | 0% |
| **Total** | **18** | **18** | **0** | **18** | **0%** |

**Type distribution:** 15 CLAIMs, 2 ARGUMENTs, 1 PROPOSITION
**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2

---

## Priority Guide

### P0 (Critical) — paper fails without these

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S1-1 | AI citation hallucination is a distinct failure mode | Core problem statement collapses |
| S1-2 | Confidence inflation — agents use "demonstrates" for speculative claims | Loses key distinction from citation checkers |
| S1-4 | Existing solutions operate at model/tool level, not process level | Loses the niche for the proposal |
| S2-1 | EQUATOR maintains ~500 reporting guidelines for empirical research | Central landscape claim — entire gap argument depends on this |
| S2-2 | No guidelines exist for non-empirical papers | The gap claim — paper has no reason to exist without it |
| S3-4 | Claims, arguments, and propositions require fundamentally different verification | Central interpretive claim — the paper's core insight |
| S4-1 | Proposition paper audit: 76% coverage, 100% P0, with retyping revealing false failures | Primary evidence for practical applicability |
| S5-1 | The scholarly community needs verification infrastructure for non-empirical papers | Core recommendation — paper has no purpose without it |

### P1 (Important) — target 90%

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S1-3 | Scope creep without architectural constraints | Weakens problem framing |
| S2-3 | Gregor's 5 theory types include 2 that are fundamentally non-empirical | Weakens theoretical grounding |
| S2-4 | Argument quality is the primary verification challenge for non-empirical papers | Weakens the pivot from facts to arguments |
| S3-1 | Toulmin framework provides operationalizable argument verification | Weakens proposal's theoretical basis |
| S3-2 | Whetten framework provides operationalizable proposition verification | Weakens proposal's theoretical basis |
| S3-3 | Confidence tiers enable systematic language calibration | Weakens proposal's practical value |
| S4-2 | Technology paper audit: 6/22 entries using over-confident language | Weakens evidence from second project |
| S4-3 | Structured verification + LLM outperforms LLM alone | Weakens external validation |
| S4-4 | Three audits demonstrate practical applicability across paper types | Weakens cross-project evidence |

### P2 (Supporting) — target 70%

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S5-2 | Next steps: discipline-specific templates, integration with AI tools, empirical validation | Minor — forward-looking, low risk |

---

## Registry by Section

### Section 1: The Problem (AI failure modes)

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S1-1 | AI citation hallucination is a distinct failure mode — agents invent plausible-sounding papers, authors, and DOIs that can survive multiple review rounds undetected | CLAIM | P0 | EMERGING | literature/sources/liang-2024.md; README.md "The Core Problem" | A + F | [~] |
| S1-2 | AI agents exhibit confidence inflation — stating speculative claims with the same certainty as verified facts, using "demonstrates" where "suggests" is appropriate | CLAIM | P0 | EMERGING | audits/technology-paper-retrofit.md §4 (6/22 entries over-confident); README.md "The Core Problem" | E + F | [~] |
| S1-3 | Without architectural constraints (page budgets, section specifications), AI agents expand arguments beyond evidence, add unnecessary sections, and exceed page budgets | CLAIM | P1 | EMERGING | README.md "Architecture Blueprints"; audits/technology-paper-retrofit.md §2 G2 | E + F | [~] |
| S1-4 | Existing solutions (citation checkers like RefChecker/scite.ai, model-level RAG/grounded generation) operate at model or tool level; no process-level verification infrastructure exists for academic writing | CLAIM | P0 | EMERGING | README.md "The Core Problem" paragraph 2; literature/sources/equator-gap.md | F | [~] |

### Section 2: The Landscape Gap

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S2-1 | EQUATOR Network maintains ~500 reporting guidelines for empirical health research (CONSORT for RCTs, STROBE for observational, PRISMA for reviews, etc.) | CLAIM | P0 | EMERGING | literature/sources/equator-gap.md; EQUATOR Network website | D | [~] |
| S2-2 | No EQUATOR or equivalent guidelines exist for non-empirical paper types (theoretical, design science, perspective, methodological) | CLAIM | P0 | EMERGING | literature/sources/equator-gap.md "Key Findings" | D + F | [~] |
| S2-3 | Gregor's (2006) five theory types include Type I (analytic) and Type V (design & action) that are fundamentally non-empirical — their contributions cannot be verified against sources because they ARE the new contribution | CLAIM | P1 | EMERGING | literature/sources/gregor-2006.md | A | [~] |
| S2-4 | For non-empirical papers, argument quality — warrant validity, reasoning coherence, boundary conditions — is the primary verification challenge, not factual accuracy | CLAIM | P1 | EMERGING | literature/sources/toulmin-1958.md "Relevance to DR-004"; literature/sources/whetten-1989.md "Relevance to DR-004" | C + A | [~] |

### Section 3: The Proposal (typed verification)

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S3-1 | Toulmin's (1958/2003) argument model — claim, grounds, warrant, qualifier, rebuttal — provides an operationalizable framework for verifying argument quality in academic writing | CLAIM | P1 | EMERGING | literature/sources/toulmin-1958.md; Gupta et al. 2024 (ACL) demonstrates LLM-based Toulmin extraction | C + A | [~] |
| S3-2 | Whetten's (1989) What/How/Why/Who-Where-When framework provides an operationalizable structure for verifying propositions by checking construct definition, relationship clarity, reasoning explicitness, and boundary conditions | CLAIM | P1 | EMERGING | literature/sources/whetten-1989.md | A | [~] |
| S3-3 | Mapping confidence tiers (ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE) to prescribed language ("demonstrates" vs "suggests" vs "may" vs "warrants investigation") enables systematic calibration of claim strength to evidence strength | CLAIM | P1 | EMERGING | README.md "Confidence-to-Language Mapping"; templates/writing-guide.md "Language Calibration" | E | [~] |
| S3-4 | Claims, arguments, and propositions require fundamentally different verification procedures: source checking for CLAIMs, Toulmin analysis for ARGUMENTs, and Whetten analysis for PROPOSITIONs — applying the wrong procedure produces false failures | ARGUMENT | P0 | EMERGING | audits/proposition-retrofit.md §3 (H4 false failure); audits/proposition-retrofit.md §5.1 "What the Framework Would Have Caught" | E | [~] |

**S3-4 warrant:** If entry H4 in the Proposition audit was scored SPECULATIVE (0.25) because it was evaluated as a source-backed claim, but its three premises are independently verified and its warrant is logically valid (Toulmin 4/5), then the low score was a false failure caused by applying the wrong verification procedure. The correct procedure (Toulmin checklist) reveals an EMERGING argument with strong grounds. This demonstrates that type-specific verification is not merely useful but necessary — wrong-type verification systematically misclassifies entries.

### Section 4: Preliminary Evidence

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S4-1 | Proposition paper retrofit audit achieved 76% overall coverage and 100% P0 coverage; retyping 21 entries revealed 2 ARGUMENTs and 3 PROPOSITIONs previously misclassified as CLAIMs, including a false failure (H4: scored 0.25 as CLAIM, earned EMERGING as ARGUMENT) | CLAIM | P0 | EMERGING | audits/proposition-retrofit.md §1 (coverage), §3 (retyping summary), §3 Example A (H4 false failure) | E | [~] |
| S4-2 | Technology paper retrofit audit extracted 22 claims from paper text; confidence tier assignment revealed 6 entries where the paper uses language more confident than the evidence warrants (e.g., "demonstrates" for single-unit findings) | CLAIM | P1 | EMERGING | audits/technology-paper-retrofit.md §4 "Language Calibration Impact" (6 entries need recalibration) | E | [~] |
| S4-3 | Structured verification infrastructure combined with LLM capability outperforms LLM capability alone — demonstrated for peer review aggregation (PeerArg 2024) and argument extraction (Gupta et al. 2024) | CLAIM | P1 | EMERGING | literature/sources/peerarg-2024.md; literature/sources/gupta-2024.md | A | [~] |
| S4-4 | Three retrofit audits across different paper types (empirical/technology, perspective/proposition, measurement/engineering fidelity) demonstrate that the typed verification framework is practically applicable and reveals actionable issues in each project | ARGUMENT | P1 | EMERGING | audits/proposition-retrofit.md; audits/technology-paper-retrofit.md; audits/engineering-fidelity-retrofit.md | E | [~] |

**S4-4 warrant:** If the framework's typed registry and verification checklists were applied retrospectively to three independent paper projects across different types and venues, and in each case the analysis identified actionable issues (mistyped entries, over-confident language, missing boundary conditions) that were invisible without the framework, then the framework has demonstrated practical applicability across paper types. The limitation is that all three projects share the same author team and domain cluster — generalizability to other authors and domains is not established.

### Section 5: Call to Action

| ID | Statement | Type | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|------|----------|------------|--------|-------------|--------|
| S5-1 | The scholarly community needs verification infrastructure for non-empirical papers — analogous to what EQUATOR provides for empirical research — to maintain academic integrity in the age of AI-augmented writing | PROPOSITION | P0 | EMERGING | Synthesis of S2-1 through S2-4 (landscape gap) + S3-4 (different types need different verification) + S4-1 through S4-4 (preliminary evidence of applicability) | F | [~] |
| S5-2 | Next steps include: discipline-specific verification templates beyond the medical/engineering domains tested here, integration with AI writing tools as structured prompting infrastructure, and empirical validation comparing verification-assisted vs unassisted AI writing quality | CLAIM | P2 | SPECULATIVE | Logical inference from current framework state and limitations | F | [~] |

**S5-1 premises:** S2-1 (EQUATOR exists for empirical), S2-2 (nothing for non-empirical), S3-4 (types need different verification), S4-1–S4-4 (preliminary evidence works).
**S5-1 reasoning:** If empirical research benefits from ~500 reporting guidelines (EQUATOR), and non-empirical research has zero equivalent infrastructure, and AI writing amplifies the verification challenge for non-empirical papers (where argument quality matters more than factual accuracy), and preliminary evidence shows typed verification reveals actionable issues, then extending verification infrastructure to non-empirical papers is a legitimate and urgent need.
**S5-1 boundary conditions:** Applies to academic papers intended for peer-reviewed publication. Does not apply to: informal writing, journalism, creative writing, or papers where the verification infrastructure cost exceeds the benefit (e.g., very short opinion pieces). The specific checklists (Toulmin, Whetten) are grounded in Western academic argumentation traditions and may need adaptation for other scholarly traditions.

---

## Source Verification Checklist

### Literature Sources

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| EQUATOR Network website | S2-1, S2-2 | Verify ~500 count; confirm no non-empirical guidelines | [ ] |
| Gregor 2006 (MIS Quarterly) | S2-3 | Verify 5 types; confirm Type I and V are non-empirical | [ ] |
| Toulmin 1958/2003 | S3-1 | Verify 6 components; confirm operationalizability claims | [ ] |
| Whetten 1989 (AMR) | S3-2 | Verify What/How/Why/When framework | [ ] |
| Gupta et al. 2024 (ACL) | S3-1, S4-3 | Verify Toulmin-based LLM prompting outperforms generic | [ ] |
| PeerArg 2024 (LREC-COLING) | S4-3 | Verify structured + LLM > LLM alone finding | [ ] |
| Liang et al. 2024 | S1-1 | Verify AI citation hallucination evidence | [ ] |

### Own Data

| Data Source | Claims | What to Check |
|-------------|--------|---------------|
| Proposition paper retrofit audit | S4-1, S3-4 | Audit file exists; 76% coverage verified; H4 false failure documented |
| Technology paper retrofit audit | S4-2 | Audit file exists; 6/22 over-confident language documented |
| Engineering fidelity retrofit audit | S4-4 | Audit file exists; issues documented |

### Own Work (Under Review)

| Paper | Claims | Venue | Status |
|-------|--------|-------|--------|
| Technology paper (IEEE TIM) | S4-2 source data | IEEE TIM | Under review |
| Proposition paper | S4-1 source data | TBD | In preparation |

---

## Out of Scope

<!-- Claims verified but excluded (preserve for future reference) -->

| ID | Claim | Source | Why Excluded |
|----|-------|--------|-------------|
| — | — | — | No exclusions yet |

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
statistical power, reproducibility, calibration), not source count.

### Special Cases: Reference Claims

CLAIMs that are verifiable facts about external documents — e.g., "EQUATOR maintains ~500
guidelines" or "Gregor identifies five theory types" — should use **ESTABLISHED** when the
source is publicly accessible and the statement is a direct, verifiable reference. These
are not evidence-dependent claims requiring confidence assessment; they are facts about
what a document says. If the document exists and says this, the claim is verified.

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
- Contradictory sources must be acknowledged in the text
- Claims >10 years old need a recency check
- Own work under review must be explicitly flagged

---

*Registry created: 2026-03-03*
