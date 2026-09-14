# Zhou & Yu 2026 — Auditable AI-Assisted Research Writing (L61)

**Reading status:** READ (abstract + listing, 2026-09-14). Full text not read. **Closest prior art found — read in full before Paper 1 submission.**

## Bibliographic Info
- **Authors:** Yang Zhou, Chengqun Yu
- **Year:** 2026 (submitted 2026-08-11)
- **Title:** Auditable AI-Assisted Research Writing: An Engineering Discipline with Pre-Registered Process Observation
- **Venue:** arXiv preprint (arXiv:2608.10858)
- **DOI:** [10.48550/arXiv.2608.10858](https://doi.org/10.48550/arXiv.2608.10858)
- **Local copy:** `../pdfs/zhou-yu-2026.pdf`

## Summary
Proposes treating AI-assisted research writing as an engineering discipline with an auditable process, rather than detecting machine assistance after the fact. Components: git sealing with explicit anchor lineage, hash-bound provenance tying quantitative statements to sources, **red-line gates that refuse non-compliant artifacts and log every refusal**, cross-model role separation with adversarial review, and programmatic assembly of the manuscript body from registered sources. Uses pre-registered "metric cards" frozen before the observed project is examined; the demonstration case returned a No-Go on its confirmatory test.

## Key Findings
- The framing move is *provenance over detection* — build the audit trail during writing instead of running a detector afterwards
- Red-line gates that **refuse** artifacts and log refusals — a harder enforcement posture than this framework's quality gates, which advise rather than block
- Cross-model role separation with adversarial review — independently arrived at, and the same countermeasure as DR-011's Pass 3
- Programmatic body injection: "no reported number is typed by hand"
- Pre-registration of evaluation criteria before observation, with a published No-Go result

## Relevance to the framework — PRIOR ART, closest match
Architecturally the nearest neighbour found in this scan: registry-backed assembly, staged gates, cross-model review, and a self-applied case study. Several of its moves are sharper than the framework's current equivalents and are worth considering on their merits:
- **Gates that refuse and log refusals** vs. this repo's advisory gates (`templates/vv-framework.md` §7)
- **Hash-bound provenance for every number** vs. this repo's CALCULATION type, which verifies a result but does not bind it to a source
- **Pre-registered metric cards** vs. this repo's `memory/hypothesis-log.md` — the same instinct (fix the bet before seeing the outcome), more formally executed

**The distinction that survives:** this work audits *process and provenance* — which tool produced which artifact, and whether a number traces to a source. It does not assess whether an argument's warrant holds, whether a proposition states boundary conditions, or whether confidence language matches evidence strength. It answers *where did this come from*; the framework answers *is the reasoning sound and the confidence calibrated*.

## Caveats (tier discipline)
- Preprint, single case study, self-applied → tier **B/F**. Its evidence posture is the same as this framework's own: a worked example, not a controlled evaluation. Do not cite it as demonstrating that auditable writing works.
- ⚠ The abstract-level reading of scope (provenance only, not argument quality) rests on the abstract and listing. **Confirm against the full text before making the distinction in print** — this is the one prior-art claim where being wrong would be embarrassing.

## Open Questions
- Does its "cross-model role separation" specify *cross-vendor*, or merely different models from one vendor? DR-011 Pass 3 and DR-020 both turn on that distinction, and an independent answer would be worth a lot.
- Are the metric cards published? If so they are a concrete template candidate, closer to operational than `templates/hypothesis-log.md`.
