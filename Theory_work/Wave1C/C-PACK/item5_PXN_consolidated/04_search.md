# Part 4 — The search: Lemma Λ, Lemma U, (D_S), (L), Lemma LS, Theorem P6′. Conclusions (T) and (K)

Throughout, 𝔉_n := {A ⊆ [p] : |A| ≤ s₀ + 2}, |𝔉_n| ≤ (p+1)^{s₀+2} ≤ 2^{s₀+2}n^{A(s₀+2)}; J := s₀+2, D := A(s₀+2). (The letter A is both the
fixed exponent and a generic subset; see §0.2.) By §2.2, ℰ♯_n ⊆ ℰ(𝔉_n, φ₀) ∩ {‖μ‖² ≤ Mn}, so Lemma E applies to 𝔉_n on ℰ♯_n; its event
is 𝒟_search.

## 4.1 Lemma Λ (population residuals; the uniform sample-to-population step)

For B ⊆ 𝒮𝒱 put λ(B) := Var(μ | X_B) (population, per row) and λ_i(B) := Var(μ_i | X_B) for B ⊆ K_i.

**Lemma Λ.**
(a) max_{A∈𝔉_n} |Λ_A/n − λ(A ∩ 𝒮𝒱)| → 0 in probability.
(b) λ(B) = Σ_i λ_i(B ∩ K_i) + Σ_h (β^vis_h)² Var(x_{j_h} | X_{B∩V_h}).
(c) With G_i := ψ_i²β_i²(1−ψ_i²) and η_i := ρ²(1−ψ_i²)/(1−ψ_i²ρ²) ∈ (0,1):
   λ_i(∅) = λ_i({j_b}) = β_i²(1−ψ_i²); λ_i({j_a}) = G_i; λ_i({j_a, j_b}) = 0; λ_i({j_a, l}) = G_i for l ∈ C_a∖j_a;
   λ_i({j_a, l}) = G_i(1−η_i) for l ∈ C_b∖j_b (proxy); for B ⊆ K_i with |B| ≤ 2 and j_a ∉ B: λ_i(B) ≥ λ₀β_i²(1 + ψ_i²1{j_b∉B}).
   Visible: Var(x_{j_h} | x_l) = 1 − ρ² for l ∈ V_h∖j_h; = 0 if j_h ∈ B; = 1 if B ∩ V_h = ∅.

