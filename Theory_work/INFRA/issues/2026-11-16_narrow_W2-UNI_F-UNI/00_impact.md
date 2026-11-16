# narrow W2-UNI:F-UNI

- reason: HQ GO real run (task S2, 2026-11-16): NARROW of F-UNI, correctness event. Every-n delivery cited Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered (TR1: transfer NO, Theory_work/Dept/research/FUNI_transfer/TR1_sol.md). Narrowed: (a) delivery under IDEAL-W on the bounded domain 𝔇; (b) every n and P(Ŝ⁺ = S₀) → 1 under A:IDEAL-W⁺. Statement-change check Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md@fc30c749 (Sol DIFF PASS, WEAKER, 1.1.0 -> 2.0.0). Clear to 2.1.0 in S4 with W2-FAC-A:Prop-F-FAC (manager 11-16).
- Proposition F-UNI [W2-UNI] v1.1.0 state SUSPECT; status `PROVED-CHECKED`



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
