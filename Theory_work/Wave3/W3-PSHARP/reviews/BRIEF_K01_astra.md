# BRIEF K01 — break review (blind first read) — W3-PSHARP

You are an independent adversarial reviewer (gpt-6-astra, reasoning effort high). Three sharpness records (lower
bounds / a counterexample) for a Bayesian variable-selection posterior have been stated; proofs are being written.
**Your job is to break them**: find a false claim, a hidden assumption, a wrong constant, a step of the planned proof
route that cannot work, or a numerical check that does not check what it says. You are not asked to be constructive
until section 5.

## What to read (and nothing else in `Theory_work/Wave3/W3-PSHARP/`)
- `Theory_work/Wave3/W3-PSHARP/STATEMENT.md` (v1.1) — the claims.
- `Theory_work/Wave3/W3-PSHARP/PLAN.md` (proof routes) and `ASSUMPTION_MAP.md`.
- `Theory_work/Wave3/W3-PSHARP/numerics/` — scripts `core.py`, `a_orth.py`, `a_sph.py`, `a_boundary.py`, `b_check.py`,
  `c_counter.py` and their `*_out.txt` outputs (`a_orth_out.txt` and `a_boundary_out.txt` may still be growing while
  you read: long runs).
- Definitions and the results being sharpened: `Theory_work/Wave3/W3-POST/STATEMENT.md` (§0 lines 16-39 define the
  coded target π; Lemma 1a′; Theorem 1; Corollary 1R), `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`,
  `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md`, `Theory_work/Wave3/W3-POST2/STATEMENT.md`,
  `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md` (A2), `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`.
Do **not** read `LOG.md`, `BRIEF.md`, or anything under `reviews/` other than this brief. You may write and run your
own code (Python: `py -3.13 -I`; numpy, scipy, mpmath available); keep it under
`Theory_work/Wave3/W3-PSHARP/reviews/K01_scratch/`.

## Attack list (not exhaustive)
1. **Lemma S.** Schur-complement identities; the bound D_{S∪{j}}/D_S ≤ n and its equality case; the sign and size of
   the fit term; rank-deficient S; S = ∅.
2. **Proposition A (the √(log p) lower bound).** (a) Is the constant right — Λ_n = (s₀+1)[2N_n/(2p−1−s₀)]√(log N_n/(πn))
   — or off by a factor (truncation level, studentisation by s_y, ν = 0.01 + n/2, the (n−1)/n factors)? (b) (W-orth):
   the null scores and the quantity V = s_y²(2b₀ + Q_{S₀}) are dependent — does the planned argument survive that?
   (c) (W-sph): is the claimed conditional law of the projections correct after centring and scaling the columns? Is
   independence from (X_{S₀}, ε) really enough when the other columns are arbitrary? Does the bound on
   Q_{S₀} − ‖ρ̃‖² hold with only (C) (no eigenvalue floor on S₀)? Are the two logarithmic restrictions sufficient? Does it
   really cover p ≫ n? (d) uniformity and the transfer to random (X_{S₀}, θ*). (e) Corollaries A1, A2 (growing s₀:
   are (E), (C) even satisfiable; is the conversion from odds to δ_n right when Λ_n ↛ 0?). (f) Remark A3: do the two
   example sequences satisfy the hypotheses of Theorem 1 / Corollary 1R as written?
3. **Corollary B.** The closed form of 𝒪^{lb}_n; "surely"; the constants; s₀ = 0; whether B2/B3 say more than is
   proved.
4. **Proposition C (counterexample).** Does the design exist and is it standardised? Is every hypothesis of Lemma 1a′
   except the coefficient bound really in force for T = {1, 2} (check Lemma 1a′'s exact wording), and does item 3
   really contradict its conclusion — and that of Lemma 1a″? Check the constants (k = ⌈12 log n⌉, n₀ = 200,
   C_b = 1200), the claim B_T(ϑ) ≥ b_n²(n − 1)/2 for every ϑ, the cutoff bound, and the uniform-in-S fit bound when S
   contains x₁ and/or x₂. Can a model of size ≤ k/2 fit μ after all (e.g. using x₂ with a huge coefficient — what does
   the ridge prior actually cost)?
5. **Numerics.** Is "exact" exact (the Gamma-integral/elementary-symmetric DP; the "exact-in-law reduction" in
   `a_sph.py`; the structured enumeration and cancellation-free formulas in `c_counter.py`)? Do the outputs support
   the claims, or is there a trend against them (e.g. ratios drifting below 1)? Re-run or re-implement what you doubt.
6. **A strictly stronger record?** Only after the above: is there a strictly stronger statement of the same kind
   that is provable at comparable cost (wider witness class, better constant, a matching upper bound, a sharper
   threshold in C)? Give a proof sketch; label it PROPOSAL.

## Output
Write your full review to `Theory_work/Wave3/W3-PSHARP/reviews/K01_break_astra.md`:
- per claim (S, A, A1, A2, A3, B, B1–B3, C.1–C.3): `BROKEN` / `NOT-BROKEN` / `COULD-NOT-CHECK`, with what you did
  (derived / tested numerically / read only);
- findings labelled FATAL / MAJOR / MINOR / NIT with exact place (file:line) and the exact correction;
- section 6 proposals, if any.
Do not change any file other than your review file and your scratch directory. Do not commit. Start no subagents.
Reply with the per-claim verdicts and the counts of findings by severity.
