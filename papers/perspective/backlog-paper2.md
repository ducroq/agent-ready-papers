# Papers 2 & 3 — Backlog

Last updated: 2026-03-06

## Publication Roadmap

| Paper | Type | Scope | Status |
|-------|------|-------|--------|
| Paper 1 | Perspective | The verification gap exists; typed verification is needed | Near-complete (Gate 3) |
| Paper 2 | DSR | The typed verification artifact (CLAIM/ARGUMENT/PROPOSITION + checklists) | Not started |
| Paper 3 | Methods/Tools | SE-inspired verification pipeline — specialised subagents for empirical papers | Not started |

**Separation of concerns:**
- Paper 1 establishes the *problem* (gap in verification infrastructure)
- Paper 2 presents the *solution for reasoning* (typed verification with Toulmin/Whetten checklists)
- Paper 3 presents the *solution for quantitative content* (modular SE-inspired verification agents)

Paper 3 exists because the equation-checker discovery showed that the SE mapping is not a metaphor — it's an operational approach that produces distinct, specialised tools. That deserves its own contribution rather than being compressed into Paper 2's artifact description.

---

## Parked — Paper 2 (DSR)

### Calculation Verification as a Verification Type

**Priority:** High — this is a concrete, evidence-backed addition to the framework artifact

**Context:** The framework's three verification types (source checking for CLAIMs, Toulmin for ARGUMENTs, Whetten for PROPOSITIONs) have a blind spot: none verify arithmetic. Plausibility review can miss arithmetic errors that mechanical numerical reproduction catches. The errors survive because they produce plausible-looking results — the same fluency problem Paper 1 identifies for arguments, but in the quantitative domain.

**What to draft:**
- [ ] Position calculation verification as a fourth verification type in the DSR artifact
- [ ] Describe the equation-checker prompt (`templates/equation-checker.md`) as an artifact component
- [ ] Connect to the V-model: equation checking sits at the implementation/detailed-design boundary
- [ ] Discuss limitations: LLM arithmetic is imperfect beyond ~4 significant figures; symbolic math backends (SymPy) would strengthen this
- [ ] Frame the meta-insight: the framework's own blind spot was discovered by applying its own principle (structured > impressionistic) to a domain it hadn't considered

**Key argument (Toulmin sketch):**
- **Claim:** Calculation verification should be recognised as a distinct verification type alongside source checking, argument analysis, and proposition evaluation.
- **Grounds:** Equation errors can survive plausibility review but be caught by mechanical reproduction, sharing the property of producing plausible results.
- **Warrant:** If structured numerical reproduction catches errors that expert assessment misses, and these errors can propagate into design decisions and published claims, then numerical reproduction is a necessary verification procedure that the existing types do not cover.
- **Qualifier:** Emerging — not independently validated across domains.
- **Rebuttal:** LLM arithmetic is unreliable beyond ~4 significant figures. For high-precision work, symbolic math tools are needed. The equation-checker prompt is a starting point, not a complete solution.

---

## Parked — Paper 3 (SE Verification Pipeline)

### SE-Inspired Verification Subagents for Empirical Papers

**Priority:** High — potentially the framework's most impactful expansion

**Context:** The equation-checker discovery suggests a broader pattern. Systems engineering has decades of structured verification procedures — unit testing, integration testing, regression testing, static analysis, formal inspection, FMEA — that each catch different defect classes. The current framework maps SE concepts to papers at the *process* level (claims as components, coverage as test coverage, quality gates). But it doesn't provide *specialised verification agents* analogous to the specialised test types in SE.

The equation-checker is the first example: a prompt-based agent that performs one specific verification task (numerical reproduction) better than a general-purpose review. What other SE verification types could become paper-verification subagents?

**Candidate subagents to explore:**

| SE Verification Type | Paper Equivalent | What It Would Check | Exists? |
|---------------------|-----------------|--------------------|---------|
| Unit testing | Equation checker | Each formula reproduces from stated inputs | Yes (equation-checker.md) |
| Static analysis | Style/language checker | Confidence language matches evidence tier; terminology consistency | Partial (writing guide is manual) |
| Integration testing | Cross-section consistency | Do numbers, definitions, and claims stay consistent across sections? | No |
| Regression testing | Revision checker | Did this edit break something that was previously correct? | No |
| Boundary analysis | Edge case checker | Do claims hold at the boundaries of stated conditions? (e.g., "works for all temperatures" — does it?) | No |
| FMEA | Failure mode checker | What are the most likely ways each claim could be wrong? What's the impact? | No |
| Requirements traceability | Registry completeness | Are all assertions in the manuscript tracked in the registry? | No (manual audit) |
| Formal inspection (Fagan) | Structured peer review | Systematic review with roles (moderator, reader, recorder) simulated by agents | Partial (review-prompt.md) |
| Acceptance testing | Journal compliance | Does the manuscript meet all target journal requirements? | No |
| Configuration audit | Reference integrity | Do all citations resolve? Do DOIs match? Do figure/table references exist? | Partial (anti-hallucination.md) |

**What to draft:**
- [ ] Survey which SE verification types have plausible paper-verification analogues
- [ ] For each candidate: define the prompt, the input, and the output format
- [ ] Test 2-3 candidates on a prospective case study
- [ ] Assess which provide genuine signal vs which are redundant with existing procedures
- [ ] Design a verification pipeline: which agents run when, in what order, with what dependencies
- [ ] Frame as a V&V framework for academic papers (the SE mapping made concrete)

**Key questions:**
1. Which subagents provide the highest signal-to-noise ratio? (Equation-checker is high — what else?)
2. Can they run in parallel, or do some depend on others? (e.g., registry completeness should run before cross-section consistency)
3. How do you avoid false positives drowning the author in noise?
4. Is this better as a Paper 2 (DSR) artifact section, or as a standalone contribution?

**The meta-argument:** Paper 1 argues that structured verification beats impressionistic review for argument quality. The equation-checker demonstrates this for arithmetic. A full suite of SE-inspired subagents would demonstrate it across the entire paper verification surface. This is the SE mapping from the README made operational — not just a metaphor but a set of tools.

### Next concrete step

Build and test 2 more subagents (cross-section consistency + registry completeness) on a prospective case study. If they find real issues a manual review misses, Paper 3 has legs.

---

## Parked — Paper 2 (continued)

### LEAN as Formalization Contrast

(Carried from Paper 1 backlog)

- [ ] Position the typed verification framework on a spectrum from LEAN (fully formal, machine-checkable mathematical proofs) to nothing (current state for non-empirical papers). The framework is a pragmatic middle ground. Useful for Related Work or Discussion.
