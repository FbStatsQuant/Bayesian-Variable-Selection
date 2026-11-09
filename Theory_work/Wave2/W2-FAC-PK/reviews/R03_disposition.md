# R03 disposition (L0–L2 check, Codex Sol xhigh: VERIFIED-WITH-AMENDMENTS ×3, no fatal/major)
Reviewer reply verbatim: reviews/R03_L0L1L2_check_sol.md; scratch reviews/R03_scratch/.
1. (MINOR) L0 drift identity domain: applied ("for null j ∈ T"; not used in L1–L3).
2. (MINOR) strict ordering needs no ties: applied — 𝒟_n := {ξ_j ≠ ξ_l, j ≠ l}, P(𝒟_n) = 1, intersected in L1 (lemma),
   L2.2, L2.3, L2.4.
3. (EDITORIAL) L1 scope: applied — (a), (b) under (PK′) and blocks ≤ 16; (c), (d) add (PK), (PB); stale (TK) remark and
   pending-numerics references replaced (l12_check.py, reviewer scratch).
4. (EDITORIAL) self-test description narrowed to what is compared (start mode; move count, endpoint, move types).
Reviewer note recorded (not an amendment): the simulated n never reach the threshold t_n, so (N2) and L2.2(iii) are
supported analytically and link-by-link (l2_chain.py), not by direct occurrence.
