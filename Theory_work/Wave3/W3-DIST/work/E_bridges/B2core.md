# B2-core — sparse lower bound for sample second moments, with an intercept

**Status: DRAFT (by this seat, unchecked).** Stream E, ticket W3-DIST. Target: `STATEMENT.md:351-354` (v1.3.1) and
`API_CARDS.md:92-98` (card B). Self-contained (net + Bernstein-type Chernoff bounds). Absolute constant:
**c₂ = 10⁻⁵**. Numerical sanity checks: `bridges_checks.py`, checks "B2-core …".

## Statement

Let z_1, …, z_n be i.i.d. copies of z ∈ ℝ^p (p ≥ 1) with E z = 0 and Var(z_j) = 1 for all j; put Γ := E zzᵀ (the
correlation matrix; Var(uᵀz) = uᵀΓu). Let q ≥ 1 be an integer and K > 0 such that for every u ∈ ℝ^p with at most q
nonzero entries and every λ ∈ ℝ
  E exp(λuᵀz) ≤ exp(K²λ²Var(uᵀz)/2).                                                    (SG_q)
Put q′ := min(q, p) and
  𝓔₂(q) := { n⁻¹Σ_i(a + uᵀz_i)² ≥ ½(a² + Var(uᵀz)) for all a ∈ ℝ and all u with at most q nonzero entries }.
**If q′·log(ep/q′) ≤ c₂n/K⁴ with c₂ = 10⁻⁵, then P(𝓔₂(q)) ≥ 1 − exp(−c₂n/K⁴).**
On 𝓔₂(q), for every u with at most q nonzero entries, uᵀΣ̂^z u ≥ ½uᵀΓu, where Σ̂^z := n⁻¹Σ_i(z_i − z̄)(z_i − z̄)ᵀ (and a
fortiori for the (n − 1)⁻¹-normalised sample covariance).

**Corollary B2c (raw scale).** Let x = m + D_σz with m ∈ ℝ^p, D_σ = diag(σ_1, …, σ_p), σ_j > 0 (so m = E x,
σ_j = sd(x_j), z_j = (x_j − m_j)/σ_j), and x_i = m + D_σz_i. On 𝓔₂(q), for all a ∈ ℝ and all u with at most q nonzero
entries: E(a + uᵀx)² ≤ 2·n⁻¹Σ_i(a + uᵀx_i)².

Remarks. (1) No lower bound on Γ is assumed: degenerate directions (uᵀΓu = 0, e.g. duplicated or exactly collinear
predictors) are allowed. (2) Under the hypothesis K ≥ 1 automatically (Step 0). (3) The event 𝓔₂(q) is measurable:
Step 0 shows 𝓔₂(q) = ∩_{|T|=q′}{Ŵ_T − ½Γ_T^w ⪰ 0}, a finite intersection of closed conditions on the sample.

## Proof

**Step 0 (reductions).** *K ≥ 1:* u = e_1 has one nonzero entry and Var(z_1) = 1 > 0; by Lemma B1.0(iii) of `B1.md`
(re-proved there in three lines) applied to Y = z_1, κ = K: 1 = EY² ≤ K².
*Supports.* Every u with at most q nonzero entries has |supp u| ≤ q′ (u ∈ ℝ^p), hence supp u ⊆ T for some T ⊆ [p] with
|T| = q′. Fix such T and write w := (1, z_Tᵀ)ᵀ ∈ ℝ^{1+q′}, w_i := (1, z_{i,T}ᵀ)ᵀ, v := (a, u_Tᵀ)ᵀ. Then a + uᵀz = vᵀw and
  E(vᵀw)² = a² + 2a·E(u_Tᵀz_T) + u_TᵀΓ_Tu_T = a² + Var(uᵀz) = vᵀΓ^w_T v,   Γ^w_T := E wwᵀ = diag(1, Γ_T),
because E z = 0. With Ŵ_T := n⁻¹Σ_iw_iw_iᵀ, n⁻¹Σ_i(a + uᵀz_i)² = vᵀŴ_Tv. Hence
  𝓔₂(q) = ∩_{T⊆[p], |T|=q′} {vᵀŴ_Tv ≥ ½vᵀΓ^w_Tv for all v ∈ ℝ^{1+q′}}.
Fix T, write Γ := Γ^w_T (a (1+q′)×(1+q′) PSD matrix), R := range Γ, N := ker Γ = R^⊥, r := dim R. Since Γ_{11} = 1, the
first basis vector is not in N, so 1 ≤ r ≤ 1 + q′. Γ^{1/2} and the Moore–Penrose root Γ^{+1/2} are symmetric, map ℝ^{1+q′}
into R, and Γ^{+1/2}Γ^{1/2} = Γ^{1/2}Γ^{+1/2} = Π_R (orthogonal projection onto R).

