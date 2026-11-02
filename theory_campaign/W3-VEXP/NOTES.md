# W3-VEXP working notes (referee of W1-EXP, origin/theory/W1-EXP @ fetched 2026-11-02)

Sources checked: W1-EXP REPORT.md, PROOF.md, scripts/, results/; METHODOLOGY_v3.md §§5-6.3, 6.10;
00_COMMON.md; T22 STATEMENT (wave 1), T22iii STATEMENT + PROOF_v2.tex, T27i STATEMENT, T03 STATEMENT;
LOCKED_PROOFS.md; engine Scripts/SMC_BVS/core/cpp/{v3_score.h, v3_blocks.h, v3_start.h};
Scripts/Data_generators/gen_dev_data.R.

## Step 1 (paper check, first pass)
- Lemma 1.1 (Q_S vs RSS): VERIFIED. Q = (n-1-t) + t/(n+1) + n tau/(n+1); tau <= eps/phi^2.
- Lemma 1.2 (determinant ratio): VERIFIED. Schur formulas for H and G+I correct; alpha_1, alpha_2 ranges correct;
  |log((rho+a1)/(rho+a2))| <= |a1-a2|/rho with rho >= phi^2(n-1).
- Lemma 1.3: VERIFIED (exact identity; bound uses the larger of two nonneg logs).
- Lemma 1.4 (RSS floor): VERIFIED. (C-P_W) = (C-P_W)(C-P_U); E exp(chi2_k/4)=2^{k/2}; union over <= 2^16 p pairs.
- Thm 1: VERIFIED as a composition. Form of EXP' identical to T22iii STATEMENT §2 and T27i optional EXP'.
- Engine check: v3_score.h logm = logCn - 0.5(logdet H - logdet(G+I)) - nu log(2b0+Q), Q = y'y - n z'H^{-1}z;
  tables r_b(U) = m(U)/m(empty) on full y (v3_start.h build_tables); gamma0 = varpi(|S|) prod r_b. Matches spec.

## Step 2-4 log (summary; details in REPORT.md / REPAIRS.md)
- Independent code: vcore.py (scores, engine-partition port, exact pi0/pi), sanity.py (all checks pass).
- LH reproduction (explicit Gram designs + iid designs): agrees with W1 to ~2 decimals.
- Boundary tests: psi >= rho makes pi0(S°) e^{-Theta(n)} (hub pair forms its own block); 2g <= B removes masking.
- Study-scale: SE-blk and population leakage reproduce W1; EXP' actual max|R| <= 0.145, certificate <= 1.52, kappa_EXP ~ 100-1700.
- Start at n=200 is dilution-masked (all scenarios, all c); favourable by n ~ 800-1600 (S3, p=500). Prop D ceiling >= exact in 26/26.
