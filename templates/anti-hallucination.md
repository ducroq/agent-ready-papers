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

## Verifying Web Sources: WebFetch Fallback Discipline

When the source for a claim is a website (an organisation's homepage, a non-academic publisher, a public-facing report), Step 6 (read the relevant section) becomes "fetch the relevant page and confirm the content." Two failure modes emerge that have no analogue when verifying a paper:

- **Subpage blindspot** — WebFetching the homepage may not surface a topic the site covers on a dedicated subpage. Concluding "topic absent from this source" based on a homepage fetch alone risks demoting a verifiable claim to a defect. *WebSearch lies about what is on a page; homepage WebFetch lies about what is on the rest of the site.*
- **Transport failure (Cloudflare / bot-protection)** — some sites serve WebFetch under HTTP 403 even when the content is openly readable in a browser. WebSearch typically has cached or syndicated access. Falling back to WebSearch is acceptable for some confidence tiers but not others.

### Fallback ladder

Before concluding "topic absent from primary source," walk the ladder:

1. **First attempt — most-specific guess.** `/<topic-name>/`, `/tools/<topic-name>`, `/about/<topic>`. Use the most informative URL you can guess from the claim.
2. **If negative — broaden the search:**
   - WebFetch the homepage `/` (the site index may link to the topic)
   - WebSearch `"<topic>" site:<example.org>` (returns the canonical URL on the site if any)
   - WebFetch `/sitemap.xml` (the structured site map names every indexed page)
3. **Only after the ladder returns empty,** conclude "topic absent from this source." Frame the registry note as *"not surfaced in pages we checked"* rather than *"primary source does not carry the topic."* The distinction is honest about the search bounds.

### Worked examples (grant application, 2026-05-22)

**Constructive Institute Algorithm.** Initial WebFetch of `https://constructiveinstitute.org/` returned "no Constructive News Algorithm mentioned anywhere on their public homepage." This nearly demoted a sharp differentiation claim to a soft fallback. Step 2 of the ladder (WebSearch `site:constructiveinstitute.org`) surfaced `/constructive-news-algorithm/`. WebFetching that page returned verbatim primary-source content with much stronger detail than the original framing (since 2019, GNI + EBU + EU funding, EBU "A European Perspective" consortium, in testing with newsrooms, *not openly available*). The claim was promoted from `[~]` to `[x]` ESTABLISHED with verbatim quotes.

**Solutions Journalism Network impact figures.** Initial WebFetch of `https://www.solutionsjournalism.org/impact/explore-our-impact` returned no numbers. Step 2 of the ladder (try the `/impact` root) surfaced verbatim *"102,300 Journalists, educators and students trained and using SJN tools."* The claim was recovered.

Both failures share the same mechanism: the first URL chosen does not carry the claim, even though the site does. Without the ladder, both would have failed silently — the agent concludes "absent from source" and the downstream prose softens or strikes the claim.

### When to apply

- Always, when the source is a website and the claim is P0 or P1
- Always, when a first WebFetch returns "topic not mentioned" and the claim's importance to the argument justifies a second attempt
- Skip the ladder when the topic is unambiguously not in the site's domain (don't burn cycles confirming the obvious)

### Adoption-readiness

The ladder structure is stable across applications. A companion failure mode (transport-level WebFetch 403 with bounded WebSearch fallback) is tracked separately and has not been promoted to a checklist step.

---

## Step Z: Inverse Hallucination Check (PROVOCATION-specific)

*Applies only to projects that contain PROVOCATION entries — speculative-design, design-fiction, diegetic-prototype work. See [DR-010](../decisions/DR-010_provocation-unit-type.md). Standard empirical and methodological projects can skip this section.*

The Steps 0–6 checklist guards against the standard hallucination: an agent invents a source for a real-sounding statement. PROVOCATIONs surface the *inverse* failure mode: an agent presents a speculation *as if* it had a citable source. A fictional speculative-design criterion ending in `[Author, Year]` is a hallucination *into fictional territory* — the exact opposite move from standard fabrication.

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

**Agent output (in a speculative-design book imitating DSM diagnostic form):**
> "Criterion A.1 — Strong preference for in-group members and activities (DSM-X §301.42, American Psychiatric Association, 2025)."

| Check | Action | Result |
|-------|--------|--------|
| Step 0 (DOI / Scholar) | Search "DSM-X §301.42 American Psychiatric Association 2025" | FAIL — no such reference |
| Step Z.1 | Source not verified — continue Step Z | — |
| Step Z.2 | Project is speculative-design; the diagnostic entry is a diegetic prototype by design (DR-010, Auger 2013) | No source can apply |
| Step Z.3 | Tier: **CRITICAL** — the fiction critiques DSM diagnostic reification by imitating its form | — |
| Step Z.4 | Required prose marker for CRITICAL: *"By imitating this DSM form we ask…"* | Add to manuscript |

**Result:** the citation is removed, the entry is reclassified as PROVOCATION (CRITICAL), and the chapter prose is rewritten so the diagnostic form is held seriously *inside the fiction* while the reflexive marker signals fictionality to the reader at every load-bearing moment.

A naive Steps 0–6 audit would have flagged this as a missing source and prompted a literature search. Step Z catches that the entry is a category error, not a sourcing error.

---

## Step 7: Multi-Pass Review Across Model Families

*See [DR-011](../decisions/DR-011_multi-model-review-pattern.md) for the full pattern, evidence, and revisit conditions.*

Steps 0–6 verify that **citations exist and say what we claim**. Step Z catches the inverse failure mode (speculation presented as if sourced). Step 7 addresses a third failure mode: that **the drafting model and a same-family reviewer share biases neither can escape on their own**.

Use up to three passes, each escaping a specific bias:

| Pass | Reviewer | Bias escaped | When |
|------|----------|--------------|------|
| **Pass 1** | Intra-family small (e.g., Haiku-class), fresh session | Sunk-cost-from-the-drafting-session | Every publish |
| **Pass 2** | Intra-family large (e.g., Opus-class), fresh session | Sunk-cost-from-the-drafting-session; different review character (argument-shape critique vs. checklist rigour) | Blog-scale: every publish. Paper-scale: every major revision / before each phase gate. |
| **Pass 3** | Cross-vendor (e.g., Gemini, GPT) | Training-data and stylistic priors shared by the entire family | High-stakes content only, **with mandatory style/voice filter** specified in `templates/review-prompt.md` |

Passes 1 and 2 are complementary, not redundant — in the triggering observation, different model sizes within the same family caught essentially disjoint issues. Pass 3 is opt-in for high-stakes content; without the style/voice filter, most cross-vendor suggestions will be style violations the human has to manually discard.

The three-pass structure and style-filter requirement are stable; specific cost-tier defaults are provisional pending paper-scale application. See DR-011 *Revisit If* for falsifiable demotion paths.

---

## When to Run This Checklist

- **Always:** Step 0 + full checklist for every new citation introduced by an AI agent
- **Spot-check:** Step 0 as initial filter; if it passes, continue with Steps 4–6 at minimum
- **Re-verify:** When an agent changes the claim wording for an existing citation — Steps 4–6
- **Skip only:** For citations you personally retrieved from the source paper
- **Step Z:** Run on every entry in projects with PROVOCATION enabled, before Steps 0–6 — to catch the inverse failure mode (speculation presented as if sourced)
- **Step 7:** Run before publish / submission. Pass 1 every publish; Pass 2 per the scale guidance above; Pass 3 only for high-stakes content with the style filter active

---

## Quick Version (for spot-checks)

If Step 0 passed and you cannot run the full checklist, at minimum verify the content-level checks:
1. Does the claim match the paper's scope? — Step 4 (catches attribution errors)
2. Is the exact location cited? — Step 5 (catches vague citations)
3. Have I read the relevant section? — Step 6 (catches paraphrasing errors)

Step 0 already covers existence; the Quick Version focuses on whether the source *says what we claim it says*. The full 6-point check is always preferred.

---

*Non-negotiable practice for AI-assisted academic writing.*
