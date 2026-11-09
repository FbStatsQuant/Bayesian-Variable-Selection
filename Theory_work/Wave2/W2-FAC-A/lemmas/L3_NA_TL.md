# L3 — NA and TL on the full lattice 𝓛 = [S₀, [p]]

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09; lemma check R03 (Codex gpt-6.1-sol high,
reviews/R03_L2L3L4_check_sol.md): VERIFIED-WITH-AMENDMENTS (2 MINOR), applied. Inputs: L1 (Corollary U).
Falsification: numerics/fna_check.py → FNA_summary.md; R03's independent exhaustive envelope check (0 violations).

Hypotheses (minimal list): model G; s₀ ≥ 1 fixed; ‖μ‖² ≤ Mn; (AG) with Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄) and
δ_n√(p log log n) → 0; (P) limsup log p/log n < α₀(κ̄); for TL in addition BM-∞:
θ*²_min n/log n → ∞ (θ* fixed nonzero suffices). Constants: φ² := 3ψ₀/4.

## L3.0 Uniform score expansion (deterministic, for every A ⊆ [p])

Let n be so large that δ_n ≤ ψ₀/4, so λ_min(R̂) ≥ φ², and K = p (true eventually under (P), since p = o(n)); hence every A ⊆ [p] is feasible (R03 item 1).
Write y = Y/s_Y with Y = μ + Cε, s_Y² = ‖Y‖²/(n − 1); RSS_A := ‖(I − P_A)y‖²; ν = 0.01 + n/2.

**(E1)** ½[log det H_A − log det(G_A + I)] = ½|A| log(n + 1) + ρ_A with −|A|/(2(n − 1)φ²) ≤ ρ_A ≤ 0.
*Proof.* With eigenvalues ν_i ≥ (n − 1)φ² of G_A, the left side is ½Σ_i log(((n + 1)ν_i + 1)/(ν_i + 1)) =
½Σ_i[log(n + 1) + log((ν_i + 1/(n+1))/(ν_i + 1))], and 0 ≥ log((ν + 1/(n+1))/(ν + 1)) ≥ −log(1 + 1/ν) ≥ −1/ν. ∎

**(E2)** Q_A = RSS_A + ω_A with 0 ≤ ω_A ≤ (1 + 1/((n − 1)φ²))·(n − 1)/(n + 1) ≤ 2.
*Proof.* With z = X_Aᵀy, G = G_A, ε := 1/(n + 1): Q_A = yᵀy − n zᵀH_A⁻¹z, nH_A⁻¹ = (1 − ε)(G + εI)⁻¹, RSS_A =
yᵀy − zᵀG⁻¹z, so ω_A = zᵀ{[G⁻¹ − (G + εI)⁻¹] + ε(G + εI)⁻¹}z. Both brackets are PSD; G⁻¹ − (G + εI)⁻¹ =
εG⁻¹(G + εI)⁻¹ ⪯ εG⁻² ⪯ (ε/((n − 1)φ²))G⁻¹ and ε(G + εI)⁻¹ ⪯ εG⁻¹. Hence 0 ≤ ω_A ≤ ε(1 + 1/((n−1)φ²))zᵀG⁻¹z and
zᵀG⁻¹z = yᵀP_Ay ≤ yᵀy = n − 1. ∎

**Event E_Y.** ‖Cε‖²/σ² ≥ n − 1 − 2√((n − 1) log n), ‖P_{[p]}Cε‖²/σ² ≤ p + 2√(p log n) + 2 log n, and
‖Cε‖² ≤ 2σ²n. By Laurent–Massart (χ²_{n−1} and χ²_{rank ≤ p}; for the last, the upper bound with x = n/8),
P(E_Yᶜ) ≤ 2/n + e^{−n/8} → 0. On E_Y: s_Y² ≤ (√M + σ√2)²·n/(n − 1) =: s̄² (bounded), and for every T ⊇ S₀,
since (I − P_T)μ = 0,
  RSS_T = ‖(I − P_T)Cε‖²/s_Y² ≥ σ²(n − 1 − p − 4√(n log n) − 2 log n)/s_Y² =: σ²n(1 − η_n)/s_Y²,  η_n → 0.  (0.1)

## L3.1 NA

**Lemma L3.1.** On E_n (Corollary U) ∩ E_Y, for n ≥ n₀: NA(𝓛) holds. Hence P(NA(𝓛)) → 1.

*Proof.* Let T ∈ 𝓛, |T| = k (s₀ ≤ k ≤ p − 1 < K), l ∉ T, A := T ∪ {l}. Since u_{T,l} ⊥ span(X_T) ∋ μ and u ⊥ 1,
RSS_T − RSS_A = (u_{T,l}ᵀy)² = σ²Z²_{T,l}/s_Y². By (E1), (E2), w(k+1)/w(k) = (k+1)/(2p − 1 − k), and
log(a/b) ≤ (a − b)/b:
  2[F(A) − F(T)] = 2 log((k+1)/(2p−1−k)) − log(n+1) − 2(ρ_A − ρ_T) + 2ν log((0.02 + Q_T)/(0.02 + Q_A))
               ≤ −2 log((2p−1−k)/(k+1)) − log(n+1) + (p+1)/((n−1)φ²) + 2ν[σ²Z²_{T,l}/s_Y² + 2]/RSS_A.
By (0.1) (A ⊇ S₀), 2ν/RSS_A ≤ (n + 0.02)s_Y²/(σ²n(1 − η_n)), so the last term is ≤ Z²_{T,l}(1 + η'_n) + C_ω with
η'_n → 0 and C_ω := 4s̄²/σ² (n ≥ n₀). Hence NA holds at (T, l) as soon as
  Z²_{T,l}(1 + η'_n) < log(n + 1) + 2 log((2p − 1 − k)/(k + 1)) − C_ω − 1.                                   (1.1)
On E_n, Corollary U gives |Z_{T,l}| ≤ √(2P) + κ̄√(2x_k) + ε_n with P := log p, x_k := log(p/k) ∈ [0, P] and
ε_n := [√(2 log(p2^{γ̄}) + 2 log log n) − √(2P)] + κ'√(2 log log n) + κ̄(√(2 log(e γ̄)) + ϱ_n) + L_ψδ_n√(5(p+1) log log n)
= o(√log n) (using √(2 log(eγ̄p/k)) ≤ √(2x_k) + √(2 log(eγ̄)) and ϱ_n = O((log p)^{1/4} + (log log n)^{1/2})).
Also 2p − 1 − k ≥ p and k + 1 ≤ 2k, so 2 log((2p − 1 − k)/(k + 1)) ≥ 2x_k − 2 log 2.
Fix α₁ < α₀ := α₀(κ̄) with P ≤ α₁L eventually (L := log n), and ε ∈ (0, 1/12) with 1/α₀ + 6ε ≤ (1 − 3ε)/α₁
(possible since α₁ < α₀). Put s := √(x_k/P) ∈ [0, 1] (if P = 0, i.e. p = 1, NA is trivial since 𝓛 = {[p]} or has
no additions). Then (√(2P) + κ̄√(2x_k))² = 2P(1 + κ̄s)² = 2P[(1 + κ̄s)² − s²] + 2x_k ≤ P/α₀ + 2x_k by the
definition of α₀. Moreover P/α₀ ≤ ((1 − 3ε)/α₁ − 6ε)P ≤ (1 − 3ε)L − 6εP, and 2x_k − 6εP ≤ (1 − 3ε)2x_k (x_k ≤ P), so
  (√(2P) + κ̄√(2x_k))² ≤ (1 − 3ε)(L + 2x_k).
Since this quantity is O(L) and ε_n = o(√L), (|Z| bound)²(1 + η'_n) ≤ (1 − 2ε)(L + 2x_k) for n ≥ n₀. The right
side of (1.1) is ≥ L + 2x_k − 2 log 2 − C_ω − 1. So (1.1) holds once 2εL > 2 log 2 + C_ω + 1, uniformly in T, l. ∎

*Remark (where α₀ comes from).* The worst case is s = 1, i.e. k = O(1)·p^{o(1)}: then the prior pays 2 log p
per addition, the idiosyncratic maximum costs 2 log p and the factor term costs up to κ̄√(2 log p); for κ̄ = 1
this is (2√(2P))² = 8P against L + 2P, i.e. P < L/6. Part II (lemmas/L6_sharp.md) shows this is attained.

## L3.2 TL

**Lemma L3.2.** Assume in addition BM-∞. On E_n ∩ E_Y, for n ≥ n₀: TL(𝓛) holds. Hence P(TL(𝓛)) → 1.

*Proof.* Let T ∈ 𝓛, i ∈ S₀, B := T ∖ {i}, and A = B or A = B ∪ {l} with l ∉ T. Since μ − θ*_ix_i ∈ span X_B,
(I − P_B)Y = θ*_i(I − P_B)x_i + (I − P_B)Cε. In both cases put a := ‖(I − P_B)x_i‖ (a² ≥ (n − 1)φ², a ≤ √(n − 1)) and
Z₁ := Z_{B,i}. In the swap case only (l ∉ T selected; R06 item 17) put b := u_{B,l}ᵀx_i, Z₂ := Z_{B,l}; then a² − b² =
‖(I − P_{B∪l})x_i‖² ≥ (n − 1)φ² (Gram floor; Pythagoras) and |b| ≤ a:
  s_Y²(RSS_B − RSS_T) = (θ*_ia + σZ₁)² ≥ θ*²_i a²/2 − σ²Z₁²,
  s_Y²(RSS_{B∪l} − RSS_T) = (θ*_ia + σZ₁)² − (θ*_ib + σZ₂)² ≥ θ*²_i(a² − b²) − 2|θ*_i|σ√(n−1)(|Z₁| + |Z₂|) − σ²Z₂².
On E_n, |Z₁|, |Z₂| ≤ Z̄_n := √(2 log(p2^{γ̄}) + 2 log log n) + κ'√(2 log log n) + κ̄(√(2 log(eγ̄p)) + ϱ_n) + o(1)
= O(√log n). By BM-∞, θ*²_i(n − 1)φ² / log n → ∞, so in both cases RSS_A − RSS_T ≥ τ_n := θ*²_min(n − 1)φ²/(4s̄²)
for n ≥ n₀, and τ_n/log n → ∞. Then
  2[F(A) − F(T)] ≤ 2 log(2p) + log(n + 1) + (p+1)/((n−1)φ²) − 2ν log((0.02 + Q_A)/(0.02 + Q_T)),
using log(w(k−1)/w(k)) = log((2p − k)/k) ≤ log(2p) (swaps: 0) and −(|A| − |T|) log(n+1) ≤ log(n + 1). By (E2),
Q_A − Q_T ≥ τ_n − 2 and 0.02 + Q_T ≤ n + 1.02, so 2ν log((0.02 + Q_A)/(0.02 + Q_T)) ≥ n log(1 + (τ_n − 2)/(n + 1.02))
≥ (n/(n + 1.02))·(τ_n − 2)/2 (for τ_n − 2 ≤ n + 1.02; otherwise ≥ n log 2), which is ≫ log n. Hence F(A) < F(T)
for n ≥ n₀, uniformly. ∎

## L3.3 Probability
P((E_n ∩ E_Y)ᶜ) ≤ 4/log n + 2/n + e^{−n/8} → 0 (E_n from Corollary U, conditional on X, integrated; R03 item 3).
