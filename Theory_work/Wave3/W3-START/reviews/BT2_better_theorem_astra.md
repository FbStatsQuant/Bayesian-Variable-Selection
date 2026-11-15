MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885

# Independent better-theorem review BT2

There are four credible improvements. They leave the coded method unchanged. All proposed theorem hypotheses are partition-free conditions on the design and coefficients (or population covariance and coefficients); blocks enter only the proofs. This review assesses strengthenings, not the correctness or presentation of the frozen statement.

## P1 — Sharpen the leading functional and remove F2's restriction on p

**Statement.** In §2, for s₀ ≥ 1, define

Lproper_n(h) := p⁻¹ Σ_{l∉S₀} max{J_{h_l}(δ_{U,l}, τ_U): U ⊊ S₀, |U| ≤ 15},

and Lsharp_n(h) := Lproper_n(h) + p⁻¹.

In (T1)(b) and its uniform probability bound (T1)(d), replace the leading functional 𝔏⁰_n(h) by Lsharp_n(h); retain the second-order term n⁻¹𝔏_n(S₀;h)² and every existing assumption. The constants in the uniform bound still depend on the allowed fixed constants and the requested error probability. Make the same substitution in the no-leakage transfer clause (T3)(a) and IF-START. For s₀ = 0 retain the original definition and theorem.

Consequently, in F2 delete the hypothesis p/√log n → ∞ altogether. All its conclusions, including exact order n⁻¹/² when η′ = 0 and κ_V > 1/2, remain valid, even for fixed p > s₀.

**Why strictly better.** The exceptional contribution 15√(2/π)z_n/p becomes 1/p in an O_P bound, and F2 covers previously excluded bounded or slowly growing p. This strengthens an existing design-agnostic theorem, not just an example.

**Proof sketch.** Split T₁ into columns whose conditioning set U*_{b(l)} is a proper subset of S₀ and those whose block contains all of S₀. For the first group, precisely the truncated-expectation and Markov argument of L3.4(b) gives O_P(n⁻¹/² Lproper_n(h)). For s₀ ≥ 1 the second group has at most 16−s₀ ≤ 15 members, and is empty if s₀ ≥ 16. At each such member δ_{S₀,l} = 0 and τ_{S₀} = σ.

For any error tolerance ε choose a fixed Hε with 30 exp(−Hε²/2) ≤ ε. On the event that these at most 15 standard normal variables have absolute value at most Hε, L3.3 applies for all sufficiently large n, since z_n → ∞. Each exceptional step is at most Cε n⁻¹/². Its prior multiplier is at most (s₀+1)/p. Thus their total is O_P(n⁻¹/²/p), uniformly over the admissible designs. No independence is needed. This argument bounds a finite collection in probability; it does not take the divergent untruncated expectation of exp(Z²/2).

Insert this T₁ bound into AGG-b and L5.1(b). For the uniform version allocate part of ε to the exceptional Gaussian event and the rest to the existing events; the cutoff and constants remain design independent. Conditional integration then proves the proposed T3(a) substitution.

Under F2, L6.2(i) and J1 give Lproper_n ≤ C_F n^{η′/2}. Also p⁻¹ ≤ 1, so the new exceptional term is O(n⁻¹/²) without any growth condition on p. The existing second-order hypothesis makes n⁻¹𝔏_n² = o(n⁻¹/²). L6.2(iv)–(v) and FLOOR finish the proof.

**Risk / refutation test.** The exceptional set must be design determined and contain at most 15 columns. Allowing response-dependent selection or s₀ = 0 would invalidate this particular argument. Algebraically check the count and the prior factor; numerically, fixed p with all truths and some nulls in one block tests the removed restriction. A failure of tightness of √n times an individual zero-gain step under the retained toolkit assumptions would refute the proposal. Claiming a fixed-constant probability-to-one bound here would be unjustified; only tightness and the stated ε-dependent uniform bound are proposed.

