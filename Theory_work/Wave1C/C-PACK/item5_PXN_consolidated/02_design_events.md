# Part 2 — Design events: the cutoff L_n, the event ℰ♯_n, and partition recovery (Theorem R)

## 2.1 Cutoffs and the size L_n

**Definitions.** Put q_k := C(p,k)w(k), R_m := Σ_{k=max(m+1,0)}^{K} q_k / w(s₀), and (as in the statement of T03♯, §5.1)

  m♯_n := min{m ≥ s₀ : R_m ≤ n^{−(s₀+2)/2}}.

The SE cutoff m_n := ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ½ log n)/log 2⌉ is also O(log n). Put j₀ := ⌈(2A+1)s₀⌉ + 1.

**Lemma K (the cutoff m♯_n is O(log n)).** With p ≤ n^A: m♯_n ≤ k_n := max{s₀, ⌈1 + s₀ + (As₀ + (s₀+2)/2) log₂ n⌉} = O(log n).
Consequently

  **L_n := s₀ + max{m_n, k_n, j₀, g, s₀+2} = O(log n).**

*Proof.* C(p,k)/C(2p−1,k) = ∏_{i<k}(p−i)/(2p−1−i); the i = 0 factor is ≤ 1 and each i ≥ 1 factor is ≤ ½ (2(p−i) ≤ 2p−1−i ⇔ i ≥ 1),
so q_k = ½C(p,k)/C(2p−1,k) ≤ 2^{−k}. Also 1/w(s₀) = 2C(2p−1,s₀) ≤ 2(2p)^{s₀}. Hence R_m ≤ 2(2p)^{s₀}Σ_{k>m}2^{−k} = 2^{1−m}(2p)^{s₀}, and
R_m ≤ n^{−(s₀+2)/2} as soon as m ≥ 1 + s₀ log₂(2p) + ((s₀+2)/2) log₂ n. With p ≤ n^A this gives m♯_n ≤ k_n. ∎

Every set used below has size ≤ L_n: the sets T ∖ S₀ with |T∖S₀| ≤ max(j₀, m♯_n) used by T03♯, the sets of size ≤ m_n + s₀ of the
locked SE range, the within-group sets of Lemma E (|T| ≤ g), and the sets of 𝔉_n (|T| ≤ s₀+2).

## 2.2 The design event ℰ♯_n

**Definition.** ℰ♯_n is the X-event on which
(a) λ_min(R̂_T) ≥ φ₀² := λ₀/2 for every nonempty T ⊆ [p] with |T| ≤ L_n (not only sets anchored at S₀), where λ₀ := λ_min(Σ) ≥ (1−ψ̄)(1−ρ) (F4);
(b) ‖μ‖²/n ≤ M := 2θᵀΣθ + 1;
(c) min_{j∈S₀} θ*_j² ≥ b_min := ½ min_{i,h}(β_i²ψ_i², β_i², (β^vis_h)²) (θ*_j = θ_j·sd_j, sd_j the sample SD);
(d) s₀ ≤ K (deterministic: K = min(p, ⌊n/2⌋) ≥ s₀ once p_n ≥ s₀ and n ≥ 2s₀+1; p_n → ∞).

**Lemma 2.2.** P(ℰ♯_n) → 1.
*Proof.* (a) ‖R̂_T − Σ_T‖_op ≤ |T| max_{j≠k}|r̂_jk − Σ_jk| ≤ L_nδ_n = O((log n)^{3/2}/√n) → 0 with probability ≥ 1 − 3n^{−2} by [CONC′]
(δ_n = 32√(2(A+1) log n/(n−1))), and λ_min(Σ_T) ≥ λ₀ by interlacing, so λ_min(R̂_T) ≥ λ₀ − o(1) ≥ λ₀/2.
(b), (c): the finitely many columns of 𝒮𝒱 (|𝒮𝒱| = gs₀) satisfy the SLLN; ‖μ‖²/n → θᵀΣθ and sd_j → 1 a.s., so θ*_j² → θ_j² and
(b), (c) hold eventually. ∎

**Consequences used below.** On ℰ♯_n, λ_min(R̂_T) ≥ φ₀² for every nonempty T with |T| ≤ L_n; in particular for every T ⊆ C_h
(|T| ≤ g), every T with |T| ≤ s₀+2, and every T with |T| ≤ m_n+s₀. Hence ℰ♯_n ⊆ ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn} = ℰ*(𝔉) for both
families 𝔉_start and 𝔉_n of §1.4, and ℰ♯_n is the working X-event of Lemma E in both applications. It is also the design event
of §5 (posterior concentration).

## 2.3 Theorem R (partition recovery with an explicit probability)

Let 𝒜_n := {blocks = groups} (an X-measurable event). For r ∈ (−1,1) let P_r denote the law of the Pearson correlation r̂ of n iid
bivariate normal pairs with correlation r. For t ∈ (ψ̄, ρ) put

  S(t) := Σ_{within-group pairs} P_ρ(|r̂| ≤ t) + Σ_{cross-group pairs} P_{|Σ_jk|}(|r̂| ≥ t),

with I(t; r), q_R, t*, I* as in (R) of §0.4.

