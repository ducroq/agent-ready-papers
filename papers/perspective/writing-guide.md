# Writing Guide: Registry-to-Section Mapping

<!-- Maps verified registry entries (CLAIMs, ARGUMENTs, PROPOSITIONs) to
     paper sections with language calibration. Consult before writing or
     editing any section. -->

**Paper:** The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines for Reasoning
**Last Updated:** 2026-03-16 (added Framework Component Language special case, PROPOSITION pre-submission items, negative claim hedging)

---

## How to Use This Guide

1. **Before writing a section:** Check which registry entries apply (CLAIMs, ARGUMENTs, PROPOSITIONs)
2. **For each entry:** Use the confidence tier to calibrate language
3. **For CLAIMs:** Source details are in `vv/claims/claim_registry.md`
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

### The Underlying Principle

The rules in this guide are instances of one structural requirement: **the language tier used in the manuscript must be at most the confidence tier in the registry for the same claim.** Citation drift, overclaiming, and inverse hallucination (Step Z) are all the same failure — language climbing one or more tiers above what the evidence chain supports. A reviewer's first check on any load-bearing claim is whether the language sits at or below the registered tier; if it does not, either the registry needs upgrading (with new evidence) or the language needs downshifting. (Propagated from `templates/writing-guide.md` per DR-017.)

### Writing by Unit Type

| Type | How to write it | Watch for |
|------|----------------|-----------|
| CLAIM | State the fact, cite the source, match language to tier | Overclaiming (confident language for EMERGING/SPECULATIVE) |
| ARGUMENT | State the conclusion, present the evidence (grounds), make the warrant explicit | Implicit warrants that the reader won't share; missing counter-arguments |
| PROPOSITION | State the recommendation, give the reasoning, specify where it applies | Overgeneralization; missing boundary conditions |

**ARGUMENT prose pattern:**
> [Grounds — the evidence, citing verified CLAIMs]. [Warrant — why this evidence leads to the conclusion]. [Qualifier — hedging per confidence tier]. [Therefore, conclusion]. [Rebuttal — acknowledging the strongest counter-argument].

Example: "Toulmin's model makes an argument's warrant explicit (S3-1), Whetten's framework does the same for a proposition's boundary conditions (S3-2), and confidence tiers tie language to evidence (S3-3). An argument's validity rests on its warrant and premises, not on how many sources it cites. So an argument checked as if it were a claim **may** be scored unverified when it is not wrong, a false failure caused by the procedure rather than the content. This **suggests** that each unit type needs its own verification procedure. Cross-author replication has not yet tested it."

