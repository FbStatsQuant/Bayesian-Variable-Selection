# W2-FAC-B: 2 claim(s) SUSPECT after suspect of W2-FAC-B:L5

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-FAC-B:Thm-FAC-CS (Theorem FAC-CS ((C1) start mode, (C2) path lemma, (C3), (C4) delivery)) via W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS
- W2-FAC-B:Thm-FAC-CS(C1-M) ((C1-M) Masked truths (Corollary M)) via W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS → W2-FAC-B:Thm-FAC-CS(C1-M)

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
