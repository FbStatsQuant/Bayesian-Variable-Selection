# W2-FAC-X: 1 claim(s) SUSPECT after suspect of W2-FAC-X:Thm-FAC-CS-iid

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-FAC-X:Cor-FAC-NCS (Corollary FAC-NCS (nearly equal loadings, iid rows (R) only)) via W2-FAC-X:Thm-FAC-CS-iid → W2-FAC-X:Cor-FAC-NCS

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