**PROPOSITION prose pattern:**
> [Reasoning — why this recommendation follows from the arguments]. [Proposition — the recommendation itself]. [Boundary conditions — where it applies and where it doesn't].

Example: "Given the ~700 EQUATOR guidelines for empirical research and no consensus-based equivalent for non-empirical types (S2-1, S2-2), combined with the growing use of AI writing tools that amplify argument-level verification challenges, we propose that the scholarly community develop verification infrastructure for non-empirical papers. This applies to academic papers intended for peer-reviewed publication in fields where argument quality is a primary contribution; informal writing, journalism, and very short opinion pieces fall outside this recommendation."

### Framework Component Language — Special Case

This paper **proposes** the typed verification framework. The framework components are EMERGING until empirically validated — even when the supporting evidence is strong. The framework itself is an interpretation of evidence, not the evidence.

| Anti-pattern | Correct pattern |
|-------------|----------------|
| "Our framework demonstrates..." | "We propose..." |
| "The model shows..." | "The framework posits..." |
| "The three types ARE necessary" | "The framework assumes three types are necessary" |

Confidence progression for framework components:
- **SPECULATIVE** → conjectural, no supporting evidence
- **EMERGING** → novel contribution, supporting evidence but no empirical validation of the framework itself
- **SUPPORTED** → initial validation (pilot studies, case studies)
- **ESTABLISHED** → independent replication

**Key rule:** Capability claims ("teachable," "assessable," "measurable") require evidence of teaching/assessment, not just logical inference from the framework.

### Special Cases

| Situation | Language |
|-----------|----------|
| Own work (under review) | "we observed", "our findings indicate" — never "it was found" |
| Own work (published) | "we previously demonstrated" with citation |
| Logical inference | "If [premises], then [conclusion]" — mark as inference |
| Single study | "In a study of N=X, [Author] found..." — note sample size |
| Contradictory evidence | "While [Author1] reported X, [Author2] found Y" — acknowledge both |
| Negative claims | "to our knowledge, no X exists" — search and document the null result |
| Audit data (own projects) | "A retrospective audit of [project] revealed..." — frame as preliminary |

---

## Section → Registry Mapping

### 1. The Problem (AI failure modes)

**Purpose:** Establish that AI writing assistance creates failure modes distinct from — and more subtle than — citation hallucination alone, and that existing solutions address only part of the problem.

**Word budget:** ~700 words

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| S1-1 | AI citation hallucination as distinct failure mode | CLAIM | SUPPORTED | "evidence indicates that LLMs invent plausible-sounding papers" (Mugaanyi 2024; Walters & Wilder 2023) |
| S1-2 | Confidence inflation: more certainty than the evidence warrants | CLAIM | SUPPORTED | "evidence suggests LLMs express more certainty than warranted" (Xiong, Zhou 2024, Peters). Keep the booster clause as unsettled |
| S1-3 | Scope creep without architectural constraints | CLAIM | EMERGING | "Without structural constraints, AI-assisted drafts may expand beyond what evidence supports" |
| S1-5 | AI-generated equations contain arithmetic errors surviving plausibility review | CLAIM | EMERGING | "AI-generated equations can contain arithmetic errors that survive review because they produce plausible-looking results" |
| S1-4 | No existing infrastructure applies a verification procedure per unit type (P1) | CLAIM | EMERGING | "To our knowledge, none distinguishes claims from arguments and propositions" — name L60, L61, L66 first |

**Key sources:**
- `literature/sources/liang-2024.md` — AI hallucination evidence
- `../../README.md` "The Core Problem" — failure mode taxonomy

**Cautions:**
- Do NOT frame this as "AI is bad for writing" — frame as "AI writing assistance creates *new* failure modes that require *new* infrastructure"
- S1-3 is EMERGING, so hedge it. S1-1 and S1-2 are SUPPORTED: "indicates", "evidence suggests", never "demonstrates"
- S1-4 is a hedged negative about prior art. Process-level systems exist (L60 Chen, L61 Zhou & Yu, L66 sciwrite-lint), so name them and state precisely what they lack. Never write "no process-level infrastructure exists"
- Reference model/tool level solutions generically (citation checkers, RAG) — specific tool names were removed as uncitable

---

### 2. The Landscape Gap

**Purpose:** Establish the specific gap: EQUATOR covers empirical papers comprehensively; nothing covers non-empirical paper types. Ground this in Gregor's theory types to show the gap is structural, not accidental.

**Word budget:** ~700 words

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| S2-1 | EQUATOR maintains ~700 reporting guidelines | CLAIM | ESTABLISHED | "The EQUATOR Network maintains nearly 700 reporting guidelines" — verified: 699 guidelines (2026-03-03) |
| S2-2 | No consensus-based guideline for non-empirical papers | CLAIM | EMERGING | "To our knowledge, no published consensus-based guideline of the EQUATOR type exists" — name SANRA, Nashwan, VANRA |
| S2-3 | Gregor's Type I and V are non-empirical | CLAIM | EMERGING | "Gregor (2006) identified five theory types, two of which — analytic (Type I) and design (Type V) — are fundamentally non-empirical" |
| S2-4 | Argument quality is the primary verification challenge | CLAIM | EMERGING | "For non-empirical papers, the primary verification challenge may be argument quality rather than factual accuracy" |

**Key sources:**
- `literature/sources/equator-gap.md` — EQUATOR landscape analysis
- `literature/sources/gregor-2006.md` — five theory types
- EQUATOR Network website (https://www.equator-network.org/) — verify current count

**Cautions:**
- S2-1 count verified: 699 guidelines (2026-03-03); rounded to "nearly 700" in manuscript
- S2-2 is a universal negative — PRISMA covers systematic reviews (structured but arguably non-empirical); acknowledge this partial exception
- S2-3 is a published taxonomy from 2006 — check for any updates or critiques; Gregor is well-cited in IS but may be unfamiliar to the Learned Publishing audience
- Frame the gap as an *opportunity*, not a criticism of EQUATOR

---

### 3. The Proposal (typed verification)

**Purpose:** Present the typed verification model (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists. This is the paper's novel contribution — frame it as extending verification infrastructure to non-empirical papers.

**Word budget:** ~700 words

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| S3-1 | Toulmin provides operationalizable argument verification | CLAIM | EMERGING | "Toulmin's (1958/2003) argument model may provide a basis for operationalizing argument verification" |
| S3-2 | Whetten provides operationalizable proposition verification | CLAIM | EMERGING | "Whetten's (1989) framework may similarly operationalize proposition verification" |
| S3-3 | Confidence tiers enable systematic language calibration | CLAIM | EMERGING | "Mapping confidence tiers to prescribed language may enable systematic calibration" |
| S3-4 | Different types require different verification procedures | ARGUMENT | EMERGING | See warrant in registry; use "may produce false failures", argued from S3-1–S3-3 |

**Warrant check for S3-4:**
- S3-4 warrant: if an argument is scored as a source-backed claim when its premises are verified and its warrant is valid, the low score is a false failure caused by the procedure. So type-specific verification is needed. The warrant bridges from "the procedures test different things" to "types need different procedures."
- Grounds: S3-1, S3-2, S3-3 (the registry's premises)
- Qualifier: EMERGING. The argument is reasoned from its premises; no cross-author replication yet. Since 2026-09-26 no audit data backs it (S4-1 is withdrawn, #38)

**Key sources:**
- `literature/sources/toulmin-1958.md` — argument model
- `literature/sources/whetten-1989.md` — theoretical contribution framework
- `literature/sources/gupta-2024.md` — LLM + Toulmin feasibility

**Cautions:**
- Present Toulmin and Whetten as *established frameworks being applied to a new domain* (verification), not as new contributions themselves
- S3-4 is the paper's central interpretive claim — it must be presented as an ARGUMENT with explicit warrant, not as a self-evident fact
- Do not overclaim the maturity of the proposal — this is a perspective paper proposing a model, not reporting validated results
- Connect to Gupta et al. (2024) to show LLM-based Toulmin extraction is technically feasible

---

### 4. Related Work and Design Rationale

**Purpose:** Position the proposal against existing tool-level, model-level and process-level approaches, and give its design rationale. There is no evidence section. The retrospective-audit entries (S4-1, S4-2, S4-4) were withdrawn on 2026-09-26 (#38) after their prose was stripped in `1d8c68c`. Do not reintroduce audit figures.

**Word budget:** ~400 words

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| S4-3 | Structured verification + LLM > LLM alone | CLAIM | EMERGING | "Recent work on peer review (PeerArg 2024) and argument extraction (Gupta et al. 2024) suggests that structured frameworks combined with LLMs outperform LLMs alone" |

**Key sources:**
- `literature/sources/peerarg-2024.md` — structured + LLM evidence
- `literature/sources/gupta-2024.md` — Toulmin + LLM evidence

**Cautions:**
- Each of S4-3's two sources covers one narrow task; say "suggests", and do not generalise to "verification"
- Name process-level prior art (S1-4) and draw the line precisely. Overstating what it lacks is worse than the original overclaim

---

### 5. Call to Action

**Purpose:** Make the paper's central recommendation and outline next steps. This is the PROPOSITION section — must include boundary conditions and engage alternatives.

**Word budget:** ~700 words

**Entries to use:**

| ID | Statement | Type | Tier | Appropriate Language |
|----|-----------|------|------|---------------------|
| S5-1 | The scholarly community needs verification infrastructure for non-empirical papers | PROPOSITION | EMERGING | "We propose that the scholarly community develop verification infrastructure..." — use the proposition prose pattern |
| S5-2 | Next steps: discipline-specific templates, AI tool integration, empirical validation | CLAIM | SPECULATIVE | "Future work might include..." or "Several directions warrant investigation" |

**Boundary check for S5-1:**
- Applies to: Academic papers intended for peer-reviewed publication
- Does NOT apply to: Informal writing, journalism, creative writing, very short opinion pieces
- Reasoning: If EQUATOR benefits empirical research (S2-1) and non-empirical research has no consensus-based equivalent (S2-2), and each unit type needs its own verification procedure (S3-4), then extending infrastructure is warranted
- Alternative engaged: One could argue that journal peer review already provides adequate argument verification for non-empirical papers — counter: AI writing amplifies the challenge beyond what traditional review was designed for

**Key sources:**
- Synthesis of S2-1, S2-2 and S3-4 (the registry's premises)
- `literature/sources/equator-gap.md` — the gap being addressed

**Cautions:**
- S5-1 is the paper's single PROPOSITION — it must be written with the full proposition prose pattern (reasoning → recommendation → boundaries)
- Do NOT frame as "everyone must adopt this" — frame as "the community should develop this"
- S5-2 is SPECULATIVE — use "warrants investigation" language, not "should" or "will"
- End with a concrete, memorable closing — perhaps returning to the EQUATOR comparison

---

## Quick Reference: All Entries by Tier

### ESTABLISHED / SUPPORTED — Ready for Strong Statements

⚠️ *Rebuilt from the claim registry 2026-09-24. This table and the EMERGING one below had drifted: nine entries were listed in both tables, each with contradictory tiers. The registry is the source of truth — re-derive from it rather than editing these tables by hand.*

| ID | Statement | Type | Tier | Best Source |
|----|-----------|------|------|------------|
| S2-1 | EQUATOR ~700 guidelines | CLAIM | ESTABLISHED | EQUATOR website (699, 2026-03-03) |
| S1-1 | AI citation hallucination | CLAIM | SUPPORTED | Mugaanyi 2024; Walters & Wilder 2023 |
| S1-2 | Confidence inflation | CLAIM | SUPPORTED | Xiong 2024; Zhou 2024; Peters & Chin-Yee 2025 |

### EMERGING — Appropriately Hedged

| ID | Statement | Type | Tier | Hedging Language |
|----|-----------|------|------|------------------|
| S1-3 | Scope creep | CLAIM | EMERGING | "may expand", "without constraints" |
| S1-5 | Calculation errors in AI-generated equations | CLAIM | EMERGING | "can contain", "survive plausibility review" |
| S1-4 | No per-type procedure in existing infrastructure (P1) | CLAIM | EMERGING | "to our knowledge, none distinguishes claims from arguments and propositions" |
| S2-2 | No consensus-based non-empirical guidelines | CLAIM | EMERGING | "to our knowledge, no published consensus-based guideline" |
| S2-3 | Gregor Type I and V non-empirical | CLAIM | EMERGING | "identified five types, two of which" |
| S2-4 | Argument quality is primary challenge | CLAIM | EMERGING | "may be the primary challenge" |
| S3-1 | Toulmin operationalizable | CLAIM | EMERGING | "may provide a basis for" |
| S3-2 | Whetten operationalizable | CLAIM | EMERGING | "may similarly operationalize" |
| S3-3 | Confidence tiers enable calibration | CLAIM | EMERGING | "may enable systematic calibration" |
| S3-4 | Different types need different verification | ARGUMENT | EMERGING | "may produce", "suggests" |
| S4-3 | Structure + LLM > LLM alone | CLAIM | EMERGING | "recent work suggests" |
| S5-1 | Community needs infrastructure | PROPOSITION | EMERGING | "we propose that" |

### SPECULATIVE — Requires Careful Framing

| ID | Statement | Type | Tier | How to Frame |
|----|-----------|------|------|--------------|
| S5-2 | Next steps | CLAIM | SPECULATIVE | "several directions warrant investigation" |

---

## Pre-Submission Checklist

### CLAIMs
- [ ] All P0 claims at SUPPORTED or ESTABLISHED (or explicitly framed as hypothesis)
- [ ] Language matches confidence tiers throughout
- [ ] All quotes verified against source
- [ ] "Own work" claims clearly marked with status
- [ ] Hypotheses distinguished from verified claims
- [ ] No "demonstrates", "shows" or "confirms" below **ESTABLISHED** (per the DR-002 mapping above — the earlier wording said "for EMERGING or SPECULATIVE", which passed "demonstrates" at SUPPORTED, the exact defect this rule exists to catch)

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
- [ ] Novel framework components written at EMERGING or lower (not ESTABLISHED/SUPPORTED unless validated)
- [ ] No capability claims ("teachable", "assessable", "measurable") without empirical evidence

### General
- [ ] Nuances and contradictions acknowledged
- [ ] Discussion/Conclusion entries use the prose patterns (grounds → warrant → qualifier → conclusion → rebuttal)
- [ ] All entries traceable to registry IDs
- [ ] Word count within budget (3,500 target, 5,000 max)
- [ ] This paper uses the framework it describes — all claims registered and verified

---

*Created: 2026-03-03*
