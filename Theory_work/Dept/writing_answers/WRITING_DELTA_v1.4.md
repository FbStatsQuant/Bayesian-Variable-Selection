# Writing delta — assumptions section, v1.3 → v1.4 (audit Fable, 2026-11-16). Supersedes WRITING_DELTA_v1.3.md.

Cause: the second blind review refuted the v1.3 labels and headline; HQ ordered a new format. Source: `TRACK_B.md` v1.4
(headline, summary table, §S, §T3).

**New headline, verbatim.**

> Our theorems use the same kinds of assumptions as Song and Liang (2015): a Gaussian linear model, exact sparsity, a
> bound on the dimension, a law for the predictors, eigenvalue floors on small sets of columns, and nonzero
> coefficients that are not too small. On the designs we study, the assumptions of our posterior theorems hold, strong
> factors included. Where the two papers differ, the direction depends on the regime — their model-size cap, whether
> predictors are centred, and which of their theorems is the comparator — and is given assumption by assumption in the
> table.

**Format rule.** No one-word comparison (same, stronger, weaker, comparable, not ordered) unless it holds in every regime
of both papers; then say so. Otherwise one conditional sentence naming the regime, with their page and equation
(main text or supplement). The uniform cases are: the model and exact sparsity are the same as theirs; our visibility
condition implies their Condition 5; they have no condition of the kind of our leakage set, local regressions or
no-leakage. Use the summary table of `TRACK_B.md` as the source for every other sentence.

**Conclusions: per theorem only.** Do not write "our conclusions are stronger". Use: (i) against their Theorem 3, ours
adds specificity and exact selection at a polynomial rate, theirs gives sensitivity with an exponentially small error,
and neither implies the other; (ii) against their Theorem S, the statements concern different posteriors; within one
posterior, mass on the truth with a rate is a stronger form of statement than a mode statement; (iii) for the
distribution theorem, the same distance, the same exponential form of the tail for levels M ≤ √n/log n, a radius of
order √(log n/n) that their conditions do not reach at polynomial p, and larger radii and exponential p that ours does
not reach.

**Drop these v1.3 sentences.**
- "neither uniformly stronger nor uniformly weaker … we ask a narrower range of p … we ask less elsewhere …" (the whole
  v1.3 headline).
- "their proofs treat them as constants (supplement pp. 5 and 15)" → their proof steps need rates (supp pp. 6, 15);
  whether their β* may vary with n is not stated.
- "Their Theorem S … our rate for 1 − π(S₀ | y) implies it."
- "Against their Hellinger theorems we add … a row law."
- For the sampler: replace "weaker counterpart" by "their statements are limits in the number of iterations at fixed
  data, for every data set; ours hold at the coded budget under design conditions; neither implies the other".

**Unchanged:** every inside/outside entry for our designs.
