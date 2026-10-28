# STATEMENT — T09 (T7): exact start, invariant kernels and whole-round minorisation

Source: `theorems/T09_T7_kernel_validity.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c). Decision at step 1: **(a) correct as stated.** No hypothesis is added or changed. Two informal clauses (the last sentence of (iii) and the second sentence of (v)) are given a precise mathematical reading below; the original wording is quoted next to each reading.

Standing idealisations (declared in the source): **EX-A** exact scores, convolutions, probabilities and comparisons; **EX-S** independent ideal uniform random streams.

**Change log.** v2 (after review round 1): the last sentence of the reading of (v) said "(equivalently, no lower bound on its mixing time) that tends to 0", which is wrong as written (a mixing-time lower bound tending to 0 is trivially available). It now speaks of a lower bound tending to infinity and adds the explicit bound t_mix ≤ 55. The original wording, the hypotheses and the existence claim are unchanged.

## 1. Setting and definitions

**Data.** Integers n ≥ 3, p ≥ 1. X ∈ ℝ^{n×p} and y ∈ ℝⁿ are standardised data: every column x_j and y are centred, ‖x_j‖² = ‖y‖² = n − 1. (These are exactly the outputs of the method's preprocessing; a standardised pair is returned unchanged by it.) K = min(p, ⌊n/2⌋); Ω = {S ⊆ [p] : |S| ≤ K}.

**Scores.** For S ⊆ [p], k = |S|: G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I_k, D_S = det H_S / det(G_S + I_k), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν = 0.01 + n/2, b₀ = 0.01, A_S := 2b₀ + Q_S,
BF(S) = D_S^{−1/2} (A_∅ / A_S)^{ν}  (so BF(∅) = 1; this is m(S)/m(∅)).
Size prior: w(k) = ½ / C(2p−1, k), W_K = Σ_{k≤K} C(p,k) w(k), ϖ(S) = w(|S|)/W_K for S ∈ Ω.

**Blocks and tables.** C₁, …, C_J is the method's block partition of [p] (complete linkage, top-down cut, next-fit packing), |C_b| ≤ B = min(⌊√n⌋, ⌊√p⌋, 16). Tables r_b(U) = BF(U) for U ⊆ C_b. Block size profiles e_b(j) = Σ_{U⊆C_b, |U|=j} r_b(U), j = 0, …, |C_b|.

**Start.** γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b) for S ∈ Ω; Z̄₀ = Σ_{S∈Ω} γ₀(S); π₀ = γ₀/Z̄₀.
Convolution: c^{(0)} = δ₀ (c^{(0)}(0) = 1, else 0); c^{(b)}(t) = Σ_j e_b(j) c^{(b−1)}(t − j) (b = 1, …, J), c := c^{(J)}.
**Backward sampler** (one draw, fresh uniforms): (1) draw the total size k ∈ {0, …, K} with probability w(k)c(k) / Σ_{k′≤K} w(k′)c(k′); (2) set t_J = k; for b = J, J−1, …, 1 draw j_b with probability e_b(j_b) c^{(b−1)}(t_b − j_b) / c^{(b)}(t_b) and set t_{b−1} = t_b − j_b; (3) for each b draw U_b ⊆ C_b with |U_b| = j_b with probability r_b(U_b)/e_b(j_b); return S = ∪_b U_b.

**Bridge.** d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); γ_φ(S) = γ₀(S) e^{φ d(S)} for S ∈ Ω, γ_φ(S) := 0 for S ∉ Ω; Z̄_φ = Σ_Ω γ_φ; q_φ = γ_φ/Z̄_φ (a probability on Ω, positive everywhere on Ω).

**Neighbour graph.** N(j) ⊆ [p] \ {j} for each j: the method's symmetric-union graph (l ∈ N(j) ⇔ j ∈ N(l)). Statement (ii) is also asserted, with the stated reading convention, for an arbitrary family N(j) ⊆ [p] \ {j}.

**Elementary kernels on Ω at temperature φ** (all states, all moves in Ω):
- **Gibbs j** (j ∈ [p]): with S⁺ = S ∪ {j}, S⁻ = S \ {j}: K_{G,j}(S, S^±) = γ_φ(S^±) / (γ_φ(S⁺) + γ_φ(S⁻)). (When j ∉ S and |S| = K, S⁺ ∉ Ω, so the addition has probability 0.)
- **Uniform swap**: if |S| ∈ {0, p}, stay. Otherwise pick j uniformly in S and l uniformly in [p] \ S, propose S′ = S \ {j} ∪ {l}, accept with probability 1 ∧ γ_φ(S′)/γ_φ(S); else stay.
- **Neighbour swap**: if S = ∅, stay. Otherwise pick j uniformly in S; if N(j) \ S = ∅, stay; else pick l uniformly in N(j) \ S, propose S′ = S \ {j} ∪ {l}, accept with probability 1 ∧ ([γ_φ(S′)/γ_φ(S)] · |N(j) \ S| / |N(l) \ S′|), where this ratio is read as 0 when j ∉ N(l); else stay.
- **Independence**: draw S′ ~ π₀ independently of S; accept with probability 1 ∧ e^{φ[d(S′) − d(S)]}; else stay.

**Round.** m = p + B + 2 labelled steps: Gibbs 1, …, Gibbs p, one uniform swap, B neighbour swaps, one independence step; their kernels K_1, …, K_m (as matrices on Ω). For a permutation σ of [m] (the realised order), K_σ := K_{σ(1)} K_{σ(2)} ⋯ K_{σ(m)} (step σ(1) is applied first). K_φ := (1/m!) Σ_σ K_σ (order uniform, independent of the state).

**Analytic objects.** L²(q_φ): functions on Ω with ⟨f, g⟩ = Σ q_φ f g. A kernel P is q-reversible if q(x)P(x,y) = q(y)P(y,x) for all x, y; P is self-adjoint on L²(q) if ⟨Pf, g⟩ = ⟨f, Pg⟩ for all f, g. Π_φ := the kernel Π_φ(x, ·) = q_φ(·). Absolute L² gap of P: gap*(P) := 1 − ‖P − Π_φ‖_{L²(q_φ)→L²(q_φ)}. ‖μ − ν‖_TV = sup_A |μ(A) − ν(A)|. ε_φ := min_{S∈Ω} π₀(S)/q_φ(S). A **switch** means argmax_Ω q₀ ≠ argmax_Ω q₁ (the bridge's mode changes between φ = 0 and φ = 1). The **discrepancy range** is max_Ω d − min_Ω d.

**Valid component input:** any (n, p, X, y) as above together with the method's blocks, tables and neighbour graph built from it. The kernels are component objects: they are defined for every such input, whether or not the method's exact-enumeration branch would be taken for that (n, p).

## 2. Claims (for every valid component input and every φ ∈ [0, 1], unless an existence claim says otherwise)

**(i)** Σ_{k≤K} (w(k)/W_K) c(k) = Z̄₀ exactly. Under EX-A and EX-S, the backward sampler is well defined (every conditional probability it uses has a positive denominator and sums to 1) and returns S with probability exactly π₀(S); successive draws with fresh streams are iid π₀.

**(ii)** Each elementary kernel is a Markov kernel on Ω that is q_φ-reversible, including the boundary cases: the Gibbs addition at |S| = K has probability 0; the uniform swap self-loops at |S| ∈ {0, p}; the neighbour-swap ratio read as 0 when the reverse insertion is not a neighbour (j ∉ N(l)); and the stated Hastings ratios equal γ_φ(S′)q(S′, S) / (γ_φ(S)q(S, S′)) with q the actual proposal probabilities (so they supply the reverse proposal probability). For the neighbour swap this holds for any family N(j) ⊆ [p] \ {j}; for the method's symmetric graph the "read as 0" case never arises.

**(iii)** K_φ is a Markov kernel, q_φ-invariant, and self-adjoint on L²(q_φ) (equivalently q_φ-reversible). *Original wording: "An individual realised order need not be reversible."* Reading: for every σ, K_σ is q_φ-invariant, and K_σ is q_φ-reversible if and only if K_σ = K_{σ̄}, σ̄ the reversed order; and there exist a valid component input, φ ∈ [0,1] and an order σ such that K_σ is not q_φ-reversible.

**(iv)** For every σ and every S ∈ Ω: K_σ(S, ·) ≥ ε_φ q_φ(·) (as measures), with ε_φ = (Z̄_φ/Z̄₀) e^{−φ max_Ω d} ∈ (0, 1]. Hence K_φ(S, ·) ≥ ε_φ q_φ(·), sup_S ‖K_φ^h(S, ·) − q_φ‖_TV ≤ (1 − ε_φ)^h for every integer h ≥ 0, and gap*(K_φ) ≥ ε_φ.

**(v)** ε_φ ≤ π₀(S)/q_φ(S) for every S ∈ Ω. *Original wording: "An exponentially small available minorisation constant does not establish exponentially slow mixing of the hybrid kernel; neither a switch nor a large discrepancy range alone supplies such a lower bound."* Reading: there exist constants c > 0, n₀ and, for every n ≥ n₀, a valid component input (with that n) such that at φ = 1 simultaneously: ε₁ ≤ e^{−cn}; the discrepancy range is ≥ cn; there is a switch; and gap*(K₁) ≥ 1/40 and sup_S ‖K₁^h(S, ·) − q₁‖_TV ≤ (39/40)^h for all h. Consequently, writing t_mix(K) := min{h ≥ 0 : sup_S ‖K^h(S, ·) − q_φ‖_TV ≤ 1/4}, the family has t_mix(K₁) ≤ 55 for every n ≥ n₀; so no upper bound on gap*(K_φ) that tends to 0, and no lower bound on t_mix(K_φ) that tends to infinity (in particular none exponentially large in n), can be derived from ε_φ being exponentially small, from a switch, or from a large discrepancy range, alone or together.
