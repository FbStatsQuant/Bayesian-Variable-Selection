# BRIEF BT1 — "better theorem" review (sharpness gate; blind first read), seat: Astra (codex gpt-6-astra, reasoningEffort high)

You are a strong, independent mathematical reviewer. You are asked **only one thing**: propose strictly better
provable statements than the ones in the target file — weaker hypotheses, stronger conclusions, wider scope, better
rates, or a cleaner design-agnostic formulation — each with a proof sketch that is concrete enough to check. Do not
review correctness line by line and do not praise. If you believe no credible improvement exists for a clause, say so.
Repository root = your working directory. Read-only, except the one output file. No git changes. No subagents.

## Target
`Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.1) and its entry map `Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md`
(where each hypothesis enters, and what small numerical experiments just outside each hypothesis showed; outputs in
`Theory_work/Wave3/W3-MISR/numerics/`).

Context in two lines: a Bayesian variable-selection posterior (g = n ridge-type score on standardised data, IG(0.01, 0.01)
variance prior, capped beta-binomial model prior) is run on a candidate subset of the columns only; the omitted
columns' contribution makes the candidate model misspecified. The statement reduces this, by an exact scale invariance
and a Gaussian-contrast-residual condition, to well-specified theorems (W3-POST2) in signal-to-noise form.

## Files you may read
- The inputs the statement is reduced to: `Theory_work/Wave3/W3-POST2/STATEMENT.md`,
  `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,B_tail_approx,C_expectation,D_hellinger,E_visibility}.md`,
  `Theory_work/Wave3/W3-POST/STATEMENT.md`.
- Version 1 of this theorem: `Theory_work/Wave1C/C-MIS/STATEMENT.md`, `Theory_work/Wave1C/C-MIS/lemmas/*.md`.
- Program rules for what counts as better: `Theory_work/Wave3/PROGRAM.md` (presentation rule: no design family in a
  theorem statement; tie-break design-agnosticism > range of p > rate > constants; all results asymptotic, p ≤ n^A,
  p ≫ n the regime that matters; statements about the method as coded).
- Code, if useful: `Scripts/SMC_BVS/core/`.
Do not read anything under a `reviews/` folder, any LOG/PLAN/CHECKPOINT/REPORT file, or `Theory_work/Wave3/API_AUDIT/`.

## What to deliver
For each proposal: (1) the exact improved statement; (2) which clause of STATEMENT.md it improves and on which axis
(hypothesis / scope / range of p / rate / constant / restatement only); (3) a proof sketch naming the lemmas of the
input files it uses and the new steps; (4) your estimate of the cost (trivial / a few lines / a new lemma / hard) and
of the risk that it is false; (5) whether the present proof route already gives it.
Questions you may want to consider (not exhaustive, and do not feel bound by them):
- Is the Gaussian-contrast-residual condition GR^c the weakest form in which the reduction is exact? Can the scalar
  covariance or Gaussianity be weakened at low cost (for example, to what a different exact invariance or a
  conditioning argument gives)? Is there a better way to state the conditional version (§4)?
- Are the signal-to-noise hypotheses (E^σ), (F₀), (OS), (ID^{M,σ}) the right interface, or can one be dropped or
  merged for the misspecified problem specifically? The numerics suggest (E^σ) is not needed.
- Can the conclusions of §3, §4, §6 be strengthened (for example expectation or uniform versions of §6, rates in
  §4(c), an out-of-sample statement under Gaussian rows)?
- Is there a formulation of the misspecified-subset theorem that is closer to Song–Liang (2015) Theorem 4 /
  Corollary 2, or that covers the empty projection s = 0, with the tools available?
- Anything in the statement that is weaker than what its own proof route gives ("unharvested" conclusions).
Rank your proposals by value/cost. Separate clearly: (A) follows from the present route with a few lines;
(B) needs a new lemma; (C) speculative.

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/BT1_better_theorem_astra.md`. Final message: the number of proposals in
classes A / B / C and a one-line statement of the best one.
