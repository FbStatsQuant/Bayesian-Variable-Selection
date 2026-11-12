# C — Proposition C: ridge-cost control of the reference cannot be dropped (W3-PSHARP, Claim C)

Status: **PROVED (by this seat, unchecked)**. Check record: see `../REPORT.md` §2.
Notation: `../STATEMENT.md` §0, §4. Uses Lemma V and Lemma S(1) (`S_one_step.md`) and Chebyshev's inequality. The
lemmas [L1a′] and [1a″] are **not** used: only their statements are quoted, to say what fails.

## 0. The design 𝔇_n and the constants
n ≥ n₀ := 200; k := ⌈12 log n⌉, p := k + 2, η := n⁻²; x₁, x₃, …, x_{k+2} mutually orthogonal, centred, ‖·‖² = n − 1;
u := Σ_{j∈T′} x_j, T′ := {3, …, k+2}; x₂ := c(x₁ − ηu), c := (1 + η²k)^{−1/2}; T := {1, 2}. Truth: G with X^r = X,
β* = θ* = (b/√k)1_{T′}, i.e. μ = (b/√k)u, where b = b_n ∈ (0, b̄] and n b² ≥ C_b V₀ (log n)², V₀ := σ*² + b̄², C_b := 1200.

Elementary facts (n ≥ 200, L := log n ≥ 5.298):
- (F1) k ≤ 12L + 1, p ≤ 12L + 3 ≤ n/2 (at n = 200: p = 66 ≤ 100; 12L + 3 − n/2 is decreasing in n). So
  K = min(p, ⌊n/2⌋) = p, every subset of [p] is in Ω, and k + 1 ≤ n − 1: the k + 1 orthogonal centred vectors exist
  in 1^⊥ (dimension n − 1).
- (F2) x₂ is centred and ‖x₂‖² = c²(‖x₁‖² + η²‖u‖²) = c²(n−1)(1 + η²k) = n − 1: X is a standardised design.
- (F3) rank X = k + 1 (x₂ ∈ span(x₁, T′)); 𝒳 := col X ⊂ 1^⊥ has dimension k + 1.
- (F4) x₂ᵀx₁ = c(n−1); x₂ᵀx_j = −cη(n−1) for j ∈ T′; c ≤ 1; k ≤ n².

## 1. Item 1 (the hypotheses)
‖μ‖² = (b²/k)‖u‖² = b²(n−1) ≤ n b̄²: (E) with M = b̄². T ∈ Ω, t = 2. With θ := (b/(η√k))(1, −1/c):
X_Tθ = (b/(η√k))(x₁ − x₂/c) = (b/(η√k))·ηu = μ, exactly. ‖θ‖² = (b²/(η²k))(1 + c⁻²) = (b²n⁴/k)(2 + η²k) ≥ b²n⁴/k, and
‖θ‖²/n ≥ n³b²/k ≥ n² C_bV₀L²/(12L + 1) → ∞. So every hypothesis of [L1a′] (lines 10-11: G; T ∈ Ω and θ ∈ ℝ^T with
X_Tθ = μ; ‖μ‖² ≤ nM) holds for the reference T with a fixed M, **except** ‖θ‖² ≤ nM′ with a fixed M′.
(θ is the only representation of μ on T: x₁, x₂ are linearly independent.)

**Lemma P (projection bound).** Let S ⊆ [p], d := |T′∖S| ≥ 1, and ϑ ∈ ℝ^S (put ϑ₂ := 0 if 2 ∉ S). Then
  ‖μ − X_Sϑ‖² + ϑ₂²/n ≥ (n−1) d (b²/k)/(1 + n(n−1)d c²η²) ≥ (n−1) d b²/(2k).
*Proof.* Let Π be the orthogonal projection onto span{x_j : j ∈ T′∖S}, an orthogonal family of d vectors of squared
norm n − 1. By (F4) and orthogonality: Πx₁ = 0; Πx_i = 0 for i ∈ S ∩ T′; Πx₂ = −cη Σ_{j∈T′∖S} x_j;
Πμ = (b/√k)Σ_{j∈T′∖S} x_j. Hence Π(μ − X_Sϑ) = (b/√k + cηϑ₂) Σ_{j∈T′∖S} x_j and
‖μ − X_Sϑ‖² ≥ ‖Π(μ − X_Sϑ)‖² = (n−1)d (b/√k + cηϑ₂)². For A, β > 0 and real γ,
min_x {A(β + γx)² + x²/n} = Aβ²/(1 + nAγ²) (the minimiser is x = −Aγβ/(Aγ² + 1/n)). With A = (n−1)d, β = b/√k,
γ = cη: the first inequality. nAγ² = n(n−1)d c²η² ≤ n²·k·n⁻⁴ = k/n² ≤ 1: the second. ∎

