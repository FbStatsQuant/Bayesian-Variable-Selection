# suspect HQ_AUDIT-W1C:A2

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- A2 — Proposition F on the GROW class [HQ_AUDIT-W1C] v1.0.0 state ACTIVE; status `EXTENDS`



## Impact

- 11 direct / 20 indirect dependents; tickets: HQ_AUDIT-W1C, HQ_AUDIT-W2, W2-APP, W2-FAC-A, W2-FAC-S5, W2-FAC-S5F, W2-FAC-X, W2-LOC2, W2-UNI, W3-RM; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 31 × (1 proof session + 1 cross-family lemma check), 10 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W1C:A3 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → HQ_AUDIT-W1C:A3 |
| HQ_AUDIT-W2:B1 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → HQ_AUDIT-W2:B1 |
| HQ_AUDIT-W2:B4 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2 → HQ_AUDIT-W2:B4 |
| W2-APP:Family-map | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map |
| W2-APP:Thm-APP | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map → W2-APP:Thm-APP |
| W2-FAC-A:Prop-F-FAC | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC |
| W2-FAC-A:Thm-FAC-L | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L |
| W2-FAC-S5:KL | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL |
| W2-FAC-S5:L5 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-S5:L5 |
| W2-FAC-S5:L5.C4-R | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-S5:L5.C4-R |
| W2-FAC-S5:Thm-FAC-BCS-R | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-S5:Thm-FAC-BCS-R |
| W2-FAC-S5F:C4 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-S5F:C4 |
| W2-FAC-X:Cor-FAC-NCS | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:Thm-FAC-CS-iid → W2-FAC-X:Cor-FAC-NCS |
| W2-FAC-X:Thm-FAC-CS-iid | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:Thm-FAC-CS-iid |
| W2-FAC-X:Thm-FAC-GL | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:Thm-FAC-GL |
| W2-FAC-X:X10 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X10 |
| W2-FAC-X:X6 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X6 |
| W2-FAC-X:X6.X6.4 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X6.X6.4 |
| W2-FAC-X:X7 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X6 → W2-FAC-X:X7 |
| W2-FAC-X:X8 | proof:general-loading rotation representation | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X6 → W2-FAC-X:X7 → W2-FAC-X:X8 |
| W2-FAC-X:X9 | proof:representation paragraph | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-X:X6 → W2-FAC-X:X7 → W2-FAC-X:X9 |
| W2-LOC2:F-LOC2 | proof:FACA L7 Steps 1-3 | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2 |
| W2-LOC2:F-LOC2.exp | proof:FACA L7 Steps 1-3 | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.exp |
| W2-LOC2:F-LOC2.poly | proof:FACA L7 Steps 1-3 | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.poly |
| W2-UNI:F-UNI | proof:FACA L7 Steps 1-2 | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI |
| W2-UNI:UNI-0 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 |
| W2-UNI:UNI-1 | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-1 |
| W3-RM:Examples | stmt (E-R1) | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples |
| W3-RM:RM-R | stmt (bridge [SAND(Q)], baseline rate) | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R |
| W3-RM:SAND-R | proof:UNI L2_k0 §3–§6 | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R |
| W3-RM:SAND-Rp | stmt | SUSPECT | HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp |
