# W1-EXP: One compatible family for T22 and T27, including EXP′

**Paper role:** Thm 2 (the start), item 3 in the pursuit order. Both are PROVED-LOCKED but CONDITIONAL:
- T22(iii) rests on EXP′, VIS, NL_η and NL_avg(κ);
- T27(i) rests on H2 (the sequential ratio law) and H3 (reference mass).

Astra's rule is to prove the premises jointly, on one design family (`Docs/THEORY_PRIORITIES.md`, Thm 2).

## Goals, in order
1. **EXP′ in the block-orthogonal benchmark.** EXP′ is the log-ratio expansion with an O_P(1) remainder; see `Docs/Theory/proofs/T22iii_T16_start_aggregation/STATEMENT.md` and `LOCKED_PROOFS.md`. Prove it for the block-orthogonal design (columns orthogonal across blocks, arbitrary correlation within blocks) from G, R and within-block SE. Then say how far it extends: weak cross-block correlation, or iid Gaussian designs with the actual X-dependent partition.
2. **Replace H2 with bounded leakage.** Replace T27's assumed ratio law (each table ratio about n^(−1/2)) with a **bounded-leakage condition along the chain**: a two-sided law with a controlled multiplier. Prove T27(i) from it.
3. **The compatible family.** Construct one explicit design family, for example correlated blocks with cancelling true variables, on which:
   - the T27 masking holds (π₀(S₀) → 0 at the stated rate);
   - the T22(i) deterministic bound gives near-truth start mass π₀(𝓡_d) ≥ b_n with b_n not vanishing, or vanishing at most polynomially.

   This is the input T38(b) needs. Make the family as close as you can to the study's correlated scenarios (S3–S6); see `Scripts/Data_generators/` and the R scenario code it sources, reimplemented in Python.
4. **Numerics.** Exact computation at small p (p ≤ 20) of π₀(S₀) and π₀(𝓡_d) on the family, as n grows. Show the predicted rates.
5. **Never combine regimes.** T22(iii) (favourable) and T27(i) (masked) must never be combined on one sequence. Make the regime split explicit in every statement.

## Read
`Docs/THEORY_PRIORITIES.md`; one-pagers T22, T27 and T38; statements and proofs of T22 (`T22_T16_start_aggregation/`, `T22iii_T16_start_aggregation/`) and T27 (`T27i_T20C_cancellation_budget/`); `COLLECTED_PROOFS_v2.tex` for T22(i)(ii)(iv); `00_COMMON.md`; the start-sampler sections of `METHODOLOGY_v3.md`.
