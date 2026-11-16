# W2-APP: 2 claim(s) SUSPECT after narrow of W2-FAC-A:Prop-F-FAC

Reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252

- W2-APP:Family-map (Family map (L4_families v2)) via W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map
- W2-APP:Thm-APP (W2-APP applicability map (target as a whole)) via W2-FAC-A:Prop-F-FAC → W2-FAC-A:Thm-FAC-L → W2-APP:Family-map → W2-APP:Thm-APP

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
