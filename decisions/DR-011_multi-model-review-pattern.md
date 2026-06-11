# DR-011: Multi-Model Review Pattern

---
status: Proposed
date: 2026-05-12
---

## Context

The framework currently specifies, in `README.md:190` and `README.md:375`, that peer-review simulation should run in a **fresh session — or a different model entirely**. This single-tier guidance under-specifies the most important axis: *what kind of bias the reviewer is trying to escape*.

Two distinct bias-escape problems are being conflated:

- **Sunk-cost-from-the-drafting-session bias** — the reviewer has the drafting context in working memory and rationalises rather than critiques. A fresh session in the *same model family* escapes this.
- **Training-data / stylistic-prior bias** — the reviewer shares the drafting model's training distribution and stylistic defaults. A *cross-vendor* model is needed to escape this.

These are different problems and respond to different tools. The current guidance ("use a different model") collapses them.

### Three reviewer characters

A three-reviewer comparison applied the same review-prompt rubric across three reviewer configurations:

| Reviewer | Review character | Cost |
|---|---|---|
| Intra-family small (e.g., Haiku-class) | Rigorous checklist application | Cheap |
| Intra-family large (e.g., Opus-class) | Argument-shape critique | ~10x Haiku |
| Cross-vendor (e.g., Gemini, GPT) | Outside-family perspective, but suggestions tend to violate the project's style/voice | Variable |

Each reviewer catches essentially **disjoint** issues. The small intra-family model rigorously applies the checklist; the large intra-family model surfaces argument-shape critique; the cross-vendor model suggests outside-family perspective but tends to drift into style-violating "improvements" that need filtering before delivery.

The pattern is plausible enough to land structurally; specific cost-tier prescriptions are provisional (see *Revisit If*).

## Options Considered

### Option A: Leave the single-tier guidance in place
- (+) Simplest; no framework changes
- (+) Honours the N=1 evidence limit
- (-) Loses the bias-escape distinction surfaced by the empirical observation
- (-) Doesn't address the style-violation failure mode for cross-vendor reviewers — a real and previously-unflagged risk

### Option B: Specify a two-pass pattern (intra-family + cross-vendor)
- (+) Captures the main bias-escape distinction (sunk-cost vs. training-data)
- (-) Misses the within-family size effect — Haiku and Opus caught disjoint issues, not redundant ones
- (-) Collapses two genuinely different review characters (checklist-rigour vs. argument-shape) into one

### Option C: Three-pass pattern with explicit bias-escape semantics + mandatory style/voice filter for cross-vendor
- (+) Names the three distinct review characters that emerged empirically
- (+) Pairs each pass with the bias it escapes — engineers can reason about what each pass is for
- (+) The style/voice filter requirement directly addresses the cross-vendor failure mode
- (-) Three passes per review is more surface than the current guidance
- (-) Within-family-size finding rests on N=1 — may not generalise; specific cost-tier defaults are provisional
- (-) "Pass" terminology must be chosen to avoid collision with existing "Tier" semantics in the framework

## Decision

**Option C: Three-pass review pattern with explicit bias-escape semantics and a mandatory style/voice filter for cross-vendor passes.**

### Naming: "Pass", not "Tier"

The framework already uses "tier" for two distinct things:
- CLAIM confidence (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) — DR-002
- PROVOCATION confidence (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) — DR-010

A third "tier" semantic for reviewer strength would be confusing. The pattern uses **Pass 1 / Pass 2 / Pass 3**, with the bias each pass escapes named explicitly.

### The three passes

| Pass | Reviewer | Bias escaped | Review character | Default applicability |
|------|----------|--------------|------------------|----------------------|
| **Pass 1** | Intra-family small (e.g., Haiku-class) | Sunk-cost-from-the-drafting-session | Rigorous checklist application | Every publish |
| **Pass 2** | Intra-family large (e.g., Opus-class) | Sunk-cost-from-the-drafting-session | Argument-shape critique | Blog-scale: every publish. Paper-scale: every major revision / before each phase gate. |
| **Pass 3** | Cross-vendor (e.g., Gemini, GPT) | Training-data and stylistic priors | Outside-family perspective | High-stakes content only, **with mandatory style/voice filter** |

Passes 1 and 2 are **complementary, not redundant** — different model sizes within a family applied the rubric differently in the triggering observation. Pass 3 is opt-in.

### Style/voice filter for Pass 3

Cross-vendor reviewers tend to generate style-violating suggestions because they do not share the project's stylistic priors. To prevent the human from having to manually discard most output, `agents/review-prompt.md` adds a **"Style/voice rules to filter against"** placeholder:

- For academic-paper projects: defaults to the target journal's style guide
- For non-fiction / blog projects: defaults to the project's voice rules
- The placeholder is **required with a sensible default**, not optional — forces every project to articulate its style boundary before running Pass 3, without blocking projects whose style is journal-conventional