*Proof.* (a) Write A = A_s ∪ A_0, A_s := A ∩ 𝒮𝒱, A_0 ⊆ null groups, |A_0| ≤ s₀+2.
*Signal part:* Λ_{A_s}/(n−1) = θ*ᵀ[R̂ − R̂_{·A_s}R̂_{A_sA_s}⁻¹R̂_{A_s·}]θ* (restricted to 𝒮𝒱 coordinates) → λ(A_s) a.s. by the SLLN: there
are finitely many sets A_s (≤ 2^{gs₀}).
*Null part:* 0 ≤ Λ_{A_s} − Λ_A = ‖P_{span Π^⊥_{A_s}X_{A_0}} Π^⊥_{A_s}μ‖². The null columns X_{A_0} are independent of (X_{𝒮𝒱}, μ) (F5), so
given X_{𝒮𝒱} the vector r := Π^⊥_{A_s}μ is fixed and span(Π^⊥_{A_s}X_{A_0}) is Haar on the Grassmannian of |A_0|-planes of
1^⊥ ⊖ span X_{A_s} (the Haar step of Lemma B, with U = A_s, W = A_0; the null covariance Σ_{A_0} is positive definite also when A_0
contains several members of one null group). Indices with A_0 = ∅ or Λ_{A_s} = 0 are removed from the family below: their
increments are 0. For n−1 ≥ gs₀, Λ_{A_s} = 0 iff S₀ ⊆ A_s a.s., a deterministic index set. For the remaining indices,
(Λ_{A_s} − Λ_A)/Λ_{A_s} ~ Beta(|A_0|/2, (n−1−|A_s|−|A_0|)/2). This is a family of at most 2^{gs₀}(p+1)^{s₀+2} ≤ Cn^D Beta variables
(C = 2^{gs₀+s₀+2}) with 1 ≤ j = |A_0| ≤ J = s₀+2 and u = |A_s| ≤ s₀+2 ≤ n/4 — exactly the range of **Lemma Tr-J(c)**, which gives max ≤
τ_{n,D} = 8(D+1) log n/n w.p. → 1. Intersecting afterwards with {‖μ‖² ≤ Mn} (Λ_{A_s} ≤ ‖μ‖² ≤ Mn),
max_A(Λ_{A_s} − Λ_A) ≤ Mn τ_{n,D} = 8M(A(s₀+2)+1) log n = O(log n) = o(n), uniformly. No independence between the events is needed.
(b) F5.
(c) Direct Gaussian computations: Var(μ_i) = β²(1+ψ²−2ψ²); Var(μ_i|x_{j_a}) = ψ²β²Var(x_{j_b}|x_{j_a}); l ∈ C_a∖j_a adds nothing
by F3; for a proxy l, Cov(x_{j_b}, x_l|x_{j_a}) = ρ − ψ·ψρ = ρ(1−ψ²) and Var(x_l|x_{j_a}) = 1 − ψ²ρ², so
Var(x_{j_b}|x_{j_a}, x_l) = (1−ψ²)(1−η_i); the lower bound is λ_min(Σ_{K_i}) ≥ λ₀ times the squared norm of the coefficient vector
(β, −ψβ) restricted to {j_a, j_b} ∖ B. ∎

## 4.2 Lemma U (uniform score comparison on 𝔉_n)

**Lemma U.** On 𝒟_search ∩ ℰ♯_n (Lemma E with this (J, D)), for all A, A′ ∈ 𝔉_n with ||A| − |A′|| ≤ 2:
(U1) = (E4) with κ₂ := κ_E; (U2) = (E5);
(U3) if Λ_{A′}/n ≥ Λ_A/n + c′ for a fixed c′ > 0, then for n ≥ n₀(c′, σ², M, A, s₀)

  F(A) − F(A′) ≥ (n/2) log(1 + c′/(2(σ² + M))) − (2A + 1) log n − 2κ_E − 2 =: mar_n(c′) → +∞.

(mar_n(c′) is a score-margin function; it is distinct from the SE cutoff m_n of §2.1.)

*Proof of (U3).* Write H := σ² + M and e_n := C₂n^{−1/3}. By (E6), F(A) − F(A′) ≥ ν log(RSS_{A′}/RSS_A) − |Δprior| − |Δdet| − 2κ_E, with
|Δprior| = |log w(|A|) − log w(|A′|)| ≤ 2 log(2p) ≤ 2 log 2 + 2A log n (w(k+1)/w(k) = (k+1)/(2p−1−k) ∈ [1/(2p), 1]) and
|Δdet| ≤ log(n+1). By (U2), RSS_{A′}/RSS_A ≥ (nσ² + Λ_A + c′n − C₂n^{2/3})/(nσ² + Λ_A + C₂n^{2/3}) =
1 + (c′n − 2C₂n^{2/3})/(nσ² + Λ_A + C₂n^{2/3}) ≥ 1 + c′/(2H) for n ≥ n₀, using Λ_A ≤ ‖μ‖² ≤ Mn; a sufficient condition is
e_n ≤ c′H/(4H + c′), since then (c′ − 2e_n)/(H + e_n) ≥ c′/(2H). Then ν log(·) ≥ (n/2) log(1 + c′/(2H)). Finally for n ≥ 2,
2 log 2 + log(1 + 1/n) < 2, so |Δprior| + |Δdet| ≤ (2A+1) log n + 2. ∎

The RSS error is absorbed by halving the signal margin, and the constant is explicit.

## 4.3 The lattice margins (D_S for non-progress neighbours; ties among progress moves allowed)

