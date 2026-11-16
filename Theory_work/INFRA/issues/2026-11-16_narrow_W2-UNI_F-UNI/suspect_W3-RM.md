# W3-RM: 4 claim(s) SUSPECT after narrow of W2-UNI:F-UNI

Reason: HQ GO real run (task S2, 2026-11-16): NARROW of F-UNI, correctness event. Every-n delivery cited Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered (TR1: transfer NO, Theory_work/Dept/research/FUNI_transfer/TR1_sol.md). Narrowed: (a) delivery under IDEAL-W on the bounded domain 𝔇; (b) every n and P(Ŝ⁺ = S₀) → 1 under A:IDEAL-W⁺. Statement-change check Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md@fc30c749 (Sol DIFF PASS, WEAKER, 1.1.0 -> 2.0.0). Clear to 2.1.0 in S4 with W2-FAC-A:Prop-F-FAC (manager 11-16).

- W3-RM:Examples ((C4) Examples table) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:Examples
- W3-RM:RM-R ((C2) Theorem RM-R (Gaussian rows, polylogarithmic Q)) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:RM-R
- W3-RM:SAND-R (Lemma SAND-R (abstract Gaussian-row sandwich, baseline rate n^{-2})) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R
- W3-RM:SAND-Rp (Lemma SAND-R′ (slower localisation rate r_n)) via W2-UNI:F-UNI → W2-UNI:UNI-0 → W3-RM:SAND-R → W3-RM:SAND-Rp

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
