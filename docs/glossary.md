# Glossary

> **Status: normative since 2026-10-16 (DR-027 accepted).** DR-004's vocabulary (CLAIM / ARGUMENT / PROPOSITION) is superseded; old registries are still read through v5.x. Reviewed by four models (ChatGPT, DeepSeek, Gemini, Claude Fable; reviews kept in the maintainer's work items, not shipped).

The framework's terms, each taken from its home source. Where the framework adapts a term or maps one source onto another, the entry says **framework mapping**. Quotes from Toulmin, Whetten and the IPCC note were checked verbatim against the full texts with `tools/check_quotes`; page numbers are printed pages, except the IPCC note (PDF pages). NASA quotes come from the handbook's web page and the GRADE wording from the abstract; neither was machine-checked. Sources: [Toulmin 2003](../literature/sources/toulmin-1958.md) (L01), [Whetten 1989](../literature/sources/whetten-1989.md) (L11), [NASA 2016](../literature/sources/nasa-2016-se-handbook.md) (L97), [Mastrandrea et al. 2010](../literature/sources/mastrandrea-2010-ipcc-guidance.md) (L96), [Santesso et al. 2020](../literature/sources/santesso-2020-grade-26.md) (L98, abstract only).

Papers derive their own glossary from this one (`templates/glossary.md`) and add their field's terms.

## The model in brief

1. Every statement the paper puts forward and supports is a **claim**. Declared starting points (step 3) are registered alongside claims but adopted, not argued for; provocations in speculative-design work (DR-010) make no truth claim and keep their own table.
2. Each claim records **what it says**: **descriptive** (how things are) or **normative** (what should be done).
3. Each claim records **what it rests on**, item by item. Each item is one of four: a **source** (what a cited work reports), another **claim** (joined by a warrant), a **declared starting point** (an assumption, definition or value the paper adopts), or the author's **own work** (an observation, experiment or measurement, with its method named, so it can be repeated).
4. The checks follow the items: every source gets a **source check**, every step from other claims (or from several sources combined into a point none makes alone) gets a **warrant check**, every declared starting point is stated explicitly with its contestedness recorded, every own-work item names a method someone else could repeat. Normative claims also need **boundary conditions** and at least one declared **value** among their grounds.
5. Every claim carries a **qualifier** (its hedge), which its **confidence tier** must permit.
6. Each **contribution** is a root claim: P0 by definition, with a confidence tier no higher than its weakest supporting claim. Whetten's elements and questions check it once, as **validation**. The per-claim checks are **verification**.

**Deciding what a claim rests on**, for a sentence like "Prior work shows X [cite]; therefore Y": register X (resting on the source) and Y (resting on X, via a warrant). A claim that synthesises several sources into a point none of them makes rests on those sources *and* an inference: it needs a warrant check. Ask of each claim: would it stand if I removed the citation? the inference? the assumption?

## 1. Arguments (Toulmin)

| Term | Definition | Source | Framework use | Common confusion |
|---|---|---|---|---|
| **claim** | An assertion put forward for acceptance: "the claim which any assertion necessarily involves"; within an argument, "the claim or conclusion whose merits we are seeking to establish (C)". | Toulmin p. 90 | The framework's single unit: every statement the paper puts forward and supports is a claim, including conclusions and recommendations. | DR-004's CLAIM meant only a source-checkable fact. |
| **grounds** | The framework's term for what a claim rests on; Toulmin's **data**: "the facts we appeal to as a foundation for the claim". | Toulmin p. 90 | Recorded item by item: sources, other claims, declared starting points, own work (model step 3). | Toulmin's own word is *data*; he uses *grounds* loosely, for data and backing alike: "the grounds (backing, data, facts, evidence, considerations, features)" (p. 12), and calls the datum "the ground which we produce as support" (p. 90). The framework avoids *data* because in theory papers "logic replaces data as the basis for evaluation" (Whetten p. 491) and authors read *data* as empirical observations. |
| **warrant** | "general, hypothetical statements, which can act as bridges, and authorise the sort of step to which our particular argument commits us"; "data are appealed to explicitly, warrants implicitly". | Toulmin pp. 91–92 | The step from grounds to claim. A warrant check asks whether the step holds for the paper's **audience**. Rule of thumb: grounds answer "what do you have to go on?", the warrant "how do you get from there to the claim?" | Often left unstated, which is why it needs checking. Toulmin likens grounds vs warrant to "questions of fact and questions of law" (p. 92). |
| **backing** | "other assurances, without which the warrants themselves would posses neither authority nor currency". | Toulmin p. 96 | Support for a warrant the audience might not accept; optional where they already accept it. | Toulmin: the backing needed "will change greatly as we move from one field of argument to another" (p. 96). |
| **qualifier** | "qualifiers (Q) indicating the strength conferred by the warrant on this step". | Toulmin p. 94 | The hedge in the sentence ("may", "indicates", "demonstrates"). Its strength must not exceed what the claim's **confidence tier** permits (Step Z). | The qualifier is not a property of a source, and not the tier itself. |
| **rebuttal** | "conditions of rebuttal (R) indicating circumstances in which the general authority of the warrant would have to be set aside". | Toulmin p. 94 | Stated circumstances in which the step from grounds to claim no longer holds. **Framework mapping:** for a normative claim, its boundary conditions play this role. | Not an opponent's counter-argument (see **objection**). |
| **field** | Arguments share a field "when the data and conclusions in each of the two arguments are, respectively, of the same logical type"; "all the canons for the criticism and assessment of arguments ... are in practice field-dependent, while all our terms of assessment are field-invariant in their force". | Toulmin pp. 14, 35 | Why a warrant valid in one discipline may fail in another, and why the tier names can travel while the rules for assigning them may not. | — |

Toulmin presents logic as "generalised jurisprudence" (p. 7). His 2003 preface rejects the label "the Toulmin model": "my concern was with twentieth-century epistemology, not informal logic" (p. vii). The framework uses his layout as a checklist; that use, and DR-002 and the templates that implement it, are the framework's and must be justified on their own merits.

## 2. Contributions (Whetten)

| Term | Definition | Source | Framework use | Common confusion |
|---|---|---|---|---|
| **contribution** | What a paper adds to current thinking, judged by asking "Does the paper make a significant, value-added contribution to current thinking?" | Whetten p. 494 | The root claim of the registry, one per contribution; checked once with Whetten's elements and questions (the **contribution check**). | DR-004 applied Whetten's checklist to single PROPOSITION rows. |
| **What, How, Why** | "a complete theory must contain four essential elements": What (factors), How (their relations), Why (the rationale: "the theoretical glue that welds the model together"). "What and How describe; only Why explains." | Whetten pp. 490–491 | The structure of the contribution check. **Framework mapping:** Why plays the role of warrant and backing for the contribution. | — |
| **concept / construct** | The factors (Whetten's What) a theory relates; "propositions involve concepts, whereas hypotheses require measures". | Whetten pp. 490–491 | Defined in the paper as declared starting points (definitions). | — |
| **assumption** | Whetten's Why: "This rationale constitutes the theory's assumptions". | Whetten p. 491 | A declared starting point: stated explicitly, contestedness recorded. | An unstated assumption is often a hidden warrant: if the audience may not share it, register it as a declared starting point (or give the warrant backing). |
| **Who / Where / When** | "These temporal and contextual factors set the boundaries of generalizability, and as such constitute the range of the theory." | Whetten p. 492 | The boundary conditions of a contribution. | — |
| **boundary conditions** | The range within which a theory or recommendation applies (Who/Where/When). | Whetten p. 492 | Required for every normative claim and every contribution. | A tautology ("applies where applicable") is not a boundary condition (DR-004). |
| **proposition** | A statement relating concepts that research can test; propositions "should be limited to specifying the logically deduced implications for research of a theoretical argument". | Whetten pp. 491–492 | **Not** a framework unit after DR-027; a paper may still contain Whetten-style propositions, registered as descriptive claims. | DR-004's PROPOSITION meant a recommendation. Whetten: "Some authors mistakenly use propositions to summarize a body of literature." |
| **evidence for a critique** | "logical (e.g., the theory is not internally consistent), empirical (its predictions are inconsistent with the data accumulated from several studies), or epistemological (its assumptions are invalid". | Whetten p. 493 | The kinds of **objection** the contribution check considers. | — |

Whetten's seven reviewer questions (What's new? So what? Why so? Well done? Done well? Why now? Who cares?) answer "What constitutes a publishable theory paper?" (p. 494). Some ("Are the underlying logic and supporting evidence compelling?") overlap verification; the framework splits by unit (claim vs contribution), not by question.

## 3. Verification and validation (systems engineering)

| Term | Definition | Source | Framework use | Common confusion |
|---|---|---|---|---|
| **verification** | "Verification of a product shows proof of compliance with requirements." | NASA §2.0 (web page, not machine-checked) | **Framework mapping:** checking each claim against its grounds and warrant (model step 4). A source check establishes faithful attribution, not that the source is reliable or the claim true. | Draft 1 of Paper 1 used "verification" for every kind of check without defining it. |
| **validation** | "Validation of a product shows that the product accomplishes the intended purpose in the intended environment." | NASA §2.0 (web page, not machine-checked) | **Framework mapping:** the contribution check: does the contribution serve its audience and purpose? | Not the logician's "valid argument". |
| **traceability** | IPCC authors must "provide a traceable account describing your evaluation of evidence and agreement". | Mastrandrea et al. (PDF p. 3) | The claim registry: contribution → claims → grounds → sources, each link recorded. | — |

## 4. Confidence and calibrated language

| Term | Definition | Source | Framework use | Common confusion |
|---|---|---|---|---|
| **confidence** | "Confidence in the validity of a finding, based on the type, amount, quality, and consistency of evidence ... and the degree of agreement. Confidence is expressed qualitatively." | Mastrandrea et al. (PDF pp. 2, 4) | Named by the framework's **confidence tier**. | Not "statistical confidence"; IPCC says it is "distinct from 'statistical confidence'". |
| **confidence tier** | The framework's four-level rating of a claim: ESTABLISHED, SUPPORTED, EMERGING, SPECULATIVE (DR-002). | DR-002 | Decides which qualifiers a claim may carry. DR-002 assigns it mainly by counting agreeing, independent sources (source quality is recorded separately as **Source Tier**). | The counting rule is the framework's, simpler than IPCC's evidence × agreement and not calibrated to IPCC's levels. By Toulmin's p. 35 the tier names are field-invariant but the assignment rule may be field-dependent; the rule is due its own review. |
| **calibrated language** | IPCC: "a common approach and calibrated language" for the degree of certainty in findings. GRADE's practice fixes wording per certainty level *and* effect size, e.g. for a large effect: high "x results in a large reduction", moderate "x likely results in …", low "x may result in …". | Mastrandrea et al.; Santesso et al. (abstract) | DR-002's tier-to-wording table, an adaptation with one axis (certainty) where GRADE has two. | DR-002's wording was not tested with users; GRADE's was surveyed (110 respondents) and workshopped. |
| **likelihood** | IPCC's probabilistic scale ("Likely 66-100%" etc.), separate from confidence. | Mastrandrea et al. | Not used: the framework has no probabilistic terms. | — |

## 5. Claims in the registry

