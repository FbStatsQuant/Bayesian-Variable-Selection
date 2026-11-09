# R01 disposition (statement lock, Codex gpt-6.1-sol high: REJECT)

1. **Swap margin false (analytic counterexample, p = 3).** ACCEPTED. (C2)(ii) now claims only that every null-out swap
   and every other null deletion has gain strictly below the chosen deletion's gain; the −c log n margin is kept for
   additions only (the re-addition of a deleted null loses at least the deletion gain), truth moves are negative.
   Numerics: cs_gain.py now records the best swap gain relative to F(T) (max_swap_gain); on test runs it is ≈ −10⁻⁵,
   confirming that swaps are nearly score-neutral early on the path.
2. **Define invariants; address end phase, N0, k ~ n/2; exact BB ratio and RSS.** ACCEPTED. §3 defines ξ, x_T, ϱ_n, κ_n,
   a_T, b_T; (C2)(iii) states the rank interval with the pre-move centre. L4 handles: s₀ = 1 and ρ near 1 (end-phase margin
   c_D = ½ − 1/(s₀ + 1 + κ₀) > 0), the last extras (end-phase imbalance analysis), N₀ coordinates (outside candidates with
   |ξ| ≤ L_n), k up to n/2 (multiplier bound M_T ≤ 1 + n^{−1/4} from r ≥ (n − 1 − p)(1 − n^{−1/3}), i.e. the actual residual
   dimension), exact Δ_k with log[(2p − k)/k]. No small-set expansion from GEN/GROW is used: L1 gives exact closed forms
   for every set size.
3. **FS wording; L2 obligations; H0 only; rename sign matrix.** ACCEPTED. FS stated as sufficient; c(U, l) displayed;
   L2 treats positive pairs (order-n increments vs order-log p prior cost, uniform sample error) and the zero pairs of the
   truth-complete block (noise-only increments, finitely many) separately, and includes truths before concluding. The
   relevance-set sentence is replaced by the (H0) claim and an explicit "not satisfied" remark. Sign matrix renamed Υ_n.
4. **C4 framing.** ACCEPTED. (C4) is stated as a new class extension, CAL-free, with all of Proposition F's premises and
   amended allocation including the LS0 preflight terms; discovery via 𝒦_n and D′'s pathwise inclusion, not via D_n.
5. **Scope/frontier wording.** ACCEPTED. "Targeted for proof"; name FAC-CS; p ≫ log n identified as the substantive
   regime; the N1 full-start sentence corrected (F2 p = 200 c = 0.5 and S5 p = 400 c = 0.5 at n = 10⁶ are not full);
   N2 described as one data set; obstructions labelled as obstructions to the technique.
6. **Search/branch contract.** ACCEPTED. §1 defines ℓ_n, the extra scan, scored set, both tie rules, certified search
   endpoint (not the public flag), the exact-branch convention; ℓ_n called the legacy cap.
7. **Diagnostic fidelity.** ACCEPTED. cs_gain.py and cs_core.py now implement the lexicographic tie rule (smallest
   resulting set) among all best-gain neighbours and count ties; cs_selftest rerun (cs_selftest_out.txt, 4/4 agree).
   N3/N5 runs recorded 0 ties (tie-free; the rule change cannot affect them); N3 results are cited only for what they test
   (pure deletion, final set, rank-interval contiguity, best-swap-minus-best-deletion); the revised (C2)(ii) is exactly
   best-swap-minus-best-deletion < 0, which N3 records.
