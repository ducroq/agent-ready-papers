# Paper 1 claim registry: DR-027 trial migration (copy)

> **Test fixture copy (tests/fixtures/v5/).** Copied from the maintainer's trial migration (`docs/work-items/v5-trial/`, gitignored); the changes are a sub-table marker (`**Contributions:**`, `**Declared starting points:**`, `**Claims:**`) inserted above each table, because the tools read a table only under a marker; and S1-3 and S1-5 typed as `own:` grounds with their method and a blank Source Tier, per DR-027's Tier-F rule (own observation is not a source).

> **Trial copy for DR-027's acceptance condition 2 (2026-10-16).** Not the registry of record: `papers/perspective/vv/claims/claim_registry.md` stays on DR-004's schema until the tools change. Statements are verbatim from the registry at `b6c6aed`; source notes are shortened (full notes in the original). ⚑ marks a choice the new schema forced: these are the trial's findings.

## Contributions

**Contributions:**

| ID | Contribution | Says | Rests on | What | How | Why | Who/Where/When | Objections engaged | Priority | Confidence tier | Status |
|----|--------------|------|----------|------|-----|-----|----------------|--------------------|----------|-----------------|--------|
| C1 | The scholarly community needs verification infrastructure for non-empirical papers — analogous to what EQUATOR provides for empirical research — to maintain academic integrity in the age of AI-augmented writing | normative | claim: S2-1; claim: S2-2; claim: S3-4; decl: D1; decl: D2; decl: D3; decl: D4 | Verification infrastructure, non-empirical papers, AI-augmented writing (D2–D4) | Non-empirical paper publishing requires verification infrastructure to remain trustworthy under AI augmentation | If empirical research benefits from ~700 reporting guidelines, and non-empirical research has no consensus-based equivalent, and AI writing amplifies the verification challenge for non-empirical papers, and each kind of claim needs its own check (S3-4), then extending verification infrastructure to non-empirical papers is a legitimate and urgent need | Applies to academic papers intended for peer-reviewed publication. Does not apply to: informal writing, journalism, creative writing, or very short opinion pieces. Checklists grounded in Western academic argumentation traditions | Peer review already polices argument quality. Response: peer review is end-stage and reviewer-dependent; reporting guidelines add pre-submission structural checks | P0 | EMERGING | [x] |

⚑ **C1 was S5-1** (PROPOSITION). The glossary maps a paper's central proposition to its contribution; S5-1 is that. Its Constructs became declared definitions D2–D4, its Reasoning became Why, its Relationship became How.

⚑ **"AI writing amplifies the verification challenge"** sits in C1's Why but rests on no registered claim. The backlog already flags this (S5-1). The new schema makes the gap visible: Why mentions a step that Rests on does not list.

## Declared starting points

**Declared starting points:**

| ID | Statement | Kind | Contestedness | Status |
|----|-----------|------|---------------|--------|
| D1 | Published reasoning should be checkable: readers and reviewers should be able to see what each claim rests on | value | accepted in the field | [ ] |
| D2 | "Verification infrastructure": process-level reporting plus verification scaffolding analogous to EQUATOR guidelines | definition | own | [x] |
| D3 | "Non-empirical paper": Gregor Type I (analytic) and Type V (design), plus perspective and methodological papers | definition | own | [x] |
| D4 | "AI-augmented writing": drafting and revision assisted by general-purpose LLMs | definition | accepted in the field | [x] |

⚑ **D1 is new.** S5-1 never named the value it serves ("to maintain academic integrity" points at one). The normative rule forces it to be stated; the wording is mine and needs the author's approval, hence `[ ]`.

