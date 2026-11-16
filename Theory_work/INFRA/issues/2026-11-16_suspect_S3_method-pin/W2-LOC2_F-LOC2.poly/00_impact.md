# suspect W2-LOC2:F-LOC2.poly

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Delivery on the polynomial-decay class (D3, alpha>17/2) with polynomial Q [W2-LOC2] v1.0.0 state ACTIVE; status `UNSPLIT-STATUS: PROVED (by this seat, unchecked)`



## Impact

- 1 direct / 1 indirect dependents; tickets: HQ_AUDIT-W2, W2-LOC2; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 2 × (1 proof session + 1 cross-family lemma check), 2 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W2:B4 | stmt | SUSPECT | W2-LOC2:F-LOC2.poly → W2-LOC2:F-LOC2 → HQ_AUDIT-W2:B4 |
| W2-LOC2:F-LOC2 | stmt | SUSPECT | W2-LOC2:F-LOC2.poly → W2-LOC2:F-LOC2 |