The reviewer is instructed to **pre-filter suggestions against these rules** before delivery, so the human receives only suggestions that pass the style gate.

### Adoption readiness

- **Ready to merge through this decision:**
  - The three-pass structure with bias-escape semantics
  - The style/voice filter placeholder as a required-with-default field in `agents/review-prompt.md`
  - README update at lines 190 and 375 to point at the new pattern
  - Step 7 in `templates/anti-hallucination.md` implementing cross-model verification

- **Provisional (re-evaluate at paper scale):**
  - The specific cost-tier prescriptions ("every publish" vs. "every major revision")
  - The disjoint-coverage claim between intra-family small and large
  - The cost-benefit framing of Pass 3 as "high-stakes only"

- **Pattern note (useful when applicable):**
  - The generality of the within-family-size effect beyond Claude (Opus/Haiku)

## Key Insight

**Different bias-escapes need different reviewers.** "Use a different model" is the right intuition but the wrong granularity. A fresh session in the same family escapes the sunk-cost the drafting agent accumulated. A cross-vendor model escapes the training and stylistic priors the entire family shares. These are different objectives — collapsing them obscures both what each pass is for and when each is worth its cost.

A second-order insight, specific to Pass 3: **the more bias a reviewer escapes, the more its suggestions will violate the project's style.** A reviewer that genuinely doesn't share the drafting context will also not share the drafting conventions. The mandatory style/voice filter is the operational fix.

## Design Rationale: Functorial Composition

The three-pass structure has a structural rationale beyond the empirical observation that catalysed it. Each pass is a different *view* of the manuscript — a functor onto a constraint space — that preserves some structural information and discards other. Their findings are partial *by construction*, not by accident, and the combined verification is what survives every pass.

- **Pass 1 (intra-family small)** preserves checklist-compliance information. It loses argument-shape information: the small model lacks the capacity to hold a multi-paragraph chain of reasoning in working memory while simultaneously enforcing a rubric.
- **Pass 2 (intra-family large)** preserves argument-shape information. It loses some of the rigour of mechanical rubric application: a large model is harder to anchor on a checklist than on the rhetorical pull of the prose.
- **Pass 3 (cross-vendor)** preserves training-distribution-independent information. It loses the project's stylistic priors: the cross-vendor reviewer cannot reliably distinguish substantive critique from suggestions that violate the project's voice rules, which is why the style/voice filter is mandatory rather than optional.

What survives every pass is the verified claim. Equivalently, the combined verification is a *limit* of the three pass-functors. The decomposition is the design choice. Adding a fourth pass requires showing it preserves invariants the existing three do not. Skipping a pass requires showing its invariants are preserved elsewhere.

This framing matters operationally for three decisions:

1. **Why both intra-family passes when only one model family is involved.** Pass 1 and Pass 2 preserve different invariants (checklist-compliance vs. argument-shape); collapsing them loses one. The triggering observation showed this empirically; the functorial framing names why it is structural rather than accidental.
2. **Why the cross-vendor pass requires a style filter.** Pass 3's invariant is training-distribution independence. The price of that independence is that the cross-vendor reviewer cannot also preserve project-specific style. The filter recovers what Pass 3 must structurally drop.
3. **What "no further reviewer adds value" means.** When a candidate next reviewer's invariants are already preserved by the existing battery, adding it is redundant. The structural test is the cleaner version of the empirical "did this reviewer surface findings the others did not."

Background: `docs/category-theory-as-design-lens.md`, principle 3 ("multi-pass verification is a limit of functors"). The framing does not require category-theory vocabulary in operational use of this DR; the principle is what carries.

## Consequences

- `agents/review-prompt.md`: add "Style/voice rules to filter against" as a required field with format-appropriate default; add filter-before-delivery instruction.
- `templates/anti-hallucination.md`: add Step 7 — "Multi-pass review across model families" — specifying the three passes by name and the style-filter requirement for Pass 3.
- `README.md:190` and `README.md:375`: replace "fresh session or different model" with a pointer to the three-pass pattern.
- `CLAUDE.md`: no change — existing pointer to `agents/review-prompt.md` is sufficient.
- Active papers (`papers/perspective/`): no immediate action; the three-pass pattern applies on the next major revision.

## Evidence Base

