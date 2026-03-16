# Paper Verification & Validation Framework

<!-- Verification & validation methodology adapted from systems engineering.
     Systematic verification of claims, sources, and argument flow. -->

**Paper:** [Title]
**Adapted from:** SU2049 Cyberphysical Systems V&V Methodology

---

## 1. Core Principle

Academic papers written with AI assistance require systematic verification to ensure correctness and credibility. The registry tracks three unit types: **CLAIMs** (factual statements with sources), **ARGUMENTs** (reasoning chains in Discussion/Conclusion), and **PROPOSITIONs** (novel contributions and recommendations). Each needs appropriate verification and language that matches its confidence tier.

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
| Peer review simulation | Structured review in a fresh session |
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
2. Are the grounds (evidence) verified CLAIMs in the registry?
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
4. Are boundary conditions specified? Check quality:
   - [ ] Boundary condition is specific (not tautological — "applies when applicable")
   - [ ] Boundary condition is stable (not a moving target — "unless future evidence...")
   - [ ] Boundary condition is bounded (not overgeneralized — "applies to all X")
5. Does it engage with alternative explanations?

Falsification criteria quality checklist (for each PROPOSITION):
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the proposition (not circular)
- [ ] Criterion is specific enough to be measurable
- [ ] Criterion is not a moving target

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
| Simulated reviewer | Structured peer review (fresh session) |

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
- [ ] Coverage report generated from registry dashboard (timestamped snapshot for co-author review)
- [ ] Static checks pass
- [ ] Anti-hallucination checklist complete

### Gate 2.5: Internal Consistency
- [ ] All statistics in appendices cross-checked against main text values
- [ ] Date citations consistent (same year for same source throughout)
- [ ] Numerical values in tables match claims in prose
- [ ] No data present only in appendix without main text reference (or vice versa)

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

*Version: 2.0 — updated with ARGUMENT and PROPOSITION unit types (DR-004)*
