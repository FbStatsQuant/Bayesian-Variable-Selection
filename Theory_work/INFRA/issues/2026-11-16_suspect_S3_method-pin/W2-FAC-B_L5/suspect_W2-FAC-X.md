# W2-FAC-X: 10 claim(s) SUSPECT after suspect of W2-FAC-B:L5

Reason: HQ GO real run (task S3, 2026-11-16): correctness event (same as W2-UNI:F-UNI, HQ 11-16): every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

- W2-FAC-X:Cor-FAC-NCS (Corollary FAC-NCS (nearly equal loadings, iid rows (R) only)) via W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:Cor-FAC-NCS
- W2-FAC-X:Thm-FAC-CS-iid (Theorem FAC-CS-iid ((C1)-(C4))) via W2-FAC-B:L5 → W2-FAC-B:Thm-FAC-CS → W2-FAC-X:Thm-FAC-CS-iid
- W2-FAC-X:Thm-FAC-GL (Theorem FAC-GL ((G1)-(G4))) via W2-FAC-B:L5 → W2-FAC-X:X10 → W2-FAC-X:Thm-FAC-GL
- W2-FAC-X:X10 (Lemma X10 (assembly (G3),(G4) for Target 2)) via W2-FAC-B:L5 → W2-FAC-X:X10
- W2-FAC-X:X6 (Theorem (X6.3/X6.4): consistency (C3) and delivery (C4)) via W2-FAC-B:L5 → W2-FAC-X:X6
- W2-FAC-X:X6.X6.3 (Theorem FAC-CS-iid (C3): (H0) on A_n, D_n->0, P(O and S+!=S0)->0, liminf P(O and S+=S0) = 1 - limsup P(U_n)) via W2-FAC-B:L5 → W2-FAC-X:X6.X6.3
- W2-FAC-X:X6.X6.4 (Delivery (C4): Proposition F's delivery extended to model R/(CS-R): P(no output)=0 and P(S+=S0)->1) via W2-FAC-B:L5 → W2-FAC-X:X6.X6.4
- W2-FAC-X:X7 (Lemma X7 (near-CS loadings, supports Cor FAC-NCS)) via W2-FAC-B:L5 → W2-FAC-X:X7
- W2-FAC-X:X8 (Lemma X8 (start mode, general loadings, (G1))) via W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:X8
- W2-FAC-X:X9 (Lemma X9 (iid-row transfer of L4r-S)) via W2-FAC-B:L5 → W2-FAC-X:X7 → W2-FAC-X:X9

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
