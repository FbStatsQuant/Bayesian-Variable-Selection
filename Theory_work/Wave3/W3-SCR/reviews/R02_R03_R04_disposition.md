# Dispositions: R01b (re-lock), R02 (better theorem), R03 (lemma check L1-L4), R04 (lemma check L5-L6)

All four reports are verbatim in this folder (written by the reviewers). R03 and R04 were run on the v2 lemma files;
their reports were completed before the T3 server restart.

## R01b — statement re-lock of v2 (gpt-6.1-sol high): **LOCK**
No blocker/major. Optional sentence on retained-column indexing: added to STATEMENT §0.

## R02 — "better theorem" review (gpt-6-astra high): strictly better provable statements exist
| # | Proposal (class) | Disposition |
|---|---|---|
| 1 | Geometric noise complexity (Gaussian width) instead of model count (1) | **Adopted**: b_𝓗(x), c_𝓗(x) in the master theorem SCR-M (L7); M6. |
| 2 | Exact addition threshold, model-specific residual scales, deterministic families (1) | **Adopted** as SCR-M: per-model deterministic gap δ_S (exact prior/determinant penalty B_S, residual bound Ū_S). SCR-A and SCR-A° are special cases (M3); their checked direct proofs are kept. Size-wise peeling (x_k) not adopted (cosmetic). |
| 2f / 4 | Scanned centres near the best score screen even without a certificate (1) | **Adopted**: M2; extended by the lead to capped searches and to "the search does not drop truths" (M5), with the order-n gap M4; printed form = Corollary SCR-G. New code fact CC6. |
| 3 | Excess-set characterisation with exact penalties and dual geometry (1) | **Adopted in the log-linear form**: L5.1 now gives (EC′) in terms of α(S), ω(S); (EC) with the floor φ is the special case. The exponential form (E*) is not used (constants only). The asymptotic (α, ω) theorem is **not** claimed (see R04 finding 1). |
| 5 | Directional restricted curvature instead of the anchored floor (1) | **Adopted**: φ^d_n(q) (B2d); A1, A1° stated with φ^d. |
| 6 | Quadratic contrasts for all legal moves incl. swaps at |S| = K (1 as a theorem, 2 as a useful primitive result) | **Not adopted**: abstract matrix condition (Q) without a primitive corollary; recorded as an open direction in REPORT (it is the route to |Ŝ| = K and to truths masked by a proxy). The claim "K is excluded by construction" was reworded (it is an addition-only argument). |
| g | Overstated headings (A1° rate, "no bound on total signal"), SCR-N scope, SCR-R prediction bound without floor, ω remark | **All fixed** (STATEMENT v3; L3, L5, L6). |
| 8 | Rejected shortcuts (counting adaptive endpoints; certificate inheritance by unscanned near ties) | Agreed; nothing in the package uses them. M5 covers the one unscanned model that can be handled (the capped search's returned neighbour), by a proof, not by inheritance. |

## R03 — lemma check L1-L4 (gpt-6.1-sol high): all 27 items CORRECT (2 with minor fix); no blocker/major
| # | Finding | Disposition |
|---|---|---|
| 1 | MINOR: E3b needs x′ > 0 stated | Fixed (L2). |
| 2 | MINOR: A1° heading overstated the rate | Fixed (L3, STATEMENT): rate σ√(𝐋_n/n); "no fixed bound on the total signal". |
| 7 | NOTE: zero-variance Gaussian convention | Convention sentence added to L2. |
| others | NOTES: independent derivations agree (T_n, 1.02, n/(n+1), 3e^{-x}/4e^{-x}, c₁, 16/576, 4/9) | — |

## R04 — lemma check L5-L6 (gpt-6.1-sol high): no blocker in the claimed results
| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | MAJOR (unclaimed remark) | The ω-only replacement of the floor in the L5 remark is false (counterexample with nearly collinear excess pair: ω ≤ 2 but determinant penalty O(1)) | **Fixed**: remark deleted; L5.1 restated with both α(S) (conditional lengths) and ω(S); the new remark cites the counterexample and claims no (α, ω) asymptotic theorem. |
| 2 | MINOR | "‖θ*‖₂ = O(√n)" should be relative to σ | Fixed (L5). |
| 3 | MINOR | SCR-R must allow the SCR-A° event | Fixed (L5). |
| 4 | MINOR | Lower bound of B_n needs the case u_n ≥ 2 | Fixed (L6); upper bound sharpened to B_n ≤ L_n. |
| 5 | MINOR | Consequence 2: rate (log n)²/n, not 1/n | Fixed (L6). |
| 6 | MINOR | "the square cannot be dropped" not shown by the sequence | Fixed (L6): claim restricted; scaling argument added. |
| 7 | NOTE | pair formula needs the augmented partial correlation | Fixed (L5 fact (c)). |

Next: R05 (fresh, gpt-6.1-sol high) checks the v3 deltas line by line (L7 new; L5 rewrite; B2d; L6/L2/L3 edits; CC6)
and re-locks STATEMENT v3; then mid-point, sweep, council.
