# suspect W2-FAC-A:Prop-F-FAC

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Proposition F-FAC (claim (D)) [W2-FAC-A] v1.0.0 state ACTIVE; status `PROVED (by this seat, unchecked)`



## Impact

- 6 direct / 9 indirect dependents; tickets: HQ_AUDIT-W2, W2-APP, W2-FAC-A, W2-LOC2, W2-UNI, W3-RM; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 15 × (1 proof session + 1 cross-family lemma check), 6 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W2:B1 | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → HQ_AUDIT-W2:B1 |
| HQ_AUDIT-W2:B4 | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2 → HQ_AUDIT-W2:B4 |
| W2-APP:Family-map | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map |
| W2-APP:Thm-APP | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map → W2-APP:Thm-APP |
| W2-FAC-A:Thm-FAC-L | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L |
| W2-LOC2:F-LOC2 | proof:FACA L7 Steps 1-3 | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2 |
| W2-LOC2:F-LOC2.exp | proof:FACA L7 Steps 1-3 | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.exp |
| W2-LOC2:F-LOC2.poly | proof:FACA L7 Steps 1-3 | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.poly |
| W2-UNI:F-UNI | proof:FACA L7 Steps 1-2 | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI |
| W2-UNI:UNI-0 | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 |
| W2-UNI:UNI-1 | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-1 |
| W3-RM:Examples | stmt (E-R1) | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples |
| W3-RM:RM-R | stmt (bridge [SAND(Q)], baseline rate) | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R |
| W3-RM:SAND-R | proof:UNI L2_k0 §3–§6 | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R |
| W3-RM:SAND-Rp | stmt | SUSPECT | W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp |
