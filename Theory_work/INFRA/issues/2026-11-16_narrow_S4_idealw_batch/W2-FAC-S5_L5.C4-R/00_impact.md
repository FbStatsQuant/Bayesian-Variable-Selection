# narrow W2-FAC-S5:L5.C4-R

- reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252
- (C4-R) Delivery (L5.4): P(no output)=0 and P(S+!=S0) <= P~(CC_n^c)+o(1) [W2-FAC-S5] v1.0.0 state SUSPECT; status `UNSPLIT-STATUS: PROVED-CHECKED`



## Impact

- 1 direct / 2 indirect dependents; tickets: W2-FAC-S5; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 3 × (1 proof session + 1 cross-family lemma check), 1 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| W2-FAC-S5:KL | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL |
| W2-FAC-S5:L5 | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 |
| W2-FAC-S5:Thm-FAC-BCS-R | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R |
