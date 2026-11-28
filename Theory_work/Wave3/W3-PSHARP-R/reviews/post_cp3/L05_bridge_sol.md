BRIDGE B3.8: GAP

[S] BRIDGE_orth_thm1.md:22-23 (also :35-36): The claimed dependence only on s₀ and θ* omits the noise variance σ*², which the proof itself lists among Theorem 1’s parameters. The setting does not specify its value. Exact fix: state that σ*² > 0 is fixed and allow C and n₀ to depend on (s₀, θ*, σ*²). The displayed lower constants need no change.

[E] BRIDGE_orth_thm1.md:4-6, :19-20, :46-47: The pinned reader sources are unavailable as working files: Theory_work/Wave3/W3-READER/READER_VERSIONS.md and NOTATION.md are absent. The brief requests git show but both the user and brief prohibit git operations; none were performed. Consequently the exact (S1)/(S2), (A1)–(A6), Theorem 3(b), notation, and Theorem 2 conclusion could not be independently checked against e20d287f. Exact fix: supply the two pinned source texts as readable files within the worktree, then complete these checks. GAP denotes this unresolved verification dependency, not a demonstrated false theorem.

[C] BRIDGE_orth_thm1.md:28-29: The universal assertion includes S = ∅, whose minimum eigenvalue is undefined under ordinary conventions. Exact fix: say “for every nonempty S ⊆ [p]” as in the following A5 check, or explicitly state the empty-set convention.

[F] BRIDGE_orth_thm1.md:37-43: The lower-bound calculation is correct. Orthogonality gives (W-orth) for all p − s₀ nulls; n ≥ 2s₀ + 2 ensures K ≥ s₀ + 1. The two norm bounds hold with M = M′ = ‖θ*‖². Uniformly over admissible p, (log p)²/n ≤ (log n)²/n → 0, ℓ_n ≥ ½ log n, ℓ_n ≤ 3 log n/2, and f_p ≤ 2. Thus Λ⁽ᴱ⁾_n → 0 uniformly. The factorization in line 40 is exact and both displayed choices of c are valid, using eventual Eδ_n ≥ Λ⁽ᴱ⁾_n/2. For a common threshold across all p_n, invoke Proposition A-E with ε = 1/4 and the common envelope (log n)²/n, and take n large enough that Λ⁽ᴱ⁾_n ≤ 1/4. Exact clarification: add this argument instead of relying solely on a sequencewise liminf to justify any uniform reading of n₀. The upper uniform threshold remains conditional on the unavailable reader theorem.

Counts: C=1, S=1, F=1, E=1.
