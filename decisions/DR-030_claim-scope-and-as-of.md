# DR-030: A Claim Stays Within Its Sources' Scope, and Fast-Moving Claims Carry an As-Of Date

---
status: Proposed
date: 2026-10-19
---

## Context

The maintainer's feedback on Paper 1 draft 3 (2026-10-19) asked two related questions: whether a claim's scope should be defined ("like a physics theory is applicable at a certain scale, under certain prerequisites"), and whether claims should be SMART, as requirements are. It began from a concrete failure: the paper supported "LLMs invent plausible-sounding papers" (S1-1) with a GPT-3.5/GPT-4 comparison, in a year when GPT-6 is current ("we are now at 6").

The framework handles scope only in part:
- **Normative claims and contributions** must state boundary conditions, Whetten's Who/Where/When (DR-027; `docs/glossary.md`, *boundary conditions*). For normative claims these go in the Rebuttal cell (`templates/claim-registry.md`, *boundary conditions*).
- **Descriptive claims** carry scope only if the author writes it into the statement or the rebuttal. Nothing requires it.
- **The source check** asks whether a source exists and "says what is attributed" to it. It does not name *scope-widening* as a failure: a claim whose boundary conditions (Who, Where, When) are wider than its source covers.

**Evidence: the scope test** (maintainer-local `memory/archive/hypothesis-log-resolved.md`, entry 2026-10-19; issue #66). All 21 Paper 1 claim rows with `src:` grounds were rated by two raters, the session agent and a fresh subagent given only the criteria.
- The raters agreed on 17 of 21 rows. Both found widenings beyond the seed case: 4 rows (S1-1, S1-2, S1-6, S2-5) and 8 rows respectively. The one-off hypothesis is refuted, with a caveat: both raters were agents in one session, so the test is not independent of the framework's own habits. The acceptance condition below asks for a human or outside rater.
- **"Who" widenings** (for example S2-5: "reporting guidelines are … evaluated", when only CONSORT's evaluation was cited) were fixable by rewording the statement.
- **"When" widenings** (S1-1, S1-2, S1-6: present-tense claims about AI models or detectors, resting on 2023–24 evidence) split the raters. One rated them fixable by rewording. The other rated them as needing a separate field: a date in a sentence does not prompt anyone to re-check the claim when the models move on.
- One of the sources says this directly. Xiong et al. 2024 report that "as model capability scales up, both calibration and failure prediction performance improve", so S1-2's present-tense generalisation runs against its own source's trend.

## Options Considered

### Option A: Name scope-widening as a source-check failure, using Whetten's boundary conditions
Step 2 of the source check becomes: the source says what is attributed *within the boundary conditions the claim states*, meaning Whetten's Who, Where and When, a term the glossary already defines for normative claims.
- (+) Toulmin-consistent: scope stays in the statement, its qualifier and its rebuttal. No schema change.
- (+) Fixes every "who" widening the test found.
- (-) A date written into a statement is not machine-readable, so nothing flags a claim when its evidence ages.

### Option B: Require a rebuttal (scope) for every descriptive claim
- (+) Extends an existing rule (boundary conditions for normative claims) instead of adding a new one.
- (-) Every adopter fills one more cell on every row, including rows the test found in scope (13–17 of 21).
- (-) Still not machine-readable for dates.

### Option C: A required Scope column (who/where/when/as of) on every claim
- (+) The most explicit option, and it can be machine-checked.
- (-) Duplicates the rebuttal, Toulmin's own place for "circumstances in which the general authority of the warrant would have to be set aside".
- (-) A MAJOR schema change, like DR-027, migrating every adopter's registry, for a problem that occurred in 4–8 of 21 rows.

### Option D: SMART criteria per claim
- (-) SMART is for goals. "Achievable" has no meaning for a claim, and "Measurable" is refutability, which the rebuttal already records.

### Option E: Option A, plus an as-of date for claims about fast-moving objects
Option A for boundary conditions in general. In addition, a claim whose object changes on a scale of months (AI models and tools, counts of guidelines or papers, prices, versions) records the date of its evidence in a short, parseable form, for example `as of: 2023–24`. A tool can then flag such claims when they age.
- (+) Addresses both kinds of widening the raters agreed on, and makes staleness checkable where it matters. The rows only one rater flagged (S2-4, S3-2, S4-3) are undecided.
- (+) The date can go where the schema already has room (the Grounds item or the Rebuttal cell), so no new column is needed.
- (-) "Fast-moving" is a judgement. The Revisit If section names how to tell whether it is drawn too narrowly.

## Decision (proposed)

**Option E.** It uses the framework's existing term: *boundary conditions* (Who, Where, When) become something every claim has. Normative claims must still state theirs; a descriptive claim's are what its statement says, and the source check holds the claim to them. This answers the maintainer's question (2026-10-19): population is one of the conditions, so the three are kept as Whetten's named parts, not as a new list.

1. **Source check, step 2.** "The source says what the claim attributes to it, within the boundary conditions the claim states: Who (population or object), Where (setting and conditions) and When (period). A claim that states more than its source covers fails the step, and the usual fix is to narrow the statement."
2. **As of.** A claim about an object that changes within months records `as of: <period of the evidence>`. Where it goes (the Grounds item, the Rebuttal cell, or a convention tools can read) is settled in the template change; no new column.
3. **Tooling.** `tools/check_registry.py` reports an `as of` older than a configurable age (default 18 months) as a note, not a finding. Its job is to prompt a re-check, not to block.
4. **Not adopted:** a Scope column (C), a scope rule for every descriptive claim (B), and SMART criteria (D).

## Consequences

- **Templates and glossary:** the source check's wording changes in `templates/claim-registry.md`, `templates/anti-hallucination.md` (step 4 or 6) and the `docs/glossary.md` entry *source check*. A short example of scope-widening is added.
- **Tools:** an as-of parser and an age note in `check_registry`, with tests (a positive and a negative case for each).
- **Paper 1:** S1-1, S1-2, S1-6 and S2-5 are reworded to their sources' scope, and the new S1-8 is written to scope. The four rows about AI models and tools (S1-1, S1-2, S1-6, S1-8) record `as of:` in their Rebuttal cells. That is used provisionally while this DR is Proposed, and moves if the template change settles elsewhere. The reworded rows rejoin the DR-029 re-rating queue.
- **Adopters:** a MINOR release. Existing registries stay valid; widenings are found the next time a source check runs.

## Acceptance Condition

Accept when the sharpened source check, applied by someone other than the session agent to a registry other than Paper 1's, finds at least one widening that its author agrees with. If it finds none, the Paper 1 result may be specific to how that paper was drafted.

## Open Questions

- Does "as of" belong to the claim or to each source? A claim that combines a 2023 study and a 2026 study has two dates.
- Requirements engineering has standard characteristics of well-formed requirements (singular, verifiable, bounded…). These are not read yet; read them before citing any as precedent (anti-hallucination checklist).
- The scope test has a companion hypothesis: rows verified from abstracts overstate their sources (hypothesis log, 2026-10-08). A widening found from an abstract may be the same failure seen from the other side.

## Revisit If

- Further tests find the widenings concentrated in rows written fast or by the agent (S1-8, written by the agent in the same session it was rated, was one of them). That would make it a drafting-discipline problem rather than a check problem.
- A claim goes stale that the "fast-moving" judgement did not mark. Then broaden the as-of rule, or move to option C.
