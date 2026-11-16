# W2-UNI: 3 claim(s) SUSPECT after suspect of W2-FAC-A:Prop-F-FAC

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-UNI:F-UNI (Proposition F-UNI) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI
- W2-UNI:UNI-0 (Theorem UNI-0) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0
- W2-UNI:UNI-1 (Theorem UNI-1) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-1

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
