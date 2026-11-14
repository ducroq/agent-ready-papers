# DR-033: The P0 Floor Depends on What an Entry Does: Factual Claims Need Supported, a Proposal Needs a Test

---
status: Proposed
date: 2026-11-14
---

## Context

DR-002 sets one floor for every P0 entry: "all SUPPORTED or ESTABLISHED (no EMERGING/SPECULATIVE)". DR-027 extended it to contributions. Paper 1 states the rule ("every P0 entry, the contribution included, should reach the Supported tier") and applies it to itself.

After the 2026-11-14 round, 4 of Paper 1's 6 P0 entries reach Supported (`make coverage`). The two below the floor are different kinds of entry:

- **S2-2** (no consensus checklist was found) is a factual claim. Its gap is fixable in principle by a second screener.
- **C1** (the contribution) is a proposal: a register "could make" reasoning traceable, and "trials should test" whether it does. It cannot reach Supported until trials have run, whatever the paper does, because a proposal's benefit is the thing the trials would measure. Under DR-002 any paper whose contribution is a method still to be tested fails its own floor by construction.

On 2026-11-14 two independent model reviewers (Codex, Mistral Vibe; outputs in `lab/reviews/2026-11-14-about/`) were asked about this. Both rejected moving entries from P0 to P1 to pass the floor. Both accepted a rule change only if it is general, stated in advance, and not an exemption for one paper. Codex: "use role-specific requirements … do not upgrade C1 merely by exempting it". Vibe: "the floor is right for assertoric P0 claims … and wrong as stated for the contribution".

## Options Considered

### Option A: Keep DR-002 as it is, and disclose
- (+) No rule change.
- (-) Every method paper fails by construction, so the floor no longer separates a well-argued proposal from a weak one.
- (-) A paper that fails its own stated rule invites "why prescribe a floor your exemplar cannot meet?"

### Option B: Floor by role (recommended)
- P0 **claims** (descriptive or normative statements the paper fails without) must reach SUPPORTED or ESTABLISHED, as now.
- A P0 **contribution that is a proposal to be tested** may sit at EMERGING if all three hold:
  1. its wording stays at that tier ("could", "may"; no claim of benefit);
  2. it names the trials that would test it and what result would refute it;
  3. every P0 claim it rests on meets the floor.
- A contribution that claims a demonstrated benefit is held to the floor like any claim.
- (+) Matches what the floor is for: the paper's essential assertions are adequately supported, and the untested part is labelled as untested.
- (+) Condition 3 keeps the rule from becoming an exemption: the proposal still fails while its premises fail. For Paper 1 that means C1 passes only once S2-2 does.
- (-) It is a rule change after a paper failed the old rule. The record must show the reason is general (every method paper), not this paper.

### Option C: Re-prioritise S2-2 or C1 to P1
- (-) Rejected by both reviewers as gaming: these entries are central, and demoting them because their evidence is weak empties the priority of meaning.

## Decision

Option B, if accepted. DR-002's P0 rule and DR-027's extension to contributions are amended as above; source counting and the qualifier mapping are unchanged.

## Consequences

- `tools/coverage.py`: the P0 floor treats a contribution that meets conditions 1–3 as passing. Conditions 1 and 2 need a field or marker in the contribution row (for example, a *Test* column naming the trials and the refuting result); condition 3 can be computed from the premise graph.
- `tests/test_paper1_v5.py`: the p0_floor expectation changes.
- Paper 1, the floor sentence becomes: "Priority sets how much checking a claim deserves, and every P0 claim should reach the Supported tier; a contribution that proposes something to test should instead name the trials that would test it, and rest only on claims that reach the floor." Under this rule Paper 1 still falls short until S2-2 has a second screener. The paper says so.
- `templates/claim-registry.md` and `docs/framework-summary.md` follow.

## Open Questions

- Does condition 2 need a minimum standard for the named trials (a comparison condition, outcomes, who runs them)? Codex lists what a discriminating trial would measure: correct detections, missed weaknesses, false alarms, reader reconstruction, author burden, agreement between raters.
- Does this extend to P0 normative claims other than the contribution?
