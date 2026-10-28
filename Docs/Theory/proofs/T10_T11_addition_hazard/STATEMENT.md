# STATEMENT — T10 (old label T11): feasible-addition hazards and ordered paths

Source: `theorems/T10_T11_addition_hazard.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`.

**Decision at step 1: (a) correct as stated.** No hypothesis is added or removed and no conclusion is weakened. Four informal clauses are given a precise mathematical reading below (marked **Reading**), with the original wording quoted next to each. The statement checker (fresh Opus 5.5 xhigh) returned APPROVED WITH CHANGES; all its required changes are applied here (see `review/STATEMENT_CHECK.md`, with the lead's disposition at the end).

## Setting and definitions

Data (00_COMMON §1, quoted). "Raw data (X^r, y^r), n ≥ 3, no constant column, non-constant y^r. C = I − 11ᵀ/n; D_x = diag of retained raw column sample SDs. Standardised X = CX^rD_x⁻¹, y = Cy^r/s_y with s_y² = ‖Cy^r‖²/(n−1); so ‖x_j‖² = ‖y‖² = n − 1." Entries are finite and p ≥ 1 (THEORY_BRIEF §2.1). "Admissible data" below means data satisfying these conditions.

Target pieces (00_COMMON §1). For T ⊆ [p] with |T| = t: G_T = X_TᵀX_T, z_T = X_Tᵀy, H_T = (n+1)G_T + I_t, D_T = det H_T / det(G_T + I_t), Q_T = yᵀy − n z_TᵀH_T⁻¹z_T, ν = a₀ + n/2, a₀ = b₀ = 0.01, m(T) = C_n D_T^{−1/2}(2b₀ + Q_T)^{−ν} with C_n > 0, BF(T) = m(T)/m(∅) (empty conventions: G_∅ is 0×0 with determinant 1, Q_∅ = yᵀy, D_∅ = 1). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). w(k) = ½ / C(2p−1, k); ϖ(S) = w(|S|)1{|S| ≤ K}/W_K. (The letter m also denotes the number of labels in a round; the argument always shows which is meant.)

Sampler pieces (00_COMMON §2, THEORY_BRIEF §2.6–2.8). Blocks C₁, …, C_J partition [p] (computed from X by the method; |C_b| ≤ B = min(⌊√n⌋, ⌊√p⌋, 16)); tables r_b(U) = BF(U), U ⊆ C_b. γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b); π₀ = γ₀/Z̄₀; d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); γ_φ = γ₀e^{φd} (γ_φ = 0 off Ω), q_φ = γ_φ/Z̄_φ. Neighbour graph N(·): for each j, the partners l ≠ j with |r_jl| > √(2 log p/n), always including j's single largest-|r| partner (ties by index), keeping at most the B largest; then the symmetric union; no edges when p = 1.

Elementary kernels at temperature φ, for S ∈ Ω (exactly the kernels of T09):
- Gibbs j: with S⁺ = S ∪ {j}, S⁻ = S \ {j}: K_{G,j}(S, S^±) = γ_φ(S^±)/(γ_φ(S⁺) + γ_φ(S⁻)) (so an addition at |S| = K has probability 0). o_j(S, φ) := K_{G,j}(S, S⁺) is the pre-draw inclusion probability of j at S; a_j(S, φ) := γ_φ(S+j)/γ_φ(S).
- Uniform swap: self-loop if |S| ∈ {0, p}; else delete j uniformly from S, add l uniformly from [p] \ S, accept with 1 ∧ γ_φ(S′)/γ_φ(S).
- Neighbour swap: self-loop if S = ∅; else delete j uniformly from S; if N(j) \ S = ∅ reject; else add l uniformly from N(j) \ S; accept with 1 ∧ [γ_φ(S′)/γ_φ(S)]·|N(j) \ S|/|N(l) \ S′| (read as 0 if j ∉ N(l)).
- Independence: propose S′ ~ π₀ independently of S, accept with 1 ∧ e^{φ[d(S′) − d(S)]}.

Round. m = p + B + 2 labelled elementary steps (Gibbs 1, …, Gibbs p, one uniform swap, B neighbour swaps, one independence step). A round at temperature φ started at S: draw a permutation σ of the m labels uniformly, independently of the state; set X₀ = S and X_i ~ K_{σ(i)}(X_{i−1}, ·), i = 1, …, m, each step using fresh randomness (EX-S). "Visit S′ during the round" means X_i = S′ for some i ∈ {0, 1, …, m}. "End-of-round (terminal) occupancy of S′" means X_m = S′.

Temperatures. Every elementary move of the method uses a temperature in [0, 1] (00_COMMON §2: "production φ ∈ [0,1]"; values φ > 1 occur only in restricted-ESS evaluations, which move no particle).

