# Paper Verification & Validation Framework

<!-- Verification & validation methodology adapted from systems engineering.
     Systematic verification of claims, sources, and argument flow. -->

**Paper:** [Title]
**Adapted from:** SU2049 Cyberphysical Systems V&V Methodology

---

## 1. Core Principle

Academic papers written with AI assistance require systematic verification to ensure correctness and credibility. The registry tracks three default unit types: **CLAIMs** (factual statements with sources), **ARGUMENTs** (reasoning chains in Discussion/Conclusion), and **PROPOSITIONs** (novel contributions and recommendations). Each needs appropriate verification and language that matches its confidence tier. For papers with quantitative content, a fourth verification procedure — **CALCULATION** (numerical reproduction) — applies alongside the registry but is tracked separately via the equation-checker tool.

For speculative-design / design-fiction / diegetic-prototype work, an opt-in fifth unit type — **PROVOCATION** (designed artefact making no truth claim) — uses Auger's four-criteria verification on a separate confidence axis (see DR-010, §4.1).

**Scope:** This framework applies to any outbound technical content — formal papers, but also informal technical communication (emails, messages, reports) containing quantitative claims, equations, or domain-specific terminology. The verification procedures scale down: a 3-equation WhatsApp message to a stakeholder benefits from equation-checker methodology just as a 68-equation theory document does.

---

## 2. V&V Structure

| Verification Layer | What It Checks |
|-------------------|----------------|
| Claim verification | Each claim has a verified source and appropriate confidence tier |
| Coverage | % of claims with verified sources, by priority |
| Static analysis | Automated checks (BibTeX, word count, structure) |
| Argument flow | Logical coherence, no contradictions between sections |
| Expert review | Co-author and domain expert feedback |
| Oracle comparison | Alignment with author guidelines and exemplar papers |
| Peer review simulation | Multi-pass structured review across model families (see [DR-011](../decisions/DR-011_multi-model-review-pattern.md)) |
| Traceability | Claim → Evidence → Audit trail |

---

## 3. Claim Priority Classification

| Priority | Meaning | Verification Required |
|----------|---------|----------------------|
| **P0** | Core argument — paper fails without it | Must have verified source OR own data with exact location; SUPPORTED or ESTABLISHED |
| **P1** | Supporting — strengthens argument | Should be EMERGING or above |
| **P2** | Context/background — nice to have | SPECULATIVE acceptable, but flag for reader |

### Coverage Targets

| Priority | Target |
|----------|--------|
| P0 | 100% verified, all SUPPORTED or ESTABLISHED |
| P1 | 90% verified, ≥90% at EMERGING or above |
| P2 | 70% verified |
| **Overall** | **≥85%** |

### Section-Level Coverage Analysis

Overall coverage can mask dramatic section-level variation. In audited projects, Discussion sections typically had 25–35% coverage while Methods/Results had 100%. This happens because Discussion sections contain ARGUMENTs and PROPOSITIONs that go unregistered when only CLAIMs are tracked.

**At Gate 2, check coverage by section type:**
- **Factual sections** (Introduction, Methods, Results): expect high CLAIM coverage
- **Interpretive sections** (Discussion, Conclusion): expect ARGUMENTs and PROPOSITIONs — if these sections show only CLAIMs, check for unregistered reasoning chains

See `claim-registry.md` "Detecting Mistyped Entries" for how to identify misclassified entries.

---

## 4. Test Types

### 4.1 Unit Tests (per registry entry)

**CLAIM** — each factual claim verified independently:

```markdown
CLAIM: "[Exact statement from paper]"
├── Source: [Author et al. Year]
├── Location: [Table X / Figure Y / Section Z / Page N]
├── Values: [exact numbers cited]
├── DOI: [doi]
└── Status: [VERIFIED / NEEDS CHECK]
```

For own data:
```markdown
CLAIM: "[Exact statement from paper]"
├── Source: Own experimental data
├── Data file: [path/to/data.csv]
├── Analysis: [path/to/script.py]
├── Figure: [Fig. N]
└── Status: [OWN DATA]
```

**ARGUMENT** — each reasoning chain verified using Toulmin checklist:

```markdown
ARGUMENT: "[Interpretive conclusion from Discussion/Conclusion]"
├── Grounds: [CLAIMs that serve as evidence — list registry IDs]
├── Warrant: [Why the evidence supports this conclusion]
├── Qualifier: [Confidence tier — how strongly stated?]
├── Counter-arguments: [Strongest objections addressed?]
└── Status: [VERIFIED / NEEDS CHECK]
```

Verification questions (adapted from Toulmin 1958, Walton 2008):
1. Is the claim clearly stated?
2. Are the grounds (evidence) verified CLAIMs in the registry? (SPECULATIVE grounds cannot support SUPPORTED or ESTABLISHED arguments)
3. Is the warrant explicit and valid for the target audience?
4. Is the qualifier calibrated to evidence strength?
5. Are the strongest counter-arguments addressed (not strawmen)?

