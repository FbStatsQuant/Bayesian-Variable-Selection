# W2-LOC2: 3 claim(s) SUSPECT after narrow of HQ_AUDIT-W1C:A2

Reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252

- W2-LOC2:F-LOC2 (Proposition F-LOC2) via HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2
- W2-LOC2:F-LOC2.exp (Delivery on the exponential-decay / block classes (D1 LOC-d, D2 LOC-BF) with polylogarithmic Q) via HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.exp
- W2-LOC2:F-LOC2.poly (Delivery on the polynomial-decay class (D3, alpha>17/2) with polynomial Q) via HQ_AUDIT-W1C:A2 → W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.poly

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
