# suspect W2-FAC-A:Thm-FAC-L

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Theorem FAC-L (Part I: (L1)-(L5), delivery (D), instances (I)) [W2-FAC-A] v1.0.0 state ACTIVE; status `PROVED-CHECKED`



## Impact

- 2 direct / 1 indirect dependents; tickets: HQ_AUDIT-W2, W2-APP; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 3 × (1 proof session + 1 cross-family lemma check), 2 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W2:B1 | stmt | SUSPECT | W2-FAC-A:Thm-FAC-L → HQ_AUDIT-W2:B1 |
| W2-APP:Family-map | stmt | SUSPECT | W2-FAC-A:Thm-FAC-L → W2-APP:Family-map |
| W2-APP:Thm-APP | stmt | SUSPECT | W2-FAC-A:Thm-FAC-L → W2-APP:Family-map → W2-APP:Thm-APP |
