# D — Corollary H: in-sample predictive / Hellinger contraction of the coded posterior (W3-POST2, Claim D; PROGRAM 1b)

Status: **PROVED (by this seat, unchecked)**. **Check record [C1B-2]:** v1 line check K-D (VERIFIED-WITH-AMENDMENTS, `../reviews/K_D_disposition.md`); v2 line check K2: VERIFIED-WITH-AMENDMENTS (applied, `K2_disposition.md`); M01: D(a) sound, D(b) repairable → repaired (`M01_disposition.md`); S01: remark fixes; council C1 (PASS). v2 (STATEMENT v1.2): D(b) without (F_λ), variance at the parametric rate
(R03b §D); D1 floor-free. Notation: `../STATEMENT.md`; [P1] `thm:T01i`,
`prop:closed`, `lem:spec`; [P3]; `A_occam.md`; `E_visibility.md` (event 𝒢⁵_n).

## D0. The parameter posterior and the distance
By [P1] `thm:T01i`, the working-model posterior of (S, β_S, σ²), mapped by (θ, v) = (s_yβ, s_y²σ²) to the original
response scale, is Π_b (b = b₀s_y²), with v | S, y ~ IG(ν, β_S), β_S := b + Q^c_S/2, and
θ_S | v, S, y ~ N(θ̂_S, nvH_S⁻¹), θ̂_S := nH_S⁻¹X_{c,S}ᵀy_c, so X_{c,S}θ̂_S = M_Sy_c. The fitted centred mean is μ̂ := X_Sθ;
since X_S = UX_{c,S} and μ = Uμ_c with U an isometry, ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖.
For one-dimensional normals, H²(N(a, v), N(b, w)) = 1 − A·B with A = (2√(vw)/(v + w))^{1/2}, B = e^{−(a−b)²/(4(v+w))}.

**Lemma D0.** h̄_n² := n⁻¹Σ_iH²(N(μ̂_i, v), N(μ_i, σ*²)) ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²).
*Proof.* 1 − AB ≤ (1 − A) + (1 − B) (difference = −(1 − A)(1 − B) ≤ 0 for A, B ∈ [0, 1]). 1 − B ≤ (a − b)²/(4(v + w)) ≤
(a − b)²/(4w). 1 − A ≤ 1 − A² = (√v − √w)²/(v + w) ≤ (√(v/w) − 1)² ≤ (v/w − 1)², using |√x − 1| = |x − 1|/(√x + 1) ≤ |x − 1|.
Take w = σ*², average over i. ∎

## D1. Conditional bounds for any model (no floor)
For S ⊆ [p] let L_S := μ_cᵀ(I − M_S)μ_c (ridge loss; L_S = min_ϑ B_S(ϑ) by [P1] `lem:slab` with Y = μ_c; L_S ≥ Δ_S).
**Lemma D1.** For every S ∈ Ω and the conditional posterior given (S, y):
(a) E[‖X_{c,S}(θ − θ̂_S)‖² | v, S, y] = v·tr(M_S) ≤ v|S|;
(b) ‖M_Sy_c − μ_c‖² ≤ 2‖P_Se‖² + 2L_S;
(c) E[v | S, y] = β_S/(ν − 1), Var(v | S, y) = β_S²/((ν − 1)²(ν − 2)) (ν > 2);
(d) Q^c_S = ‖e‖² − eᵀM_Se + 2eᵀ(I − M_S)μ_c + L_S, hence |Q^c_S − ‖e‖²| ≤ ‖P_Se‖² + 2|eᵀ(I − M_S)μ_c| + L_S.
*Proof.* (a) Cov(θ | v) = nvH_S⁻¹, and E‖X_c(θ − θ̂)‖² = tr(X_{c,S}nvH_S⁻¹X_{c,S}ᵀ) = v tr(M_S); 0 ⪯ M_S ⪯ P_S ([P3]
`lem:smoother`(b)) so tr(M_S) ≤ rank ≤ |S|. (b) M_Sy_c − μ_c = M_Se − (I − M_S)μ_c; ‖M_Se‖ ≤ ‖P_Se‖ (0 ⪯ M_S ⪯ P_S, and
M_S² ⪯ M_S); ‖(I − M_S)μ_c‖² ≤ μ_cᵀ(I − M_S)μ_c = L_S since 0 ⪯ I − M_S ⪯ I. (c) IG(ν, β) moments.
(d) Q^c_S = y_cᵀ(I − M_S)y_c ([P1] `lem:spec`(a)) with y_c = μ_c + e; 0 ≤ eᵀM_Se ≤ ‖P_Se‖². No eigenvalue condition. ∎
(v1 of D1 used a floor on S; v2, STATEMENT v1.2, follows R03b §D.)

