# W3-DIST — Theorem DIST-3 (oracle bound with an additive selection error; parametric rate) — stream B

**Status: DRAFT (by this seat, unchecked).** Author: stream B (Claude Opus 5.5, Claude Third). Target: STATEMENT.md
v1.3.1 §1 "Theorem DIST-3" (lines 93–104), with ROUTES.md §3. Uses Lemma H (`H.md`, this folder; DRAFT). Notation:
STATEMENT §0 and API_CARDS "Common definitions" (binding).

## Clarifications requested (no mathematical change; tag EQUAL)

These are not STATEMENT-CHANGE REQUESTS: the theorem is proved as stated. They make the quantifiers explicit.
1. **Letter clash.** In (TR₀) the direction is called u, and u is also the deviation level. Below the direction is
   called w: (TR₀; C_T) = { E_x(a + wᵀx)² ≤ C_T·n⁻¹Σ_i(a + wᵀx_i)² for all a ∈ ℝ and all w ∈ ℝ^{p_raw} with supp w ⊆ supp β* }.
2. **Constants.** The proof gives c = 1; C and n₀ are explicit (§1). n₀ depends on (s₀^r, σ*², M, B, κ₀); the radius
   constant also on C_T. Neither depends on A, p_raw, p_ret or on the design beyond the four events; p ≤ n^A and the
   event 𝒟_n are not used (𝒟_n only makes the object the one of §0).
3. **In-probability corollary.** (M, B, C_T, κ₀) are fixed (do not depend on n); "the four design events have
   probability → 1" means P*(𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T)) → 1.

## 0. Setting and the inherited premise

Fixed design first: X^r is fixed and ε ~ N_n(0, σ*²I) (in the random-design part, ε is independent of X^r, STATEMENT
§0 (RD)). The objects (C, U, N = n − 1, retained columns, ŝ_j, X, μ = CX^rβ*, θ*, S₀ = supp θ*, s₀, y_c = μ_c + e,
G_S, H_S, M_S, P_S, Q^c_S, L_S, K, Ω, b, ν) are those of API_CARDS lines 5–17 and H.md §H.0. In particular
e = Uᵀε, μ_c = Uᵀμ, ε̄ = n⁻¹1ᵀε, a₀ := b₀ := 0.01, ν = a₀ + n/2, b = b₀s_y², s_y² = ‖y_c‖²/N.

**Premise (P-T01; the only inherited premise; STATEMENT.md:390–391).** For S ∈ Ω the conditional posterior of the coded
prior given (S, D_n), on the response scale, is: v | S, D_n ~ IG(ν, β_S), β_S := b + Q^c_S/2, and
θ | v, S, D_n ~ N(θ̂_S, nvH_S⁻¹), θ̂_S := nH_S⁻¹X_{c,S}ᵀy_c (API_CARDS.md:13; [D] D0, `W3-POST2/lemmas/D_hellinger.md:8–11`,
from [P1] `thm:T01i`, locked). It is well defined when y_c ≠ 0 (then b > 0). The density attached to a draw and d_H are
those of STATEMENT §0 / H.md §H.0.

**Constants.** With k_s := 4 + 2s₀^r log 2 and b̄ := 4b₀(M + σ*²):
  C_ρ := 2b̄/σ*² + 2a₀ + 1 + 2√2 + k_s + 2√(2B)/σ* + B/σ*²,   C_v := 2(C_ρ + 2√2),   C_μ := 8σ*²k_s + 4B,
  C_rad := ( C_v² + C_T(2σ*² + C_μ)/(4σ*²) )^{1/2},   C := max{C_rad, 7},   c := 1,
  n₀ := max{3, 2s₀^r, ⌈C_v^{2/κ₀}⌉}.

## 1. Statement proved

