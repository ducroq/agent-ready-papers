# Claim Registry

<!-- Seeded 2026-06-24 from the ovr.news [2026-05-27] lineage entry + PROPOSITION.md.
     These are STARTING claims for Phase 0 framing — every row is [ ] (unverified)
     and most sources are unread. Do not promote confidence until the source is
     read (literature) or the measurement is documented (own-data). -->

**Paper:** Constructive Lenses: An Open, Diversity-Aware AI Pipeline for Public-Interest News Selection (WORKING)
**Last Updated:** 2026-06-24 (scaffolded — 0% verified by design)
**Thesis (WORKING):** Constructive news selection can be operationalised as a transparent, diversity-aware, distillation-based AI pipeline; ovr.news is an existence proof, and evaluating it against a normative diversity framework shows what such a system can and cannot yet do.

---

## Coverage Summary

**Coverage by Priority**

| Priority | Total | Verified | Needs Evidence | Coverage |
|----------|-------|----------|----------------|----------|
| P0 | 4 | 0 | 4 | 0% |
| P1 | 3 | 0 | 3 | 0% |
| P2 | 0 | 0 | 0 | 0% |
| **Total** | **7** | **0** | **7** | **0%** |

**Coverage by Type**

| Type | Total | Verified | Coverage |
|------|-------|----------|----------|
| CLAIM | 4 | 0 | 0% |
| ARGUMENT | 1 | 0 | 0% |
| PROPOSITION | 2 | 0 | 0% |
| **Total** | **7** | **0** | **0%** |

**Targets:** ≥85% overall, 100% P0, 90% P1, 70% P2. Every ARGUMENT and PROPOSITION `[x]` before Gate 2.

---

## Priority Guide

### P0 (Critical) — paper fails without these

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S1-1 | The constructive-journalism field has producers + methodology authorities but no open infrastructure between them | The "gap" the paper fills disappears |
| S2-1 | Helberger 2024 identifies a provider/deployer asymmetry under the AI Act that disincentivises in-house AI in small media | Loses the governance frame that makes ovr.news's open-build move significant |
| S3-1 | ovr.news scores news in 25+ languages via five distilled lens classifiers and surfaces a daily constructive selection with per-article rationale | The existence proof — no artefact, no paper |
| SN-1 | (PROPOSITION) Constructive selection is implementable as an open, diversity-aware, distillation-based pipeline | The contribution itself |

### P1 (Important) — target 90%

| ID | Claim | Risk if Wrong |
|----|-------|---------------|
| S2-2 | Vrijenhoek 2021 formalises normative diversity metrics for news recommenders | Loses the evaluation framework |
| S3-2 | ovr.news's constructive selection lives in the lens, not the source list (same scoring across constructive + general feeds) | Weakens the "methodology, not curation" distinction |
| SN-2 | (ARGUMENT/boundary) A feed of short summaries changes valence (doom→constructive) but not the additive *form* Han critiques | Paper looks naive about its own deepest critique |

---

## Registry by Section

> Section structure is provisional — Phase 0 outline pins it. Sections below are placeholders that group the seed claims by role (problem / landscape / artefact / contribution).

### Section 1: The infrastructure gap

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S1-1 | The constructive-journalism field has content producers and methodology authorities (SJN, Constructive Institute, Bonn Institute) but no open infrastructure between them; the Constructive Institute's classifier is partner-only | P0 | EMERGING | [OWN WORK — ovr.news LANDSCAPE.md]; [Karadimitriou 2026] | E; [TBD] | [ ] |

### Section 2: Governance + diversity frame

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S2-1 | The AI Act creates a provider/deployer asymmetry (Art. 52 authenticity duties) that disincentivises in-house AI adoption by smaller media orgs | P0 | EMERGING | [Helberger 2024] | [TBD] | [ ] |
| S2-2 | Normative diversity metrics for news recommenders can be formalised and computed against a recommender's output distribution | P1 | EMERGING | [Vrijenhoek 2021] | [TBD] | [ ] |

### Section 3: The artefact (ovr.news)

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S3-1 | ovr.news ingests RSS in 25+ languages, scores every article with five distilled lens classifiers, and surfaces ~200 articles/day from 175–225 distinct sources with per-article rationale and attribution | P0 | EMERGING | [OWN DATA — ovr.news PROPOSITION.md + live DB] | E | [ ] |
| S3-2 | The constructive selection lives in the lens, not the source list — the same scoring runs across dedicated constructive feeds and general news | P1 | EMERGING | [OWN WORK — ovr.news ADR-038] | E | [ ] |

<!-- S3-1 is an OWN-DATA claim (DR-008): verify by documenting the query that produces
     the 200/day + 175–225 source numbers against the live DB on a stated date, not by
     source count. Today these are PROPOSITION.md prose, not yet a reproduced measurement. -->

### Section N: Contribution + boundary

**ARGUMENTs** (Toulmin):

| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Source | Source Tier | Status |
|----|-----------|----------|------------|---------|---------|----------|--------|-------------|--------|
| SN-2 | Constructive selection changes the *valence* of the feed but not the additive *form* Han critiques; longitudinal arcs ("what happened next") are the structural answer, not more snapshots | P1 | SPECULATIVE | S3-1; S1-1 | A constructive feed of short, decay-ranked summaries is still "information" in Han's sense unless it binds past/present/future | Han may overstate; a curated daily reading may already provide orientation | [Han 2024] | [TBD] | [ ] |

**PROPOSITIONs** (Whetten):

| ID | Statement | Priority | Confidence | Constructs | Relationship | Premises | Reasoning | Boundary conditions | Alternatives engaged | Source | Source Tier | Status |
|----|-----------|----------|------------|------------|--------------|----------|-----------|---------------------|----------------------|--------|-------------|--------|
| SN-1 | Editorially-meaningful constructive news selection can be implemented as an open, diversity-aware, distillation-based AI pipeline runnable on consumer hardware | P0 | EMERGING | constructive lens; distilled classifier; normative diversity; open infrastructure | Distillation + lens taxonomy + transparent rationale together yield a reproducible selection layer | S1-1; S3-1; S3-2 | ovr.news runs this in production; llm-distillery is public and forkable | Holds for small newsrooms/researchers with light Python+GPU capacity; does NOT claim venture-scale adoption or that it replaces human editorial judgment | Closed per-org pipelines (status quo); partner-only classifiers (Constructive Institute) | [OWN WORK] | E | [ ] |

---

## Own Work / Own Data

| Source | Claims | What to Check | Status |
|--------|--------|---------------|--------|
| ovr.news live DB + PROPOSITION.md | S3-1, S3-2 | Reproduce the 200/day + 175–225 source + 25+ language numbers with a dated query; cite ADR-038 for lens decoupling | [ ] |
| llm-distillery (public, EUPL-1.2) | SN-1 premise | Confirm public + forkable; note the 2/5 public scorer state honestly | [ ] |

## Out of Scope

| ID | Claim | Why Excluded |
|----|-------|-------------|
| — | The augmented-engineering / SE-with-AI proposition | Different paper, different venue (`ducroq/augmented-engineering`); do not fold in |

---

*Registry created: 2026-06-24*
