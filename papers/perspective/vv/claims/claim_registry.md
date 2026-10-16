# Claim Registry

<!-- Paper 1's verification registry, in the DR-027 schema (migrated 2026-10-16 from the DR-004
     registry; that version is frozen at tests/fixtures/dr004/paper1-v4-registry.md and in git
     history). Terms: docs/glossary.md. Each claim records what it says and what it rests on;
     the checks follow the grounds. Coverage and the P0 floor come from `make coverage`, not
     from hand-kept tables. -->

**Paper:** The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing (draft 2)
**Last Updated:** 2026-10-16: migrated to the DR-027 schema; rows rewritten and added for draft 2 (S1-3 withdrawn; S1-4, S2-2, S3-3, S3-4 rewritten; S2-3 split; S1-7, S3-5, S3-6, S4-5 and D1–D8 added; S5-1 became contribution C1). Tiers set conservatively after a Step Z check: claims that report what a single document says are SUPPORTED, not ESTABLISHED (the reference-claim exception below is not used in draft 2, whose Table 1 does not state it). Rows marked `[ ]` were written in the 2026-10-16 session and await checking in a later session.
**Thesis:** AI-assisted non-empirical papers need their reasoning checked, not only their citations; Toulmin and Whetten supply the vocabulary: register each claim with what it rests on, check each item by its kind, and check the contribution once.

**P0 tier floor (`make coverage`, 2026-10-16): 3 of 6 P0 entries meet it; below: C1, S2-2, S3-4.** The paper states this in its appendix.

---

## Contributions

**Contributions:**

| ID | Contribution | Says | Rests on | What | How | Why | Who/Where/When | Objections engaged | Priority | Confidence tier | Status |
|----|--------------|------|----------|------|-----|-----|----------------|--------------------|----------|-----------------|--------|
| C1 | The scholarly community needs verification infrastructure for non-empirical papers — analogous to what EQUATOR provides for empirical research — to maintain academic integrity in the age of AI-augmented writing | normative | claim: S1-7; claim: S2-1; claim: S2-2; claim: S3-4; decl: D1; decl: D2; decl: D3; decl: D4 | Verification infrastructure, non-empirical papers, AI-augmented writing (D2–D4) | Non-empirical paper publishing requires verification infrastructure to remain trustworthy under AI augmentation | If empirical research benefits from ~700 reporting guidelines, and non-empirical research has no consensus-based equivalent, and AI writing amplifies the verification challenge for non-empirical papers, and each kind of claim needs its own check (S3-4), then extending verification infrastructure to non-empirical papers is a legitimate and urgent need | Academic papers whose contribution is an argument, and the interpretive parts of empirical papers. Other writing that asks readers to trust its reasoning, such as journalism, untested. Frameworks from Western academic traditions | Peer review already polices argument quality. Response: peer review is end-stage and reviewer-dependent; reporting guidelines add pre-submission structural checks | P0 | EMERGING | [x] |

## Declared starting points

**Declared starting points:**

| ID | Statement | Kind | Contestedness | Status |
|----|-----------|------|---------------|--------|
| D1 | Published reasoning should be checkable: readers and reviewers should be able to see what each claim rests on | value | accepted in the field | [x] |
| D2 | "Verification infrastructure": process-level reporting plus verification scaffolding analogous to EQUATOR guidelines | definition | own | [x] |
| D3 | "Non-empirical paper": a paper whose main contribution is reasoning rather than new data; theoretical, conceptual, design-science and perspective papers are examples, not a closed list | definition | own | [x] |
| D4 | "AI-augmented writing": drafting and revision assisted by general-purpose LLMs | definition | accepted in the field | [x] |

## Claims by section

### Section 1: The Problem

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S1-1 | AI citation hallucination is a distinct failure mode — LLMs invent plausible-sounding papers, authors, and DOIs at substantial rates (lower for GPT-4 than GPT-3.5 in the one study comparing them) | descriptive | src: Mugaanyi et al. 2024; src: Walters & Wilder 2023 | | | | | P0 | SUPPORTED | A; A | [x] |
| S1-2 | AI writing assistants may express more certainty than the evidence warrants: LLMs verbalise overconfidence and overgeneralise scientific findings; whether this extends to boosters in academic prose is unsettled (one abstract corpus finds twice the human rate of boosters and also more hedges) | descriptive | src: Xiong et al. 2024; src: Zhou et al. 2024; src: Peters & Chin-Yee 2025; src: El-Dakhs et al. 2025 | The three studies of LLM output, each on a different task, jointly support the general claim | | Booster clause rests on one study with mixed direction; stated as unsettled | Zou & Fan 2025, Sadigzade 2026 find fewer stance markers (abstract level) | P0 | SUPPORTED | A; A; A; A | [x] |
| S1-4 | Existing tools for AI-assisted writing check whether evidence exists, supports a claim or suffices (one also checks causal wording against study design); none found asks whether a warrant holds for its readers or chooses the check by what a claim rests on | descriptive | src: Samsonau 2026; src: Chen et al. 2026; src: Zhou & Yu 2026; src: VANRA registration | Absence inferred from the closest tools found: each checks evidence, none applies a per-kind procedure | | "To our knowledge": a hedged negative | | P1 | EMERGING | B; B; B; D | [x] |
| S1-5 | In informal trials on the author's projects, prompting a model to recompute every value caught arithmetic errors that prompting it to judge soundness missed | descriptive | own: comparison of model reviews prompted to judge soundness vs to recompute every value, on the author's own projects (2026) |  |  |  |  | P1 | SPECULATIVE |  | [x] |
| S1-6 | AI-text detection is no substitute for verification: detection asks who wrote a text, verification asks whether it holds (definitional). Detectors are fragile: accuracy varies with generation settings, and paraphrase can collapse it | descriptive | decl: D5; src: Dugan et al. 2024; src: Krishna et al. 2023 |  |  | Both test 2023–24 detectors |  | P2 | EMERGING | A; A | [x] |
| S1-7 | AI-assisted prose can be fluent and cite only real sources while its reasoning is weak | descriptive | claim: S1-1; claim: S1-2; claim: S1-4 | Hallucination checks catch false citations; confidence inflation and unchecked warrants pass them, so fluent, well-cited prose can still carry weak reasoning | | | | P1 | EMERGING | | [ ] |

### Section 2: The Landscape Gap

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S2-1 | EQUATOR Network maintains ~700 reporting guidelines for empirical health research (CONSORT for RCTs, STROBE for observational, PRISMA for reviews, etc.) | descriptive | src: EQUATOR website (699 displayed 2026-03-03, 704 on 2026-09-14) |  |  |  |  | P0 | SUPPORTED | D | [x] |
| S2-2 | Guidance for papers without new data exists but is scattered; no consensus checklist was found for verifying the reasoning of non-empirical papers (whether each step from evidence to claim holds) | descriptive | src: EQUATOR searches 2026-03-03, 2026-09-26; src: Jaakkola 2020; src: Larsen et al. 2025; src: Gregor & Hevner 2013; src: Dinter & Krawatzeck 2015; src: Ralph et al. 2020 | Absence inferred from library searches and from gap statements that each cover one paper type | | Design science has two agreeing sources, conceptual one, theoretical and perspective none | Baethge et al. 2019 (SANRA), Nashwan et al. 2026, VANRA: neighbouring types, not counter-examples | P0 | EMERGING | D; A; A; A; A; D | [x] |
| S2-3a | Gregor's (2006) taxonomy has five theory types, including Type I (analytic) and Type V (design and action) | descriptive | src: Gregor 2006 |  |  |  |  | P1 | SUPPORTED | A | [ ] |
| S2-3b | Type I and Type V contributions are largely non-empirical: they may not be checkable against an earlier source, because they are the new contribution | descriptive | claim: S2-3a | Theories that propose rather than report have no prior source to be checked against | | | | P1 | EMERGING | | [ ] |
| S2-4 | For non-empirical papers, argument quality — warrant validity, reasoning coherence, boundary conditions — is the primary verification challenge, not factual accuracy | descriptive | src: Toulmin 2003; src: Whetten 1989 | From "warrants are the inferential bridge" and "Why is most critical and most often missing" to "argument quality is the primary challenge" is our inference | | Hedged in the manuscript ("may not be") | | P1 | EMERGING | C; A | [x] |