**Step 1 (degenerate directions).** Let v_1, …, v_{1+q′−r} be a basis of N. E(v_kᵀw)² = v_kᵀΓv_k = 0, so v_kᵀw_i = 0 a.s.
for every i and k. Let 𝓝_T := {v_kᵀw_i = 0 for all i, k}; P(𝓝_T) = 1, and on 𝓝_T, by linearity, vᵀw_i = 0 for every v ∈ N
and every i, hence Ŵ_Tv = n⁻¹Σ_iw_i(w_iᵀv) = 0 for v ∈ N. On 𝓝_T, for any v = v_R + v_N (v_R ∈ R, v_N ∈ N):
  vᵀŴ_Tv = v_RᵀŴ_Tv_R  and  vᵀΓv = v_RᵀΓv_R.                                               (1)
With ξ := Γ^{1/2}v_R ∈ R we have v_R = Π_Rv_R = Γ^{+1/2}ξ, ‖ξ‖² = v_RᵀΓv_R, and v_RᵀŴ_Tv_R = ξᵀB_Tξ, where
B_T := Γ^{+1/2}Ŵ_TΓ^{+1/2} (symmetric PSD, maps into R). So on 𝓝_T,
  {vᵀŴ_Tv ≥ ½vᵀΓv ∀v} ⟸ {ξᵀB_Tξ ≥ ½ for all unit ξ ∈ R}.                                      (2)

**Step 2 (one direction).** Let ξ₀ ∈ R with ‖ξ₀‖ = 1 and v₀ := Γ^{+1/2}ξ₀ = (a, u_Tᵀ)ᵀ. Then v₀ᵀΓv₀ = ξ₀ᵀΠ_Rξ₀ = 1, i.e.
a² + σ² = 1 with σ² := Var(u_Tᵀz_T), and ξ₀ᵀB_Tξ₀ = n⁻¹Σ_iX_i² with X_i := v₀ᵀw_i = a + Y_i, Y_i := u_Tᵀz_{i,T} i.i.d.,
E Y = 0, E X² = 1. By (SG_q) (u_T padded by zeros has ≤ q′ ≤ q nonzero entries) Y satisfies the hypothesis of Lemma B1.0
of `B1.md` with κ² = K²σ² when σ > 0; when σ = 0, Y = 0 a.s. (E Y² = 0). In both cases, for k ≥ 1,
  E Y^{2k} ≤ 2·k!·(2K²σ²)^k                                                                (3)
(B1.0(ii); trivial when σ = 0). By convexity (a + y)^{2k} ≤ 2^{2k−1}(a^{2k} + y^{2k}), and a² ≤ 1, σ² ≤ 1, K ≥ 1:
  E X⁴ ≤ 8(a⁴ + 16K⁴σ⁴) ≤ 128K⁴(a⁴ + σ⁴) ≤ 128K⁴(a² + σ²)² = 128K⁴;                          (4)
  E X^{2k}/k! ≤ 2^{2k−1}(a^{2k}/k! + 2(2K²σ²)^k) ≤ 2^{2k−1}·3·(2K²)^k = (3/2)(8K²)^k  for k ≥ 2,     (5)
using a^{2k}/k! ≤ 1 ≤ (2K²)^k and σ^{2k} ≤ 1.
*Lower tail.* e^{−u} ≤ 1 − u + u²/2 for u ≥ 0, so for μ ≥ 0: E e^{−μX²} ≤ 1 − μ + μ²EX⁴/2 ≤ 1 − μ + 64μ²K⁴ ≤ e^{−μ + 64μ²K⁴}.
Chernoff with μ := δ/(128K⁴), δ := 1/5:
  P(n⁻¹ΣX_i² ≤ 1 − δ) ≤ e^{μn(1−δ)}(E e^{−μX²})^n ≤ exp(−nμδ + 64nμ²K⁴) = exp(−nδ²/(256K⁴)) = exp(−n/(6400K⁴)).
*Upper tail.* For 0 ≤ λ ≤ 1/(16K²), by monotone convergence and (5),
E e^{λX²} = 1 + λ + Σ_{k≥2}λ^kEX^{2k}/k! ≤ 1 + λ + (3/2)(8λK²)²/(1 − 8λK²) ≤ 1 + λ + 3(8λK²)² = 1 + λ + 192λ²K⁴ ≤ e^{λ + 192λ²K⁴}.
Chernoff with λ := δ′/(384K⁴), δ′ := 1 (λ ≤ 1/(16K²) since K ≥ 1):
  P(n⁻¹ΣX_i² ≥ 1 + δ′) ≤ e^{−λn(1+δ′)}(E e^{λX²})^n ≤ exp(−nλδ′ + 192nλ²K⁴) = exp(−nδ′²/(768K⁴)) = exp(−n/(768K⁴)).
Hence, for every fixed unit ξ₀ ∈ R:
  P( ξ₀ᵀB_Tξ₀ ∉ [4/5, 2] ) ≤ exp(−n/(6400K⁴)) + exp(−n/(768K⁴)) ≤ 2exp(−n/(6400K⁴)).                (6)