| Term | Definition | Framework use |
|---|---|---|
| **descriptive claim** | A claim about how things are: a finding, an inference, a Whetten-style proposition. | Checked by the checks its grounds require. |
| **normative claim** | A claim about what should be done. | As descriptive, plus boundary conditions, plus at least one declared value among its grounds (framework rule: a recommendation names the value it serves). |
| **source** | A cited work. As grounds, what counts is what the source **reports**; the citation only locates it. | Each source gets a source check and a Source Tier. |
| **own work** | The author's own observation, experiment, measurement or query, used as grounds (`own:`). | Recorded with its method and date, so it can be repeated; judged by the rigour of the method (DR-008), not by counting. Not a source: it has no Source Tier. |
| **declared starting point** | An assumption, definition or value the paper adopts rather than argues for. | Stated explicitly in the text; its contestedness recorded (accepted in the field / contested / the paper's own). A distinction taken from a source and adopted as a premise is recorded both ways: `src:` for where it comes from, `decl:` for the adoption. Definitions also appear in the paper's glossary (DR-028). No confidence tier: a claim resting on a contested starting point says so in its text. |
| **source check** | Two steps: the source exists; it says what the claim attributes to it. Its Source Tier is recorded alongside. | The implicit warrant ("this source is a reliable authority on this point") is assessed through the Source Tier. |
| **warrant check** | Does the step from these grounds to this claim hold for the audience? | Required whenever a claim rests on other claims, or synthesises several sources. |
| **contribution check** | Whetten's elements and questions applied to each contribution. | A validation step. |

**Worked examples.**

| Claim | Says | Grounds | Checks | Qualifier / tier |
|---|---|---|---|---|
| "Smith (2020) found that X." | descriptive | source: Smith 2020 (reports X) | source check | "found" (attribution) / EMERGING, one source |
| "No consensus checklist exists for verifying argument quality in non-empirical papers." | descriptive | sources: searches of EQUATOR and the literature; claims: field-specific guidance covers other aspects | source checks; warrant check (absence inferred from a search) | "we found no" / EMERGING |
| "Journals should ask authors of perspective papers to register their central claims." | normative | claims: the two above; value: published reasoning should be checkable | warrant check; value declared; boundary conditions | "should" / per tier of its weakest grounds |

## 6. Other framework terms

| Term | Definition | Framework use |
|---|---|---|
| **claim registry** | The record of every claim in a paper: statement, what it says, grounds, qualifier, confidence tier, priority, check status. | Its links are the traceability. |
| **priority** | How much the paper depends on a claim: P0 "paper fails without these"; P1 strengthens but does not break the argument; P2 context. | Assigned by asking what fails if the claim is wrong. Sets coverage targets and, for P0, the tier floor (DR-002). |
| **coverage** | The share of claims at each priority whose checks are complete. | Targets ≥85% overall, 100% P0, 90% P1, 70% P2 (`templates/claim-registry.md`, `docs/THRESHOLDS.md`). |
| **check status** | Per claim: not started `[ ]`, in progress `[~]`, complete `[x]`, problem needing attention `[!]` (`templates/claim-registry.md`). | Coverage counts `[x]`. |
| **Source Tier** | Quality class of a cited work: A peer-reviewed primary research; B peer-reviewed review; C textbook or established reference; D guidelines or standards; E own work published or under review elsewhere. (F, logical inference, is retired under DR-027: an inference is a warrant.) | Recorded per source (`templates/claim-registry.md`); distinct from the confidence tier. |
| **independent sources** | Sources that do not derive the point from one another or from a shared origin (same data, same group, one citing the other for it). | What DR-002's counting rule should count. |
| **evidence** | Informal: what the sources report, taken together. | The formal term is grounds. |
| **objection** | A claim made against a claim or contribution: logical, empirical or epistemological (Whetten p. 493). | Engaged objections are recorded with the claim they target. Distinct from rebuttal (a stated exception). |
| **audience** | The readers a paper addresses. | Warrants are judged relative to it; it fixes the field. |
| **provenance** | Who introduced a claim or citation into the text: the author, or an AI tool. | AI-introduced citations always get the anti-hallucination checklist. |
| **hallucinated citation** | A citation to a work that does not exist, or that does not say what it is cited for. | Caught by the source check. |
| **gate** | A checkpoint a paper must pass before the next phase (`templates/vv-framework.md`). | Unchanged. |
| **Step Z** | The check that a sentence's language does not outrun the tier its evidence actually supports, which also catches a wrongly registered tier (`templates/anti-hallucination.md`; scope: every surface that states claims, DR-019). | Unchanged. |

## 7. From DR-004 terms to this glossary (DR-027)

| DR-004 term | Becomes | Why |
|---|---|---|
| CLAIM | descriptive claim resting on sources | Toulmin's claim is any assertion; what the source reports is its grounds. |
| ARGUMENT | claim resting on other claims, with a warrant check | The argument is the layout; what is registered is its claim. |
| PROPOSITION | normative claim if it recommends; descriptive if it says what can be done; for a paper's central idea, the contribution | Whetten's proposition relates concepts; DR-004's recommended. |
| Confidence / tier | confidence tier; the hedge in the sentence is the qualifier | Toulmin's qualifier is the strength of the step; the tier is the framework's rating. |
| Grounds / Premises columns | grounds, typed per item | One term for what a claim rests on. |
