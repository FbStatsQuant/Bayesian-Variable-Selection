# R07 disposition (exhaustive sweep, Codex gpt-6.1-sol xhigh): 0 fatal, 2 major, 11 minor, 4 editorial — all fixed

1. MAJOR model identification — FIXED: STATEMENT §1 G now defines C, D_x, X = CX^rD_x⁻¹, θ* := D_xβ, μ := CX^rβ = Xθ*,
   Y := Cy^r = μ + Cε, y = Y/s (as GEN/STATEMENT.md:29-30).
2. MAJOR blanket saturation claim — FIXED: STATEMENT §0, (C5)(a) and METHOD_REQUIREMENTS state saturation only as the N2
   observation (with layout, N₀ = ∅); general saturation not claimed (p − |N₀| < K possible).
3. Partition scope — FIXED: statistical claims for every partition with blocks ≤ 16 at indices with K = p; (C4) for the
   specified method's partition (B ≤ K).
4. "reaches" vs "terminates" — FIXED in STATEMENT §1.
5. Redundant b ≤ 0 subcase in L4 (B1) — DELETED (b ≥ (1 − 3ε_b)H > 0 already).
6. Small-regime summary — FIXED (O(log(p + 1) + L_n²), small fixed multiple of log n; onset at indices with p ≤ ⌊n/2⌋).
7. Caps below ℓ_n — FIXED: nonnegative integer caps; single-search prefix property from CAP's loop rule (L3), valid for
   every cap; CAP's integration statement only for a ≥ ℓ_n (STATEMENT §1, (C2); L4.5 remark 1).
8. L2's N1 description — FIXED (exceptions at n = 10⁶ listed).
9. cs_selftest description — FIXED in L1 (endpoint and move count only).
10. N2 final-scan description — FIXED (last centre 4 extras, returned neighbour 3 extras) in N2_summary and METHOD_REQUIREMENTS.
11. N3 NA maximum — FIXED (−0.237 over n ≥ 10⁵; −0.0136 over all runs).
12. N5 centre_err description — FIXED (0/1 indicator).
13. N1 "moves − symdiff" label — FIXED.
14. κ₀ clash — FIXED: L1's common z-component renamed κ_c; L4's limit renamed κ_∞; λ_θ = λ₁/κ₁ stated.
15. ϑ indexing — FIXED: ordered support map i_r(n), ϑ_{i_r(n)} := ϑ_r.
16. (C1) event qualifier — FIXED ("On this event").
17. "Not claimed" vs (C4) — FIXED (finite-n statistical bounds excluded; the ideal-machine P(no output) = 0 retained).
STATEMENT → v3.1 (logged; no conclusion strengthened except the flagged hypothesis-weakening (C1-M)).