### Section 3: The Proposal

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S3-1 | Toulmin's (1958/2003) argument model — claim, grounds, warrant, qualifier, rebuttal — provides an operationalizable framework for verifying argument quality in academic writing | descriptive | src: Toulmin 2003; src: Gupta et al. 2024 | Gupta shows Toulmin-guided extraction; that the layout can drive verification is this paper's extension | | Toulmin's 2003 preface rejects "the Toulmin model" as an analytical model | | P1 | EMERGING | C; A | [x] |
| S3-2 | Whetten's criteria judge a theoretical contribution as a whole, so they may serve as a check of a paper's central contribution, applied once | descriptive | src: Whetten 1989 | Whetten wrote the elements as an editor's test of theory papers; using them to check single propositions is this paper's extension | | | | P1 | EMERGING | A | [x] |
| S3-3 | Mapping confidence tiers to prescribed qualifiers may help authors notice when a sentence claims more than its grounds allow | descriptive | claim: S3-6; decl: D6 | Fixed-wording practice from intelligence analysis, climate assessment and evidence grading is adapted to academic writing; the adaptation is untested | | Tiers counted by sources, not tested with readers | | P1 | EMERGING | | [ ] |
| S3-4 | Each claim needs the checks its grounds call for: a procedure that does not fit what a claim rests on may fail it for the wrong reason (a false failure) | descriptive | claim: S3-1; claim: S3-2; claim: S3-5; own: trial migration of this paper's registry (2026-10-16, docs/work-items/v5-trial) | If a claim is checked by a procedure that does not fit its grounds, an inference judged by whether it has a source looks unsupported even when its reasoning holds; recording grounds item by item lets the kind of grounds choose the check | Own design rationale | Cross-author replication not yet demonstrated | | P0 | EMERGING | | [x] |
| S3-5 | Toulmin modelled his layout of arguments on jurisprudence; in it any assertion is a claim with data, warrant, qualifier and rebuttal; he later wrote that he had not intended an analytical model like "the Toulmin model" | descriptive | src: Toulmin 2003 (pp. vii, 7, 90–94) |  |  |  |  | P1 | SUPPORTED | C | [ ] |
| S3-6 | Fixed wording for levels of certainty has precedents in intelligence analysis, climate assessment and evidence grading | descriptive | src: Kent 1964; src: Mastrandrea et al. 2010; src: Santesso et al. 2020 |  |  |  |  | P1 | SUPPORTED | D; D; A | [ ] |

### Section 4: Related Work and Design Rationale

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S4-3 | Structured verification combined with LLMs may outperform LLMs alone: reported for peer review aggregation (PeerArg 2024) and argument extraction (Gupta et al. 2024) | descriptive | src: PeerArg 2024; src: Gupta et al. 2024 | Two narrow tasks generalised to "structured + LLM beats LLM alone": an extrapolation | | Hedged in the manuscript ("may outperform") | | P1 | EMERGING | A; A | [x] |
| S4-5 | Argument-quality research distinguishes logical, rhetorical and dialectical quality and catalogues argumentation schemes | descriptive | src: Wachsmuth et al. 2017; src: Walton et al. 2008 (publisher description) |  |  |  |  | P1 | SUPPORTED | A; C | [ ] |
| S4-6 | Assurance cases from safety engineering are the closest existing practice: explicit claims linked to evidence by arguments, with assumptions stated; the claims–arguments–evidence approach defines arguments as Toulmin's warrants | descriptive | src: Bishop & Bloomfield 1998; src: Kelly & Weaver 2004; src: Bloomfield & Netkachova 2014 | | | | | P1 | SUPPORTED | A; A; A | [ ] |

