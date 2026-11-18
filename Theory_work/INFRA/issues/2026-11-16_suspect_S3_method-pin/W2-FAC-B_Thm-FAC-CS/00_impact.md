# suspect W2-FAC-B:Thm-FAC-CS

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Theorem FAC-CS ((C1) start mode, (C2) path lemma, (C3), (C4) delivery) [W2-FAC-B] v1.0.0 state ACTIVE; status `PROVED-CHECKED`



## Impact

- 3 direct / 1 indirect dependents; tickets: HQ_AUDIT-W2, W2-FAC-B, W2-FAC-X; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 4 × (1 proof session + 1 cross-family lemma check), 3 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| HQ_AUDIT-W2:B3 | stmt | SUSPECT | W2-FAC-B:Thm-FAC-CS → HQ_AUDIT-W2:B3 |
| W2-FAC-B:Thm-FAC-CS(C1-M) | stmt | SUSPECT | W2-FAC-B:Thm-FAC-CS → W2-FAC-B:Thm-FAC-CS(C1-M) |
| W2-FAC-X:Cor-FAC-NCS | stmt | SUSPECT | W2-FAC-B:Thm-FAC-CS → W2-FAC-X:Thm-FAC-CS-iid → W2-FAC-X:Cor-FAC-NCS |
| W2-FAC-X:Thm-FAC-CS-iid | stmt | SUSPECT | W2-FAC-B:Thm-FAC-CS → W2-FAC-X:Thm-FAC-CS-iid |
