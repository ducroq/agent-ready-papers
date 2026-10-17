# DR-029: An Inference's Confidence Tier Comes from Its Warrant Check

---
status: Proposed
date: 2026-10-16
---

## Context

Four model referees reviewed Paper 1 draft 2 (2026-10-16; tag `paper1-draft-2`, private synthesis in `papers/perspective/feedback/`). All four found that the paper fails its own P0 gate. One of them (Claude Fable, point C1) named the cause: the tier rules fail every P0 claim that is an inference, by construction. Paper 1's appendix states the rule it applied, for its P1 example S2-4, and the same rule caps every P0 inference: "the step from the sources to the claim is the author's inference, so the tier cannot exceed Emerging" (`papers/perspective/manuscript.tex:527`). DR-002 requires every P0 claim to reach SUPPORTED. So a paper whose main contribution is an argument cannot pass the gate, however good the argument is. That is the false failure Paper 1 argues against ([#62](https://github.com/ducroq/agent-ready-papers/issues/62), [#38](https://github.com/ducroq/agent-ready-papers/issues/38)).

The cap comes from three places in the framework's own text.

1. **DR-002 puts inference in the lowest tier.** Its SPECULATIVE row reads "Logical inference, hypothesis, single non-peer-reviewed source, or extrapolation". The template repeats this for `src:` grounds: SPECULATIVE is "inference only: a warrant over other grounds (`claim:` or `decl:`), no source" (`templates/claim-registry.md:302,314`).
2. **The template has a second rule for inferences, but it does not judge the step.** The `claim:` row of *Confidence by Grounds* gives SUPPORTED at "4/5" warrant-check items (`templates/claim-registry.md:315`). Items 1 and 2 are bookkeeping: the claim is stated, the grounds are checked (`:219-220`). Item 5 is circular: the qualifier must stay within the tier, which is what is being set (`:223`). Items 3 and 6 bear on the step ("Is the warrant explicit and valid for the paper's audience?"; rebuttal and strongest objections, `:221,224`), but neither gives criteria. Item 4 (backing) applies only sometimes. Three of the four referees said the same: the warrant check has no content. `tools/check_registry.py:964` says so in its own docstring: "Presence and form only, never quality".
3. **No rule covers a synthesis.** A claim that combines several sources into a point none of them makes alone, or that combines a search with sources, has no row of its own. Paper 1's S2-2 (the gap claim) is such a claim, and it fell back to the strictest reading.

Two smaller faults travel with these. DR-002's bands overlap: two agreeing sources fit both SUPPORTED ("2–3") and EMERGING ("1–2"), and Paper 1's Table 1 copies the overlap (`manuscript.tex:350-351`). And two referees (GPT-6, Fable) pointed out that a paper checked by its own procedure's rules proves compliance with that procedure, not correctness. The framework never says so.

DR-027 left this open on purpose: "DR-002's counting rule: what replaces 'count agreeing independent sources' for argued claims, whose strength is the warrant's? (A later DR.)" This is that DR.

## Options Considered

### Option A: Keep the counting rule and exempt argument-based papers from the P0 floor
- (+) Smallest change: one exception in DR-002's gate
- (-) Lowers the bar without saying by how much: an exempted paper's central inferences get no rating at all
- (-) Needs a test for "argument-based paper", and DR-027 dropped paper types because sentences, not papers, carry the kind of support

### Option B: Rate each inference by a warrant check with stated criteria (chosen)
- (+) The gate stays the same for every paper. What changes is how an inference earns its tier
- (+) Gives the warrant check content from argument-quality research, which three referees asked for
- (-) Introduces a judgement the tools cannot make. The tools can check only that the judgement was recorded and that the tier respects it
- (-) Risk named in the hypothesis log (2026-10-16): the bar may drop if nearly every warrant passes, or the paradox may stay if nearly every one fails

### Option C: Give inferences no tier; record only the outcome of the check
- (+) Honest about what an inference is
- (-) Step Z needs a tier to judge the qualifier, so an inference's wording would go unchecked
- (-) Contributions inherit the tier of their weakest claim (DR-027), so the P0 floor would have nothing to read

### Option D: Replace DR-002's tiers with a two-axis rating (IPCC's evidence × agreement, or GRADE)
- (+) Established outside this framework
- (-) Both rate bodies of evidence, not single steps of reasoning, so the warrant still has no check
- (-) A much larger change to every registry, for a problem that sits in one rule

## Decision

**Option B** (maintainer, 2026-10-16). A claim's confidence tier has two inputs. It takes the lower of the two.

### 1. Evidential support: how well the grounds themselves hold

This is what Wachsmuth et al. (2017, p. 177) call the **acceptability** of the premises. One rule sets it, whether a claim's sources all report the same point or are cited for different points.

**The counting rule, per point.** For each point a claim relies on, count the **independent sources** that report it and pass their source check (glossary: they do not take the point from one another or from a shared origin). DR-002's requirements are kept and the overlap is removed:

| Tier | Assign when |
|------|-------------|
| ESTABLISHED | Three or more independent sources agree, at least two of them peer-reviewed; no credible dispute is known |
| SUPPORTED | Two independent peer-reviewed sources agree |
| EMERGING | One peer-reviewed source; or two or more agreeing sources that are not peer-reviewed; or preliminary or pilot data |
| SPECULATIVE | No source reports the point, or a single source that is not peer-reviewed |

Peer-reviewed means Source Tier A or B. The Source Tier scale gains one letter, **N: not peer-reviewed** (a preprint, a report, a web page that is not a guideline or standard), because the scale had no place for a preprint and notes had been recording preprints as B (maintainer, 2026-10-17). The author's own preprint stays E. Count sources, not citations: two papers reporting the same dataset count once. DR-002's wording column is unchanged. The template's special case for **reference claims** (a claim that states what a public document says, `templates/claim-registry.md:356`) still applies and permits ESTABLISHED. A tier below what the rules permit is always allowed, so S2-1, set at SUPPORTED on purpose (registry header), stays valid.

