# DR-032: "Accepted" Needs a Source; Otherwise a Starting Point's Contestedness Is "Not Known"

---
status: Proposed
date: 2026-11-08
---

## Context

DR-027 gives every declared starting point a **Contestedness**: `accepted` (in the field), `contested`, or `own` (the paper's own) (`templates/claim-registry.md`, *Declared starting points*; `docs/glossary.md`, *declared starting point*). Paper 1 states the check as "a note on whether the field accepts or contests it".

A reader of Paper 1 (comments 2026-11-07) wrote that whether the field generally accepts an assumption "is often impossible to answer", and especially hard for innovative research.

- **Innovative research is already covered**: a new starting point is `own`. Paper 1 doesn't say so, which is why the check read as unanswerable.
- **`accepted` is asserted, never checked.** No rule says what shows acceptance. Paper 1's register marks three starting points accepted: D1 (published reasoning should be checkable: a value), D4 ("AI-augmented writing": a definition) and D7 (a proposal should be tested before it is adopted: a value), none of them with a source. A check on 2026-11-08 (session agent, unconfirmed) found:
  - D4: only the category is sourced. The ICMJE recommendations (2026) treat AI-assisted writing as a category authors must disclose, which shows that the notion is in use, not that the field accepts D4's definition. Liang et al. use a narrower operational term ("substantially updated by ChatGPT beyond basic spelling and grammatical edits"; arXiv version read). Under Decision 3: not known. (First rated accepted; corrected after review, 2026-11-08.)
  - D7: only a weaker form is sourced. Moher et al. (2010), guidance for developing reporting guidelines, call pilot testing "worth considering" (step 9.1) and recommend evaluating impact after publication (step 15), noting "few guidelines appear to have been evaluated to date".
  - D1: no source found that states it at the level of claims. Transparency norms for data and methods exist, but they say less.

A label the framework asks for, but nothing checks, is the kind of unverified confident statement the framework exists to catch.

## Options Considered

### Option A: `accepted` requires a source; add `not known`
`accepted` cites a source that shows the field accepts the starting point: a standard, guideline, textbook or review, or a survey of the field. Without one, the value is `not known`. `contested` likewise names at least one source that disputes it. `own` is unchanged.
- (+) Makes the check answerable in every case, which answers the reader's objection.
- (+) Holds the label to the framework's own rule: no confident statement without support.
- (+) Small: a new value and a source rule, no new column.
- (-) Most `accepted` values in existing registries become `not known` until someone finds a source. That is honest, but it reads as a downgrade.

### Option B: Drop Contestedness; keep only stated / not stated
- (+) Simplest.
- (-) Loses `contested`, the value that matters most: DR-027 requires a claim resting on a contested starting point to say so in its text.

### Option C: Keep the three values, and add guidance on judging acceptance
- (+) No schema change.
- (-) Leaves `accepted` uncheckable. The reader's objection stands.

## Decision (proposed)

**Option A.**

1. **Values:** `accepted` (with a source), `contested` (with a source that disputes it), `own`, `not known`.
2. **Where the source goes:** in the Status cell or a note after the row, in the `src:` notation used for claims, for example `accepted (src: ICMJE 2026)`. No new column.
3. **What counts:** a source *showing acceptance*: a standard, guideline, textbook or review that adopts it, or a survey of the field. One paper that merely uses the notion shows that it exists, not that it is accepted.
4. **Paper prose:** the declared-starting-point check reads "checked for being stated, and for whether it is the paper's own, contested, or accepted in the field; 'accepted' needs a source that shows it, and otherwise the record says it is not known."

## Consequences

- **Templates and glossary:** `templates/claim-registry.md` (*Declared starting points* and the rule after the table), `docs/glossary.md` (*declared starting point*, *assumption*). DR-027's schema line gains the fourth value; DR-027 stays Accepted, amended by this record.
- **Tools:** `tools/check_registry.py` (if it validates Contestedness values) accepts `not known` and, for `accepted` and `contested`, warns when no `src:` is given.
- **Paper 1:** D1, D4 and D7 become `not known`. D4 notes that ICMJE sources the category, not the definition; D7 notes the weaker form Moher et al. support. The §4 declared-starting-point bullet is reworded as in Decision 4. The Values row of the paper's contribution table may say that both values are the paper's starting points, not established norms.
- **Adopters:** a MINOR release. Existing `accepted` values remain readable; the tool warning prompts a source.

## Acceptance Condition

Accept when the rule has been applied to a second registry by someone other than the session agent, and at least one `accepted` value there either gained a source or became `not known` with its author's agreement.

## Open Questions

- DR-027's open question: should a `contested` starting point cap the tier of claims resting on it? The same question now applies to `not known`. Proposal: neither caps the tier, but a P0 claim resting on one says so in its text.
- Does `own` need anything checked? It is checkable only in the weak sense that the author asserts it. A search for prior statements (as for a claim) would make it heavier than the reader's objection requires.

## Revisit If

- `not known` becomes the majority value across registries, so that the label carries no information. Then consider dropping `accepted` and keeping only `contested` / `own` / `not known`.
