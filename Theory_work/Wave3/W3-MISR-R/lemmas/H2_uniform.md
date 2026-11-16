# H2 — Corollary H-U (W3-MISR-R:CorH-U): uniform and conditional random-design forms

Status (verbatim source for the registry):
- CorH-U: **PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C, W3-POST2:A0; clause (G) also conditional on W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128, C-MIS:GDb**
(W3-POST2:D through CorH-plus; W3-POST2:C through BASE MIS-R (i) (fillers in (U-a); (UP) in (G)); W3-POST2:A0 through
the fillers' (OS); (G) consumes CorGb-plus's proof (`G2_corr.md`) and so carries its conditions.)

Statement: `../STATEMENT.md` §5 (v1.2); notation §1. BASE = `Theory_work/Wave3/W3-MISR/`; [POST2] =
`Theory_work/Wave3/W3-POST2/STATEMENT.md`; [D] = `…/W3-POST2/lemmas/D_hellinger.md`; [A] = `…/W3-POST2/lemmas/A_occam.md`;
[W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`. Monotonicity used throughout: (E^σ; M) is weaker for larger M, (F₀; φ₀)
for smaller φ₀, (OS; C_OS) for larger C_OS (each is a single inequality in the constant).

## H2.0 The parameter posterior as a function of the contrast vector

By BASE (R3) (`lemmas/R_reduction.md:37`), Π(· | x, y^r) = Ψ(x, Uᵀy^r) with Ψ(x, u) := Π(· | x, Uu), for every non-constant
y^r (u = Uᵀy^r ≠ 0). Explicitly ([POST2] `:101-103`; [D] D0 `:8-11`): with y_c = u, s_y² = ‖u‖²/N, b = b₀s_y², Ψ(x, u) is the
mixture over S ∈ Ω of π_𝒞(S | ·) = Φ(x, u)(S) (BASE (R1), `R_reduction.md:26`) times v′ | S ~ IG(ν, b + Q^c_S/2) and
θ_S | v′, S ~ N(nH_S⁻¹X_{c,S}ᵀu, nv′H_S⁻¹), where X_c = UᵀX, H_S, Q^c_S = uᵀ(I − M_S)u are continuous functions of (x, u) on
{x ∈ 𝔛_n(p), u ≠ 0}.
(i) *Same law for all GR^c laws.* Under any law of y^r with (GR^c) at κ, u = Uᵀxβ + √v W, W ~ N_N(0, I) (u ≠ 0 a.s.); so
the law of Π(· | x, y^r) — hence P_κ(Π(B) > η) for any set B fixed by κ — does not depend on which such law is used.
(ii) *Measurability.* For each n and each of the six set families B_n(κ) ∈ {B^a_n, H^a_n, K^a_n, B̄^b_n, H̄^b_n, K̄^b_n} put
  g_n(κ, w) := Ψ(x, Uᵀxβ + √v w)(B_n(κ)) if Uᵀxβ + √v w ≠ 0, and g_n(κ, w) := 0 otherwise.
On each stratum {p = p′} of the configuration space 𝔎_n (BASE `STATEMENT.md:28-31`, `M_misr.md:133`), the indicator
1_{B_n(κ)}(S, θ, v′) is a Borel function of (κ, S, θ, v′) (each defining inequality compares continuous functions of
(x, β, v, S, θ, v′): μ̂ = X_Sθ with X continuous in x on 𝔛_n(p′), μ(κ), θ(κ), h̄_n, k̄_n), and the kernel Ψ(x, u)(dS dθ dv′)
has a density in (θ, v′) w.r.t. counting × Lebesgue that is jointly Borel in (x, u, S, θ, v′) on {u ≠ 0}. By Tonelli g_n is
Borel on 𝔎_n × ℝ^N [L1-4]. For fixed κ the set {w : Uᵀxβ + √v w = 0} is N_N(0, I)-null.

## H2.1 Lemma H0 (fillers)

Fix s ≥ 1, A ≥ 1 and c > 0. Put p_f := max(s, 2). For n ≥ p_f + 1 choose orthonormal e_1, …, e_{p_f} in 1^⊥ ⊂ ℝⁿ (dim n − 1 ≥
p_f) and x^f := √(n − 1)[e_1 ⋯ e_{p_f}], β^f := Σ_{j≤s} u_j (u_j the coordinate vectors of ℝ^{p_f}), v^f := 1, κ^f_n := (x^f, β^f, 1).
Columns are centred and non-zero, so non-constant; their sample SDs are 1, so X = x^f, D_x = I, θ = β^f, S₀ = [s],
G_S = (n − 1)I_{|S|} for every S. Then: (SZ) for n ≥ max(p_f, 2s) (2 ≤ p_f ≤ n ≤ n^A; s ≤ min(p_f, ⌊n/2⌋)); (E^σ; s):
‖μ‖² = s(n − 1) ≤ sn; (F₀; 1), (F_λ; 1): λ_min(G_T/(n − 1)) = 1 for every T; (F_w; 1): λ_min(G_{S₀∪J}) = n − 1 ≥ 1, so by
[A] Lemma A0 (i)–(iii) (`:14-15`; in R1) (OS; C_f) for n ≥ n_OS, with (n_OS, C_f) depending only on (s, A, c_D = ½);
(BM^σ; c): θ_j² = 1 ≥ c log n/n for n ≥ n_c. So for n ≥ n_f(s, A, c) := max(p_f + 1, 2s, n_OS, n_c):
  κ^f_n ∈ 𝒦^λ_n(s, A, s, 1, C_f, c) ⊆ 𝒦⁰_n(s, A, s, 1, C_f) ⊆ 𝒦^F_n(s, A, s, 1),
and, by monotonicity, for any M ≥ 0, 0 < φ₀ ≤ 1, C_OS: κ^f_n ∈ 𝒦⁰_n(s, A, M ∨ s, φ₀, C_OS ∨ C_f). ∎

## H2.2 Proof of (U-b)

Fix one of the three families b ∈ {B̄^b, H̄^b, K̄^b} and suppose the claim fails: there are ε > 0, an infinite set 𝒩 ⊆ ℕ and,
for n ∈ 𝒩, κ_n ∈ 𝒦⁰_n(≤s̄, A, M, φ₀, C_OS) with P_{κ_n}(Π(b_n(κ_n)) > η) > ε (a supremum > ε is exceeded by a member).
As s(κ_n) ∈ {1, …, s̄}, there is an infinite 𝒩′ ⊆ 𝒩 and s with s(κ_n) = s on 𝒩′. Define κ̂_n := κ_n for n ∈ 𝒩′ and
κ̂_n := κ^f_n (H0 with this s and any c) for n ∉ 𝒩′, n ≥ n_f. Then κ̂_n ∈ 𝒦⁰_n(s, A, M ∨ s, φ₀, C_OS ∨ C_f) for all n ≥ n_f.
By CorH-plus (b) (`H1_plus.md` H1.2) for this array: for the given M_n → ∞, Π(B^b_n(κ̂_n)), Π(H^b_n(κ̂_n)), Π(K^b_n(κ̂_n))
→ 0 in probability, where these sets use C_H(s, A) — which does not depend on (M ∨ s, φ₀, C_OS ∨ C_f) ([POST2] `:113`,
[D] line 72). Since C̄_H ≥ C_H(s, A), B̄^b_n(κ) ⊆ B^b_n(κ), H̄^b_n(κ) ⊆ H^b_n(κ), K̄^b_n(κ) ⊆ K^b_n(κ) (the thresholds on
‖μ̂ − μ‖², h̄², k̄ are larger; the variance part is the same). Along 𝒩′, P_{κ_n}(Π(b_n(κ_n)) > η) ≤ P_{κ̂_n}(Π(·) > η) for the
corresponding set with C_H(s, A), which → 0 (H2.0(i): the probabilities do not depend on the choice of law): this
contradicts > ε on the infinite set 𝒩′. ∎

## H2.3 Proof of (U-a)

Fix b ∈ {B^a, H^a, K^a}; suppose the claim fails: ε > 0, infinite 𝒩′, s, κ_n ∈ 𝒦^♭_n ∩ 𝒦^F_n(s, A, M, φ₀) for n ∈ 𝒩′ with
P_{κ_n}(Π(b_n(κ_n)) > η) > ε (as in H2.2). Let κ̂_n := κ_n on 𝒩′ and κ^f_n (H0 with c := c₀(s, A) + 1) off 𝒩′, n ≥ n_f; then
κ̂_n ∈ 𝒦^F_n(s, A, M ∨ s, φ₀) for n ≥ n_f. Selection: for η′ > 0, on 𝒩′, P_{κ_n}(δ > η′) ≤ sup_{κ∈𝒦^♭_n} P_κ(δ(κ) > η′) → 0
by (UP); off 𝒩′, κ^f_n ∈ 𝒦^λ_n(s, A, s, 1, C_f, c) with c > c₀(s, A), so BASE MIS-R (i) (`STATEMENT.md:113`) gives
E δ(κ^f_n) ≤ C r_n for n ≥ n₀ and P(δ(κ^f_n) > η′) ≤ C r_n/η′ → 0. So δ(κ̂_n) → 0 in probability along all n. CorH-plus (a′)
(`H1_plus.md` H1.1) gives Π(b_n(κ̂_n)) → 0 in probability for the given M_n (the sets B^a, H^a, K^a involve no class
constant), contradicting the choice of 𝒩′. ∎

## H2.4 Proof of (RD)

Setting of BASE §4: κ_n = (X^r_𝒞, β^𝒞, σ²_𝒞) is 𝓕_n-measurable and W_n := Uᵀ(y^r − X^r_𝒞β^𝒞)/σ_𝒞 is independent of 𝓕_n with law
N_N(0, I). Then Uᵀy^r = UᵀX^r_𝒞β^𝒞 + σ_𝒞W_n, which is non-zero a.s. (conditionally on 𝓕_n it is non-degenerate Gaussian);
by H2.0, Π(B_n(κ_n) | X^r_𝒞, y^r) = g_n(κ_n, W_n) a.s. By the freezing property used in BASE `M_misr.md:143-145` (bounded
jointly Borel F of an 𝓕_n-measurable variable and an independent one: E[F(κ_n, W_n) | 𝓕_n] = ∫ F(κ_n, w) N_N(0, I)(dw)
a.s.), applied to F := 1{g_n > η}:
  P(Π(B_n(κ_n) | X^r_𝒞, y^r) > η | 𝓕_n) = Ĝ_n(κ_n) a.s.,  Ĝ_n(κ) := ∫ 1{g_n(κ, w) > η} N_N(0, I)(dw) = P_κ(Π(B_n(κ)) > η)
(H2.0(i): for fixed κ, Uᵀxβ + √v w with w ~ N(0, I) is the contrast vector under a law with (GR^c) at κ, and the zero-contrast
set is null). On 𝒜_n ⊆ {κ_n ∈ 𝒦♯_n}, Ĝ_n(κ_n) ≤ sup_{κ∈𝒦♯_n} P_κ(Π(B_n(κ)) > η) = ε_n. Hence
P(Π(B_n(κ_n)) > η) = E Ĝ_n(κ_n) ≤ E[Ĝ_n(κ_n)1_{𝒜_n}] + P(𝒜_nᶜ) ≤ ε_n + P(𝒜_nᶜ), and ε_n → 0 by (U-b), resp. (U-a). If
P(𝒜_n) → 1, the bound → 0 for every η > 0: convergence in probability. *η-family*, (a)-type sets: for each η″ the same bound
with the class 𝒦^{♭,η″}_n and 𝒜^{η″}_n gives limsup_n P(Π(B_n(κ_n)) > η) ≤ 0 + η″ (B^a, H^a, K^a depend only on M_n and κ, not
on (s̄, A, M, φ₀)_{η″}); η″ is arbitrary. ∎

## H2.5 Proof of (G) [LA-1]

Setting and hypotheses of STATEMENT §3. By `G2_corr.md` (steps 1–5 and [R-4]): with κ_n := (X^r_𝒞, β^𝒞, σ²_𝒞) (reference off
the null event), (GR^c | σ(X^r_𝒞)) holds, and for n ≥ n* the event 𝒜_n ∈ σ(X^r_𝒞) satisfies
𝒜_n ⊆ {κ_n ∈ 𝒦^λ_n(s, A, M, φ₀, C_OS, c)} with M = 2M₀ + 1, φ₀ = (c_R/8)^{1/2} (≤ 1, as c_R ≤ R_jj = 1), and
P(𝒜_nᶜ) ≤ (2 + 2k_n)n^{−2} + n^{−1} → 0. Take 𝒦^♭_n := 𝒦^λ_n(s, A, M, φ₀, C_OS, c) ⊆ 𝒦^F_n(s, A, M, φ₀): by BASE MIS-R (i)
(c > c₀(s, A)), sup_{κ∈𝒦^♭_n} P_κ(δ(κ) > η′) ≤ C r_n/η′ → 0, i.e. (UP). (RD) with 𝓕_n := σ(X^r_𝒞) and these 𝒜_n gives
P(Π(B | X^r_𝒞, y^r) > η) ≤ ε_n + P(𝒜_nᶜ) → 0 for B ∈ {B^a_n(κ_n), H^a_n(κ_n), K^a_n(κ_n)}, every M_n → ∞ and η > 0. ∎

## H2.6 Implication CorH-plus (STATEMENT §8)

For a sequence κ_n ∈ 𝒦^F_n(s, A, M, φ₀) with δ_n → 0 in probability, 𝒦^♭_n := {κ_n} satisfies (UP), and (U-a) gives (a′); for
κ_n ∈ 𝒦⁰_n(s, …) (s̄ := s, C̄_H = C_H(s, A)), (U-b) gives (b). (CorH-U's proof uses CorH-plus; the implication records that
CorH-U contains it.)