- Mechanism caveat: the triggering observation conflates training-data bias and stylistic-prior bias for cross-vendor reviewers. The DR claims the operational effect (style filter needed) without committing to which mechanism dominates.
- **Token-cost replication (2026-06-08), code-tooling scale.** Within-Claude application to `tools/coverage.py` + `tools/check_dois.py` (~620 LOC of Python) across two batteries: scaffolding stage + parser stage. Pass 1 (Haiku, subagent `total_tokens`) averaged **36,812 tokens** across N=2 with **0 / 2 rounds load-bearing findings** (1 false positive in the scaffolding round). Pass 2 (Opus, subagent `total_tokens`) averaged **52,540 tokens** across N=2 (**~1.4× Pass 1**) with **2 / 2 rounds load-bearing design findings** that would have shipped broken without it. Per-operation log: `papers/perspective/vv/cost-log.md`. Subagent tool results report `total_tokens` only — input/output/cache breakdown not surfaced at this granularity, so per-pass economics here is total-only.
- **Token-cost replication (2026-06-11), paper-scale prose.** Within-Claude application to the framework's own home document (v2.1.0–v2.1.2 README sections + `docs/non-claude-setup.md` + `agents/README.md` + CHANGELOG entries, ~500 lines of new prose). Pass 1 (Haiku) **81,464 total tokens** with **5 load-bearing findings** (10 tool uses; checklist-rigour character: stale paths, format consistency, freshness markers, procedural-discipline gaps, label-vs-tier tensions). Pass 2 (Opus) **69,747 total tokens** with **5 load-bearing findings** (5 tool uses; argument-shape character: warrant-counter omissions, aspirational framing, motivated retrospection, principled-distinction edges, principle-overreach). **Zero overlap between the two pass's load-bearing findings** — first paper-scale prose confirmation of the disjoint-coverage prediction at intra-family scale. **Token-cost ratio inverted** vs. 2026-06-08 (Pass 2 was ~0.86× Pass 1, where it was ~1.4× at code-tooling scale) — Pass 1's checklist character required more file reads (10) than Pass 2's argument-shape character (5), suggesting the size-vs-cost relationship depends on artefact type. Per-operation log: `vv/cost-log.md` (framework self-application, new in v2.2.0). N=1 at this scale; not yet aggregable.
- **Paper-scale cross-vendor data point (2026-06-11), Pass 3 via Gemini.** Same scope as Pass 1 + Pass 2 (v2.1.0–v2.1.2 work). Run via `gemini -p` headless (CLI v0.45.2); the four artefact files plus the Rubric B definition from `agents/review-prompt.md` bundled inline in the prompt rather than fetched. **~21,000 tokens estimated** (byte-based: ~80 KB prompt / ~5 KB response; gemini CLI does not report token counts in stderr). **~30 s wall.** Weighted score **4.2 / 5.0** on Rubric B (above ≥3.5 ship-readiness threshold). **3-4 novel load-bearing findings**: Toulmin/Whetten jargon used without definition or citation (README:120, 621); Step 6 "Delegation Paradox" — anti-hallucination Step 6 is a P0 gate that cannot be delegated without circularity, in tension with the "delegate most" framing; three-way structural cut alternative — `templates/` (state) + `agents/` (prompts) + `procedures/` (manual checklists); terminology micro-violations Pass 1 missed (e.g., "credibility move" README:625). **4-of-7 findings overlap with Pass 2**: identical match on v2.1.1 CHANGELOG "over-cautious" performative register; mechanism overlap on delegation aspirational framing (Pass 2 anchored at Step 3 human-judgement, Pass 3 at Step 6 circularity); topic overlap on `agents/` vs `templates/` soft edge (Pass 3 proposes the novel three-way cut Pass 2 didn't); validating engagement on auto-memory Hard Constraint narrowing (Pass 3 *agrees* with v2.2.0's narrowing direction). **Two-tier empirical pattern emerges:** the "essentially disjoint" framing in Context above holds for intra-family (Pass 1 ↔ Pass 2 = zero overlap at both code-tooling and prose scale), but does *not* extend cleanly to cross-vendor at paper-scale prose. The weaker `memory/hypothesis-log.md` prediction (≥1 novel load-bearing item from Pass 3) is confirmed with margin. Structural implication for the DR: Pass 3's marginal value at high-stakes is content-novelty + style-priors escape, but ~half of its findings at paper-scale prose can be pre-empted by Pass 2 — sequencing matters. **Methodological caveat:** Pass 3's token cost is not directly comparable to Pass 1+2's because of delivery-mechanism asymmetry (inline content vs. multi-round file navigation). Apples-to-apples re-run would have Pass 3 navigate to a public artefact (raw GitHub URL or local clone) the same way Passes 1+2 did. Per-operation log: `vv/cost-log.md`. N=1 at this scale; not yet aggregable. Resolves `memory/hypothesis-log.md` 2026-06-09 entry.

## Open Questions Carried Forward

