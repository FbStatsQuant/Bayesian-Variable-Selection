# W2-APP — PLAN

1. Statement lock (Codex gpt-6.1-sol high): STATEMENT.md + PLAN.md vs FIN sources. Fix, lock.
2. Part 1 lemmas (lead writes; each gets falsification numerics in numerics/ and a cross-family line check):
   - L1_POST (random-design T03♯ hypotheses under LSF) — numerics: sample sparse eigenvalues vs population for
     AR(1)/equicorrelation/factor at p ≫ n (exact small k + greedy).
   - L2_CT (Combes–Thomas; uniform conditional-covariance decay) — numerics: random LOC matrices, all U up to size 6
     plus random large U, check |Cov(W_j,W_k|W_U)| ≤ K₂e^{−a₂d} with the explicit constants.
   - L3_LOC (delta-proof vs GROW L6: replace P1–P4 by L2_CT; new NA lemma with windowed approximate innovations)
     — key lemma; xhigh check. Numerics: approximation error |Z_{T,l} − Z'| for MA(2)/AR(2)/block designs.
   - L5_VN (obstruction) — numerics: start mode (Python port of D0 score + exact block DP, or the core) on STAR,
     growing blocks, equicorrelation: count of nulls in S̃₀ vs the bound.
   - L4_families — per-family verification of the hypotheses; ARMA/Toeplitz spectral facts cited as standard
     (Grenander–Szegő) with explicit statement.
3. Part 2 (Sonnet helper, data_diag/): public designs, design-only diagnostics, classification.
4. Mid-point review (fresh Sol xhigh: STATEMENT + lemma files only) once L3_LOC is written and checked.
5. Exhaustive sweep (Sol xhigh), fixes; CITECHECK script; council (Sol xhigh + Opus high) over Part 1 and Part 2
   conclusions; REPORT.md with the applicability table.
Helpers: Sonnet for numerics; Opus subagent possibly as parallel prover for L3 NA step.
