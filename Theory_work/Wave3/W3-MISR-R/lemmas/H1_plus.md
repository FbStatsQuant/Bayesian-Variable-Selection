# H1 — Corollary H⁺ (W3-MISR-R:CorH-plus)

Status (verbatim source for the registry):
- CorH-plus: **PROVED (by this seat, unchecked), conditional on W3-POST2:D**
(Clauses (a′) and (b) consume [POST2] Claim D(a), resp. D(b), by statement; (KL) and the readings are elementary.
Lemma R′ is W3-MISR:R'@1.0.0, "PROVED-CHECKED; …", unconditional.)

Statement: `../STATEMENT.md` §4 (v1.2); notation §1. BASE = `Theory_work/Wave3/W3-MISR/`; [POST2] =
`Theory_work/Wave3/W3-POST2/STATEMENT.md`; [D] = `Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md`; [W3P] =
`Theory_work/Wave3/W3-POST/STATEMENT.md`. Argument pattern: BASE `lemmas/G_corollaries.md` G.3 (`:67-93`, line-checked K2).

## H1.0 The scaling transfer (as BASE G.3)

For a configuration κ = (x, β, v) the unit-noise model is ỹ = xβ/√v + ε̃, ε̃ ~ N_n(0, I_n) (BASE `STATEMENT.md:90-93`),
with S₀ = S₀(κ), θ̃* = θ(κ)/√v, μ̃ = μ(κ)/√v; P̃ its law, Π̃(· | x, ỹ) its parameter posterior. T := T_{1/√v} :
(S, θ, v′) ↦ (S, θ/√v, v′/v). By Lemma R′(b) (BASE `STATEMENT.md:90-93`; `lemmas/R_reduction.md:59-72`), under P_κ:
(T1) the law of π_𝒞(· | x, y^r) equals the law of π_𝒞(· | x, ỹ) under P̃; in particular δ(κ) has the same law;
(T2) the random measure T♯Π(· | x, y^r) has the law of Π̃(· | x, ỹ) under P̃.
Images of the sets of STATEMENT §1 under T (all with θ zero-padded; X the standardised x, μ̂ = X_Sθ):
‖X_Sθ − μ(κ)‖² = v‖X_S(θ/√v) − μ̃‖²; |v′/v − 1| is the unit-noise |ṽ − 1|; ‖θ − θ(κ)‖ = √v‖θ/√v − θ̃*‖; and for normals
H²(N(a, v′), N(b, w)) and KL(N(a, v′) ‖ N(b, w)) depend on (a, b, v′, w) only through v′/w and (a − b)²/w (H²: [D] line 12,
as BASE G.3 `:79-82`; KL: the closed form in H1.3). Hence
  T(B^a_n(κ)) = B̃^a_n := {‖μ̃̂ − μ̃‖² > M_n} ∪ {|ṽ − 1| > M_n n^{−1/2}} ∪ {S ≠ S₀} ∪ {‖θ̃ − θ̃*‖ > M_n n^{−1/2}},
  T(B^b_n(κ)) = B̃^b_n := {‖μ̃̂ − μ̃‖² > C_H log n} ∪ {|ṽ − 1| > M_n n^{−1/2}},
and h̄_n(κ), k̄_n(κ) at (S, θ, v′) equal the unit-noise h̄_n, k̄_n (against N(μ̃_i, 1)) at T(S, θ, v′). By (T2), for each of
these sets B: Π(B | x, y^r) under P_κ has the law of Π̃(T(B) | x, ỹ) under P̃. (BASE G.3 `:74-78`.)

## H1.1 Proof of (a′)

Let κ_n ∈ 𝒦^F_n(s, A, M, φ₀) for n ≥ n₁ and δ_n → 0 in P_{κ_n}-probability. By (T1), δ̃_n := 1 − π_𝒞(S₀ | x_n, ỹ) → 0 in
P̃-probability. The unit-noise array (x_n, β_n/√v_n, σ*² = 1) is in regime R1 ([W3P] `:63-64`: s₀ = s ≥ 1 fixed;
2 ≤ p ≤ n^A and s ≤ K by (SZ); σ*² = 1 fixed; G) and satisfies (E) with constant M (‖μ̃‖² = ‖μ(κ_n)‖²/v_n ≤ nM by (E^σ; M))
and (F₀; φ₀) (design-only) for n ≥ n₁. These are exactly the hypotheses of [POST2] D(a) (`:107-111`: "In R1 under G, (E),
(F₀), if δ_n → 0 in probability"); (OS) and the margin are not among them. D(a) gives, for every M_n → ∞,
Π̃(B̃^a_n | ỹ) → 0 and Π̃(h̄_n > M_n n^{−1/2} | ỹ) → 0 in P̃-probability. By H1.0, Π(B^a_n(κ_n) | x_n, y^r) and
Π(H^a_n(κ_n) | x_n, y^r) have the same laws, so they → 0 in P_{κ_n}-probability.
*KL set.* Given M_n → ∞, put M′_n := min(M_n^{1/2}/2, n^{1/4}) → ∞. Let n ≥ 16 with M_n ≥ 4. Off B^a_n(κ_n) computed with
M′_n: |v′/v_n − 1| ≤ M′_n n^{−1/2} ≤ n^{−1/4} ≤ ½ and ‖μ̂ − μ(κ_n)‖² ≤ M′_n v_n, so by (KL)
  k̄_n ≤ M′_n²/n + M′_n/(2n) ≤ M_n/(4n) + M_n/(8n) < M_n/n
(M′_n² ≤ M_n/4; M′_n ≤ M_n^{1/2}/2 ≤ M_n/4 as M_n ≥ 4). So K^a_n(κ_n) ⊆ B^a_n(κ_n)|_{M′_n} for all large n, and
Π(K^a_n(κ_n) | x_n, y^r) → 0 in probability by the first part applied with M′_n. ∎

## H1.2 Proof of (b)

Let moreover κ_n ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS) for n ≥ n₁. As BASE G.3 (b) (`:69-82`): the unit-noise array is in R1 and
satisfies (E), (F₀), (OS; C_OS), the hypotheses of [POST2] D(b) (`:112-116`), which gives C_H = C_H(s, A, σ*² = 1) (this is
C_H(s, A) of STATEMENT §1; explicitly C_H = 8(C_A(s + j₀) + c₂) + 1 at σ*² = 1, [D] line 72, depending on (s, A) only) and,
for every M_n → ∞, Π̃(B̃^b_n | ỹ) → 0 and Π̃(h̄_n² > (1 + C_H/4) log n/n | ỹ) → 0 in P̃-probability (C′_H = 1 + C_H/4 at
σ*² = 1, [POST2] `:115`). By H1.0 the same holds for B^b_n(κ_n), H^b_n(κ_n) under P_{κ_n}.
*KL set.* Put M″_n := (log n)^{1/2}. Off B^b_n(κ_n) computed with M″_n: |v′/v_n − 1| ≤ (log n/n)^{1/2} ≤ ½ for n ≥ 5 and
‖μ̂ − μ(κ_n)‖² ≤ C_H v_n log n, so by (KL) k̄_n ≤ log n/n + C_H log n/(2n) = (1 + C_H/2) log n/n. Hence
K^b_n(κ_n) ⊆ B^b_n(κ_n)|_{M″_n} for n ≥ 5 and Π(K^b_n(κ_n) | x_n, y^r) → 0 in probability. ∎

## H1.3 Proof of (KL)

For one-dimensional normals, KL(N(a, v′) ‖ N(b, v)) = ½[log(v/v′) + v′/v − 1 + (a − b)²/v]. Averaging over i (v′ and v do
not depend on i): k̄_n(κ) = ½(v′/v − 1 − log(v′/v)) + ‖μ̂ − μ(κ)‖²/(2nv). For f(x) := x − 1 − log x on x > 0: f(1) = f′(1) = 0,
f″(ξ) = ξ^{−2}, so by Taylor's theorem f(x) = (x − 1)²/(2ξ²) for some ξ between 1 and x; if x ≥ ½ then ξ ≥ ½ and
f(x) ≤ 2(x − 1)², i.e. ½f(x) ≤ (x − 1)². With x = v′/v this is the displayed bound on {|v′/v − 1| ≤ ½}. ∎

## H1.4 The Kullback–Leibler reading (STATEMENT §4)

(i) Under (GR^c) at κ, Uᵀy^r = Uᵀxβ + √v W with W ~ N_N(0, I), so Uᵀy^r ~ N_N(Uᵀxβ, vI_N), and Uᵀxβ = UᵀXD_xβ = UᵀXθ(κ):
the law is the member (b, w) = (θ(κ), v) of the family, and KL of a law from itself is 0, the minimum.
(ii) By CorG-min (b) (`G1_min.md` G1.2(ii)), the conditional law of y^r given X^r_𝒞 is N_n((α + a)1 + X^r_𝒞β^𝒞, σ²_𝒞I), a
member of {N_n(a₀1 + X^r_𝒞b, wI)}; KL from itself is 0. Row-wise, in (E1) with deterministic α and parameters: by G1.5,
y_i = (α + a) + x_{𝒞,i}ᵀβ^𝒞 + ζ_iᵀβ_𝓜 + ε_i with (x_{𝒞,i}, ζ_i, ε_i), i ≤ n, independent across i and ζ_i, ε_i independent of
x_{𝒞,i}; so y_i | x_{𝒞,i} ~ N(α + a + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞), as in BASE G.3 `:91-93`. ∎

## H1.5 Implication BASE Cor-H (STATEMENT §8)

BASE Cor-H's setting is κ_n ∈ 𝒦⁰_n ⊆ 𝒦^F_n. BASE (b) is clause (b) (B^b, H^b). BASE (a) assumes in addition
κ_n ∈ 𝒦_n(…, c), c > c₁(s, A), or 𝒦^λ_n, c > c₀(s, A); then BASE MIS-R (i) gives E δ_n ≤ C r_n for n ≥ n₀, so δ_n → 0 in
probability (Markov), and (a′) gives BASE (a)'s conclusions (B^a, H^a). ∎
