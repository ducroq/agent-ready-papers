# Paper Verification & Validation Framework

<!-- Adapted from systems engineering V&V methodology.
     Treat the paper as a system requiring systematic validation. -->

**Paper:** [Title]
**Adapted from:** SU2049 Cyberphysical Systems V&V Methodology

---

## 1. Core Principle

> A paper is a system. Claims are components. Sources are tests. Reviewers are stakeholders.

Just as engineered systems require systematic V&V to ensure reliability, academic papers require systematic verification to ensure correctness and credibility.

---

## 2. V&V Mapping

| Systems Engineering V&V | Paper V&V |
|------------------------|-----------|
| System requirements | Paper goals (what must the paper demonstrate?) |
| Components | Claims (individual statements of fact/data) |
| Unit tests | Claim verification (source exists, data supports claim) |
| Test coverage | % of claims with verified sources |
| SIL classification | Claim priority (P0 / P1 / P2) |
| Static analysis | Automated checks (BibTeX, word count, structure) |
| Integration tests | Argument flow (logical coherence, no contradictions) |
| HIL testing | Expert review (co-author, domain expert) |
| Digital twin oracle | Reference documents (author guidelines, exemplar papers) |
| CI/CD pipeline | Build automation (LaTeX compile, checks) |
| Stakeholder validation | Peer review simulation |
| Traceability matrix | Claim → Evidence → Audit trail |

---

## 3. Claim Priority Classification

| Priority | Meaning | Verification Required |
|----------|---------|----------------------|
| **P0** | Core argument — paper fails without it | Must have verified source OR own data with exact location |
| **P1** | Supporting — strengthens argument | Should have ≥0.6 confidence |
| **P2** | Context/background — nice to have | ≥0.5 confidence acceptable |

### Coverage Targets

| Priority | Target |
|----------|--------|
| P0 | 100% verified |
| P1 | 90% verified |
| P2 | 70% verified |
| **Overall** | **≥85%** |

---

## 4. Test Types

### 4.1 Unit Tests (Claim-Level)

Each claim verified independently:

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

- Claims connect logically between sections
- No contradictions between sections
- Evidence supports conclusions drawn
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
- [ ] Claim registry populated
- [ ] P0 claims identified
- [ ] Data files organized

### Gate 2: Verification Complete
- [ ] P0 claims 100% verified
- [ ] P1 claims 90% verified
- [ ] Coverage report generated
- [ ] Static checks pass
- [ ] Anti-hallucination checklist complete

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
│   └── coverage_report.md   <- Overall verification coverage
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

---

*Version: 1.0*
