# suspect W2-FAC-S5:L5.C4-R

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- (C4-R) Delivery (L5.4): P(no output)=0 and P(S+!=S0) <= P~(CC_n^c)+o(1) [W2-FAC-S5] v1.0.0 state ACTIVE; status `UNSPLIT-STATUS: PROVED-CHECKED`



## Impact

- 1 direct / 2 indirect dependents; tickets: W2-FAC-S5; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 3 × (1 proof session + 1 cross-family lemma check), 1 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| W2-FAC-S5:KL | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL |
| W2-FAC-S5:L5 | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 |
| W2-FAC-S5:Thm-FAC-BCS-R | stmt | SUSPECT | W2-FAC-S5:L5.C4-R → W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R |
