# L1 — Metric toolkit R1: CT_M, CD_M, RB_M, TAIL_M, SC_M and the new Lemma LOCL

Status: **PROVED (by this seat, unchecked)**; check R02 (Codex gpt-6.1-sol high, `reviews/R02_L1L2_check_sol.md`):
VERIFIED-WITH-AMENDMENTS (1 MINOR, applied). Seat: parallel prover (Claude Opus 5.5 subagent), 2026-11-09.
Target: `W2-UNI/STATEMENT.md:143-151` (R1, as amended by `reviews/R01_statement_lock_sol.md:63-77`, required change 4).
Model (delta source): LOC2 `lemmas/L3_CTd.md` (CT_d, CD_d, RB, TAIL; status there "PROVED (by this seat, unchecked)",
check R02 "VERIFIED-WITH-AMENDMENTS"; inside W2-LOC2 "PROVED-CHECKED", `W2-LOC2/REPORT.md:3`), itself modelled on APP
`lemmas/L2_CT.md`. Falsification numerics: `numerics/n2_metric.py` → `numerics/n2_metric_out.txt` (zero-distance
clusters, distances in (0, 1), non-unit diagonals, both branches, block pseudometric, exhaustive p = 10 enumeration; see §M8).
All statements are uniform in p, n and the pseudometric; constants depend only on (C₀, d₀, c, C, K, a). Asymptotic use only.

**Notation.** K is the decay-envelope constant of 𝓛𝓞𝓒 (not the model-size cap K_n). For a finite index set I, a
*pseudometric* δ on I is symmetric, δ(i, i) = 0, satisfies the triangle inequality, and may vanish between distinct
indices. B(i, r) := {k ∈ I : δ(i, k) ≤ r} (contains i). Growth: N_δ(r) := max_i |B(i, r)| ≤ C₀(1 + r)^{d₀} for all r ≥ 0
(`STATEMENT.md:50-53`); necessarily C₀ ≥ 1, d₀ ≥ 0 real. Empty index sets carry zero vectors and empty sums are 0.

## M0. Two elementary facts about the growth function

**(G-restr)** If J ⊆ I, the restriction δ|_J is a pseudometric on J with max_{i∈J}|B(i, r) ∩ J| ≤ N_δ(r). (Trivial.)
**(G-shell)** For every i, every integer m ≥ 0: #{k : m ≤ δ(i, k) < m + 1} ≤ |B(i, m + 1)| ≤ C₀(m + 2)^{d₀}.
Hence for any nonincreasing g ≥ 0 on [0, ∞) and any real r ≥ 0,
  Σ_{k : δ(i,k) > r} g(δ(i, k)) ≤ C₀ Σ_{m ≥ ⌊r⌋} (m + 2)^{d₀} g(m),   Σ_k g(δ(i, k)) ≤ C₀ Σ_{m ≥ 0} (m + 2)^{d₀} g(m).
*Proof.* Group k by the shell m := ⌊δ(i, k)⌋ (shells start at m = 0; distance-0 indices, including i, lie in shell 0).
On the shell g(δ) ≤ g(m). If δ(i, k) > r then m + 1 > r, so m > r − 1, i.e. m ≥ ⌊r⌋. ∎
(Replaces the packing fact of LOC2 `L3_CTd.md:15-21`, which needed site separation ≥ 1 and started shells at m = 1.)

**(G-tail) explicit tail.** For t > 0, d₀ ≥ 0 and integer M ≥ 0 put T_{d₀}(M, t) := Σ_{m≥M}(m + 2)^{d₀}e^{−tm}. With
μ(t) := e^{t}(2d₀/(et))^{d₀} (μ := e^{t} if d₀ = 0), (m + 2)^{d₀}e^{−tm/2} ≤ μ(t) for all m ≥ 0 [since
sup_{y>0} y^{d₀}e^{−ty/2} = (2d₀/(et))^{d₀}], hence T_{d₀}(M, t) ≤ μ(t)e^{−tM/2}/(1 − e^{−t/2}) < ∞, and → 0 as M → ∞.

## M1. Lemma CT_M (Combes–Thomas for a pseudometric of polynomial growth)

