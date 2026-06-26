# DR-018: Notation-Consistency Checker as an Opt-In Agent

---
status: Proposed
date: 2026-06-25
---

## Context

The framework's verification surface has three agent/checklist lenses that operate on a manuscript's body:

- **`agents/equation-checker.md`** (DR-009) — *correctness*: reproduces equations, checks units, verifies numerical results and that **values** agree across the document (its Step 4, "internal consistency").
- **`templates/anti-hallucination.md`** (incl. generalized Step Z, DR-017) — *citations + tier-monotonicity*: is each source real and does the language tier match the evidence tier.
- **`templates/vv-framework.md` §4.6 Scope Drift** (v2.5) — *promised vs delivered*: does each abstract/contribution promise get delivered.

None of these covers a fourth, distinct exposition lens: **is every mathematical symbol defined — in the notation table and/or glossed at first use — before a reader meets it?** A symbol can be:

- used in an equation but never defined anywhere (`UNDEFINED`),
- defined later than its first use with no forward pointer (`USED-BEFORE-DEF`),
- named one way in the glossary and another way in the body (`INCONSISTENT`),
- glossed nowhere at a first use where a reader expects it, though present in the notation table (`PROSE-GAP`).

The equation-checker's internal-consistency step does **not** catch these, because it audits whether *values* are consistent, not whether *symbols* are introduced. The two are disjoint: one is about the numbers a symbol carries, the other about whether the reader knows what the symbol means. A `44/44` correctness pass can sit on top of a paper whose first equation uses two undefined-in-prose symbols.

This DR was triggered by a dog-fooding run on an external adopter paper (see *Evidence Base*): a 47-symbol sweep surfaced a real glossary-vs-body symbol-name inconsistency that the equation-checker had passed clean, plus several lower-severity gaps. The class of defect is real, recurrent in equation-heavy papers, and currently has no home in the framework.

### Status of related work

- **DR-009** — Accepted. Equation/calculation verification. The notation checker is its sibling, not its replacement; the boundary between them is stated in *Scope* below.
- **DR-017** — Accepted. This repo is custodian of the operationalized typed-verification layer. A notation checker is a natural addition to that layer.
- **`agents/README.md`** — the "paste-as-system-prompt, no per-project state" heuristic places a notation checker squarely in `agents/` (it does not accumulate state, it just runs), alongside `equation-checker.md`.
- **Conditional gates 2.6–2.8** (`templates/vv-framework.md`) — precedent for *project-conditional* quality gates. A notation gate would be 2.9, conditional on the work having a formal symbol table / heavy math.

## Options Considered

### Option A: Status quo — no notation lens
- (+) Zero surface added; framework stays lean.
- (-) Leaves a real, recurrent defect class (symbol-definition completeness) with no owner.
- (-) Risks the false comfort of a clean equation-check pass reading as "notation is fine too."

### Option B: Fold notation checks into `agents/equation-checker.md`
- (+) One agent, one pass.
- (-) Collapses two disjoint lenses (value-consistency vs symbol-definition) into one verdict; the equation-checker's "correctness only, do not assess style" charter explicitly excludes exposition. Muddies what a "pass" means.
- (-) Forces the notation lens to run wherever the equation-checker runs, even on papers where it adds nothing beyond what the equation pass already implies.

### Option C: Standalone opt-in agent + project-conditional gate *(proposed)*
- (+) Mirrors the framework's established "one agent per lens" shape; sibling to `equation-checker.md`.
- (+) Opt-in / conditional, so non-math work (e.g. the journalism-studies adopter case) carries no dead weight.
- (+) Keeps the equation-checker's correctness verdict clean; the two artefacts cross-link.
- (-) One more agent file to maintain.
- (-) Narrower applicability than the universal lenses (only papers with formal notation).

### Option D: Guidance prose only (a writing-guide bullet, no agent)
- (+) Lowest cost.
- (-) Not systematically runnable; the defect class is exactly the kind a human author misses precisely because they already know their own symbols. An agent pass is what makes it reliable.

## Proposed Decision (pending field-test)

**Option C: a standalone, opt-in notation-checker agent, plus a project-conditional Gate 2.9.**

The agent is drafted and staged at **`extensions/notation-checker.md`** (staged, not live, while this DR is Proposed — same discipline as DR-015's "no template changes in this session" and DR-014's `extensions/` precedent). The opt-in / conditional shape matches the framework's standing preference for minimum surface change and for not imposing math-paper machinery on non-math work.

This DR is **Proposed**, not Accepted. Promotion is contingent on the checks in *Pending Assessment*.

### The boundary vs. equation-checker (the load-bearing distinction)

> **Equation-checker checks that VALUES agree across the document. Notation-checker checks that SYMBOLS are defined before use.** Different objects; no overlap.

Worked illustration from the dog-fooding run: the first equation passed the equation-checker (form and dimensions correct), yet two of its symbols were never glossed in the surrounding prose — caught only by the notation pass. Conversely, a renamed glossary symbol (a notation defect) carried no wrong *value*, so the equation-checker correctly stayed silent.

### Scope of the proposed change

If accepted, the following land together as one coordinated commit batch:

- **Promote `extensions/notation-checker.md` → `agents/notation-checker.md`** and remove the `extensions/` staging copy.
- **`agents/README.md`** — add a row for the notation checker (Role: symbol-definition auditor; Input: manuscript + notation table; Output: per-symbol status with fixes) and note the explicit boundary vs. equation-checker.
- **`templates/vv-framework.md`** — add **Gate 2.9: Notation Completeness (conditional — applies when the work has a formal symbol table / heavy math)**, in the same shape as Gates 2.6–2.8. Skip-clause for prose-only work. Draft criteria:
  - [ ] Every symbol used in an equation or inline math is defined in the notation table or glossed at/before first use
  - [ ] No symbol is used before its definition without a forward pointer
  - [ ] No symbol is named one way in the glossary and another in the body (glossary↔body consistency)
  - [ ] Glossary symbols are actually used in the body (no orphan rows)
  - [ ] Defects are fixed by minimum-surface remedy (a rename or a short inline gloss), not a rewrite
- **`docs/framework-summary.md`** — add the notation checker to the Cross-Cutting / verification surface list, with the one-line boundary vs. equation-checker.

### What stays unchanged

- **`agents/equation-checker.md`** charter — correctness only, "do not assess style." Its internal-consistency step still audits *values*, not symbols.
- **`templates/anti-hallucination.md`** and **§4.6 Scope Drift** — untouched.
- **Quality gates 1–4 and conditional gates 2.6–2.8** — no criterion change; 2.9 is purely additive and conditional.
- **Non-math adopters** — carry no new obligation; the gate is conditional and the agent is opt-in.

## Consequences

If Accepted:

- Equation-heavy papers gain a reliable, runnable symbol-definition audit that produces an artefact in the same style as the equation-check report, cross-linked to it.
- The equation-checker's correctness verdict stays clean and unambiguous.
- Adopters of non-math work are unaffected (conditional gate, opt-in agent).
- CHANGELOG version bump: **MINOR** — additive agent + conditional gate, no breaking change, no registry-shape change.

If Rejected:

- DR-018 closes with rationale (e.g. the defect class proves too rare across adopter papers to justify a dedicated agent), and the notation discipline survives, if at all, as a one-line bullet in the writing-guide (Option D fallback).

## Pending Assessment

Before promotion from Proposed to Accepted:

