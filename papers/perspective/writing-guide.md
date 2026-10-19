# Writing Guide: Registry-to-Section Mapping

<!-- Maps registry entries (claims, contribution C1, declared starting points D1-D8) to
     draft 2's sections with language calibration. Consult before writing or editing any
     section. Terms: glossary.md, which links to ../../docs/glossary.md (DR-027, DR-028).
     The registry is the source of truth for tiers: re-derive these tables from it, never
     edit a tier here by hand. -->

**Paper:** The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing
**Last Updated:** 2026-10-16 (rebuilt for draft 2 and the DR-027 registry). Earlier history: git log.

---

## How to Use This Guide

1. **Before writing a section:** Check which registry entries apply (claims, C1, D rows)
2. **For each claim:** Choose a qualifier its confidence tier permits
3. **For `src:` grounds:** Source details are in `vv/claims/claim_registry.md`
4. **For `claim:` grounds:** Make the warrant explicit; every claim it rests on must be checked
5. **For normative claims (C1, S5-2):** Name the value (D1, D7) and state the boundary conditions
6. **For declared starting points:** State each one in the text; definitions also go in `glossary.md`
7. **For quotes:** Keep a key quotes file for verbatim text

---

## Language Calibration

| Confidence Tier | Language |
|-----------------|----------|
| ESTABLISHED | "demonstrates", "shows", "confirms", "established" |
| SUPPORTED | "indicates", "supports", "evidence suggests" |
| EMERGING | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | "warrants investigation", "remains unclear", "we hypothesize" |

### The Underlying Principle

The rules in this guide are instances of one structural requirement: **the language tier used in the manuscript must be at most the confidence tier in the registry for the same claim.** Citation drift, overclaiming, and inverse hallucination (Step Z) are all the same failure: language climbing one or more tiers above what the evidence chain supports. A reviewer's first check on any load-bearing claim is whether the language sits at or below the registered tier; if it does not, either the registry needs upgrading (with new evidence) or the language needs downshifting. (Propagated from `templates/writing-guide.md` per DR-017.)

### Writing a Claim

| Grounds | How to write it | Watch for |
|---------|----------------|-----------|
| `src:` (sources) | State what the source reports, cite it, match the qualifier to the tier | Overclaiming (confident language for EMERGING/SPECULATIVE) |
| `claim:` (other claims) | Present the grounds, make the warrant explicit, then state the claim | Implicit warrants the reader won't share; missing objections |
| `decl:` (declared starting points) | State the definition, assumption or value as adopted, not argued | A contested starting point presented as settled |
| `own:` (own work) | Say what was observed and how; call it an observation | An informal trial written as a measured result (S1-5) |
| Normative claim | State the recommendation, name the value it serves, say where it applies | Overgeneralization; missing boundary conditions |

**Prose pattern for a claim on `claim:` grounds:**
> [Grounds: the claims it rests on, each checked]. [Warrant: why they lead to the claim]. [Qualifier: hedging per confidence tier]. [Therefore, the claim]. [Rebuttal: when the step fails, and the strongest objection].

Example (S3-4, draft 2 §3): "If a claim is checked by a procedure that does not fit what it rests on, the check **may** fail it for the wrong reason: an inference judged by whether it has a source looks unsupported even when its reasoning holds. Recording each claim's grounds item by item, and letting the kind of grounds decide the check, **may** avoid such false failures. The argument rests on design reasoning and on this paper's own registry; it has not been tested across authors or fields."