**Rating: ADOPT NOW (cheap and safe).**

## P2 — Extend Proposition OVL to margin visibility

**Statement.** In (T5), Proposition OVL, replace its assumption (V-c) by “either (V-c) or (V-m), the latter for the same Q.” Retain the bounded number of leaking columns, their gain levels a_{n,l}, (E), (GF-16), and (AL). The exponent E_n and both conclusions remain unchanged:

P(π₀(S₀) ≥ n^{−E_n−ε}) → 1 for every ε > 0,

and the stated sufficient condition for production P-OVL still applies. This removes the explicit exclusion of OVL under (V-m) in §6.

**Why strictly better.** It extends the overlap interface to truths certified by the weaker margin route, without requiring the stronger deletion functional e_n to vanish. The other start theorems already accept that route, while OVL currently does not.

**Proof sketch.** Write Z_L := Σ_{T∈𝓛(Q)}γ₀(T). The exact identity

1/π₀(S₀) = [Z_L/γ₀(S₀)] / π₀(𝓛(Q))

separates lattice concentration from the relative mass inside the lattice. Under either visibility assumption, (T1)(a) gives π₀(𝓛(Q)) → 1. For T = S₀ ∪ N with N ⊆ Q∖S₀, the prior path bound P3 in L1 and the chain bound CH give

γ₀(T)/γ₀(S₀) ≤ ∏_{l∈N} (|Q|m_l/p).

Here the successive models have size at most |Q| ≤ K. Summing over N gives the deterministic inequality

Z_L/γ₀(S₀) ≤ ∏_{l∈Q∖S₀}(1 + |Q|m_l/p).

The proof of L10.2(iii)–(iv) uses only the toolkit, bounded |Q∖S₀|, and the prescribed gains to show that this product is at most n^{E_n+ε/2} with probability tending to one, after absorbing constants. Since 1/π₀(𝓛(Q)) ≤ 2 with probability tending to one, the proposed conclusion follows. The case Q = S₀ is immediate from T1. No bound on e_n is used.

**Risk / refutation test.** The gain estimates for the m_l within Q remain required; lattice concentration alone does not control the relative weight of S₀. Check the displayed identity and the product inequality on arbitrary positive block tables with |Q| ≤ K; they are the decisive algebraic tests. The (V-m) assumption must be evaluated with this same Q, not with S₀ in its place.

**Rating: ADOPT NOW (cheap and safe).**

## P3 — A nonvacuous partition-free leaking-null limit for small support

**Statement.** Extend (T4)(N2), under its retained Setting F, (E), and (GF-16), for s₀ ≥ 1 as follows. Put

r(s₀) := max(1, 17−s₀).

Suppose for all sufficiently large n there is a deterministic set I_n ⊆ [p]∖S₀ of r(s₀) distinct nulls, and a fixed c > 1+2Ā, such that

δ²_{V,l} ≥ c τ²_V log n

for every l ∈ I_n and every proper subset V ⊊ S₀ with |V| ≤ 15. Then

P(π₀(S₀) ≤ n^{−κ′}) → 1

for every 0 < κ′ < (c−1−2Ā)/2. For s₀ ≥ 16 this is the original N2 premise and conclusion. For 1 ≤ s₀ ≤ 15 it is an additional, nonempty partition-free failure condition.

**Why strictly better.** It supplies a limit where N2 is currently vacuous, by requiring a bounded collection of leaking columns instead of one column. It is not a claim that one column alone suffices for small s₀. The improved statement contains the old N2 for its nonvacuous range and adds new support sizes without any design-family or partition hypothesis.

**Proof sketch.** A block containing all s₀ truths can contain at most 16−s₀ nulls, and at most one block can contain all truths. If the truths are split among blocks, no block contains them all. Thus when s₀ ≤ 15, among 17−s₀ designated nulls at least one has U*_{b(l)} ⊊ S₀. When s₀ ≥ 16, every null has this property because its block has at most 15 other columns. Select the first qualifying designated null in a fixed ordering. Its conditioning set has size at most 15 and hence satisfies the proposed gain inequality. Apply the proof of C2(i), L7.1, to this witness. The witness depends only on X, so its noise projection remains a single standard Gaussian in Setting F; there is no response selection penalty. The exponent is unchanged.

