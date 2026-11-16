# W3-RM: 4 claim(s) SUSPECT after suspect of W2-UNI:F-UNI

Reason: HQ GO real run (task S1, 2026-11-16): correctness event: every-n delivery cites Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered by the cited proof (HQ GO 11-16; Sol transfer check pending; Cor-H pattern)

- W3-RM:Examples ((C4) Examples table) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples
- W3-RM:RM-R ((C2) Theorem RM-R (Gaussian rows, polylogarithmic Q)) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R
- W3-RM:SAND-R (Lemma SAND-R (abstract Gaussian-row sandwich, baseline rate n^{-2})) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R
- W3-RM:SAND-Rp (Lemma SAND-R′ (slower localisation rate r_n)) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
