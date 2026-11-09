# X9 — Iid rows with general one-factor loadings: uniform transfer of Lemma L4r-S (claim (G2)(R) of STATEMENT_T2)

Status: **PROVED (by this seat, unchecked)**; key-lemma check R11 (Codex Sol xhigh, reviews/R11_L4rS_X9_check_sol.md):
VERIFIED-WITH-AMENDMENTS (2 MINOR for X9, applied; R11's third MINOR concerned T2/STATEMENT_T2.md §2, also applied). Falsification numerics: numerics/N2X_summary.md ('iid' runs: 32/32 pure
deletions to S₀ with heterogeneous loadings); T2/numerics/N_T2_summary.md (exact Gram).

Setting: STATEMENT_T2 (model (R), (1F), (θ), (P-S): p ≤ n^{A₁}, A₁ < A_S ≤ 1/6). T2/L4r_path.md = the exact-Gram proof
(Lemma L4r-S). Notation of X1–X2 (N := n − 3, W, a, φ, η, ξ, e, M_T, e¹, ε^d, r) with general loadings: ℓ_j ∈ [ℓ_lo, ℓ_hi].

## X9.1 Representation and reference (general loadings)

As X7 (representation paragraph): with the frame (e₁, e₂) of X1.1, g_j = (λ_jη + √ψ_jξ_j)e₁ + (λ_jφ + √ψ_ja_j)e₂ + √ψ_ju_j^⊥,
G^r_T = Ψ_T^{1/2}[ṽ1ṽ1ᵀ + A_T]Ψ_T^{1/2}, ṽ1 := ξ + ℓη, ṽ2 := ℓφ + a, A_T := W_T + ṽ2ṽ2ᵀ, W ~ W_p(N, I) independent of
(‖e‖, η, φ, ξ, a) (X1.1's proof never uses equal loadings). Column scalings leave spans and partial statistics unchanged,
so X1.2 holds verbatim: RSS_T = ‖e‖²/(1 + q_T), q_T − q_{T∖j} = ω_j(T)². X1.4 (g1)–(g3) hold verbatim (they use only
λ_min(G_T) ≥ c₀(n − 1), here c₀ := ψ_lo/5 on the event of X9.2, the s² bounds and the RSS identities); written with
Nω_j² (note (1 + γ_{k−1})M_T τ̂² = M_T Nω² in X1.4's notation):
  G_del(j; T) = Δ_k − ½e¹_j(T) − ν log(1 + M_T(1 + ε^d_j)Nω_j(T)²/ν + r_j/ψ_T),  G_add(l; T) = −G_del(l; T ∪ l),
  G_sw(j, l) = G_del(j; T) + G_add(l; T ∖ j)  (telescoping, exact).
**Reference.** Replacing W_T by NI and a by 0: N(A⁰_T)⁻¹ṽ1 = (ξ_j − ℓ_jX_T)_{j∈T} and N((A⁰_T)⁻¹)_jj = 1 − ℓ_j²/D_T with
  X_T := (ℓ_Tᵀξ_T − ϱ)/D_T,  D_T := ‖ℓ_T‖² + κ₀,  κ₀ := N/φ²,  ϱ := Nη/φ²
(Sherman–Morrison: (NI + φ²ℓℓᵀ)⁻¹ = N⁻¹(I − φ²ℓℓᵀ/(N + φ²‖ℓ‖²)) and φ²(ℓᵀξ + η‖ℓ‖²)/(N + φ²‖ℓ‖²) − η = X_T). Put
s_j(T) := (ξ_j − ℓ_jX_T)/(1 − ℓ_j²/D_T)^{1/2} and δ_j(T) := √N ω_j(T) − s_j(T). Drift: X_{T∪l} = X_T + ℓ_l(ξ_l − ℓ_lX_T)/(D_T + ℓ_l²),
X_{T∖j} = X_T − ℓ_j(ξ_j − ℓ_jX_T)/(D_T − ℓ_j²). This is L4r.0's structure with ε_j ≡ 1 and κ₀ = N/φ² ∈ [½, 2] (instead of 1);
in particular s_l(T ∪ l)² = (1 − ℓ_l²/(D_T + ℓ_l²))(ξ_l − ℓ_lX_T)² — L4r.0(c)'s addition statistic.

## X9.2 Event and uniform perturbation bound

𝔈_n^G := D1–D4 of X2.1 (with H̄² := 2 log(2m_all + 2) + 2L_n, |η|, |ξ_{S₀}| ≤ √(2L_n), max|a_j| ≤ 2√(log n),
|φ²/N − 1| ≤ n^{−1/3}) ∩ {E4′ of T2/L4r_path.md: ζ_(i)² ≤ Z_i² for all i}. P(𝔈_n^G) → 1 (X2.1, FACB L3.1). On it:
**centre bound** |X_T| ≤ (Z_m² + 2)^{1/2}/ℓ_lo + C√L_n ≤ C_X9H̄ for every T ⊇ S₀ with m = |T ∖ S₀| ≥ 1, and |X_{S₀}| ≤ C√L_n
(L4r.2(b)'s Cauchy–Schwarz proof, the truths' terms ℓ_iξ_i (i ∈ S₀) and ϱ being O(√L_n)).

**Lemma X9.2.** On 𝔈_n^G, n ≥ n₀: for every T with S₀ ⊆ T ⊆ [p] (or T ∪ l, l ∉ T) and every null j ∈ T,
  |δ_j(T)| ≤ δ̄_n := C_9(p/√n + √(p log n/n) + √(log n/n))H̄,  and δ̄_nH̄ → 0 (A₁ < ½).
*Proof.* X2's Proposition X2 proof, steps (i), (ii), (iii), (v) verbatim with the vector b⁰ := φℓ_T/√N (instead of
ℓφ1/√N): (i) uses only c⁰ = ṽ1 − b⁰S(b⁰), b⁰_jS(b⁰) = ℓ_j(η + X_T) (so |S(b⁰)| ≤ 2(|η| + |X_T|)), ‖α‖_∞ ≤ 2√(log n/N)
and 1 + ‖b‖² ≥ ℓ_lo²k/2; (v) uses (B₀⁻¹)_jj ≥ 1/(1 + b_j²) ≥ 1/(1 + 2ℓ_hi²). **Step (iv) is replaced by the structure-free
bound** |(Rc)_j| ≤ ‖R‖‖c‖ ≤ r_n(‖c⁰‖ + ‖c − c⁰‖) with ‖c⁰‖² = Σ_{i∈T}(ξ_i − ℓ_iX_T)² ≤ k(H̄ + ℓ_hi|X_T|)² and k ≤ p:
r_n√p(1 + ℓ_hi C_X9)H̄ ≤ C(p/√n + √(p log n/n))H̄. Second order ≤ r_n²‖c‖ ≤ C(p^{3/2}/n + √p log n/n)H̄ ≤ C(p/√n + √(log n/n))H̄ for p ≤ √n (R11 item 1). Collect. Since
p ≤ n^{A₁} with A₁ < ½ and H̄² = O(log n), δ̄_nH̄ → 0. ∎
(No band structure, no Gaussian conditioning over ξ-defined sets and no path information is used: the bound is uniform
over all sets, which is what the uniform argument of L4r.3 needs. Its price, p/√n, is affordable because A₁ < A_S ≤ 1/6.)

## X9.3 Lemma L4r-S under iid rows

**Lemma X9.** Under (R), (1F), (θ), (P-S), on 𝔈_n^G ∩ {s² ∈ [s_min², s_max²]} ∩ (X5-type events for λ_min, here
λ_min(R̂) ≥ c₀ from D1–D4), n ≥ n₀: items 1–5 of T2/STATEMENT_T2 §3 (L4r-S) hold for every T with S₀ ⊆ T ⊆ [p], except that
"the within-loading-value argmin" is replaced by "a null deletion maximising G_del" (the iid perturbation is not
constant within a loading value). Hence (G2)(R).
*Proof.* Follow T2/L4r_path.md §L4r.3 with τ_j(T)²(1 + γ'_j(T)) replaced by Nω_j(T)² = (s_j(T) + δ_j(T))²,
|δ| ≤ δ̄_n, and with X1.4's errors (|e¹| ≤ 3/(c₀n), ε^d ≤ 2ω² ≤ C H̄²/n, |r/ψ| ≤ Cn^{−5/2}(1 + H̄²)) and multiplier bound
M_T ≤ ½(1 + C/n) (X1.4 (g3); replaces L4r.1 (s4)):
(i) *Deletions.* L4r.2(a) holds for the reference: Σ_{i∈K_T}ℓ_i(ξ_i − ℓ_iX_T) = X_T(κ₀ + Σ_{S₀}ℓ_i²) + ϱ − Σ_{S₀}ℓ_iξ_i, so some
kept i has |ξ_i − ℓ_iX_T| ≤ H̄ + C√L_n/ℓ_lo; then Nω_i² ≤ (1 + γ_m)(H̄ + C√L_n)² + 2δ̄_n·CH̄ + δ̄_n² with
γ_m := ℓ_hi²/(κ₀ + Σ_{S₀}ℓ² + (m − 1)ℓ_lo²) ≤ γ̄(1 + o(1)) (κ₀ ≥ 1 − n^{−1/3}; the proof's γ̄ uses κ₀ = 1 — the ratio is
1 + O(n^{−1/3})). The rest of L4r.3(i) is unchanged: G_del(i; T) ≥ (½ − A₁max(1, γ̄))log n − o(log n).
(ii) *Additions.* G_add(l; T) ≤ −Δ_{k+1} + 3/(c₀n) + ½(1 + C/n)(1 + CH̄²/n)(|s_l(T ∪ l)| + δ̄_n)² (absolute value, R11 item 2) + o(1), and
s_l(T ∪ l)² ≤ τ_l² := (ξ_l − ℓ_lX_T)², |τ_l| ≤ H̄ + ℓ_hi|X_T|, with the centre bound of X9.2; L4r.3(ii)'s computation
gives G_add ≤ −(½ − A₁((1 + R)² − 1))log n + o(log n), also at T = S₀.
(iii) *Swaps.* Exact telescoping and (ii) at T ∖ j: G_sw ≤ G_del(j; T) − c_add log n.
(iv) *Truth moves.* X4.6's argument with λ_min(G^r_U) ≥ ψ_loN/2 and ‖P_Ue‖ ≤ C√pH̄ (general loadings): negative.
(v) *At S₀:* as L4r.3(v). Paths: as L4r.3(vi) (every maximiser is a null deletion; uniform over starts, so the random
N₀ is irrelevant; caps by the single-search prefix property). ∎
