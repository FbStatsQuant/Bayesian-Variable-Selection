# L1a′ — design-free size tail for the coded prior (W3-POST)

Status: **PROVED (by this seat, unchecked)**. Check record [C1B-N4]: R01 (gpt-6-astra high,
`../reviews/R01_recheck_astra.md`) VERIFIED-WITH-AMENDMENTS (remarks 2, 5; applied); R02 (Opus 5.5 high,
`../reviews/R02_recheck_opus.md`) VERIFIED; council C1 seats A and B re-derived the proof line by line (no defect). Changed step relative to
[P1] `lem:den` written in full; everything else cited by label. Notation of `../STATEMENT.md` §0 and of [P1] §1
(contrast coordinates y_c = Uᵀy^r, X_c = UᵀX, ε_c = Uᵀε ~ N_{n−1}(0, σ*²I), Q^c_S, m^c_b(S), b± , κ, 𝓑_n, c_IG).

## Statement
Fix n ≥ 3 and a standardised design X (any p ≥ 2). Assume G and that there are T ∈ Ω and θ ∈ ℝ^T with
**X_Tθ = μ**, **‖μ‖² ≤ nM** and **‖θ‖² ≤ nM′**. Put t := |T|, R^T_m := Σ_{k=max(m+1,0)}^K q_k / w(t) [C2A-F4],
m^T_n(ω) := min{m ≥ t : R^T_m ≤ n^{−(t+1)/2}e^{−ω}}. Define Θ^T_{n,m} ≥ 0 by
π(|S| > m) = R^T_m (n+1)^{t/2}√n Θ^T_{n,m} (Θ^T := 0 if R^T_m = 0). Then for every L > c♯² (c♯ := κ²/(c_IG σ*²) of
[T03R] line 77, depending on (σ*², M) only):

  sup_m P(Θ^T_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C′_Λ / log(√L/c♯),  C′_Λ := 1/√2 + 1/2 + (M + M′)/(2σ*²),

and π(|S| > m^T_n(ω)) ≤ (1 + 1/n)^{t/2}e^{−ω}Θ^T_{n,m^T_n(ω)}. The right side of the display depends on X only through
(M, M′): the bound is uniform over all designs and all T satisfying the hypothesis with these constants.

## Proof
The proof of T02(i♯) ([T03R] lines 93-97) uses three ingredients: (1) [P1] `lem:num` for the numerator (no condition
on X; any data-free rate b₋); (2) [P1] `thm:Ta` on 𝓑_n and `thm:T01iii` for P(𝓑_nᶜ) (uses only ‖μ‖² ≤ nM);
(3) Lemma den′ ([T03R] lines 89-91), the only place where λ_min(R_{S₀}) ≥ φ₀² enters, through the bound on Q^c_{S₀}.
Replace S₀ by T in (3) and (in the prior ratio) w(s₀) by w(t). We re-prove (3) without an eigenvalue condition.

*Changed step (bound on Q^c_T).* By [P1] `lem:slab`, Q^c_T = min_ϑ {‖y_c − X_{c,T}ϑ‖² + ϑᵀ(G_T + I)ϑ/n}, where
G_T = X_{c,T}ᵀX_{c,T} = X_TᵀCX_T = X_TᵀX_T (columns centred). Since y_c = X_cθ* + ε_c = Uᵀμ + ε_c and
X_{c,T}θ = UᵀX_Tθ = Uᵀμ, the choice ϑ = θ gives
  Q^c_T ≤ ‖ε_c‖² + θᵀ(G_T + I)θ/n = σ*²E′ + ρ,  ρ := (‖X_Tθ‖² + ‖θ‖²)/n = (‖μ‖² + ‖θ‖²)/n ≤ M + M′,
deterministically (E′ := ‖ε_c‖²/σ*² ~ χ²_{n−1}). This replaces "Q^c_{S₀} ≤ σ*²E′ + R_n" in [P1] `lem:den`.
(If t = 0 then μ = 0, Q^c_∅ = ‖ε_c‖² and ρ = 0.)

*Rest of den′, verbatim with R_n → ρ.* The integral representation and the exponent bound of [P1] `lem:den`
(lines 339-353) use only Q^c ≤ σ*²E′ + (a nonnegative quantity), so with Λ′_n := |E′ − (n−1)|/(2√n) + E′/(2n) +
ρ/(2σ*²), m^c_{b+}(T)/f₀(y_c) ≥ D_T^{−1/2} c_IG σ*² n^{−1/2} e^{−Λ′_n} and D_T ≤ (n+1)^t ([P1] `lem:spec`(e), no
condition). E Λ′_n ≤ √(2n)/(2√n) + (n−1)/(2n) + (M + M′)/(2σ*²) ≤ C′_Λ ([P1] `lem:chi`(b) as in `lem:den`).

*Assembly.* As in [T03R] lines 93-97 with S₀ → T: on 𝓑_n, [P1] `thm:Ta` (its last inequality needs only T ∈ Ω, since
Z^c_{b+} ≥ ϖ(T)m^c_{b+}(T)) gives π(E_m) ≤ κ² v_m Θ^{(1)}_{n,m} / (ϖ(T) m^c_{b+}(T)/f₀) with v_m = ϖ(E_m) =
R^T_m ϖ(T) and E Θ^{(1)} = 1, hence Θ^T_{n,m} ≤ c♯e^{Λ′_n}Θ^{(1)}_{n,m}; Markov on Θ^{(1)} and on Λ′_n ≥ 0 and
P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n−1) give the display. At m = m^T_n(ω): R^T_m ≤ n^{−(t+1)/2}e^{−ω}. ∎

