# Vrijenhoek et al. 2021 — Recommenders with a Mission (L50)

**Reading status:** TO READ — **highest expected payoff** in the cluster. This is the one that could promote the paper from perspective → design-science-with-evaluation.

## Bibliographic Info
- **Authors:** Sanne Vrijenhoek, Mesut Kaya, Nadia Metoui, Judith Möller, Daan Odijk, Natali Helberger *(verify author list + order)*
- **Year:** 2021
- **Title:** Recommenders with a Mission: Assessing Diversity in News Recommendations
- **Venue:** CHIIR 2021 (Conf. on Human Information Interaction and Retrieval)
- **DOI/URL:** TODO verify (ACM Digital Library)

## What to extract (→ claim map)
- The **normative diversity metrics** themselves (the RADio family / the five democratic models: liberal, participatory, deliberative, etc.) → **S2-2** (P1).
- **Required inputs** for each metric — exactly which per-article signals the metric needs (stance? viewpoint labels? category? source?). This decides hypothesis-log bet **[2026-06-24] "diversity score computable on an ovr.news snapshot"**: check each required input against the ovr.news DB schema.
- Whether "diversity" as they define it maps onto ovr.news's **five-lens distribution** or needs something ovr.news doesn't capture.

## Decision this read forces
- **If** the metric's inputs are all present in ovr.news's data → prototype the score on one dated daily snapshot → paper becomes design-science with a real evaluation.
- **If not** → record the instrumentation gap; paper stays perspective/case scope. (Backlog parking-lot item.)

## Caveats (tier discipline)
- Peer-reviewed conference paper → tier A. Strong source.

## Relevance to the Constructive Lenses paper
The evaluation framework. Possibly the difference between a think-piece and a contribution. Read first.
