# narrow W2-UNI:UNI-0

- reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252
- Theorem UNI-0 [W2-UNI] v1.1.3 state SUSPECT; status `PROVED-CHECKED, conditional on SOP:TH05.0`



## Impact

- 2 direct / 2 indirect dependents; tickets: W3-RM; headlines: —; paper blocks: 0 (regeneration by assemble.py is free)
- re-proof + re-review: 4 × (1 proof session + 1 cross-family lemma check), 1 × 1 exhaustive sweep, 0 × 1 council (2 reviewers) + 0 × 1 strength gate (lit + necessity + better-theorem review)

| dependent | uses | becomes | path |
|---|---|---|---|
| W3-RM:Examples | stmt (E-R1) | SUSPECT | W2-UNI:UNI-0 → W3-RM:Examples |
| W3-RM:RM-R | stmt (bridge [SAND(Q)], baseline rate) | SUSPECT | W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R |
| W3-RM:SAND-R | proof:UNI L2_k0 §3–§6 | SUSPECT | W2-UNI:UNI-0 → W3-RM:SAND-R |
| W3-RM:SAND-Rp | stmt | SUSPECT | W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp |
