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
