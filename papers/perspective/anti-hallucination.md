# Anti-Hallucination Checklist

<!-- Run this for EVERY citation introduced by an AI agent.
     Takes ~2 minutes per citation. Catching a fake citation in review takes weeks. -->

## Step 0: Quick Web Verification

Before running the full checklist, do a quick web search to catch obvious hallucinations in seconds:

1. Search Google Scholar for `[Author Year Title]`
2. Check if a DOI resolves at `https://doi.org/[DOI]`
3. **If a DOI is cited, it must resolve.** A cited DOI that 404s is **HIGH RISK** even when Scholar confirms a paper of that name — that is the wrong-DOI / attribution case, not a fabrication, and Scholar cannot detect it.
4. **If no DOI is cited**, a Google Scholar, publisher, or ISBN record is sufficient to proceed.
5. If **neither** signal confirms the source → **HIGH RISK** of hallucination; investigate before proceeding

   > **Absence of a DOI is not itself a risk signal.** Books, standards, reports and websites are verified by publisher page, ISBN or Scholar record. 12 of the 25 entries in this framework's own `literature/` carry no resolvable DOI (no `10.xxxx/` identifier anywhere in the entry) — including Toulmin (1958), the source underpinning the ARGUMENT unit type. (Corrected twice on 2026-08-13. It first required **both** signals, which classified every DOI-less source as HIGH RISK and contradicted the rule stated 12 lines below, in the Hard Constraints, and in the WebFetch section built for those sources. The first fix made it a plain **either**, which was worse: an adversarial review seeded a positive against it using *this file's own worked example* — `10.1109/JTEHM.2024.3410652` 404s while Scholar returns a real Lim 2024 JTEHM paper, so the conjunctive rule caught it and a disjunctive rule does not. Step 1 only *records* the DOI when Step 0 passes, so nothing downstream re-resolves it. Gating on DOI **presence** rather than DOI **success** keeps the cross-check between two independent signals — which is what Step 0 actually contributes — without failing books and reports.)

This catches fabricated citations in seconds. The full 6-step checklist below remains necessary for verifying exact claims against the source content.

---

## The Checklist

For each new citation, verify ALL six points:

- [ ] **1. Confirm and record the canonical citation**
  - If Step 0 passed: record the exact DOI, canonical title, and publication year for use in Steps 2–6
  - If Step 0 was skipped: search Google Scholar or resolve at `https://doi.org/[DOI]`
  - This step ensures the exact source identity is pinned down before checking author, journal, and content

- [ ] **2. Is the author real?**
  - Check institutional affiliation page
  - Verify on Google Scholar author profile or ORCID
  - Watch for: plausible names that don't match any real researcher

- [ ] **3. Is the journal real?**
  - Check publisher website directly
  - Cross-reference with known journal lists (Web of Science, Scopus)
  - Watch for: predatory journal clones with similar names

- [ ] **4. Does the claim match the paper's scope?**
  - Read the abstract (not just the title)
  - Check: could this paper plausibly contain the cited claim?
  - Watch for: real paper, but claim attributed to wrong source

- [ ] **5. Is the exact location cited?**
  - Page number, table number, figure number, or section
  - "Smith et al. (2020)" is insufficient — where in the paper?
  - Watch for: vague citations that can't be checked

- [ ] **6. Have I read the relevant section?**
  - Not just the abstract — the actual section containing the cited claim
  - Does the source actually say what we claim it says?
  - Watch for: paraphrasing that subtly changes meaning

---

## Common AI Hallucination Patterns

| Pattern | Example | How to Catch |
|---------|---------|-------------|
| **Plausible fabrication** | Real author + real journal + fake paper | DOI check fails |
| **Attribution error** | Real paper, but claim is from a different paper | Read the actual source |
| **Number invention** | "Found a 23% improvement" — number doesn't appear in source | Check exact values against source |
| **Journal confusion** | Paper exists but in a different journal than cited | Verify publication venue |
| **Author swapping** | Correct finding but attributed to wrong author | Check author list |
| **Recency fabrication** | "Recent study (2024)" — paper is actually from 2018 | Verify publication year |

---

## Worked Example

**Agent claims:** "Human adult chest stiffness ranges 5.3–13.6 N/mm (Lim et al., 2024)"

| Check | Action | Result |
|-------|--------|--------|
| 0. Quick web check | Google Scholar + DOI: 10.1109/JTEHM.2024.3429422 → both resolve | PASS |
| 1. Canonical citation | DOI confirmed, title and year recorded | PASS |
| 2. Author real? | Lim at university affiliation page | PASS |
| 3. Journal real? | IEEE JTEHM on IEEE Xplore | PASS |
| 4. Scope match? | Paper is about a **CPR manikin mechanism**, not a study of human chests | **FAIL** |
| 5. Exact location? | Results, "Mechanical Characteristic Analysis" | PASS |
| 6. Read section? | "stiffness at maximum depth ranged from 5.34 to 13.59 N/mm" — **the device the authors built**. The paper's *human* figure is 4–10 N/mm, cited from its own reference [16] | **FAIL** |

**Verdict:** Citation **rejected** — an attribution error. The paper is real and the numbers are real, but they describe the authors' apparatus, not human anatomy. Either cite the device figure for what it is, or follow reference [16] to the human measurement and cite that source. (Corrected 2026-08-13: this table previously carried a wrong DOI (`…3410652` for `…3429422`; four digits differ, so not a transposition) and scored Steps 4–6 PASS. See the note in `../../templates/anti-hallucination.md`.)

---

## Verifying Negative Claims ("No X Exists")

Claims that something *doesn't* exist require a different verification strategy:

1. **Define the search scope** — what databases/registries would contain X if it existed?
2. **Search systematically** — search each database using relevant terms
3. **Document the null result** — record search date, terms used, and databases checked
4. **Hedge the universal negative** — use "to our knowledge" or "we are not aware of"

**Paper 1 example:**
> "No EQUATOR guidelines exist for non-empirical papers" → Verified by searching EQUATOR Network database (equator-network.org, accessed 2026-03-03): all 699 guidelines address empirical research types; search for "theoretical," "design science," and "perspective" returned no results. Hedged in manuscript as "to our knowledge, no equivalent guidelines exist."

---

## When to Run This Checklist

- **Always:** Step 0 + full checklist for every new citation introduced by an AI agent
- **Spot-check:** Step 0 as initial filter; if it passes, continue with Steps 4–6 at minimum
- **Re-verify:** When an agent changes the claim wording for an existing citation — Steps 4–6
- **Skip only:** For citations you personally retrieved from the source paper

---

## Quick Version (for spot-checks)

If Step 0 passed and you cannot run the full checklist, at minimum verify the content-level checks:
1. Does the claim match the paper's scope? — Step 4 (catches attribution errors)
2. Is the exact location cited? — Step 5 (catches vague citations)
3. Have I read the relevant section? — Step 6 (catches paraphrasing errors)

Step 0 already covers existence; the Quick Version focuses on whether the source *says what we claim it says*. The full 6-point check is always preferred.

---

*Non-negotiable practice for AI-assisted academic writing.*
