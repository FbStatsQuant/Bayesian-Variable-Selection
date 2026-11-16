# HQ_AUDIT-W2: 1 claim(s) SUSPECT after suspect of W2-LOC2:F-LOC2.poly

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- HQ_AUDIT-W2:B4 (B4_loc2_redteam.md) via W2-LOC2:F-LOC2.poly → W2-LOC2:F-LOC2 → HQ_AUDIT-W2:B4

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