⚑ **D3 is the definition the reviewers attacked** (paper types are not a taxonomy, feedback #10). As a declared definition marked "own", its contestedness is now on record instead of hidden inside a PROPOSITION's Constructs cell.

## Claims

### Section 1: The Problem

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S1-1 | AI citation hallucination is a distinct failure mode — LLMs invent plausible-sounding papers, authors, and DOIs at substantial rates (lower for GPT-4 than GPT-3.5 in the one study comparing them) | descriptive | src: Mugaanyi et al. 2024; src: Walters & Wilder 2023 | | | | | P0 | SUPPORTED | A; A | [x] |
| S1-2 | AI writing assistants may express more certainty than the evidence warrants: LLMs verbalise overconfidence and overgeneralise scientific findings; whether this extends to boosters in academic prose is unsettled (one abstract corpus finds twice the human rate of boosters and also more hedges) | descriptive | src: Xiong et al. 2024; src: Zhou et al. 2024; src: Peters & Chin-Yee 2025; src: El-Dakhs et al. 2025 | The three studies of LLM output, each on a different task, jointly support the general claim | | Booster clause rests on one study with mixed direction; stated as unsettled | Zou & Fan 2025, Sadigzade 2026 find fewer stance markers (abstract level) | P0 | SUPPORTED | A; A; A; A | [x] |
| S1-3 | Without architectural constraints (page budgets, section specifications), AI agents expand arguments beyond evidence, add unnecessary sections, and exceed page budgets | descriptive | own: observation of agent sessions without page budgets, recorded in README "Architecture Blueprints" | | | | | P1 | EMERGING | | [x] |
| S1-4 | Existing verification infrastructure for AI-assisted writing — citation and consistency linters, claim–evidence adjudication, provenance disciplines — checks whether evidence exists, supports or suffices, and some of it audits language against empirical study design; to our knowledge none distinguishes claims from arguments and propositions and applies a procedure suited to each, and none targets papers whose contribution is reasoning rather than fact | descriptive | src: Samsonau 2026; src: Chen et al. 2026; src: Zhou & Yu 2026; src: VANRA registration | Absence inferred from the closest tools found: each checks evidence, none applies a per-kind procedure | | "To our knowledge": a hedged negative | | P1 | EMERGING | B; B; B; D | [x] |
| S1-5 | AI-generated equations can contain arithmetic errors that survive plausibility review but are caught by mechanical numerical reproduction | descriptive | own: internal experiments, LLM reviews prompted to "assess soundness" vs to "numerically reproduce every calculation", errors detected compared | | | | | P1 | EMERGING | | [x] |
| S1-6 | AI-text detection is no substitute for verification: detection asks who wrote a text, verification asks whether it holds (definitional). Detectors are fragile: accuracy varies with generation settings, and paraphrase can collapse it | descriptive | decl: D5; src: Dugan et al. 2024; src: Krishna et al. 2023 | | | Both test 2023–24 detectors | | P2 | SUPPORTED | A; A | [x] |

⚑ **S1-3 and S1-5 were Source Tier F** ("logical inference"), but neither is an inference from registered claims: both are the author's own observations. They become own work, **Source Tier E**. DR-027 said a Tier-F source becomes a warrant; these two show that rule is wrong for some F rows: Tier F was being used for "own experience" as well as for "inference". (Finding for DR-027's open question on retiring F.)

⚑ **S1-2 and S1-4 gain Warrants.** Both combine several sources into a point none states alone (S1-2: three tasks into one general claim; S1-4: an absence inferred from a search). Under DR-004 they were plain CLAIMs and the inference was invisible.

⚑ **S1-6 contains a definition** ("verification asks whether it holds"), now declared as D5 (table at the end). Its two sources each support one half: a conjunction, not a synthesis, so no warrant.