## Remarks
1. **What was removed.** T02(i♯) needs λ_min(R_{S₀}) ≥ φ₀² only to bound the ridge bias of the reference model. The
   variational form of Q makes the bias at most (‖μ‖² + ‖θ‖²)/n for *any* exact representation μ = X_Tθ. With the
   raw-scale convention (fixed |β_j| ≤ b_hi, raw sds ≤ 2 on the event ℋ_n of [POST]) ‖θ*‖² ≤ 4s₀b_hi² = O(1), so the
   hypothesis is free. If λ_min(R_{S₀}) ≥ φ₀², then ‖θ*‖² ≤ ‖μ‖²/((n−1)φ₀²) ≤ 1.5M/φ₀² (n ≥ 3), so L1a′ contains
   Lemma 1a (with a different but still fixed constant).
2. **Is a coefficient bound needed? (open) [R01-2].** For a near-collinear pair (corr(x₁, x₂) = 1 − η, difference
   eigenvalue g = (n − 1)η) and μ = L(x₁ − x₂), the signal part of Q_{S₀} is exactly 2L²g(g + 1)/((n + 1)g + 1) ≤ ‖μ‖²,
   whereas the variational bound used above is (‖μ‖² + ‖θ‖²)/n ≈ 2L²/n. So outside the hypothesis the *proof's
   reference bound* degrades; this does not show the *conclusion* fails. Numerics L1a′(e) (θ = (n, −n), 1 − corr ≍ n⁻²;
   `../numerics/post_exact_out.txt`) find max over seeds of max_{t≤m<K} Θ ≤ 1.5·10⁻⁵ (scanned range t ≤ m < K) [C3A-N1], i.e. no failure. Whether some coefficient/approximation
   control is necessary is open; R03 §6A proposes the weaker "bounded penalised approximation" reference.
3. **Random designs.** Because the bound is uniform over X, it holds under any joint law of (X, ε) with ε ⫫ X,
   integrated over X, on the event where the hypothesis holds; no diagonal argument is needed.
4. **Growing s₀.** Nothing in the proof requires s₀ fixed; s₀ enters only through the cutoff — but (E) is then a
   real condition (R02-F1: s₀ identical truth columns give ‖μ‖² ≍ ns₀²). For t ≥ 1 and p ≤ n^A,
   m^T_n(½ log n) ≤ t + ⌈(t log p + ((t+2)/2) log n)/log 2⌉ ([T03R] E2(ii), which needs t ≥ 1, ω ≥ 0) [R02-F5].
5. **Order of the cutoff (worst case) [R01-3].** For fixed t ≥ 1, ω = ½ log n and p ≍ n^A (A > 0), the cutoff satisfies
   m^T_n − t ≈ [(A + ½)t + 1] log n / log 2 ([T03R] E2(ii) upper, E3 lower: this proof route cannot do better). In the
   worst case some growth is necessary: [T03R] Proposition D (lines 103-121; p duplicates of one truth) gives
   π(|S| > m) ≥ 2^{−(m+4)}e^{−m(m−1)/(4(p−m))} w.p. → 1, so a cutoff valid uniformly over designs must be
   ≥ ½ log₂ n − O(1). For a given design the tail may vanish much earlier (and m^T_n = t if t = K; with fixed p the
   cutoff is bounded). The gap between the constants [(A + ½)t + 1]/log 2 and ½/log 2 is open.
