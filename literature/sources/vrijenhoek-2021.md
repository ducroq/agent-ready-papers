# Vrijenhoek et al. 2021 — Recommenders with a Mission (L50)

**Reading status:** READ (input-mapping pass, 2026-07-06) — highest-payoff cluster paper. Resolves both `[2026-06-24]` hypothesis-log bets. **Tier caveat below.**

## Bibliographic Info
- **Authors:** Sanne Vrijenhoek, Mesut Kaya, Nadia Metoui, Judith Möller, Daan Odijk, Natali Helberger
- **Year:** 2021 (arXiv preprint 2020-12-18; CHIIR 2021)
- **Title:** Recommenders with a Mission: Assessing Diversity in News Recommendations
- **Venue:** CHIIR 2021 (Conf. on Human Information Interaction and Retrieval)
- **DOI:** 10.48550/arXiv.2012.10185 — arXiv:2012.10185 [cs.IR]. *(The ACM/CHIIR DOI still needs verifying separately; this is the preprint DOI.)*

## The five metrics + their required inputs

Each metric is tied to a normative democratic model (liberal / participatory / deliberative / critical). **Crucial structural point:** all five are *personalisation-centric* — they compare a **user's recommendation list** against a pool, and Fragmentation compares **across users**. ovr.news is a single, unpersonalised editorial feed (verified: no `user_id`, no reading-history, no per-user lists anywhere in the pipeline). So none is computable *as literally defined*.

The rescue is a reframe: substitute **"editorial selection vs. candidate pool"** for **"user recommendation list vs. pool."** Both exist in the ovr.news DB — candidate pool = all NexusMind-scored articles (`articles` / `article_filter_scores`); selection = published + placed lens (`editorial_decisions.lens`).

| Metric | Democratic model(s) | Required per-article signal | In ovr.news DB? | Verdict (under selection-vs-pool reframe) |
| --- | --- | --- | --- | --- |
| **Calibration** — topic/genre/complexity match | Liberal, Participatory | topic/category (+ complexity + user history) | ✅ 5-lens + `filter`/`scorer` + `sources.category` as category proxy; user-history dim dropped by the reframe | **Computable now** on a dated snapshot |
| **Activation** — emotional intensity | Participatory, Deliberative, Critical | per-article sentiment (valence/arousal) | ⚠️ not stored, but `articles.content` present → derivable with a sentiment pass | **Computable with light instrumentation** — pointed, given the constructive-framing thesis |
| **Fragmentation** — cross-user story-chain overlap | Participatory, Deliberative, Critical | recommendation lists across *many users* | ❌ single unpersonalised feed | **N/A structurally** — reconceive as pool→selection narrowing, or drop |
| **Representation** — opinion/stance balance | Participatory, Deliberative, Critical | stance/viewpoint labels + opinion-holder identity | ❌ no stance detection anywhere (verified) | **Not computable** — needs a new opinion-extraction pipeline (heavy) |
| **Alternative Voices** — minority-actor presence | Critical, Participatory | NER + protected-group classification of mentioned actors | ❌ `entities` table exists in schema but **zero inserts — unpopulated** (verified); no group classifier | **Not computable** — needs NER population + ethically-loaded group labels (heaviest) |

Verification done in code (2026-07-06), not just from the schema: grep confirmed no `sentiment`/`stance`/`polarity`/`viewpoint`, no personalisation/`user_id`, and no writes to `entities`/`claims`.

## Decision this read forces — RESOLVED

**Score computable on a snapshot? → partial YES.** One metric family (**Calibration**, reframed as selection-vs-pool category/lens divergence) is computable *today* from existing data on one dated daily snapshot. The paper can therefore carry a **real, scoped evaluation** with an honest gap table for the other four — a stronger and more defensible design-science claim than pretending to run the full RADio suite.

**Cluster load-bearing or decorative? → load-bearing.** Vrijenhoek yields (a) one computable metric, (b) precise vocabulary for *which* democratic-diversity dimensions ovr.news's data can and can't speak to, and (c) the structural insight that an **unpersonalised editorial feed re-poses the personalisation-centric diversity literature as selection-vs-pool** — itself a section-worthy contribution.

→ Update **S2-2** (computable-metric claim), promote the take into the claim registry when prose starts.

## Caveats (tier discipline)
- Peer-reviewed conference paper → tier A source. Strong.
- **BUT** the per-metric input list above was extracted via a summariser model reading the paper, not a maintainer read of the PDF. Good enough for the go/no-go. **Before any confident prose, confirm the exact metric formulas + input requirements against the PDF** (`anti-hallucination.md` discipline). Flag as EMERGING until then.

## Relevance to the Constructive Lenses paper
The evaluation framework, and the difference between a think-piece and a design-science contribution. The reframe (selection-vs-pool, not user-vs-pool) plus the one-computable-metric + honest-gap-table is the spine of the evaluation section.