**Step 3 (net).** *Volumetric bound.* Let 𝒩_T be a maximal subset of the unit sphere of R whose points are pairwise at
distance > ε := 1/10. By maximality every unit ξ ∈ R is within ε of 𝒩_T. The balls of radius ε/2 around the points of
𝒩_T are disjoint and contained in the ball of radius 1 + ε/2 of R (dimension r), so |𝒩_T|(ε/2)^r ≤ (1 + ε/2)^r, i.e.
|𝒩_T| ≤ (1 + 2/ε)^r = 21^r ≤ 21^{1+q′}. 𝒩_T depends only on Γ (deterministic).
*Deterministic step.* Suppose ξ₀ᵀB_Tξ₀ ∈ [4/5, 2] for all ξ₀ ∈ 𝒩_T. ‖ξ‖_B := (ξᵀB_Tξ)^{1/2} is a seminorm on R, so
‖ξ‖_B ≤ ‖ξ₀‖_B + ‖ξ − ξ₀‖_B and ‖ξ‖_B ≥ ‖ξ₀‖_B − ‖ξ − ξ₀‖_B, and ‖ξ − ξ₀‖_B ≤ ‖B_T|_R‖^{1/2}‖ξ − ξ₀‖, where
‖B_T|_R‖ := sup_{ξ∈R, ‖ξ‖=1} ξᵀB_Tξ. For every unit ξ ∈ R pick ξ₀ ∈ 𝒩_T with ‖ξ − ξ₀‖ ≤ ε:
  upper: ‖ξ‖_B ≤ √2 + ε‖B_T|_R‖^{1/2}; taking the sup over ξ, ‖B_T|_R‖^{1/2} ≤ √2/(1 − ε) = √2/0.9;
  lower: ‖ξ‖_B ≥ √(4/5) − ε√2/(1 − ε) = 0.894427… − 0.157134… = 0.737292… > 0,
so ξᵀB_Tξ ≥ 0.737292² = 0.543600… ≥ ½ for every unit ξ ∈ R (arithmetic: `bridges_checks_out.txt`, "B2-core net
inequality"). By (2), on 𝓝_T this gives vᵀŴ_Tv ≥ ½vᵀΓ^w_Tv for all v.

**Step 4 (union bound).** Let 𝓖 := ∩_T 𝓝_T ∩ ∩_T ∩_{ξ₀∈𝒩_T}{ξ₀ᵀB_Tξ₀ ∈ [4/5, 2]} (T over the C(p, q′) subsets of size q′).
By Steps 0–3, 𝓖 ⊆ 𝓔₂(q). P(∪_T𝓝_Tᶜ) = 0. The number of pairs (T, ξ₀) is at most C(p, q′)·21^{1+q′} ≤ (ep/q′)^{q′}·21^{1+q′}
(C(p, k) ≤ p^k/k! ≤ (ep/k)^k because k! ≥ (k/e)^k). Put L := q′log(ep/q′); since q′ ≤ p, log(ep/q′) ≥ 1 and L ≥ q′ ≥ 1.
log of the count ≤ L + (1 + q′)log 21 ≤ L + 2q′log 21 ≤ (1 + 2log 21)L. By (6),
  P(𝓖ᶜ) ≤ 2exp((1 + 2log 21)L − n/(6400K⁴)) = exp(log 2 + (1 + 2log 21)L − n/(6400K⁴)).
Under L ≤ c₂n/K⁴: from 1 ≤ L, log 2 ≤ (log 2)L; so the exponent is ≤ (log 2 + 1 + 2log 21)c₂n/K⁴ − n/(6400K⁴). With
c₂ = 10⁻⁵: (log 2 + 1 + 2log 21 + 1)c₂ = 8.78…·10⁻⁵ ≤ 1/6400 = 1.5625·10⁻⁴, i.e.
(log 2 + 1 + 2log 21)c₂ − 1/6400 ≤ −c₂. Hence P(𝓔₂(q)ᶜ) ≤ P(𝓖ᶜ) ≤ exp(−c₂n/K⁴). ∎(main claim)

**"In particular".** On 𝓔₂(q), for u with ≤ q nonzero entries take a := −uᵀz̄:
uᵀΣ̂^z u = n⁻¹Σ_i(uᵀz_i − uᵀz̄)² ≥ ½((uᵀz̄)² + uᵀΓu) ≥ ½uᵀΓu. The (n − 1)⁻¹-normalised version is larger by n/(n − 1). ∎

**Proof of Corollary B2c.** a + uᵀx = (a + uᵀm) + (D_σu)ᵀz and a + uᵀx_i = (a + uᵀm) + (D_σu)ᵀz_i; D_σu has the same
support as u. By E z = 0, E(a + uᵀx)² = (a + uᵀm)² + Var((D_σu)ᵀz). Apply 𝓔₂(q) with (a + uᵀm, D_σu). ∎

## Notes for the checker
- Only the *lower* bound of the conclusion is claimed; the upper-tail bound in Step 2 is used only to control
  ‖B_T|_R‖ in the net step.
- The constant c₂ = 10⁻⁵ is not optimised (any c₂ ≤ 1/(6400(2 + log 2 + 2 log 21)) ≈ 1.78·10⁻⁵ works with this proof).
- The hypothesis (SG_q) is the ψ₂–L₂ form on sparse directions (reader (A3)); it is used for every v₀ = Γ^{+1/2}ξ₀, i.e.
  for the variable a + uᵀz with u supported in T, |T| = q′ ≤ q.
