# DR-017: agent-ready-papers Is Custodian of the Typed-Verification Layer; Sibling Repos Vendor It with Provenance

---
status: Accepted
date: 2026-06-24
---

## Context

The `agent-ready-*` family now has four repos:

- **agent-ready-projects** — the family root for *code* projects; Layer-1 session-continuity scaffolding (DRs, memory, hypothesis-log, gotcha-log, coverage tooling) plus the *generic* V&V primitives (`docs/vv/anti-hallucination.md`, `claim_registry.md`, `writing-guide.md`).
- **agent-ready-papers** (this repo) — AI-augmented authoring; first operationalized the *typed* verification model in DR-004.
- **agent-ready-assessment** — grading of HAN student reports.
- **agent-ready-research** — AI-assisted research methods.

A 2026-06-24 cross-repo diff (this session) found that the **typed-verification core** — CLAIM / ARGUMENT / PROPOSITION, Toulmin (for ARGUMENT), Whetten (for PROPOSITION), confidence tiers + tier→language mapping, reproduction-mode verification, and the persistent claim-registry artifact — does not live in one place. `agent-ready-assessment`'s `Reproduction_Verification_Prompt.md` (892 lines) independently re-implements essentially the whole model and *extends* it; `agent-ready-research` imports a subset by declaration. The user asked whether the repos should consolidate, and which elements.

### What triggered this

The diff was prompted by the observation that this repo is built to *generate* papers yet also carries *review* machinery, and assessment is built to *review* yet carries the same conceptual core. The natural question — "consolidate?" — forced a prior question: **where is the root?** Two distinct genealogies turned out to be in play.

### The distinction this DR turns on

"Is agent-ready-papers the root?" splits into two claims with different answers:

1. **Family/scaffolding root** = `agent-ready-projects`. All three siblings declare `agent-ready-projects: vX.Y.Z` as upstream (papers tracks v1.10.3; assessment v1.2.0; research v1.10.3). Projects owns the generic substrate. Papers is **not** this root.
2. **Typed-verification-layer custodian** = `agent-ready-papers` — see the ownership-vs-custody clarification below.

### Custody, not authorship — and not implementation-maturity

A review pass (see *Evidence Base*) flagged an implicit warrant in the first draft: it inferred "papers owns the typed layer" from "the verified sources live in papers," without arguing why source-custody beats the competing criterion that *assessment has the most mature implementation* (892 lines vs this repo's leaner templates). Two corrections close the gap:

- **Not authorship.** DR-004 is explicit that the typed model was *imported from published argumentation theory* (Toulmin, Walton, Hevner, Whetten). Papers did not invent CLAIM/ARGUMENT/PROPOSITION; it **operationalized** that scholarship and **holds the verified primary-source bibliography**. The claim here is custodianship of the operationalization + sources, not origination.
- **Custody beats maturity as the ownership criterion** *because the verified primary sources are the part that must not drift; implementations may.* A more elaborate implementation is a reason to backport *from* it, not a reason to relocate the canonical definition *to* it.

So the precise claim is: **papers is the custodian of the operationalized typed layer and its verified argumentation-theory sources.** The bare concepts are more widely shared (next section).

### The decisive evidence: the Whetten primitive — and its limit

Whetten (the PROPOSITION schema: constructs, relationships, **boundary conditions**) is the single clearest custody signal, because the *named schema + its verified source* land in exactly one repo:

| Repo | Where Whetten appears | Status |
|---|---|---|
| **agent-ready-papers** | `literature/sources/whetten-1989.md` (verified primary source), `DR-004`, `templates/`, `docs/framework-summary.md`, the manuscript, `memory/` | **Canonical + source-backed** |
| agent-ready-projects | *only* `docs/archive/LANDSCAPE.md` | **Whetten *name* archived** (see limit below) |
| agent-ready-assessment | `Reproduction_Verification_Prompt.md`, `issues/005-typed-claim-registry.md`, `issues/003`, `memory/` | **Forked** — tracked as adoption debt |
| agent-ready-research | — | **Absent** |

Both reviewers who checked this table confirmed every cell reproduces. **But the narrative needs one correction they also surfaced:** it is the *Whetten name and verified source* that are papers-exclusive — **not the typed model in general.** The broader CLAIM/ARGUMENT/PROPOSITION model and Toulmin breakdowns are *live, in active use* in projects (`docs/verifying-what-we-write.md`, `docs/vv/claims/claim_registry.md`), not merely archived. Only the Whetten *citation* retreated to `LANDSCAPE.md` there.

This sharpens rather than weakens the layering:
- The **generic typed concepts** (the *idea* of typing statements, Toulmin for ARGUMENTs, tiers) are co-used and legitimately live one level up, in **projects** (the generic substrate).
- What **papers** uniquely holds is the **full operationalization** — per-type checklists, the Whetten PROPOSITION schema with boundary-condition discipline, and the *verified argumentation-theory bibliography* (`whetten-1989.md`, `toulmin-1958.md`). Toulmin's *concept* is shared with projects; its *verified source* is papers-exclusive. Whetten is the cleaner signal because both name and source are papers-exclusive.

### Drift is bidirectional

Assessment is not a stale copy — it has invented refinements papers lacks, and tracks each as an issue (all four issue files confirmed to exist by the evidence audit):

- **tier-monotonicity** (one principle unifying citation drift, overclaiming, Step Z) — `issues/010-tier-monotonicity.md`
- **STEP Z** (inverse hallucination: claim-shaped language over weak evidence) — generalized beyond papers' current PROVOCATION-only scoping
- **SCOPE DRIFT** (planned-but-not-delivered as a distinct finding type) — `issues/002`
- **failure-pattern table** (plausible fabrication, index drift, number invention, …) — `issues/006`
- **WebFetch fallback ladder** + cross-vendor outside-ness escalation — `issues/012`

Papers, conversely, has the clean equation-checker error codes (FORMULA/NUMERICAL/DIMENSION/…) and the multi-pass review structure (DR-011, still Proposed) that assessment's single prompt lacks.

That assessment carries `memory/project_arpapers_boundaries.md` and `memory/project_claim_registry.md` shows the boundary question has already been circling on the maintainer side; this DR records it.

### The asymmetry that blocks a full merge

papers = **self-verification** (author red-teams own work before publishing). assessment = **external evaluation** (grader judges another's work, with a power differential, accreditation-locked rubrics, mandatory anonymization, and a no-AI-training institutional policy; CC-BY-public vs institutional). A merge would conflate two genuinely different acts. The confidentiality objection is real but, on its own, *softer* than the first draft implied — papers already co-locates public and private material behind `.gitignore` (`audits/`, `memory/`), so a merged repo with a gitignored institutional subtree is technically possible. The decisive reason against a merge is therefore the **act-asymmetry** (self- vs external-evaluation, with its power/accreditation/licensing differences), not the mere existence of confidential files; the confidentiality point is downgraded to "added operational risk we chose not to take."

## Options Considered

### Option A: Merge agent-ready-papers and agent-ready-assessment into one repo
- (+) One home for the shared core; no duplication.
- (-) Collapses the self-verification / external-evaluation act-asymmetry.
- (-) Operational risk: requires a gitignored institutional subtree to keep accreditation/anonymized/no-AI-training material out of a public CC-BY repo — doable (papers already does this for `audits/`) but a standing hazard we prefer not to take on.

### Option B: Status quo — let each repo keep its own fork of the core
- (+) Zero coordination cost.
- (+) Divergence under different load is how assessment's best inventions (SCOPE DRIFT, the general STEP Z catalogue) arose in the first place — a single owner with veto might have suppressed them.
- (-) The typed model now exists in multiple dialects that drift independently; Whetten/tiers/registry must be fixed in N places.
- (-) Assessment's inventions never flow back to the framework whose thesis they would sharpen.

### Option C (Proposed): Keep repos separate; papers is custodian of the typed layer; siblings vendor it with provenance; backport the sibling inventions (adapted)
- (+) Preserves the act-asymmetry and assessment's confidentiality boundary.
- (+) Gives the operationalized typed layer one custodian (the repo with the verified sources and DR-004), while leaving the generic concepts where they already live (projects).
- (+) Lets assessment's inventions flow into the framework — *adapted* to the authoring context, not lifted raw.
- (-) Requires a vendor-with-provenance discipline across repos and (maintainer-driven) reciprocal notes in assessment/research.
- (-) Backport is a *reconciliation* job (merge two dialects), not a clean lift.

### Option D: Extract a new shared `agent-ready-verification` module both consume
- (+) The cleanest DRY: one module, no custodian/consumer asymmetry.
- (-) Adds a fourth versioned artifact and a dependency edge to a family that has never used submodules.
- (-) Premature at N=2 consumers; the cost only pays off with more. Folded into *Revisit If* as the escalation trigger if the consumer count grows or the vendor discipline proves leaky.

## Decision

**Option C** (Accepted 2026-06-24). Three-layer custody:

1. **`agent-ready-projects`** owns the **generic V&V substrate** — anti-hallucination shape, claim-registry shape, confidence tiers as a generic device, the *generic* typed concepts (typing statements, Toulmin for ARGUMENTs), session scaffolding. (Unchanged; stated for the record.)
2. **`agent-ready-papers`** is **custodian of the operationalized typed layer** — per-type verification checklists, the **Whetten** PROPOSITION schema with boundary-condition discipline, the typed claim-registry, and the **verified argumentation-theory sources** (`whetten-1989.md`, `toulmin-1958.md`). Normative statement: `docs/framework-summary.md` + `templates/` + DR-004.
   - *Not* claimed as papers-owned: **reproduction-mode discipline** (originated in assessment's `Reproduction_Verification_Prompt.md`; a shared primitive, credited to assessment) and **multi-pass review (DR-011)** (a Proposed pattern *hosted* here, not a settled owned asset). These are offered/shared, not asserted as custody.
3. **`agent-ready-assessment`** and **`agent-ready-research`** **vendor the typed layer with a provenance note** (`imported-from: agent-ready-papers vX.Y.Z`), not as independent forks.

The repos stay separate. Do **not** hoist the operationalized typed layer into projects.

### Reference mechanism: vendor-with-provenance (decided, not open)

A feasibility review confirmed **zero `.gitmodules` anywhere in the family**; the established pattern is copy-with-version-header (research's `heritage:` block already pins `agent-ready-papers v1.7.0` and imports primitives on demand). Therefore:

- **Default: vendor with an `imported-from: agent-ready-papers vX.Y.Z` note**, drift surfaced at session start via the existing companion-drift Before-You-Start row.
- **Rejected: git submodule** — it would be the only submodule in four repos, would pin a public repo into an institutional one (breaking assessment's confidentiality posture), and would break the cross-tool portability the framework advertises (`docs/non-claude-setup.md`: Cursor/Copilot/web-chat adopters can't resolve submodules).

### Backport — full, but adapted to the authoring context

A feasibility review found **most of the backport is already present in the templates**: `templates/anti-hallucination.md` already carries Step Z, the WebFetch fallback ladder, and the failure-pattern table; `templates/writing-guide.md` already names tier-monotonicity. So the backport is mostly *generalize / extend / propagate*, not insert-from-scratch.

| Invention | Current state in papers | Backport action (adapted) | Target |
|---|---|---|---|
| **tier-monotonicity** | Named in `templates/writing-guide.md` | Add a one-line reference-card mention; **propagate** the paragraph to the Paper 1 copy (`papers/perspective/writing-guide.md`, currently missing it) | `docs/framework-summary.md`, `papers/perspective/writing-guide.md` |
| **STEP Z** | Present but **PROVOCATION-gated** in `anti-hallucination.md` | **Generalize** the existing section from PROVOCATION-only to the broad *tier-monotonicity-violation* form (per the decision below); keep one definition, cross-referenced from `vv-framework.md` | `templates/anti-hallucination.md`, `templates/vv-framework.md` |
| **SCOPE DRIFT** | Absent | **Adapt to an authoring analogue**: *declared scope (abstract / intro promises / stated contributions) vs. delivered sections* — drop the Plan-of-Approach/MoSCoW machinery, which has no authoring counterpart | `templates/vv-framework.md` (new finding type, authoring form) |
| **failure-pattern table** | Present | **Merge** assessment's extra rows (index drift, number-invention-uncited, single-run-as-measurement, library-version drift, missing model card) | `templates/anti-hallucination.md` |
| **WebFetch fallback ladder** | Present (full) | No-op — confirm parity, no edit | — |

**The one reconciliation to resolve first (riskiest edit):** papers' Step Z is currently scoped to PROVOCATION/speculative-design only; assessment's is general. Per the adopted decision (*full backport, adapted*), **generalize** papers' Step Z to the broad tier-monotonicity-violation form so there is a single definition — *not* two. **Reconciled with DR-014 (2026-06-24).** DR-014 (Proposed) had proposed moving Step Z *out* of core into `templates/extensions/anti-hallucination-step-z.md`, on the premise that Step Z is PROVOCATION-coupled. DR-017's assessment evidence falsifies that premise (assessment runs Step Z on ordinary, PROVOCATION-free reports), so DR-014 was amended: **Step Z stays in core, generalized** (the PROVOCATION-only gate is removed); the extension file is **withdrawn**; PROVOCATION's own extraction proceeds unchanged. The Step Z edit is therefore unblocked. (See DR-014 *Reconciliation with DR-017*.)

The reverse flow (equation-checker codes, DR-011 multi-pass) is offered to assessment via the vendor relationship.

### Paper 1 impact check (Hard Constraint: template changes may affect active papers)

A feasibility review quantified the ripple as **effectively nil**: Paper 1's registry (19 entries, 100% verified) has **no PROVOCATION entries and no Plan-of-Approach**, so neither the generalized Step Z nor SCOPE DRIFT forces any reclassification. Mandatory edits: **zero**. Optional: (a) propagate the tier-monotonicity paragraph into `papers/perspective/writing-guide.md` for consistency; (b) a one-time tier re-scan of the 19 entries (the paper already passed peer review at 3.95/5.0, so the violation surface is low).

### Licensing (DR-013)

The vendor direction (papers → siblings) is CC-BY-clean with attribution. The **backport direction** (siblings → papers) relicenses assessment's inventions CC-BY on import; this is clean because the **same maintainer holds the rights across all four repos**. Recorded here because the DR itself raises the public/institutional asymmetry.

### Reciprocal actions (maintainer-driven, outside this repo — intentions, not bindings)

A DR in this repo can record an intention but cannot bind another repo's contents:

- `agent-ready-assessment`: an answering note recording that its typed core is vendored from agent-ready-papers vX.Y.Z; relabel `issues/005`/`issues/010` as adoption-from-upstream once the backport lands.
- `agent-ready-research`: its `heritage:` block already cites papers v1.7.0 — re-pin to the version this DR's backport ships in.

### What stays unchanged

- The Hard Constraints, unit types, and quality gates of this repo.
- agent-ready-projects' generic substrate and its role as family root.
- Assessment's anonymization / accreditation / no-AI-training constraints (they are why no merge).

## Consequences

If Accepted:
- The operationalized typed layer has one custodian; Whetten/Toulmin sources + per-type checklists are maintained in one place and vendored elsewhere with provenance.
- The framework absorbs the sibling refinements **in adapted form** (tier-monotonicity propagated, Step Z generalized, SCOPE DRIFT recast for authoring). Their *value* remains untested — see Evidence Base; logged as a hypothesis with a revisit trigger rather than asserted.
- CHANGELOG bump: **MINOR** (additive, adapted concepts; the custody statement itself is documentation). If the ownership designation lands alone (backport deferred), that half is PATCH.

If Rejected:
- The position is closed with rationale; the diff + review findings remain in the decision trail so the consolidation question is not re-litigated from scratch.

## Evidence Base

- **2026-06-24 cross-repo diff (this session).** File-level grep for Whetten / Toulmin / PROPOSITION across all four repos; full read of `equation-checker.md` (125 lines) and `Reproduction_Verification_Prompt.md` (892 lines); upstream-version headers; research `heritage:` block. **Not pre-registered** — a structural finding from reading artifacts, not an experiment.
- **2026-06-24 review battery (6 independent agents).** Adversarial skeptic, reproduction-mode evidence auditor, framework-lens self-application, cross-DR consistency, peer-review simulation (own rubric), implementation feasibility. Convergent outcome: the *direction* is sound (no agent rejected it); the evidence narrative and backport scope needed the corrections folded into this revision. The evidence auditor **reproduced all factual claims** (Whetten table, version pins, the 892-line count, issue-file existence, DR-004 as origin). The skeptic + auditor jointly surfaced the projects-co-use correction now in §"The decisive evidence". Peer-review sim: **4.35/5.0, accept with minor revisions**. Framework-lens: **framework-clean**, PROPOSITION 4.5/5 Whetten at a correctly-assigned SUPPORTED tier.
- **Custody half — not contingent.** That the Whetten name + verified sources are papers-exclusive is readable off the repos; needs no replication.
- **Backport *value* — untested.** That the adapted inventions improve the framework *in use* is asserted from design, not measured. Logged to `memory/hypothesis-log.md` with a revisit trigger; tied to DR-016's open question about whether components earn their keep.

## Open Questions Carried Forward

- ~~**DR-014 reconciliation (blocking the Step Z edit).**~~ **Resolved 2026-06-24.** DR-014 amended (*Reconciliation with DR-017*): Step Z decouples from PROVOCATION — it is audience-general, so it **stays in core** (generalized, PROVOCATION-only gate removed) and DR-014's proposed `extensions/anti-hallucination-step-z.md` is withdrawn; PROVOCATION's own extraction proceeds. The Step Z generalization is now unblocked, pending DR Acceptance.
- **Does the adapted SCOPE DRIFT earn its place?** The authoring analogue (declared-scope vs delivered-sections) is weaker than the grading version. If it fires for no real paper, retire it. Test on Paper 1 + the next external audit.
- **Interaction with DR-016 (preventive vs evaluative).** SCOPE DRIFT and the failure-pattern table are *evaluative* findings; DR-016 suspects the evaluative apparatus is under-justified vs a generic prompt. The adaptation keeps them authoring-flavored, but their value is gated on DR-016's pending replication, not assumed here.
- **Reproduction-mode provenance.** This DR credits reproduction-mode to assessment. Whether it should be promoted to a *shared* primitive documented in projects (the generic substrate) is a separate, smaller question.

## Revisit If

- An external adopter (or a third consumer) needs the typed core without papers' paper apparatus → re-evaluate **Option D** (extract a shared module); the vendor-with-provenance discipline is the interim answer, not the permanent one.
- A second sibling independently re-invents a typed-layer refinement → the vendor discipline is leaking; revisit Option D.
- DR-016 replication shows the framework's value is process/coverage only → reconsider how much typed machinery is worth centralizing vs simplifying, and reweigh the evaluative backports.
- assessment's institutional constraints change such that a merge becomes safe → the act-asymmetry argument weakens; revisit Option A.
