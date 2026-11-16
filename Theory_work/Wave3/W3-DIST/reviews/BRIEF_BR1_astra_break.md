# W3-DIST — CP2 key-lemma break review BR1 — gpt-6-astra, codex, reasoningEffort high

You are an independent reviewer. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one output
file `Theory_work/Wave3/W3-DIST/reviews/BR1_astra_break.md`.** Run no git command that changes state; start no agents.
You may read: `Theory_work/Wave3/W3-DIST/STATEMENT.md` (the target statements: §0 setting and interfaces, §1 master
theorems DIST-1, DIST-2, DIST-3, §1R reader versions, §3 lemmas and bridges); the key lemma
`Theory_work/Wave3/W3-DIST/lemmas/X.md` (Lemma X and Lemma X′; §8 and §10 are commentary, not proof); what it consumes:
the locked [P1] = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
and `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`; `Theory_work/Wave3/W3-DIST/API_CARDS.md` ("Common definitions");
`Theory_work/Wave3/W3-DIST/ROUTES.md`. Read nothing else in the ticket folder (no `reviews/`, `LOG.md`, `CHECKPOINT_*.md`,
`DEPS.*`, `work/`, other files of `lemmas/`). Do not read the changelog table at the foot of STATEMENT.md (stop at "## Changelog").

## Your only job: break it
The key lemma is Lemma X (the in-sample exponential core). The headline master theorem DIST-1 (display (1.1)) is to be
obtained from it by: Lemma H (deterministic Hellinger bound), Lemma T (distribution-free transfer from the n design
rows to the population on sparse directions) and integration over the design. Attack, in this order:
1. **Lemma X itself.** Construct, if you can, a fixed design, a truth and a range of t satisfying (E; M), (C; M′),
   (ND; c_D, m_n(t)) for which the conclusion fails — or a step of `lemmas/X.md` that does not hold: the pointwise
   Bayes-factor bound on the noise event; the fractional moment with λ = (4A+1)/(4A+2); the use of the average
   condition (ND) through Jensen (can a small exceptional set of J's with no determinant growth carry posterior mass
   ≥ e^{−ct} on Hellinger-far or large models?); the union device for models not containing S₀; the size tail above
   m_n(t) with the data-dependent inverse-gamma rate; models of size near n/2; the variance plug-in at the top of the
   range t = n^{1−κ₀}; s₀ = 0; uniformity of n₀ in t.
2. **Is Lemma X the right key lemma?** Does display (1.1) really follow from Lemma X + Lemma H + Lemma T + integration
   over the design as STATEMENT and ROUTES describe (the bad set of (1.1) including |S| > s₀ + C′t/log n; the interfaces
   being X-measurable while S₀ and p are themselves design-dependent; the remainder P*(interfaces fail); constants
   independent of the law of the data)? Is anything used in that passage that Lemma X does not deliver?
3. **Lemma X′ and DIST-2** (no (ND)): the same two questions.
4. **Hidden dependence.** Does Lemma X's proof use anything beyond its hypotheses and the locked [P1] (an eigenvalue
   floor, identifiability, a beta-min level, p ≤ n^A beyond the stated places, a fixed σ*)?

## Then answer the checkpoint question
Given what you found: **CONTINUE** (the proof leg should proceed to the sweep and council on this route), **REDIRECT**
(say to what, and why), or **STOP** (say why). Give reasons in at most ten lines.

## Output (`reviews/BR1_astra_break.md`)
First line: `BR1 break review — lemmas/X.md sha256 <first 16 hex> ; STATEMENT.md sha256 <first 16 hex>`. Findings with id,
severity (CRITICAL / MAJOR / MINOR / NIT), the object, the argument or counterexample in full, the minimal repair. A
verdict for each of: Lemma X; passage Lemma X → (1.1); Lemma X′; passage Lemma X′ → (1.2): BROKEN / NOT BROKEN (with what
you tried). Final line: `CP2: CONTINUE | REDIRECT | STOP` and one sentence. Do not soften findings; say exactly what you
could not check.
