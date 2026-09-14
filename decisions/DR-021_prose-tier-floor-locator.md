# DR-021: Prose Tier-Floor Scanning as a Locator, Not a Gate

---
status: Proposed
date: 2026-09-14
---

## Context

Tier-monotonicity is the rule the confidence-tier table is an instance of: *prose language tier ≤ the registered confidence tier for the same entry* (`docs/framework-summary.md`). Citation drift, overclaiming and Step Z are all the same failure — language climbing above the evidence. It is the framework's most load-bearing rule and the only major one with **no mechanical support whatsoever**.

The inputs for a mechanical scan all exist already, which is what makes the question live rather than speculative:

- the word→tier map is fixed and normative (`templates/writing-guide.md`, DR-002): ESTABLISHED = *demonstrates / shows / confirms*; SUPPORTED = *indicates / supports / evidence suggests*; EMERGING = *may / preliminary evidence*; SPECULATIVE = *warrants investigation / remains unclear*
- the registry declares a tier per entry
- the manuscript carries `% S#-#:` anchors binding prose to entries

So a scan is constructible today: for each anchored span, flag any tier-word ranking above the entry's registered tier. `tools/check_registry.py` (2026-09-14) already parses two of the three inputs.

### The ambiguity this DR has to resolve first

Two shipped documents state the rule differently, and the difference decides the whole question:

| Source | Statement | Decidable? |
|---|---|---|
| `docs/verification-hooks.md` | "Nothing mechanical can decide whether a sentence's confidence tier exceeds **its evidence** — that is Step Z, and it stays a human-and-agent pass." | No |
| `docs/framework-summary.md` | "prose language tier ≤ **the registered confidence tier** for the same entry" | Yes |

These are different rules. *Prose vs. evidence* is irreducibly judgment. *Prose vs. the tier already declared in the registry* is internal consistency between two artifacts the author controls. The second is the form actually written down as the rule, and it is mechanisable.

The hooks sentence is not wrong — it is unqualified. Whatever this DR concludes, that sentence needs a scope qualifier, or the two documents will keep disagreeing about whether this work is possible.

### Status of related work

- **DR-002** — Accepted. Supplies the four tiers and the word map this would scan for.
- **DR-017** — Accepted. Generalised Step Z into the framework; this DR proposes tooling *under* Step Z, not a replacement for it.
- **DR-018** — Proposed. Precedent for staging a mechanical checker in `extensions/` rather than shipping it into `agents/` or `tools/` on first proposal.
- **DR-020** — Proposed. Its first draft proposed a mechanical circularity test that was rejected outright; the rejection reasoning governs this DR and is quoted below.
- **`tools/check_registry.py`** — the graph half of tier-monotonicity (a conclusion may not outrank its weakest premise) is already implemented and fully decidable. This DR concerns only the *prose* half.

### The governing constraint

`memory/dead-ends.md`, on the rejected DR-020 substitution test:

> be suspicious of mechanical-looking tests in this area generally: **a determinate-but-invalid test is worse than an acknowledged judgment call**, because it manufactures confident false positives with procedural authority.

Any option here must clear that bar. Two further dead-ends entries point the same way: plausibility-style equation review failed 0/3 where mechanical reproduction caught 3/3 (the discriminative procedure cannot be substituted by a cheaper-looking one), and the anti-hallucination scope entry establishes that a gate's *scope* is itself something to verify.

### Why a naive scan would be invalid

Four failure sources, none of them marginal:

1. **Ordinary modal use.** "The effect *may* be seen in Table 2" carries no confidence claim. *May* is the single most common word in the EMERGING band and the most common English modal.
2. **Quotation and attribution.** "Palmblad et al. state the specification *demonstrates* compliance" reports someone else's tier, not the author's.
3. **Negation and hedged construction.** "does not demonstrate", "stops short of showing" invert the tier while matching the word.
4. **Span attribution is unsound.** Anchors mark where an entry's prose *begins*; nothing marks where it ends. A sentence two paragraphs below an anchor may belong to a different entry, to no entry, or to framing prose. **This is the strongest objection**, because unlike the first three it cannot be fixed by a better word list — it is missing data in the source format.

## Options Considered

### Option A: Status quo — Step Z stays entirely manual
- (+) Zero new surface; no false-positive risk; no new failure mode.
- (+) Honours the `verification-hooks.md` position as written.
- (-) Leaves the framework's central rule with no mechanical support, while every adjacent rule has some.
- (-) The 2026-03 retrofit audit found over-confident language in 6 of 22 entries — a single-audit figure registered at EMERGING (`S3-3`), not a calibrated rate, but the only measurement the repo has. Manual-only is what produced it.

### Option B: A gate — fail the build on any tier-word above the registered tier
- (+) Enforceable; would appear in `make check` alongside everything else.
- (-) **Rejected on the dead-ends bar.** All four failure sources above produce confident false positives, and span attribution makes them unfixable in principle. This is precisely the determinate-but-invalid test that entry warns against.
- (-) A gate that cries wolf gets suppressed, taking the true positives with it.

### Option C: A locator — report candidate sentences with counts; a human adjudicates
- (+) Clears the dead-ends bar by claiming nothing: it returns *where to look*, not *what is wrong*. A false positive costs one glance, not a suppressed check.
- (+) Structurally identical to `agents/equation-checker.md`, which the framework already accepts: mechanical reproduction locates, human judgment adjudicates. That precedent is the argument.
- (+) Span unsoundness degrades to noise rather than to error — an unattributable sentence is simply a candidate a human dismisses.
- (-) Adds a surface with an ongoing maintenance cost and no enforcement.
- (-) Risks the green-checkmark effect if anyone mistakes a clean locator run for a completed Step Z.

### Option D: An LLM tier classifier — have a model judge each sentence's tier
- (+) Handles negation, quotation and modal ambiguity that a word list cannot.
- (-) **Rejected.** It substitutes a judgment-shaped procedure for the judgment, which is the shared failure of two existing dead-ends entries. It also makes Step Z's output depend on the same class of system that produced the prose — DR-020's circular-evidence problem, now in the checker itself.
- (-) `S1-2`'s own source (Liang et al. 2024, verified) is that LLMs catch surface issues and struggle with deep argument analysis. Tier calibration is the deep kind.

## Decision

**Option C: a locator, staged in `extensions/`.**

Three properties are normative and not negotiable in implementation:

1. **It reports candidates and counts, never verdicts.** Output names a sentence, the matched word, its band, and the entry's registered tier. It never says a sentence is wrong. The word "violation" does not appear in its output.
2. **It never gates.** Not in `make check`, not as a verification hook, not as a Gate 2 precondition. Exit code is 0 whenever it ran successfully, whatever it found.
3. **It does not discharge Step Z.** Its output is an input to the human pass. Any documentation of it says so in the same breath as describing it.

Staged in `extensions/` rather than shipped, per the DR-018 precedent, until the measurement below exists.

Accepting this DR also requires a scope qualifier on the `docs/verification-hooks.md` sentence, distinguishing *prose vs. evidence* (not decidable) from *prose vs. registered tier* (decidable, and what this locates).

## Consequences

- The framework gains mechanical support for its central rule without claiming a decision procedure for it. The claim stays exactly as strong as the evidence: *here are the sentences worth re-reading*.
- `docs/verification-hooks.md` gains a qualifier; until it does, two shipped docs disagree.
- A measurement becomes possible that the framework currently lacks. Run the locator over Paper 1, adjudicate every candidate by hand, and record precision. That number decides whether this ever leaves `extensions/` — and it is the sort of own-data evidence the `S4-*` entries currently lack, all of which rest on tier F ("own design rationale").
- Span attribution is now a known-unsound input. If it proves to be the dominant noise source, the fix is in the *manuscript* format (an end-marker convention), not in the locator — and that would be a separate DR, touching a shipped template.
- Accepting this adds a 21st decision record, which breaks the self-verifying count probe in `CLAUDE.md`'s decisions row. That probe is doing its job; the row needs updating as part of acceptance.

## Revisit If

- Hand-adjudicated precision on Paper 1 falls below ~50%. At that rate the locator costs more attention than it saves and Option A was right.
- Anyone proposes promoting it to a gate or a hook. That is Option B arriving by increment, and it needs to re-argue the dead-ends bar explicitly rather than inherit this DR's acceptance.
- A manuscript end-marker convention is adopted, making span attribution sound. The calculus changes materially and Option B becomes arguable for the first time.
- Step Z's manual pass stops finding tier drift the locator missed — evidence the locator's recall is high enough to reconsider its standing.