Budgets and final run (00_COMMON §2, quoted; used only in (iv-c) and a remark). "N₀ = max(2500, n, p); H₀ = ⌈512N₀/2500⌉; ℓ = ⌈log₂(n+p+1)⌉; T₀ = max(1000, ℓ²); (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), e ∈ {0,1}; L = max(4, ⌈log₂(n+1)⌉). Q_f := 4N_e(T + L + 5) iid π₀ draws scored in the final run (initialisation + independence proposals); 4N_e(L+6) ≤ Q_f ≤ 4N_e(T_e + L + 5)." "Final run: 4 fresh islands × N_e iid π₀ draws; frozen grid; multinomial resampling after every reweighting; one round per stage; L burn-in rounds and 4 measured rounds at φ = 1"; T is the number of grid stages. "Exact branch: Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)p; it precedes block/Gram construction and scores every feasible model."

Constants. For 0 ≤ k ≤ K − 1: r_k := (k+1)/((2p−k−1)√(n+1)), h_k := r_k/(1+r_k). (Since k ≤ p − 1, 2p − k − 1 ≥ p ≥ 1.)

## Assumptions

EX-A (exact arithmetic), EX-S (independent ideal uniform streams). SR is not used (it is needed only when a Gibbs evaluation is translated into a scoring event, which is T11's business). No statistical assumption (G, R, …) is used: every conclusion holds for every data set.

## Conclusions

For every S ∈ Ω with k = |S| < K, every j ∉ S, and every φ ∈ [0, 1]:

**(i)** a_j(S, φ) = γ_φ(S+j)/γ_φ(S) ≥ r_k; o_j(S, φ) ≥ h_k; π₀(S+j) ≥ r_k π₀(S).

**(ii) [ordered path]** Let J ⊆ [p] \ S, |J| = a ≥ 0, k + a ≤ K. For a round at temperature φ ∈ [0, 1] started at S:
P(visit S ∪ J during the round | X₀ = S) ≥ C(m, a)⁻¹ ∏_{i=0}^{a−1} h_{k+i},
and the right side is a lower bound for the probability of the event "the first a labels of σ are the Gibbs labels of J (in some order) and each of these a Gibbs steps adds its coordinate". In particular (a = 1) P(visit S + j | X₀ = S) ≥ h_k/m.

> Original: "The unconditional one-addition bound carries the ordering factor 1/m; the v2 clause 'no ordering constant for a = 1' is false."
> **Reading (ii-neg).** There exist admissible data (n, p, X, y, with the blocks and neighbour graph computed by the method), S ∈ Ω with |S| = k < K, j ∉ S and φ ∈ [0, 1] such that P(visit S + j during the round | X₀ = S) < h_k. (So the inequality "P(visit S+j) ≥ h_k" without an ordering constant fails in general.)

**(iii) [execution time]** Original: "At an actual execution of coordinate j with current state S, conditional on the whole past, the addition probability is o_j(S, φ) ≥ h_k; the expected number of such entries is Σ_e P(X_{e⁻} = S)o_j(S, φ_e) ≥ h_kΣ_e P(X_{e⁻} = S)."

> **Reading.** Consider any run of the algorithm (pilot, calibration or final run; any number of particles, resampling and adaptive choices) under EX-A, EX-S, indexed by its elementary steps u = 1, 2, … (finitely or countably many; the step index is written u, the original's e, to avoid a clash with the budget tier e). For each u let 𝓕_{u⁻} be the σ-field generated by the data and by every stream variate consumed before step u's own draw (including the round orders, resampling and adaptive choices made so far); it determines the label λ_u of step u, its temperature φ_u and the current state X_{u⁻} of the particle executing it. X_u is that particle's state after step u. Hypothesis (as a property of the method, see "Temperatures"): φ_u ∈ [0, 1] for every move. Then, for fixed S ∈ Ω with |S| = k < K and j ∉ S:
> (iii-a) on the event {λ_u = Gibbs j, X_{u⁻} = S}: P(X_u = S + j | 𝓕_{u⁻}) = o_j(S, φ_u) ≥ h_k almost surely;
> (iii-b) the number N_j(S) := Σ_u 1{λ_u = Gibbs j, X_{u⁻} = S, X_u = S + j} of such entries satisfies
> E N_j(S) = Σ_u E[1{λ_u = Gibbs j, X_{u⁻} = S} o_j(S, φ_u)] ≥ h_k Σ_u P(λ_u = Gibbs j, X_{u⁻} = S)
> (both sides possibly +∞). When the temperatures φ_u are non-random (e.g. the final run given the frozen calibration 𝓒, all probabilities then conditional on 𝓒), the middle term equals Σ_u P(λ_u = Gibbs j, X_{u⁻} = S) o_j(S, φ_u), the original display with the sum taken over the executions of coordinate j.

**(iv)** Original: "These are visit/entry statements, not terminal-occupancy statements. A fixed-length addition path is inverse-polynomially accessible in polynomial-dimensional regimes; this does not establish discovery within the declared budget. No feasible addition is counted beyond the cap."

> **Reading.**
> (iv-a) [visit ≠ terminal occupancy] The lower bound of (ii) does not hold for terminal occupancy: there exist admissible data, S, j, φ with P(X_m = S + j | X₀ = S) < C(m, 1)⁻¹h_k.
> (iv-b) [inverse-polynomial accessibility] If p ≤ n^A for a constant A ≥ 0 and a is fixed, then uniformly over data, S, J (k + a ≤ K) and φ ∈ [0, 1], the bound of (ii) satisfies C(m, a)⁻¹∏_{i<a} h_{k+i} ≥ a!·(16 p² √(n+1))^{−a} ≥ a!·(16√2·n^{2A+1/2})^{−a}; hence P(visit S ∪ J during the round | X₀ = S) ≥ a!·(16√2·n^{2A+1/2})^{−a}.
> (iv-c) [no discovery guarantee from these bounds; scope: the final-run budget] Take a = 1, k fixed and p = n (polynomial with A = 1) and the final run with the declared budgets of 00_COMMON §2 (either tier e ∈ {0, 1}). (1) The sum of the (ii) lower bound h_k/m over all 4N_e(T + L + 4) ≤ 4N_e(T_e + L + 4) particle-rounds of the final run tends to 0 as n → ∞. (2) The (iii) lower bound h_k × (number of Gibbs-j executions in the final run) = h_k·4N_e(T + L + 4) also tends to 0. Hence (ii)–(iii) do not by themselves establish discovery of S + j within the declared final-run budget. (The theorem asserts nothing about discovery.)
> (iv-d) [cap] If |S| = K and j ∉ S then S + j ∉ Ω, γ_φ(S + j) = 0 and o_j(S, φ) = 0: no addition from a size-K state ever occurs, and (i)–(iii) are asserted only for k < K (and k + a ≤ K in (ii)).
> *Supplementary, not part of the original's content (its failure would not affect the verdict):* along a sequence of admissible data sets, P(X_m = S + j | X₀ = S)/(C(m,1)⁻¹h_k) → 0.

## Cited results (wave 1, `proofs/COLLECTED/COLLECTED_PROOFS_v2.tex`)

- T09(ii): each elementary kernel above (Gibbs j, uniform swap, neighbour swap, independence) is a Markov kernel on Ω that is q_φ-reversible, φ ∈ [0,1]; in particular the Gibbs-j kernel formula above, with addition at |S| = K of probability 0.
- T22, Lemma 1 (positivity and a closed form): Q_S ≥ 0, D_S ≥ 1, m(S) ∈ (0, ∞) for every S ⊆ [p]; all table entries, w(k), γ_φ(S) (S ∈ Ω) are positive and finite.
- T22, Lemma 2 (one addition): for every T ⊆ [p] and j ∉ T, Q_{T∪{j}} ≤ Q_T, D_{T∪{j}}/D_T ≤ n + 1, m(T∪{j})/m(T) ≥ (n+1)^{−1/2}.
- T22, Lemma 3 (prior ratios): w(k+1)/w(k) = (k+1)/(2p−k−1) for 0 ≤ k ≤ p − 1.
- (T22's lemma "One feasible addition under π₀" is the π₀ clause of (i); noted, not needed.)
- Nothing else; no unproved v3 conjecture is used.

## Change log
- v1 (2026-10-22): readings of (ii)-last sentence, (iii), (iv).
- v2 (2026-10-22): statement checker's required changes applied (scope remark removed from the statement; kernels written out; 𝓕_{u⁻} defined by consumed stream variates; φ ∈ [0,1] for moves made explicit; "ratio → 0" moved to a supplementary remark; (iv-b) visit sentence; (iv-c) final-run scope and (iii) analogue; step index renamed u). Cited results extended to T22 Lemmas 1–3 (HQ note; citation only).
- v3 (2026-10-22, after review round 1): the data conditions of 00_COMMON §1, the budget block, final-run structure and exact-branch rule of 00_COMMON §2 are quoted verbatim (definitions only; closes the round-1 gap R1-CP-1 / R1-CW-F1); T09(ii) citation extended to reversibility of every elementary kernel (used only in a corroborating remark). No conclusion changed.