**Theorem DIST-3 (explicit form).** Let n ≥ n₀, u ∈ [1, n^{1−κ₀}] real, and let X^r be a design in
𝒢_n := 𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T). There is a noise event 𝓔_u = 𝓔_u(X^r) with P(𝓔_uᶜ) ≤ 7e^{−u} on which
π(S₀) > 0 and, with 𝔅_u := {(S, θ, v) : d_H(f_{S,θ,v}, f*) > C_rad√(u/n)}:
  (a) Π(𝔅_u | S = S₀, D_n) ≤ 3e^{−u};
  (b) Π(𝔅_u | D_n) ≤ δ_n + 3e^{−u},  δ_n := 1 − π(S₀).
Since C ≥ C_rad and C ≥ 7, this is STATEMENT's DIST-3 display with (c, C) = (1, C).
**Corollary DIST-3(R) (random design).** In (RD), for n ≥ n₀ and u ∈ [1, n^{1−κ₀}]:
  P*( {X^r ∈ 𝒢_n} ∩ [ {Π(𝔅_u | S₀, D_n) > 3e^{−u}} ∪ {Π(𝔅_u | D_n) > δ_n + 3e^{−u}} ] ) ≤ 7e^{−u}.
**Corollary DIST-3(P) (in probability).** If (M, B, C_T, κ₀) are fixed, P*(𝒢_n) → 1 and δ_n → 0 in P*-probability, then
for every sequence M_n → ∞: Π(d_H(f, f*) > M_n/√n | D_n) → 0 in P*-probability.

## 2. Tools (each with proof)

**(G1)** Z ~ N(0, 1), x ≥ 0: P(|Z| > x) ≤ 2e^{−x²/2}. *Proof.* P(Z > x) ≤ e^{−λx}Ee^{λZ} = e^{−λx + λ²/2}; λ = x; symmetry. ∎
**(G2)** ξ₁, …, ξ_r i.i.d. N(0, 1), λ_k ∈ [0, 1]: P(Σ_kλ_kξ_k² > x) ≤ 2^{r/2}e^{−x/4} for every x. *Proof.*
Ee^{λ_kξ_k²/4} = (1 − λ_k/2)^{−1/2} ≤ 2^{1/2}; Markov applied to e^{Σλ_kξ_k²/4}. ∎ (r = 0: the sum is 0.)
**(G3)** G ~ Gamma(α, 1), α > 0. For 0 < t ≤ α: P(G − α ≥ t) ≤ e^{−t²/(4α)}. For t > 0: P(α − G ≥ t) ≤ e^{−t²/(2α)}.
*Proof.* For λ ∈ [0, 1): log Ee^{λ(G−α)} = α(−log(1 − λ) − λ) = αΣ_{j≥2}λ^j/j ≤ (αλ²/2)Σ_{j≥0}λ^j = αλ²/(2(1 − λ)) ≤ αλ²
if λ ≤ ½. Markov with λ := t/(2α) ≤ ½: P(G − α ≥ t) ≤ e^{−λt + αλ²} = e^{−t²/(2α) + t²/(4α)} = e^{−t²/(4α)}. For λ ≥ 0:
log Ee^{−λ(G−α)} = α(λ − log(1 + λ)) ≤ αλ²/2 (log(1 + λ) ≥ λ − λ²/2 for λ ≥ 0); Markov with λ := t/α gives e^{−t²/(2α)}. ∎
**(G4)** χ²_N, N ≥ 1, 0 < u ≤ N/8: P(|χ²_N − N| > 2√(2Nu)) ≤ 2e^{−u}. *Proof.* χ²_N = 2G with G ~ Gamma(N/2, 1). With
α = N/2 and t := √(2Nu): t ≤ α ⟺ 8u ≤ N. By G3, P(G − α ≥ t) ≤ e^{−t²/(2N)} = e^{−u} and P(α − G ≥ t) ≤ e^{−t²/N} ≤ e^{−u};
{|χ²_N − N| > 2t} ⊆ {|G − α| ≥ t}. ∎
**(M1) Spectrum of M_S.** Let X_{c,S} = Σ_{k=1}^{r}s_kφ_kψ_kᵀ (singular value decomposition, s_k > 0, r = rank X_{c,S}
≤ |S|). Since UᵀU = I, G_S = X_SᵀX_S = X_{c,S}ᵀX_{c,S} = Σ_ks_k²ψ_kψ_kᵀ, and H_S = (n + 1)G_S + I has eigenvalue
(n + 1)s_k² + 1 on ψ_k and 1 on span{ψ_k}^⊥. Hence H_S⁻¹X_{c,S}ᵀ = Σ_ks_kψ_kφ_kᵀ/((n + 1)s_k² + 1) and
  M_S = nX_{c,S}H_S⁻¹X_{c,S}ᵀ = Σ_k λ_kφ_kφ_kᵀ,  λ_k := ns_k²/((n + 1)s_k² + 1) ∈ (0, 1).
