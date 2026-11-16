# W3-RM: 4 claim(s) SUSPECT after narrow of W2-FAC-A:Prop-F-FAC

Reason: HQ GO real run (task S4, 2026-11-16): batch NARROW (A:IDEAL-W⁺ / bounded domain 𝔇), correctness event (same as W2-UNI:F-UNI): every-n delivery under plain IDEAL-W not covered (validators le ≤ 10⁶, ℓ+|S̃₀| ≤ INT_MAX). Statement-change check Theory_work/Dept/research/IDEALW_BATCH/DIFF2_sol.md@46e58252 (Sol DIFF PASS, WEAKER); patches Theory_work/Dept/research/IDEALW_BATCH/patches/@46e58252

- W3-RM:Examples ((C4) Examples table) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples
- W3-RM:RM-R ((C2) Theorem RM-R (Gaussian rows, polylogarithmic Q)) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R
- W3-RM:SAND-R (Lemma SAND-R (abstract Gaussian-row sandwich, baseline rate n^{-2})) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R
- W3-RM:SAND-Rp (Lemma SAND-R′ (slower localisation rate r_n)) via W2-FAC-A:Prop-F-FAC → W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
