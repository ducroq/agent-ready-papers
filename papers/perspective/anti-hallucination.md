# Anti-Hallucination Checklist

<!-- Run this for EVERY citation introduced by an AI agent.
     Takes ~2 minutes per citation. Catching a fake citation in review takes weeks. -->

## The Checklist

For each new citation, verify ALL six points:

- [ ] **1. Is the paper real?**
  - Search Google Scholar or DOI.org
  - If DOI provided: resolve at `https://doi.org/[DOI]`
  - If no DOI: search exact title in quotes on Google Scholar

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
| 1. Paper real? | DOI: 10.1109/JTEHM.2024.3410652 → resolves | PASS |
| 2. Author real? | Lim at university affiliation page | PASS |
| 3. Journal real? | IEEE JTEHM on IEEE Xplore | PASS |
| 4. Scope match? | Abstract mentions chest mechanical properties | PASS |
| 5. Exact location? | Table 2, Results section | PASS |
| 6. Read section? | Values confirmed in Table 2: 5.3–13.6 N/mm | PASS |

**Verdict:** Citation verified. Safe to use.

---

## When to Run This Checklist

- **Always:** For every new citation introduced by an AI agent
- **Spot-check:** For citations you provided that the agent reformulated
- **Re-verify:** When an agent changes the claim wording for an existing citation
- **Skip only:** For citations you personally retrieved from the source paper

---

## Quick Version (for spot-checks)

If pressed for time, at minimum verify:
1. DOI resolves (catches fabrications)
2. Abstract matches claim scope (catches attribution errors)
3. Specific location exists (catches vague citations)

The full 6-point check is always preferred.

---

*Non-negotiable practice for AI-assisted academic writing.*
