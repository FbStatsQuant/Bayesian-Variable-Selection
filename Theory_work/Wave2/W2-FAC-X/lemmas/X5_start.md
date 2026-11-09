# X5 — Start mode under iid CS rows: S̃₀ = S* = [p] ∖ N₀ (claim (C1))

Status: **PROVED (by this seat, unchecked)**; lemma check R05 (Codex Sol high, reviews/R05_X5X6_check_sol.md):
VERIFIED-WITH-AMENDMENTS (items 1–4), applied (reviews/R05_disposition.md). Falsification numerics: numerics/n5x_start.py → N5X_out.txt (exact
iid-row sufficient statistics, the production partition and start-mode routine of bvs_core).

Setting: STATEMENT v3 §1–2 (model R, (CS-R), (P-½), (θ), (FS)); Υ_n = I (X1). The argument is FACB L2 conditionally on
the **raw design Z := X^r**, on a raw-design event 𝒜_n with common constants (R05 item 1: the standardised X does not
determine D_x or θ* = D_xβ; Z determines X, D_x, θ*, the partition and N₀, and given Z, e = Cε ~ N(0, σ²C)).
Blocks C_b: the method's realised partition (a Z-measurable partition
into blocks of size ≤ 16). N₀ := ⋃{C_b ∖ S₀ : S₀ ⊆ C_b} (at most one block contains S₀; |N₀| ≤ 15 as s₀ ≥ 1).

## X5.1 Design event 𝒜_n

R̂ := XᵀX/(n − 1) (sample correlation). 𝒜_n := {max_{j<k}|R̂_jk − Σ_jk| ≤ δ′_n} ∩ {max_j|sd_j − 1| ≤ δ′_n} ∩
{λ_min(R̂) ≥ c₀}, δ′_n := 32√(2(A + 1)log n/(n − 1)) (A := 1), c₀ := (1 − ρ)/5. P(𝒜_n) → 1: the first event by Lemma
CR/[CONC′] (`Theory_work/Wave1/W1-PXN/lemmas/CR_corr_tails.md`, status "PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)";
as used in FACA L5.1, eventually: P(max|R̂ − Σ| > δ′_n) ≤ 3n^{−2} for p ≤ n); the second by χ²_{n−1} concentration (sd_j² = ‖Cx^r_j‖²/(n − 1),
unit population variance); the third by X2.1 (on 𝔈_n). Consequence: θ*_j = sd_jβ_j, so |θ*_j − ϑ_j| ≤ δ′_n|ϑ_j|
(sign-corrected coordinates). 𝒜_n is an event in Z.

## X5.2 Block increments conditionally on Z

For U ⊆ C_b, |U| = u ≤ 15, l ∈ C_b ∖ U, put V := U ∪ {l} ∪ S₀ (|V| ≤ 16 + s₀). By X1.4 (g1)–(g2), extended to
blocks missing truths (R05 item 3): the Schur identity for Q and (g1) are algebraic and use only λ_min(G_T) ≥ c₀(n − 1);
in (g2) the bound on b(0) is replaced by ‖b(0)‖ = ‖G_T⁻¹X_Tᵀy‖ ≤ ‖y‖/√λ_min(G_T) ≤ 1/√c₀ (‖y‖² = n − 1), valid for every
nonempty T (U = ∅: empty-vector conventions); the rest of (g2) is unchanged. So on 𝒜_n:
  log r_b(U ∪ l) − log r_b(U) = −½[LD(U ∪ l) − LD(U)] − ν log(1 − (Q_U − Q_{U∪l})/ψ_U),
LD(U ∪ l) − LD(U) = log(n + 1) + O(1/n), and Q_U − Q_{U∪l} = (n/(n + 1))P^{ε₁}_l with
|√P^{ε₁}_l − √P⁰_l| ≤ C n^{−3/2}(1 + √P⁰_l), P⁰_l = (r_lᵀy)²/‖r_l‖², r_l := residual of x_l on X_U (r_l := x_l if U = ∅).
Decompose r_lᵀY = r_lᵀμ + r_lᵀe. **Population part:** r_lᵀμ = (n − 1)c_n(U, l) with
c_n(U, l) := R̂_{l,S₀}θ*_{S₀} − R̂_{lU}R̂_UU⁻¹R̂_{U,S₀}θ*_{S₀}, a smooth function of (R̂_V, θ*_{S₀}) on {λ_min ≥ c₀} with a
Lipschitz constant depending only on (c₀, |V|, ‖ϑ‖); its population value (R̂ → Σ, θ* → ϑ) is FACB L2.1's
c(U, l) = (1 − ρ)[ϑ_l + ρϑ(S₀ ∖ U)/(1 + (u − 1)ρ)] (ϑ_l := 0 for a null; FACB's computation, which is an identity for
Σ). Hence on 𝒜_n, uniformly over all such (U, l) in all realisable blocks: |c_n(U, l) − c(U, l)| ≤ C δ′_n → 0.
* If U ⊇ S₀ and l is null ("zero pair"): μ ∈ span X_U, so r_lᵀμ = 0 **exactly**.
* Otherwise c(U, l) ≠ 0 by (FS) (FACB L2.1), so |c_n(U, l)| ≥ c_FS/2 for n ≥ n₀ (c_FS := min |c| over the finitely many
  nonzero values, a constant).