**Prose pattern for a normative claim:**
> [Warrant: why the recommendation follows from its grounds and the value it serves]. [The recommendation itself]. [Boundary conditions: where it applies and where it doesn't].

Example (C1, draft 2 §5): "I propose that the scholarly community develop verification infrastructure for non-empirical papers, as EQUATOR did for empirical health research. The value behind the proposal is that published reasoning should be checkable (D1) ... The proposal applies to academic papers whose contribution is an argument, and to the interpretive parts of empirical papers."

### Framework Component Language: Special Case

This paper **proposes** a procedure built on Toulmin and Whetten. Its components are EMERGING until empirically validated, even when the supporting evidence is strong. The procedure is an interpretation of evidence, not the evidence.

| Anti-pattern | Correct pattern |
|-------------|----------------|
| "Our framework demonstrates..." | "We propose..." |
| "The model shows..." | "The framework posits..." |
| "Each kind of grounds NEEDS its own check" | "The procedure lets the kind of grounds decide the check" |

Confidence progression for framework components:
- **SPECULATIVE** → conjectural, no supporting evidence
- **EMERGING** → novel contribution, supporting evidence but no empirical validation of the framework itself
- **SUPPORTED** → initial validation (pilot studies, case studies)
- **ESTABLISHED** → independent replication

**Key rule:** Capability claims ("teachable," "assessable," "measurable") require evidence of teaching/assessment, not just logical inference from the framework.

### Special Cases

| Situation | Language |
|-----------|----------|
| Own work (under review) | "we observed", "our findings indicate"; never "it was found" |
| Own work (published) | "we previously demonstrated" with citation |
| Own observation in this paper (`own:`) | "In informal trials on my own projects, ..."; "this is an observation, not a measured result" |
| Logical inference | "If [premises], then [conclusion]"; mark as inference |
| Single study | "In a study of N=X, [Author] found..."; note sample size |
| Contradictory evidence | "While [Author1] reported X, [Author2] found Y"; acknowledge both |
| Negative claims | "I found no X"; search and document the null result |
| Adaptation of a source | "Using his layout as a checklist is my adaptation"; "The mapping is mine" |

---

## Section → Registry Mapping

### 1. Polished prose, unchecked reasoning

**Purpose:** AI-assisted prose can be fluent and cite only real sources while its reasoning is weak (S1-7). Existing tools check evidence; none found checks warrants or chooses the check by what a claim rests on.

**Entries to use:**

| ID | Statement | Says / Grounds | Tier | Appropriate Language |
|----|-----------|----------------|------|---------------------|
| D4 | "AI-augmented writing": drafting and revision assisted by general-purpose LLMs | definition, accepted | none | "In this paper 'generative AI tools', or 'AI' for short, means these assistants" |
| S1-7 | Fluent, well-cited prose can carry weak reasoning (P1) | descriptive / `claim:` S1-1, S1-2, S1-4 | EMERGING | "can read as polished and complete while it contains errors that only checking would reveal" |
| S1-1 | Citation hallucination is a distinct failure mode (P0) | descriptive / `src:` ×2 | SUPPORTED | Report the figures with attribution ("found that 62–89% ... were fabricated"); never "demonstrates" |
| S1-2 | Confidence inflation (P0) | descriptive / `src:` ×4 | SUPPORTED | "The evidence indicates that LLMs verbalise high confidence ..."; booster clause "unsettled" |
| S1-5 | Recomputation caught errors that soundness review missed (P1) | descriptive / `own:` | SPECULATIVE | "warrants investigation"; "this is an observation, not a measured result" |
| S1-4 | Existing tools check evidence, not warrants (P1) | descriptive / `src:` ×4 + Warrant | EMERGING | Name Samsonau, Chen, Zhou & Yu, VANRA first; "None that I found asks ..." |
| S1-6 | Detection is no substitute for verification (P2) | descriptive / `decl:` D5 + `src:` ×2 | EMERGING | Lead with D5; "have proved fragile in tests", "varies", "can collapse"; never "shows" |
| D5 | Detection asks who wrote a text; verification asks whether it holds | definition, own | none | State as the paper's distinction |

**Cautions:**
- Do NOT frame this as "AI is bad for writing"; frame it as new failure modes that need new checks
- S1-1 and S1-2 are SUPPORTED: "indicates", "evidence suggests", never "demonstrates"
- S1-4 is a hedged negative about prior art. Name the systems and state precisely what they lack. Never write "no process-level infrastructure exists"
- Reference model/tool level solutions generically (citation checkers, RAG); specific tool names were removed as uncitable

---

### 2. What reporting guidelines cover

**Purpose:** EQUATOR covers empirical health research; guidance for papers without new data is scattered and seems not to reach the reasoning. Gregor's theory types suggest the gap may be structural.

**Entries to use:**

| ID | Statement | Says / Grounds | Tier | Appropriate Language |
|----|-----------|----------------|------|---------------------|
| S2-1 | EQUATOR lists ~700 reporting guidelines (P0) | descriptive / `src:` | SUPPORTED | "which lists about 700 reporting guidelines for health research" (699 on 2026-03-03, 704 on 2026-09-14) |
| S2-2 | No consensus checklist found for verifying the reasoning of non-empirical papers (P0) | descriptive / `src:` ×6 + Warrant | EMERGING | "seems not to reach the reasoning"; "I found no consensus checklist"; SIGSOFT standards ask for valid arguments "but give no procedure for checking them" |
| S2-3a | Gregor's taxonomy has five theory types (P1) | descriptive / `src:` | SUPPORTED | "distinguishes five types of theory" (attribution) |
| S2-3b | Type I and V contributions are largely non-empirical (P1) | descriptive / `claim:` S2-3a | EMERGING | "may not be checkable against an earlier source" |
| D3 | "Non-empirical paper": main contribution is reasoning, not new data; examples, not a closed list | definition, own | none | "examples of non-empirical papers in this sense; the list is not a classification" |
| S2-4 | Argument quality as the main challenge (P1) | descriptive / `src:` ×2 + Warrant | EMERGING | "I suggest that ... the main question may be less ..." |

**Cautions:**
- S2-1 count: 699 guidelines (2026-03-03); rounded to "about 700" in the manuscript
- S2-2 is a hedged negative; design science has two agreeing sources, conceptual one, theoretical and perspective none
- Frame the gap as an *opportunity*, not a criticism of EQUATOR

---

### 3. A vocabulary from Toulmin and Whetten

**Purpose:** Present the vocabulary (Box 1) and the procedure: register each claim with what it rests on, check each item by its kind, check the contribution once. Table 1 gives the confidence tiers.

**Entries to use:**

| ID | Statement | Says / Grounds | Tier | Appropriate Language |
|----|-----------|----------------|------|---------------------|
| S3-5 | Toulmin's layout, its jurisprudential origin, his later disclaimer (P1) | descriptive / `src:` | SUPPORTED | Quote with page numbers; attribution verbs |
| S3-1 | Toulmin's layout can be operationalised for verification (P1) | descriptive / `src:` ×2 + Warrant | EMERGING | "That adaptation may be workable"; Gupta is "extraction and not yet verification" |
| S3-2 | Whetten's criteria may check the contribution, once (P1) | descriptive / `src:` + Warrant | EMERGING | "they may serve best as a check of the paper's central contribution" |
| D8 | Claim checks are verification; the contribution check is validation | assumption, own | none | "is closer to validation. The mapping is mine." |
| S3-6 | Fixed certainty wording has precedents (P1) | descriptive / `src:` ×3 | SUPPORTED | Attribute each precedent (Kent, IPCC, GRADE) |
| S3-3 | Mapping tiers to qualifiers may help authors notice overclaiming (P1) | descriptive / `claim:` S3-6 + `decl:` D6 | EMERGING | "It may still help an author notice ..."; say the tier rule is untested with readers |
| D6 | The tier-to-wording mapping is this paper's proposal | assumption, own | none | "Table 1 adapts this practice" |
| S3-4 | Each claim needs the checks its grounds call for (P0) | descriptive / `claim:` S3-1, S3-2, S3-5 + `own:` | EMERGING | "may fail it for the wrong reason", "may avoid such false failures"; state that it is untested across authors |

**Warrant check for S3-4:**
- Warrant: if a claim is checked by a procedure that does not fit its grounds, an inference judged by whether it has a source looks unsupported even when its reasoning holds; recording grounds item by item lets the kind of grounds choose the check.
- Grounds: S3-1, S3-2, S3-5, and the own trial migration of this paper's registry.
- Qualifier: EMERGING. Reasoned from its grounds; no cross-author replication.

**Cautions:**
- Present Toulmin and Whetten as *established frameworks applied to a new task*, not as new contributions
- S3-4 is the paper's central claim: present it with its warrant, not as self-evident
- Say where the paper adapts a source ("my adaptation", "the mapping is mine")

---

### 4. What this does not settle

**Purpose:** Name what the vocabulary leaves open: judging warrants, the role of tools, the simplified tier rule, one user so far.

**Entries to use:**

| ID | Statement | Says / Grounds | Tier | Appropriate Language |
|----|-----------|----------------|------|---------------------|
| S4-5 | Argument-quality research offers more structure (P1) | descriptive / `src:` ×2 | SUPPORTED | Attribute: Wachsmuth et al. "distinguish"; Walton's schemes "which their publisher describes as" |
| S4-3 | Structure plus LLMs may outperform LLMs alone (P1) | descriptive / `src:` ×2 + Warrant | EMERGING | "Both are narrow tasks, so they suggest only that ... may outperform" |

**Cautions:**
- Each of S4-3's sources covers one narrow task; do not generalise to "verification"
- Do not reintroduce the withdrawn audit figures (S4-1, S4-2, S4-4, withdrawn 2026-09-26, #38)

---

### 5. A proposal for authors and journals

**Purpose:** The paper's contribution (C1), with its value, boundary conditions and the objection from peer review, then next steps.

**Entries to use:**

| ID | Statement | Says / Grounds | Tier | Appropriate Language |
|----|-----------|----------------|------|---------------------|
| C1 | The community needs verification infrastructure for non-empirical papers (contribution, P0) | normative / `claim:` S1-7, S2-1, S2-2, S3-4 + `decl:` D1–D4 | EMERGING | "I propose that ..."; use the normative prose pattern |
| D1 | Published reasoning should be checkable | value, accepted | none | "The value behind the proposal is that ..." |
| D2 | "Verification infrastructure": process-level reporting plus scaffolding analogous to EQUATOR | definition, own | none | Define at first use |
| S5-2 | Next steps (P2) | normative / `claim:` S4-3, S3-1 + `decl:` D7 | SPECULATIVE | "Several directions warrant investigation" |
| D7 | A proposal should be tested before it is adopted | value, accepted | none | Implicit in "does not show that the way works" (§4) |

**Boundary check for C1:**
- Applies to: academic papers whose contribution is an argument, and the interpretive parts of empirical papers
- Untested for: other writing that asks readers to trust its reasoning, journalism among them
- Limit: Toulmin's and Whetten's frameworks come from Western academic traditions
- Objection engaged: peer review already judges arguments. Response: a register would not replace it; it could help authors find weak steps before submission and help reviewers see where a paper's weight rests

**Cautions:**
- C1 fails the P0 tier floor (EMERGING); Section 5 says so. Do not raise its language to compensate
- Do NOT frame as "everyone must adopt this"; frame as "the community should develop this"
- S5-2 is SPECULATIVE: "warrants investigation", not "should" or "will"

---

## Quick Reference: All Entries by Tier

### ESTABLISHED / SUPPORTED: Ready for Strong Statements

*Re-derive from the claim registry; never edit tiers here by hand.* No entry is ESTABLISHED in draft 2.

| ID | Statement | Says | Tier | Best Source |
|----|-----------|------|------|------------|
| S1-1 | AI citation hallucination | descriptive | SUPPORTED | Mugaanyi 2024; Walters & Wilder 2023 |
| S1-2 | Confidence inflation | descriptive | SUPPORTED | Xiong 2024; Zhou 2024; Peters & Chin-Yee 2025 |
| S2-1 | EQUATOR ~700 guidelines | descriptive | SUPPORTED | EQUATOR website (699, 2026-03-03) |
| S2-3a | Gregor's five theory types | descriptive | SUPPORTED | Gregor 2006 |
| S3-5 | Toulmin's layout and its origin | descriptive | SUPPORTED | Toulmin 2003 |
| S3-6 | Calibrated-language precedents | descriptive | SUPPORTED | Kent 1964; Mastrandrea 2010; Santesso 2020 |
| S4-5 | Argument-quality research | descriptive | SUPPORTED | Wachsmuth 2017; Walton 2008 |

### EMERGING: Appropriately Hedged

| ID | Statement | Says | Tier | Hedging Language |
|----|-----------|------|------|------------------|
| S1-4 | Existing tools check evidence, not warrants | descriptive | EMERGING | "None that I found asks ..." |
| S1-6 | Detection is no substitute | descriptive | EMERGING | "have proved fragile in tests" |
| S1-7 | Fluent prose, weak reasoning | descriptive | EMERGING | "can read as polished ... while" |
| S2-2 | No consensus checklist for reasoning | descriptive | EMERGING | "I found no consensus checklist" |
| S2-3b | Types I and V largely non-empirical | descriptive | EMERGING | "may not be checkable" |
| S2-4 | Argument quality as the main challenge | descriptive | EMERGING | "may be less ... and more" |
| S3-1 | Toulmin operationalisable | descriptive | EMERGING | "may be workable" |
| S3-2 | Whetten checks the contribution | descriptive | EMERGING | "may serve best as" |
| S3-3 | Tiers may help notice overclaiming | descriptive | EMERGING | "may still help" |
| S3-4 | Checks follow the grounds | descriptive | EMERGING | "may fail it", "may avoid" |
| S4-3 | Structure + LLM > LLM alone | descriptive | EMERGING | "suggest only that ... may" |
| C1 | Community needs infrastructure | normative (contribution) | EMERGING | "I propose that" |

### SPECULATIVE: Requires Careful Framing

| ID | Statement | Says | Tier | How to Frame |
|----|-----------|------|------|--------------|
| S1-5 | Recomputation caught missed errors | descriptive | SPECULATIVE | "an observation, not a measured result" |
| S5-2 | Next steps | normative | SPECULATIVE | "several directions warrant investigation" |

---

## Pre-Submission Checklist

### Every claim
- [ ] All P0 claims and C1 at SUPPORTED or ESTABLISHED. Where not (C1, S2-2, S3-4 are EMERGING), Section 5 says so and the gate records the failure; framing does not waive the floor
- [ ] Language matches confidence tiers throughout
- [ ] All quotes verified against source
- [ ] "Own work" claims clearly marked with status
- [ ] Hypotheses distinguished from verified claims
- [ ] No "demonstrates", "shows" or "confirms" below **ESTABLISHED** (per the DR-002 mapping above; the earlier wording said "for EMERGING or SPECULATIVE", which passed "demonstrates" at SUPPORTED, the exact defect this rule exists to catch)

### Claims on `claim:` grounds
- [ ] Each has its warrant stated explicitly (not left implicit)
- [ ] Its grounds are checked claims in the registry (not unregistered assertions)
- [ ] Qualifier matches the weakest grounds in the chain
- [ ] Strongest objections acknowledged (not strawmen)
- [ ] None rests solely on SPECULATIVE claims without flagging

### Declared starting points
- [ ] D1–D8 each stated in the text; definitions also in `glossary.md`
- [ ] A claim resting on a contested one says so

### Normative claims and the contribution
- [ ] C1 and S5-2 have boundary conditions stated and name the value they serve
- [ ] Key concepts are defined as declared starting points (not assumed)
- [ ] Reasoning is explicit (not "it follows that..." without warrant)
- [ ] Objections engaged with
- [ ] Scope not overgeneralized beyond what the grounds support
- [ ] Novel framework components written at EMERGING or lower (not ESTABLISHED/SUPPORTED unless validated)
- [ ] No capability claims ("teachable", "assessable", "measurable") without empirical evidence

### General
- [ ] Nuances and contradictions acknowledged
- [ ] Claims on `claim:` grounds use the prose pattern (grounds → warrant → qualifier → claim → rebuttal)
- [ ] All entries traceable to registry IDs
- [ ] Word count within budget (3,500 target, 5,000 max)
- [ ] This paper uses the framework it describes: all claims registered and verified

---

*Created: 2026-03-03*
