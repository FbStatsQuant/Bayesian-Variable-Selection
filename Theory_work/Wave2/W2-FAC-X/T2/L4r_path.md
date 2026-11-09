# L4r — Path lemma for exact-Gram one-factor designs with general loadings

Status: §L4r.0–L4r.4: **PROVED (by this seat, unchecked)**; §L4r.0–L4r.3 key-lemma check R11 (Codex Sol xhigh, ../reviews/R11_L4rS_X9_check_sol.md): **VERIFIED**. §L4r.5: PROVED (static, conditional hypotheses stated).
§L4r.6: obstruction analysis (not a proof). Falsification numerics: T2/numerics/N_T2_summary.md (closed form validated
against direct linear algebra and against the general production-path code, 32/32 identical paths; 366/366 exact paths
pure null deletions ending at S₀; adversarial non-path sets; end-phase diagnostics).

Setting and notation: T2/STATEMENT_T2.md §1–2. FACB = `Theory_work/Wave2/W2-FAC-B/lemmas/`. Υ_n = I (FACB L1.0: the
sign-flip invariance uses only Gram/score invariances). ψ_j := 1 − λ_j², ψ_lo := 1 − λ_hi² ≤ ψ_j, ν := n/2 + 0.01,
a := n² − 1, L_n := log log n. For T ⊆ [p]: k := |T|; for S₀ ⊆ T: K_T := T ∖ S₀ (kept nulls), m := |K_T|.
𝒩 := [p] ∖ S₀ (all nulls), m_all := |𝒩| = p − s₀.

**Organisation versus FACB L4.** FACB L4 = L4.0 preliminaries, L4.1 gap invariant, L4.2 regime (S), L4.3 bulk
(B1–B4), L4.4 end phase. Here: L4r.0 replaces FACB L1 + L4.0 (exact closed form for general loadings); L4r.1 the event
and standing bounds; L4r.2 two **uniform** lemmas (a good kept null exists at every T; a centre bound at every T) that
replace L4.1 + L4.3 + L4.4 on the range A₁ < A_S — this is FACB's regime-(S) argument L4.2 pushed to a polynomial
range by two new ingredients (L4r.2(a), the Σℓ'τ identity, and L4r.2(b), the top-square-sum centre bound); L4r.3
assembly; L4r.4 the per-class gap invariant (FACB L4.1 analogue, deterministic); L4r.5 static per-class B3; L4r.6 why
FACB L4.3/L4.4 do not transfer.

## L4r.0 Exact closed form (any loadings)

**Data.** As FACB L1.1 (the derivation uses only XᵀX = (n − 1)Σ and Xᵀ1 = 0): with g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ),
r := ‖(C − P_X)ε‖²/σ² ~ χ²_{n−1−p} independent of g, ‖e‖² = σ²(gᵀΣ⁻¹g + r) (e := Cε), and
z := Xᵀy = [(n − 1)Σθ* + σ√(n − 1)g]/s. Write (enlarging the probability space) g = λη + Ψ^{1/2}ξ, η ~ N(0, 1),
ξ ~ N(0, I_p), η, ξ, r independent. For every U: RSS_U := ‖(I − P_U)Y‖², and for U ⊇ S₀, RSS_U = ‖e‖² − σ²Φ(U),
Φ(U) := g_UᵀΣ_UU⁻¹g_U (μ ∈ span X_U; X_Uᵀe = σ√(n − 1)g_U).

