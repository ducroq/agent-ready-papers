# Anti-Hallucination Checklist

<!-- Run this for EVERY citation introduced by an AI agent.
     Takes ~2 minutes per citation. Catching a fake citation in review takes weeks. -->

## Step 0: Quick Web Verification

Before running the full checklist, do a quick web search to catch obvious hallucinations in seconds:

1. Search Google Scholar for `[Author Year Title]`
2. Check if a DOI resolves at `https://doi.org/[DOI]`
3. If both return the source → proceed to full checklist for exact claims
4. If the source cannot be confirmed via both signals → **HIGH RISK** of hallucination; investigate before proceeding

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
| **Inverse fabrication** *(speculative-design only)* | Fictional artefact presented with a citation as if sourced (e.g., a diegetic DSM entry attributed to a real journal) | Run Step Z — reclassify as PROVOCATION, not source-hunt |

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

## Verifying Negative Claims ("No X Exists")

Claims that something *doesn't* exist (e.g., "no guidelines exist for non-empirical papers") require a different verification strategy:

1. **Define the search scope** — what databases/registries would contain X if it existed?
2. **Search systematically** — search each database using relevant terms
3. **Document the null result** — record search date, terms used, and databases checked
4. **Hedge the universal negative** — use "to our knowledge" or "we are not aware of" rather than unqualified "no X exists"

**Worked example:**
> "No EQUATOR guidelines exist for non-empirical papers" → Verified by searching EQUATOR Network database (equator-network.org, accessed 2026-03-03): all 699 guidelines address empirical research types; search for "theoretical," "design science," and "perspective" returned no results. Hedged in manuscript as "to our knowledge, no equivalent guidelines exist."

## Step Z: Inverse Hallucination Check (PROVOCATION-specific)

*Applies only to projects that contain PROVOCATION entries — speculative-design, design-fiction, diegetic-prototype work. See [DR-010](../decisions/DR-010_provocation-unit-type.md). Standard empirical and methodological projects can skip this section.*

The Steps 0–6 checklist guards against the standard hallucination: an agent invents a source for a real-sounding statement. PROVOCATIONs surface the *inverse* failure mode: an agent presents a speculation *as if* it had a citable source. A fictional FSD criterion ending in `[Author, Year]` is a hallucination *into fictional territory* — the exact opposite move from standard fabrication.

The check has to run in both directions:

- **Forward (Steps 0–6):** is the cited source real, and does it say this?
- **Inverse (Step Z):** is the entry behaving as a citation when no source can apply?

Inverse hallucinations are dangerous because Steps 0–6 will *fail to fail* on them — the source plausibly does not exist (the agent invented it), and the entry will look like a verifiable CLAIM that simply needs more sourcing. The fix is type re-classification, not source-hunting.

### Workflow

For every entry in a project with PROVOCATION enabled, before running Steps 0–6:

1. **Is the source real?** Run Steps 0–6 of the checklist.
   - If the source verifies → entry is a **CLAIM**; Steps 0–6 are sufficient.
   - If the source cannot be verified → continue.
2. **Could a source apply at all?** Inspect the entry against the unit-type decision tree (`templates/claim-registry.md` → "Detecting Mistyped Entries").
   - If a source *should* apply but is fabricated → standard hallucination; remove the citation, search literature, replace with a verified source or downgrade tier.
   - If no source can apply (the entry is a designed/fictional artefact) → reclassify as **PROVOCATION**; continue.
3. **Assign a PROVOCATION tier** (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL — see `templates/claim-registry.md` → "PROVOCATION Confidence — Separate Axis").
4. **Add the tier-required reflexive marker** to the prose. Without the marker, the entry remains indistinguishable from a fabricated CLAIM and must be rewritten or downgraded to EMERGING CLAIM with additional sources.

### Worked Example

**Agent output (in an FSD-style speculative-design book):**
> "Criterion A.1 — Strong preference for in-group members and activities (DSM-FSD §301.42, American Psychiatric Association, 2025)."

| Check | Action | Result |
|-------|--------|--------|
| Step 0 (DOI / Scholar) | Search "DSM-FSD §301.42 American Psychiatric Association 2025" | FAIL — no such reference |
| Step Z.1 | Source not verified — continue Step Z | — |
| Step Z.2 | Project is speculative-design; the FSD diagnostic entry is a diegetic prototype by design (DR-010, Auger 2013) | No source can apply |
| Step Z.3 | Tier: **CRITICAL** — the fiction critiques DSM diagnostic reification by imitating its form | — |
| Step Z.4 | Required prose marker for CRITICAL: *"By imitating this DSM form we ask…"* | Add to manuscript |

**Result:** the citation is removed, the entry is reclassified as PROVOCATION (CRITICAL), and the chapter prose is rewritten so the diagnostic form is held seriously *inside the fiction* while the reflexive marker signals fictionality to the reader at every load-bearing moment.

A naive Steps 0–6 audit would have flagged this as a missing source and prompted a literature search. Step Z catches that the entry is a category error, not a sourcing error.

---

## When to Run This Checklist

- **Always:** Step 0 + full checklist for every new citation introduced by an AI agent
- **Spot-check:** Step 0 as initial filter; if it passes, continue with Steps 4–6 at minimum
- **Re-verify:** When an agent changes the claim wording for an existing citation — Steps 4–6
- **Skip only:** For citations you personally retrieved from the source paper
- **Step Z:** Run on every entry in projects with PROVOCATION enabled, before Steps 0–6 — to catch the inverse failure mode (speculation presented as if sourced)

---

## Quick Version (for spot-checks)

If Step 0 passed and you cannot run the full checklist, at minimum verify the content-level checks:
1. Does the claim match the paper's scope? — Step 4 (catches attribution errors)
2. Is the exact location cited? — Step 5 (catches vague citations)
3. Have I read the relevant section? — Step 6 (catches paraphrasing errors)

Step 0 already covers existence; the Quick Version focuses on whether the source *says what we claim it says*. The full 6-point check is always preferred.

---

*Non-negotiable practice for AI-assisted academic writing.*