Convention: min ∅ := +∞ (relevant when v = 0).

For S ∈ Lat(S°) ∖ {S₀} = {S° ∪ 𝓜′ : 𝓜′ ⊊ 𝓜} let I := {i : j_{b_i} ∉ S} ≠ ∅ and i* ∈ argmax_{i∈I} G_i. The **progress neighbours** of S are exactly
the additions S + j_{b_i}, i ∈ I (S ⊆ S₀ has no extras, so no deletion or swap lowers Φ). Put P* := S + j_{b_{i*}}. Every other neighbour A of S
(feasible flip or swap, A ∉ {S + j_{b_i} : i ∈ I}), and A = S itself, satisfies the **population margin**

  λ(A ∩ 𝒮𝒱) − λ(P* ∩ 𝒮𝒱) ≥ c₂ := min{ G_min, G_min(1 − η_max), c₄, min_i β_i²(1−ψ_i²)², min_i λ₀β_i², min_h (β^vis_h)²(1−ρ²) } > 0,

with G_min := min_i G_i, η_max := max_i η_i, c₄ := min{ min_i β_i²(1−ψ_i²)², min_i β_i²(1−ψ_i²), G_min, min_h (β^vis_h)² }.

*Proof (case list; λ(S) = Σ_{i∈I}G_i, λ(P*) = λ(S) − G_{i*}).*
- A = S: margin G_{i*} ≥ G_min.
- Add a neutral l (null-group member, a-group non-hub, visible non-hub): λ unchanged (Lemma Λ(c): an a-group member adds nothing given j_a; a
  visible member adds nothing given j_h; null independent). Margin G_{i*}.
- Add a proxy l ∈ C_{b_i}∖j_{b_i}: if i ∉ I nothing changes (pair complete); if i ∈ I, λ drops by G_iη_i ≤ G_{i*}η_max. Margin ≥ G_{i*}(1 − η_max) ≥ G_min(1−η_max).
- Delete a truth k ∈ S: λ rises by β_i²(1−ψ_i²)² (k = j_{a_i}, i ∈ I), β_i²(1−ψ_i²) (k = j_{a_i}, i ∉ I), G_i (k = j_{b_i}), or (β^vis_h)² (k = j_h).
  Margin ≥ c₄ + G_{i*} ≥ c₄.
- Swap k → l, l in a different component from k: the k-component rises by ≥ c₄. If the destination is an incomplete pair i′ ∈ I, its gain is at
  most G_{i′} ≤ G_{i*} (hub: G_{i′}; proxy: G_{i′}η_{i′}; a-group non-hub: zero). In a complete pair, visible component, or null group its gain is zero.
  Margin ≥ c₄ + G_{i*} − G_{i*} = c₄.
- Swap inside one component. Visible {j_h} → {l}: residual (β^vis_h)²(1−ρ²) > 0 = before; margin ≥ (β^vis_h)²(1−ρ²). Complete pair {j_a, j_b} → {j_a, l}:
  ≥ G_i(1−η_i) from 0; → {j_b, l}: ≥ λ₀β_i² from 0. Incomplete pair {j_a} → {l}, l ≠ j_b: λ_i({l}) − G_i + G_{i*} ≥ λ₀β_i²(1+ψ_i²); {j_a} → {j_b}:
  β_i²(1−ψ_i²) − G_i + G_{i*} ≥ β_i²(1−ψ_i²)². Margins ≥ c₂.
- Add j_{b_i}, i ∈ I ∖ {i*}: a progress neighbour; **excluded** from (D_S) (it may tie with P*; a tie does not obstruct progress, see Lemma LS). ∎

**Sample version.** Let Ω_n := ℰ♯_n ∩ 𝒟_search ∩ {max_{A∈𝔉_n}|Λ_A/n − λ(A ∩ 𝒮𝒱)| ≤ c₂/4} (P(Ω_n) → 1 by §2.2, Lemma E, Lemma Λ(a)). On Ω_n, for every
S ∈ Lat(S°)∖{S₀} and every non-progress neighbour A (and A = S): Λ_A/n ≥ Λ_{P*}/n + c₂/2, so by (U3) with (A, A′) := (P*, A) and c′ = c₂/2,

  F(P*) − F(A) ≥ mar_n(c₂/2) = (n/2) log(1 + c₂/(4(σ²+M))) − (2A+1) log n − 2κ_E − 2 > 0 for n ≥ n₀.                  (D_S)

All sets involved have size ≤ s₀ + 1 and lie in 𝔉_n, and sizes differ by ≤ 2. (D_S) holds simultaneously for all 2^c − 1 lattice states, because Ω_n is a
single event. (It needs mar_n(c₂/2) > 0, i.e. n ≳ (4A+2)(4(σ²+M)/c₂) log n.)

## 4.4 (L): S₀ is a strict local maximum

Let 𝒵_n := {max_{l∉S₀} Z_l² ≤ 2 log p + 2 log log n}, where Z_l := ũ_lᵀε/σ and ũ_l is the unit vector of Π^⊥_{S₀}x_l (defined a.s.).
Note c₅ below satisfies c₅ ≥ c₂ (each term defining c₅ is ≥ c₂).

**(L).** For n ≥ n₀, on Ω_n ∩ 𝒵_n no feasible flip or swap of S₀ attains a score ≥ F(S₀).

*Proof.* **Deletions and swaps.** Every deletion or swap A of S₀ misses a truth, so λ(A ∩ 𝒮𝒱) ≥ c₅ := min{ min_i β_i²(1−ψ_i²), G_min, min_h(β^vis_h)², G_min(1−η_max),
min_i λ₀β_i², min_h (β^vis_h)²(1−ρ²) } > 0 = λ(S₀) (the deletion and within-component cases of §4.3 with S = S₀). Since Λ_{S₀} = 0 (μ ∈ span X_{S₀}),
on Ω_n, Λ_A/n ≥ Λ_{S₀}/n + c₅/2, hence by (U3) F(S₀) − F(A) ≥ mar_n(c₅/2) > 0.

**Additions A = S₀ + l (corrected step).** Work on Ω_n ∩ 𝒵_n, with Lemma E applied to 𝔉_n. Since μ ∈ span X_{S₀}, Λ_{S₀} = 0 and RSS_{S₀} = ‖Π^⊥_{S₀}ε‖², and
RSS_{S₀+l} = RSS_{S₀} − σ²Z_l². By (E5), |RSS_{S₀} − nσ²| ≤ C₂n^{2/3} (C₂ = C₂(σ², M, A(s₀+2))), so for n ≥ n₀,

  RSS_{S₀} ≥ nσ²(1 − ε_n), ε_n := C₂n^{−1/3}/σ² = O(n^{−1/3}).

With x_l := σ²Z_l²/RSS_{S₀}: x_l ≤ (2 log p + 2 log log n)/(n(1−ε_n)) ≤ 3A log n/n ≤ ¼ for n ≥ n₀ (p ≤ n^A). Using −log(1−x) ≤ x + x² for x ≤ ½ (in fact
≤ x(1+2x) for x ≤ ¼ suffices) and ν = n/2 + 0.01:

  −ν log(1 − x_l) ≤ ν x_l(1 + x_l) ≤ (n/2 + 0.01) · Z_l²/(n(1−ε_n)) · (1 + 3A log n/n)
                 ≤ (Z_l²/2)(1 + 2ε_n)(1 + 3A log n/n)(1 + 0.02/n)      (ε_n ≤ ½)
                 ≤ Z_l²/2 + (Z_l²/2)·κ_n,   κ_n := O(n^{−1/3} + (log n)/n).