With P_S = Σ_kφ_kφ_kᵀ (projection onto col X_{c,S}): 0 ⪯ M_S ⪯ P_S, M_S² ⪯ M_S, 0 ⪯ I − M_S ⪯ I and (I − M_S)² ⪯ I − M_S. ∎
**(M2) Conditional law of the fitted mean.** Given (v, S, D_n), X_{c,S}θ ~ N(M_Sy_c, vM_S): mean X_{c,S}θ̂_S = M_Sy_c and
covariance X_{c,S}(nvH_S⁻¹)X_{c,S}ᵀ = vM_S. Hence ‖X_{c,S}(θ − θ̂_S)‖²/v has the law of Σ_{k≤r}λ_kξ_k², ξ_k i.i.d. N(0, 1).

## 3. Proof of the theorem (fixed design)

Fix n ≥ n₀, u ∈ [1, n^{1−κ₀}] and X^r ∈ 𝒢_n. Write M := M_{S₀}, P := P_{S₀}, Q := Q^c_{S₀}, L := L_{S₀} ≤ B,
a₀' := (I − M)μ_c, r₀ := rank X_{c,S₀} ≤ s₀ ≤ s₀^r, R := supp β*.

**Step 0 (range facts used repeatedly).** (i) n ≥ 2s₀^r gives s₀ ≤ s₀^r ≤ ⌊n/2⌋ and s₀ ≤ p, so S₀ ∈ Ω.
(ii) n^{κ₀} ≥ C_v² ≥ 32 (C_v ≥ 4√2), so u/n ≤ n^{−κ₀} ≤ 1/32 and, since n ≥ 3, u ≤ n/32 ≤ (n − 1)/8 = N/8 and 4u ≤ n/8 ≤ ν.
(iii) Since 1 ≤ u ≤ n: 1/n ≤ √(u/n), √u/n ≤ √(u/n), u/n ≤ √(u/n), √(Nu)/n ≤ √(u/n).
(iv) C_v√(u/n) ≤ C_vn^{−κ₀/2} ≤ 1, and hence (C_v/2 = C_ρ + 2√2) 2√2·√(u/n) ≤ ½.

