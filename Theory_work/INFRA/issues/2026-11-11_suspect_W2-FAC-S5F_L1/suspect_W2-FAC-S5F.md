# W2-FAC-S5F: 4 claim(s) SUSPECT after suspect of W2-FAC-S5F:L1

Reason: API audit pass3 GAP confirmed by Sol R-AUD2 (Wave3/API_AUDIT/pass3/R-AUD2_sol.md); local repairs specified; stopped ticket, repair not scheduled

- W2-FAC-S5F:C1 (Claim (C1) start mode) via W2-FAC-S5F:L1 → W2-FAC-S5F:C1
- W2-FAC-S5F:C2 (Claim (C2) bulk theorem (unconditional, every p<=n/2)) via W2-FAC-S5F:L1 → W2-FAC-S5F:C2
- W2-FAC-S5F:C3 (Claim (C3) end phase (conditional on (CC_theta))) via W2-FAC-S5F:L1 → W2-FAC-S5F:C3
- W2-FAC-S5F:C4 (Claim (C4) consequences) via W2-FAC-S5F:L1 → W2-FAC-S5F:C4

For each: re-check the step that uses the upstream claim. PATCH if it survives (`propagate.py clear <id>`), otherwise narrow / retract and propagate.
