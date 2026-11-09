# R03 — Adversarial check of L0, L1, and L2

Reviewed the three lemma files against STATEMENT.md §§1–3, GEN L1 and L4, SoP 02_method.tex:459–506, and T37R PROOF.md:85–120. Line references below refer to the reviewed versions. No source files were changed. No numerical experiment was needed: the checks below are algebraic and geometric.

The substantive descent and probability arguments survive. L2 needs a correction to its auxiliary family before its invocation of L0 is literally justified. I found no counterexample to the three intended lemma conclusions.

## Required amendments

**1. L2_NA_TL.md:10–14: separate truth deletions from the swap comprehension, and include the empty set.**

As written, the final comprehension has the shared restriction `l ∉ T` for both `T ∖ {i}` and `(T ∖ {i}) ∪ {l}`. When Q = [p] and T = Q, there is no such l. If 𝒫 is nonempty, Q ∖ {i} is nevertheless generated as a swap from Q ∖ {e}, e ∈ 𝒫. But when Q = S₀ = [p], there is no smaller lattice member, and the required truth deletions really are omitted. These are feasible neighbours at |Q| = K = p, and the TL proof at lines 24–29 invokes the toolkit for them without establishing their membership in the family. This is an actual boundary case permitted by (G1), rather than an infeasible-neighbour issue.

For example, take fixed p = s₀ = 2, S₀ = Q = [2], and large n. The displayed family is just {Q}, omitting both singleton truth deletions. Orthogonal centred columns and fixed nonzero coefficients give an admissible Gram and signal geometry, so the hypotheses do not remove this case.

Also, GEN L1.1 explicitly assumes ∅ ∈ 𝔉. With s₀ ≥ 2 the displayed L2 family never contains ∅, even away from Q = [p]. L0 says the other assumptions are unchanged. This hypothesis is harmless to supply, but currently missing.

Replace the family by

```text
𝔉* = {∅} ∪ 𝓛
   ∪ {T ∪ {l} : T ∈ 𝓛, l ∉ T}
   ∪ {T ∖ {i} : T ∈ 𝓛, i ∈ S₀}
   ∪ {(T ∖ {i}) ∪ {l} : T ∈ 𝓛, i ∈ S₀, l ∉ T}.
```

Use this family to define 𝓔_n. A sufficient count is

```text
|𝔉*| ≤ 1 + 2^{|𝒫|}(1 + p + s₀ + s₀p)
      ≤ 5s₀ n^{C_P log 2 + A}.
```

Thus D, D_V, t_n, h_n, and every subsequent asymptotic calculation are unchanged; only the allowed family prefactor changes. Every nonempty member remains a subset of some Q ∪ {l}, so the Gram argument remains valid. For a pure deletion, use the Gram floor on Q directly (obtained from (G2) by choosing l ∈ Q). This also removes the unbound `l` in the pure-deletion instance of line 25.

**2. L2_NA_TL.md:62: replace the asserted asymptotic equality by an upper bound.**

Under (G4-χ), |𝒫| is bounded above by (1 − δ₀) log n; it need not equal that leading term. The parenthesis should say that the left side is **at most**

```text
(1 − δ₀) log n + O(√(log n · log log n)).
```

For example, |𝒫| = 0 satisfies the hypothesis but makes the stated equality false. The needed comparison with log(n + 1) follows from the upper bound, so this is a wording correction, not a failure of the union bound.

## L0 — line-by-line checks

**Lines 12–27: the growing-rank extension works.** Apart from the size assumptions and n₀ declarations themselves, the operative J-dependence in GEN is precisely the χ² moment factor in 𝒟₂ and the determinant/remainder estimates (E1)/(E4). GEN's (E2) uses only the minimum Gram eigenvalue and ‖y‖² = n − 1; it has no hidden multiplicative J factor.

For d ≤ C_J log n,

```text
2^{d/2} exp(−t_n/4)
 ≤ n^{C_J(log 2)/2 − D − 2 − C_J}
 ≤ n^{−D−2}.
```

The union bound gives C_F n⁻². The proposed t_n is more than sufficient. The phrase “hold verbatim” should be understood with J replaced by J_n and the displayed improved 𝒟₂ probability bound; a retained n-dependent prefactor 2^{J_n/2} alone would obscure the reason for increasing t_n.