**Step 1 (noise event).** Put 𝓔_u := 𝓔¹ ∩ 𝓔² ∩ 𝓔³ ∩ 𝓔⁴ ∩ 𝓔⁵ with
  𝓔¹ := {nε̄² ≤ 2σ*²u},  𝓔² := {‖Pe‖² ≤ σ*²(4u + 2s₀^r log 2)},  𝓔³ := {|‖e‖² − Nσ*²| ≤ 2σ*²√(2Nu)},
  𝓔⁴ := {|eᵀa₀'| ≤ σ*√(2Bu)},  𝓔⁵ := {y_c ≠ 0}.
Laws: e = Uᵀε ~ N_N(0, σ*²UᵀU) = N_N(0, σ*²I); √nε̄/σ* = 1ᵀε/(σ*√n) ~ N(0, 1); P and a₀' are fixed (functions of X^r).
- P((𝓔¹)ᶜ) = P(|N(0, 1)| > √(2u)) ≤ 2e^{−u} (G1).
- ‖Pe‖²/σ*² = Σ_{k≤r₀}(φ_kᵀe/σ*)², a χ²_{r₀} (the φ_k are orthonormal); by G2 with λ_k = 1,
  P((𝓔²)ᶜ) ≤ 2^{r₀/2}exp(−u − (s₀^r/2) log 2) ≤ e^{−u} (r₀ ≤ s₀^r).
- ‖e‖²/σ*² ~ χ²_N and u ≤ N/8 (Step 0(ii)): P((𝓔³)ᶜ) ≤ 2e^{−u} (G4).
- eᵀa₀' ~ N(0, σ*²‖a₀'‖²) with ‖a₀'‖² = μ_cᵀ(I − M)²μ_c ≤ μ_cᵀ(I − M)μ_c = L ≤ B (M1). If a₀' = 0, 𝓔⁴ is sure; else
  P((𝓔⁴)ᶜ) ≤ P(|N(0, 1)| > √(2u)) ≤ 2e^{−u} (σ*√(2Bu) ≥ σ*‖a₀'‖√(2u)).
- P((𝓔⁵)ᶜ) ≤ P(e ∈ {−μ_c}) = 0 (e has a Lebesgue density on ℝ^N).
Hence P(𝓔_uᶜ) ≤ 2e^{−u} + e^{−u} + 2e^{−u} + 2e^{−u} = 7e^{−u}. From now on the noise is in 𝓔_u. By 𝓔⁵ and Step 0(i),
b > 0, every model in Ω has positive posterior weight, and in particular π(S₀) > 0.

**Step 2 (data-level bounds on 𝓔_u; deterministic).**
(D1) ‖e‖² ≤ Nσ*² + 2σ*²√(2Nu) ≤ 2Nσ*², since 2√(2Nu) ≤ N ⟺ 8u ≤ N (Step 0(ii)).
(D2) ‖μ_c‖² = μᵀUUᵀμ = μᵀCμ = ‖μ‖² ≤ nM by (E; M) (μ ∈ 1^⊥). Hence s_y² = ‖μ_c + e‖²/N ≤ 2(‖μ_c‖² + ‖e‖²)/N
  ≤ 2nM/N + 4σ*² ≤ 3M + 4σ*² (n/N ≤ 3/2 for n ≥ 3), so 0 < b = b₀s_y² ≤ b̄.
(D3) Expanding y_c = μ_c + e in Q = y_cᵀ(I − M)y_c (API_CARDS:12): Q = ‖e‖² − eᵀMe + 2eᵀa₀' + L. By M1, 0 ≤ eᵀMe ≤ eᵀPe =
  ‖Pe‖². On 𝓔² ∩ 𝓔³ ∩ 𝓔⁴, with L ≤ B:
  |Q − Nσ*²| ≤ 2σ*²√(2Nu) + σ*²(4u + 2s₀^r log 2) + 2σ*√(2Bu) + B.
(D4) Put β := β_{S₀} = b + Q/2 and ρ := β/(νσ*²). Since 2ν = n + 2a₀ = N + 2a₀ + 1:
  2β − 2νσ*² = 2b + (Q − Nσ*²) − (2a₀ + 1)σ*², so, with 2ν ≥ n, (D2), (D3) and Step 0(iii),
  |ρ − 1| = |2β − 2νσ*²|/(2νσ*²) ≤ (1/n)[2b̄/σ*² + (2a₀ + 1) + 2√(2Nu) + 4u + 2s₀^r log 2 + 2√(2Bu)/σ* + B/σ*²]
    ≤ [2b̄/σ*² + 2a₀ + 1 + 2√2 + 4 + 2s₀^r log 2 + 2√(2B)/σ* + B/σ*²]·√(u/n) = C_ρ√(u/n).
  (Termwise: constants κ/n ≤ κ√(u/n); 2√(2Nu)/n ≤ 2√2√(u/n); 4u/n ≤ 4√(u/n); 2√(2B)√u/(σ*n) ≤ (2√(2B)/σ*)√(u/n).)
(D5) M y_c − μ_c = Me − (I − M)μ_c. By M1, ‖Me‖² = eᵀM²e ≤ eᵀMe ≤ ‖Pe‖² and ‖(I − M)μ_c‖² ≤ L. Hence
  ‖My_c − μ_c‖² ≤ (‖Pe‖ + √L)² ≤ 2‖Pe‖² + 2L ≤ 2σ*²(4u + 2s₀^r log 2) + 2B ≤ 2σ*²k_su + 2B,
  using 4u + 2s₀^r log 2 ≤ (4 + 2s₀^r log 2)u = k_su for u ≥ 1.
(D6) ε̄² ≤ 2σ*²u/n (𝓔¹).

**Step 3 (the conditional posterior given S₀).** The data are fixed in 𝓔_u; probabilities are under Π(· | S₀, D_n).
*Variance.* By P-T01, G := β/v ~ Gamma(ν, 1) (v ~ IG(ν, β) ⟺ 1/v ~ Gamma(ν, rate β)). Let 𝒱 := {|G − ν| ≤ 2√(νu)}.
With t := 2√(νu) ≤ ν (⟺ 4u ≤ ν, Step 0(ii)), G3 gives Π(G − ν > t) ≤ e^{−t²/(4ν)} = e^{−u} and
Π(ν − G > t) ≤ e^{−t²/(2ν)} = e^{−2u} ≤ e^{−u}; so Π(𝒱ᶜ | S₀, D_n) ≤ 2e^{−u}. On 𝒱, with g := G/ν:
|g − 1| ≤ 2√(u/ν) ≤ 2√(2u/n) ≤ ½ (ν ≥ n/2; Step 0(iv)), so g ≥ ½; and v/σ*² = β/(σ*²νg) = ρ/g, hence
  |v/σ*² − 1| = |(ρ − 1) − (g − 1)|/g ≤ 2(C_ρ√(u/n) + 2√2·√(u/n)) = C_v√(u/n) ≤ 1 (Step 0(iv)),
so in particular v ≤ 2σ*².
*Mean.* Let 𝒲 := {‖X_{c,S₀}(θ − θ̂_{S₀})‖² ≤ v(4u + 2s₀^r log 2)}. Conditionally on v, by M2 and G2 (r = r₀ ≤ s₀^r,
λ_k ∈ (0, 1)): Π(𝒲ᶜ | v, S₀, D_n) ≤ 2^{r₀/2}exp(−u − (s₀^r/2) log 2) ≤ e^{−u}; integrating over v, Π(𝒲ᶜ | S₀, D_n) ≤ e^{−u}.
On 𝒱 ∩ 𝒲: ‖X_{c,S₀}(θ − θ̂_{S₀})‖² ≤ 2σ*²k_su. By H-id (H.md §H.6(iv)), ‖μ̂ − μ‖ = ‖X_{c,S₀}θ − μ_c‖ and
X_{c,S₀}θ − μ_c = X_{c,S₀}(θ − θ̂_{S₀}) + (My_c − μ_c) (M2: X_{c,S₀}θ̂_{S₀} = My_c), so by (‖a‖ + ‖b‖)² ≤ 2‖a‖² + 2‖b‖² and (D5):
  ‖μ̂ − μ‖² ≤ 4σ*²k_su + 4σ*²k_su + 4B ≤ (8σ*²k_s + 4B)u = C_μu.
*Transfer by (TR₀).* S₀ = {j retained : ŝ_jβ*_j ≠ 0} = R ∩ {retained} ⊆ R. For a draw with S = S₀, b (raw coefficients)
is supported in S₀ ⊆ R, so Δ(x) = (â − α*) + (b − β*)ᵀx with supp(b − β*) ⊆ R. Since X^r ∈ (TR₀; C_T), applied with
a := â − α* and w := b − β* (the event quantifies over all such (a, w) simultaneously, so data-dependent coefficients
are allowed), and by H-id,
  E_xΔ(x)² ≤ C_T·n⁻¹Σ_iΔ_i² = C_T(ε̄² + ‖μ̂ − μ‖²/n).
*Hellinger.* By Lemma H (H-pop, second form), on 𝒱 ∩ 𝒲, using (D6):
  d_H²(f_{S₀,θ,v}, f*) ≤ (v/σ*² − 1)² + E_xΔ²/(4σ*²) ≤ C_v²u/n + (C_T/(4σ*²))(2σ*²u/n + C_μu/n) = C_rad²·u/n.
Hence 𝔅_u ∩ {S = S₀} ⊆ 𝒱ᶜ ∪ 𝒲ᶜ, and Π(𝔅_u | S₀, D_n) ≤ 2e^{−u} + e^{−u} = 3e^{−u}. This is (a).

**Step 4 (mixture over models).** Π(𝔅_u | D_n) = Σ_{S∈Ω}π(S)Π(𝔅_u | S, D_n) ≤ Σ_{S≠S₀}π(S) + π(S₀)·3e^{−u}
≤ (1 − π(S₀)) + 3e^{−u} = δ_n + 3e^{−u}. This is (b). ∎

*Measurability of 𝔅_u.* For fixed S and data, d_H²(f_{S,θ,v}, f*) = ∫(1 − A(v)B(x; θ, v)) ν_x(dx) (H.md Claim 2) with
an integrand that is jointly Borel in (x, θ, v, data); by Tonelli it is Borel in (θ, v, data), so 𝔅_u is measurable
and S ↦ Π(𝔅_u | S, D_n), Π(𝔅_u | D_n) are measurable functions of the data.

## 4. Integration over the design

**Measurability of 𝒢_n.** 𝒟_n, (E; M), (L₀; B) are defined by inequalities between Borel functions of X^r (which
columns are retained is one of finitely many Borel cases). For (TR₀; C_T) put ξ := (1, x_R) ∈ ℝ^{1+|R|}. If E_xx_j² = ∞
for some j ∈ R, then (a, w) = (0, e_j) violates the inequality for every sample (finite right side), so the event is
empty. Otherwise Σ := E ξξᵀ is finite and (TR₀; C_T) = {C_TΣ_n − Σ ⪰ 0}, Σ_n := n⁻¹Σ_iξ_iξ_iᵀ, a closed condition on the
Borel matrix Σ_n. In both cases it is measurable.

**Proof of Corollary DIST-3(R).** Choose U once and for all (a fixed matrix). The set
𝔈 := {(X^r, ε) : X^r ∈ 𝒢_n, ε ∉ 𝓔_u(X^r)} is Borel (each 𝓔^k is defined by inequalities between Borel functions of
(X^r, ε)). By §3, {X^r ∈ 𝒢_n} ∩ [{Π(𝔅_u | S₀, D_n) > 3e^{−u}} ∪ {Π(𝔅_u | D_n) > δ_n + 3e^{−u}}] ⊆ 𝔈. Since ε is
independent of X^r with law N_n(0, σ*²I), Fubini gives P*(𝔈) = ∫_{𝒢_n} P(ε ∉ 𝓔_u(X^r)) P*_{X}(dX^r) ≤ 7e^{−u}P*(𝒢_n)
≤ 7e^{−u}. ∎ (Equivalently: P*[Π(𝔅_u | D_n) > δ_n + 3e^{−u}] ≤ 7e^{−u} + P*(𝒢_nᶜ).)

**Proof of Corollary DIST-3(P).** C_rad and n₀ are fixed numbers (constants fixed). Let u_n := min{(M_n/C_rad)², n^{1−κ₀}}.
Since M_n → ∞ and n^{1−κ₀} → ∞, u_n → ∞; let n₁ ≥ n₀ be such that u_n ≥ 1 for n ≥ n₁. For n ≥ n₁, u_n ∈ [1, n^{1−κ₀}] and
C_rad√(u_n/n) ≤ M_n/√n, so {d_H > M_n/√n} ⊆ 𝔅_{u_n} and Π(d_H > M_n/√n | D_n) ≤ Π(𝔅_{u_n} | D_n). Fix η' ∈ (0, 1) and let
n ≥ n₁ be so large that 3e^{−u_n} ≤ η'/2. If X^r ∈ 𝒢_n and Π(𝔅_{u_n} | D_n) ≤ δ_n + 3e^{−u_n}, then
Π(d_H > M_n/√n | D_n) > η' forces δ_n > η'/2. Hence, by Corollary DIST-3(R),
  P*( Π(d_H > M_n/√n | D_n) > η' ) ≤ P*(𝒢_nᶜ) + 7e^{−u_n} + P*(δ_n > η'/2) → 0. ∎

## 5. Remarks

1. **Note (i) of the statement.** No eigenvalue floor on S₀, no beta-min and no coefficient recovery are used: the
   only design inputs are L_{S₀} ≤ B (through D3, D5, 𝓔⁴), ‖μ‖² ≤ nM (only through b, D2) and (TR₀) (the transfer).
   p ≤ n^A is not used; only one model enters, so there is no union over models and no logarithm (ROUTES §3).
2. **Note (ii) of the statement (proof).** Suppose the law of x_R does not depend on n and E‖x_R‖² < ∞, and fix
   C_T > 1. With ξ, Σ, Σ_n as in §4, let V := range Σ. For z ⊥ V, E(zᵀξ)² = zᵀΣz = 0, so zᵀξ = 0 a.s.; hence a.s. every
   ξ_i ∈ V and Σ_nz = 0 for z ⊥ V. Let λ > 0 be the smallest eigenvalue of Σ restricted to V. Every entry of Σ_n is an
   average of n i.i.d. integrable variables with a law not depending on n (|x_jx_k| ≤ (x_j² + x_k²)/2), so by the weak law
   of large numbers P(‖Σ_n − Σ‖_op > λ(1 − 1/C_T)) → 0. On the complement, for z = z_V + z_⊥ (z_V ∈ V):
   zᵀΣ_nz = z_VᵀΣ_nz_V ≥ z_VᵀΣz_V − ‖Σ_n − Σ‖_op‖z_V‖² ≥ (1 − (1 − 1/C_T))z_VᵀΣz_V = zᵀΣz/C_T (as z_VᵀΣz_V ≥ λ‖z_V‖²).
   With z = (a, w_R) this is (TR₀; C_T). Degenerate directions are covered by the a.s. inclusion ξ_i ∈ V. For triangular
   arrays (TR₀) is an explicit assumption, as stated.
3. **Note (iii).** Only δ_n → 0 in probability is assumed, so the term δ_n has no exponential control; the second
   display is in probability for that reason alone. Display (a) is an exponential bound at the parametric radius.
4. **Use in DIST-C (C-iii), (C-iv).** Display (a) is the "exponential oracle bound at √(u/n)" for Π(· | S₀, D_n) quoted
   there; it needs 𝒢_n and the noise event 𝓔_u only.
5. **Sizes of the constants.** C_v ≥ 4√2 so n₀ ≥ 32^{1/κ₀}: the theorem is asymptotic in the usual sense; no attempt to
   optimise. With σ*² = 1, s₀^r = 3, M = B = 1, C_T = 2, κ₀ = ½: C_ρ ≈ 16.0, C_v ≈ 37.7, C_rad ≈ 38.1 and
   n₀ = ⌈C_v⁴⌉ ≈ 2.0·10⁶ (check_DIST3_out.txt [0]). The large n₀ comes only from asking C_v√(u/n) ≤ 1 over the whole range
   u ≤ n^{1−κ₀}; for a fixed u it suffices that n ≥ max{3, 2s₀^r, 32u, C_v²u}.
6. **Numerics.** `check_DIST3.py` → `check_DIST3_out.txt`: exact d_H² for Gaussian x (closed form), S₀-conditional
   posterior draws, n·d_H² flat in n, every step of the bound chain (Lemma H, H-id, realised C_T) verified on the draws.