On 𝒵_n, Z_l²/2 ≤ log p + log log n ≤ A log n + log log n, so the additive remainder is (Z_l²/2)κ_n ≤ (A log n + log log n)·κ_n = O(n^{−1/3} log n + (log n)²/n) = o(1)
uniformly in l ∉ S₀ (A fixed). By (E6) with A = S₀ + l, A′ = S₀ (|R_A − R_{A′}| ≤ 2κ_E):

  F(S₀+l) − F(S₀) ≤ log((s₀+1)/(2p−1−s₀)) − ½ log(n+1) + log p + log log n + 2κ_E + o(1)
                  ≤ log(s₀+1) + log(p/(2p−1−s₀)) − ½ log n + log log n + 2κ_E + o(1)
                  = −½ log n + log log n + O(1) → −∞,

uniformly in l ∉ S₀ (p/(2p−1−s₀) ≤ 1 for p ≥ s₀+1). Combined with the deletion/swap case, (L) follows. ∎

**Probability of 𝒵_n.** Given X, Z_l ~ N(0,1) for each l ∉ S₀. With u_n² := 2 log p + 2 log log n and the Mills bound P(|N| > u) ≤ 2φ(u)/u,
P(𝒵_nᶜ | X) ≤ p · 2e^{−log p − log log n}/(√(2π) u_n) = 2/(√(2π) u_n log n) → 0. (No independence across l is needed; u_n → ∞ since p → ∞. u_n is
not a Tr-J threshold.)

*Remark.* The (L) part has the slow margin ½ log n − log log n − O(1). A first-order heuristic for addition failure is (s₀+1)/√(2π n w_n) with threshold
w_n := 2 log((2p−s₀−1)/(s₀+1)) + log(n+1) (W3-PXN, PROOF.md, 330–331; about 2.5% at (n, p, s₀) = (200, 750, 3)); the proof gives only P((L) fails) → 0.
The failure of (L) affects certification only, not scoring (Lemma LS(ii)).

## 4.5 Lemma LS (what the production search does on the lattice)

**The search.** The production local search from a centre S_c: scan every feasible flip and swap of the centre (every scanned model is scored); if the best
scanned score strictly exceeds F(S_c), move there (lexicographic ties) and count one move; repeat while moves < ℓ; after ℓ moves perform one further scan; stop
at the first scan with no strict improvement (`local_certified`); if the last scan still improves, set `local_limit`. With LS0, S_c = S̃₀ and the centre itself
is scored (emitted). An addition is infeasible only from a centre already of size K; every swap is scanned (engine: `CODE/cpp/v3_engine.h:400-420`). A scan at a centre of
size k evaluates at most p + k(p−k) models (p flips, k(p−k) swaps).

**Lemma LS.** Setting as above, with s₀ ≤ K (eventual: s₀ fixed, p → ∞, n → ∞). Suppose (D_S) holds for every S ∈ Lat(S°) ∖ {S₀} (progress ties allowed) and the centre
is S° with Φ(S°) = c ≥ 1.
(i) Every accepted move before the first arrival at S₀ adds one missing masked hub (states stay in Lat(S°)); the search makes min(c, ℓ) accepted moves before arrival
    or cap, and first reaches S₀ as a centre iff ℓ ≥ c, after exactly c moves.
(ii) S₀ is scored at the c-th scan, which is performed iff ℓ ≥ c − 1 (if c − 1 = ℓ it is the final scan). Hence S₀ ∈ 𝒮_LS0 whenever ℓ ≥ c − 1.
(iii) If moreover (L) holds and ℓ ≥ c, the search returns S₀ with `local_certified` and without `local_limit`, after exactly c accepted moves and c + 1 scans.

