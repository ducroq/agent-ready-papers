# Claim Registry

<!-- The paper's verification registry, in the DR-027 schema. Terms: docs/glossary.md.
     Every statement the paper puts forward and supports is a claim. Each claim records
     what it says (descriptive or normative) and what it rests on (its grounds), item by
     item; the checks follow the items. Declared starting points and contributions sit in
     their own tables. Update this living document throughout the writing process. -->

**Paper:** [Title]
**Last Updated:** [date]
**Thesis:** [One-line thesis]

---

## Coverage Summary

Two cuts of the same rows. `python -m tools.coverage <registry>` computes both; fill these tables from its output, never by hand counting.

**Coverage by Priority**

| Priority | Total | Verified | Needs Evidence | Coverage |
|----------|-------|----------|----------------|----------|
| P0 | 0 | 0 | 0 | 0% |
| P1 | 0 | 0 | 0 | 0% |
| P2 | 0 | 0 | 0 | 0% |
| **Total** | **0** | **0** | **0** | **0%** |

**Coverage by Says**

| Says | Total | Verified | Coverage |
|------|-------|----------|----------|
| descriptive | 0 | 0 | 0% |
| normative | 0 | 0 | 0% |
| contribution | 0 | 0 | 0% |
| provocation | 0 | 0 | 0% |
| **Total** | **0** | **0** | **0%** |

Contributions always count as P0. Declared starting points are excluded from both cuts and reported apart (how many, how many `[x]`).

**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2. **P0 tier floor (DR-002):** every P0 row, contributions included, at SUPPORTED or ESTABLISHED. A contribution's tier counts as no higher than its weakest supporting claim, so a contribution resting on an EMERGING claim fails the floor whatever that claim's own priority (DR-027).

---

## Priority Guide

### P0 (Critical): paper fails without these
<!-- Claims that, if wrong, break the core argument. Every contribution is P0. -->

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| [ID] | [claim] | [consequence] |

### P1 (Important): target 90%
<!-- Claims that strengthen but don't break the argument -->

### P2 (Supporting): target 70%
<!-- Context and background claims -->

---

## Registry Conventions

The tools read a table only directly under its marker line (`**Contributions:**`, `**Declared starting points:**`, `**Claims:**`, `**PROVOCATIONs**`), not under a heading. Keep the marker on its own line, then a blank line, then the table. Any prose between the marker and the table stops `tools/coverage.py` with an error.

**IDs.** Claims are `S<section>-<number>` (e.g. `S3-2`; a split row may take a letter, `S2-3a`), contributions `C<n>`, declared starting points `D<n>`. Every ID is unique in the registry, and each table holds only its own prefix. Anchor each ID in the manuscript as a comment: `% S1-1: label (descriptive, P0, SUPPORTED)`, `% C1: label (contribution, P0, EMERGING)`, `% D1: label (definition, own)`.

