# W2-FAC-S5: 2 claim(s) SUSPECT after suspect of W2-FAC-S5:L5

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-FAC-S5:KL (Lemma KL (claim (C5)): P~(CC_n(delta)) -> 1) via W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R → W2-FAC-S5:KL
- W2-FAC-S5:Thm-FAC-BCS-R (Theorem FAC-BCS-R (reduction): (C1), (C2-R), (C3-R), (C4-R)) via W2-FAC-S5:L5 → W2-FAC-S5:Thm-FAC-BCS-R

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