- **Within-family-size generality.** Disjoint-coverage between intra-family small and large is observed within Claude. **Still untested across families** (GPT-mini vs. GPT-4, Gemini-Flash vs. Gemini-Pro). Re-evaluate on next cross-family application.
- **Pass 2 economics at paper scale.** Full-paper scale (~8,000+ words with multiple revision rounds) still untested. Pass 2 cost on a manuscript revision needs measurement before the "every major revision" default can be considered hardened.
- **Pass 3 yield by content type.** Cross-vendor yield may differ across content types. **Paper-scale prose (2026-06-11):** Pass 3 via Gemini surfaced 3-4 novel + 4 overlap-with-Pass-2 findings. Code-tooling and grant scale still untested. Recommend attempting Pass 3 on those scales to build a multi-content-type cost-vs-yield comparison.
- **Pass 3 ↔ Pass 2 overlap at cross-vendor.** The 4-of-7 overlap observed at paper-scale prose (Pass 3 hit Pass 2 directly on the v2.1.1 "over-cautious" finding and partially on three more) suggests cross-vendor's marginal value at high-stakes depends on whether Pass 2 has already run. Sequential framing — Pass 3 *after* Pass 2 vs. Pass 3 *instead of* Pass 2 — may need to be specified in the DR if this overlap pattern replicates. N=1 at this scale; not yet load-bearing.
- **Paper-scale token cost calibration.** The 2026-06-08 token-cost replication (above) is N=2 within-Claude at **code-tooling scale** (~620 LOC of Python reviewed, not prose). Pass 2 cost on an ~8,000-word manuscript revision is still unmeasured. Tracked in `papers/perspective/vv/cost-log.md` under *Forward-looking entries to gather*.
- **External-ground-truth ρ calibration (ICLR/OpenReview).** Stanford Agentic Reviewer (paperreview.ai, Jiang & Ng, late 2025) reports Spearman ρ = 0.42 vs human ICLR reviewers, matching the 0.41 human-human inter-rater baseline on 147 ICLR 2025 submissions. ICLR 2025 reviews + final scores are publicly accessible via OpenReview API — same data source open to this framework. A 30-paper calibration run (Pass 1 Haiku + Pass 2 Opus, no Pass 3 at this scale) is bounded at ~€44 in compute plus roughly a maintainer-day to build the OpenReview scraper, pre-register a score-mapping from `agents/review-prompt.md` qualitative output to a 1-10 number, and write up. Three outcome bands: ρ ≈ 0.4 supports cross-domain portability (framework runs on a content type it wasn't designed for); ρ ≈ 0.2 is honest scope evidence (review prompt doesn't transfer cleanly to ICLR-style scoring); ρ ≈ 0 is diagnostic for the score-mapping. The aggregate-correlation evidence type is *different from* — not strictly better than — DR-011's existing disjoint-coverage mechanism evidence. Cross-references [vmodel.eu#135](https://github.com/ducroq/vmodel.eu/issues/135) (parallel methodology adoption in the sibling project) and the `agentic-engineering` "LLM behavioural properties" pattern slot (cross-domain prompt transfer is a behavioural property). Not load-bearing; framework's current evidence base supports the multi-pass claims via mechanism, not aggregate ρ. Pickup would be either a backlog action (run it, report it) or a DR-016 proposal (only if the calibration result triggers a methodology change in `agents/review-prompt.md` or DR-011 itself).
- **Dialogical-logic *Underlying Form* subsection (deferred candidate).** A 2026-06-11 survey of patterns from philosophical logic against the framework's current apparatus flagged Lorenzen / Hintikka dialogical logic as a HIGH-FIT candidate for an *Underlying Form* subsection that would recast Pass 1 / Pass 2 / Pass 3 as three rounds of a Proponent-Opponent attack-defense game — naming *why* the bias-escape semantics has the shape it does (parallel to the existing *Design Rationale: Functorial Composition* section's *why*-the-invariants-decompose framing). Deferred until DR-011 stabilises after paper-scale Pass 2 validation AND [DR-015](DR-015_rebutting-undercutting-defeater-distinction.md)'s broader borrowing-pattern bet in [`vv/hypothesis-log.md`](../vv/hypothesis-log.md) resolves — adding a second philosophical-logic conceptual layer before either lands risks paint-on-paint. Pickup would be a DR-016 proposal, not an in-place DR-011 edit.

## Revisit If

- Pass 2 is applied to a paper-scale artefact and the disjoint-coverage finding fails to replicate (Haiku and Opus catch substantially the same issues) → demote Pass 2 from default-for-every-publish to opt-in.
- A cross-family observation shows the within-family-size effect is Claude-specific → revise the Pass 1/Pass 2 split.
- Style-filter pre-delivery proves unreliable in practice (cross-vendor reviewers cannot reliably filter against project style) → move the filter to a human post-review step rather than a reviewer-side pre-filter.
- Pass 3 yield on a highly-technical paper turns out to be high → re-promote Pass 3 from "high-stakes only" to default.
- A different bias-escape axis surfaces (e.g., domain-expert reviewer vs. generalist reviewer) that doesn't fit the intra-family / cross-vendor split → revise the structure to add a fourth pass or reframe the axes.
