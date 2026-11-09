# L3 — Key lemma U-LOC: uniform add-statistic bound for one global factor + metric-local idiosyncratic part

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09. Falsification numerics: `numerics/n3_uloc.py` →
`numerics/n3_out.txt` (identity (a) error ≤ 1.3e-14, 0 violations of (b) in 27 324 random/greedy pairs [R05a-16] on non-block Ψ);
`numerics/n3b_exhaustive.py` → `numerics/n3b_out.txt` (exhaustive p ≤ 10, planned per R01 optional suggestion).
Check record: R03 (Codex gpt-6.1-sol xhigh, `reviews/R03_L3L6_check_sol.md`): VERIFIED-WITH-AMENDMENTS (1 MAJOR: empty
conditioning set for TL; 2 MINOR), all applied (v1.1; `reviews/R03_disposition.md`). The exhaustive script was corrected
to include T = [p] in the c_𝒢 enumeration and re-run [R03-3].

Generalises W2-FAC-A `lemmas/L1_uniform_add.md` (Lemma U(a)–(c), Corollary U; "PROVED (by this seat, unchecked)", R02 Sol
xhigh VERIFIED-WITH-AMENDMENTS, inside W2-FAC-A "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)") from block-diagonal Ψ to Ψ ∈ 𝓛𝓞𝓒 (STATEMENT §2).
The only new inputs are the metric toolkit of `lemmas/L1_metric.md` (RB_M: uniform ℓ¹ regression bound L₀; CD_M(b):
conditional variances of ζ are ≥ c; LOCL: ℓ¹ localisation ε(r) → 0 with the variance comparison).

## L3.0 Setting and notation

Σ = λλᵀ + Ψ is a p × p correlation matrix (unit diagonal), Ψ ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) with pseudometric δ;
𝒢 a partition of [p] into groups of size ≤ γ̄, G := |𝒢| ≤ p; c_𝒢 := inf_{∅≠T} s_T/h_𝒢(T) > 0;
κ′ := sup_{T, l∉T}|λ̃_{l|T}|/√ψ_{l|T}; κ := κ′/√c_𝒢 ≤ κ̄ (STATEMENT (A2-1)). Since Ψ_jj = 1 − λ_j² ≥ λ_min(Ψ) ≥ c,
|λ_j| ≤ 1 and Ψ_jj ≤ 1.
For T ⊆ [p], l ∉ T (Ψ_TT ≻ 0 always): β_T(l) := Ψ_TT⁻¹Ψ_{Tl} ∈ ℝ^T (zero-padded to ℝ^p when compared),
ψ_{l|T} := Ψ_ll − Ψ_{lT}β_T(l), λ̃_{l|T} := λ_l − β_T(l)ᵀλ_T, s_T := λ_TᵀΨ_TT⁻¹λ_T (empty-set conventions as FACA U(a):
β_∅ = 0, ψ_{l|∅} = Ψ_ll, λ̃_{l|∅} = λ_l, s_∅ = 0).
Facts used: (F1) ψ_{l|T} ≥ c (Schur complement of a principal submatrix of Ψ ⪰ cI); (F2) ‖β_T(l)‖₁ ≤ L₀ (RB_M), hence
|λ̃_{l|T}| ≤ 1 + L₀ and κ′ ≤ κ′_bd := (1 + L₀)/√c; (F3) s_T ≥ c_𝒢 h_𝒢(T) > 0 for T ≠ ∅ (definition of c_𝒢).

A probability space carries independent ξ₀ ~ N(0, 1) and ζ ~ N(0, Ψ); γ := λξ₀ + ζ ~ N(0, Σ). For T ≠ ∅ put
  Ξ_{l,T} := (ζ_l − β_T(l)ᵀζ_T)/√ψ_{l|T},  F_T := λ_TᵀΨ_TT⁻¹ζ_T/√s_T,  W_T := (ξ₀ − √s_T F_T)/√(1 + s_T),
and Ξ_{l,∅} := ζ_l/√Ψ_ll, W_∅ := ξ₀. Z^M_{T,l}(x) is the standardised innovation of FACA L1 (L1.0 notation).

## L3.1 Lemma U-LOC(a) — exact decomposition (any Ψ ≻ 0)

For every T ⊆ [p] and l ∉ T: Ξ_{l,T} ~ N(0, 1), W_T ~ N(0, 1), F_T ~ N(0, 1) (T ≠ ∅), Ξ_{l,T} is independent of
(ξ₀, ζ_T) — hence of W_T — and

  Z^Σ_{T,l}(γ) = [√ψ_{l|T} Ξ_{l,T} + (λ̃_{l|T}/√(1 + s_T)) W_T] / √(ψ_{l|T} + λ̃²_{l|T}/(1 + s_T)).          (a)

*Proof.* FACA U(a) verbatim with U replaced by T in ψ, λ̃, Ξ; we re-check the two places where block-diagonality was
used there. Let 𝓗_T := span{γ_j : j ∈ T} ⊆ 𝓚_T := span{ξ₀, ζ_j : j ∈ T} (L² of the space; dim 𝓚_T = |T| + 1 since
Cov(ξ₀, ζ_T) = diag(1, Ψ_TT) ≻ 0; dim 𝓗_T = |T| since Σ_TT ⪰ Ψ_TT ≻ 0). Decompose orthogonally
γ_l − P_{𝓗_T}γ_l = (γ_l − P_{𝓚_T}γ_l) + (P_{𝓚_T}γ_l − P_{𝓗_T}γ_l).
*First term (use 1).* P_{𝓚_T}γ_l = λ_lξ₀ + P_{𝓚_T}ζ_l, and since ζ_l and ζ_T are both uncorrelated with ξ₀,
P_{𝓚_T}ζ_l = P_{span ζ_T}ζ_l = β_T(l)ᵀζ_T (no block structure needed). So the first term is √ψ_{l|T}Ξ_{l,T}, with variance
ψ_{l|T} > 0, orthogonal to 𝓚_T; being jointly Gaussian with (ξ₀, ζ_T), Ξ_{l,T} is independent of them.
*Second term (use 2).* ω_T := ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T ∈ 𝓚_T satisfies E[ω_Tγ_j] = λ_j − λ_TᵀΨ_TT⁻¹Ψ_{Tj} = 0 (j ∈ T), and
Var ω_T = 1 + s_T; FACA's argument shows 𝓚_T ⊖ 𝓗_T = span(ω_T), W_T = ω_T/√(1 + s_T) (= the displayed definition since
λ_TᵀΨ_TT⁻¹ζ_T = √s_T F_T). The coefficient is E[γ_lW_T] = E[(λ_lξ₀ + ζ_l)ω_T]/√(1 + s_T)
= (λ_l − λ_TᵀΨ_TT⁻¹Ψ_{Tl})/√(1 + s_T) = λ̃_{l|T}/√(1 + s_T) (symmetry of Ψ_TT⁻¹; no block structure needed).
Assembly as in FACA. Var F_T = λ_TᵀΨ_TT⁻¹Ψ_TTΨ_TT⁻¹λ_T/s_T = 1. ∎

## L3.2 Lemma U-LOC(b) — deterministic bound

For every T ⊆ [p], l ∉ T:
  |Z^Σ_{T,l}(γ)| ≤ |Ξ_{l,T}| + κ′|ξ₀| + κ′(|F_T|/√s_T)·1{T ≠ ∅}.                                             (b)
*Proof.* Write (a) as (αΞ + βW)/√(α² + β²) with α = √ψ_{l|T}, β = λ̃_{l|T}/√(1 + s_T). Since √(α² + β²) ≥ α,
|Z| ≤ |Ξ| + (|β|/α)|W| = |Ξ| + κ′_{l,T}|ξ₀ − √s_TF_T|/(1 + s_T) with κ′_{l,T} := |λ̃_{l|T}|/√ψ_{l|T} ≤ κ′. Then
|ξ₀|/(1 + s_T) ≤ |ξ₀| and, for T ≠ ∅ (s_T > 0 by F3), √s_T/(1 + s_T) ≤ 1/√s_T. For T = ∅, W = ξ₀. ∎