Eventually (n − 1)φ₀² ≥ max(J_n,100), and J_n/((n − 1)φ₀²) ≤ 1. Hence the same C_R, c_E, and κ_E work. The 0.52/c_E bound remains valid because `(1/2 + 0.01/n)·1.03 < 0.52` for sufficiently large n. Contrast bounds require the vector-set inclusions specified in GEN L1.4; L0 has not removed those requirements.

**Lines 31–35: the sharp floor is valid.** Completing the square gives Λ − 2σh_n√Λ ≥ −σ²h_n². The χ² deviation is at most 4n^{2/3}; the extra `+1` in ω_n accounts for the lost degree of freedom n − 1. Thus the stated floor follows with the stated constant 4. Also ω_n = O(n^{-1/3} + log n/n), which is strong enough for L2's later error estimate.

**Lines 37–43: both likelihood-ratio inequalities are valid.** On [0,1/2], `−log(1−x) ≤ x+x²`; for example, the derivative of `x+x²+log(1−x)` is x(1−2x)/(1−x) ≥ 0. The claimed factor 1+2x is therefore conservative. The coefficient `(1+0.02/n)/(1−ω_n)` is exactly the coefficient obtained from ν = n/2+0.01 and the RSS floor. For the second display, `log u ≤ u−1` uses the floor for the smaller RSS, RSS_{A′}; the denominator is correct. This second bound does not require x ≤ 1/4.

**Lines 45–53: score signs and prior ratios are correct.** The table normalizer cancels, so the displayed block identity does not need a separate approximation for m(∅). The exact addition ratio is (k+1)/(2p−1−k). For k ≤ p−1 its denominator is at least p. The deletion ratio is (2p−k)/k, which lies between 1 and 2p for 1 ≤ k ≤ p. No fixed-size restriction is hidden here.

## L1 — line-by-line checks

**Lines 11–38: the neighbour classification is exhaustive.** Additions are handled by NA; truth deletions and truth-removing swaps by TL; extra deletions improve by NA at the smaller lattice set; and extra-removing swaps lose against the corresponding extra deletion by NA at that same smaller set. This last comparison is the necessary one: an extra-removing swap need not lose against the current centre, but it loses against an available improving deletion. The proof uses precisely this comparison.

At |C| = K, additions from C are absent, but C ∖ {e} has size K−1, so both NA applications at the smaller set remain feasible. Swaps preserve size. Directions l outside Q are included in NA, so a swap leaving Q is covered. All maximising neighbours are extra deletions; ties among them do not affect the argument. The plain lexicographic scan tie rule matches SoP and GEN L4 and is distinct from the global HPM size-then-lex rule.

At S₀, every non-addition neighbour removes a truth. If no additions exist, no NA statement at size K is needed. Thus the endpoint argument covers saturation as well.

**Lines 42–56: the move count and caps are correct.** Each move removes exactly one extra, so τ = |C ∖ S₀| exactly. With a nonnegative integer cap ℓ, scan centres have path indices 0 through min(ℓ,τ). The final scan at index ℓ cannot make another move.

For τ > 0, S₀ first occurs among these scanned neighbours at index τ−1. Earlier centres have at least two extras, and a flip or swap cannot remove two extras; hence they cannot scan S₀. Consequently, within this search, S₀ is scored iff ℓ ≥ τ−1. For τ = 0 the emitted centre supplies the score. This “iff” concerns scoring by this search, not whether another phase already scored S₀.

When ℓ = τ−1, the final scan scores S₀ but still has a strict improvement, so the endpoint remains the predecessor and `local_limit` is set. When ℓ ≥ τ, the search moves to S₀ and completes its non-improving scan: certified endpoint S₀, no `local_limit`. This is endpoint certification, not a claim about the public flag for a possibly different reported HPM. The emitted-centre and completed-scan premises are the stipulated semantics.

## L2 — remaining line-by-line checks

