# API-T26BUD: referee-response task R5 (T26-BUDGET)

Copied verbatim from `theory/F-REFEREE:theory_campaign/F-REFEREE/RESPONSE_PLAN.md` §3, task R5. Run `git fetch origin` and read the branches it names; also read the campaign synthesis `theory/W8-SYNTH:theory_campaign/W8-SYNTH/SYNTHESIS.md` for the current state, and the open PR branch `theory/E-SPINE` (the story is now 'moving off the start is needed', not 'tempering is needed').

### R5. T26-BUDGET: Theorem 6 with a proved stage count

**Paper role:** Theorem 6's premise (M5, m15).

**Claim to prove.** On ORTH (and on FAV of W5-FAVIID if R6 verifies it), the calibration's ESS bisection rule produces a
realised stage count T_n with T_n ≤ C₁ + C₂ log(1/Δ_n) (or any bound such that (T_n + 1)Δ_n → 0 in P₀-probability);
hence (P1) holds and Theorem 6(A-i)(A-ii) follow with no premise on the run. Inputs: `v3_calib.h` (the bisection on the
ESS of e^{(φ′−φ)d}), W2-T26 Lemmas 1–3, W1-EXP Thm 1/6, W2-T26 Prop. C (ORTH). If the bound fails because the grid can
over-refine, state the weakest extra rule (e.g. a cap T^max_n = C log n) under which it holds and whether the cap is
ever active in the study (it is not: realised T ∈ {1, 2}).
**Deliverable.** `theory_campaign/T26-BUDGET/REPORT.md` with the statement, proof, and the exact p = 18 numerics
extended with the realised T_n.