### Section 5: Call to Action

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S5-2 | Next steps include: testing whether registers change what reviewers find, adapting the checks to other fields, building them into writing tools, and recognising recomputation of derived values as a check of its own | normative | claim: S4-3; claim: S3-1; decl: D7 | (1) evaluation across projects still needed (§4); (2) process-level argument plus extraction feasibility (S3-1, S4-3); (3) the open empirical question (§4) | | Directions, not commitments; each depends on others taking it up | | P2 | SPECULATIVE | | [x] |

### Declared starting points added for draft 2

**Declared starting points:**

| ID | Statement | Kind | Contestedness | Status |
|----|-----------|------|---------------|--------|
| D5 | Detection asks who wrote a text; verification asks whether it holds | definition | own | [x] |
| D6 | Mapping confidence tiers to prescribed language is this paper's proposal (an adaptation of calibrated-language practice) | assumption | own | [ ] |
| D7 | A proposal should be tested before it is adopted | value | accepted | [ ] |
| D8 | Checking claims against grounds and warrant is verification, and checking the contribution with Whetten's questions is validation, in the systems-engineering sense | assumption | own | [ ] |

---

## Source notes (carried from the DR-004 registry)

Full source notes for rows that existed before the migration, by ID. Newer rows cite their literature notes in `literature/sources/`.