### Section 2: The Landscape Gap

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S2-1 | EQUATOR Network maintains ~700 reporting guidelines for empirical health research (CONSORT for RCTs, STROBE for observational, PRISMA for reviews, etc.) | descriptive | src: EQUATOR website (accessed 2026-03-03: 699 displayed) | | | | | P0 | ESTABLISHED | D | [x] |
| S2-2 | To our knowledge, no consensus-based reporting guideline of the EQUATOR type exists for theoretical, perspective or conceptual papers; [… statement verbatim as in the original …]; none sets out how to verify arguments or propositions as distinct from cited statements | descriptive | src: EQUATOR searches 2026-03-03, 2026-09-26; src: Jaakkola 2020; src: Larsen et al. 2025; src: Gregor & Hevner 2013; src: Dinter & Krawatzeck 2015; src: Ralph et al. 2020 | Absence inferred from library searches and from gap statements that each cover one paper type | | Design science has two agreeing sources, conceptual one, theoretical and perspective none | Baethge et al. 2019 (SANRA), Nashwan et al. 2026, VANRA: neighbouring types, not counter-examples | P0 | EMERGING | D; A; A; A; A; D | [x] |
| S2-3a | Gregor's (2006) taxonomy has five theory types, including Type I (analytic) and Type V (design and action) | descriptive | src: Gregor 2006 | | | | | P1 | ESTABLISHED | A | [ ] |
| S2-3b | Type I and Type V contributions are fundamentally non-empirical: they cannot be verified against sources because they are the new contribution | descriptive | claim: S2-3a | Theories that propose rather than report have no prior source to be checked against | | | | P1 | EMERGING | | [ ] |
| S2-4 | For non-empirical papers, argument quality — warrant validity, reasoning coherence, boundary conditions — is the primary verification challenge, not factual accuracy | descriptive | src: Toulmin 2003; src: Whetten 1989 | From "warrants are the inferential bridge" and "Why is most critical and most often missing" to "argument quality is the primary challenge" is our inference | | Hedged in the manuscript ("may not be") | | P1 | EMERGING | C; A | [x] |

⚑ **S2-1 shows the one-source problem** already on the backlog: ESTABLISHED, one source. The new schema shows it plainly (one `src:` item, ESTABLISHED) where the old one buried it in a long cell.

⚑ **S2-3 split into S2-3a and S2-3b**, the split the registry note proposed. The model makes the split natural: the reference fact rests on a source (ESTABLISHED), the interpretation rests on that fact plus a warrant (EMERGING). Both new rows `[ ]`: written in this session.

⚑ **S2-4's Source Tier "C; A"** stays, but its tier was corrected in 2026-09 *because* it is an inference. The Warrant cell now says so in the place a checker reads.

### Section 3: The Proposal

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S3-1 | Toulmin's (1958/2003) argument model — claim, grounds, warrant, qualifier, rebuttal — provides an operationalizable framework for verifying argument quality in academic writing | descriptive | src: Toulmin 2003; src: Gupta et al. 2024 | Gupta shows Toulmin-guided extraction; that the layout can drive verification is this paper's extension | | Toulmin's 2003 preface rejects "the Toulmin model" as an analytical model | | P1 | EMERGING | C; A | [x] |
| S3-2 | Whetten's (1989) What/How/Why/Who-Where-When framework provides an operationalizable structure for verifying propositions by checking construct definition, relationship clarity, reasoning explicitness, and boundary conditions | descriptive | src: Whetten 1989 | Whetten wrote the elements as an editor's test of theory papers; using them to check single propositions is this paper's extension | | | | P1 | EMERGING | A | [x] |
| S3-3 | Mapping confidence tiers (ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE) to prescribed language ("demonstrates" vs "suggests" vs "may" vs "warrants investigation") enables systematic calibration of claim strength to evidence strength | descriptive | decl: D6 | | | The supporting audit (6/22 entries) is no longer in the repository | | P1 | EMERGING | | [x] |
| S3-4 | Claims, arguments, and propositions require fundamentally different verification procedures: source checking for CLAIMs, Toulmin analysis for ARGUMENTs, and Whetten analysis for PROPOSITIONs — applying the wrong procedure produces false failures | descriptive | claim: S3-1; claim: S3-2; claim: S3-3 | If an entry is scored low-confidence because it is evaluated as a source-backed CLAIM but its three premises are independently verified and its warrant is logically valid, then the low score is a false failure caused by applying the wrong verification procedure | Own design rationale | Cross-author replication not yet demonstrated | | P0 | EMERGING | | [x] |

⚑ **S3-3 is the paper's own proposal**, so it rests on no source. It becomes a claim grounded in a declared starting point D6 ("own proposal") — or it should be part of C1. The reviewers' advice (adapt IPCC/GRADE) would give it real `src:` grounds in draft 2.

⚑ **S3-1 and S3-2 gain Warrants** that admit the extension (extraction → verification; theory test → single proposition), and S3-1 gains a Rebuttal from Toulmin's own preface. Both points came out of reading the sources in full this session.