## D2. Proof of D(a) (with selection; oracle rate)
Assume R1, G, (E), (F₀), δ_n → 0 in probability, M_n → ∞. Let Bad := {‖μ̂ − μ‖² > M_n} ∪ {|v/σ*² − 1| > M_nn^{−1/2}} ∪
{S ≠ S₀} ∪ {‖θ − θ*‖ > M_nn^{−1/2}} (θ zero-padded to ℝ^p). Then Π(Bad | y) ≤ δ_n + Π(Bad′ | S₀, y), Bad′ the first, second and fourth events.
*Mean.* By D1(b) with S = S₀: ‖M_{S₀}y_c − μ_c‖² ≤ 2‖P_{S₀}e‖² + 2L_{S₀} = O_P(1) (σ*⁻²‖P_{S₀}e‖² ~ χ²_{s₀}; L_{S₀} ≤ B_{S₀}(θ*) =
(‖μ‖² + ‖θ*‖²)/n ≤ ρ̄ := M + M/(2φ₀²) by (E), (F₀) and [L1a′] Remark 1).
‖μ̂ − μ‖² ≤ 2‖X_c(θ − θ̂)‖² + 2‖M_{S₀}y_c − μ_c‖², and by D1(a) and Markov,
Π(2‖X_c(θ − θ̂)‖² > M_n/2 | S₀, y) ≤ 4s₀E[v | S₀, y]/M_n.
*Variance.* By D1(d), |Q^c_{S₀} − ‖e‖²| ≤ ‖P_{S₀}e‖² + 2|eᵀ(I − M_{S₀})μ_c| + L_{S₀} = O_P(1) (the cross term is
N(0, ≤ σ*²L_{S₀})), and ‖e‖² = Nσ*² + O_P(√n), so Q^c_{S₀} = Nσ*² + O_P(√n). With b = b₀s_y² = O_P(1)
([P1] `thm:T01iii`) and ν − 1 = n/2 − 0.99: E[v | S₀, y] = σ*² + O_P(n^{−1/2}) and Var(v | S₀, y) ≤ 4(E v)²/n = O_P(1/n).
By Chebyshev, Π(|v/σ*² − 1| > M_nn^{−1/2} | S₀, y) → 0 in probability, and E[v | S₀, y] = O_P(1) makes the mean term → 0.
*Coefficients.* On S = S₀, μ_c = X_{c,S₀}θ*, so ‖μ̂ − μ‖² = ‖X_{c,S₀}(θ − θ*)‖² ≥ Nφ₀²‖θ − θ*‖² by (F₀); hence
{‖θ − θ*‖ > M_nn^{−1/2}} ⊆ {‖μ̂ − μ‖² > Nφ₀²M_n²/n} and Nφ₀²M_n²/n ≥ φ₀²M_n²/2 → ∞; apply the mean bound with M_n replaced
by min(M_n, φ₀²M_n²/2).
*Hellinger.* By Lemma D0, {h̄_n > M_nn^{−1/2}} ⊆ {(v/σ*² − 1)² > M_n²/(2n)} ∪ {‖μ̂ − μ‖² > 2σ*²M_n²}; both events are of the
above form (with M_n/√2 and 2σ*²M_n² → ∞). ∎

## D3. Proof of D(b) (no beta-min, no floor away from S₀; rate log n / n, variance at the parametric rate)
Assume R1, G, (E), (F₀), (OS). Fix c₂ := c₁ + 1 (c₁ of Claim E) and let 𝔉 := {S ∈ Ω : S₀ ⊄ S, |S∖S₀| ≤ j₀} and
  𝒮_n := {S₀} ∪ 𝒰_near,  𝒰_near := {S ∈ 𝔉 : L_S < c₂σ*² log n}.