- **S1-1**: Mugaanyi et al. 2024 (JMIR, DOI: 10.2196/52935): 62–89% DOI fabrication rates across disciplines. Walters & Wilder 2023 (Sci Rep 13:14045, DOI: 10.1038/s41598-023-41032-5, full text read 2026-09-26): 55% of GPT-3.5 and 18% of GPT-4 citations fabricated across 636 citations in 84 generated literature reviews. ⚠️ **Tier raised 2026-09-26 (EMERGING → SUPPORTED):** two agreeing peer-reviewed sources meet DR-002. The unmeasured clause "can survive multiple review rounds undetected" was dropped from the statement. Bhattacharyya 2023 (Cureus) and Chelli 2024 (JMIR) also agree, but only their abstracts have been read; add them after a full-text read.
- **S1-2**: Xiong et al. 2024 (ICLR, arXiv:2306.13063): verbalised confidence mostly 80–100% even when wrong. Zhou et al. 2024 (ACL, DOI: 10.18653/v1/2024.acl-long.198): overconfident answers, and users rely on them. Peters & Chin-Yee 2025 (RSOS, DOI: 10.1098/rsos.241776): LLM summaries overgeneralise scientific findings. El-Dakhs et al. 2025 (Corpus Pragmatics, DOI: 10.1007/s41701-025-00210-8, applied-linguistics abstracts): boosters 0.0162 vs 0.0077 per word, and hedges also higher, 0.0122 vs 0.0081 (Table 8). All four read in full 2026-09-26. The tier rests on the first three, which agree on the general claim. The booster clause is one study with mixed direction (Zou & Fan 2025 and Sadigzade 2026 find fewer stance markers, at abstract level) and is stated as unsettled. ⚠️ **Reworded and raised 2026-09-26 (EMERGING → SUPPORTED):** the old "demonstrates-for-suggests" statement had no direct source. Liang 2024 did not support it and is dropped.
- **S1-3 (withdrawn 2026-10-16)**: README.md "Architecture Blueprints"; hedged with "may"
- **S1-4**: L66 Samsonau 2026 (arXiv:2604.08501): 23-check manuscript linter incl. causal-language-vs-design and citation-purpose checks, experimental claim-typing by type/testability/scope; no warrant analysis or per-kind procedure; calibrated on empirical papers only. L60 Chen et al. 2026 (arXiv:2607.26512): four support relations routed back to the author; no warrant, calibration or boundary check. L61 Zhou & Yu 2026 (arXiv:2608.10858): provenance discipline with a claim–evidence index and a sampled sufficiency audit; standing tiers attach to its metrics, not to manuscript claims. Adjacent: L62 WarrantScore scores warrants in peer-review comments, not manuscripts. VANRA (EQUATOR registration 2026-09-02) verifies cited assertions in tiers for narrative reviews, which covers cited statements only. All three read in full 2026-09-26. ⚠️ **Reworded and P0 → P1 2026-09-26:** the earlier "no process-level verification infrastructure exists" is falsified by L60, L61 and L66. As a positioning claim the paper does not collapse without it (its case rests on S2-2, S3-4 and S5-1). It remains a hedged negative, so it stays EMERGING.
- **S1-5**: Internal experiments comparing LLM reviews prompted to "assess soundness" vs LLM reviews prompted to "numerically reproduce every calculation" show systematic difference in error detection.
- **S1-6**: Two peer-reviewed sources agree that detectors are fragile (DR-002); each supports one half. Dugan et al. 2024 (ACL, DOI: 10.18653/v1/2024.acl-long.674): repetition penalty cuts accuracy by up to 32 points; changing generator, decoding or settings gives up to 95+% error; detectors "not yet robust enough for widespread deployment or high-stakes use" (§7). Paraphrase effects in RAID are mixed (Table 6: accuracy rose for 3 of 6 detectors), so Dugan is not cited for paraphrase. Krishna et al. 2023 (NeurIPS, arXiv:2303.13408): DIPPER paraphrase of GPT2-XL generations cut DetectGPT 70.3 → 4.6 and watermark detection 100 → 57.2 at 1% FPR (Table 1); a retrieval defence still detected 80–97%. Both test 2023–24 detectors
- **S2-1**: EQUATOR Network website (equator-network.org, accessed 2026-03-03): 699 guidelines displayed. Reference claim — verifiable fact about external database.
- **S2-2**: EQUATOR library searches (2026-03-03, 2026-09-26): no guideline for these types. Peer-reviewed gap statements: Jaakkola 2020 (AMS Review, DOI: 10.1007/s13162-020-00161-0, full text): conceptual papers lack "commonly accepted templates or 'recipes'" (p. 18). Larsen et al. 2025 (MIS Quarterly 49(4), DOI: 10.25300/misq/2024/18064, author version read): "validity is neither well-understood nor consistently established in design science" (abstract), based on IS design-science papers. Gregor & Hevner 2013 (MIS Quarterly 37(2), DOI: 10.25300/MISQ/2013/37.2.01, full text): authors, reviewers and editors "struggle to present and interpret DSR work well"; the goal is "to establish some consensus on guidelines by which DSR research … can be judged" (it proposes its own publication schema, an author proposal). Dinter & Krawatzeck 2015 (ICIS, Research-in-Progress, full text): "still no common sense and no comprehensive guidance how to present DSR". These two agree on one proposition, for design science only. Exceptions named in the text: the ACM SIGSOFT Empirical Standards (Ralph et al. 2020, arXiv:2010.03525; community evidence standards of the CONSORT/PRISMA kind, not a formal consensus method). Their "Engineering Research (AKA Design Science)" standard is an artefact checklist that also asks for "correctness arguments" for analytical contributions; their "Methodological Guidelines and Meta-Science" standard covers papers that "may or may not include … empirical data", requires "clear, valid arguments supporting recommendations" and lists "informal logical fallacies" as antipatterns, but gives no procedure for verifying an argument. Neighbouring types: Baethge et al. 2019 (SANRA, "not a reporting guideline"), Nashwan et al. 2026, the VANRA registration (not peer-reviewed). ⚠️ **Stays EMERGING (2026-10-01):** a raise to SUPPORTED was drafted and refuted in review. Jaakkola and Larsen state different gaps (templates; validity norms) for different types, so they do not agree on one proposition (DR-002). Design science now has two agreeing sources (Gregor & Hevner, Dinter), conceptual papers one (Jaakkola), and theoretical and perspective papers none (editorials only), so the four-type claim stays EMERGING
- **S2-3 (now S2-3a and S2-3b)**: Gregor 2006 (MIS Quarterly, DOI: 10.2307/25148742): Types I–V confirmed; Type I (analytic) and Type V (design) are non-empirical in contribution. Reference claim — verifiable fact about Gregor's taxonomy. ⚠️ **Tier corrected 2026-09-24 (ESTABLISHED → EMERGING):** that Gregor defines five types is a reference claim, but this row's statement — Types I and V "cannot be verified against sources because they ARE the new contribution" — is our interpretation, which the reference-claim exception in `templates/claim-registry.md` excludes. Candidate for a split: the taxonomy half would be ESTABLISHED.
- **S2-4**: Toulmin (1958/2003): warrants are the inferential bridge; Whetten (1989): "Why" is most critical and most often missing. Both support argument quality over source checking for non-empirical contributions. ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** Toulmin and Whetten describe argument and theory structure; that argument quality is the *primary* challenge for non-empirical papers is our inference from them, not their finding. The manuscript hedges it ("may not be").
- **S3-1**: Toulmin (1958/2003): 6 components confirmed (claim, grounds, warrant, backing, qualifier, rebuttal). Gupta et al. 2024 (ACL, DOI: 10.18653/v1/2024.acl-long.552): LLM zero-shot Toulmin extraction outperforms generic prompts — reported evidence of technical feasibility (extraction, not verification). ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** Gupta et al. show Toulmin-guided *extraction*, not verification; operationalising verification is this paper's proposal. The manuscript hedges it ("may provide a basis").
- **S3-2**: Whetten 1989 (AMR, DOI: 10.5465/amr.1989.4308371): 4 components confirmed (What/How/Why/Who-Where-When). "Why" identified as most critical and most often missing. Operationalization was reported in own Whetten checklists (proposition audit §3, Examples C and D — see note). ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** the "proposition audit §3" cited here is no longer in the repository — `audits/` was purged from history in the v2.0.0 scrub and has been gitignored since `1d8c68c` (2026-06-10) — so the operationalisation evidence cannot be checked; what remains is Whetten's framework itself. Open: the manuscript states this one unhedged ("Propositions can be evaluated…").
- **S3-3**: Own proposal (this paper's contribution). Supporting evidence: technology audit §4 found 6/22 entries with over-confident language that the tier system would have caught. Framed with "may enable" in manuscript. ⚠️ **Noted 2026-09-24:** the "technology audit §4" is no longer in the repository (purged in the v2.0.0 scrub; `audits/` gitignored since `1d8c68c`), so the 6/22 figure cannot be re-checked. Tier unchanged — EMERGING already rests on the proposal itself.
- **S3-4**: Grounds S3-1; S3-2; S3-3; warrant: If an entry is scored low-confidence because it is evaluated as a source-backed CLAIM but its three premises are independently verified and its warrant is logically valid, then the low score is a false failure caused by applying the wrong verification procedure. This demonstrates that type-specific verification is not merely useful but necessary.; rebuttal: Limitation acknowledged: cross-author replication not yet demonstrated.; backing: Own design rationale.
- **S4-3**: PeerArg (NeLaMKRR@KR 2024, arXiv:2409.16813): "a variant of PeerArg outperforms end-to-end LLM baseline." Gupta (ACL 2024): Toulmin-based prompts outperform generic prompts. Both confirmed via content verification. ⚠️ **Tier corrected 2026-09-24 (SUPPORTED → EMERGING):** both sources are real and say what is quoted, but each covers one narrow task (review aggregation; argument extraction); the general "structured + LLM outperforms LLM alone" is our extrapolation. The manuscript hedges it ("may outperform").
- **S5-2**: Logical inference from current framework state and limitations. (1) Templates: follows from §4's opening (evaluation across projects, authors and domains still needed) and §5's limited-domain statement. (2) AI integration: follows from process-level argument + Gupta 2024 feasibility. (3) Empirical validation: follows from §4's closing "open empirical question". Manuscript language ("warrant investigation") matches SPECULATIVE tier.
- **S5-1 (now C1)**: Constructs: "verification infrastructure" (process-level reporting + verification scaffolding analogous to EQUATOR guidelines); "non-empirical paper" (Gregor Type I analytic, Type V design, plus perspective and methodological papers); "AI-augmented writing" (drafting and revision assisted by general-purpose LLMs) Relationship: Non-empirical paper publishing requires verification infrastructure (analogous to EQUATOR for empirical work) to remain trustworthy under AI augmentation Premises: S2-1; S2-2; S3-4 Reasoning: If empirical research benefits from ~700 reporting guidelines (EQUATOR), and non-empirical research has no consensus-based equivalent, and AI writing amplifies the verification challenge for non-empirical papers (where argument quality matters more than factual accuracy), and claims, arguments and propositions each need their own verification procedure (S3-4), then extending verification infrastructure to non-empirical papers is a legitimate and urgent need. Boundary: Applies to academic papers intended for peer-reviewed publication. Does not apply to: informal writing, journalism, creative writing, or papers where the verification infrastructure cost exceeds the benefit (e.g., very short opinion pieces). The specific checklists (Toulmin, Whetten) are grounded in Western academic argumentation traditions and may need adaptation for other scholarly traditions. Alternatives: Peer review counter-argument engaged in manuscript: peer review already polices argument quality. Response: peer review is end-stage and reviewer-dependent; reporting guidelines provide pre-submission structural checks complementary to (not replacing) peer review. Source: S2-1 [x], S2-2 [x], S3-4 [x] — all premises verified within this registry

---

## Source Verification Checklist

### Literature Sources

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| EQUATOR Network website | S2-1, S2-2 | Verified: 699 guidelines (2026-03-03); all empirical; no non-empirical guidelines found. Re-searched 2026-09-26: still none; VANRA and a concept-analysis guideline are in development | [x] |
| Xiong et al. 2024 (ICLR) | S1-2 | Verified 2026-09-26 (arXiv:2306.13063 + ICLR stamp, full text): verbalised overconfidence | [x] |
| Zhou et al. 2024 (ACL) | S1-2 | Verified 2026-09-26 (Crossref + full text); DOI 10.18653/v1/2024.acl-long.198 | [x] |
| Peters & Chin-Yee 2025 (RSOS) | S1-2 | Verified 2026-09-26 (Crossref + full text); DOI 10.1098/rsos.241776 | [x] |
| El-Dakhs et al. 2025 (Corpus Pragmatics) | S1-2 | Verified 2026-09-26 (Crossref + full text, Table 8 p. 15); DOI 10.1007/s41701-025-00210-8 | [x] |
| Larsen et al. 2025 (MIS Quarterly) | S2-2 | Verified 2026-10-01 (Crossref 49(4) 1267–1294; author version arXiv:2503.09466, abstract and literature-review findings read); DOI 10.25300/misq/2024/18064 | [x] |
| Gregor & Hevner 2013 (MIS Quarterly) | S2-2 | Verified 2026-10-01 (Crossref 37(2) 337–355; full text, pp. 338 and 353); DOI 10.25300/MISQ/2013/37.2.01 | [x] |
| Dinter & Krawatzeck 2015 (ICIS) | S2-2 | Verified 2026-10-01 (AIS eLibrary record; full text, abstract and introduction); Research-in-Progress; no DOI | [x] |
| Ralph et al. 2020 (ACM SIGSOFT Empirical Standards) | S2-2 (named exceptions) | Verified 2026-10-01 (arXiv:2010.03525; README, Engineering Research and Meta-Science standards read on GitHub); not peer-reviewed | [x] |
| Jaakkola 2020 (AMS Review) | S2-2 | Verified 2026-09-26 (Crossref + full text, p. 18 and Conclusions); DOI 10.1007/s13162-020-00161-0 | [x] |
| Baethge et al. 2019 (SANRA) | S2-2 | Verified 2026-09-26 (Crossref + full text); DOI 10.1186/s41073-019-0064-8 | [x] |
| Nashwan et al. 2026 (J Res Nurs) | S2-2 | Verified 2026-09-26 (Crossref + full text, Introduction); DOI 10.1177/17449871251410464 | [x] |
| VANRA registration (EQUATOR) | S1-4, S2-2 | Verified 2026-09-26: registration entry read on equator-network.org (registered 2026-09-02); web source, not peer-reviewed | [x] |
| Gregor 2006 (MIS Quarterly) | S2-3 | Verified: 5 types; Type I (analytic) and Type V (design) are non-empirical in contribution; DOI 10.2307/25148742 | [x] |
| Toulmin 1958/2003 | S3-1 | Verified: 6 components (claim, grounds, warrant, backing, qualifier, rebuttal); ISBN 978-0-521-53483-3 | [x] |
| Whetten 1989 (AMR) | S3-2 | Verified: What/How/Why/Who-Where-When; DOI 10.5465/amr.1989.4308371 | [x] |
| Gupta et al. 2024 (ACL) | S3-1, S4-3 | Verified: Toulmin-based zero-shot prompting outperforms generic; DOI 10.18653/v1/2024.acl-long.552 | [x] |
| PeerArg 2024 (NeLaMKRR@KR) | S4-3 | Verified: PeerArg outperforms end-to-end LLM baseline; arXiv:2409.16813 | [x] |
| Krishna et al. 2023 (NeurIPS) | S1-6 | Verified 2026-09-27 (NeurIPS proceedings page + arXiv:2303.13408 v2, §4 and Table 1 read): paraphrase cuts detection sharply (DetectGPT 70.3 → 4.6 at 1% FPR); no publisher DOI, arXiv DOI 10.48550/arXiv.2303.13408 | [x] |
| Dugan et al. 2024 (ACL) | S1-6 | Verified 2026-09-27 (full text, §7 and Tables 4–6): accuracy depends on generation settings and attacks (paraphrase mixed, Table 6); detectors "not yet robust enough for … high-stakes use"; DOI 10.18653/v1/2024.acl-long.674 | [x] |
| Mugaanyi et al. 2024 (JMIR) | S1-1 | Verified: 62–89% DOI fabrication rates; DOI 10.2196/52935 | [x] |
| Walters & Wilder 2023 (Sci Rep) | S1-1 | Verified 2026-09-26 (Crossref + full text): 55% GPT-3.5 / 18% GPT-4 citations fabricated; DOI 10.1038/s41598-023-41032-5 | [x] |
| Liang et al. 2024 (NEJM AI) | — (was S1-2; no longer cited, 2026-09-26) | Verified: LLMs catch surface issues but struggle with deep argument analysis; DOI 10.1056/AIoa2400196 | [x] |
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

## Checks

The checks follow each claim's grounds (DR-027; `docs/glossary.md`, "The model in brief"): a source check per `src:` item (the work exists; it says what is attributed), a warrant check for `claim:` grounds or combined sources, declared starting points stated with their contestedness, `own:` items with a repeatable method, boundary conditions and a declared value for normative claims, and Whetten's elements and questions for the contribution.

---

## Confidence Tier Reference

| Tier | Assign when... | Language |
|------|---------------|----------|
| **ESTABLISHED** | CLAIM: multiple independent sources. ARGUMENT: complete Toulmin + fair engagement. PROPOSITION: premises verified + logic valid + tested | "demonstrates", "shows", "confirms" |
| **SUPPORTED** | CLAIM: 2-3 sources agree. ARGUMENT: warrant valid + evidence sufficient. PROPOSITION: premises verified + logic valid | "indicates", "supports", "evidence suggests" |
| **EMERGING** | CLAIM: 1-2 sources. ARGUMENT: evidence partial or warrant debatable. PROPOSITION: premises plausible + logic sound | "may", "preliminary evidence", "initial findings suggest" |
| **SPECULATIVE** | CLAIM: inference only. ARGUMENT: position stated, logic incomplete. PROPOSITION: conjectural | "warrants investigation", "remains unclear", "we hypothesize" |

## Source Tier Reference

| Tier | Type | Weight |
|------|------|--------|
| A | Peer-reviewed primary research | 1.0 |
| B | Peer-reviewed review article | 0.8 |
| C | Textbook / established reference | 0.9 |
| D | Guidelines / industry standards | 0.7 |
| E | Own unpublished work (under review) | 0.6* |
| F | *(retired by DR-027: an inference is a warrant; an own observation is an `own:` item)* | — |

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