1. **Second adopter field-test.** Run the staged agent on a *second* equation-heavy paper (e.g. the framework's own empirical/DSP dog-fooding corpus, or a second adopter manuscript). If it surfaces ≥1 genuine `UNDEFINED` / `USED-BEFORE-DEF` / `INCONSISTENT` defect that no other lens would catch, the lens earns its keep. (N=1 so far — see *Evidence Base*.)
2. **Boundary-non-overlap check.** On that same paper, confirm the notation findings are disjoint from the equation-checker's internal-consistency findings (no double-reporting). If they overlap materially, reconsider Option B (fold-in).
3. **False-positive rate.** Audit the `PROSE-GAP` findings from at least one run: are they real reader-facing gaps, or noise from a comprehensive notation table that makes inline glosses redundant? If `PROSE-GAP` is mostly noise, demote it from a reported status to a silent/optional one so the agent's signal stays high.
4. **Cross-vendor pass.** Run the agent under a second model family (per DR-011's cross-vendor discipline) to confirm the symbol inventory and classifications are not model-specific.

## Key Insight

**A clean correctness pass and a clean exposition pass are independent guarantees, and conflating them hides the gap between them.** The equation-checker answers "are the numbers right?"; it cannot answer "will a reader know what this symbol means when they first meet it?" Those are orthogonal failure modes — a paper can be numerically flawless and notationally opaque, or notationally pristine and arithmetically wrong. The framework already separates lenses elsewhere (Step Z distinct from the citation checklist; Scope Drift distinct from claim coverage); the notation checker is the same move applied to symbol exposition. The cheapest place to catch a symbol defect is a dedicated pass that does nothing else.

## Evidence Base

- **Dog-fooding run, 2026-06-25 — adopter paper (infant-CPR-manikin mechanical-fidelity submission, V0.27).** A 47-symbol sweep using the staged `extensions/notation-checker.md` returned: 41 `OK`, 1 `INCONSISTENT`, 1 `UNDEFINED` (soft), 3 `PROSE-GAP`, 1 `UNUSED`. The `INCONSISTENT` finding — a scaling exponent named one symbol in the notation table and a different symbol everywhere it was used in the body — was independently confirmed by two separate reads and had been **passed clean by the equation-checker** (no wrong value attached), establishing the boundary claim empirically: the notation lens caught a defect the correctness lens structurally could not. The same paper's first equation was a `PROSE-GAP` (two symbols defined in the notation table but not glossed in the surrounding prose), which is what prompted the human author to ask for a systematic sweep.
- **N=1 caveat.** This is a single adopter paper. Pending Assessment #1 (a second field-test) and #4 (cross-vendor) gate promotion precisely because one run does not establish that the defect class is common enough to warrant a permanent agent.
- **No cross-vendor run yet** for this agent (DR-011 Pass 3 discipline not yet applied).

## Open Questions Carried Forward

- **Should `PROSE-GAP` be a reported status or a silent one?** If comprehensive notation tables make inline glosses genuinely redundant in a given venue's house style, `PROSE-GAP` may be noise. Pending Assessment #3 tests this; the status taxonomy is permissive enough to demote it without restructuring the agent.
- **Glossary-vs-body as a tooling check.** The `INCONSISTENT` (glossary symbol ≠ body symbol) and `UNUSED` (glossary orphan) classes are partly mechanisable — a script could diff the set of symbols in the notation table against the set used in the `.tex` body. Whether to add such a check to `tools/` (alongside `coverage.py` / `check_dois.py`) is a downstream question; the agent pass is the first, more flexible form.
- **Interaction with `glossary.md`.** Multi-paper projects share a binding glossary (per several adopters' ADR-003-style decisions). A notation checker could, in principle, verify body symbols against the *shared* glossary, not only the paper-local notation table. Deferred until single-paper uptake is established.
- **Generalisation beyond symbols.** Abbreviations / acronyms (`\ac{}`-style) are the same defect class one level up (defined-at-first-use). Whether the agent should also audit acronym introduction, or whether that belongs to a separate pass, is unsettled.

## Revisit If

- The second field-test (Pending Assessment #1) surfaces no defect that other lenses miss — close DR-018 and fall back to Option D (writing-guide bullet).
- The boundary-non-overlap check (#2) shows material double-reporting with the equation-checker — reconsider Option B (fold the notation step into the equation-checker as an explicitly separate sub-section).
- `PROSE-GAP` proves to be mostly noise (#3) — demote it to a silent/optional status.
- A `tools/`-based glossary↔body diff proves to catch the `INCONSISTENT` / `UNUSED` classes more cheaply than an agent — narrow the agent's scope to the judgement-bound classes (`USED-BEFORE-DEF`, `PROSE-GAP`) and move the mechanical classes to tooling.
- An adopter reports the conditional Gate 2.9 fires on prose-only work — tighten the skip-clause.