## L3.3 Lemma U-LOC(c) — idiosyncratic part: references + vanishing atoms

Let n ≥ 16 (so log log n ≥ 1.01), r_n := ⌈(log log n)²⌉, B(l, r) := {v : δ(l, v) ≤ r}, and N_n := C₀(1 + r_n)^{d₀}
(≥ |B(l, r_n)| by polynomial growth). Let ε_n := ε(r_n) with ε(·) the LOCL function of `lemmas/L1_metric.md`.
Reference family ℛ_n := {(l, A) : l ∈ [p], A ⊆ B(l, r_n) ∖ {l}}, |ℛ_n| ≤ p·2^{N_n}; for (l, A) ∈ ℛ_n,
R_{l,A} := (ζ_l − β_A(l)ᵀζ_A)/√ψ_{l|A} ~ N(0, 1). Define
  E_ref := {|R_{l,A}| ≤ t_n ∀(l, A) ∈ ℛ_n},  t_n² := 2 log(p 2^{N_n}) + 2 log log n;
  E_atom := {max_v |ζ_v| ≤ t′_n},  t′_n² := 2 log p + 2 log log n.
Then P(E_refᶜ) ≤ 1/log n and P(E_atomᶜ) ≤ 1/log n, and on E_ref ∩ E_atom, for every T ⊆ [p] and l ∉ T,
  |Ξ_{l,T}| ≤ √(1 + Cε_n²/c)·t_n + ε_n t′_n/√c =: Ξ̄_n,   and   Ξ̄_n ≤ √(2 log p) + η_n,  η_n = o(√log n)
with η_n deterministic, depending only on (A, C₀, d₀, c, C, K, a) and n.

*Proof.* Tails: P(|N(0,1)| > u) ≤ e^{−u²/2} for u ≥ 0 (since P(N > u) ≤ ½e^{−u²/2}); unions over |ℛ_n| standard
normals and over p coordinates ζ_v with Var ζ_v = Ψ_vv ≤ 1 give |ℛ_n|e^{−t_n²/2} = 1/log n and p e^{−t′_n²/2} = 1/log n.
Fix T, l ∉ T and put A := T ∩ B(l, r_n) (so (l, A) ∈ ℛ_n since l ∉ T) and Δ := β_T(l) − β̄_A(l) (zero-padded). Since
β_T(l)ᵀζ_T = β_A(l)ᵀζ_A + Δᵀζ,
  √ψ_{l|T}|Ξ_{l,T}| = |(ζ_l − β_A(l)ᵀζ_A) − Δᵀζ| ≤ √ψ_{l|A}|R_{l,A}| + ‖Δ‖₁ max_v|ζ_v| ≤ √ψ_{l|A}t_n + ε_n t′_n
by LOCL (‖Δ‖₁ ≤ ε(r_n) uniformly in T, l). LOCL's variance comparison gives ψ_{l|A} ≤ ψ_{l|T} + Cε_n², and ψ_{l|T} ≥ c (F1);
dividing by √ψ_{l|T} gives the first display. (If A = T, Δ = 0 and Ξ_{l,T} = R_{l,T}.)
Rates: log p ≤ A log n; N_n = O((log log n)^{2d₀}) = o(log n); ε_n → 0 (LOCL: ε(r) → 0 as r → ∞, r_n → ∞). Hence
t_n ≤ √(2 log p) + √(2N_n log 2 + 2 log log n), and
η_n := (√(1 + Cε_n²/c) − 1)√(2A log n) + √(1 + Cε_n²/c)·√(2N_n log 2 + 2 log log n) + ε_n√(2A log n + 2 log log n)/√c
= o(√log n). ∎