**PROPOSITION** — each novel contribution verified using Whetten checklist:

```markdown
PROPOSITION: "[Recommendation or novel contribution]"
├── Constructs: [Key terms defined?]
├── Relationship: [What is being proposed?]
├── Reasoning: [Why this holds — logical warrant]
├── Boundary conditions: [Where does this apply? Where not?]
└── Status: [VERIFIED / NEEDS CHECK]
```

Verification questions (adapted from Whetten 1989):
1. Are all key constructs defined?
2. Is the relationship clearly stated?
3. Is the reasoning (warrant) explicit and valid?
4. Are boundary conditions specified? Check quality (see `claim-registry.md` for annotated examples):
   - [ ] Not **tautological** — boundary condition is specific, not restating the proposition ("applies when applicable")
   - [ ] Not a **moving target** — boundary condition is stable, not unfalsifiable ("unless future evidence...")
   - [ ] Not **overgeneralized** — boundary condition is bounded, not open-ended ("applies to all X")
5. Does it engage with alternative explanations?

After completing the Whetten checklist, evaluate falsifiability:
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the proposition (not circular)
- [ ] Criterion is specific enough to be measurable
- [ ] Criterion is not a moving target

**PROVOCATION** (opt-in for speculative-design / design-fiction / diegetic-prototype work; see DR-010) — each designed artefact verified using Auger's four criteria:

```markdown
PROVOCATION: "[Artefact — diegetic prototype, reflexive Ask, paradox box, etc.]"
├── Plausible: [Why a reader could hold this seriously inside the fiction]
├── Generative: [What new questions or interpretive moves it opens]
├── Reflexive: [Where the prose marker signals fictionality]
├── Ethically held: [DR-level pre-commitment; harm consideration]
├── Tier: [GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL]
└── Status: [VERIFIED / NEEDS CHECK]
```

Verification questions (adapted from Auger 2013, *Digital Creativity* 24:1):
1. Is the artefact internally consistent — could it exist in some adjacent world such that a reader holds it seriously?
2. Does subsequent prose reach into the artefact (generative) rather than around it?
3. Is a reflexive marker visible in the prose at every load-bearing moment, not only in the registry?
4. Has potential for harm been considered, with mitigations binding for chapter writing?
5. Is the tier (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) assigned, with the required prose marker present?

If the marker is absent: rewrite to add it, or downgrade to EMERGING CLAIM with additional sources. PROVOCATIONs without reflexive markers are indistinguishable from authoritative-toned hallucinations.

### 4.2 Static Analysis (Automated Checks)

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| LaTeX compiles | `pdflatex` exit code 0 | No errors |
| BibTeX valid | `biber` exit code 0 | All refs resolve |
| DOIs exist | Web lookup | All DOIs return 200 |
| Word count | `texcount` | Within journal limit |
| Data files exist | Script check | All referenced files present |
| Figures sourced | Manual check | All figures from own data or cited |

### 4.3 Integration Tests (Argument Flow)

- CLAIMs connect logically between sections
- No contradictions between sections
- ARGUMENTs in Discussion are grounded in CLAIMs from Results
- PROPOSITIONs in Conclusion follow from ARGUMENTs in Discussion
- Core argument flow is coherent end-to-end

### 4.4 System Tests (Full Paper)

- Paper achieves stated goals
- Meets journal scope and format requirements
- Abstract accurately summarizes content
- Title reflects the contribution

### 4.5 Acceptance Tests (Stakeholder)

| Stakeholder | Test |
|-------------|------|
| Co-author | Review and signoff |
| Domain expert | Technical accuracy check |
| Simulated reviewer | Multi-pass peer review across model families (see DR-011) |

---

## 5. Oracle Documents

Reference documents that define "correct" behavior:

### Specification Oracle
- **Author guidelines** — journal requirements (word count, structure, data policy)
- **Paper goals** — what the paper must demonstrate

### Behavioral Oracle
- **Exemplar papers** — successful papers in the target journal
- **Own prior work** — established methodology from published papers

### Domain Oracle
- **Reference data** — ground truth for comparison
- **Standards and guidelines** — domain-specific standards

---

## 6. Traceability

```
Paper Goal (Requirement)
    ↓
Claim (Component)
    ↓
Evidence (Source OR Data)
    ↓
Verification (Audit)
    ↓
Status (Pass / Fail)
```

---

## 7. Quality Gates

### Gate 1: Draft Complete
- [ ] All sections drafted to page budget
- [ ] Registry populated (CLAIMs, ARGUMENTs, PROPOSITIONs identified)
- [ ] P0 entries identified
- [ ] Data files organized

