# R08 disposition (exhaustive sweep, Codex gpt-6.1-sol xhigh): fatal 0, major 0, minor 9, editorial 7 — all fixed
1. S5 certificate covariance formula (θ_j + 0.3Σ_{k≠j}θ_k = 0.7θ_j + 0.3Σ_kθ_k) — fixed in L5(b) (the script already used the correct form).
2. (C5)(c) noise model: Y = Xθ* + Cε, ε ~ N(0, σ²I) independent of the raw design; y = Y/(‖Y‖/√(n−1)) in the score — fixed in STATEMENT.
3. Factor-design growth claim → finite observation (median start sizes 23, 43, 74 at p = 100, 200, 400; c = 1, n = 3200; numerics/D2_summary.md:30,36,41) + conjecture label — fixed.
4. p = 400 MR1 evidence: scored 47/47, reached 45/47 (all 27 at n ≥ 800) — fixed.
5. Python-port conventions (tie tolerances, enumeration cap, zero truncations) disclosed; "production" reserved for R-core runs (D4) — fixed in STATEMENT §0 and L5(b).
6. f2_exact_tau0.py now computes and prints the partition; F2_exact_tau0.txt regenerated (consecutive blocks: True) — fixed.
7. Stale SUMMARY_DIAG.md: STATEMENT now cites the current individual D1/D2/D3 summaries — fixed.
8. Frontier now mentions S5 NA failures in 10/20 runs at n = 12800 — fixed.
9. Minimal hypothesis list for L2/(C2) — fixed (STATEMENT (C2), L2 header).
10. S2 denominators 120/120 (n ≥ 800) vs 160/160 (incl. n = 200) — fixed.
11. L6 stale "unchecked / checking still required" prose — replaced by the check record and incorporation note.
12. Review-file paths added to every check record (00_MAIN table and lemma headers).
13. GEN's 2^{v̄} − 1 described as a sufficient upper bound — fixed (00_MAIN, L4 note 5).
14. G1_summary.md source header corrected (G1_raw.csv, G1_raw_p800.csv; no p = 4000 file).
15. L0.2 heading "Three consequences" — fixed.
16. STATEMENT §1 defines C, D_x, P_T (P_∅ = 0), π — fixed.