**Corroboration** (all sources report the claim's own point) needs no Warrant; the count above is the claim's evidential support. **Conjunction** (the claim joins several points, each with its own sources, and asserts nothing beyond them): each point is counted on its own, and the claim's evidential support is the lowest of them (maintainer, 2026-10-17). It is recorded in the Warrant cell as `conjunction:` followed by which ground supports which clause, and its warrant check asks one question: does the claim assert anything beyond its clauses? The answer is `pass` or `fail`. A `pass` sets no ceiling of its own, so the claim's tier is that of its weakest point, up to ESTABLISHED; the rebuttal and objection requirements of section 2 do not apply, because a conjunction takes no step. A `fail` makes the row a synthesis. A connective such as "so", a generalisation, a comparison ("closest") or a hedge that reaches past the clauses ("may help") makes it a synthesis, which needs a stated warrant. A source counts toward a point only if it reports that point; folding several points into one does not turn a conjunction into corroboration. **Synthesis** (the claim draws from its grounds a point that none of them states) needs a Warrant, and its evidential support is the lowest tier among the points it relies on, each rated by the rule for its kind of grounds (sources by the count above, `own:` items by DR-008, `claim:` items by their own tier). A premise therefore gets the same tier whether it is written into a synthesis or registered as a claim of its own, so the form of the row cannot raise a tier. What this DR removes is the cap from the inference itself: a synthesis whose premises are each well supported can reach SUPPORTED. A synthesis that leans on a point only one study reports stays at EMERGING, as that point would on its own. A point that only states what a public document says (a definition, a framework's elements, a tool's description of its own checks) is rated by the reference-claim case and does not cap the synthesis (maintainer, 2026-10-17). The case covers the document's own statement read as such: "tool T describes its checks as X". A point used for the truth of a finding is counted, and so is a statement about what a tool actually does when used, which is a finding about the tool.

The other kinds of grounds are unchanged from DR-027: `claim:` items by tier monotonicity (no higher than the weakest `claim:` ground), `own:` items by the rigour of the method (DR-008). DR-008's scale is written for experiments; for two other kinds of own work these rows replace its bullets (`templates/claim-registry.md:349-354`), including its "pilot data, proof-of-concept" row (maintainer, 2026-10-17):

| Own work | SUPPORTED | EMERGING | SPECULATIVE |
|----------|-----------|----------|-------------|
| Literature or database search | Documented and repeatable, two screeners, the field's main databases | Documented, but one screener or partial coverage | Not documented |
| Design trial (applying a method to cases) | Documented cases by at least two different people | Documented cases by one person or team | One undocumented case |

A claim whose only grounds are `decl:` items has an evidential input of at most EMERGING: it rests on nothing beyond what the paper adopts.

A claim with no Warrant (corroboration only) has only this input.

### 2. Inferential strength: whether the step from grounds to claim holds

This applies to every claim that has a Warrant, except a conjunction (section 1). It is the warrant check, which now asks two questions, both from the definition of a cogent argument in Wachsmuth et al. (2017, p. 177): premises "relevant to the argument’s conclusion and, together, sufficient to draw the conclusion".

- **Relevance.** Does each ground bear on this claim? The test: would the claim be less credible without it? An irrelevant ground fails the check. The author corrects the row, and the check is run again on the corrected row.
- **Sufficiency.** Do the grounds together justify the claim at the strength its qualifier states? The check names what would be needed and is missing: a case not covered, a search not run, an alternative explanation not ruled out, a premise resting on one study where the claim needs it replicated. Two further requirements belong here and are recorded separately: the **rebuttal** says in which circumstances the step would no longer hold (a hedge such as "to our knowledge" names no circumstance, so it is not a rebuttal and the check is at most `partial`); the **objection** is the strongest known challenge to this argument, and the row says how it is answered.
- **Critical questions, where they apply.** When the step follows a common pattern (from expert opinion, from analogy, from cause to effect, or from the absence of results in a search), the check also asks that pattern's critical questions. Walton, Reed & Macagno (2008) collect such patterns as "stereotypical patterns of human reasoning". Until someone reads the book text and records the questions with page numbers in the source note, this part stays optional and the check rests on relevance and sufficiency alone (maintainer, 2026-10-16; the note is flagged unverified).

The outcome sets the highest tier the step allows. Each outcome has its own first word, which is what the tool reads:

| Outcome | Assign when | Highest tier |
|---------|-------------|--------------|
| `pass` | Relevance and sufficiency hold for stated reasons; rebuttal stated; strongest known objection engaged | SUPPORTED |
| `confirmed` | A pass, and a person other than the author, able to judge the grounds and the reasoning, reviewed the recorded justification and agreed (a co-author, colleague or referee; a model panel does not count) | ESTABLISHED |
| `partial` | Relevance holds, but a sufficiency gap is named and left open, or an objection goes unanswered | EMERGING |
| `fail` | A ground is irrelevant, the warrant does not make the step, or the gap undermines the claim | SPECULATIVE |

A synthesis registered without a Warrant is rated as `fail` until the author writes one: the step it takes is not stated, so it cannot be checked (maintainer, 2026-10-17). Whoever runs the warrant check records it in the Warrant check cell as `fail: no warrant`, the one case where that cell is filled while Warrant is empty. The tool cannot tell a synthesis from corroboration, so it cannot find such rows itself.

A `fail` means the recorded justification does not support the claim as worded, not that the claim is false. Rewording the claim to what the grounds do support, and checking again, is a normal response.

**Tier of a claim = min(evidential support, inferential strength).** The minimum is taken over every ground in the row. An irrelevant ground does not drop out: it makes the check `fail`, and only after the author corrects the row and the check runs again is the minimum taken over the corrected row. A supplementary point that should not limit the claim belongs in the text, not in Grounds. A contribution's tier is still no higher than its weakest supporting claim (DR-027) or its contribution check. Contributions have no Warrant check cell: Whetten's Why plays that role, in the contribution check.

### 3. Recording

The Claims table gains one column after Warrant: **Warrant check**. It holds the outcome word, the reason in a few words, who checked, and the date. The reason names the issue: `partial: no search of humanities indexes` says what is open, `partial: insufficient evidence` does not. A longer reason goes in the registry's notes, with the cell pointing to it. Examples: `pass: protocol covers the named databases; agent 2026-10-20`, `partial: no search of humanities indexes; agent 2026-10-20`. The cell stays empty when Warrant is empty, except for `fail: no warrant` (section 2). In a table that has the column, a row whose Warrant is filled but whose Warrant check is empty cannot be `[x]`.

**A worked example (hypothetical).** Claim: "The reporting checklists of field X do not check reasoning." Grounds: `src: A; src: B`, two independent peer-reviewed reviews (2019, 2021), each listing X's checklists and their items. Warrant: none of the listed items asks whether a step of reasoning holds, so the checklists do not check reasoning. Evidential support: both reviews report the same list, so that point is SUPPORTED. Relevance: both grounds bear on the claim. Sufficiency: a checklist published after 2021 would be in neither review. Rebuttal: the claim fails if any checklist in X has an item on whether reasoning holds. Objection: some items ask for a "rationale"; answered in the row: they ask that a rationale be reported, not that it holds. Outcome: `partial: no checklists after 2021 covered`, so the claim is EMERGING. Rewording it to "the checklists listed up to 2021", or adding a search of later ones, would make a pass possible, and the claim could then reach SUPPORTED.

The old six-item checklist (`templates/claim-registry.md:217-224`) is replaced. Items 1, 2 and 5 become preconditions of the check and no longer count toward a score; item 5 is already Step Z. Item 3 becomes relevance and sufficiency, item 6 moves into sufficiency, and item 4 (backing) stays as it is: needed where the audience may not accept the warrant. The "5/5" to "<3/5" scoring in the `claim:` row of *Confidence by Grounds* is dropped. The Contribution row's Whetten scoring is not changed by this DR.

### 4. What passing means

Passing the checks means the paper followed the method: each claim's grounds and warrant were recorded and checked against stated criteria. It does not mean the claims are true. A warrant check by the author or the author's agent can be wrong in the author's favour. This is why ESTABLISHED requires a check by a person other than the author, and why the Warrant check cell names the checker. Model reviewers, including DR-011's cross-vendor panels, can find problems but cannot confirm a pass: they come from the same kind of system that may have drafted the claim (maintainer, 2026-10-16). This statement goes into the glossary entry for **verification** and into the paper templates.

### Tools

- `tools/check_registry.py`: read the Warrant check column. Report a row with a Warrant but no Warrant check. Report a row whose confidence tier exceeds what its outcome word allows (`pass` → SUPPORTED, `confirmed` → ESTABLISHED, `partial` → EMERGING, `fail` → SPECULATIVE); a `pass` on a row whose Warrant starts with `conjunction:` has no ceiling. Report a `decl:`-only claim above EMERGING. Report a cell whose first word (read without its colon) is not one of the four outcome words, and compare no tier for it. Report a `confirmed` cell whose checker names an agent or a model. The tool checks that the judgement was recorded and that the tier respects it. It cannot check the judgement itself, or that the person named as checker exists and is independent.
- `tools/coverage.py`: no rule change; the P0 floor reads the tiers as before.
- Registries whose Claims tables have no Warrant check column: each row with a Warrant gets a **note**, which does not change the exit code. Old registries keep passing and show what is missing. Where the column exists, the rules above are findings; this includes the `decl:`-only rule, so no rule in this DR can fail an old registry. Tests seed a positive for each rule and for the note path.

### Amendments to other DRs (on acceptance, an "Amended by DR-029" line in each)

- **DR-002**: the bands become the table in section 1: ESTABLISHED needs three or more independent sources (DR-002: "multiple"), at least two peer-reviewed; SUPPORTED two peer-reviewed; EMERGING one peer-reviewed, or two or more that are not. They no longer overlap. "Logical inference" leaves the SPECULATIVE row: an inference's tier comes from its warrant check. The single non-peer-reviewed source stays SPECULATIVE. The wording column and the P0 floor are unchanged.
- **DR-027**: its Open Question on the counting rule for argued claims is answered here. Its question on how to tell a synthesis from corroboration is answered by the author's choice: a synthesis has a Warrant and a Warrant check; a conjunction has a `conjunction:` Warrant and the one-question check; corroboration has neither. The tool cannot tell them apart, so a synthesis registered without a Warrant is rated `fail` by the checker (section 2), not reported by the tool.

## Consequences

- An inference can reach SUPPORTED when its warrant check passes. An argument-based paper can then pass the P0 floor, but only on recorded reasons that a reader can dispute.
- The P0 floor itself does not change. Whether Paper 1 should keep proposing a pass/fail gate to others is a question for draft 3, not for this DR.
- Paper 1's three P0 claims below the floor (C1, S2-2, S3-4) are checked again under this rule. S3-4's `own:` ground is two trial migrations by one agent (widened from one on 2026-10-17, after the predictions were registered), so under the design-trial row its evidential support stays at EMERGING whatever its warrant check says, and C1 stays at EMERGING with it.
- A synthesis is still limited by its weakest point. Where a paper's argument leans on a finding only one study reports, the claim stays at EMERGING until a second independent source is found or the claim is narrowed. That is a real limit of the evidence, which the gate should show.
- Authors write one more cell per inference. In exchange, the "5/5" scoring goes away.
- Changed on implementation:
  - `docs/glossary.md`: warrant check, confidence tier, verification, Source Tier (N), corroboration, conjunction and synthesis
  - `templates/claim-registry.md` Source Tier Reference: add N; own-data rigour note (`:349-354`): add the search and design-trial rows; reference-claim case (`:356-366`): add the case inside a synthesis
  - `templates/claim-registry.md`: the warrant check (`:215-226`), the Tier Reference bands (`:300-302`), the `claim:` and `src:` rows of Confidence by Grounds and their comment (`:314-320`)
  - `templates/writing-guide.md:98` and `papers/perspective/writing-guide.md:84`: the "Logical inference" row
  - `README.md:198-200`: the bands and the SPECULATIVE row
  - `docs/THRESHOLDS.md`: its row on inference
  - `tools/check_registry.py` and its tests
  - Paper 1's registry, Table 1 and appendix (S1-4's three preprints already moved to N, 2026-10-17)
  - Source notes that record a preprint as B: `literature/sources/ghostcite-2026.md`, `li-2026-self-correction.md`, `mori-2026-warrantscore.md` (none is used in Paper 1's registry)
- A MINOR release: the new column is optional for old registries, which get notes, not findings.

## Acceptance Condition

Accept when all hold:

1. **Predictions first.** Before the re-rating, the expected outcome for Paper 1's C1, S2-2 and S3-4 is written in `vv/hypothesis-log.md`, with a reason for each.
2. **Re-rating.** Paper 1's registry and the migrated constructive-lenses registry (`docs/work-items/archive/2026-10-16-v5-and-draft2/v5-trial/`, the only other registry in the DR-027 schema) are re-rated under this rule, as copies, with every Warrant check cell filled. The re-rating is done by an agent in a fresh context, given an extract of sections 1 to 3 of the Decision and not this file, so it does not know what result is wanted.
3. **The check discriminates.** Among the P0 and P1 rows that have a Warrant, in both registries together, at least two come out `pass` and at least two `partial` or `fail`, each for a stated reason. If every warrant passes, the bar has dropped. If none passes, the paradox remains. Either result means this DR needs rework, not acceptance (the alternative recorded in the hypothesis log, 2026-10-16).
4. **Review.** The maintainer reads every P0 outcome and agrees, or the DR or the row is revised where they disagree. The maintainer also judges whether the passes and the non-passes differ for real reasons, not only in their labels. The results are compared with the predictions in condition 1.

## Open Questions

- Should a contested declared starting point cap inferential strength at EMERGING? (DR-027 asked the same of the tier as a whole.) A model review of the first draft suggested a qualified cap: only when the starting point is essential to the argument, the dispute is credible and material, and it is unresolved. Left open by the maintainer (2026-10-16) until the re-rating shows how often it applies.
- Which critical questions, for which patterns? Decide after the Walton text is read. Argument from absence of results is the one Paper 1 needs (S2-2, S1-4).
- Should a pass require that the strongest objection be found by someone other than the author?
- Is EMERGING the right ceiling for a claim resting only on declared starting points? A step from accepted definitions can be strong.
- Should a single study be enough for SUPPORTED when a recorded reason says why (a census, a direct measurement, a definitive document)? If so, the same lift must apply to a claim of its own and to a premise in a synthesis.

## Revisit If

- Nearly all recorded warrant checks pass across several papers, which would mean the bar has dropped.
- Two checkers given the same row often disagree on the outcome. Wachsmuth et al. (2017, p. 183) found low agreement among seven annotators with simple guidelines, so the criteria may need examples before they can be applied consistently.