**Mass outside 𝒮_n.** Ω∖𝒮_n ⊆ {|S| > m♯_n} ∪ {S ⊋ S₀, |S| ≤ m♯_n} ∪ 𝒰_far, 𝒰_far := {S ∈ Ω underfitting, |S| ≤ m♯_n,
S ∉ 𝒰_near} (an underfit S ∈ 𝔉 has |S| ≤ s₀ + j₀ − 1 ≤ min(s₀ + j₀, K) ≤ m♯_n for n ≥ n₀, by Lemma E0 of
`E_visibility.md` with B = s₀ + j₀) [C1B-5]. The first two sets have mass
O_P(n^{−1/2}) (T02(i♯)) and O_P(r_n) (Claim A1 5(a); uses (E), (F₀), (OS)). For 𝒰_far, run the assembly of
`E_visibility.md` E2 with 𝒰 := 𝒰_far: an S ∈ 𝒰_far with |S∖S₀| ≤ j₀ is in 𝔉 with L_S ≥ c₂σ*² log n, so Lemma E1(b)
(c₂ > c₁; uses (E), (F₀) only) gives ℓ(S)/ℓ(S′) ≤ n^{−2} on 𝒢^sup_n ∩ 𝒢⁵_n; those with |S∖S₀| > j₀ use [T03R] (C6)(a)
and Υ′^{>j₀}_n; hence π(𝒰_far) = O_P(n^{−2} + r_n) by `A_occam.md` (C5′)(c) [K-D-2]. So π(Ω∖𝒮_n) = O_P(r_n).
**Conditional bounds on 𝒮_n.** Each S ∈ 𝒮_n has |S| ≤ s₀ + j₀ and L_S ≤ max(c₂σ*² log n, L_{S₀}) ≤ c₂σ*² log n for
n ≥ n₀ (L_{S₀} ≤ ρ̄). Work on 𝒢^sup_n ∩ 𝒢⁵_n (P ≥ 1 − 5/n; 𝒢⁵_n of Lemma E1 covers 𝔉 ⊇ 𝒰_near; for S₀: a₀ := (I − M_{S₀})μ_c ∈ col X_{c,S₀}, ‖a₀‖² ≤ L_{S₀} ≤ ρ̄, so on (G2*) |eᵀa₀| = |(P_{S₀}e)ᵀa₀| ≤ σ*√(C_As₀ρ̄ log n)
≤ σ*²√(2C_xc₂) log n for n ≥ n₀ [M01-1]). All bounds below hold deterministically and simultaneously for all S ∈ 𝒮_n on
this event [L01-5]:
- *Mean:* by D1(b) and (G2*), ‖M_Sy_c − μ_c‖² ≤ 2σ*²C_A(s₀ + j₀) log n + 2c₂σ*² log n =: m_n^{fit}.
- *Variance:* by D1(d), (G2*) and 𝒢⁵_n, |Q^c_S − ‖e‖²| ≤ σ*²[C_A(s₀ + j₀) + 2√(2C_xc₂) + c₂] log n =: σ*²C_Q log n
  (S₀ included, by the bound just given). With 0 < b ≤ 6b₀(M + σ*²) and ν − 1 = n/2 − 0.99:
  E[v | S, y] − σ*² = [‖e‖² − Nσ*² + (Q^c_S − ‖e‖²) + 2b + 0.98σ*²]/(n − 1.98), so
  sup_{S∈𝒮_n}|E[v | S, y] − σ*²| ≤ |‖e‖² − Nσ*²|/(n − 1.98) + 2σ*²C_Q log n/n. On the event, (G1) bounds the first term by
  3σ*²√(N log n)/(n − 1.98), so deterministically sup_S|E[v | S, y]/σ*² − 1| = O(√(log n/n)) ≤ 1/4 for n ≥ n₀, and the exact IG
  formula gives sup_S Var(v | S, y) = (E v)²/(n/2 − 1.99) ≤ (5σ*²/4)²·(2.1/n) ≤ 4σ*⁴/n [M01-1]. Separately, the actual χ²
  fluctuation ‖e‖² − Nσ*² = O_P(√n) is common to all S, so sup_S|E[v | S, y] − σ*²| = O_P(n^{−1/2}).