*Remark.* No union over the lattice: the only unions are over p·2^{N_n} = p·n^{o(1)} references and p atoms. The atom part
is controlled through ‖Δ‖₁ → 0, so (unlike NA-R's (R2), where atoms carry bounded ℓ¹ weight over a polylogarithmic set)
the atom set may be all of [p]. No sample quantity appears: this is a statement about one Gaussian vector.

## L3.4 Lemma U-LOC(d) — factor part: entropy-stratified union

For 1 ≤ h ≤ G let 𝒯_h := {∅ ≠ T ⊆ [p] : h_𝒢(T) = h}; with b := 2^{γ̄} − 1, |𝒯_h| ≤ C(G, h)b^h (choose the h groups met,
then a nonempty subset of each). Put x_h := log C(G, h) + h log b + 2 log(h + 1) + log log n + log 2 and
  E_F := {|F_T| ≤ √(2x_{h_𝒢(T)}) for every nonempty T ⊆ [p]}.
Then P(E_Fᶜ) ≤ 1/log n, and on E_F, for every nonempty T,
  |F_T|/√s_T ≤ √(2x_h/(c_𝒢h)) ≤ c_𝒢^{−1/2}[√(2 log(eγ̄p/|T|)) + ϱ_n],  ϱ_n := √(2(γ̄ + 3) log 2 + 2 log log n),   (d)
with h := h_𝒢(T).
*Proof.* Each F_T ~ N(0, 1) (L3.1; no independence across T is used). Union: P(E_Fᶜ) ≤ Σ_h |𝒯_h|e^{−x_h} ≤
Σ_{h≥1}[2(h + 1)² log n]⁻¹ ≤ (π²/6 − 1)/(2 log n) ≤ 1/log n. On E_F, s_T ≥ c_𝒢h (F3) gives the first inequality. For the
second: log C(G, h) ≤ h log(eG/h); 2 log(h + 1)/h ≤ 2 log 2; (log log n + log 2)/h ≤ log log n + log 2; log b ≤ γ̄ log 2; so
x_h/h ≤ log(eG/h) + (γ̄ + 3) log 2 + log log n; and since h ≥ |T|/γ̄ and G ≤ p, log(eG/h) ≤ log(eγ̄p/|T|).
Finally √(u + v) ≤ √u + √v. ∎

*Remark (normalisation).* With 𝒢 = singletons this is the generic bound (c_𝒢 = inf s_T/|T|). When Ψ is block-diagonal with
respect to bounded groups 𝒢 (FACA's class), s_T = Σ_g s_{T∩g} ≥ c_min h_𝒢(T) with FACA's c_min, i.e. c_𝒢 ≥ c_min and,
since λ̃_{l|T} = λ̃_{l|T∩g(l)} and ψ_{l|T} = ψ_{l|T∩g(l)} there, κ′ coincides with FACA's κ′; so κ_UNI ≤ κ_FACA (= 1 for
every block compound symmetry, FACA L5 Lemma κ). [Equality c_𝒢 = c_min: the infimum over a single group's subsets V is
FACA's c_min, h = 1.]

## L3.5 Corollary U-LOC (population and sample versions)

Let E_U := E_ref ∩ E_atom ∩ E_F ∩ {|ξ₀| ≤ √(2 log log n)}; P(E_Uᶜ) ≤ 4/log n (the last event: e^{−log log n}).
**(Population.)** On E_U, for every T ⊆ [p] (including T = ∅ [R03-1]) and l ∉ T,
  |Z^Σ_{T,l}(γ)| ≤ √(2 log p) + κ√(2 log(eγ̄p/|T|))·1{T ≠ ∅} + ε^U_n,
  ε^U_n := η_n + κ′_bd√(2 log log n) + κ̄ϱ_n = o(√log n)  (deterministic; constants (A, C₀, d₀, c, C, K, a, γ̄, κ̄)),
where for T = ∅ the whole size-dependent summand is defined as 0 (its logarithm is not evaluated).
*Proof.* (b), (c), (d) and κ′ ≤ κ′_bd, κ ≤ κ̄. For T = ∅, (b) gives |Z| ≤ |Ξ_{l,∅}| + κ′|ξ₀| and (c) applies with A = ∅
(Δ = 0), so |Z| ≤ √(2 log p) + η_n + κ′_bd√(2 log log n) ≤ √(2 log p) + ε^U_n on the same event. ∎
**Consequence for TL [R03-1].** On E_U, uniformly over all T and l ∉ T (empty or not),
  |Z^Σ_{T,l}(γ)| ≤ Z̄^pop_n := √(2 log p) + κ̄√(2 log(eγ̄p)) + ε^U_n = O(√log n).
**(Sample; design (E) or (R) conditionally on X.)** Let X be such that ‖R̂ − Σ‖_op ≤ δ ≤ c/4, g := Xᵀε/(σ√(n − 1)), and
Z_{T,l} the add statistic (FACA (0.1): Z_{T,l} = Z^{R̂}_{T,l}(g), g | X ~ N(0, R̂)). Then, with
L_ψ := C₂ + 2C₃/ψ₀ of FACA U(d) at ψ₀ := c (λ_min(Σ) ≥ λ_min(Ψ) ≥ c),
  P(∀ T ⊆ [p], l ∉ T : |Z_{T,l}| ≤ √(2 log p) + κ√(2 log(eγ̄p/|T|))·1{T ≠ ∅} + ε^U_n + L_ψδ√(5(p + 1) log log n) | X)
    ≥ 1 − 5/log n,
(the T = ∅ summand defined as 0 [R03-1]); in particular, on the same event, max_{T, l∉T}|Z_{T,l}| ≤ Z̄_n :=
√(2 log p) + κ̄√(2 log(eγ̄p)) + ε^U_n + L_ψδ√(5(p + 1) log log n), which covers the empty conditioning sets
B = T ∖ {i} that FACA's TL proof (L3_NA_TL.md L3.2) meets when s₀ = 1. Under UNI-1's additional rate
δ_n√(p log log n) → 0, Z̄_n = O(√log n) [R04-3].
*Proof.* FACA Corollary U's coupling, unchanged: γ := Σ^{1/2}R̂^{−1/2}g ~ N(0, Σ) given X; on an enlarged space with an
independent V ~ N(0, 1), b := Σ⁻¹λ, ξ₀ := bᵀγ + √(1 − λᵀΣ⁻¹λ)V, ζ := γ − λξ₀ (1 − λᵀΣ⁻¹λ > 0 because Ψ ≻ 0). Then
Var ξ₀ = 1, Cov(ξ₀, γ) = λ so Cov(ξ₀, ζ) = 0, Cov ζ = Σ − λλᵀ = Ψ, and γ = λξ₀ + ζ — none of this uses block structure.
FACA U(d) (needs only: Σ a correlation matrix with Σ ⪰ ψ₀I, R̂ a correlation matrix, ‖R̂ − Σ‖ ≤ δ ≤ ψ₀/4) gives
|Z^{R̂}_{T,l}(g) − Z^Σ_{T,l}(γ)| ≤ L_ψδ‖g‖, and P(‖g‖² > 5(p + 1) log log n | X) ≤ 1/log n. Combine with the population
bound on E_U (probability ≥ 1 − 4/log n under the enlarged law, which leaves the law of (X, ε) unchanged; as in FACA, no
claim that E_U is in the original σ-field). ∎

This has exactly the form of FACA Corollary U ("|Z_{T,l}| ≤ √(2 log(p2^γ̄) + 2 log log n) + κ′√(2 log log n) +
κ̄(√(2 log(eγ̄p/|T|)) + ϱ_n) + L_ψδ_n√(5(p + 1) log log n)"), with a deterministic o(√log n) remainder, which is the only
remainder property used in FACA L3.1 [R03-2]; L3.1 of FACA
(the α₀ computation) consumes only this form (`W2-FAC-A/lemmas/L3_NA_TL.md`, proof of Lemma L3.1: "On E_n, Corollary U
gives |Z_{T,l}| ≤ √(2P) + κ̄√(2x_k) + ε_n … = o(√log n)").
