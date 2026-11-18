# W2-FAC-S5: 1 claim(s) SUSPECT after narrow of W2-FAC-S5:Thm-FAC-BCS-R

Reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252

- W2-FAC-S5:KL (Lemma KL (claim (C5)): P~(CC_n(delta)) -> 1) via W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
