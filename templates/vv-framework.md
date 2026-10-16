# Paper Verification & Validation Framework

<!-- Verification & validation methodology adapted from systems engineering.
     Systematic verification of claims, sources, and argument flow. -->

**Paper:** [Title]
**Adapted from:** SU2049 Cyberphysical Systems V&V Methodology

---

## 1. Core Principle

Academic papers written with AI assistance require systematic verification to ensure correctness and credibility. The registry follows DR-027's model (terms: `docs/glossary.md`). Every statement the paper puts forward and supports is a **claim**. Each claim records what it says (descriptive or normative) and its grounds, item by item: sources, other claims, declared starting points, or the author's own work. The checks follow the items, and each claim's qualifier must stay within its confidence tier. Each **contribution** is a root claim, checked once with Whetten's elements and questions. The per-claim checks are **verification**; the contribution check is **validation**. For claims whose grounds include a computation, **calculation verification** (numerical reproduction, DR-009) applies, using the equation-checker; it is a procedure, not a registry unit.

For speculative-design / design-fiction / diegetic-prototype work, an opt-in table of **provocations** (designed artefacts making no truth claim) uses Auger's four-criteria verification on a separate confidence axis (see DR-010, §4.1).

**Scope:** This framework applies to any outbound technical content — formal papers, but also informal technical communication (emails, messages, reports) containing quantitative claims, equations, or domain-specific terminology. The verification procedures scale down: a 3-equation WhatsApp message to a stakeholder benefits from equation-checker methodology just as a 68-equation theory document does.

---

## 2. V&V Structure

| Verification Layer | What It Checks |
|-------------------|----------------|
| Claim verification | Each claim passes the checks its grounds call for and has an appropriate confidence tier |
| Contribution validation | Each contribution passes the contribution check (Whetten) |
| Coverage | % of claims whose checks are complete, by priority |
| Static analysis | Automated checks (BibTeX, word count, structure) |
| Argument flow | Logical coherence, no contradictions between sections |
| Expert review | Co-author and domain expert feedback |
| Oracle comparison | Alignment with author guidelines and exemplar papers |
| Peer review simulation | Multi-pass structured review across model families (see [DR-011](../decisions/DR-011_multi-model-review-pattern.md)) |
| Traceability | Contribution → claims → grounds → sources (§6) |

---

## 3. Claim Priority Classification

| Priority | Meaning | Verification Required |
|----------|---------|----------------------|
| **P0** | Core argument: paper fails without it. Every contribution is P0 | Checks complete for every grounds item (`own:` items with exact location); SUPPORTED or ESTABLISHED, a contribution no higher than its weakest supporting claim |
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

Overall coverage can mask dramatic section-level variation. In the two audited projects, Discussion-section coverage ran far below Methods/Results. (This previously gave "typically 25–35%" against 100% — a band drawn from two data points whose underlying audits were removed from the repo in v2.0.0, so no reader can reproduce it. Treat the pattern as directional; measure your own sections rather than checking against a number.) This happens because Discussion sections hold claims resting on other claims, and recommendations, that go unregistered when only sourced statements are tracked.

**At Gate 2, check coverage by section type:**
- **Factual sections** (Introduction, Methods, Results): expect mostly claims on `src:` and `own:` grounds, with high coverage
- **Interpretive sections** (Discussion, Conclusion): expect claims on `claim:` grounds and normative claims. If these sections show only `src:` grounds, check for unregistered reasoning

See `claim-registry.md` "Checks → Recording grounds" for how to spot misrecorded grounds.

---

## 4. Test Types

### 4.1 Unit Tests (per registry entry)

Each claim gets the checks its grounds call for, one per item. The full checklists are in `claim-registry.md` → "Checks".

**Source check** (each `src:` item). Two steps: the source exists; it says what the claim attributes to it (`anti-hallucination.md` Steps 0–6). Record the Source Tier.

```markdown
S1-1: "[Exact statement from paper]"
├── src: [Author et al. Year]
├── Location: [Table X / Figure Y / Section Z / Page N]
├── Values: [exact numbers cited]
├── DOI: [doi]
├── Source Tier: [A–E]
└── Status: [VERIFIED / NEEDS CHECK]
```

**Own work** (each `own:` item). The method is named so someone else could repeat it (DR-008):

```markdown
S1-2: "[Exact statement from paper]"
├── own: [what was observed or measured]
├── Method: [protocol, script or query; date]
├── Data file: [path/to/data.csv]
├── Analysis: [path/to/script.py]
└── Status: [VERIFIED / NEEDS CHECK]
```

**Warrant check** (`claim:` grounds, or several sources combined into a point none makes alone), adapted from Toulmin 1958 and Walton 2008:

```markdown
S4-1: "[Claim drawn from other claims]"
├── Grounds: [claim: IDs; decl: IDs]
├── Warrant: [Why the grounds support this claim, for this audience]
├── Backing: [Support for the warrant, if the audience may not accept it]
├── Qualifier: [The hedge; within the confidence tier?]
├── Rebuttal: [When the step fails; strongest objections engaged?]
└── Status: [VERIFIED / NEEDS CHECK]
```

1. Is the claim clearly stated?
2. Are its `claim:` grounds checked in the registry? **Tier monotonicity:** a claim's tier is no higher than its weakest `claim:` ground, so SPECULATIVE grounds cannot support a SUPPORTED or ESTABLISHED claim.
3. Is the warrant explicit and valid for the target audience?
4. Is the qualifier calibrated to the confidence tier?
5. Is the rebuttal stated, and are the strongest objections addressed (not strawmen)?

**Declared starting points** (each `decl:` item). Stated in the text, Kind and Contestedness recorded; a claim resting on a contested one says so.

**Normative claims** additionally need a `decl:` value among their grounds and boundary conditions in the Rebuttal. Check their quality (see `claim-registry.md` for annotated examples):
- [ ] Not **tautological**: specific, not restating the claim ("applies when applicable")
- [ ] Not a **moving target**: stable, not unfalsifiable ("unless future evidence...")
- [ ] Not **overgeneralized**: bounded, not open-ended ("applies to all X")

**Contribution check** (each contribution, once; validation), adapted from Whetten 1989:

```markdown
C1: "[What the paper adds]"
├── Rests on: [claim: IDs; decl: IDs]
├── What: [Concepts defined, as decl: definitions?]
├── How: [Their relation stated?]
├── Why: [Rationale explicit and valid?]
├── Who/Where/When: [Boundary conditions?]
├── Objections engaged: [Logical, empirical, epistemological?]
└── Status: [VALIDATED / NEEDS CHECK]
```

1. Are all key concepts defined?
2. Is the relation clearly stated?
3. Is the rationale (Why) explicit and valid?
4. Are boundary conditions specified, passing the three quality checks above?
5. Does it engage objections and alternative explanations?
6. Whetten's reviewer questions: What's new? So what? Why so? Well done? Done well? Why now? Who cares?

Then evaluate falsifiability:
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the contribution (not circular)
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
3. Is a reflexive marker visible in the prose at every key moment, not only in the registry?
4. Has potential for harm been considered, with mitigations binding for chapter writing?
5. Is the tier (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) assigned, with the required prose marker present?

If the marker is absent: rewrite to add it, or register the statement as an EMERGING claim with verified sources. A provocation without a reflexive marker is indistinguishable from an authoritative-toned hallucination.

### 4.2 Static Analysis (Automated Checks)

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| LaTeX compiles | `pdflatex` exit code 0 | No errors |
| BibTeX valid | `biber` exit code 0 | All refs resolve |
| DOIs resolve | `python -m tools.check_dois <registry>` | All DOIs resolve at doi.org (HTTP 2xx **or 3xx** — 3xx is the normal case, doi.org redirects to the publisher) |
| Word count | `texcount` | Within journal limit |
| Data files exist | Script check | All referenced files present |
| Figures sourced | Manual check | All figures from own data or cited |

### 4.3 Integration Tests (Argument Flow)

- Claims connect logically between sections
- No contradictions between sections
- Claims in Discussion rest on checked claims from Results (`claim:` grounds)
- Recommendations in Conclusion follow from the claims they rest on
- Each contribution rests on the claims that support it; the premise graph is acyclic (`tools/check_registry.py`)
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

### 4.6 Scope Drift Check (declared vs delivered)

A paper can be internally consistent, well-cited, and arithmetically sound — and still not deliver what its own abstract, introduction, or stated contributions promised. The gap is neither a citation error nor a tier-monotonicity violation (Step Z); it is a distinct finding.

Compare the paper's **declared scope** — abstract claims, introduction "we show / we propose", explicitly enumerated contributions — against the **delivered sections**. For each declared item, classify:

- **Delivered** — a section substantiates the promise.
- **Acknowledged non-delivery** — the paper names the gap (e.g., in Limitations).
- **Silent** — neither delivered nor acknowledged. Highest-information case; flag it.

Flag acknowledged and silent gaps as **SCOPE DRIFT**. This is not in itself a defect — every paper negotiates scope as it is written — but a silent gap between the abstract and the body is a reviewer's first finding, so catching it before submission is the point. Record findings in the registry Notes or a section audit; SCOPE DRIFT is a finding type, not a registry unit type.

*Origin: adapted from agent-ready-assessment's SCOPE DRIFT finding (which compares a Plan-of-Approach against a delivered student report) to the authoring context, which has no Plan-of-Approach — the abstract and the stated-contributions list play that role. See DR-017.*

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
Contribution (root claim; validated by the contribution check)
    ↓
Claims (each verified by the checks its grounds call for)
    ↓
Grounds (src: / claim: / decl: / own: items)
    ↓
Sources and own work (source check, Source Tier; repeatable method)
    ↓
Status (Pass / Fail)
```

Each link is a recorded cell in the registry: a contribution's Rests on, a claim's Grounds, a source's row in the Source Verification Checklist. This is the traceable account IPCC asks of its authors (`docs/glossary.md`, traceability).

---

## 7. Quality Gates

### Gate 1: Draft Complete
- [ ] All sections drafted to page budget
- [ ] Registry populated (claims with their grounds, declared starting points, contributions)
- [ ] P0 entries identified (every contribution is P0)
- [ ] Data files organized

### Gate 2: Verification Complete
- [ ] P0 entries 100% verified (every grounds item checked: source checks, warrant checks, declared starting points stated, `own:` methods named)
- [ ] Contribution check done for each contribution (validation; §4.1)
- [ ] P0 tier floor: every P0 entry, contributions included, at SUPPORTED or ESTABLISHED (`tools/coverage.py --strict`)
- [ ] P1 entries 90% verified
- [ ] P1 tier floor: ≥90% at EMERGING or above — **manual check.** `tools/coverage.py` counts coverage from the Status checkbox (`_STATUS_VERIFIED_REGEX`) and reads the Confidence column only for the **P0** tier floor (DR-002), so `--strict` reports this gate met for a registry whose P1 rows are all verified and all SPECULATIVE. Priority and confidence are deliberately orthogonal axes (DR-017); do not read a green `--strict` as covering this line.
- [ ] P2 entries 70% verified
- [ ] Coverage checked by section type (see Section 3 — Section-Level Coverage Analysis)
- [ ] Grounds re-checked (see `claim-registry.md`, "Checks → Recording grounds")
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
- [ ] Marker is present at every key moment, not only on first introduction
- [ ] No authoritative-toned speculation slides silently into apparent claim
- [ ] Entries failing this audit are rewritten (marker added) or registered as EMERGING claims with verified sources

### Gate 2.7: Ethical Review (conditional — applies when the project engages contested topics)

For projects engaging actively contested ethical territory — political, religious, identity-based, or otherwise. Skip if the work does not engage such cases.

- [ ] No real-world group is pathologised in the author's voice
- [ ] Harm consideration is documented in a DR or equivalent pre-commitment
- [ ] Treatment is symmetric across the contested traditions in the work (no asymmetric scrutiny)
- [ ] Reviewer composition for the contested chapters matches the traditions discussed (the work is reviewed by readers from each)
- [ ] Project-specific operational rules from the contested-topic DR (e.g., paired-mirror rules, vocabulary substitution policies) are applied chapter by chapter

Project-specific operational rules belong in a DR per the project's `decision-record.md` template.

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
- [ ] Language matches confidence levels: no qualifier above its claim's confidence tier (Step Z, `anti-hallucination.md`)

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

*Version: 3.0. v3.0: DR-027's claim model replaces the three unit types; contribution check (validation) in §4.1 and Gate 2; §6 traceability runs contribution → claims → grounds → sources. v2.1: Gate 2.5, PROPOSITION boundary condition quality criteria, falsification checklist, Toulmin grounds tier constraint. v2.2: scope note (informal technical communication), section-level coverage analysis, mistype re-check in Gate 2. v2.3: PROVOCATION as opt-in fifth unit type for speculative-design work (DR-010). v2.4: project-conditional Gates 2.6 (Reflexivity), 2.7 (Ethical Review), 2.8 (Voice Consistency) added. v2.5: §4.6 Scope Drift Check (declared vs delivered), adapted from agent-ready-assessment (DR-017).*