**Grounds items.** The Grounds cell (and a contribution's Rests on cell) lists typed items, semicolon-separated:

| Item | Means | Check it calls for |
|------|-------|--------------------|
| `src: Author Year` | What a cited work reports | Source check |
| `claim: S1-2` | Another claim in this registry | Warrant check; tier monotonicity |
| `decl: D1` | A declared starting point | Stated in the text, contestedness recorded |
| `own: what, method or query, date` | The author's own observation, experiment or measurement | A method someone else could repeat (DR-008) |

A distinction taken from a source and adopted as a premise is recorded both ways: `src:` for where it comes from, `decl:` for the paper's adoption of it.

**Source Tier** lists one tier per `src:` item, in the same order (`src: Smith 2020; src: Lee 2022` → `A; C`). `own:`, `claim:` and `decl:` items carry no Source Tier. A source with no tier yet takes `[TBD]` in its position, and the row stays `[~]` until the tier is assigned.

**Empty cells.** Leave Warrant empty when every source supports the claim on its own; Backing when the audience already accepts the warrant; Rebuttal and Objections engaged when none apply to a descriptive claim. A blank cell in a column a row needs (Warrant for `claim:` grounds; Rebuttal and a `decl:` value for a normative claim) means the row is not yet checkable: keep it `[ ]` or mark it `[!]`.

**`|` inside a cell** breaks the table; escape it as `\|`. The semicolon is safe.

---

## Contributions

<!-- Each contribution is a root claim: what the paper adds. P0 by definition, with a
     confidence tier no higher than its weakest supporting claim. Rests on lists claim:
     and decl: items only; a normative contribution names its value there. Checked once
     with Whetten's elements and questions (the contribution check, a validation step). -->

**Contributions:**

| ID | Contribution | Says | Rests on | What | How | Why | Who/Where/When | Objections engaged | Priority | Confidence tier | Status |
|----|--------------|------|----------|------|-----|-----|----------------|--------------------|----------|-----------------|--------|
| C1 | [What the paper adds to current thinking] | normative | claim: S4-1; claim: S4-2; decl: D1; decl: D2 | [the concepts it relates; definitions in D rows] | [how they relate] | [why: the rationale that makes How hold] | [who, where, when it applies; where it does not] | [strongest objection; response] | P0 | EMERGING | [ ] |

## Declared starting points

<!-- Assumptions, definitions and values the paper adopts, not argues for. No priority and
     no confidence tier: they are excluded from coverage and the P0 floor. State each one
     in the text. A claim resting on a contested starting point says so in its text
     (Step Z). Definitions also go in the paper's glossary.md (DR-028). -->

**Declared starting points:**

| ID | Statement | Kind | Contestedness | Status |
|----|-----------|------|---------------|--------|
| D1 | [A term as this paper uses it: "X" means ...] | definition | own | [ ] |
| D2 | [A value a recommendation serves: "Y should be ..."] | value | accepted | [ ] |

Kind is `assumption`, `definition` or `value`. Contestedness is `accepted` (in the field), `contested` or `own` (the paper's own).

## Claims by section

### Section 1: [Section Name]

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S1-1 | [What two cited works report, attributed to them] | descriptive | src: [Author1 Year]; src: [Author2 Year] | | | | | P0 | SUPPORTED | A; A | [ ] |
| S1-2 | [What the author observed or measured] | descriptive | own: [what was measured, method or query, date] | | | [conditions the observation does not cover] | | P1 | EMERGING | | [ ] |

<!-- Repeat for each section. A row whose sources each support it alone needs no Warrant. -->

### Section 4: Discussion

**Claims:**

| ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status |
|----|-----------|------|---------|---------|---------|----------|--------------------|----------|-----------------|-------------|--------|
| S4-1 | [A conclusion drawn from the claims above] | descriptive | claim: S1-1; claim: S1-2; decl: D1 | [why these grounds lead to this claim, for this paper's audience] | [support for the warrant, if the audience may not accept it] | [circumstances in which the step from grounds to claim fails] | [an objection to the claim; the response] | P1 | EMERGING | | [ ] |
| S4-2 | [A recommendation: what should be done] | normative | claim: S4-1; decl: D2 | [why the grounds and the value lead to the recommendation] | | [boundary conditions: where it applies; where it does not] | | P1 | EMERGING | | [ ] |

As filled in, the example fails the P0 tier floor: C1 rests on S4-1, which is EMERGING. That is the floor working as DR-027 intends. A paper whose contribution rests on preliminary evidence says so, and the gate records it.

Column semantics for the PROVOCATION sub-table below differ from the claim tables: Auger's four criteria are *evaluative questions*, so each column records the **evidence or move that answers the question**, not a yes/no judgment.

<!-- Keep this paragraph ABOVE the sub-table marker, not between the marker and
     the table header. `tools/coverage.py` skips only blank lines after a marker
     before expecting a table row; any prose there makes it stop with an error
     (exit 2), and before 2026-09-26 it abandoned the sub-table silently.
     Until 2026-08-13 this paragraph sat below the marker, and the released
     template's PROVOCATION rows were invisible to the released tool;
     found by the repo-wide sweep, which ran the tool against the template
     instead of reading it. -->

**PROVOCATIONs** (Auger; opt-in, speculative-design only; see DR-010):

| ID | Statement | Priority | Tier (PROVOCATION axis) | Plausibility evidence | Generative move | Reflexive marker | Ethics commitment | Status |
|----|-----------|----------|--------------------------|------------------------|------------------|-------------------|--------------------|--------|
| S4-3 | [diegetic prototype / reflexive Ask / paradox box] | P1 | GROUNDED | [why a reader could hold this seriously inside the fiction] | [how the surrounding prose develops the artefact as material] | "[exact prose phrasing, required, verbatim]" | [potential harm considered + DR-level pre-commitment binding for writing] | [ ] |

<!-- A provocation makes no truth claim, so it is not a claim in DR-027's model and keeps
     this table. Tier uses the PROVOCATION axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE /
     CRITICAL), not the confidence tier. Reflexive marker must quote the prose phrasing
     verbatim; without it the entry is indefensible (see Step Z in anti-hallucination.md
     and DR-010). An empty criterion cell means the entry is not yet verifiable as a
     provocation: keep it `[ ]` or mark it `[!]`. -->

---

## Source Verification Checklist

### Literature Sources

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| [Author Year] | [IDs] | [specific values/statements to verify] | [ ] |

### Own Work Used as Grounds

| Item | Claims | Method recorded | Status |
|------|--------|-----------------|--------|
| [dataset / experiment / query] | [IDs] | [data files exist, analysis reproducible, query and date stated] | [ ] |

### Own Work (Under Review)

| Paper | Claims | Venue | Status |
|-------|--------|-------|--------|
| [paper title] | [IDs] | [journal] | [under review / accepted / published] |

---

## Out of Scope

<!-- Claims verified but excluded (preserve for future reference) -->

| ID | Claim | Source | Why Excluded |
|----|-------|--------|-------------|
| [ID] | [claim] | [source] | [reason; link to DR if applicable] |

---

## Checks

The checks follow the grounds (DR-027). The per-claim checks are **verification**; the contribution check is **validation**. Terms: `docs/glossary.md`.

### Recording grounds

For a sentence like "Prior work shows X [cite]; therefore Y", register X (resting on the source) and Y (resting on X, through a warrant). Ask of each claim: would it stand if I removed the citation? the inference? the assumption? Whatever it would fall without is a grounds item.

Red flags, to run after first registration (Gate 1) and again after verification (Gate 2):

- A claim cites several sources for a point none of them makes alone. It is a synthesis: add a Warrant.
- A claim says "should", "needs" or "we propose" but is marked descriptive. Mark it normative and give it a value and boundary conditions.
- A claim scored low on its sources "feels" well supported. Its strength may lie in a warrant over other claims; record those as `claim:` grounds.
- A claim rests on an assumption the audience may not share, and nothing records it. Register the assumption as a declared starting point, or give the warrant backing.
- An entry is a fictional category, diegetic prototype or reflexive construction with no real source. It is a provocation (DR-010), not a SPECULATIVE claim. Registering it as a claim with a fabricated source is the inverse of standard hallucination and equally dangerous.

### Source check (each `src:` item)

Two steps: the source exists, and it says what the claim attributes to it. Run `anti-hallucination.md` Steps 0–6 (Steps 0–3 establish existence; Steps 4–6 that it says it). Record the Source Tier. A source check establishes faithful attribution, not that the source is reliable or the claim true.

### Warrant check (`claim:` grounds, or several sources combined)

Toulmin's elements, as a checklist:

1. Is the claim clearly stated?
2. Are the grounds checked? Every `claim:` item must be `[x]` in its own row.
3. Is the warrant explicit and valid for the paper's audience?
4. Where the audience may not accept the warrant, is there backing?
5. Does the qualifier stay within the claim's confidence tier (Step Z)?
6. Is the rebuttal stated: the circumstances in which the step no longer holds? Are the strongest objections engaged, not strawmen?

**Tier monotonicity:** a claim's confidence tier is no higher than the weakest claim among its `claim:` grounds. SPECULATIVE grounds cannot support a SUPPORTED or ESTABLISHED claim. `tools/check_registry.py` checks this over the premise graph.

### Declared starting points (`decl:` items)

Each is stated explicitly in the text, with its Kind and Contestedness recorded. A claim resting on a `contested` starting point says so in its text. Every definition also appears in the paper's `glossary.md` (DR-028).

### Own work (`own:` items)

Each names what was observed or measured, the method (script, protocol or query) and the date, so someone else could repeat it. Confidence follows the rigour of the method (DR-008), not a count of sources; see the Source Tier note below.

### Normative claims

A normative claim needs at least one `decl:` value among its grounds and **boundary conditions** in its Rebuttal cell: where does it apply, and where not?

Good boundary conditions are specific and testable:
- **Good:** "Applies to engineering domains requiring judgment; may not hold for routine, well-defined tasks"
- **Good:** "Holds when team size < 10 and iteration cycles are weekly or shorter"
- **Bad (tautological):** "Applies when applicable" / "Holds when conditions are met"
- **Bad (moving target):** "Applies unless future evidence suggests otherwise"
- **Bad (overgeneralized):** "Applies to all engineering domains": no upper bound on scope
- **Bad (missing):** no boundary conditions stated; every recommendation has limits

Anti-patterns to check:
- **Tautological:** the boundary condition restates the claim
- **Moving target:** the boundary condition can never be falsified
- **Overgeneralized:** "applies to all X" without saying where it breaks down

### Contribution check (each contribution, once)

Whetten's elements and questions (Whetten 1989), applied to the contribution as a whole:

1. **What:** are the concepts it relates defined (as `decl:` definitions)?
2. **How:** is their relation stated?
3. **Why:** is the rationale explicit, and does it hold? (Why plays the role of warrant and backing for the contribution.)
4. **Who / Where / When:** are its boundary conditions stated? Apply the anti-patterns above.
5. **Objections:** are the logical, empirical and epistemological objections engaged?
6. Whetten's reviewer questions: What's new? So what? Why so? Well done? Done well? Why now? Who cares?

**Falsifiability** (for each contribution, and for any normative claim that states one):
- [ ] Criterion is testable (not "if we decide it's false")
- [ ] Criterion is independent of the claim (not circular)
- [ ] Criterion is specific enough to be measurable
- [ ] Criterion is not a moving target

See `vv-framework.md` Section 4.1 for where these checks sit in the gates.

### Provocations (Auger checklist; opt-in, see DR-010)

Applies only to projects that contain designed artefacts making no truth claim (speculative-design, design-fiction, diegetic-prototype work). Standard empirical and methodological papers do not need this section.

Verification questions (adapted from Auger 2013, *Digital Creativity* 24:1):

1. **Plausible:** Could this exist in some adjacent world consistent enough that a reader holds it seriously inside the fiction?
2. **Generative:** Does the surrounding prose reach into the artefact (taking it as material to develop) and not around it?
3. **Reflexive:** Is a marker visible *in the prose* (not only in the registry) at every key moment, signalling fictionality?
4. **Ethically held:** Has potential for harm been considered, with a DR-level pre-commitment binding for chapter writing?

**Reflexive marker:** required field for every provocation:

```markdown
Reflexive marker: [Quote the exact prose phrasing that signals fictionality]
```

If no marker is present in the prose: rewrite to add it, or register the statement as an EMERGING claim with verified sources. A provocation without a reflexive marker is indistinguishable from an authoritative-toned hallucination and undermines the speculative-design contract with the reader.

**The inverse-hallucination risk:** a standard hallucination invents a source for a real-sounding claim. A provocation risks the reverse: being read as a claim with a citable source when no source applies. An agent presenting a fictional speculative-design criterion ending in `[Author, Year]` has hallucinated *into* fictional territory. See `anti-hallucination.md` Step Z.

---

## Confidence Tier Reference

| Tier | Assign when... | Language |
|------|---------------|----------|
| **ESTABLISHED** | Sources: multiple independent sources. Claim grounds: warrant checked + fair engagement. Contribution: supporting claims checked + reasoning valid + tested | "demonstrates", "shows", "confirms" |
| **SUPPORTED** | Sources: 2-3 sources agree. Claim grounds: warrant valid + grounds sufficient. Contribution: supporting claims checked + reasoning valid | "indicates", "supports", "evidence suggests" |
| **EMERGING** | Sources: 1-2 sources. Claim grounds: grounds partial or warrant debatable. Contribution: supporting claims plausible + reasoning sound | "may", "preliminary evidence", "initial findings suggest" |
| **SPECULATIVE** | Sources: inference only, no source (record the inference as a Warrant). Claim grounds: position stated, warrant incomplete. Contribution: conjectural | "warrants investigation", "remains unclear", "we hypothesize" |

The tier values and their wording are DR-002's and unchanged. A claim with mixed grounds takes the lowest tier its items allow; a claim's tier never exceeds its weakest `claim:` ground, and a contribution's never exceeds its weakest supporting claim.

### Confidence by Grounds

<!-- How the checks map to each tier, by what a claim rests on. For src: grounds the tier
     tracks source strength; for claim: grounds, warrant-check completeness and the tier of
     the grounds; for own: grounds, the rigour of the method (DR-008). -->

| Grounds | ESTABLISHED | SUPPORTED | EMERGING | SPECULATIVE |
|---------|-------------|-----------|----------|-------------|
| `src:` only | 3+ independent sources, textbook consensus | 2–3 sources agree, open questions | 1–2 sources, not replicated | No source yet: register the inference as a warrant over other grounds |
| `claim:` (warrant check) | 5/5 warrant check, grounds ESTABLISHED | 4/5, grounds SUPPORTED+ | 3/5, grounds checked but conclusion untested | <3/5, or grounds unchecked |
| Contribution (contribution check) | 5/5 Whetten, tested in practice | 4/5 Whetten, supporting claims checked | 3/5 Whetten, reasoning valid but untested | <3/5 Whetten, or missing boundary conditions |

<!-- "5/5" counts the operationalized warrant-check items 1, 2, 3, 5, 6 above (claim,
     grounds, warrant, qualifier, rebuttal); backing (item 4) applies only where the
     audience may not accept the warrant. "5/5 Whetten" counts contribution-check items 1-5. -->

### PROVOCATION Confidence — Separate Axis

Provocations do not measure evidence strength; they measure quality of speculation. The tiers below replace ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE for provocation entries only. Each tier carries a *required prose marker*: a phrasing that must appear in the manuscript itself, not only in the registry. See DR-010.

| Tier | Assign when… | Required prose marker |
|------|--------------|------------------------|
| **GROUNDED** | Speculation explicitly anchored in cited research; mechanism named; warrant visible | *"If X (source Y), then a speculative manifestation might look like…"* |
| **EXTRAPOLATED** | Extension of an existing pattern (e.g., DSM dimensional approach) into fictional territory; warrant visible but underpinning partial | *"By analogy with X, we propose a fictional Y…"* |
| **PROVOCATIVE** | Deliberately uncomfortable, rhetorical; ethical hedge explicit; no empirical pretension | *"Deliberately uncomfortable: what if…"* |
| **CRITICAL** | The fiction itself critiques an existing system (e.g., DSM form imitated to surface diagnostic reification) | *"By imitating this DSM form we ask…"* |

No marker = indefensible provocation. Remediation: rewrite to add the marker, or register the statement as an EMERGING claim with verified sources.

## Source Tier Reference

| Tier | Type | Weight |
|------|------|--------|
| A | Peer-reviewed primary research | 1.0 |
| B | Peer-reviewed review article | 0.8 |
| C | Textbook / established reference | 0.9 |
| D | Guidelines / industry standards | 0.7 |
| E | Own work published or under review elsewhere | 0.6* |

**Tier F ("logical inference") is retired (DR-027).** It covered two different things: an inference from other claims, now a Warrant over `claim:` or `decl:` grounds, and the author's own observation, now an `own:` item.

\* **Own data vs. own work (DR-008):** The 0.6 weight applies to own work cited from
papers under review elsewhere. For **`own:` grounds** (results from observations or
experiments reported in the current paper), confidence should reflect methodological rigour
(sample size, statistical power, reproducibility, calibration), not source count. Assign
confidence based on the evidence quality:
- Large sample, adequate power, validated method → ESTABLISHED or SUPPORTED
- Small sample, exploratory, single-site → EMERGING
- Pilot data, proof-of-concept → SPECULATIVE

### Special Cases: Reference Claims

A claim resting on one `src:` item that states what a document says, e.g. "AHA recommends
X with Class I evidence" or "ISO 17025 requires Y", should use **ESTABLISHED** when the
source is publicly accessible and the statement is a direct, verifiable reference. These
are not evidence-dependent claims requiring confidence assessment; they are facts about
what a document says. If the document exists and says this, the claim is verified.

Use ESTABLISHED for reference claims when:
- The source document is publicly accessible (published guideline, standard, or regulation)
- The statement is a direct reference to what the document says (not an interpretation)
- Verification requires only checking the document, not evaluating evidence strength

### Special Cases: Framework Components

<!-- DR-004: Novel frameworks get written in ESTABLISHED language when they're
     actually EMERGING/SPECULATIVE. This is the most common language calibration error.
     See also writing-guide.md, Framework Component Language special case. -->

When a paper proposes a new framework, the framework components start at EMERGING or lower
regardless of the evidence that motivated them. The framework is an interpretation of
evidence, not the evidence itself.

| Stage | Confidence | Example |
|-------|-----------|---------|
| Conjectural, no supporting evidence | SPECULATIVE | "We hypothesize a multiplicative relationship" |
| Novel contribution, supporting evidence but no validation | EMERGING | "We propose a multiplicative relationship" |
| Initial validation (pilot, case study) | SUPPORTED | "Pilot data supports the multiplicative model" |
| Independent replication | ESTABLISHED | "Multiple studies confirm the multiplicative relationship" |

This applies even when the evidence *supporting* the framework is strong: the evidence
supports the framework's premises, but the framework's structure and claims are untested
interpretations until validated.

### Special Cases: Methodological Facts

<!-- DR-008: Results from applying a published standard method (e.g., GUM uncertainty
     budgets, ISO statistical tests, validated analytical procedures) are not
     evidence-strength claims; they are calculations with documented inputs. -->

Results from applying a published standard method are **ESTABLISHED** when:
- The calculation follows a published standard (e.g., GUM, ISO 5725, ASTM method)
- All inputs are documented (raw data, parameters, assumptions)
- The result is reproducible (another analyst with the same inputs gets the same answer)

These are methodological facts: the confidence comes from the method's validity, not from
independent replication of the result itself. Record them as `own:` grounds naming the
standard and the inputs; calculation verification (DR-009) applies to them.

**Key distinction:**
| Statement | Grounds and check | Why |
|-----------|------|-----|
| "Expanded uncertainty is ±2.29% (k=2, GUM)" | `own:` (GUM, documented inputs) → ESTABLISHED | Calculation follows published standard with documented inputs |
| "This uncertainty is acceptable for clinical use" | `claim:` + Warrant → warrant check | Interprets the result against a threshold; the warrant can be challenged |
| "GUM requires combining Type A and Type B uncertainties" | `src:` reference claim → ESTABLISHED | Direct statement about what the standard says |

## Status Legend

| Status | Meaning |
|--------|---------|
| [ ] | Not yet verified |
| [~] | In progress |
| [x] | Verified |
| [!] | Problem, needs attention |

---

## Cross-Reference Rules

- No claim accepted on a single non-textbook source
  - **Exception (DR-008):** claims on `own:` grounds with documented methodology (data files, analysis scripts, reproducible pipeline) are accepted on the strength of the methodology, not source count
- Contradictory sources must be acknowledged in the text
- Claims >10 years old need a recency check
- Own work under review must be explicitly flagged

---

## Migrating from DR-004

A registry with `**CLAIMs:**`, `**ARGUMENTs**` and `**PROPOSITIONs**` sub-tables still works: the tools read these markers as deprecated aliases through v5.x, check them under DR-004's rules, and print a deprecation note. Removal comes no earlier than v6.0.0. To migrate, map the columns with DR-027's table (`decisions/DR-027_toulmin-whetten-verification-model.md`, "Aliases through v5.x") as a default and judge each row: CLAIM Source becomes `src:` grounds, ARGUMENT Grounds become `claim:` grounds, PROPOSITION Boundary conditions become the Rebuttal, Constructs become `decl:` definitions, and a Tier-F source becomes a Warrant or an `own:` item. A central PROPOSITION usually becomes the contribution.

---

*Registry created: [date]*
