You are a reviewer applying a verification framework to a Dutch-language essay. Read it fully. The essay's cited sources are provided as plain-text files in the directory ./sources/ (sources/refNN.txt is reference NN in the essay's reference list). Read them. Do NOT browse the web and do not read files outside the current directory. Answer in English, quote the Dutch text you flag.

Work in this order, the framework's process:
STEP 1 - Claim registry: list every claim the essay puts forward, each with what it says, its grounds (src:refNN / claim:another claim / decl:declared starting point / own:author's own work / none) and a confidence tier.
STEP 2 - Source check: for every src: ground, open the source file and check (a) the source exists and can be found; (b) the claim matches the source's scope: could this source plausibly contain the claim?; (c) the exact location of the supporting passage; (d) read that passage: does the source actually say what the essay claims it says? Watch for paraphrasing that subtly changes meaning. Record the passage.
STEP 3 - Apply the rules below to the essay, using the registry.

Framework rules:
1. Confidence tiers -> allowed language. ESTABLISHED: "demonstrates/shows/confirms" (NL: toont aan, bewijst, laat zien). SUPPORTED: "indicates/supports/evidence suggests". EMERGING: "may/preliminary". SPECULATIVE: "we hypothesize/remains unclear". Step Z: flag every sentence whose language tier exceeds what its grounds (cited source, argument, or nothing) support. Also flag the reverse only if striking (heavy hedging on a well-sourced fact).
2. Every claim has grounds: a source, another claim (needs a warrant: does the step hold?), a declared starting point (assumption/definition/value, stated in text), or own work (repeatable method). Flag claims with no visible grounds, and inferential steps whose warrant is missing or weak (Toulmin: claim, grounds, warrant, backing, qualifier, rebuttal).
3. Normative claims (ought/should/responsibility) need explicit boundary conditions and a declared value. Check every normative proposal in the essay against this.
4. Calculation verification: recompute every number the text derives itself (derived values, percentages, worked examples, growth rates). Note any input the text computes with but does not state. A figure the text attributes to a cited source is grounded by that source, not an unstated input.
5. Scope drift: does the essay deliver what its title and introduction promise?
6. Contribution check (Whetten): for the essay's main contributions, what/how/why/who-where-when — is each answered?

Output: a markdown list of findings, each with: id, rule number, quoted text, problem, severity (high/medium/low), suggested fix. Then a 3-sentence overall verdict. Be adversarial but fair; do not pad. Max ~900 words for the findings and verdict. Then append the registry from STEP 1 as a compact table (up to ~800 words; it is not scored).
