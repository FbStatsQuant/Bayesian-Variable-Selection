# K-BC (line check of B_tail_approx.md and C_expectation.md v1, gpt-6.1-sol high) — disposition

Verdicts: B VERIFIED-WITH-AMENDMENTS, C (v1) VERIFIED-WITH-AMENDMENTS; 0 FATAL / 0 MAJOR / 3 MINOR / 1 NIT; no
counterexample to B in 2,160 enumeration draws (reviewer's scratch).

| # | finding | action |
|---|---|---|
| 1 MINOR | B Remark 1: C″_Λ(M+M′) ≠ C′_Λ | Fixed as proposed: general constant larger; exact-reference case recovers C′_Λ via the improved Step 3; Θ^T ≤ Θ″ transfer stated. |
| 2 MINOR | C: zero-tail case R_m = 0 | C v1 superseded by v2 (adopted R03b C+); the case convention is added to v2 Lemma C2. |
| 3 NIT | C v1: undefined d | Moot (the v1 χ² step is not in v2). |
| 4 MINOR | C v1 Remark 3 over-broad obstruction claim | Moot (v2 removes the e^{2√(2 log n)} factor and the remark). |

Note: C v2 (and D v2, E1 v2) are under a separate line check, K2 (`K2_v2_check_sol.md`).