**Reference cost.** For ϑ ∈ ℝ^T, B_T(ϑ) = ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≥ ‖μ − X_Tϑ‖² + ϑ₂²/n. By Lemma P with
S = T (d = k): B_T(ϑ) ≥ b²(n−1)/(1 + k/n²) ≥ b²(n−1)/2. And B_T(0) = ‖μ‖² = b²(n−1). So
b²(n−1)/2 ≤ min_ϑ B_T(ϑ) ≤ b²(n−1): the reference cost of T is of exact order n b², and n b² ≥ C_bV₀(log n)² → ∞.
For T′ and ϑ′ = (b/√k)1: μ − X_{T′}ϑ′ = 0, so B_{T′}(ϑ′) = (‖μ‖² + ‖ϑ′‖²)/n = (b²(n−1) + b²)/n = b² ≤ b̄².

## 2. Item 2 (the cutoffs)
q_j = C(p, j)w(j) = ½ Π_{i=0}^{j−1}(p−i)/(2p−1−i) for 1 ≤ j ≤ K = p. The factor i = 0 is p/(2p−1) ≤ 2/3 (p ≥ 2); for
i ≥ 1, (p−i)/(2p−1−i) ≤ ½ (⟺ i ≥ 1). So q_j ≤ (2/3)2^{−j} and Σ_{j>m} q_j ≤ (2/3)2^{−m}. With t = 2:
1/w(2) = 2C(2p−1, 2) = (2p−1)(2p−2) ≤ 4p², so R^T_m = Σ_{j=m+1}^{K} q_j/w(2) ≤ (8/3)p²2^{−m}.
For m_n := ⌊k/2⌋ ≥ (k−1)/2 ≥ 6L − ½: 2^{−m_n} ≤ √2 n^{−6 log 2}, 6 log 2 = 4.1588…, so
  n² R^T_{m_n} ≤ (8√2/3) p² n^{−2.158} ≤ 3.78 (12L + 3)² n^{−2.158} ≤ 1   (n ≥ 200):
at n = 200 the right side is 3.78·66.6²/200^{2.158} ≤ 0.19, and (12L+3)²n^{−2.158} is decreasing in n. Since R^T_m is
nonincreasing in m and m_n ≥ t = 2, m^T_n(½ log n) = min{m ≥ 2 : R^T_m ≤ n^{−3/2}e^{−(log n)/2}} ≤ m_n.
For [1a″]: D_T = det((n+1)G_T + I)/det(G_T + I) = [1 + (n+1)tr G_T + (n+1)²det G_T]/[1 + tr G_T + det G_T], with
tr G_T = 2(n−1) and det G_T = (n−1)²(1 − c²) = (n−1)²η²k/(1 + η²k) ≤ k/n². Numerator ≤ 1 + 2(n²−1) + (n+1)²k/n² ≤ 2n² + 2k,
denominator ≥ 2n − 1, so D_T ≤ (2n² + 2k)/(2n − 1) ≤ 2n (⟸ 2k ≤ 2n² − 2n). Hence
A^T_{m_n} = R^T_{m_n}√(D_T)√n ≤ n⁻²·√2·n ≤ 2/n ≤ n^{−1/2}.
(Exact values: `../numerics/c_counter_out.txt` E2 — n²R^T_{m_n} = 3.6·10⁻⁴ at n = 200; the selected larger n give smaller
values. The exact quantity is not monotone in n (ceiling/floor steps); the decreasing upper envelope above is what
proves the bound for every n ≥ 200.) [KBC-1]

## 3. Item 3 (the posterior leaves the small models)
Let 𝒮_n := {S ⊆ [p] : |S| ≤ m_n}. For S ∈ 𝒮_n: |S ∩ T′| ≤ m_n ≤ k/2, so d = |T′∖S| ≥ k/2.

**Step 1 (signal loss, uniform in S ∈ 𝒮_n).** L_S := min_{ϑ∈ℝ^S}{‖μ − X_Sϑ‖² + ‖ϑ‖²/n} ≥ (n−1)b²/4, by Lemma P with
d ≥ k/2 (‖ϑ‖² ≥ ϑ₂²). This holds whether or not S contains x₁ and/or x₂.

