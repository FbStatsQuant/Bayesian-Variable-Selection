# W3-VT37R: Adversarial verification of W1-T37R

Run `git fetch origin theory/W1-T37R` and read `theory_campaign/W1-T37R/` on that branch: REPORT.md, PROOF.md (and any other proof or notes files), scripts/ and outputs.

You are an **independent referee**. Try to break the claims; don't just restate them. The claims to check: Prop 1 (literal TD unsatisfiable for d >= 1), Lemma 0 (search is F-monotone; forces 0/541 repairs), Theorem A (refined T37(i) with TD'_inf / TD'_P; move cap l >= a + d), Theorems B and C (path-wise finite-n bound with 2^{Phi(S_c)} states; asymptotics under PGD and LD), and the counterexample that SE + BM-inf do not imply PGD.

1. Check each claim line by line against the method spec `Docs/Methodology/METHODOLOGY_v3.md`, `Docs/Theory/theorems/00_COMMON.md` and the locked results it cites (`Docs/Theory/proofs/`, `COLLECTED_PROOFS_v2.tex`, `LOCKED_PROOFS.md`). For each step, record one of: VERIFIED, GAP (and whether it is fixable), or ERROR (with a counterexample).
2. Reproduce the key numerical evidence and counterexamples independently, with your own code (Python; R is not available).
3. Check that the method is modelled faithfully. Compare what the proof assumes the method does (move order, scoring, ESS/resampling rules, local search, cap K, streams) with the spec and with `Scripts/SMC_BVS/core/`.
4. **Deliverable:** `theory_campaign/W3-VT37R/REPORT.md` with a verdict table (claim | verdict | evidence), complete repairs of any GAP you can fix, and the confidence card.