### Gate 2: Verification Complete
- [ ] P0 entries 100% verified (CLAIMs source-checked; ARGUMENTs Toulmin-checked; PROPOSITIONs Whetten-checked)
- [ ] P1 entries 90% verified
- [ ] Coverage checked by section type (see Section 3 — Section-Level Coverage Analysis)
- [ ] Entry types re-checked (see `claim-registry.md` — Detecting Mistyped Entries)
- [ ] Coverage report generated from registry dashboard (timestamped snapshot for co-author review)
- [ ] Static checks pass
- [ ] Anti-hallucination checklist complete

### Gate 2.5: Internal Consistency
- [ ] All statistics in appendices cross-checked against main text values
- [ ] Date citations consistent (same year for same source throughout)
- [ ] Numerical values in tables match claims in prose
- [ ] No data present only in appendix without main text reference (or vice versa)

### Gate 2.6: Reflexivity (conditional — applies when PROVOCATIONs are present)

For projects with PROVOCATION entries (see DR-010). Skip entirely if the registry contains none.

- [ ] Walk every PROVOCATION in the registry
- [ ] For each one, locate the required prose marker for its tier (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) in the manuscript itself, not only in the registry
- [ ] Marker is present at every load-bearing moment, not only on first introduction
- [ ] No authoritative-toned speculation slides silently into apparent claim
- [ ] Entries failing this audit are rewritten (marker added) or downgraded to EMERGING CLAIM with additional sources

### Gate 2.7: Ethical Review (conditional — applies when the project engages contested topics)

For projects engaging actively contested ethical territory — political, religious, identity-based, or otherwise. Skip if the work does not engage such cases.

- [ ] No real-world group is pathologised in the author's voice
- [ ] Harm consideration is documented in a DR or equivalent pre-commitment
- [ ] Treatment is symmetric across the contested traditions in the work (no asymmetric scrutiny)
- [ ] Reviewer composition for the contested chapters matches the traditions discussed (the work is reviewed by readers from each)
- [ ] Project-specific operational rules from the contested-topic DR (e.g., paired-mirror rules, vocabulary substitution policies) are applied chapter by chapter

See `audits/feedback-from-fsd.md` Tier 1 item 3 for the source pattern; project-specific operational rules belong in a DR per the project's `decision-record.md` template.

### Gate 2.8: Voice Consistency (conditional — applies when the work has a voice-driven register)

For voice-driven work — books, essays, perspective pieces, or any work where the manuscript's register is itself part of the contribution. Standard academic-prose papers can skip this gate.

- [ ] The project has a defined voice manifest (e.g., a voice-policy DR or section in the project CLAUDE.md)
- [ ] The manifest is binding for every chapter, not only the opening
- [ ] No drift into modes the manifest excludes (e.g., academic hedging, tweet-thread snark, righteous register)
- [ ] Read-aloud test passes — the manuscript reads coherently in the manifest's register
- [ ] Drift detected during the read-aloud is logged and resolved before proceeding to Gate 3

### Gate 3: Review Complete
- [ ] Co-author signoff
- [ ] Simulated peer review ≥3.5/5.0
- [ ] Language matches confidence levels

### Gate 4: Submission Ready
- [ ] All gates passed
- [ ] Journal requirements met
- [ ] Final proofread complete
- [ ] Data availability prepared
- [ ] Author agreement signed

---

## 8. Folder Structure

```
vv/
├── PAPER_VV_FRAMEWORK.md    <- This file
├── claims/
│   └── claim_registry.md    <- All claims with priority & status
├── audits/
│   ├── section_X_audit.md   <- Per-section claim audits
│   └── coverage_report.md   <- Timestamped verification snapshot (see note below)
├── oracles/
│   ├── author_guidelines.md <- Journal requirements
│   └── exemplar_papers.md   <- Reference successful papers
├── tests/
│   ├── static_checks.md     <- Automated check results
│   └── build_log.md         <- LaTeX/BibTeX build results
└── validation/
    ├── coauthor_review.md   <- Co-author feedback
    └── reviewer_checklist.md<- Simulated peer review results
```

**Coverage report vs. registry dashboard:** The coverage report (`coverage_report.md`) is a timestamped snapshot for co-author review and submission audit. The claim registry dashboard is the living working document. Generate the coverage report from the registry dashboard before each quality gate review. The registry dashboard changes daily; the coverage report captures a specific point-in-time verification state.

---

*Version: 2.4 — v2.1: Gate 2.5, PROPOSITION boundary condition quality criteria, falsification checklist, Toulmin grounds tier constraint (DR-004 Issues #1–#4). v2.2: scope note (informal technical communication), section-level coverage analysis, mistype re-check in Gate 2, full reflection pass (2026-03-16). v2.3: PROVOCATION as opt-in fifth unit type for speculative-design work (DR-010, 2026-05-10). v2.4: project-conditional Gates 2.6 (Reflexivity), 2.7 (Ethical Review), 2.8 (Voice Consistency) added (2026-05-10, FSD audit Tier 1 items 3+4).*