**Lines 11–18: family size, floors, and null-add identity.** After amendment 1, all sets have size O(log n), the family has polynomial cardinality with exponent D, and the contrast vectors have cardinality at most 2C_F²n^{2D}. Interlacing supplies the same φ₀² floor. The stronger feasibility clause of (G1) is unnecessary for these estimates: even a formally infeasible add set can be included in the toolkit family, and NA itself only asks for feasible additions. Each relevant residual direction exists by (G2), is centred, and is orthogonal to μ because T contains S₀. Therefore the RSS drop is exactly σ²Z², with a standard normal Z.

**Lines 24–31: TL constants and signs are correct after amendment 1.** A truth-removing neighbour misses exactly one truth, so its residual signal is θ*_i(I−P_A)x_i. The Schur-complement floor is `(n−1)φ₀²θ_i*²`, without an extra factor φ₀². BM-∞ makes L′_n/log n diverge. Applying the contrast inequality with ε=1/2 gives the displayed Λ_A/4 bound eventually. The likelihood contribution to F(A)−F(T) is negative, bounded above by `−(RSS_A−RSS_T)/(2C_R)`. Deleting one variable contributes at most `log(2p)+(1/2)log(n+1)` from prior and dimension. For large n this is at most `(A+1)log n+1`. Thus the final `−L′_n/(8C_R)` dominates. The conclusion is uniform over the family.

**Lines 35–43: NA reduction is correct.** Since k<K≤p, k≤p−1; the denominator lower bound p holds even when K=p. The maximal-Z event gives x=O(log n/n), hence x≤1/4 eventually. More specifically, ϑ_n=O(n^{-1/3}+log n/n), so the likelihood excess over Z²/2 is

```text
O(log n · n^{-1/3} + (log n)²/n) = o(1).
```

This establishes the claimed eventual bound 1/2; mere convergence ϑ_n→0 without its rate would not suffice, but L0 supplies the rate. Substituting c_n cancels all log p, log(|Q|+1), log(n+1), and κ_E terms, leaving exactly −1/2. Also c_n is eventually positive and O(log n), including fixed p.

**Lines 51–59: the Pythagorean bound is valid.** Since l∉T and S₀⊆T, any l inside Q belongs to 𝒫, never S₀. Thus S₀⊆T⊆Q_l⊆Q in every indexed case. The a,b decomposition is orthogonal, and a≠0 follows from the Gram floor on Q∪{l}. Weighted Cauchy–Schwarz gives precisely the sum of the two squared standardized components. The b component is bounded by the projected noise onto range(P_{Q_l}−P_T), which is contained in range(P_Q−P_{S₀}). This is a pathwise inequality; no independence is being presumed.

The Gram floor on Q gives rank(P_Q−P_{S₀})=|Q|−s₀=|𝒫|, so the common noise term has the claimed χ² law. Rank zero is a deterministic zero term and causes no difficulty. There are (p−|Q|)+|𝒫|=p−s₀≤p base normals. The normal union bound and Laurent–Massart bound each cost at most 1/log n, even though their events may be dependent.

**Lines 60–66: both final probability comparisons work.** Adding the two thresholds gives exactly the displayed `2log(2p)+4log log n+|𝒫|+2√(|𝒫|log log n)`. Its comparison to c_n cancels 2log p, leaving the displayed inequality. With amendment 2 the remaining error is o(log n), absorbed by δ₀log n. Thus the maximal-Z failure probability is at most 2/log n eventually under (G4-χ).

For (G4-dir), distinct deterministic directions give at most pN_n Gaussian linear functions; independence and distinct realized values are unnecessary. The displayed union bound costs at most 1/log n. Its threshold comparison is correct, and log N_n=o(log n), together with |Q|=O(log n), supplies the needed slack. Empty direction families make NA vacuous; their maxima may simply be omitted. Intersecting these events with 𝓔_n requires only another union bound.

## Final verdicts

- **L0_toolkit.md: VERIFIED.** The rank adjustment, RSS floor, likelihood bounds, and constants track.
- **L1_descent.md: VERIFIED.** All neighbour classes, saturation, ties, and both cap thresholds are correct under the stated search semantics.
- **L2_NA_TL.md: VERIFIED-WITH-AMENDMENTS (1–2).** Amendment 1 repairs the missing toolkit-family membership and inherited empty-set hypothesis; amendment 2 corrects an unjustified asymptotic equality. With those explicit repairs, TL and both NA arguments are verified. No substantive counterexample was found.
