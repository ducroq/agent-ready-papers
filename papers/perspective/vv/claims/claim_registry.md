# Claim Registry

<!-- The paper's verification registry. Every factual claim, argument,
     and proposition tracked here. Most entries are CLAIMs (default).
     Use ARGUMENT for reasoning chains combining evidence + inference.
     Use PROPOSITION for novel contributions and recommendations.
     Update this living document throughout the writing process. -->

**Paper:** The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines Beyond Citation Checking
**Last Updated:** 2026-09-24 (eight Confidence tiers corrected to DR-002 criteria — S1-1, S1-2, S2-2, S2-3, S2-4, S3-1, S3-2, S4-3, each with a ⚠️ note; manuscript anchors and appendix table now agree with the registry); 2026-03-03 (P0 + P1 + P2 verification complete; 100% overall coverage)
**Thesis:** The scholarly community lacks verification infrastructure for non-empirical papers written with AI assistance; we propose typed verification (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists.

---

## Coverage Summary

**Coverage by Priority**

| Priority | Total | Drafted | Verified | Needs Evidence | Coverage |
|----------|-------|---------|----------|----------------|----------|
| P0 | 6 | 6 | 6 | 0 | 100% |
| P1 | 9 | 9 | 9 | 0 | 100% |
| P2 | 1 | 1 | 1 | 0 | 100% |
| **Total** | **16** | **16** | **16** | **0** | **100%** |

**Coverage by Type**

| Type | Total | Verified | Coverage |
|------|-------|----------|----------|
| CLAIM | 14 | 14 | 100% |
| ARGUMENT | 1 | 1 | 100% |
| PROPOSITION | 1 | 1 | 100% |
| **Total** | **16** | **16** | **100%** |

⚠️ **P0 tier floor (2026-09-24; S4-1 withdrawn and S1-4 moved to P1, 2026-09-26): 4 of 6 P0 entries are below SUPPORTED** (S1-2, S2-2, S3-4, S5-1; S2-1 and S1-1 meet it). **The P0 gate therefore fails.** DR-002 (Accepted, binding) sets it as "all SUPPORTED or ESTABLISHED (no EMERGING/SPECULATIVE)" with no exception; the "or explicitly framed as hypothesis" clause in `papers/perspective/writing-guide.md`'s checklist is not in DR-002 and cannot waive it. Remedies are stronger sources, re-prioritisation, or an explicit decision — not a reading of the exception. The 100% figures below are *verification coverage* (Status column), not tier. `tools.coverage` reports the floor separately, below its coverage table (it reports 2 of 6 meeting it), and `--strict` fails on it (added in 75f928c, #37).

**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2. Every registered ARGUMENT and PROPOSITION is `[x]` per the type-conditional Gate 2 expectation.

---

## Priority Guide

### P0 (Critical) — paper fails without these

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S1-1 | AI citation hallucination is a distinct failure mode | Core problem statement collapses |
| S1-2 | Confidence inflation — agents use "demonstrates" for speculative claims | Loses key distinction from citation checkers |
| S2-1 | EQUATOR maintains ~700 reporting guidelines for empirical research | Central landscape claim — entire gap argument depends on this |
| S2-2 | No guidelines exist for non-empirical papers | The gap claim — paper has no reason to exist without it |
| S3-4 | Claims, arguments, and propositions require fundamentally different verification | Central interpretive claim — the paper's core insight |
| S5-1 | The scholarly community needs verification infrastructure for non-empirical papers | Core recommendation — paper has no purpose without it |

### P1 (Important) — target 90%

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S1-3 | Scope creep without architectural constraints | Weakens problem framing |
| S1-4 | No existing infrastructure applies a verification procedure per unit type (P0 → P1 2026-09-26) | Weakens positioning; prior art L60/L61/L66 must be engaged either way |
| S1-5 | AI-generated equations contain arithmetic errors surviving plausibility review | Weakens breadth of problem framing beyond non-empirical |
| S2-3 | Gregor's 5 theory types include 2 that are fundamentally non-empirical | Weakens theoretical grounding |
| S2-4 | Argument quality is the primary verification challenge for non-empirical papers | Weakens the pivot from facts to arguments |
| S3-1 | Toulmin framework provides operationalizable argument verification | Weakens proposal's theoretical basis |
| S3-2 | Whetten framework provides operationalizable proposition verification | Weakens proposal's theoretical basis |
| S3-3 | Confidence tiers enable systematic language calibration | Weakens proposal's practical value |
| S4-3 | Structured verification + LLM outperforms LLM alone | Weakens external validation |

### P2 (Supporting) — target 70%

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S5-2 | Next steps: discipline-specific templates, integration with AI tools, empirical validation | Minor — forward-looking, low risk |

---

## Registry by Section

Each section uses per-type sub-tables (one each for CLAIMs / ARGUMENTs / PROPOSITIONs as applicable). IDs are `S<section>-<number>` and are unique within a section across all sub-tables. Grounds/premises references resolve by `Ctrl-F` within the section.

### Section 1: The Problem (AI failure modes)

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S1-1 | AI citation hallucination is a distinct failure mode — LLMs invent plausible-sounding papers, authors, and DOIs at substantial rates (lower for GPT-4 than GPT-3.5 in the one study comparing them) | P0 | SUPPORTED | Mugaanyi et al. 2024 (JMIR, DOI: 10.2196/52935): 62–89% DOI fabrication rates across disciplines. Walters & Wilder 2023 (Sci Rep 13:14045, DOI: 10.1038/s41598-023-41032-5, full text read 2026-09-26): 55% of GPT-3.5 and 18% of GPT-4 citations fabricated across 636 citations in 84 generated literature reviews. ⚠️ **Tier raised 2026-09-26 (EMERGING → SUPPORTED):** two agreeing peer-reviewed sources meet DR-002. The unmeasured clause "can survive multiple review rounds undetected" was dropped from the statement. Bhattacharyya 2023 (Cureus) and Chelli 2024 (JMIR) also agree, but only their abstracts have been read; add them after a full-text read. | A | [x] |
| S1-2 | AI agents exhibit confidence inflation — stating speculative claims with the same certainty as verified facts, using "demonstrates" where "suggests" is appropriate | P0 | EMERGING | Liang et al. 2024 (NEJM AI): LLMs catch surface issues, struggle with deep argument analysis ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** Liang et al. find LLM *review feedback* misses deep argument problems; that does not show AI *writing* states speculative claims with verified-fact certainty, which is this row's claim. The manuscript hedges it ("may state") and always did — its anchor said EMERGING since the first draft. Below the P0 SUPPORTED floor — see the P0 tier-floor line in the header; a source measuring expressed confidence would lift it. | A | [x] |
| S1-3 | Without architectural constraints (page budgets, section specifications), AI agents expand arguments beyond evidence, add unnecessary sections, and exceed page budgets | P1 | EMERGING | README.md "Architecture Blueprints"; hedged with "may" | F | [x] |
| S1-4 | Existing verification infrastructure for AI-assisted writing — citation and consistency linters, claim–evidence adjudication, provenance disciplines — checks whether evidence exists, supports or suffices, and some of it audits language against empirical study design; to our knowledge none distinguishes claims from arguments and propositions and applies a procedure suited to each, and none targets papers whose contribution is reasoning rather than fact | P1 | EMERGING | L66 Samsonau 2026 (arXiv:2604.08501): 23-check manuscript linter incl. causal-language-vs-design and citation-purpose checks, experimental claim-typing by type/testability/scope; no warrant analysis or per-kind procedure; calibrated on empirical papers only. L60 Chen et al. 2026 (arXiv:2607.26512): four support relations routed back to the author; no warrant, calibration or boundary check. L61 Zhou & Yu 2026 (arXiv:2608.10858): provenance discipline with a claim–evidence index and a sampled sufficiency audit; standing tiers attach to its metrics, not to manuscript claims. Adjacent: L62 WarrantScore scores warrants in peer-review comments, not manuscripts. All three read in full 2026-09-26. ⚠️ **Reworded and P0 → P1 2026-09-26:** the earlier "no process-level verification infrastructure exists" is falsified by L60, L61 and L66. As a positioning claim the paper does not collapse without it (its case rests on S2-2, S3-4 and S5-1). It remains a hedged negative, so it stays EMERGING. | B | [x] |
| S1-5 | AI-generated equations can contain arithmetic errors that survive plausibility review but are caught by mechanical numerical reproduction | P1 | EMERGING | Internal experiments comparing LLM reviews prompted to "assess soundness" vs LLM reviews prompted to "numerically reproduce every calculation" show systematic difference in error detection. | F | [x] |

### Section 2: The Landscape Gap

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S2-1 | EQUATOR Network maintains ~700 reporting guidelines for empirical health research (CONSORT for RCTs, STROBE for observational, PRISMA for reviews, etc.) | P0 | ESTABLISHED | EQUATOR Network website (equator-network.org, accessed 2026-03-03): 699 guidelines displayed. Reference claim — verifiable fact about external database. | D | [x] |
| S2-2 | No EQUATOR or equivalent guidelines exist for non-empirical paper types (theoretical, design science, perspective, methodological) | P0 | EMERGING | EQUATOR Network database (accessed 2026-03-03): all 699 guidelines address empirical research types; search for theoretical/design science/perspective returns no results. Reference claim — verifiable by searching the database. ⚠️ **Tier corrected 2026-09-24 (ESTABLISHED → EMERGING):** one database search, covering EQUATOR only; the "or equivalent" half was not searched, and an absence claim is not a reference claim (a direct statement of what a document says). DR-002: 1–2 sources is EMERGING. The manuscript qualifies it "to our knowledge". Below the P0 SUPPORTED floor. | D | [x] |
| S2-3 | Gregor's (2006) five theory types include Type I (analytic) and Type V (design & action) that are fundamentally non-empirical — their contributions cannot be verified against sources because they ARE the new contribution | P1 | EMERGING | Gregor 2006 (MIS Quarterly, DOI: 10.2307/25148742): Types I–V confirmed; Type I (analytic) and Type V (design) are non-empirical in contribution. Reference claim — verifiable fact about Gregor's taxonomy. ⚠️ **Tier corrected 2026-09-24 (ESTABLISHED → EMERGING):** that Gregor defines five types is a reference claim, but this row's statement — Types I and V "cannot be verified against sources because they ARE the new contribution" — is our interpretation, which the reference-claim exception in `templates/claim-registry.md` excludes. Candidate for a split: the taxonomy half would be ESTABLISHED. | A | [x] |
| S2-4 | For non-empirical papers, argument quality — warrant validity, reasoning coherence, boundary conditions — is the primary verification challenge, not factual accuracy | P1 | EMERGING | Toulmin (1958/2003): warrants are the inferential bridge; Whetten (1989): "Why" is most critical and most often missing. Both support argument quality over source checking for non-empirical contributions. ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** Toulmin and Whetten describe argument and theory structure; that argument quality is the *primary* challenge for non-empirical papers is our inference from them, not their finding. The manuscript hedges it ("may not be"). | C; A | [x] |

### Section 3: The Proposal (typed verification)

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S3-1 | Toulmin's (1958/2003) argument model — claim, grounds, warrant, qualifier, rebuttal — provides an operationalizable framework for verifying argument quality in academic writing | P1 | EMERGING | Toulmin (1958/2003): 6 components confirmed (claim, grounds, warrant, backing, qualifier, rebuttal). Gupta et al. 2024 (ACL, DOI: 10.18653/v1/2024.acl-long.552): LLM zero-shot Toulmin extraction outperforms generic prompts — reported evidence of technical feasibility (extraction, not verification). ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** Gupta et al. show Toulmin-guided *extraction*, not verification; operationalising verification is this paper's proposal. The manuscript hedges it ("may provide a basis"). | C; A | [x] |
| S3-2 | Whetten's (1989) What/How/Why/Who-Where-When framework provides an operationalizable structure for verifying propositions by checking construct definition, relationship clarity, reasoning explicitness, and boundary conditions | P1 | EMERGING | Whetten 1989 (AMR, DOI: 10.5465/amr.1989.4308371): 4 components confirmed (What/How/Why/Who-Where-When). "Why" identified as most critical and most often missing. Operationalization was reported in own Whetten checklists (proposition audit §3, Examples C and D — see note). ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** the "proposition audit §3" cited here is no longer in the repository — `audits/` was purged from history in the v2.0.0 scrub and has been gitignored since `1d8c68c` (2026-06-10) — so the operationalisation evidence cannot be checked; what remains is Whetten's framework itself. Open: the manuscript states this one unhedged ("Propositions can be evaluated…"). | A; E | [x] |
| S3-3 | Mapping confidence tiers (ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE) to prescribed language ("demonstrates" vs "suggests" vs "may" vs "warrants investigation") enables systematic calibration of claim strength to evidence strength | P1 | EMERGING | Own proposal (this paper's contribution). Supporting evidence: technology audit §4 found 6/22 entries with over-confident language that the tier system would have caught. Framed with "may enable" in manuscript. ⚠️ **Noted 2026-09-24:** the "technology audit §4" is no longer in the repository (purged in the v2.0.0 scrub; `audits/` gitignored since `1d8c68c`), so the 6/22 figure cannot be re-checked. Tier unchanged — EMERGING already rests on the proposal itself. | E | [x] |

**ARGUMENTs** (Toulmin):

| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Source | Source Tier | Status |
|----|-----------|----------|------------|---------|---------|----------|--------|-------------|--------|
| S3-4 | Claims, arguments, and propositions require fundamentally different verification procedures: source checking for CLAIMs, Toulmin analysis for ARGUMENTs, and Whetten analysis for PROPOSITIONs — applying the wrong procedure produces false failures | P0 | EMERGING | S3-1; S3-2; S3-3 | If an entry is scored low-confidence because it is evaluated as a source-backed CLAIM but its three premises are independently verified and its warrant is logically valid, then the low score is a false failure caused by applying the wrong verification procedure. This demonstrates that type-specific verification is not merely useful but necessary. | Limitation acknowledged: cross-author replication not yet demonstrated. | Own design rationale. | F | [x] |

### Section 4: Related Work and Design Rationale

**Withdrawn 2026-09-26 ([#38](https://github.com/ducroq/agent-ready-papers/issues/38)): S4-1, S4-2 and S4-4.** Their prose was removed deliberately in `1d8c68c` ("strip evidence claims"), and each was sourced only to own design rationale (tier F), so nothing in the manuscript still asserts them. S5-1 is re-grounded on S2-1, S2-2 and S3-4. The IDs are retired, not reused. The rows are in git history.

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S4-3 | Structured verification infrastructure combined with LLM capability outperforms LLM capability alone — reported for peer review aggregation (PeerArg 2024) and argument extraction (Gupta et al. 2024) | P1 | EMERGING | PeerArg (NeLaMKRR@KR 2024, arXiv:2409.16813): "a variant of PeerArg outperforms end-to-end LLM baseline." Gupta (ACL 2024): Toulmin-based prompts outperform generic prompts. Both confirmed via content verification. ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** both sources are real and say what is quoted, but each covers one narrow task (review aggregation; argument extraction); the general "structured + LLM outperforms LLM alone" is our extrapolation. The manuscript hedges it ("may outperform"). | A | [x] |

### Section 5: Call to Action

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S5-2 | Next steps include: discipline-specific verification templates beyond the medical/engineering domains tested here, integration with AI writing tools as structured prompting infrastructure, and empirical validation comparing verification-assisted vs unassisted AI writing quality | P2 | SPECULATIVE | Logical inference from current framework state and limitations. (1) Templates: follows from §4's opening (evaluation across projects, authors and domains still needed) and §5's limited-domain statement. (2) AI integration: follows from process-level argument + Gupta 2024 feasibility. (3) Empirical validation: follows from §4's closing "open empirical question". Manuscript language ("warrant investigation") matches SPECULATIVE tier. | F | [x] |

**PROPOSITIONs** (Whetten):

| ID | Statement | Priority | Confidence | Constructs | Relationship | Premises | Reasoning | Boundary conditions | Alternatives engaged | Source | Source Tier | Status |
|----|-----------|----------|------------|------------|--------------|----------|-----------|---------------------|----------------------|--------|-------------|--------|
| S5-1 | The scholarly community needs verification infrastructure for non-empirical papers — analogous to what EQUATOR provides for empirical research — to maintain academic integrity in the age of AI-augmented writing | P0 | EMERGING | "verification infrastructure" (process-level reporting + verification scaffolding analogous to EQUATOR guidelines); "non-empirical paper" (Gregor Type I analytic, Type V design, plus perspective and methodological papers); "AI-augmented writing" (drafting and revision assisted by general-purpose LLMs) | Non-empirical paper publishing requires verification infrastructure (analogous to EQUATOR for empirical work) to remain trustworthy under AI augmentation | S2-1; S2-2; S3-4 | If empirical research benefits from ~700 reporting guidelines (EQUATOR), and non-empirical research has zero equivalent infrastructure, and AI writing amplifies the verification challenge for non-empirical papers (where argument quality matters more than factual accuracy), and claims, arguments and propositions each need their own verification procedure (S3-4), then extending verification infrastructure to non-empirical papers is a legitimate and urgent need. | Applies to academic papers intended for peer-reviewed publication. Does not apply to: informal writing, journalism, creative writing, or papers where the verification infrastructure cost exceeds the benefit (e.g., very short opinion pieces). The specific checklists (Toulmin, Whetten) are grounded in Western academic argumentation traditions and may need adaptation for other scholarly traditions. | Peer review counter-argument engaged in manuscript: peer review already polices argument quality. Response: peer review is end-stage and reviewer-dependent; reporting guidelines provide pre-submission structural checks complementary to (not replacing) peer review. | S2-1 [x], S2-2 [x], S3-4 [x] — all premises verified within this registry | F | [x] |

---

## Source Verification Checklist

### Literature Sources

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| EQUATOR Network website | S2-1, S2-2 | Verified: 699 guidelines (2026-03-03); all empirical; no non-empirical guidelines found | [x] |
| Gregor 2006 (MIS Quarterly) | S2-3 | Verified: 5 types; Type I (analytic) and Type V (design) are non-empirical in contribution; DOI 10.2307/25148742 | [x] |
| Toulmin 1958/2003 | S3-1 | Verified: 6 components (claim, grounds, warrant, backing, qualifier, rebuttal); ISBN 978-0-521-53483-3 | [x] |
| Whetten 1989 (AMR) | S3-2 | Verified: What/How/Why/Who-Where-When; DOI 10.5465/amr.1989.4308371 | [x] |
| Gupta et al. 2024 (ACL) | S3-1, S4-3 | Verified: Toulmin-based zero-shot prompting outperforms generic; DOI 10.18653/v1/2024.acl-long.552 | [x] |
| PeerArg 2024 (NeLaMKRR@KR) | S4-3 | Verified: PeerArg outperforms end-to-end LLM baseline; arXiv:2409.16813 | [x] |
| Mugaanyi et al. 2024 (JMIR) | S1-1 | Verified: 62–89% DOI fabrication rates; DOI 10.2196/52935 | [x] |
| Walters & Wilder 2023 (Sci Rep) | S1-1 | Verified 2026-09-26 (Crossref + full text): 55% GPT-3.5 / 18% GPT-4 citations fabricated; DOI 10.1038/s41598-023-41032-5 | [x] |
| Liang et al. 2024 (NEJM AI) | S1-2 | Verified: LLMs catch surface issues but struggle with deep argument analysis; DOI 10.1056/AIoa2400196 | [x] |
| Liang et al. 2025 (Nat Hum Behav) | S1 (opening) | Verified: up to 22% of CS papers show LLM modification; DOI 10.1038/s41562-025-02273-8 | [x] |
| Turner et al. 2012 (Cochrane) | S2, S5 | Verified: 25/27 CONSORT items favoured endorsing journals, 5 significant; DOI 10.1002/14651858.MR000030.pub2 | [x] |
| Glasziou et al. 2014 (Lancet) | S2, S5 | Verified: incomplete reporting contributes to research waste; DOI 10.1016/S0140-6736(13)62228-X | [x] |
| Peffers et al. 2007 (JMIS) | S2 | Verified: DSR process model (6 activities); DOI 10.2753/MIS0742-1222240302 | [x] |

### Own Design Rationale

| Source | Claims |
|--------|--------|
| Framework design rationale; misclassification mechanism described in S3-4 | S3-4 |

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
2. Are the grounds (evidence) verified CLAIMs in this registry?
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
4. Are boundary conditions specified? Check quality:
   - [ ] Not **tautological** — boundary condition is specific, not restating the proposition
   - [ ] Not a **moving target** — boundary condition is stable, not unfalsifiable
   - [ ] Not **overgeneralized** — boundary condition is bounded, not open-ended
5. Does it engage with alternative explanations?

After completing the Whetten checklist, evaluate falsifiability:
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the proposition (not circular)
- [ ] Criterion is specific enough to be measurable
- [ ] Criterion is not a moving target

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

CLAIMs that are verifiable facts about external documents — e.g., "EQUATOR maintains ~700
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
