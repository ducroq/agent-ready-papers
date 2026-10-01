# Adopter feedback: an argument-shaped non-fiction project

**Framework version in use:** v3.0.0
**Written:** 2026-09-14 (generic version 2026-10-01; the project-specific draft stays private)
**Status:** draft for the maintainer. Nothing here is filed as an issue yet.

The adopter is a non-fiction project that makes an argument rather than presenting design fiction. It used the framework while drafting. Four findings came out of it, and one of them may be worth a framework note (§3).

## 1. PROVOCATION scoped to one device, with a tripwire

DR-010 makes PROVOCATION opt-in for speculative-design work, and reads as a project-level choice. This project is not speculative design, but it has one recurring rhetorical device that makes no truth claim. Registering that device as a CLAIM would be the inverse-hallucination failure `templates/claim-registry.md` names. Adopting DR-010 wholesale would import rules written for a fictional artefact the project does not have.

What the project did instead: it adopted PROVOCATION **for that one device only**. A local decision record says an entry qualifies only if it makes no truth claim at all. It adds a tripwire: **if PROVOCATION rows outnumber the project's top-level pieces, the type is being used to dodge verification, and the registry should be audited.**

**Suggestion for DR-010 / `claim-registry.md`:** allow a scoped opt-in at device or section level, which may be the more common case. Name the escape-hatch failure (PROVOCATION used for a claim that proved hard to source) in the template either way.

## 2. A deliberative gate became a mechanical one

Gate 2.7 asks whether a contested real-world case is handled symmetrically. This project's constraint has the opposite shape: avoid a whole class of named entity. So the gate became a grep for that class, then a triage of each hit. It was cheap, and it ran clean on two drafts. The general point: when a project's constraint is an absence, a deliberative gate can turn into a search.

## 3. Registering claims while drafting caught a contradiction that reading could not

One passage made a methodological point. A later passage in the same piece undercut it by leaning on an idea closely related to evidence that the project's own registry already recorded as weak.

Re-reading did not surface this. Each passage is defensible on its own, and nothing at sentence level signals a problem. **The contradiction is relational:** it lives between two claims that never share a page. Reading is sequential, while a registry is a flat list that puts the two claims next to each other.

**Suggestion:** `templates/vv-framework.md` §4.6 covers scope drift (declared vs delivered). This is a sibling class, **internal evidential contradiction**: a manuscript claim that contradicts the recorded status of another claim in the same registry. §4.3 asks for no contradictions between sections, but that is a reading check, and reading is what missed this. No gate compares manuscript prose against the recorded status of other registry entries. The cheap detection is temporal (register while drafting), not algorithmic.

## 4. Two smaller observations

- **Dead-reference false positives on nested projects.** While the adopter was on v3.0.0 of this framework, the then-current `/curate` dead-reference step flagged 2 dead and 17 unresolvable references in the adopter repo. Both dead flags and 12 of the 17 were false. The cause was a project directory one level inside a repo root, which is the layout the framework prescribes, where references are relative to the document. That step left `/curate` in companion v1.45.0, and dead references are now `audit-context` Step 4's job. Whether that step has the same false positives has not been checked.
- **A voice-driven project wants a rule-versus-prose ledger.** Gate 2.8 checks voice consistency, but the more useful question was the reverse: do the rules make the prose better? In one measured instance a rule forced a rewrite, and the rewrite was better. The project logged this as a hypothesis with a stopping condition: three "worse" verdicts in a row mean the rule set is over-fitted and gets cut. That may belong in `templates/hypothesis-log.md` as an example: an over-fitted rule set is a plausible framework-wide failure mode, and nothing in `templates/` watches for it.

## 5. What to do with this

Nothing yet. If any of §1–§4 deserves an issue, the issue should link to this file.
