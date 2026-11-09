# R01 disposition (statement lock, Codex Sol high, verdict LOCK-WITH-CHANGES)

1. Statistics / probability space / Π / terminal index — ACCEPTED. STATEMENT v2 §3 defines v_{l|R}, τ_{l|R}, e_R, V_R,
   A_l(U), the exact identity with a_u, ψ_u (= c_u, s_u² in lemmas/L1), the enlarged space incl. r ~ χ²_{n−1−p}, Π through
   the actual ridge score with the lexicographic tie rule, indices i = 0..m₀ (terminal included). CC uses δ (size-dependent
   form CC_n(δ), introduced by the lead before the verdict, LOG 09:36) instead of c.
2. Score-level bridge obligations (a)–(e) — ACCEPTED; recorded in STATEMENT v2 §4 and discharged in lemmas/L1 §L1.4
   ((a) leakage and regularisation, (b) M_T, (c) determinant increments (L1.4.1)), lemmas/L4 §L4.4 ((d) truth moves by a
   separate signal argument; no CC needed) and L4 §L4.2 ((e) every outside null, N₀ included).
3. Positivity / genericity wording — ACCEPTED; STATEMENT v2 §2 rewritten (positivity for l, i ∉ U; zero coefficients on
   S₀ ∩ U; finitely many incidence patterns over the whole sequence with truth labels; uniform c_FS). L2.1 matches.
4. Necessity claims — ACCEPTED; §0 and (C6) now state "proposed direction, no necessity claimed"; FAC-A's sharpness is
   attributed to the full-lattice CS route only.
5. Numerical evidence — ACCEPTED. S1 relabelled as candidate-restricted search; new complete-scan certification
   numerics/s1_exh.sh → s1_exh/, S1X_summary.txt: every flip and EVERY swap pair scanned at every step, S5, p ∈ {200, 500},
   n ∈ {1e6, 1e8, 1e10, 1e12}, 3 seeds: pure null deletion ending at S₀ in 15/15, best swap ≤ chosen deletion − 0.436 log n,
   best addition ≤ −0.363 log n. Output paths cited for every numerical claim.
Optional suggestions (variable group sizes, mixed signs, N₀ ≠ ∅, truth-out swaps): l1_identities.py uses variable group
sizes and random (ρ_b, ρ_w); S4 covers N₀ ≠ ∅; truth-out swaps are scanned exhaustively in S1-EXH.
STATEMENT v2 LOCKED.
