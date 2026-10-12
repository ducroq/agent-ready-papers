# EXP-001: Does a review by a second model find method-level problems the reader panel misses? Preregistration (2026-10-12)

Written and committed before the review is run and before any finding is seen. The test runs on a private paper, so this file describes it without naming the paper (DR-024 rule 6). Background: [#53](https://github.com/ducroq/agent-ready-papers/issues/53).

## 0. What is under test, and the decision it feeds

**Hypothesis.** A review by a model from a different vendor finds method-level problems in a full draft that the simulated reader panel does not find. The panel is four reader roles played by one model family, so its readers share that family's blind spots.

**Where it comes from.** One private narrative review (about 11,000 words at the time). After two review passes and three panel rounds, a single cross-vendor review raised three method-level problems, and the author accepted all three. The panel had raised part of one of them. That is one draft and one review, and that review also used a different prompt. So it suggests the effect may exist. It cannot say whether the model or the prompt caused it.

**Alternative.** The gain came from the different prompt, or from any fresh reading, not from a different model. With the same prompt, the second model finds nothing method-level that the panel misses, or what it finds mostly fails when checked.

**Decision it feeds.** Whether DR-011 should make Pass 3 (cross-vendor) the default before a full draft goes to an outside reader, and whether the reader-panel template should include a reader from a second model. Either change needs a new DR or an amendment. The maintainer decides.

## 1. Design

- **Draft.** The next full draft of the paper, after its 2026-10-10 revision and the author's reread, before it goes to the outside expert reader. One reading copy, frozen by its commit hash, recorded in the evidence folder before either arm runs.
- **Arm A, the panel.** The paper's reader panel, run as usual (same model family, same four roles).
- **Arm B, the second model.** One model from a different vendor than the panel's, used once, in a fresh session. Its name and version go in a run record kept with the private evidence, written before the run.
- **Same prompt.** Both arms get the reading copy and `agents/review-prompt.md`, filled in identically except for the Pass field. This is what separates the model from the prompt.
- **Known confounds.** The panel's role framing is added to arm A as usual. Arm A is four readings and arm B is one, so arm A has more chances to raise any given problem; this biases the test against the hypothesis. Both are recorded with the result.
- **Order.** Both arms run before anyone reads either output.

## 2. Counting

1. **One findings table.** An agent that did not run either arm lists every finding from both arms, one row each, rewritten in a neutral wording so the role framing and style do not show the arm. It records the arm of each in a separate key file. The run record names this agent's model, which belongs to neither arm's vendor where one is available.
2. **Matching.** The same agent, which knows the arms, marks two findings from different arms as the same if they name the same problem in the same part of the paper. It merges each matched pair into one row and logs each match, and each near-miss it did not merge, with a one-line reason. Matches are decided here and not revisited.
3. **Method-level or local.** A finding is method-level if acting on it would change the method, a verdict, or the framing of a section. Otherwise it is local. A second agent, which has not seen the key file, classifies each row.
4. **Holds up, fails, or declined.** The author judges each row without seeing the key file. Accepted, or confirmed against the sources, counts as holding up. A finding whose factual claim is wrong when checked counts as failed. A finding the author declines on judgment, with no factual error, counts as declined. A finding with a factual error counts as failed, even if the author accepts its point. If the author can tell which arm raised a finding, they note it on that row.
5. **Unblinding.** Only after step 4 is the key file opened.

## 3. Bars, fixed now

- **Confirmed** if arm B contributes at least 2 method-level findings that hold up and that no arm A reader raised. Registry decision: `kept`, meaning a DR change is proposed.
- **Inconclusive** if it contributes exactly 1. Registry decision: `parked`; the test is repeated on the next full draft.
- **Refuted** if it contributes none. Registry decision: `rejected`.
- **Cost check, whatever the count.** Count all of arm B's findings, method-level and local. If those that fail outnumber those that hold up, the step costs more checking than it gives, and the decision is `rejected` even if the first bar is met. Declined findings count on neither side, and their number is reported, so a reader can see how much the author's judgment decided.
- One draft is one observation. A confirmed result supports proposing the DR change; it does not by itself make it ESTABLISHED.

## 4. Data and cost

- The draft, both reviews and the findings table stay in the private paper. This folder later gets an anonymised summary with the counts, and the SHA-256 of each private file the summary draws on. The registry entry's `notes` will say that its metrics trace to a private source.
- Cost: arm B's API spend in USD goes in `spend_usd`; token counts for both arms go in `vv/cost-log.md`.

## 5. Predictions (before looking)

Written by the agent that drafted this file, from the one earlier case. The maintainer may add their own before the run.

- Arm B, method-level findings that hold up and that arm A did not raise: expected 1 to 3. Zero would point to the prompt as the cause last time; 4 or more would point to a fault in the matching step.
- Arm B, findings that fail: expected 1 to 3. Last time, its review contained unchecked source summaries and promised an audit it had not carried out.
- Arm A, method-level findings that hold up and that arm B did not raise: expected 0 to 2.