**Definitions.** d_i² := aψ_i + 1, ε_i² := aψ_i/d_i², ℓ'_i := √a λ_i/d_i = ε_iℓ_i, d''_i² := (n − 1)ψ_i + 1,
ℓ''_i² := (n − 1)λ_i²/d''_i²; D'_U := 1 + Σ_{i∈U}ℓ'_i², D''_U := 1 + Σ_{i∈U}ℓ''_i²;
ξ̌_i := ξ_i + √(n − 1)√ψ_i θ*_i/σ (= ξ_i for nulls), ζ̌_i := ε_iξ̌_i, ϱ₀ := η + √(n − 1)Λ/σ with Λ := λᵀθ*;
κ₁² := σ²/(s²(n + 1)); X̌_U := (Σ_{i∈U}ℓ'_iζ̌_i − ϱ₀)/D'_U, τ_j(U) := ζ̌_j − ℓ'_jX̌_U (any j ∈ [p]);
γ'_j(U) := ℓ'_j²/(D'_U − ℓ'_j²) (j ∈ U). quad_U := z_UᵀH_U⁻¹z_U, H_U := (n + 1)G_U + I, Q_U := (n − 1) − n quad_U,
ψ_U := 0.02 + Q_U, L_U := log det H_U − log det(G_U + I).

**Lemma L4r.0.** For every U ⊆ [p], j ∈ U, l ∉ U:
(a) quad_U − quad_{U∖j} = κ₁²(1 + γ'_j(U))τ_j(U)²;
(b) X̌_{U∖j} = X̌_U − ℓ'_jτ_j(U)/(D'_U − ℓ'_j²) and X̌_{U∪l} = X̌_U + ℓ'_lτ_l(U)/(D'_U + ℓ'_l²);
(c) quad_{U∪l} − quad_U = κ₁²(1 − ℓ'_l²/(D'_U + ℓ'_l²))τ_l(U)²;
(d) L_U − L_{U∖j} = log(n + 1) + e_j(U), e_j(U) := −log(1 + n/(aψ_j + 1)) + log(D'_U/D'_{U∖j}) − log(D''_U/D''_{U∖j}),
    |e_j(U)| ≤ 3/((n − 1)ψ_lo); for fixed U, e_j(U), γ'_j(U), ε_j depend on j only through λ_j;
(e) for U ⊇ S₀: X̌_U = X_U := (Σ_{i∈U∖S₀}ℓ'_iζ_i − ϱ)/D'_U with ζ_i := ε_iξ_i and ϱ as in STATEMENT §2, and for a
    null j, τ_j(U) = ζ_j − ℓ'_jX_U = ε_j(ξ_j − ℓ_jX_U).

*Proof.* H_U = aΣ_UU + I = diag(aψ_i + 1) + (√aλ_U)(√aλ_U)ᵀ = Δ(I + ℓ'ℓ'ᵀ)Δ, Δ := diag(d_i), since Δℓ' = √aλ. Hence
H_U⁻¹ = Δ⁻¹(I − ℓ'ℓ'ᵀ/D'_U)Δ⁻¹ (Sherman–Morrison), and with z̃ := Δ⁻¹z_U, c_U := ℓ'ᵀz̃/D'_U:
(H_U⁻¹z_U)_j = d_j⁻¹(z̃_j − ℓ'_jc_U), (H_U⁻¹)_jj = d_j⁻²(1 − ℓ'_j²/D'_U). The Schur identity
quad_U − quad_{U∖j} = (H_U⁻¹z_U)_j²/(H_U⁻¹)_jj (X1.2(b), any positive definite H_U with H_{U∖j} its principal submatrix)
gives (z̃_j − ℓ'_jc_U)²·D'_U/(D'_U − ℓ'_j²). Now (Σθ*)_i = λ_iΛ + ψ_iθ*_i and g_i = λ_iη + √ψ_iξ_i, so
z_i = λ_ib + (σ√(n − 1)/s)√ψ_iξ̌_i, b := [(n − 1)Λ + σ√(n − 1)η]/s; since λ_i/d_i = ℓ'_i/√a and √ψ_i/d_i = ε_i/√a,
z̃_i = κ₁(ℓ'_iϱ₀ + ζ̌_i) (κ₁ = σ√(n − 1)/(s√a), b/(√aκ₁) = ϱ₀). Then
z̃_j − ℓ'_jc_U = κ₁[ζ̌_j + ℓ'_jϱ₀ − ℓ'_j(Σℓ'ζ̌ + (D'_U − 1)ϱ₀)/D'_U] = κ₁(ζ̌_j − ℓ'_jX̌_U), proving (a).
(b): X̌_{U∖j}(D'_U − ℓ'_j²) = X̌_UD'_U − ℓ'_jζ̌_j; rearrange. Same for U ∪ l.
(c): apply (a) at U ∪ l and (b): τ_l(U ∪ l) = τ_l(U)D'_U/(D'_U + ℓ'_l²), 1 + γ'_l(U ∪ l) = (D'_U + ℓ'_l²)/D'_U.
(d): det H_U = Πd_i²·D'_U and det(G_U + I) = det((n − 1)Ψ_U + I + (n − 1)λλᵀ) = Πd''_i²·D''_U (matrix determinant
lemma). log(d_j²/d''_j²) = log(n + 1) − log(1 + n/(aψ_j + 1)) because (n + 1)d''_j² = aψ_j + n + 1, and
0 ≤ log(1 + n/(aψ_j + 1)) ≤ n/(aψ_j) ≤ δ_n := 1/((n − 1)ψ_lo). Next, ℓ'_i² − ℓ''_i² = λ_i²n(n − 1)/(d_i²d''_i²) =
ℓ''_i²·n/d_i² ∈ [0, δ_nℓ''_i²]. With φ(x, y) := log(1 + x/y) (x ≥ 0, y ≥ 1), the last two terms of e_j are
φ(x′, y′) − φ(x″, y″), x′ = ℓ'_j² ≥ x″ = ℓ''_j², y′ = D'_{U∖j} ≥ y″ = D''_{U∖j}, x′ − x″ ≤ δ_nx″, y′ − y″ ≤ δ_n(y″ − 1).
φ is increasing in x and decreasing in y, so
φ(x′, y′) − φ(x″, y″) ≤ φ(x′, y″) − φ(x″, y″) ≤ (x′ − x″)/(y″ + x″) ≤ δ_n, and
φ(x′, y′) − φ(x″, y″) ≥ φ(x″, y′) − φ(x″, y″) = −log[(y′/y″)·(y″ + x″)/(y′ + x″)] ≥ −log(y′/y″) ≥ −δ_n.
Total |e_j| ≤ 2δ_n ≤ 3δ_n. Only λ_j, U enter.
(e): Σ_{S₀}ℓ'_iζ̌_i = Σ_{S₀}ε_i²ℓ_iξ_i + (√(n − 1)/σ)Σ_{S₀}ε_i²ℓ_i√ψ_iθ*_i and ℓ_i√ψ_i = λ_i; subtract ϱ₀. ∎

**Gains (exact).** For S₀ ⊆ T with k = |T|, put M_T := νnκ₁²/ψ_T > 0 and Δ_k := log((2p − k)/k) + ½log(n + 1)
(w(k − 1)/w(k) = (2p − k)/k). From F(U) = log w(|U|) − ½L_U − ν log ψ_U, Q_{U∖j} − Q_U = n(quad_U − quad_{U∖j}) and
L4r.0:
  G_del(j; T) = Δ_k + ½e_j(T) − ν log(1 + M_T(1 + γ'_j(T))τ_j(T)²/ν)                                  (j ∈ T)
  G_add(l; T) = −Δ_{k+1} − ½e_l(T ∪ l) − ν log(1 − M_T(1 − ℓ'_l²/(D'_T + ℓ'_l²))τ_l(T)²/ν)              (l ∉ T, k < K)
  G_sw(j, l; T) = G_del(j; T) + G_add(l; T ∖ j)                                                        (telescoping)
(the logarithms' arguments are ψ_{T∖j}/ψ_T, ψ_{T∪l}/ψ_T > 0). For a null j, τ_j(T)² = ε_j²(ξ_j − ℓ_jX_T)² and every
other j-dependent factor depends on j only through λ_j: **within a loading value, G_del is a strictly decreasing
function of |ξ_j − ℓ_jX_T|.** (Self-test: numerics/eg_selftest_out.txt.)

## L4r.1 Event, multiplier, truth moves

**Event E_n** := E1 ∩ E2 ∩ E3′ ∩ E4′ with (FACB L3 notation, 𝒩* replaced by 𝒩):
E1: |η| ≤ L_n, |ξ_j| ≤ L_n (j ∈ S₀); E2: r ≥ (n − 1 − p)(1 − n^{−1/3}), |gᵀΣ⁻¹g + r − (n − 1)| ≤ n^{2/3},
|θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2}; E3′: max_{j∈𝒩}|ξ_j| ≤ H̄, H̄² := 2log(2m_all + 2) + 2L_n; E4′: ζ_(i)² ≤ Z_i² :=
2log(2m_all/i) + 4L_n for 1 ≤ i ≤ m_all (ζ_(i) the i-th largest |ξ_j|, j ∈ 𝒩). **P(E_n) → 1**: FACB L3.1's proofs of
E1–E4 verbatim (they use only that the ξ_j are iid N(0, 1), η ~ N(0, 1), gᵀΣ⁻¹g ~ χ²_p independent of r, and p ≤ n/2;
compound symmetry is not used).

Standing consequences on E_n, n ≥ n₀ (all constants depend on λ_lo, λ_hi, ϑ, σ, s₀, A₁ only):
(s1) s² ∈ [σ²/2, 2(θ*ᵀΣθ* + σ²)] (FACB L3 (c1)); θ*ᵀΣθ* ≤ ‖ϑ‖₁².
(s2) **Top-square sums:** for 1 ≤ m ≤ m_all, Σ_{i≤m}ζ_(i)² ≤ Σ_{i≤m}Z_i² ≤ m(Z_m² + 2) (log m! ≥ m log(m/e)).
(s3) |ϱ| ≤ (1 + s₀ℓ_hi)L_n + 1 =: C_ϱL_n (E1; the last term of ϱ is ≤ √n·Σ|θ*_i|/(σaψ_lo) → 0).
(s4) **Multiplier.** Q_U ≥ RSS_U/s² for every U (FACB L1.5(b), lower half: uses only H_U ⪰ (n + 1)G_U), so for T ⊇ S₀
  M_T ≤ νnσ²/((n + 1)RSS_T) ≤ ½nσ²/RSS_T. Φ(T) = g̃_Tᵀ(I + ℓ_Tℓ_Tᵀ)⁻¹g̃_T ≤ ‖g̃_T‖² (g̃_i := g_i/√ψ_i = ℓ_iη + ξ_i)
  ≤ 2pH̄² + 2s₀L_n² + 2pℓ_hi²L_n² ≤ n/log n (p ≤ n^{A₁}, A₁ < 1), and ‖e‖²/σ² ≥ n − 1 − n^{2/3} (E2), so
  **M_T ≤ ½(1 + 2/log n)** uniformly in T ⊇ S₀.
(s5) Q_U ≤ RSS_U/s² + 1 + δ_n for every U (FACB L1.5(b), upper half, with 1 − ρ replaced by ψ_lo ≤ λ_min(Σ_UU)); and, separately, quad_U ≥ 0 gives Q_U = (n − 1) − n·quad_U ≤ n − 1, hence ψ_U ≤ n − 0.98 < n for every U
  (corrected by the lead after R16 item 1).
(s6) p ≤ n^{A₁} ≤ ⌊n/2⌋, so K = p and every move between sets of size ≤ p is feasible.

**(TL) Truth moves.** Let S₀ ⊆ T, j ∈ S₀, T′ ∈ {T ∖ j, T ∖ j ∪ l (l ∉ T)}, U := T′ ∪ {j} (= T or T ∪ l),
r_j := (I − P_{T′})x_j. Since μ − θ*_jx_j ∈ span X_{T′}: RSS_{T′} − RSS_U = (r_jᵀY)²/‖r_j‖², r_jᵀY = θ*_j‖r_j‖² + r_jᵀe,
‖r_j‖² = (n − 1)/(Σ_UU⁻¹)_jj ≥ (n − 1)ψ_lo, |r_jᵀe|/‖r_j‖ ≤ ‖P_Ue‖ = σΦ(U)^{1/2} ≤ σ(n/log n)^{1/2} (as in (s4); Φ(U)
bound holds for any U). So RSS_{T′} − RSS_U ≥ (|ϑ_j|((n − 1)ψ_lo)^{1/2} − σ(n/log n)^{1/2})² ≥ ½ϑ_min²ψ_lon, and
RSS_T − RSS_U = ‖(P_U − P_T)e‖² ≤ σ²Φ(U) ≤ σ²n/log n. By (s4)–(s5), Q_{T′} − Q_T ≥ (RSS_{T′} − RSS_T)/s² − 1 − δ_n ≥ c_θn,
c_θ := ϑ_min²ψ_lo/(5s_max²), so ν log(ψ_{T′}/ψ_T) ≥ (n/2)log(1 + c_θ). Size terms: deletion ≤ log(2p) + ½log(n + 1) + δ_n
(L4r.0(d)); swap: prior ratio 1 and ½|L_{T′} − L_T| = ½|e_l(T′) − e_j(T)| ≤ 3δ_n. Hence every truth deletion and every
truth-out swap has gain ≤ log(2p) + log n − (n/2)log(1 + c_θ) ≤ −c n. Truths are never added (S₀ ⊆ T). ∎

## L4r.2 Two uniform lemmas (the new ingredients)

**Lemma L4r.2(a) (a good kept null exists).** On E_n, for every T ⊇ S₀ with m ≥ 1 there is i ∈ K_T with
|τ_i(T)| ≤ H̄ + |ϱ|/ℓ'_lo (ℓ'_lo := min_j ℓ'_j ≥ ℓ_lo(1 − 1/(aψ_lo))).
*Proof.* By L4r.0(e), Σ_{i∈K_T}ℓ'_iτ_i = Σ_Kℓ'_iζ_i − X_TΣ_Kℓ'_i² = (X_TD'_T + ϱ) − X_T(D'_T − κ'_S) = X_Tκ'_S + ϱ,
κ'_S := 1 + Σ_{S₀}ℓ'_i² ≥ 1. Suppose X_T ≥ 0. Every kept i has τ_i = ζ_i − ℓ'_iX_T ≤ ζ_i ≤ |ξ_i| ≤ H̄ (E3′; ε_i ≤ 1).
If every kept i had τ_i < −(H̄ + |ϱ|/ℓ'_lo), then Σℓ'_iτ_i < −(H̄ + |ϱ|/ℓ'_lo)Σ_Kℓ'_i ≤ −|ϱ| (Σ_Kℓ'_i ≥ ℓ'_lo),
contradicting Σℓ'_iτ_i = X_Tκ'_S + ϱ ≥ −|ϱ|. So some kept i has −(H̄ + |ϱ|/ℓ'_lo) ≤ τ_i ≤ H̄. X_T < 0: symmetric. ∎

**Lemma L4r.2(b) (centre bound).** On E_n, for every T ⊇ S₀: |X_{S₀}| ≤ |ϱ|, and for m ≥ 1,
|X_T| ≤ (Z_m² + 2)^{1/2}/ℓ'_lo + |ϱ|.
*Proof.* Cauchy–Schwarz: |Σ_Kℓ'_iζ_i| ≤ (Σ_Kℓ'_i²)^{1/2}(Σ_Kξ_i²)^{1/2} ≤ Q'^{1/2}(m(Z_m² + 2))^{1/2} by (s2) (K has m
elements), Q' := Σ_Kℓ'_i² ≥ mℓ'_lo². Divide by D'_T ≥ Q' and use |ϱ|/D'_T ≤ |ϱ|. ∎

(Numerics: both hold on all adversarial sets, numerics/adversarial_T_out.txt; (b) is nearly attained by sets of
same-sign low-loading nulls, which is why the addition exponent below depends on R.)

## L4r.3 Proof of Lemma L4r-S (STATEMENT §3)

Fix n ≥ n₀ and the event E_n. Write R′ := ℓ_hi/ℓ'_lo ≤ R(1 + 2/(aψ_lo)), γ̄′ := ℓ_hi²/κ'_S ≤ γ̄(1 + 2/(aψ_lo)).
Below, o(log n) denotes terms bounded by C(H̄L_n + L_n² + 1 + H̄²/log n) = o(log n) uniformly in T (H̄² ≤ 2A₁log n + O(L_n)).

**(i) Deletions (item 1).** Let T ⊇ S₀, m ≥ 1, and i from L4r.2(a): τ_i² ≤ (H̄ + C_ϱL_n/ℓ'_lo)² = H̄² + o(log n).
By log(1 + u) ≤ u, (s4) and L4r.0(d):
  G_del(i; T) ≥ Δ_k − 3δ_n/2 − ½(1 + 2/log n)(1 + γ'_i(T))(H̄² + o(log n)).
γ'_i(T) = ℓ'_i²/(κ'_S + Σ_{K∖i}ℓ'²) ≤ γ_m := ℓ_hi²/(κ'_S + (m − 1)ℓ'_lo²) ≤ γ̄′. Δ_k ≥ log(p/k) + ½log n (2p − k ≥ p),
½H̄² ≤ log(2p) + L_n (2m_all + 2 ≤ 2p). Hence
  G_del(i; T) ≥ ½log n − log k − γ_m log(2p) − o(log n).
If m ≤ log n: log k ≤ log(log n + s₀) = O(L_n) and γ_m log(2p) ≤ γ̄′A₁log n + O(1). If m > log n: γ_m ≤
ℓ_hi²/((log n − 1)ℓ'_lo²) → 0 and log k ≤ log p ≤ A₁log n. In both cases G_del(i; T) ≥ (½ − A₁max(1, γ̄))log n − o(log n).
The best move's gain is ≥ G_del(i; T) > 0, and by (ii)–(iv) every non-deletion move is strictly smaller; so every
maximiser over the neighbourhood is a null deletion maximising G_del, i.e. (L4r.0, gains) the within-loading-value
argmin of |ξ_j − ℓ_jX_T|. Truth deletions are excluded by (TL).

**(ii) Additions (items 2, 5).** Let l ∉ T (a null, since S₀ ⊆ T), k < K = p. With v := (Q_T − Q_{T∪l})/ψ_T ∈ [0, 1),
−log(1 − v) ≤ v/(1 − v), and v ≤ M_Tτ_l²/ν ≤ Cτ_l²/n:
  G_add(l; T) ≤ −Δ_{k+1} + 3δ_n/2 + ½(1 + 2/log n)(1 + Cτ_l²/n)τ_l(T)²,  |τ_l(T)| ≤ |ξ_l| + ℓ_hi|X_T| ≤ H̄ + ℓ_hi|X_T|.
*m = 0 (T = S₀):* |X_{S₀}| ≤ |ϱ| = O(L_n), Δ_{s₀+1} ≥ log p − log(s₀ + 1) + ½log n (2p − s₀ − 1 ≥ p), so
G_add ≤ −½log n − log p + log(2p) + o(log n) = −½log n + o(log n).
*m ≥ 1:* k + 1 = m + s₀ + 1 ≤ (s₀ + 2)m and 2p − k − 1 ≥ p > m_all, so
log((2p − k − 1)/(k + 1)) ≥ log(2m_all/m) − log(2s₀ + 4) = ½Z_m² − 2L_n − log(2s₀ + 4). With Z := (Z_m² + 2)^{1/2} and
L4r.2(b), |τ_l| ≤ H̄ + R′Z + ℓ_hi|ϱ|, so
  G_add(l; T) ≤ −½log n + ½[(H̄ + R′Z)² − Z²] + o(log n).
The bracket H̄² + 2R′H̄Z + (R′² − 1)Z² is increasing in Z ≥ 0 (R′ ≥ 1) and Z² ≤ H̄² + 2L_n + 2 (Z_m² ≤ Z_1² ≤ H̄² + 2L_n);
so ½[…] ≤ ½((1 + R′)² − 1)H̄² + o(log n) ≤ ((1 + R)² − 1)A₁log n + o(log n). Hence
G_add(l; T) ≤ −(½ − A₁((1 + R)² − 1))log n + o(log n) for every T ⊇ S₀ and l ∉ T.

**(iii) Swaps (item 3).** Null-out swap (j ∈ K_T, l ∉ T): G_sw(j, l; T) = G_del(j; T) + G_add(l; T ∖ j), and
T ∖ j ⊇ S₀, |T ∖ j| < K, so (ii) at T ∖ j gives G_sw ≤ G_del(j; T) − c_add log n ≤ G_del(j°; T) − c_add log n.
Truth-out swaps: (TL).

**(iv) Truth moves (item 4):** (TL). **(v) At S₀ (item 5):** there are no null deletions or null-out swaps; additions
≤ −½log n + o(log n) by (ii); truth moves < 0 by (TL).

**(vi) Paths.** From T₀ ⊇ S₀ the search moves, by (i), to T₀ ∖ j° with j° a null; the new set again contains S₀, so by
induction every move is a null deletion of the stated type, each strictly increases F, there are exactly |T₀ ∖ S₀| of
them, and the search stops at S₀ by (v). No nondegeneracy is needed: every maximiser (and hence the production
tie-break's choice) is a null deletion. The claim is uniform over T₀, hence holds for S* = [p] ∖ N for all N
simultaneously. Caps: FACB L4.5(1) (single-search prefix property). ∎

**Remark (CS).** For λ_j ≡ λ, R = 1 and γ̄ < 1, so L4r-S re-proves FACB L4 on p ≤ n^{A₁}, A₁ < 1/6, without
FACB's gap invariant, B1–B4, end phase or E5–E7 (FACB's regime (S) was p ≤ n^{1/200}). numerics/adversarial_T_out.txt:
at log p/log n = 0.33 there are non-path sets T ⊇ S₀ (CS) with positive addition gains, which suggests (numerically, not proved) that
uniform-over-T arguments are limited to 1/6-type exponents (wording corrected by the lead after R15 item 3).

## L4r.4 Per-class gap invariant (FACB L4.1 analogue; deterministic)

Assume the loading values form a finite set {λ^{(1)}, …, λ^{(r)}} (classes 𝒩_c := {j ∈ 𝒩 : λ_j = λ^{(c)}}). Let
T₀ ⊇ S₀, T_{i+1} = T_i ∖ j_i with j_i a best null deletion at T_i (i < I), c_i the class of j_i. Write μ_c(i) :=
ℓ_cX_{T_i} (class-c centre), K_c(i) := K_{T_i} ∩ 𝒩_c, a_c(i) := max{ξ_j : j ∈ K_c(i), ξ_j < μ_c(i)},
b_c(i) := min{ξ_j : j ∈ K_c(i), ξ_j > μ_c(i)} (∓∞ if empty), L_c := μ_c − a_c, R_c := b_c − μ_c, d_c := min(L_c, R_c).
Assume ξ_j ≠ μ_c(i) for all relevant j, c, i (probability one). Step i is **class-c-crossing** if some point of K_c(i + 1)
lies strictly between μ_c(i + 1) and μ_c(i).

**Lemma L4r.4.** (a) A step with c_i = c is never class-c-crossing. (b) If T₀ ⊇ 𝒩_c (all class-c nulls initially kept) and no step
i < I is class-c-crossing, then 𝒩_c ∖ K_c(I) = 𝒩_c ∩ (a_c(I), b_c(I)). (c) If step i (c_i = c′ ≠ c) is class-c-crossing, then
  d_c(i) < θ_{cc′}(T_i)·(d_c(i)² + C₁/n)^{1/2},  θ_{cc′}(T) := ℓ_cℓ_{c′}(1 + γ'_c(T))^{1/2}/((1 + γ'_{c′}(T))^{1/2}(D'_T − ℓ'_{c′}²)),
  with C₁ := 48nδ_n/ε_lo² = O(1), on E_n, n ≥ n₀ (γ'_c(T) := ℓ'_c²/(D'_T − ℓ'_c²)). In particular, if θ_{cc′}(T_i) ≤ θ < 1 then
  d_c(i) ≤ θ(C₁/(n(1 − θ²)))^{1/2}; in the bulk D'_T ≥ mℓ'_lo², so θ_{cc′} ≤ C/m and a crossing forces d_c(i) ≤ C/(m√n).

*Proof.* (a) Within class c the best deletion is the class argmin (L4r.0 gains), i.e. a_c or b_c; say b_c (R_c ≤ L_c).
By L4r.0(b) μ_c moves by −ℓ_cℓ'_cτ_j/(D' − ℓ'_c²) with τ_j = ε_cR_c, i.e. by −ℓ'_c²R_c/(D' − ℓ'_c²) (ℓ_cε_c = ℓ'_c).
If a_c is finite, D' − ℓ'_c² ≥ κ'_S + ℓ'_c² > ℓ'_c² (a_c is another kept class-c point), so the move is < R_c ≤ L_c and
μ_c(i + 1) ∈ (a_c, μ_c(i)): no kept class-c point is crossed. If a_c = −∞ there is nothing to cross. Symmetric for a_c.
(b) Induction as FACB L4.1(i): own-class steps delete the edge point and extend the hole to the next kept point
(using (a)); foreign steps move μ_c without crossing (assumption), leaving K_c, a_c, b_c unchanged.
(c) Say j_i is above μ_{c′} (else symmetric); then X decreases and μ_c moves down by s := ℓ_cℓ'_{c′}τ_{j_i}/(D' − ℓ'_{c′}²),
τ_{j_i} = ε_{c′}d_{c′}; a crossing needs s > L_c ≥ d_c. Best-deletion comparison with the class-c argmin j_c:
G_del(j_i) ≥ G_del(j_c) gives ν log((1 + u_i)/(1 + u_c)) ≤ ½(e_{c′} − e_c) ≤ 3δ_n with u := M_T(1 + γ')τ²/ν, so
u_i − u_c ≤ (1 + u_c)(e^{3δ_n/ν} − 1) ≤ 12δ_n/ν (u_c = O(log n/n)). On E_n, M_T ≥ ¼ (ψ_T ≤ (‖e‖² + 1.1s²)/s² by (s5),
‖e‖² ≤ σ²(n + n^{2/3}) by E2), so (1 + γ'_{c′})ε_{c′}²d_{c′}² ≤ (1 + γ'_c)ε_c²d_c² + 48δ_n. Hence
s ≤ ℓ_cℓ'_{c′}d_{c′}/(D' − ℓ'_{c′}²) ≤ θ_{cc′}(T_i)(d_c² + 48δ_n/ε_lo²)^{1/2} (ℓ' ≤ ℓ, ε ≤ 1), and s > d_c gives (c). ∎

**Remarks.** (1) For r = 1 the offsets e_j(T) do not depend on j and (c) is void: FACB L4.1(i) is recovered exactly.
(2) For r ≥ 2 the offsets e_{c′} − e_c = O(1/n) are deterministic and nonzero, so an exact gap invariant needs a
probabilistic exclusion of O(n^{−1/2}/m) near-coincidences along the (data-dependent) path; this seat did not prove it
(an X3-type soft-gap band of width O(n^{−1/2}) is the natural route). (3) In the end phase D'_T = O(1) and θ_{cc′} can
exceed 1 (e.g. ℓ_c = 1, ℓ_{c′} = 3, κ'_S = 1, one kept point of each class: θ ≈ 1.8): no comparison argument can then
exclude crossings. Numerically no crossing occurred in 366 paths (numerics/N_T2_summary.md (ii)).

## L4r.5 Static per-class centre bound (per-class B3)

Assume finitely many classes with |𝒩_c| ≥ c_*p, the per-class versions E5_c of FACB L3 E5 (sign-symmetric top sums
D^c_j, counts P^c_j, and m^c_± ≥ |𝒩_c|/3 for each class sample; probability → 1 by FACB L3.1's E5 proof per class,
union over r classes), and let T ⊇ S₀ be a set such that **for every class c both a_c, b_c are finite** (two-sided)
and K_c = 𝒩_c ∖ (a_c, b_c), with m_c := |K_c|. Put Δ_c := |R_c − L_c| (per-class asymmetry, in ξ units), x_u := 2log(u + 1) + L_n.

**Lemma L4r.5.** If X_T > max_c Δ_c/(2ℓ_c) then
  X_T ≤ [Σ_c ℓ'_cH̄(10m_cx_{5m_c})^{1/2}·1{m_c ≥ 1} + C_ϱL_n] / (κ'_S + Σ_cℓ'_c²m_c),
and symmetrically for X_T < −max_c Δ_c/(2ℓ_c). In particular, if every m_c ≥ m₁ := ⌈K₁L_n⌉ then
X_T ≤ 0.34ε_bH̄/ℓ_lo + o(1) (FACB constants).

*Proof.* For each class c, ℓ_cX_T > Δ_c/2 gives a_c + b_c = 2μ_c + (R_c − L_c) > 0. Case a_c < 0 < b_c: b_c > |a_c|, so
K_c ⊆ Top_c(J_c) := {j ∈ 𝒩_c : |ξ_j| ≥ |a_c|} with Top_c ∖ K_c consisting of positives; Σ_{K_c}ξ ≤ D^c_{J_c}, and FACB
L4.3 (B3) Case A verbatim (negatives in Top_c(J_c) are exactly the kept negatives) gives J_c ≤ 5m_c and
Σ_{K_c}ξ ≤ H̄(10m_cx_{5m_c})^{1/2}. Case a_c ≥ 0: every negative of class c is kept (m_c ≥ |𝒩_c|/3), the hole lies in
(0, ∞), so Σ_{K_c}ξ = Σ_{𝒩_c}ξ − Σ_{hole}ξ ≤ |D^c_{|𝒩_c|}| ≤ H̄(2|𝒩_c|x_{|𝒩_c|})^{1/2} ≤ H̄(6m_cx_{3m_c})^{1/2}
≤ H̄(10m_cx_{5m_c})^{1/2}. Case b_c ≤ 0 is impossible (μ_c > 0). Then X_TD'_T = Σ_cℓ'_cε_cΣ_{K_c}ξ − ϱ ≤
Σ_cℓ'_c max(0, Σ_{K_c}ξ) + |ϱ|; divide by D'_T. The last claim:
(10m_cx_{5m_c})^{1/2}/(ℓ'_cm_c) ≤ (11/K₁)^{1/2}/ℓ'_c (FACB L4.3) and Σ_cℓ'_c·ℓ'_cm_c·(…)/Σ_cℓ'_c²m_c ≤ max_c(…). ∎

**What it does not give.** The hypothesis "every class two-sided" and a bound Δ_c ≤ 2ℓ_cεH̄ must come from the path
dynamics (FACB B1, B2). Numerically both fail along actual paths (one-sided classes during the bulk; max Δ_c/(2ℓ_c) up to
0.70H̄ while |X_T| ≤ 0.074H̄; numerics/N_T2_summary.md (iii)); see §L4r.6.

## L4r.6 Why FACB L4.3–L4.4 do not transfer (exact failing steps)

1. **Bulk (B2) per class.** FACB L4.1(iv): Δ_{i+1} ≤ max(Δ_i, g_i + 2d_i/(k_i − 1 + κ)) — every step is a deletion of the
   single class, so the hole only re-centres. With r ≥ 2 classes a deletion in class c′ moves μ_c by
   ℓ_cℓ'_{c′}τ/(D' − ℓ'_{c′}²) **without changing class c's hole**, so Δ_c grows by up to 2ℓ_cℓ_{c′}d/D' per foreign step.
   Summed, Δ_c ≲ 2ℓ_c·TV(X) + O(g_max) (backlash of the class hole behind its centre), and then L4r.5 only gives
   |X| ≤ max_c Δ_c/(2ℓ_c) ≤ TV(X): the induction does not close (factor-2 loss and no smallness). This is the **first
   failing step** of the FACB route. The low-loading classes are the bottleneck (Δ_c/(2ℓ_c) with ℓ_c small).
2. **Bulk (B1) per class.** FACB's B1 contradiction uses that a one-sided configuration forces x ≈ H. With several
   classes, class c one-sided only forces ℓ'_c·(m_c H̄) of excess in X·D', negligible if m_c ≪ m. Numerically classes do
   become one-sided in the bulk (up to 30 steps with m ≥ 30, design 20%/80% shares).
3. **End phase (E-side).** In the limit where kept nulls sit at ±H̄, the deletion statistic of a kept null of class c,
   sign s, is h·(sD' − ℓ'_cW)²/(D'(D' − ℓ'_c²)) + o(log n), W := X_TD'_T/H̄; at near balance (W ≈ 0) this is
   h·D'/(D' − ℓ'_c²): the **smallest-loading class is deleted first, on either side**, so FACB's majority-side rule and
   its monotone imbalance |I_{i+1}| ≤ |I_i| fail (numerics: minority-side deletions up to 13/160 end-phase steps in
   two-class designs, 0 in CS). No invariant of the form max_c ℓ_c|X_T| ≤ θH̄ holds (observed up to 1.75H̄); additions
   nevertheless lose on all paths because the addition statistic carries D'/(D' + ℓ'_c²) (L4r.0(c)). A correct end-phase
   invariant would have to bound h·(D'/(D' + ℓ'_c²))(1 + ℓ_c|X_T|/H̄)² directly, through the finite dynamics of the
   signed loading counts; this seat did not prove one.
