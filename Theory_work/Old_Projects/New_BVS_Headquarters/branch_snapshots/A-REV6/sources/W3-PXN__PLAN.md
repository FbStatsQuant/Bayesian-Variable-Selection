# W3-PXN working plan (run of 2026-11-02)

Family: **LH-iid(A)** = rows iid N(0, Sigma_LH) (W1-EXP linked-hub correlation: equicorrelated groups of size g,
c linked hub pairs with a suppressor coefficient, optional visible groups, null groups), p_n = G g >= n^{1+eps},
g in [floor(B/2)+1, B] (B -> 16, so 9 <= g <= 16 asymptotically). Reference S° = S0 minus the masked hubs.

Steps (each committed when done):
1. Partition lemma: blocks = groups w.p. -> 1 (sample margin argument on complete linkage, cut, next-fit).
2. SE family (SE-blk, locked SE at size m_n + s0, anchored SE of W1-T03R), R, BM-inf: sparse-eigenvalue concentration.
3. Near-truth start mass: AGG q = O_P(sqrt(log n / n)) via exact Beta laws + truncation; e = O_P(p sqrt(n) e^{-cn});
   locked T22(i) => 1 - pi0(S°) = O_P(sqrt(log n/n)).
4. Masking: exact odds identity T22(ii-a) => log pi0(S0) + c log p + (c/2) log n -> sum log((s+i)/2) + chi2_c/2.
5. Eligibility (S~0 = S°), TD' lattice condition from S° (W1-T37R Thm A), D2 hypotheses for c = 1.
6. pi(S0) -> 1 via locked T03 + design-randomisation transfer lemma.
7. Numerics: exact start law by convolution at n up to ~1600, p ~ n^{1.2}..; LS0 path; local posterior checks.
8. Study n = 200 masking: S1/S3/S4/S6 simulation, exact pi0, per-truth decomposition (weak-signal / variance inflation?).