**Noise part.** Conditionally on Z, e ~ N(0, σ²C). (a) Uniformly over all U, l with |U ∪ l| ≤ 16:
|r_lᵀe|/‖r_l‖ ≤ ‖P_{U∪l}e‖ ≤ (16 max_j(x_jᵀe)²/(c₀(n − 1)))^{1/2}, and on the event
E^Z_1 := {max_j|x_jᵀe| ≤ σ√(n − 1)(2 log(2p) + 2L_n)^{1/2}} (conditional probability ≥ 1 − e^{−L_n}) this is
≤ C√(log n). (b) For the zero pairs of the (unique, X-determined) block containing S₀ — at most 2¹⁵·16 pairs —
r_lᵀe/‖r_l‖ | Z ~ N(0, σ²), so E^Z_2 := {|r_lᵀe|/‖r_l‖ ≤ σ√(2(20 + L_n)) for all these pairs} (two-sided, R05
item 2; the whole space if there are no zero pairs) has conditional probability
≥ 1 − 2²⁰e^{−(20+L_n)}. Also ‖e‖²/σ² ∈ [n − 1 − n^{2/3}, n − 1 + n^{2/3}] (E^Z_3, conditional χ² bound). On 𝒜_n ∩ E^Z_1 ∩ E^Z_3
(R05 item 4): (n − 1)s² = ‖μ‖² + 2μᵀe + ‖e‖² with ‖μ‖² = (n − 1)θ*ᵀR̂θ* ≤ 2(n − 1)s₀‖ϑ‖² and
|μᵀe| ≤ Σ_{S₀}|θ*_j|·max_j|x_jᵀe| = O(√(n log n)); hence s² ∈ [s_min², s_max²] with s_min² := σ²/2,
s_max² := 2(2s₀‖ϑ‖² + σ²) for n ≥ n₀ (common onset).

## X5.3 Single-flip improvements (FACB L2.3 with sample quantities)

On 𝒜_n ∩ E^Z_1 ∩ E^Z_2 ∩ E^Z_3, n ≥ n₀, for S ∈ Ω, k := |S|, block b, U := S ∩ C_b:
(i) **Positive pair** (l ∈ C_b ∖ U not a zero pair, k < p): P⁰_l ≥ ((n − 1)c_FS/2 − ‖r_l‖C√(log n))²/(s²‖r_l‖²) ≥
c₂n with c₂ := c_FS²/(8s_max²) (‖r_l‖² ≤ n − 1). As ψ_U ≤ n, the increment of log γ₀ is
≥ −log(2p) − ½log(n + 2) − 1 + ν log(1/(1 − c₂/2)) ≥ (n/2)(c₂/2) − 3 log n > 0.
(ii) **Zero pair** (U ⊇ S₀, l ∈ C_b ∖ U null, so l ∈ N₀): P⁰_l ≤ 2σ²(20 + L_n)/s² and ψ_U ≥ RSS_U/s² ≥ (‖e‖² −
‖P_Ue‖²)/s² ≥ σ²n/(2s_max²) (‖P_Ue‖² = O(log n) by (a)); so the increment of adding l is
≤ −½log(n + 1) + C(20 + L_n) < −¼log n, and removing l ∈ S ∩ N₀ with (S ∩ C_b) ∖ {l} ⊇ S₀ raises log γ₀ by ≥ ¼log n
(w(k − 1)/w(k) ≥ 1 for k ≤ p).

## X5.4 Lemma (C1)

**Lemma X5.** On 𝒜_n ∩ E^Z_1 ∩ E^Z_2 ∩ E^Z_3, n ≥ n₀: S* = [p] ∖ N₀ is the unique maximiser of γ₀ on Ω. Hence
P(S̃₀ = S*, unique) → 1 under the joint law, and the emitted centre (coded routine and TDP, e4/e4′ irrelevant by
uniqueness — FINAL s5 Lemma UM, as in FACB L2 remark (1)) is S*.
*Proof.* FACB L2.4 verbatim, with L2.3 replaced by X5.3 (the proof uses only the dichotomy positive pair / zero pair and
the two increment bounds). Probability: P(failure) ≤ P(𝒜_nᶜ) + sup_{z∈𝒜_n}P((E^Z_1 ∩ E^Z_2 ∩ E^Z_3)ᶜ | Z = z) → 0, the
conditional bounds being uniform in z. ∎

**Remarks.** (1) K = p eventually (p ≤ n/2 eventually under (P-½)). (2) The partition enters only through N₀ and the
zero pairs of the S₀-block, both handled conditionally on Z; no independence between the partition and ξ is used.
(3) (FS′) is not treated (STATEMENT v3 §2).
