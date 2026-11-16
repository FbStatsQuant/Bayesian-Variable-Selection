# suspect W2-FAC-B:L5

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Theorem L5.3 / L5.4 (assembly: (H0), D_n->0, delivery) [W2-FAC-B] v1.0.0 state ACTIVE; status `PROVED (by this seat, unchecked)`



## Impact

- 12 direct / 8 indirect dependents; tickets: HQ_AUDIT-W2, W2-FAC-B, W2-FAC-PK, W2-FAC-S5, W2-FAC-S5F, W2-FAC-X; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 20 × (1 proof session + 1 cross-family lemma check), 6 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W2:B3 | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS → HQ_AUDIT-W2:B3 |
| W2-FAC-B:Thm-FAC-CS | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS |
| W2-FAC-B:Thm-FAC-CS(C1-M) | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS → W2-FAC-B:Thm-FAC-CS(C1-M) |
| W2-FAC-PK:Thm-FAC-PK | proof:L5.1 (H0) and L5.4 delivery | SUSPECT | W2-FAC-B:L5 → W2-FAC-PK:Thm-FAC-PK |
| W2-FAC-S5:KL | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL |
| W2-FAC-S5:L5 | proof:L5.1, proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5:L5 |
| W2-FAC-S5:L5.C3-R | proof:L5.1 | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5:L5.C3-R |
| W2-FAC-S5:L5.C4-R | proof:L5.1, proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5:L5.C4-R |
| W2-FAC-S5:Thm-FAC-BCS-R | proof:assembly pattern | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5:Thm-FAC-BCS-R |
| W2-FAC-S5F:C4 | proof:L5.3-L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-S5F:C4 |
| W2-FAC-X:Cor-FAC-NCS | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:Cor-FAC-NCS |
| W2-FAC-X:Thm-FAC-CS-iid | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS → W2-FAC-X:Thm-FAC-CS-iid |
| W2-FAC-X:Thm-FAC-GL | stmt | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X10 → W2-FAC-X:Thm-FAC-GL |
| W2-FAC-X:X10 | proof:L5.3, proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X10 |
| W2-FAC-X:X6 | proof:L5.2, proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X6 |
| W2-FAC-X:X6.X6.3 | proof:L5.2 | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X6.X6.3 |
| W2-FAC-X:X6.X6.4 | proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X6.X6.4 |
| W2-FAC-X:X7 | proof:L5.4 | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X7 |
| W2-FAC-X:X8 | proof:general-loading rotation representation | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:X8 |
| W2-FAC-X:X9 | proof:representation paragraph | SUSPECT | W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:X9 |
