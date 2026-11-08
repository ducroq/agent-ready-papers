# Supplementary material: How to read a claim register

*Draft 2026-11-08, written in answer to a reader's comment that the Toulmin layout is unfamiliar to most readers. For Learned Publishing this goes in as a separate supporting-information file. Not yet registered or checked; every quotation was checked against `literature/pdfs/toulmin-2003.pdf`.*

## 1. Toulmin's layout of an argument

Toulmin (2003, pp. 92–94) takes apart an everyday argument:

```
Harry was born in Bermuda  ──►  So, presumably,  Harry is a British subject
         (data)                   (qualifier)            (claim)
                    │                              │
                  Since                          Unless
                    │                              │
   A man born in Bermuda will            both his parents were aliens,
   generally be a British subject        or he has become a naturalised
            (warrant)                    American  (rebuttal)
```

- **Claim**: what the arguer asks us to accept.
- **Data**: the facts appealed to. The register calls them *grounds*, because they can also be other claims, a declared starting point or the author's own work.
- **Warrant**: the general rule that makes the step from data to claim legitimate. Toulmin calls it "incidental and explanatory, its task being simply to register explicitly the legitimacy of the step involved" (p. 92): "data are appealed to explicitly, warrants implicitly" (p. 93). In a paper the warrant is often unstated, and that is where a weak step hides.
- **Qualifier**: how strong the step is ("presumably").
- **Rebuttal**: when the step fails.
- **Backing**: what supports the warrant itself, such as the statutes behind the rule about Bermuda (p. 95ff). The register records it only when readers may not accept the warrant.

Toulmin modelled the layout on the law court, which separates questions of fact from questions of law (p. 93): data are the facts of the case, and the warrant is the law applied to them.

## 2. One row of this paper's register

Row S1-1, read with the layout:

| Register column | Content | Toulmin |
|---|---|---|
| Statement | LLMs tested in 2023–24 (ChatGPT on GPT-3.5 and GPT-4) invented plausible-sounding references and DOIs at substantial rates | claim |
| Grounds | `src:` Mugaanyi et al. 2024; `src:` Walters & Wilder 2023. Both peer-reviewed, both reporting their own studies | data |
| Warrant | none needed: each source reports the claim's own point (corroboration) | — |
| Confidence tier | Supported: two peer-reviewed sources agree, so the prose may say "indicates", not "shows" | qualifier |
| Rebuttal | as of 2023–24; Walters & Wilder found fewer fabrications from the newer model, so later models may fabricate less | rebuttal |

The first version of this row said "LLMs invent plausible-sounding papers": present tense, all models. Nothing in the grounds licensed the step from two studies of ChatGPT in 2023–24 to every current model. In Toulmin's terms it had an unstated warrant, and the warrant was false. A reader caught it.

## 3. Grounds that are not sources

A **declared starting point** is an assumption, definition or value that *this paper* adopts without arguing for it, for example D5: "Detection asks who wrote a text; verification asks whether it holds". It is not a claim taken from a source. A point a source took from another source is still a source item, recorded as relayed (see the source check).

## 4. Where to find the full register

The register, the glossary of terms and the tools that check them are in the public repository (see Code and Data Availability).