**Step 2 (fit of S from below).** By Lemma V, s_y²Q_S = min_ϑ{‖μ + Cε − X_Sϑ‖² + ϑᵀ(G_S + I)ϑ/n} (Cy^r = μ + Cε). Fix ϑ
and put v := μ − X_Sϑ ∈ 𝒳. Since v is centred and v ∈ 𝒳: vᵀCε = vᵀε = vᵀP_𝒳ε (P_𝒳 the projection onto 𝒳), so
‖v + Cε‖² = ‖v‖² + 2vᵀP_𝒳ε + ‖Cε‖² ≥ ‖v‖² − 2‖v‖‖P_𝒳ε‖ + ‖Cε‖² ≥ ½‖v‖² − 2‖P_𝒳ε‖² + ‖Cε‖²
(2ab ≤ a²/2 + 2b²). Also ϑᵀ(G_S + I)ϑ/n ≥ ‖ϑ‖²/n ≥ ½‖ϑ‖²/n. Minimising over ϑ:
  s_y²Q_S ≥ ‖Cε‖² − 2‖P_𝒳ε‖² + ½L_S ≥ ‖Cε‖² − 2‖P_𝒳ε‖² + (n−1)b²/8   for every S ∈ 𝒮_n.

**Step 3 (fit of T′ from above).** By Lemma V with ϑ′ = (b/√k)1 (μ − X_{T′}ϑ′ = 0):
s_y²Q_{T′} ≤ ‖Cε‖² + (‖μ‖² + ‖ϑ′‖²)/n = ‖Cε‖² + b².

**Step 4 (the event).** E := ‖Cε‖²/σ*² ~ χ²_{n−1}; E_𝒳 := ‖P_𝒳ε‖²/σ*² ~ χ²_{k+1} by (F3). Let
F_n := {E ≤ 2(n−1)} ∩ {E_𝒳 ≤ 2(k+1)}; by Chebyshev, P(F_nᶜ) ≤ 2/(n−1) + 2/(k+1) → 0. On F_n:
- a := 2b₀s_y² = 0.02‖μ + Cε‖²/(n−1) ≤ 0.04(‖μ‖² + ‖Cε‖²)/(n−1) ≤ 0.04(b² + 2σ*²);
- Δ := (n−1)b²/8 − 2‖P_𝒳ε‖² − b² ≥ (n−1)b²/8 − 4σ*²(k+1) − b². Here 4σ*²(k+1) ≤ σ*²(48L + 8) ≤ n b²(48L + 8)/(C_bL²)
  ≤ 0.0078 n b² (using n b² ≥ C_bσ*²L² and L ≥ 5.298: 48/(1200·5.298) + 8/(1200·28.07) ≤ 0.0078); (n−1)b²/8 ≥ 0.1243 n b²;
  b² ≤ 0.005 n b². So Δ ≥ 0.111 n b² ≥ n b²/10.
- For S ∈ 𝒮_n, by Steps 2–3 (numerator ≥ denominator + Δ):
  (2b₀ + Q_S)/(2b₀ + Q_{T′}) = (a + s_y²Q_S)/(a + s_y²Q_{T′}) ≥ 1 + Δ/(a + ‖Cε‖² + b²) ≥ 1 + (n b²/10)/(2nV₀) = 1 + b²/(20V₀),
  because a + ‖Cε‖² + b² ≤ 0.04(b² + 2σ*²) + 2σ*²(n−1) + b² ≤ 2σ*²n + 1.04b̄² ≤ 2n(σ*² + b̄²).
- Since b²/(20V₀) ≤ 1/20 and log(1 + x) ≥ x − x²/2 ≥ 0.975x on [0, 1/20], and ν ≥ n/2:
  ((2b₀ + Q_{T′})/(2b₀ + Q_S))^{ν} ≤ exp(−0.975 n b²/(40V₀)) ≤ exp(−n b²/(42V₀)).

**Step 5 (prior, determinant, count).** For S ∈ 𝒮_n (S ≠ T′ since |S| ≤ k/2 < k; T′, S ∈ Ω by (F1)):
  π(S)/π(T′) = [w(|S|)/w(k)] (D_{T′}/D_S)^{1/2} ((2b₀ + Q_{T′})/(2b₀ + Q_S))^{ν}.
w(|S|)/w(k) = C(2p−1, k)/C(2p−1, |S|) ≤ C(2p−1, k) ≤ 2^{2p−1}. D_{T′} = n^k (Lemma S(1), equality case, k times from
D_∅ = 1). D_S = Π_i ((n+1)λ_i + 1)/(λ_i + 1) ≥ 1 (λ_i ≥ 0 the eigenvalues of G_S). |𝒮_n| ≤ 2^p. So on F_n
  π(|S| ≤ m_n) ≤ Σ_{S∈𝒮_n} π(S)/π(T′) ≤ 2^{3p−1} n^{k/2} exp(−n b²/(42V₀)).
