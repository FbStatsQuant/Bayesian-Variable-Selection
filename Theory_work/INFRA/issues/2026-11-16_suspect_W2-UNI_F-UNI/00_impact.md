# suspect W2-UNI:F-UNI

- reason: HQ GO real run (task S1, 2026-11-16): correctness event: every-n delivery cites Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered by the cited proof (HQ GO 11-16; Sol transfer check pending; Cor-H pattern)
- Proposition F-UNI [W2-UNI] v1.1.0 state ACTIVE; status `PROVED-CHECKED`



## Impact

- 2 direct / 4 indirect dependents; tickets: W2-UNI, W3-RM; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 6 × (1 proof session + 1 cross-family lemma check), 2 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| W2-UNI:UNI-0 | stmt | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-0 |
| W2-UNI:UNI-1 | stmt | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-1 |
| W3-RM:Examples | stmt (E-R1) | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples |
| W3-RM:RM-R | stmt (bridge [SAND(Q)], baseline rate) | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R |
| W3-RM:SAND-R | proof:UNI L2_k0 §3–§6 | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R |
| W3-RM:SAND-Rp | stmt | SUSPECT | W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp |
