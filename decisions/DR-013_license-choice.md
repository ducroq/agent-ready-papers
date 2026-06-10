# DR-013: License Choice — CC BY 4.0

---
status: Accepted
date: 2026-06-08
---

## Context

External feedback (June 2026, three independent reviews) flagged the absence of a LICENSE file as the highest-priority adoption gap. Without a declared licence, the repo is legally unusable for adopters even though the content is intended for public reuse.

The repo's content is a mix:

- **Prose-heavy** — `README.md`, `docs/framework-summary.md`, decision records.
- **Markdown templates** — `templates/CLAUDE.md`, `claim-registry.md`, `vv-framework.md`, `writing-guide.md`, `review-prompt.md`, `anti-hallucination.md`, `equation-checker.md`, `glossary.md`, `decision-record.md`, `key-quotes.md`.
- **Active papers** — `papers/perspective/manuscript.tex` and supporting `.tex` / `.bib` files.
- **Short bash and tool snippets** embedded in README and CLAUDE.md.

A future `tools/` directory (per issue #17) may add Python scripts. That is anticipated but not yet present.

The licence needs to:

1. Permit reuse (the repo's whole reason to be public).
2. Require attribution (the framework's empirical claims trace back to specific paper-project failures — attribution preserves the citation chain).
3. Fit prose-heavy content idiomatically (academic methodology and educational resources have an established licensing lingua franca).
4. Not preclude commercial use (consultants, institutions, and edtech vendors are plausible adopters; the framework's value is undermined if commercial use is gated).
5. Be widely recognised by GitHub's licence detector and by adopters' compliance teams.

## Options Considered

### Option A: CC BY 4.0 (Creative Commons Attribution 4.0 International)
- (+) Lingua franca for academic methodology, educational resources, and prose-heavy public goods.
- (+) Attribution requirement aligns with academic citation norms.
- (+) Permits commercial use (criterion 4).
- (+) Recognised by GitHub's licence detector.
- (-) Designed for prose / creative work; less idiomatic for software (small bash snippets, future Python scripts).
- (-) Has a "share-alike" sibling (CC BY-SA) which some adopters prefer for derivative work; choosing BY over BY-SA is a deliberate trade.

### Option B: MIT
- (+) Maximally permissive, well-understood.
- (+) Idiomatic for code (covers any future `tools/` scripts naturally).
- (-) Designed for software; less idiomatic for prose, methodology.
- (-) Less recognised in academic-methodology contexts.

### Option C: Apache 2.0
- (+) Permissive plus explicit patent grant (useful for institutional adoption).
- (+) Well-understood, GitHub-detected.
- (-) Heavier text than MIT or CC BY 4.0.
- (-) Patent grant is unnecessary for a methodology repo (no patentable subject matter).

### Option D: Dual licence — CC BY 4.0 (prose) + MIT (templates and tools)
- (+) Most accurate to the content's actual nature.
- (+) Future-proofs against the `tools/` directory.
- (-) Requires a CONTRIBUTING note explaining the split per file or directory.
- (-) Adds compliance overhead for adopters (which licence applies to which file?).
- (-) Adds maintenance overhead (any new file needs a licence assignment).

### Option E: No licence (status quo)
- (+) No decision to revisit.
- (-) Repo legally unusable. Adopters in well-governed organisations cannot consume it.
- (-) Contradicts the repo's stated purpose; public methodology goods need public licences.

## Decision

**Option A: CC BY 4.0.**

The repo is overwhelmingly prose: methodology, templates as markdown patterns, DRs, manuscripts. The bash snippets are short enough to fall under fair use / quotation in any normal adoption context. The future `tools/` directory is anticipated but its volume is uncertain — if it grows substantially, a dual-licence transition (Option D) is straightforward and revisitable per the trigger conditions below.

Attribution serves both an academic norm (the framework's claims are evidence-traced) and a practical purpose (adopters who use the framework should be able to cite it; citations strengthen the framework's evidence base over time).

## Consequences

- `LICENSE` file added at repo root with the CC BY 4.0 deed, URL reference to the canonical legal code, and a citation block for adopter convenience. Closes issue #20.
- `CONTRIBUTING.md` (separate issue #22) should reference this DR and note that contributions are accepted under CC BY 4.0.
- README's "Templates" section gains implicit permission to be quoted and adapted with attribution.
- Active paper artefacts (`papers/perspective/manuscript.tex` and `references.bib`) are covered, but a published paper version eventually transfers some rights to the publisher per journal terms — this is the author's standard publication transfer, not a licence conflict. Pre-publication versions in the repo remain CC BY 4.0.
- Adopters who use the framework for commercial purposes (consulting, training, institutional V&V) are permitted without notification, subject to attribution.

## Revisit If

- A `tools/` directory (per issue #17) grows substantially — re-evaluate whether dual-licence (Option D) clarifies adopter compliance.
- An adopter requests an explicit patent grant for institutional use — re-evaluate Apache 2.0 or a dual licence.
- A specific academic or grant context requires CC BY-SA or CC BY-NC — assess the trade against the broader commercial-permissive intent.
- Contribution volume from outside the maintainer grows such that the attribution chain becomes ambiguous — formalise via a contributor agreement or DCO sign-off requirement.

## Evidence Base

- External feedback flagging the gap: ducroq/agent-ready-papers#20, filed with citation to the convergent review feedback.
- Convention check: methodology and educational-resource repos in adjacent spaces (e.g., the Carpentries, OpenStax, various academic methodology repos) standardise on CC BY 4.0.
- Companion repo `agent-ready-projects` is code; its licensing question is separate and not bound by this DR.