Let A be real symmetric on a finite I with λ_min(A) ≥ α > 0 (no upper spectral bound), δ a pseudometric on I with
growth ≤ C₀(1 + r)^{d₀}, and |A_ij| ≤ K′e^{−a′δ(i,j)} for i ≠ j (K′, a′ > 0; if the envelope holds with K′ = 0 it holds
with any K′ > 0, so WLOG K′ > 0). For 0 ≤ t < a′ put
  S(t) = S(t; K′, a′) := K′C₀ Σ_{m≥0} (m + 2)^{d₀} e^{−(a′−t)m}(1 − e^{−t(m+1)}).
S is finite, continuous, nondecreasing on [0, a′), S(0) = 0, S(t) → ∞ as t ↑ a′. Define
  t*(α, K′, a′) := max{t ∈ [0, a′) : S(t) ≤ α/2} ∈ (0, a′)   (dependence on (C₀, d₀) suppressed).
Then for **all** i, j ∈ I (including i = j and pairs with δ(i, j) = 0):  |(A⁻¹)_ij| ≤ (2/α)e^{−t*δ(i,j)}.
**Restricted version.** For every J ⊆ I, A_JJ satisfies the same hypotheses with the same (α, K′, a′, C₀, d₀)
(Cauchy interlacing gives λ_min(A_JJ) ≥ α; entries are inherited; (G-restr)), so |((A_JJ)⁻¹)_ij| ≤ (2/α)e^{−t*δ(i,j)},
i, j ∈ J, with the same t*.

*Proof.* (i) *S.* Each term is continuous, nonnegative and nondecreasing in t (both factors are). On [0, a′ − η] terms
are ≤ (m + 2)^{d₀}e^{−ηm}, summable, so the series converges uniformly there: S is finite and continuous on [0, a′),
nondecreasing, S(0) = 0. As t ↑ a′ the partial sum up to M tends to K′C₀Σ_{m≤M}(m + 2)^{d₀}(1 − e^{−a′(m+1)}) ≥
K′C₀(1 − e^{−a′})Σ_{m≤M}(m + 2)^{d₀} ≥ K′C₀(1 − e^{−a′})(M + 1), unbounded in M; by monotonicity S → ∞. Hence
{t ∈ [0, a′) : S(t) ≤ α/2} = [0, t*] with 0 < t* < a′ (continuity at 0, α > 0).
(ii) *Conjugation.* Fix j and φ(i) := δ(i, j). By the triangle inequality |φ(i) − φ(k)| ≤ δ(i, k) (φ is 1-Lipschitz for
δ; no Euclidean structure is used). Put D := diag(e^{t*φ(i)}), A_t := DAD⁻¹, E := A_t − A. Then E_ii = 0 and, for i ≠ k,
  |E_ik| = |A_ik||e^{t*(φ(i)−φ(k))} − 1| ≤ |A_ik|(e^{t*δ(i,k)} − 1) ≤ K′e^{−a′δ(i,k)}(e^{t*δ(i,k)} − 1)
(|e^s − 1| ≤ e^{|s|} − 1). In particular **E_ik = 0 whenever δ(i, k) = 0**: zero-distance pairs contribute nothing,
whatever the size of A_ik.
(iii) *Schur test, shells from m = 0.* g(x) := e^{−a′x}(e^{t*x} − 1) = e^{−(a′−t*)x}(1 − e^{−t*x}) is not monotone, so bound it
shell-wise: for x ∈ [m, m + 1), g(x) ≤ e^{−(a′−t*)m}(1 − e^{−t*(m+1)}). By (G-shell),
Σ_k |E_ik| ≤ K′Σ_{m≥0} C₀(m + 2)^{d₀}e^{−(a′−t*)m}(1 − e^{−t*(m+1)}) = S(t*) ≤ α/2. The bound on |E_ik| is symmetric in
(i, k), so column sums obey it too, and ‖E‖₂ ≤ √(‖E‖₁‖E‖_∞) ≤ α/2.
(iv) ‖A⁻¹‖₂ ≤ 1/α, so ‖A⁻¹E‖₂ ≤ ½ and A_t = A(I + A⁻¹E) is invertible with ‖A_t⁻¹‖₂ ≤ 2/α. A_t⁻¹ = DA⁻¹D⁻¹ has (i, j)
entry e^{t*φ(i)}(A⁻¹)_ij e^{−t*φ(j)} = e^{t*δ(i,j)}(A⁻¹)_ij (φ(j) = δ(j, j) = 0); entries are bounded by the spectral norm. ∎