Nonvacuity can be checked algebraically with s₀ = 1. In a centred orthonormal collection e₀,…,e₁₆, set x₁ = √(n−1)e₀ and x_{l_i} = √(n−1)(ρ_n e₀ + √(1−ρ_n²)e_i), i=1,…,16, with μ = θ x₁ for fixed θ ≠ 0. Take

ρ_n² = c(σ²+θ²)log n / ((n−1)θ²).

Then δ²_{∅,l_i} = c τ²_∅ log n for all sixteen nulls. The small Gram eigenvalues are of order n, and the energy is O(n). These statements verify the proposed premises; the construction is only a nonvacuity check, not a design family in the theorem. One can choose a fixed c > 1+2Ā and add orthogonal null columns while dimension permits. The counting proof itself has no restriction p ≤ n and applies equally to admissible p ≫ n designs.

**Risk / refutation test.** The count is essential: 16−s₀ designated nulls could all share a block with all truths, where their conditional mean gains are zero. A partition of size at most 16 that shields all 17−s₀ designated nulls would refute the combinatorial step, but cannot exist. Check the construction's marginal gain directly; including V = S₀ would restore the old vacuity. No stronger one-null result is asserted.

**Rating: ADOPT NOW (cheap and safe).**

## P4 — Allow polynomial-size Gaussian leakage sets

**Statement.** In (L-R) and (T3)(b), decouple the bounds on Q and H_l. Keep |H_l| ≤ (log n)^{κ_Q}, all its containment requirements, and the population gain and localisation conditions exactly as stated. Replace |Q| ≤ (log n)^{κ_Q} by

|Q| ≤ n^{1/2−ε_Q},   |Q| ≤ K,

for any fixed ε_Q ∈ (0,1/2). Retain every other hypothesis of T3(b). Its probability-to-one bound

1−π₀(𝓛(Q)) ≤ (|Q|+1)n⁻¹/² exp(C_R√log n)

and its C_L = 0 tightness bound both remain valid. The no-leakage clause Q = S₀ is unchanged. The exponent κ_Q now controls the reference-set sizes, not the size of Q.

**Why strictly better.** This widens the lattice theorem from polylogarithmic to nearly square-root-size leakage sets, still allowing p ≫ n and imposing only population conditions. Every originally allowed Q eventually satisfies the new size bound for any fixed ε_Q < 1/2. The proof cost is small because Q and H_l play different roles.

**Proof sketch.** Inspect L9.3–L9.6: N_ref ≤ (1+(log n)^{κ_Q})^{15} counts subsets of H_l. The number of reference pairs is at most pN_ref, regardless of |Q|. Removing more columns from the sum over l∉Q only reduces that count. The energy, Gram, and visibility steps L9.1–L9.2 do not use |Q|. Therefore the same high-probability design event yields 𝔏_n(Q) ≤ exp(C_B√log n), with the same type of constants.

The only subsequent size requirement is smallness of ϱ_n(Q). With the new bound,

ϱ_n(Q) ≤ (n^{1/2−ε_Q}+1)n⁻¹/² exp(C_B√log n)
         = n^{−ε_Q+o(1)}.

In particular it is eventually smaller than c_{0,n}, of order 1/log n in L6.0′. Apply that uniform theorem conditionally as in L9.7. Its logarithmic multiplier is absorbed in exp((C_B+1)√log n); its n⁻¹ visibility remainder is also negligible. This proves the first conclusion. For C_L = 0, L9.6(b)'s tightness estimate is unaffected, and multiplying it by (|Q|+1)n⁻¹/² gives a vanishing rate n^{−ε_Q} times a fixed logarithmic power. The ε-dependent design-set argument in L9.7 then gives the same tightness conclusion. T1(d)'s constants are uniform in Q; c_Q is already accounted for by |Q|+1.

