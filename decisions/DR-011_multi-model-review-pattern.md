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

Cross-vendor reviewers tend to generate style-violating suggestions because they do not share the project's stylistic priors. To prevent the human from having to manually discard most output, `templates/review-prompt.md` adds a **"Style/voice rules to filter against"** placeholder:

- For academic-paper projects: defaults to the target journal's style guide
- For non-fiction / blog projects: defaults to the project's voice rules
- The placeholder is **required with a sensible default**, not optional — forces every project to articulate its style boundary before running Pass 3, without blocking projects whose style is journal-conventional

The reviewer is instructed to **pre-filter suggestions against these rules** before delivery, so the human receives only suggestions that pass the style gate.

### Adoption readiness

- **Ready to merge through this decision:**
  - The three-pass structure with bias-escape semantics
  - The style/voice filter placeholder as a required-with-default field in `templates/review-prompt.md`
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

- `templates/review-prompt.md`: add "Style/voice rules to filter against" as a required field with format-appropriate default; add filter-before-delivery instruction.
- `templates/anti-hallucination.md`: add Step 7 — "Multi-pass review across model families" — specifying the three passes by name and the style-filter requirement for Pass 3.
- `README.md:190` and `README.md:375`: replace "fresh session or different model" with a pointer to the three-pass pattern.
- `CLAUDE.md`: no change — existing pointer to `templates/review-prompt.md` is sufficient.
- Active papers (`papers/perspective/`): no immediate action; the three-pass pattern applies on the next major revision.

## Evidence Base

- Mechanism caveat: the triggering observation conflates training-data bias and stylistic-prior bias for cross-vendor reviewers. The DR claims the operational effect (style filter needed) without committing to which mechanism dominates.
- **Token-cost replication (2026-06-08), code-tooling scale.** Within-Claude application to `tools/coverage.py` + `tools/check_dois.py` (~620 LOC of Python) across two batteries: scaffolding stage + parser stage. Pass 1 (Haiku, subagent `total_tokens`) averaged **36,812 tokens** across N=2 with **0 / 2 rounds load-bearing findings** (1 false positive in the scaffolding round). Pass 2 (Opus, subagent `total_tokens`) averaged **52,540 tokens** across N=2 (**~1.4× Pass 1**) with **2 / 2 rounds load-bearing design findings** that would have shipped broken without it. Per-operation log: `papers/perspective/vv/cost-log.md`. Subagent tool results report `total_tokens` only — input/output/cache breakdown not surfaced at this granularity, so per-pass economics here is total-only.

## Open Questions Carried Forward

- **Within-family-size generality.** Disjoint-coverage between intra-family small and large is observed within Claude. **Still untested across families** (GPT-mini vs. GPT-4, Gemini-Flash vs. Gemini-Pro). Re-evaluate on next cross-family application.
- **Pass 2 economics at paper scale.** Full-paper scale (~8,000+ words with multiple revision rounds) still untested. Pass 2 cost on a manuscript revision needs measurement before the "every major revision" default can be considered hardened.
- **Pass 3 yield by content type.** Cross-vendor yield may differ across content types. Recommend attempting Pass 3 on the next major content type to build the cost-vs-yield comparison.
- **Paper-scale token cost calibration.** The 2026-06-08 token-cost replication (above) is N=2 within-Claude at **code-tooling scale** (~620 LOC of Python reviewed, not prose). Pass 2 cost on an ~8,000-word manuscript revision is still unmeasured. Tracked in `papers/perspective/vv/cost-log.md` under *Forward-looking entries to gather*.

## Revisit If

- Pass 2 is applied to a paper-scale artefact and the disjoint-coverage finding fails to replicate (Haiku and Opus catch substantially the same issues) → demote Pass 2 from default-for-every-publish to opt-in.
- A cross-family observation shows the within-family-size effect is Claude-specific → revise the Pass 1/Pass 2 split.
- Style-filter pre-delivery proves unreliable in practice (cross-vendor reviewers cannot reliably filter against project style) → move the filter to a human post-review step rather than a reviewer-side pre-filter.
- Pass 3 yield on a highly-technical paper turns out to be high → re-promote Pass 3 from "high-stakes only" to default.
- A different bias-escape axis surfaces (e.g., domain-expert reviewer vs. generalist reviewer) that doesn't fit the intra-family / cross-vendor split → revise the structure to add a fourth pass or reframe the axes.
