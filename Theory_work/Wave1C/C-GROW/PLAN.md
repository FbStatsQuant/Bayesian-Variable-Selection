# C-GROW — PLAN

1. Diagnosis numerics (done for p = 100: numerics/SUMMARY_DIAG.md D1–D3; p = 400 and the full method D4 running).
2. Statement lock (Codex gpt-6.1-sol, high) on STATEMENT.md + PLAN.md.
3. Lemmas (one file each), each with a falsification numeric and a cross-family check before downstream use:
   * L0 `L0_toolkit.md`: GEN L1 (score expansion, Gaussian events) restated for families of size n^{O(1)} with sets of
     size O(log n): the χ²-rank factor 2^{J/2} changes the 𝒟₂ threshold t_n; RSS floor and remainders rechecked.
   * L1 `L1_descent.md` (C1): deterministic lattice backward elimination on NA ∩ TL (model: T37R Lemma 2(b)) + capped
     search bookkeeping (model: GEN L4.1).
   * L2 `L2_NA_TL.md` (C2): P(TL) → 1; P(NA) → 1 under (G4-χ) [Pythagorean bound Z²_{T,l} ≤ Z²_{Q_l,l} + χ²_Q] and
     under (G4-dir) [finite direction family].
   * L3 `L3_sandwich.md` (C3): exchange argument on the block product γ₀: size ladder (per-block junk removal + Markov
     count over blocks), then per-element exchanges (TV in, NEG out).
   * L4 `L4_assembly.md` (C4): [OP] + M5(0) + S-T, with MR1 / production cap.
   * L5 `L5_instances.md` (C5): AR(1) exact Gram (MTP2 conditional-covariance bounds, Markov locality of residuals);
     S5 population design with fixed p (finite exact check of TV on the coded partition).
   * L6 `L6_frontier.md` (C6): random-design and growing-p factor obstruction/frontier with evidence.
4. Numerics for falsification: exact-Gram AR(1) with growing p (lattice NA max add statistic vs threshold, sandwich,
   path = deletions), S5 exact Gram p = 100 (TV computation), and the p = 400 / full-method runs.
5. Mid-point review (fresh Sol, xhigh) after L1–L3; exhaustive sweep (Sol); council (Sol high + Opus high).
6. Checkpoint 01:30 CST (CHECKPOINT.md); REPORT.md by 04:30 CST; METHOD_REQUIREMENTS.md (MR1) for C-ENG.

Fallbacks: if (G4-dir)/AR(1) fails review, keep the general theorem with (G4-χ) and the S5 fixed-p instance; if the
sandwich lemma fails, state (C4) with the sandwich as a hypothesis (as GEN did with (H2)).