**Risk / refutation test.** Do not enlarge H_l to polynomial size at the same time: that changes N_ref and can consume the rate. The algebraic audit is to substitute |Q| = n^{1/2−ε_Q} in the bounds for ϱ̄_n, c_{0,n}, and the failure probability (4+3N_ref)n⁻². All still vanish in the required direction. Any independent use of |Q| ≤ polylogarithmic size in the Gaussian bridge would invalidate the proposal; the displayed bridge uses that bound only in L9.7's final rate comparison.

**Rating: ADOPT NOW (cheap and safe).**

## No credible improvement found for

- **FLOOR's exponent and a universal saturated-model analogue.** The n⁻¹/² floor is a deterministic obstruction, and F2 attains that order. A saturated model has no feasible addition, and its mass can approach one much faster. P1 does not alter this conclusion.
- **Dropping (GF-16) altogether while retaining T1's rates.** L2's determinant correction and score residual correction explicitly depend on 1/g_*. Rank loss changes the dimension penalty itself. The current aggregation controls cardinality, not effective rank. A floor-free result needs additional work; merely deleting the assumption is not justified.
- **Dropping the energy bound without replacing the score argument.** The τ-form RSS concentration does not need it, but the scored residual lower bound in TK-b does. When signal energy dominates n, the fixed scorer offset and ridge residual correction need not be bounded relative to scored RSS. This blocks the present proof; it is not a necessity claim about the method.
- **Necessity of (AL), or removing its all-15-set maximum without replacement.** The necessary quantities T₁ and Ξ are evaluated on actual table configurations. The partition-free maximum can be attained at other configurations, and truncated first moments are only upper bounds on random sums. Neither AGG-b nor the Markov proof provides a converse. A response-independent smaller deterministic envelope would need a new argument valid for the coded partition. P1 sharpens only the leading functional, not AL.
- **A complete necessary-and-sufficient visibility condition or the boundary window in C2/N3.** The one-truth threshold is constrained by the prior-plus-dimension price. Near that threshold the Gaussian cross term has order √log n, so a vanishing relative margin is not automatically sufficient. V-m also compares configurations involving several missing truths and substituting nulls, which a one-truth deletion diagnostic does not cover. P2 extends its usefulness but does not close this gap.
- **A one-null, small-support replacement for N2 with only proper-subset gains.** A null can share a block with every truth, making its relevant gain zero. P3 resolves this by a counting condition on multiple nulls, not by ignoring the shielding possibility.
- **Removing exp(C_R√log n) in T3(b), or upgrading the C_L = 0 bound to a fixed-constant probability-to-one result at the same rate.** L9.5 integrates a shifted Gaussian at a critical exponential moment; the shift produces the displayed subpolynomial factor. L9.6 controls a sum by its mean and Markov, without establishing concentration across dependent columns. Neither factor can be deleted on the strength of that proof. P4 improves the size of Q only.
- **Non-Gaussian rows or noise, growing s₀, a universal distributional limit of √n o₀, or a universal √(log p/n) lower bound.** The conditional Gaussian geometry and exact J_h integral need replacement for broader laws; growing support changes the aggregation and truth-event factors. Dependence among columns and residual signal variance affect the leading T₁ law. In particular F2's exact n⁻¹/² order rules out a universal extra √log p lower factor for growing p under the full existing scope. No matching universal strengthening is justified here.
- **A substantively broader T3(a) response-selected-target theorem.** Its conditional fixed-design argument already admits arbitrary design laws and design-measurable targets. Response selection destroys that conditioning argument. P1 transfers because it retains uniform conditional bounds; it does not license response selection.

The proposed changes need no method modification, new design-family theorem, finite-n refinement, or extension into the excluded strong-factor and masked-truth regimes.