*Proof.* (i) At S ∈ Lat(S°) ∖ {S₀}, S ⊆ S₀ has no extras, so the only Φ-decreasing neighbours are additions of missing masked hubs (every swap and every deletion is
non-progress), and (D_S) makes the best scanned score strictly exceed F(S) and be attained only at such additions; the lexicographic rule picks one; Φ drops by 1. Each
such addition is feasible because |S| < s₀ ≤ K. So moves continue while the move count is < ℓ and the centre is not S₀: after min(c, ℓ) accepted moves either the centre
is S₀ (c ≤ ℓ) or the cap is reached (ℓ < c). No earlier scan stops the search (each found a strict improvement).
(ii) The c-th scan is the scan at the centre S° ∪ (𝓜 ∖ {one hub}), which contains S₀ = that centre + its last missing hub as a flip neighbour; scanned models are scored.
The scan at move count k = c − 1 is performed iff k < ℓ, or k = ℓ and it is the final scan.
(iii) After the c-th move the centre is S₀ (c ≤ ℓ moves); the next scan — inside the loop if c < ℓ, else the final scan — finds no strict improvement by (L); the search
stops with S₀ a scanned centre with no improving neighbour; there have been exactly c accepted moves and c + 1 scans. ∎

(Lemma LS is the lattice version of the deterministic descent of the best-improvement search, specialised to a centre without extras; it is proved here directly.)

## 4.6 Theorem P6′ — conclusions (T) and (K)

Let 𝒯_n := 𝒜_n ∩ Ω_n ∩ 𝒵_n ∩ {S̃₀ = S°}. Choose n₀ with ℓ_n = ⌈log₂(n+p+1)⌉ ≥ c and s₀ ≤ K for n ≥ n₀.

**Theorem P6′.** P(𝒯_n) → 1 and, on 𝒯_n, for n ≥ n₀: LS0 of R̄⁺ scores S₀ (this needs only the Ω_n-part (D_S) and ℓ_n ≥ c − 1), reaches S₀ after exactly c moves and returns it
with `local_certified`, using c + 1 scans and

  N_scores ≤ 1 + Σ_{t=0}^{c} [p + (s+t)(p − s − t)] ≤ 1 + (c+1)(p + s₀p).

On arbitrary data, N_scores ≤ 1 + (ℓ_n+1) max_{0≤k≤K}[p + k(p−k)] = O(p² log(n+p)).

*Proof.* P(𝒯_n) → 1 is a union bound of vanishing complements — P(𝒜_nᶜ) → 0 (Theorem R or (R′)), P(ℰ♯_nᶜ) → 0 (Lemma 2.2), P(𝒟_searchᶜ ∩ ℰ♯_n) → 0 (Lemma E),
P(max|Λ_A/n − λ| > c₂/4) → 0 (Lemma Λ(a)), P(𝒵_nᶜ) → 0 (§4.4), P(S̃₀ ≠ S°) → 0 (P5); no independence is used. On 𝒯_n, by Lemma T the LS0 centre is S̃₀ = S°, with
Φ(S°) = c; (D_S) holds on Ω_n for every lattice state (§4.3) and (L) holds on Ω_n ∩ 𝒵_n (§4.4); Lemma LS(i)–(iii) with ℓ_n ≥ c gives arrival after exactly c moves,
scoring of S₀ (already for ℓ_n ≥ c − 1), and certification after c + 1 scans. Count: the centres are the lattice states of sizes s, s+1, …, s+c = s₀, one scan at each (c + 1
scans), a scan at size k evaluating at most p + k(p−k) models, plus one evaluation of the initial centre; since s + t ≤ s₀ and p − s − t ≤ p, each term is ≤ p + s₀p. The
general bound: at most ℓ_n + 1 scans, each at a centre of some size k ≤ K, plus the centre evaluation; max_k k(p−k) ≤ p²/4 and ℓ_n = ⌈log₂(n+p+1)⌉ give O(p² log(n+p)). ∎

**Conclusions.** P(LS0 of R̄⁺ scores S₀) ≥ P(𝒯_n) → 1 and P(LS0 returns S₀ with `local_certified`) ≥ P(𝒯_n) → 1: this is (T). The cost statement (K) is the last display, and the
c + 1 scans and ≤ 1 + (c+1)(p + s₀p) scores hold on the joint event 𝒯_n (lattice arrival, (L), ℓ_n ≥ c), not merely on {LS0 scores S₀}.