**Theorem R.** Assume (SIZE) at n and n ≥ 5.
(R-a) For every t ∈ (ψ̄, ρ): P(𝒜_nᶜ) ≤ S(t).
(R-b) With t = t*: P(𝒜_nᶜ) ≤ S(t*) ≤ K_n := (2/(√π(1−ρ))) p²√n e^{−(n−4)I*}.
(R-c) For every fixed A ≥ 1 and C > 0: P(𝒜_nᶜ) ≤ p^{−C} once n ≥ max(5, n₁) and
 (n−4)I* ≥ log(2/(√π(1−ρ))) + ((2+C)A + ½) log n; and P(𝒜_nᶜ) ≤ (2/(√π(1−ρ))) e^{4I*} n^{2A+½} e^{−nI*}, which is summable in n with
no lower growth bound on p. In particular Σ_n P(𝒜_nᶜ) < ∞, and P(𝒜_nᶜ) ≤ p^{−C} for n ≥ max{n₁, n₀(A, C, ρ, ψ̄)}.

(The display (R-a)/(R-b) is not a single chain over all t: S(t) ≤ K_n is asserted
here only at t = t*. A uniform assertion over all t is false; for t near ρ a
within-pair term of S(t) can be close to ½.)

**Lemma R0 (deterministic recovery under a global margin).** Assume (SIZE) at n, and the strict global margin: every within-group
|r̂| is > t and every cross-group |r̂| is < t (some t). Then blocks = groups.
*Proof.* Under the margin every distance 1 − |r̂| inside an unfinished group is below every distance between different groups,
so until all groups are complete an internal merge is available and every cross merge loses: the minimum distance is always
attained inside an incomplete group. Thus (a) complete linkage completes every group before any cross merge, each group is a node
of the dendrogram, and the dendrogram is laminar (ties inside either class are allowed). (b) Since g ≤ B_n, a group node is
retained by the top-down cut, and since B_n < 2g no union of groups is retained: the cut retains exactly the group nodes.
(c) Next-fit cannot put two groups of size g > B_n/2 into one bin: each group is packed alone. Hence blocks = groups. ∎

*Proof of Theorem R.* In LH-iid within-group population correlations equal ρ and cross-group ones are 0, ψ_i, ψ_iρ or ψ_iρ² in
absolute value, all ≤ ψ̄ < ρ. By Lemma R0 the complement of 𝒜_n is contained in the complement of the margin event, which is contained
in {∃ within pair (j,l): |r̂_jl| ≤ t} ∪ {∃ cross pair (j,k): |r̂_jk| ≥ t} for any t ∈ (ψ̄, ρ); the union bound gives (R-a).
For (R-b) the pairwise Gaussian laws suffice (no independence across pairs is used) and we cite **[W7-B]** (W7-PART Theorem B
and Corollary B, restricted to LH-iid; Corollary 1 of W7 (the two tails are monotone in |Σ_jk|) reduces each cross pair to ψ̄ and
each within pair to ρ, and W7 Lemma 2 (Hotelling density bounds) gives, for n ≥ 5, S(t*) ≤ K_n with the equal-rate threshold t*).
For (R-c): p²√n e^{−(n−4)I*} ≤ n^{2A+½} e^{−(n−4)I*} ≤ p^{−C} (as p^{−C} ≥ n^{−CA}) once
(2A + ½ + CA) log n + log(2/(√π(1−ρ))) ≤ (n−4)I*. For summability, K_n ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I*} ≤ (2/(√π(1−ρ))) e^{4I*} n^{2A+½}e^{−nI*}
directly (the bound p^{−C} alone would not give summability for arbitrarily slowly growing p). ∎

*Numbers.* With ρ=0.7 and ψ̄=0.5, direct substitution in the displayed formulas gives t*=0.6096117968 and I*=0.0125871528. At
(n,p)=(200,500), K_n=1.128102951×10⁶, hence the bound is vacuous (R39 #7: the W7 `results/union_bound.txt` artifact is not in
the archive; these values are recomputed in `Theory_work/Wave1C/C-PACK/numerics/R39_thmR_numbers.py` → `_out.txt`). As a historical W7 report claim (not independently available here), a Monte Carlo failure rate ≤ 1.5·10⁻⁴ at (200, 500, g = 10, ψ = 0.5) is reported
by W7-PART. The bound is explicit, not sharp.

## 2.4 Route (R′): a self-contained summable alternative to the W7 constant

**Corollary (R′).** On LH-iid with (SIZE) at n: put δ* := (ρ−ψ̄)/2 ∈ (0, ½) and t := (ρ+ψ̄)/2. On {max_{j<k}|r̂_jk − Σ_jk| < δ*}:
every within |r̂| > ρ − δ* = t and every cross |r̂| < ψ̄ + δ* = t, i.e. the strict global margin holds, and Lemma R0 (equivalently
W7 Theorem A (A4 ⇒ A1 ⇒ A3)) gives blocks = groups. Hence, by [CONC′] in its non-strict form (§1.2) at δ*, for every n ≥ 3 at which
SIZE holds,

  P(𝒜_nᶜ) ≤ 3p² exp(−(n−1)(ρ−ψ̄)²/4096).

Consequences: with p ≤ n^A, Σ_n P(𝒜_nᶜ) < ∞, and for every C > 0, P(𝒜_nᶜ) ≤ p^{−C} once log 3 + (2+C)A log n ≤ (n−1)(ρ−ψ̄)²/4096
(using p ≤ n^A for p^{2+C}); this is the summable form of (R) used in (S), (T), (C), (P). The exponent (ρ−ψ̄)²/4096 is far from I*
(crude constants); it is explicit and needs no Hotelling density. This route uses only [LM], the Gaussian tail and the deterministic
Lemma R0; it replaces only the probabilistic step of Theorem R.