Delta to LOC2 `L3_CTd.md:23-43`: (2m + 3)^d → C₀(m + 2)^{d₀}; shells m ≥ 1 → m ≥ 0 (no separation); φ(y) = ‖y − x_j‖ →
φ(i) = δ(i, j); sites → indices. Nothing else changes; the argument never uses an upper spectral bound or unit diagonal.

## M2. Class 𝓛𝓞𝓒 and Lemma CD_M (conditional decay and conditional spectra)

𝓛𝓞𝓒(C₀, d₀, c, C, K, a) is as in `STATEMENT.md:50-53` (symmetric Ψ on [p], spectrum in [c, C], 0 < c ≤ C; pseudometric of
growth ≤ C₀(1 + r)^{d₀}; (Σ-branch) |Ψ_jk| ≤ Ke^{−aδ(j,k)} or (Θ-branch) |(Ψ⁻¹)_jk| ≤ Ke^{−aδ(j,k)}, j ≠ k). Unit diagonal is
NOT assumed. Write t*(·, ·, ·) for the CT_M rate with the class's (C₀, d₀). Define
  (Σ-branch) t₁ := t*(c, K, a), K₁ := 2/c;   (Θ-branch) t₁ := a, K₁ := K;   t₂ := t*(1/C, K₁, t₁),  K₂ := 2C.

**Lemma CD_M.** Let Ψ ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a), ζ ~ N(0, Ψ), Θ := Ψ⁻¹. For every U ⊆ [p] (U = ∅ allowed):
 (a) |Cov(ζ_j, ζ_k | ζ_U)| ≤ K₂e^{−t₂δ(j,k)} for all j, k ∉ U (j = k and δ(j, k) = 0 allowed);
 (b) for every V ⊆ [p] ∖ U, Cov(ζ_V | ζ_U) has spectrum in [c, C]; in particular c ≤ Var(ζ_j | ζ_U) ≤ min(Ψ_jj, C) ≤ C
     (not ≤ 1: Ψ need not be unit diagonal);
 (c) (branch equivalence) Θ-branch with (K, a) ⇒ Ψ obeys the Σ-branch envelope with (K_Ψ, t_Ψ) := (2C, t*(1/C, K, a)),
     for all j, k; Σ-branch with (K, a) ⇒ Θ obeys the Θ-branch envelope with (2/c, t*(c, K, a)), for all j, k.
 Define in both branches (K_Ψ, t_Ψ) := (K, a) (Σ-branch) or (2C, t*(1/C, K, a)) (Θ-branch): |Ψ_jk| ≤ K_Ψe^{−t_Ψδ(j,k)}, j ≠ k.

*Proof.* Θ has spectrum in [1/C, 1/c]. In both branches |Θ_jk| ≤ K₁e^{−t₁δ(j,k)} for j ≠ k: Θ-branch by assumption,
Σ-branch by CT_M applied to Ψ (α = c, (K, a)). This, and CT_M applied to Θ (α = 1/C, (K, a)) in the Θ-branch, gives (c).
Let H := [p] ∖ U (the full complement). For Gaussian ζ, block inversion gives Cov(ζ_H | ζ_U) = (Θ_HH)⁻¹. Θ_HH is a
principal submatrix of Θ: spectrum in [1/C, 1/c] (interlacing) and off-diagonal entries ≤ K₁e^{−t₁δ}; restricted CT_M
(α = 1/C) gives (a) for j, k ∈ H, and spec((Θ_HH)⁻¹) ⊆ [c, C]. For V ⊆ H, Cov(ζ_V | ζ_U) is a principal submatrix of
Cov(ζ_H | ζ_U) (not (Θ_VV)⁻¹), so its spectrum lies in [c, C] by interlacing; and Var(ζ_j | ζ_U) ≤ Var(ζ_j) = Ψ_jj. ∎
Delta to LOC2 `L3_CTd.md:50-65`: CT_d → CT_M; "Var(W_j | W_U) ≤ 1" → "≤ min(Ψ_jj, C)" (the only use of unit diagonal there).

## M3. Lemma RB_M (pointwise and ℓ¹ bounds for population regression coefficients)

For l ∈ [p] and A ⊆ [p] ∖ {l} let β_A(l) := Ψ_AA⁻¹Ψ_{Al} ∈ ℝ^A (E[ζ_l | ζ_A] = ζ_Aᵀβ_A(l); β_∅ = 0); β̄_A(l) ∈ ℝ^p its
zero-padding. Put t′ := t*(c, K_Ψ, t_Ψ), **B := 2C/c**, L₀ := B·C₀ Σ_{m≥0}(m + 2)^{d₀}e^{−t′m} = B·C₀T_{d₀}(0, t′) < ∞.

**Lemma RB_M.** For Ψ ∈ 𝓛𝓞𝓒 (either branch), all l, all A ⊆ [p] ∖ {l} and v ∈ A:
  |β_A(l)_v| ≤ B e^{−t′δ(l,v)},    ‖β_A(l)‖₁ ≤ L₀.
*Proof.* 𝔅 := Ψ_{A∪{l}} is a principal submatrix of Ψ: λ_min ≥ c, off-diagonal entries ≤ K_Ψe^{−t_Ψδ} (CD_M(c) in the
Θ-branch). Let G := 𝔅⁻¹. Block inversion: β_A(l)_v = −G_vl/G_ll and G_ll = 1/Var(ζ_l | ζ_A) **≥ 1/C** by CD_M(b) [R01-4:
LOC2's "Ψ_ll ≥ 1" used unit diagonal and is not available; in general G_ll ≥ 1/Ψ_ll ≥ 1/C]. Restricted CT_M on 𝔅
(α = c, (K_Ψ, t_Ψ)) gives |G_vl| ≤ (2/c)e^{−t′δ(v,l)}. Hence |β_v| ≤ (2C/c)e^{−t′δ(l,v)}; sum with (G-shell) (shells from
m = 0; indices at distance 0 from l, if any, lie in shell 0). ∎
*Simplification (unit-diagonal Ψ, e.g. UNI-0's Σ):* G_ll ≥ 1 and B may be replaced by 2/c, as in LOC2 `L3_CTd.md:67-75`.

## M4. Lemma TAIL_M (far conditioning)

Put κ(r) := (K₂²/c)·C₀ Σ_{m≥⌊r⌋}(m + 2)^{d₀}e^{−2t₂m} = (K₂²/c)C₀T_{d₀}(⌊r⌋, 2t₂); κ(r) → 0 as r → ∞, and by (G-tail)
κ(r) ≤ (K₂²/c)C₀μ(2t₂)e^{−t₂⌊r⌋}/(1 − e^{−t₂}).
**Lemma TAIL_M.** Ψ ∈ 𝓛𝓞𝓒, l ∈ [p], T ⊆ [p] ∖ {l}, r ≥ 0, T′ := T ∩ B(l, r). Then
 (a) Var(E[ζ_l | ζ_T] − E[ζ_l | ζ_{T′}]) ≤ κ(r);
 (b) Var(ζ_l | ζ_{T′}) = Var(ζ_l | ζ_T) + Var(E[ζ_l | ζ_T] − E[ζ_l | ζ_{T′}]); hence ψ_{l|T′} ≤ (1 + κ(r)/c)ψ_{l|T}, where
     ψ_{l|A} := Var(ζ_l | ζ_A) = Ψ_ll − Ψ_{lA}Ψ_AA⁻¹Ψ_{Al} ≥ c.
*Proof.* (b) e_T := ζ_l − E[ζ_l | ζ_T] is uncorrelated with every linear function of ζ_T, in particular with
𝒟 := E[ζ_l | ζ_T] − E[ζ_l | ζ_{T′}]; e_{T′} = e_T + 𝒟. (a) With 𝒱 := ζ_{T∖T′} − E[ζ_{T∖T′} | ζ_{T′}] and
M := Cov(ζ_{T∖T′} | ζ_{T′}), ζ_T is a bijective linear image of (ζ_{T′}, 𝒱) with 𝒱 ⟂ ζ_{T′}, so
𝒟 = E[e_{T′} | 𝒱] = bᵀM⁻¹𝒱, b_v := Cov(ζ_l, ζ_v | ζ_{T′}) (v ∈ T ∖ T′); Var 𝒟 = bᵀM⁻¹b ≤ ‖b‖²/c (CD_M(b),
T ∖ T′ ⊆ [p] ∖ T′). By CD_M(a) (l ≠ v, both ∉ T′), |b_v| ≤ K₂e^{−t₂δ(l,v)} with δ(l, v) > r; (G-shell) with
g(x) = K₂²e^{−2t₂x} gives ‖b‖² ≤ K₂²C₀T_{d₀}(⌊r⌋, 2t₂). The ratio uses ψ_{l|T} ≥ c (CD_M(b)). ∎
(Delta to LOC2 `L3_CTd.md:77-85`: shells m ≥ ⌊r⌋, m ≥ 1 → m ≥ ⌊r⌋ ≥ 0 with counts C₀(m + 2)^{d₀}.)

## M5. Lemma LOCL (localisation of regression coefficients) — new

Put **ε(r) := (1 + L₀)·B·C₀ Σ_{m≥⌊r⌋}(m + 2)^{d₀}e^{−t′m} = (1 + L₀)B C₀T_{d₀}(⌊r⌋, t′)** (the formula of
`reviews/R01_statement_lock_sol.md:73`); ε(r) ≤ ε̄ e^{−t′⌊r⌋/2} with ε̄ := (1 + L₀)BC₀μ(t′)/(1 − e^{−t′/2}) (G-tail);
ε(r) → 0 as r → ∞, monotonically in ⌊r⌋.

**Lemma LOCL.** Let Ψ ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) (either branch), T ⊆ [p], l ∉ T, r ≥ 0, U := T ∩ B(l, r), V := T ∖ U, and
write β_T(l) = (β_{T,U}, β_{T,V}). Then
 (i) (exact identity) β_{T,U} = β_U(l) − Ψ_UU⁻¹Ψ_UVβ_{T,V};
 (ii) ‖Ψ_UU⁻¹Ψ_UV‖_{1→1} = max_{w∈V} ‖β_U(w)‖₁ ≤ L₀;
 (iii) ‖β̄_T(l) − β̄_U(l)‖₁ ≤ (1 + ‖Ψ_UU⁻¹Ψ_UV‖_{1→1})‖β_{T,V}‖₁ ≤ (1 + L₀)‖β_{T,V}‖₁ ≤ ε(r);
 (iv) (variance comparison) with Δ := β̄_T(l) − β̄_U(l):  ψ_{l|U} = ψ_{l|T} + Var(Δᵀζ) = ψ_{l|T} + ΔᵀΨΔ, and
      ΔᵀΨΔ ≤ C‖Δ‖₂² ≤ C ε(r)²; hence ψ_{l|U}/ψ_{l|T} ≤ 1 + Cε(r)²/c;
 (v) (atom form) for every x ∈ ℝ^p, |Δᵀx| ≤ ε(r)·max_{j∈T}|x_j| (Hölder; Δ is supported on T).
All bounds are uniform in T, l, r, p, n and the pseudometric. Conventions: if U = ∅ then β_U = 0 and (i) reads
0 = 0 − (empty) (the identity is vacuous and Δ = β̄_T); if V = ∅ then U = T and Δ = 0. A matrix with zero rows or zero columns has induced ℓ¹ operator norm zero. In (ii) and (v), a maximum over an
empty index set is defined to be zero [R02-1].

*Proof.* (i) The normal equations Ψ_TTβ_T(l) = Ψ_{Tl}, restricted to the U-rows, read Ψ_UUβ_{T,U} + Ψ_UVβ_{T,V} = Ψ_{Ul};
multiply by Ψ_UU⁻¹ (λ_min(Ψ_UU) ≥ c) and use β_U(l) = Ψ_UU⁻¹Ψ_{Ul}.
(ii) The ℓ¹→ℓ¹ operator norm is the maximal column ℓ¹ norm; column w ∈ V of Ψ_UU⁻¹Ψ_UV is Ψ_UU⁻¹Ψ_{Uw} = β_U(w) (w ∉ U),
bounded by RB_M (applied with l := w, A := U).
(iii) By (i), Δ = (−Ψ_UU⁻¹Ψ_UVβ_{T,V} on U; β_{T,V} on V; 0 elsewhere), so ‖Δ‖₁ ≤ ‖Ψ_UU⁻¹Ψ_UV‖_{1→1}‖β_{T,V}‖₁ + ‖β_{T,V}‖₁.
By RB_M, |β_T(l)_v| ≤ Be^{−t′δ(l,v)}, and every v ∈ V has δ(l, v) > r; (G-shell) gives
‖β_{T,V}‖₁ ≤ BC₀Σ_{m≥⌊r⌋}(m + 2)^{d₀}e^{−t′m}. Multiply by (1 + L₀).
(iv) ζ_l − β̄_Uᵀζ = (ζ_l − β̄_Tᵀζ) + Δᵀζ. The first term is uncorrelated with ζ_T (normal equations), the second is a linear
function of ζ_T (Δ supported on T); variances add. Var(ζ_l − β̄_Uᵀζ) = ψ_{l|U}, Var(ζ_l − β̄_Tᵀζ) = ψ_{l|T}. Then
ΔᵀΨΔ ≤ λ_max(Ψ)‖Δ‖₂² ≤ C‖Δ‖₁²; finally ψ_{l|T} ≥ c (CD_M(b)). (v) |Δᵀx| ≤ ‖Δ‖₁ max_{j∈supp Δ}|x_j|. ∎

*Remarks.* (1) The Θ-branch enters only through (K_Ψ, t_Ψ) of CD_M(c) inside RB_M (Σ-branch decay of Ψ itself), as
required. (2) TAIL_M(a) and LOCL(iv) bound the same quantity Var(Δᵀζ) = Var(E[ζ_l | ζ_T] − E[ζ_l | ζ_U]) by two
different routes (κ(r) vs Cε(r)²); either suffices for every use below. (3) Unlike the crude bound
‖Δ‖₁ ≤ ‖β_T‖₁ + ‖β_U‖₁ ≤ 2L₀ (used by LOC2 `L4_LOCd.md:51-53` for NA-R's (R2)), LOCL makes the atom coefficient
**vanish** as r → ∞; with r_n → ∞ the atom part of NA-R becomes o(1)·max|atom statistic|, which is what R3(b) of
`STATEMENT.md:158-161` needs. Sample usage: with r_n = ⌈(log log n)²⌉, ε(r_n) ≤ ε̄e^{−t′((log log n)²−1)/2} = o((log n)^{−M})
for every fixed M.

## M6. Lemma SC_M (rescaling to unit diagonal stays in the class)

If Ψ ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) and R := D^{−1/2}ΨD^{−1/2}, D := diag(Ψ), then (same pseudometric) R is unit diagonal with
spectrum in [c/C, C/c], and R obeys the Σ-branch envelope with (K/c, a) if Ψ does (Σ-branch), the Θ-branch envelope with
(KC, a) if Ψ does (Θ-branch). Hence R ∈ 𝓛𝓞𝓒(C₀, d₀, c/C, C/c, K max(1/c, C), a).
*Proof.* Ψ_jj ∈ [c, C] (diagonal entries of a matrix with spectrum in [c, C]). For x ≠ 0, xᵀRx = yᵀΨy with y = D^{−1/2}x,
‖y‖² ∈ [‖x‖²/C, ‖x‖²/c]: spectrum of R ⊆ [c/C, C/c]. R_jk = Ψ_jk/√(Ψ_jjΨ_kk), |R_jk| ≤ |Ψ_jk|/c; R⁻¹ = D^{1/2}Ψ⁻¹D^{1/2},
|(R⁻¹)_jk| ≤ C|(Ψ⁻¹)_jk|. ∎ (This is what makes "Σ_n unit diagonal WLOG" of `STATEMENT.md:22-23` compatible with membership in
𝓛𝓞𝓒 at changed fixed constants; it is a remark, not used below.)

## M7. Constant table (all explicit in (C₀, d₀, c, C, K, a))

| Symbol | Value | Where |
|---|---|---|
| S(t; K′, a′), t*(α, K′, a′) | K′C₀Σ_{m≥0}(m+2)^{d₀}e^{−(a′−t)m}(1−e^{−t(m+1)}); max{t < a′ : S ≤ α/2} | M1 |
| (t₁, K₁) | Σ: (t*(c,K,a), 2/c); Θ: (a, K) | M2 |
| (t₂, K₂) | (t*(1/C, K₁, t₁), 2C) | M2 |
| (t_Ψ, K_Ψ) | Σ: (a, K); Θ: (t*(1/C,K,a), 2C) | M2(c) |
| t′, B, L₀ | t*(c, K_Ψ, t_Ψ); 2C/c (2/c if unit diagonal); BC₀T_{d₀}(0, t′) | M3 |
| κ(r) | (K₂²/c)C₀T_{d₀}(⌊r⌋, 2t₂) | M4 |
| ε(r), ε̄ | (1+L₀)BC₀T_{d₀}(⌊r⌋, t′); (1+L₀)BC₀μ(t′)/(1−e^{−t′/2}) | M5 |
| μ(t) | e^{t}(2d₀/(et))^{d₀} | M0 |
The constants are extremely conservative (iterated Combes–Thomas); they are fixed positive numbers when the class
constants are fixed, which is all the asymptotic arguments use.

## M8. Falsification record (`numerics/n2_metric.py` → `numerics/n2_metric_out.txt`)

Geometries: (1) 2-D jittered grid of cluster centres (jitter 0.45, so many centre distances lie in (0, 1)) carrying
clusters of 1–3 indices at mutual distance 0; (2) a line with 30 % zero gaps (runs ≤ 4) and Exp(0.6) gaps; (3) the block
pseudometric (0 within blocks of size ≤ 4, p between). Matrices: Σ-branch exponential kernels and Θ-branch diagonally
dominant precisions, all with random **non-unit diagonals** (scales in [0.6, 1.4]); block CS. C₀ is the exact growth
constant. Checks: CT_M with the analytic t* on Ψ (Σ) / Θ (Θ) and random principal submatrices; the Schur step
"row/column sums of |E| ≤ S(t)" for several t (this is the step where shells now start at m = 0); CD_M(a),(b); RB_M with
B = 2C/c and the observed min G_ll (< 1 in the non-unit runs, confirming the R01-4 correction is needed); LOCL identity
(i), operator-norm identity (ii), chain (iii), variance identity (iv) and Cε², TAIL_M ratio; and an exhaustive
enumeration of all (l, T, r) at p = 10 with zero-distance pairs (both branches). Results (5 geometry/branch runs,
p = 235–260, 234–478 zero-distance pairs and up to 1226 pairs at distance in (0, 1)):
* CT_M with the analytic t*: max |(A⁻¹)_ij|/((2/α)e^{−t*δ}) ∈ [0.38, 0.44] over full matrices and 11 random principal
  submatrices each; Schur step max (row/column sum of |E|)/S(t) ≤ 0.133 (0.000 for the block pseudometric, where E = 0).
* CD_M(a) ratio ≤ 0.44; every sampled conditional spectrum inside [c, C].
* RB_M ratio ≤ 0.016; observed min G_ll ∈ [0.48, 0.71] < 1 in every non-unit run (the unit-diagonal shortcut G_ll ≥ 1
  would be false; G_ll ≥ 1/C held).
* LOCL: identity (i) residual ≤ 2.9e-15, operator-norm identity (ii) and ≤ L₀ with 0 violations, chain (iii) and
  ΔᵀΨΔ ≤ Cε² with 0 violations, variance identity (iv) residual ≤ 1.2e-15; ‖β_T − β̄_U‖₁ decays from ≈ 1.4 (r = 0) to
  ≈ 10⁻⁴–10⁻³ (r = 8). Exhaustive p = 10: 56 320 (l, T, r) triples per branch, identity residuals ≤ 4.4e-16, 0 violations.
* Honest caveat on power: the analytic ε(r), κ(r), L₀ are astronomically large at the probed radii (e.g. ε(0) ≈ 10²⁵–10⁸⁹,
  t₂ ≈ 10⁻¹⁷ in the 2-D cluster Σ-branch), so the checks "‖Δ‖₁ ≤ ε(r)", "VarD ≤ κ(r)" are passed trivially; the
  informative checks are the CT_M ratio, the Schur step, the exact identities and the inequality chain. The analytic
  proofs above are the certificate.
