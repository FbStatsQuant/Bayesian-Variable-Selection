# W2-VT03R working notes (REPORT.md is the deliverable)

Referee run on W1-T03R (branch theory/W1-T03R, commit fetched 2026-11-02).
Locked proofs: [P1] Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex,
[P3] Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex.

## step 0 — read PROTOCOL, task, W1 REPORT/PROOF, [P1], [P3]

## step 1 — W1 scripts rerun: tail_bound, duplicate_counterexample, proof_n0, bm_constants outputs byte-identical.
## step 2 — scripts/verify_E1_exact.py (independent, exact rationals): E1(a)-(d) on 2779 triples PASS; E2(i)-(iii) on 129 PASS;
   W1 threshold table reproduced exactly (m_old, m#, uncapped m#; first n below K: 342 vs 464). The "65-100" saving claim
   refers to p=500 rows in W1's raw output (not in its REPORT table) -> consistent.
## Observation (task 3): by Cauchy interlacing, anchored SE_w(m) <=> lambda_min(G_T) >= g0 for EVERY nonempty T with |T \ S0| <= m
   (T is a subset of S0 u (T\S0)). Same for SE_lambda(j0). So "anchoring" only buys s0 extra columns; the real weakenings are
   (1) normalised -> unnormalised for large sets, (2) size m_n -> m#, (3) normalised only up to j0.
## step 3 — scripts/propD_independent.py: Prop D reproduced (brute-force m(S) == closed form to 1e-13; bound holds on E_n
   108/108 small-n incl. adversarial y; P(E_n)=1, bound 100% at n up to 2e5; cutoffs 4/6/8/9). Constant 0.25157>=1/4 (margin 0.0016).
## Idea to check: SE_lambda(j0) normalised is needed ONLY in lem:signal; cor:diff lower half and ongood(c) work with g0 (rho_n -> O(1) const).
## step 4 — scripts/check_deterministic.py: B3, C6a (crude, no eigen), B1, eq:score identity, proposed OGc'/CDl' variants,
   den' and the T02(i#) pointwise chain on B_n: all hold on 60 random small designs (iid/equi/near-collinear), exhaustive over models.
## step 5 — scripts/proof_thresholds.py: W1 proof_n0 claim "other thresholds bind earlier" is FALSE.
   q_n <= 1/2 ([P3] prop:sup(b), geometric series) first holds n ~ 2.12e6 (A=1.17, m#) / 2.46e6 (A=1.30);
   e^{2 eps_n} <= 4 (W1 (C5)(b)) first holds n ~ 2.56e7 / 2.98e7.  delta_n<=1/2 (W1's binding): 1.15e5 / 1.30e5.
   -> REPORT/disclosure "deterministic thresholds from n ~ 1e5" should read ">= 2e6 (as written)". Direction: strengthens the disclosure.