Let C_H := 4(m_n^{fit}/log n) + 1 = 8σ*²(C_A(s₀ + j₀) + c₂) + 1 and M_n → ∞. Uniformly over S ∈ 𝒮_n:
Π(|v/σ*² − 1| > M_nn^{−1/2} | S, y) ≤ 1{sup_S|E v − σ*²| > σ*²M_n/(2√n)} + 16/M_n² (Chebyshev), and, since
2m_n^{fit} ≤ C_H log n/2, Π(‖μ̂ − μ‖² > C_H log n | S, y) ≤ Π(‖X_c(θ − θ̂)‖² > C_H log n/4 | S, y) ≤ 8σ*²(s₀ + j₀)/(C_H log n)
(D1(a), Markov, E v ≤ 2σ*²).
**Conclusion.** With Bad_b := {‖μ̂ − μ‖² > C_H log n} ∪ {|v/σ*² − 1| > M_nn^{−1/2}}:
Π(Bad_b | y) ≤ π(Ω∖𝒮_n) + sup_{S∈𝒮_n}Π(Bad_b | S, y) → 0 in probability, using P((𝒢^sup_n ∩ 𝒢⁵_n)ᶜ) ≤ 5/n. By Lemma D0,
off Bad_b: h̄_n² ≤ M_n²/n + C_H log n/(4nσ*²); taking M_n := √(log n) gives Π(h̄_n² > C′_H log n/n | y) → 0 in probability
with C′_H := 1 + C_H/(4σ*²). ∎
Neither (F_λ), (ID), (G4) nor beta-min is used; the only eigenvalue condition is (F₀) (through L_{S₀}, R_n in Lemma E1 and
η_n in (C4′)).

## D4. Remarks
0. **Intercept [C1B-4].** h̄_n is the *centred* in-sample Hellinger distance. With the plug-in intercept the coded
   predictive law for y^r_i is N(ȳ^r + μ̂_i, v) and the truth N(α* + (X^rβ*)_i, σ*²); the mean error is ε̄1 + (μ̂ − μ) with
   ε̄ the noise mean, and the two pieces are orthogonal (μ̂ − μ ∈ 1^⊥). By Lemma D0's argument the intercept-inclusive
   distance satisfies h̄²_{int} ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²) + ε̄²/(4σ*²), with nε̄²/σ*² ~ χ²₁, so D(a) and D(b)
   hold verbatim for h̄_{int} (the extra term is O_P(1/n)).
1. **Song–Liang comparison.** SL (2015) Thms 1–2 (printed pp. 952–953): random design, Hellinger distance of the joint
   density of (x, y) integrated over the design law, exponential bounds P*[π{d > ε_n} > e^{−c₁nε_n²}] < e^{−c₁nε_n²};
   Cor 1 (printed p. 954): under its hypotheses (strict sparsity, P_n < exp(Cn^α), eigenvalue envelopes) and its
   logarithmic model-size branch, ε_n = O(n^{−(1−α)/2}log^{k/2} n) (SL's α; their ξ is a model index) [C1B-9] (a polynomial branch gives another rate); SL's distance
   is d² = ∫(√f − √f*)² = 2H² in our normalisation [K-D-3]. Here: fixed design, in-sample average over the n design points, convergence in
   probability; rate ε_n² = log n/n with no beta-min and no floor away from S₀ (D(b)), ε_n = M_n/√n with selection (D(a)). Random designs enter
   through [W3P] item 6; an integrated (out-of-sample) version would need a design law and is not claimed.
2. **Scale (no lower bound proved) [S01-8].** D(a): given S₀ the posterior law of ‖μ̂ − μ‖² has a non-degenerate
   χ²_{s₀}-type spread (posterior covariance trace v·tr(M_{S₀}) ≍ s₀σ*²), so the 1/n scale cannot be improved for the mean
   part. D(b): numerics are consistent with the log n/n scale (`../numerics/post2_checks_out.txt` N7, two weak truths with
   θ² = 0.5 log n/n: posterior E‖μ̂ − μ‖²/log n ≈ 1.0 for n = 400 … 6400, where the posterior drops the weak truths); this
   is a posterior expectation of an upper bound, not a proved lower bound. With beta-min (N7, D(a) design): n·E[h̄² bound]
   ≈ 4–5, flat in n.
3. Posterior expectations of unbounded losses are not claimed (small wrong-model mass does not control them).
