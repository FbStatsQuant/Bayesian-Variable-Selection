# W3-PGD: The asymptotic hypotheses of the refined T37 (PGD and LD)

W1-T37R (branch `theory/W1-T37R`, folder `theory_campaign/W1-T37R/`) proved several things:
- the literal TD is unsatisfiable for d ≥ 1;
- the refined T37(i) holds under TD′ (Theorem A);
- a path-wise finite-n bound (Theorems B and C), whose asymptotics need two extra hypotheses: **PGD** (population greedy dominance) and **LD** (local dependence of nulls).

It also gave a counterexample: SE + BM-∞ do not imply PGD (a "combination look-alike"). W1-T38E independently found that greedy still repairs in proxy-rich designs, and recommends TD′ as the black-box repair input.

**Goal:**
1. Find the weakest natural, checkable design condition that implies PGD. Candidates: a restricted-isometry / irrepresentable-type condition on 𝓡_d, a bound on combination leakage, or a block-local condition matching the start partition. Prove PGD from it.
2. Do the same for LD, or show it can be dropped, for example via a chaining or union bound over the 2^{Φ} lattice states only.
3. Check whether the study's correlated scenarios S2–S6 (as designs; reimplement the generators from `Scripts/Data_generators/` in Python) satisfy your condition at the population level and at n = 200. Compute the greedy path's margins.
4. Give the resulting clean asymptotic theorem: TD′ holds w.p. → 1 under G, R, (anchored) SE, BM-∞ and your condition. Write it with a full proof.

**Deliverable:** `theory_campaign/W3-PGD/REPORT.md` with statements, proofs, numerics and the confidence card.