⚑ **S3-4's statement still uses DR-004's types.** Under the new model the argument itself changes: the claim becomes "each claim needs the checks its grounds call for". That is a draft-2 rewrite, not a migration; the row is kept verbatim. Its old "This demonstrates…" sentence was dropped from the Warrant (already on the backlog: confident language on an EMERGING row).

### Section 4: Related Work and Design Rationale

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S4-3 | Structured verification infrastructure combined with LLM capability outperforms LLM capability alone — reported for peer review aggregation (PeerArg 2024) and argument extraction (Gupta et al. 2024) | descriptive | src: PeerArg 2024; src: Gupta et al. 2024 | Two narrow tasks generalised to "structured + LLM beats LLM alone": an extrapolation | | Hedged in the manuscript ("may outperform") | | P1 | EMERGING | A; A | [x] |

### Section 5: Call to Action

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S5-2 | Next steps include: discipline-specific verification templates beyond the medical/engineering domains tested here, integration with AI writing tools as structured prompting infrastructure, and empirical validation comparing verification-assisted vs unassisted AI writing quality | normative | claim: S4-3; claim: S3-1 | (1) evaluation across projects still needed (§4); (2) process-level argument plus extraction feasibility (S3-1, S4-3); (3) the open empirical question (§4) | | | | P2 | SPECULATIVE | | [x] |

⚑ **S5-2 was a CLAIM; it is normative** ("next steps include…" recommends). As normative it now needs a declared value and boundary conditions, which it lacks, so under the new rules it would fail the schema check. Correct outcome: the row was under-specified all along.

⚑ **S5-2 was Source Tier F** and really is an inference from registered claims, so here DR-027's Tier-F → Warrant rule works.

### Declared starting points added during migration

**Declared starting points:**

| ID | Statement | Kind | Contestedness | Status |
|----|-----------|------|---------------|--------|
| D5 | Detection asks who wrote a text; verification asks whether it holds | definition | own | [x] |
| D6 | Mapping confidence tiers to prescribed language is this paper's proposal (an adaptation of calibrated-language practice) | assumption | own | [ ] |

## Before and after

| Measure | DR-004 registry | Trial copy | Why it differs |
|---------|-----------------|------------|----------------|
| Rows | 17 | 17 claims + 1 contribution + 6 declared | S2-3 split; S5-1 → C1; six starting points made explicit |
| P0 rows | 6 (S1-1, S1-2, S2-1, S2-2, S3-4, S5-1) | 6 (S1-1, S1-2, S2-1, S2-2, S3-4, C1) | Same set; S5-1 is now C1 |
| P0 at SUPPORTED or above | 3 of 6 (floor fails) | 3 of 6 (floor fails) | Same result |
| Claims with a Warrant | 1 (S3-4) | 10 | Inferences hidden inside "CLAIM" rows are now recorded |
| Normative claims missing a value or boundary conditions | not checked | S5-2 | The new rule catches an under-specified row |
| Source Tier F | 5 rows | 0 | S1-3, S1-5 own observations → E; S5-2 inference → warrant; S3-4's F was backing; S5-1's F annotated its premises, now C1's Rests on |
| Rows needing author approval (`[ ]`) | 0 | 4 (S2-3a, S2-3b, D1, D6) | Written in this session |

## Findings for DR-027

1. **The schema holds.** Every column of every old row found a home; no row needed a column the schema lacks.
2. **Tier F is two things**: own observation (→ Source Tier E) and inference (→ Warrant). DR-027's rule "a Tier-F source becomes a warrant" is wrong for the first kind. Fix the migration rule; retire F.
3. **Hidden inferences surface**: 9 rows that DR-004 typed as plain CLAIMs (counting S2-3b, split from one) combine sources into a point none makes alone. Their warrants are now recorded and checkable. This is the model's main gain, and it matches Gemini's usability warning about synthesised sources.
4. **The normative rule catches real gaps**: C1 needed a declared value (D1, new); S5-2 is normative and under-specified.
5. **Definitions surface**: four definitions (D2–D5) were buried in Constructs cells and a CLAIM statement; one of them (D3) is exactly what the reviewers contested.
6. **One judgement call the rules don't settle**: whether S3-3 (an own proposal) is a claim on a declared starting point or part of the contribution.
7. **P0 floor unchanged** (3 of 6), as acceptance condition 3 requires.
