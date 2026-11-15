# R — Lemma R′: scale invariance of the coded posterior and the contrast-law reduction (W3-MISR)

Status: **PROVED (by this seat, unchecked)**. Check record: line check K1 (gpt-6.1-sol high, blind,
`../reviews/K1_RM_check_sol.md`): R′(a), (a′), (a″), (b), (c) and table R.6 VERIFIED (no finding).
Notation and aliases: `../STATEMENT.md` (v1.3) §0–§1. [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`; [POST2] =
`Theory_work/Wave3/W3-POST2/STATEMENT.md`. The target π_𝒞 is the one defined in [W3P] lines 18-29 with X^r := x.

## R.0 The posterior as a function of the contrast vector

Fix n ≥ 3 and x (n × p, non-constant columns). X = CxD_x⁻¹ does not involve the response. For a non-constant y^r:
y = Cy^r/s_y with s_y² = ‖Cy^r‖²/(n − 1) > 0 ([W3P] lines 20-21), and the posterior is
π_𝒞(S) ∝ w(|S|)·D_S^{−1/2}(2b₀ + Q_S)^{−ν} on Ω, with Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, z_S = X_Sᵀy ([W3P] lines 21-24). D_S,
H_S, w, ν, b₀, Ω depend on (n, x) only. So π_𝒞(· | x, y^r) depends on y^r **only through the standardised vector y**, and
through y only via the two quadratic forms yᵀy and z_SᵀH_S⁻¹z_S = yᵀX_SH_S⁻¹X_Sᵀy.

## R.1 Proof of (a)

Let y′^r := a1 + c·y^r, c ≠ 0. C1 = 0, so Cy′^r = c·Cy^r; this is non-zero, so y′^r is non-constant, and
s_{y′} = |c|s_y. Hence y′ = c·Cy^r/(|c|s_y) = sgn(c)·y. Both quadratic forms of R.0 are even in y, so Q_S is the same
for y′ and y, for every S; the other factors do not involve the response. Therefore the unnormalised weights
w(|S|)D_S^{−1/2}(2b₀ + Q_S)^{−ν} agree for every S ∈ Ω, and so do π_𝒞 and every function of π_𝒞 (PIP_j, the set of
modes, MPM, ξ_q). ∎

Two consequences used below. (1) *Shift:* with a = −ȳ^r, c = 1: π_𝒞(· | x, y^r) = π_𝒞(· | x, Cy^r) = π_𝒞(· | x, UUᵀy^r).
So, for u ∈ ℝ^N∖{0}, define Φ(x, u) := π_𝒞(· | x, Uu) (Uu is non-constant: CUu = UUᵀUu = Uu ≠ 0). Then
  π_𝒞(· | x, y^r) = Φ(x, Uᵀy^r) for every non-constant y^r (then Uᵀy^r ≠ 0),        (R1)
(2) *Scale:* Φ(x, c·u) = Φ(x, u) for every c ≠ 0.                                      (R2)

## R.2 Proof of (a′)

The working model of [W3P] lines 26-28 is stated on the standardised scale: y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I),
β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01), S ~ ϖ. Its joint posterior Π^{std}(· | X, y) of (S, β_S, σ²) is a
function of (X, y). [POST2] lines 101-103 define Π(· | x, y^r) as the image of Π^{std}(· | X, y) under
(S, β, σ²) ↦ (S, s_yβ, s_y²σ²). For y′^r = a1 + c·y^r with c > 0: y′ = y (R.1), so Π^{std} is unchanged, and
s_{y′} = c·s_y; hence Π(· | x, y′^r) is the image of Π^{std}(· | X, y) under (S, β, σ²) ↦ (S, c·s_yβ, c²s_y²σ²), i.e. the
image of Π(· | x, y^r) under T_c : (S, θ, v) ↦ (S, cθ, c²v). ∎
As in R.1: Π(· | x, y^r) = Ψ(x, Uᵀy^r) with Ψ(x, u) := Π(· | x, Uu), and Ψ(x, c·u) = T_c♯Ψ(x, u) for c > 0 (♯ = image).  (R3)

## R.3 (a″) The code path (read at commit 16a7f85; `Scripts/SMC_BVS/core/`)

| step | file:line | what happens to the response |
|---|---|---|
| entry | `v3_fit.R:97` | `pre <- v3_preprocess(X, y, …)` |
| standardise | `v3_preprocess.R:123` with `:37-68` | `sy <- v3_standardise(y)`: divide by max\|y\|, centre, divide by the sample SD (n − 1); real-arithmetic value Cy/s_y (the anchored branch `:47-65` computes the same real number; it also stores metadata `centering`, `:62-64`, kept as `stable_centering`, `:129-130`, and copied into `fit$preprocessing`, `v3_fit.R:98` — none reaches a score [R1-F6]) |
| store | `v3_preprocess.R:124-127` | `y = sy$z` (standardised); `y_max`, `y_mean`, `y_sd_scaled`, `s_y` kept as metadata |
| budgets | `v3_preprocess.R:19-33`, `v3_fit.R:104-116` | functions of (n, p) and of timings; no response scale |
| context | `v3_fit.R:118`, `v3_setup.R:7-13` | `v3_context(pre$X, pre$y, …)` → C++ `data_init` |
| constants | `cpp/v3_score.h:14` | `a0 = 0.01, b0 = 0.01` — fixed numbers on the standardised scale |
| sufficient statistics | `cpp/v3_score.h:55-60` | `z = Xᵀy`, `yty = yᵀy`, `logm0 = logCn − ν log(2 b0 + yty)` |
| score | `cpp/v3_score.h:217-223` | `Q = yty − n·quad` (quad = zᵀH⁻¹z), `logm = logCn − ½(ldH − ldA) − ν log(2 b0 + Q)` |

`s_y`, `y_max`, `y_mean`, `y_sd_scaled` occur nowhere else under `Scripts/SMC_BVS/core/` (search for `s_y`, `y_sd`,
`y_max`, `y_mean` over `*.R`, `cpp/*.h`, `cpp/*.cpp`: only `v3_preprocess.R:126-127`). So the quantity the code
scores is the function of (X, y) of R.0, with the response entering only through y = Cy^r/s_y: its real-arithmetic
target is π_𝒞, to which (a) applies. No floating-point claim is made (STATEMENT §1 (a″)).
Observation (not a proof): `../numerics/N0_code_invariance.R` → `../numerics/N0_out.txt`: 25 transformed fits with the
compiled code, status and HPM unchanged, max |ΔPIP| = 1.304·10⁻¹⁰ (exact branch) and 1.037·10⁻¹¹ (SMC branch).

## R.4 Proof of (b)

Let the law of y^r satisfy GR^c at κ = (x, β, v): W := Uᵀ(y^r − xβ)/√v ~ N_N(0, I_N). Then
Uᵀy^r = Uᵀxβ + √v·W, which is non-zero almost surely (W has a density), so y^r is non-constant a.s. and by (R1), (R2)
  π_𝒞(· | x, y^r) = Φ(x, Uᵀxβ + √v·W) = Φ(x, Uᵀxβ/√v + W)   a.s.
Under the unit-noise G-model ỹ = xβ/√v + ε̃, ε̃ ~ N_n(0, I_n): Uᵀỹ = Uᵀxβ/√v + W̃ with W̃ := Uᵀε̃ ~ N_N(0, UᵀU) = N_N(0, I_N),
and π_𝒞(· | x, ỹ) = Φ(x, Uᵀxβ/√v + W̃) a.s. Φ(x, ·) is a measurable map into the probabilities on the finite set Ω
(continuous on ℝ^N∖{0}), and W, W̃ have the same law; so the two random probabilities have the same law. In
particular the law of π_𝒞(· | x, y^r) is the same for every law of y^r satisfying GR^c at κ.
Parameter posterior: by (R3) with c = 1/√v, T_{1/√v}♯Π(· | x, y^r) = Ψ(x, Uᵀy^r/√v) = Ψ(x, Uᵀxβ/√v + W), and
Π(· | x, ỹ) = Ψ(x, Uᵀxβ/√v + W̃): same law (Ψ(x, ·) is a measurable kernel). T_{1/√v} is the map
(S, θ, v′) ↦ (S, θ/√v, v′/v) of the statement.
The unit-noise model is model G of [W3P] line 31 with X^r = x, α* = 0, β* = β/√v, σ*² = 1; there θ* = D_xβ* = θ(κ)/√v,
μ = Cxβ* = μ(κ)/√v, S₀ = supp θ* = supp β = S₀(κ) (D_x has a positive diagonal). ∎

## R.5 Proof of (c) (projective form; stability)

Let y^r be non-constant, z := Uᵀy^r ≠ 0, T := zzᵀ/‖z‖². Cy^r = UUᵀy^r = Uz and s_y² = ‖Uz‖²/N = ‖z‖²/N, so y = √N·Uz/‖z‖.
For any symmetric n × n matrix B, yᵀBy = N·zᵀUᵀBUz/‖z‖² = N·tr(UᵀBU·T). The posterior depends on y only through
yᵀy = N and yᵀX_SH_S⁻¹X_Sᵀy, S ∈ Ω (R.0), each of this form; so
Q_S = N − nN·tr(UᵀX_SH_S⁻¹X_SᵀU·T) =: q_{x,S}(T), a linear function of T, and
π_𝒞(· | x, y^r) = F_x(T), F_x(T)(S) ∝ w(|S|)D_S^{−1/2}(2b₀ + q_{x,S}(T))^{−ν}: a continuous, hence measurable, function of T
on the set of rank-one projections of ℝ^N (there 2b₀ + q_{x,S}(T) = 2b₀ + Q_S ≥ 2b₀ > 0, as Q_S ≥ 0).
Under GR^c at κ, z = Uᵀxβ + √v·W with W ~ N_N(0, I); T_G(κ) is T(xβ + √vε̃), whose contrast vector is Uᵀxβ + √v·Uᵀε̃ with
Uᵀε̃ ~ N_N(0, I). So Law(T(y^r)) = Law(T_G(κ)): GR^c implies (PR), and E_κ h(π_𝒞) = E h(F_x(T_G(κ))) for every measurable
h with values in [0, 1].
For an arbitrary law of y^r (non-constant a.s.): E h(π_𝒞(· | x, y^r)) = E (h∘F_x)(T(y^r)), with h∘F_x measurable and
[0, 1]-valued. For two probability laws P₁, P₂ and a measurable f with values in [0, 1],
|∫f dP₁ − ∫f dP₂| ≤ sup_B |P₁(B) − P₂(B)| = d_TV(P₁, P₂). Apply it to the laws of T(y^r) and T_G(κ). ∎
*The example.* If Uᵀy^r = R·Z with Z := Uᵀxβ + √v·W and R > 0, then T(y^r) = R²ZZᵀ/(R²‖Z‖²) = ZZᵀ/‖Z‖²: (PR) holds whatever
the joint law of (R, W). *Why (c) stops at the model space.* Π(· | x, y^r) involves s_y = ‖z‖/√N (R.2), which is not a
function of T.

## R.6 Translation of the hypotheses (used by every later proof)

Let κ = (x, β, v) and write a tilde for the unit-noise model (x, β/√v, 1). Design objects (X, G_S, H_S, D_S, M_S, P_S,
the ranks d_J), the support S₀, s, p, K, j₀, m♯_n, 𝔉, Ω and the prior are the same in both. Mean objects scale:
μ̃ = μ(κ)/√v, μ̃_c = μ_c/√v, θ̃ = θ(κ)/√v, and L̃_S = μ̃_cᵀ(I − M_S)μ̃_c = L_S(κ)/v. Hence, at a given n:

| W3-MISR hypothesis at κ | [POST2]/[W3P] hypothesis for the unit-noise model (σ*² = 1) | source lines |
|---|---|---|
| (SZ) | 2 ≤ p ≤ n^A, 1 ≤ s₀ ≤ K (the per-n part of R1) | [POST2] 86; [W3P] 63-64 |
| (E^σ; M): ‖μ(κ)‖² ≤ nMv | (E): ‖μ̃‖² ≤ nM | [W3P] 67 |
| (F₀; φ₀) | (F₀) — identical (design and S₀ only) | [POST2] 25 |
| (OS; C_OS) | (OS; C_OS) — identical (design, S₀, n, p, A only) | [POST2] 29-36 |
| (ID^{M,σ}; c): L_S(κ) ≥ cv log n on 𝔉 | (ID^M; c): L̃_S ≥ c·1·log n on the same family | [POST2] 40-41, 128-129 |
| (ID^{M,σ}_j; c) | (ID^M_j; c) | [POST2] 42 |
| (F_λ; φ₀) | (F_λ) — identical | [W3P] 68-70 |
| (BM^σ; c): θ_j(κ)² ≥ cv log n/(nφ₀²) on S₀ | BM(c): θ̃_j² ≥ c·1·log n/(nφ₀²) | [W3P] 74-75 |

Model G holds for the unit-noise model by construction. Every implication is an equivalence, at each n separately.
