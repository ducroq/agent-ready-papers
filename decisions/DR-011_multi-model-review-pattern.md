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

A pending TODO at `audits/feedback-from-fsd.md:208` ("Cross-model verification pattern as Step 7 in `templates/anti-hallucination.md`") anticipated this refinement. This DR implements that Step 7 with the multi-model structure built in.

### Triggering observation (2026-05-11 session at dev.jeroenveen.nl)

A LinkedIn cross-post draft for the article *"Senior developers trust AI less than juniors"* was reviewed by three reviewers using the same `templates/review-prompt.md` Variant B rubric.

| Reviewer | Substantive findings | Voice-rule violations in suggestions | Cost |
|---|---|---|---|
| Haiku (intra-family, small, fresh context) | 0 (all hard rules pass) | 0 | Cheap |
| Opus (intra-family, large, fresh context) | 2 (subtitle drift, CTA pre-loading direction) | 0 | ~10x Haiku |
| Gemini (cross-vendor) | 0 net after filter | 5+ (coined labels, subheadings, slogan copy, slide-register chart suggestion, popular-psych references) | Free for casual use |

Each reviewer caught essentially **disjoint** issues. The small intra-family model rigorously applied the checklist; the large intra-family model surfaced argument-shape critique; the cross-vendor model suggested mostly style-violating "improvements". Combined coverage was strictly greater than any single review. A second cross-vendor review on the published article in the same session showed the same pattern: many suggestions, most failed style rules, near-zero substantive items survived the filter.

Evidence base is **N=1 session at blog scale**. The pattern is plausible enough to land structurally; specific cost-tier prescriptions are provisional and gated on paper-scale application (see *Revisit If*).

## Options Considered

### Option A: Leave the single-tier guidance in place
- (+) Simplest; no framework changes
- (+) Honours the N=1 evidence limit
- (-) Loses the bias-escape distinction surfaced by the empirical observation
- (-) Doesn't address the style-violation failure mode for cross-vendor reviewers — a real and previously-unflagged risk
- (-) Step 7 from `feedback-from-fsd.md` remains pending

### Option B: Specify a two-pass pattern (intra-family + cross-vendor)
- (+) Captures the main bias-escape distinction (sunk-cost vs. training-data)
- (-) Misses the within-family size effect — Haiku and Opus caught disjoint issues, not redundant ones
- (-) Collapses two genuinely different review characters (checklist-rigour vs. argument-shape) into one

### Option C: Three-pass pattern with explicit bias-escape semantics + mandatory style/voice filter for cross-vendor
- (+) Names the three distinct review characters that emerged empirically
- (+) Pairs each pass with the bias it escapes — engineers can reason about what each pass is for
- (+) The style/voice filter requirement directly addresses the cross-vendor failure mode
- (+) Implements pending Step 7 from `feedback-from-fsd.md`
- (-) Three passes per review is more surface than the current guidance
- (-) Within-family-size finding rests on N=1 — may not generalise; specific cost-tier defaults are provisional
- (-) "Pass" terminology must be chosen to avoid collision with existing "Tier" semantics in the framework

## Decision

**Option C: Three-pass review pattern with explicit bias-escape semantics and a mandatory style/voice filter for cross-vendor passes.**

### Naming: "Pass", not "Tier"

The framework already uses "tier" for three distinct things:
- CLAIM confidence (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) — DR-002
- PROVOCATION confidence (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) — DR-010
- Merge readiness in audit recommendations (battle-tested / proven-once / pattern-note) — `audits/feedback-from-fsd.md`

A fourth "tier" semantic for reviewer strength would be confusing. The pattern uses **Pass 1 / Pass 2 / Pass 3**, with the bias each pass escapes named explicitly.

### The three passes

| Pass | Reviewer | Bias escaped | Review character | Default applicability |
|------|----------|--------------|------------------|----------------------|
| **Pass 1** | Intra-family small (e.g., Haiku-class) | Sunk-cost-from-the-drafting-session | Rigorous checklist application | Every publish |
| **Pass 2** | Intra-family large (e.g., Opus-class) | Sunk-cost-from-the-drafting-session | Argument-shape critique | Blog-scale: every publish. Paper-scale: every major revision / before each phase gate. |
| **Pass 3** | Cross-vendor (e.g., Gemini, GPT) | Training-data and stylistic priors | Outside-family perspective | High-stakes content only, **with mandatory style/voice filter** |

Passes 1 and 2 are **complementary, not redundant** — different model sizes within a family applied the rubric differently in the triggering observation. Pass 3 is opt-in.

### Style/voice filter for Pass 3

Cross-vendor reviewers in the triggering observation generated 5+ style-violating suggestions for 0 net substantive findings after filter. To prevent the human from having to manually discard most output, `templates/review-prompt.md` adds a **"Style/voice rules to filter against"** placeholder:

- For academic-paper projects: defaults to the target journal's style guide
- For non-fiction / blog projects: defaults to the project's voice rules
- The placeholder is **required with a sensible default**, not optional — forces every project to articulate its style boundary before running Pass 3, without blocking projects whose style is journal-conventional