By (F1): (3p−1) log 2 + (k/2) log n ≤ (36L + 8)(0.6932) + (6L + ½)L ≤ 6L² + 25.5L + 5.6 ≤ 12L² (⟸ 6L² − 25.5L − 5.6 ≥ 0,
true for L ≥ 4.46). And 12L² ≤ n b²/(100V₀) because n b² ≥ 1200V₀L². Therefore, on F_n,
  π(|S| ≤ m_n) ≤ exp(n b²/(100V₀) − n b²/(42V₀)) ≤ exp(−c₁ n b²),   c₁ := 1/(73V₀) = 1/(73(σ*² + b̄²)).
P(F_n) → 1 and n b² ≥ 1200V₀(log n)² → ∞: π(|S| ≤ m_n) → 0 in probability, and by item 2
π(|S| > m^T_n(½ log n)) ≥ π(|S| > m_n) → 1 in probability. ∎

## 4. What fails
- **[L1a′]** (lines 12-16) defines Θ^T_{n,m} by π(|S| > m) = R^T_m (n+1)^{t/2}√n Θ^T_{n,m} and asserts
  sup_m P(Θ^T_{n,m} > L) ≤ (8 + 24M/σ*²)/(n−1) + L^{−1/2} + C′_Λ/log(√L/c♯), C′_Λ = 1/√2 + ½ + (M + M′)/(2σ*²); so Θ^T is
  tight when (σ*², M, M′) are fixed, and π(|S| > m^T_n(½ log n)) = O_P(n^{−1/2}). On 𝔇_n with t = 2, on F_n:
  Θ^T_{n,m_n} = π(|S| > m_n)/(R^T_{m_n}(n+1)√n) ≥ (1 − e^{−c₁nb²}) n²/((n+1)√n) → ∞, and π(|S| > m^T_n(½ log n)) → 1.
  So no bound of that form with constants free of M′ can hold: the coefficient bound cannot be dropped. (For each n
  the lemma does apply with M′ = M′_n := ‖θ‖²/n ≍ b²n³/k; for fixed L its bound is eventually vacuous, and to make
  the right side tend to zero with a growing threshold L = L_n one needs log L_n ≫ n³b²/k [KBC-2]. No contradiction.)
- **[1a″]** (lines 7-14) asserts, for a deterministic ϑ with B_T(ϑ) ≤ B, that π(|S| > m) = A^T_mΘ″_{n,m} with Θ″ tight
  for fixed (M, B). On 𝔇_n, on F_n, Θ″_{n,m_n} ≥ (1 − e^{−c₁nb²})·n/2 → ∞, although the approximation error ‖μ − X_Tϑ‖
  can be made 0. So the bounded-cost hypothesis cannot be replaced by a bound on the approximation error alone. Nor
  by a growing cost allowance B_n with B_n/(log n)² → ∞: fix any b̄ > 0 and put b_n² := C_bV₀(log n)²/n. For all large n,
  b_n ≤ b̄ and n b_n² = C_bV₀(log n)² ≤ B_n, so 𝔇_n is admissible, min_ϑ B_T(ϑ) ≤ b_n²(n−1) ≤ B_n, and the conclusion fails.
- Shown [KBC-3]: a sufficiently large constant multiple of (log n)² already breaks the conclusion (with
  b_n² = C_bV₀(log n)²/n, §1 gives 600V₀(1 − 1/n)(log n)² ≤ min_ϑ B_T(ϑ) ≤ 1200V₀(1 − 1/n)(log n)²). Not shown: whether an
  allowance B_n = o((log n)²) can break it, nor the sharp constant at order (log n)². Bounded cost is sufficient
  (`W3-POST2:B`); the intermediate regime is open. W3-POST2's numerics N6b (T = ∅, cost n − 1, conclusion intact) show that a large
  cost does not always break it; here it does, because the signal needs ≍ log n columns that T does not contain.

## 5. Numerics
`../numerics/c_counter.py` → `c_counter_out.txt`. V1: the structured formulas against generic linear algebra (float64,
η = 0.05, all models: 2·10⁻¹³; mpmath 60 digits at η = n⁻²: 1·10⁻¹⁵). E2: exact cutoffs at k = ⌈12 log n⌉. E1 (exact
enumeration at scaled-down k = 16–22, with the cutoffs computed exactly from their definitions; 20 seeds per row): on
the counterexample arm π(|S| > m′) has median 0.997 at n = 50 and 1.000 for n ≥ 100 (b = 3), posterior mean size ≈ k,
while on the control arm (μ = (b/2)(x₁ + x₂): bounded coefficients on T) it is ≤ 3.2·10⁻¹³ in every seed [KBC-4].
