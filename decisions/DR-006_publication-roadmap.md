# DR-006: Publication Roadmap — Writing About the Framework

---
status: Accepted
date: 2026-03-02
---

## Context

The research conducted for DR-004 revealed a concrete, publishable gap: EQUATOR Network maintains ~500 reporting guidelines for empirical health research; essentially zero exist for non-empirical paper types or for AI-augmented writing verification. This project is the first to address that gap with process-level verification infrastructure.

The project has sufficient raw material for publication:
- A quantifiable landscape gap (EQUATOR)
- An artifact (typed verification registry with Toulmin/Whetten checklists)
- Evaluation evidence from three real paper projects (IEEE TIM, MST, medical education)
- 47 indexed literature sources
- Five decision records documenting design rationale
- A methodology narrative (patterns extracted, cross-validated, generalized)

The framework will be used to write the papers about the framework.

## Publication Strategy

Two papers, sequenced to build on each other:

### Paper 1: Perspective / Short Communication

**Working title:** "The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines Beyond Citation Checking"

**Core argument:** AI writing tools are proliferating, citation checkers exist, but the scholarly infrastructure for verifying *argument quality* — not just factual accuracy — is missing. EQUATOR covers empirical papers; nothing covers the rest. We propose a typed verification model.

**Target venues (in order of preference):**

| Venue | Fit | Format | Typical length |
|-------|-----|--------|---------------|
| Learned Publishing | Scholarly communication infrastructure | Perspective | 3,000-5,000 words |
| Research Integrity and Peer Review (BMC) | AI integrity, verification methods | Commentary | 2,000-4,000 words |
| European Science Editing | Editorial/publishing practice | Short communication | 2,000-3,000 words |
| Accountability in Research | Research integrity, AI writing | Perspective | 3,000-5,000 words |

**Structure:**
1. The problem: AI writing failure modes beyond citation hallucination (confidence inflation, argument validity, scope creep)
2. The landscape gap: tool-level and model-level solutions exist; process-level is missing; EQUATOR covers empirical only
3. The proposal: typed verification registry (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists
4. Preliminary evidence: patterns extracted from three real projects
5. Call to action: the scholarly community needs verification infrastructure for AI-augmented writing

**Registry units:** Mostly CLAIMs (landscape data, EQUATOR statistics) + 2-3 ARGUMENTs (the gap interpretation) + 1 PROPOSITION (the call to action)

**Timeline:** Can be drafted quickly — most content exists in README, DR-004, and literature folder.

### Paper 2: Design Science Research Article

**Working title:** "Verification Infrastructure for AI-Augmented Academic Writing: A Design Science Approach"

**Core argument:** We present a designed artifact — a verification framework with typed registries, confidence-calibrated language mapping, quality gates, and anti-hallucination checklists — developed and evaluated across three paper projects. The artifact addresses the gap identified in Paper 1.

**Target venues (in order of preference):**

| Venue | Fit | Format | Typical length |
|-------|-----|--------|---------------|
| JAIS | Design science, IS methodology | DSR article (Peffers DSRM) | 12,000-15,000 words |
| EJIS | European IS, methodology innovation | Research article | 10,000-12,000 words |
| Scientometrics | Quantitative scholarly infrastructure | Research article | 8,000-10,000 words |
| Journal of Information Technology | IT artifacts, design theory | DSR article | 10,000-12,000 words |

**Structure (Peffers et al. 2007 DSRM):**
1. Problem identification: AI writing failure modes + EQUATOR gap
2. Objectives: process-level verification for claims, arguments, propositions
3. Design & development: the framework (registry, confidence tiers, anti-hallucination, quality gates, Toulmin/Whetten checklists)
4. Demonstration: application to three paper projects
5. Evaluation: coverage metrics, hallucination catch rate, reviewer feedback, cross-project pattern validation
6. Communication: this paper

**Registry units:** Full mix of CLAIMs (literature, evaluation data), ARGUMENTs (interpretation of results), PROPOSITIONs (design principles, generalizability claims), and DESIGN PRINCIPLEs (activating DR-004's reserved types)

**Evaluation evidence available:**
- EngineeringFidelity (MST): V&V framework, claim registry, quality gates
- Proposition (medical education): confidence scoring, language mapping, 7 decision records
- Technology Paper (IEEE TIM): architecture blueprint, peer review simulation (scored 4.4/5.0)
- Cross-project pattern extraction: 7 common patterns, 3 complementary, project-specific excluded

**Timeline:** After Paper 1 is submitted. Requires gathering additional evaluation metrics from the three source projects.

### Paper 3: SE-Inspired Verification Pipeline (Methods/Tools)

**Added:** 2026-03-06. Motivated by the discovery that the equation-checker prompt (a single SE-inspired verification agent) caught 3/3 arithmetic errors that a general-purpose review missed. If one specialised agent works this well, a modular suite of them — each targeting a different defect class — could provide comprehensive verification coverage for empirical and technical papers.

**Working title:** TBD — "Verification Agents for AI-Augmented Academic Writing: An SE-Inspired Pipeline" or similar

**Core argument:** Systems engineering verification types (unit testing, integration testing, regression testing, static analysis, FMEA) can be mapped to paper-verification subagents. Each agent is a prompt, not a program — specialised instructions that force an LLM into a specific verification mode. The equation-checker is the proof of concept; the paper presents a suite tested on real papers.

**Target venues:** TBD — depends on results. Could be software engineering (EMSE, JSS), scholarly communication (Learned Publishing), or AI tools (similar venues to Paper 2).

**Depends on:** Building and testing 2-3 more subagents beyond the equation-checker.

**Evidence:** `audits/equation-verification-journey.md`, `papers/perspective/backlog-paper2.md` (candidate subagent table)

## Sequencing

```
Paper 1 (perspective)     Paper 2 (DSR)              Paper 3 (methods/tools)
├── Establishes gap       ├── Cites Paper 1          ├── Cites Papers 1 & 2
├── Proposes model        ├── Full artifact           ├── Specialised agents
├── Quick to publish      ├── Rigorous evaluation     ├── Empirical + technical focus
└── Plants the flag       └── Design theory           └── Operational SE mapping
```

Paper 1 establishes the territory (Swales Move 1) and the niche (Move 2). Paper 2 occupies the niche (Move 3) with the typed verification artifact. Paper 3 extends the SE mapping from metaphor to operational tooling, focused on quantitative and empirical content where Paper 2's argument-level verification is necessary but insufficient.

**Separation of concerns:**
- Paper 1: the *problem* (verification gap)
- Paper 2: the *solution for reasoning* (typed verification)
- Paper 3: the *solution for quantitative content* (modular verification agents)

## Meta: Using the Framework

Both papers will be written using the agent-ready-papers framework itself:
- CLAUDE.md for each paper project
- Claim registry with typed entries
- Confidence-to-language mapping
- Anti-hallucination checklist for all AI-introduced citations
- Quality gates before submission
- Decision records for scope choices
- Peer review simulation in a fresh session

This serves as both methodology and additional evaluation evidence ("the framework was used to write the paper describing the framework, and the process surfaced N issues that would have been missed without it").

## Consequences

- Create a `papers/` directory (or separate repos) for each paper project when writing begins
- Paper 1 can be drafted from existing material (README, DRs, literature folder)
- Paper 2 requires going back to the three source projects for quantitative evaluation data
- Both papers need co-author(s) — domain expertise in scholarly communication or IS methodology
- The literature folder (47 sources) serves as the starting point for related work in both papers

## Revisit If

- Paper 1 is rejected — reconsider venue selection or reframe the argument
- A competing publication addresses the EQUATOR gap before Paper 1 is submitted — pivot to differentiation
- The DSR paper (Paper 2) needs more evaluation evidence — consider adding a fourth paper project as a prospective case study
- The podcast/creative writing pivot happens — consider extending verification to non-academic structured content
- Paper 3 subagent testing shows low signal-to-noise — fold best results into Paper 2 instead of a separate paper
