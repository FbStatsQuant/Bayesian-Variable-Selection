# R02 disposition (L1–L3 check, Codex Sol high): L1 FAILED as written; L2, L3 VERIFIED-WITH-AMENDMENTS

1. MAJOR (leakage rate) — ACCEPTED. L1.4 now gives the exact three-term ε_j and the bound
   |ε_j| ≤ C_d[(1 + |τ| + G_n)k/n² + √k/n^{3/2}]; L3 (c4) corrected to C_d[(…)p/n² + √p/n^{3/2}] ≤ n^{−1/2} for
   p ≤ n^α, α < 1. Downstream: L4 uses only |ε| ≤ n^{−1/2} (L4.2.1) — unaffected. New check numerics/l1_leak.py →
   l1_leak_out.txt: exact identity t̃ = (σ√(n−1)/s)(τ + ε) to relative 7e−12; n^{3/2}·(leakage term) bounded (≈ 0.008).
2. MAJOR (multiplier needs sublinear p) — ACCEPTED. L3 (c1) split: s² bounds for p ≤ n/2; (c1′) M_T = ½(1 + η_T)
   only for p ≤ n^α, α < 1 (used only by L4 under (P_α)); L2 does not use (c1′).
3. MINOR (determinant increment; positive-pair denominator) — ACCEPTED. L2.2(i) now has the explicit √(1 + 1/a) divisor
   and the exact Schur identity L(U ∪ l) − L(U) = log(n + 1) + log[s(1/a)/s(1/a′)] ≤ log(n + 1) (s′ > 0).
4. MINOR (numerical claims) — ACCEPTED. L1 status line: selftest = every flip and the best exhaustive swap gain, tolerance
   9e−7; l1_identities tests L1.3 only (score_tau unused); leakage evidence from l1_leak.py.
With these amendments L1 is repaired (re-verification by the mid-point/sweep reviewers).
