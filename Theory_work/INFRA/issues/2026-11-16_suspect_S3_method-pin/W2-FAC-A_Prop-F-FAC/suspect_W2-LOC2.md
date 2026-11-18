# W2-LOC2: 3 claim(s) SUSPECT after suspect of W2-FAC-A:Prop-F-FAC

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-LOC2:F-LOC2 (Proposition F-LOC2) via W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2
- W2-LOC2:F-LOC2.exp (Delivery on the exponential-decay / block classes (D1 LOC-d, D2 LOC-BF) with polylogarithmic Q) via W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.exp
- W2-LOC2:F-LOC2.poly (Delivery on the polynomial-decay class (D3, alpha>17/2) with polynomial Q) via W2-FAC-A:Prop-F-FAC → W2-LOC2:F-LOC2.poly

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