The reviewer is instructed to **pre-filter suggestions against these rules** before delivery, so the human receives only suggestions that pass the style gate.

### Adoption readiness

Borrowing the Tier 1/2/3 merge-readiness split from `audits/feedback-from-fsd.md`:

- **Ready to merge (battle-tested through this decision):**
  - The three-pass structure with bias-escape semantics
  - The style/voice filter placeholder as a required-with-default field in `templates/review-prompt.md`
  - README update at lines 190 and 375 to point at the new pattern
  - Step 7 in `templates/anti-hallucination.md` implementing cross-model verification

- **Incubate (proven once at blog scale, re-evaluate at paper scale):**
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
- `audits/feedback-from-blog-application.md` (new): empirical case study of the triggering observation, alongside the existing *Framing Accuracy* and *Retroactive Verification* sections referenced in the originating issue.
- `audits/feedback-from-fsd.md:208`: mark Step 7 as implemented by this DR.
- `CLAUDE.md`: no change — existing pointer to `templates/review-prompt.md` is sufficient.
- Active papers (`papers/perspective/`): no immediate action; the three-pass pattern applies on the next major revision.

## Evidence Base

- Triggering session at dev.jeroenveen.nl (2026-05-11): three-reviewer comparison on a LinkedIn cross-post draft, plus a second cross-vendor review on the published article. Disjoint-coverage finding; cross-vendor style-violation finding.
- Replication at grant scale (2026-05-22) on NLnet NGI Zero Commons Fund v3 application (~3,500 words + 19-entry V&V claim registry): Pass 1 (Haiku) caught 3 P0 + 5 minor defects with 1 false positive; Pass 2 (Opus) caught 5 major weaknesses + 6 suggestions weighted 4.05/5.0 (above NLnet >5.0/7 threshold) with 5 style-violating suggestions correctly pre-filtered. Within-Claude disjoint-coverage pattern replicated. Pass 3 deferred per low-yield caveat — no grant-scale Pass 3 data point gathered. Second application same day on the V&V-wrap edits (~600 words of §5 prose + claims.md updates + audit content drafting): Pass 2 weighted 3.85/5.0.
- Originating issue: [ducroq/agent-ready-papers#7](https://github.com/ducroq/agent-ready-papers/issues/7)
- Grant-scale feedback issue: [ducroq/agent-ready-papers#8](https://github.com/ducroq/agent-ready-papers/issues/8) — Proposal 4 sourced this Evidence Base / Open Questions update.
- Roadmap precedent: `audits/feedback-from-fsd.md:208` (Step 7 cross-model verification was already pending).
- Mechanism caveat: the triggering observation conflates training-data bias and stylistic-prior bias for cross-vendor reviewers. The DR claims the operational effect (style filter needed) without committing to which mechanism dominates; this matches the evidence.

## Open Questions Carried Forward

- **Within-family-size generality.** N=2 within-Claude as of 2026-05-22 (blog 2026-05-11 + NLnet v3 grant 2026-05-22): the disjoint-coverage pattern replicated. Pass 1 (Haiku) caught 3 P0 + 5 minor defects with 1 false positive; Pass 2 (Opus) caught 5 major weaknesses + 6 suggestions (weighted 4.05/5.0) with 5 style-violating suggestions correctly pre-filtered. **Still untested across families** (GPT-mini vs. GPT-4, Gemini-Flash vs. Gemini-Pro). Re-evaluate on next cross-family application.
- **Pass 2 economics at paper scale.** At ~3,450 words (blog) and ~3,500 words + 19-entry registry (grant), Pass 2 cost has remained acceptable; the "every major revision" default is defensible at these content scales. Full-paper scale (~8,000+ words with multiple revision rounds) still untested.
- **Pass 3 yield by content type.** Cross-vendor showed near-zero substantive yield on blog-style prose. Grant-scale application (2026-05-22) deferred Pass 3 per the low-yield caveat — no grant-scale data point gathered. Yield may differ for highly-technical numerical claims or content adjacent to Claude-specific training data. Recommend attempting Pass 3 on next grant or paper to build the evidence base.

## Revisit If

- Pass 2 is applied to a paper-scale artefact and the disjoint-coverage finding fails to replicate (Haiku and Opus catch substantially the same issues) → demote Pass 2 from default-for-every-publish to opt-in.
- A cross-family observation shows the within-family-size effect is Claude-specific → revise the Pass 1/Pass 2 split.
- Style-filter pre-delivery proves unreliable in practice (cross-vendor reviewers cannot reliably filter against project style) → move the filter to a human post-review step rather than a reviewer-side pre-filter.
- Pass 3 yield on a highly-technical paper turns out to be high → re-promote Pass 3 from "high-stakes only" to default.
- A different bias-escape axis surfaces (e.g., domain-expert reviewer vs. generalist reviewer) that doesn't fit the intra-family / cross-vendor split → revise the structure to add a fourth pass or reframe the axes.
