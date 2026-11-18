# suspect W2-FAC-X:X10

- reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W
- Lemma X10 (assembly (G3),(G4) for Target 2) [W2-FAC-X] v1.0.0 state ACTIVE; status `PROVED (by this seat, unchecked)`



## Impact

- 1 direct / 0 indirect dependents; tickets: W2-FAC-X; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 1 × (1 proof session + 1 cross-family lemma check), 1 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| W2-FAC-X:Thm-FAC-GL | stmt | SUSPECT | W2-FAC-X:X10 → W2-FAC-X:Thm-FAC-GL |
