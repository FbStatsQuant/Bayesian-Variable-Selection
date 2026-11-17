# ASSEMBLY — Theorem 2SG from Lemma B3w and W3-POST Theorem 1 item 6; Proposition ExSG

**Status: PROVED (by this seat, unchecked).** Ticket W3-D3 (Tier B). Targets: `STATEMENT.md` §1 (Theorem 2SG) and §3
(Proposition ExSG), v1.0.

Aliases: [EB] = `Theory_work/Wave3/W3-DIST/work/E_bridges/`; [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`.

## Inherited results used (statuses verbatim; registry at main 029bb748)
- `W3-POST:Thm-1@1.0.1` ([W3P] `:61-100`) — "PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7
  PASS". Used: item 6 (`:95-100`): "Let (X, θ*) be random with ε independent of (X, θ*), and suppose there are
  (X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which |supp θ*| = s₀ and (E), (F_λ), (F_w) hold with common constants
  (M, φ₀, g₀) and (BM) holds with a common c > c₀ or a common deterministic envelope M_n → ∞. Then 1–4 hold under the
  joint law of (X, θ*, ε)"; item 1 "(Rate) Under (BM): δ_n = 1 − π(S₀) = O_P(r_n)"; item 2 "P(HPM = S₀) ≥ P(δ_n < ½) → 1
  … P(MPM = S₀) → 1"; item 3 "For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; under (BM) this is O_P(r_n)".
- `W3-DIST:B0@1.0.1` ([EB]`B0.md` (a), (e)) — "PROVED-CHECKED; council R2, …": "(a) ỹ is non-constant, and
  Π(· | x, y^r) = T_{σ*}♯ Π(· | x, ỹ) (image measure); the model posteriors coincide: π(· | x, y^r) = π(· | x, ỹ)";
  "(e) … the rows (x_i, ỹ_i) satisfy the same model with intercept 0, coefficients β̃* = β*/σ* and noise variance 1, the
  same law ν_x of x, and the same supp β̃* = supp β*".
- `W3-D3:B3w` (`lemmas/B3w.md`, this ticket).

## Theorem 2SG

**Step 1 (scale).** Fix n and a data set with non-constant y^r (probability one: y^r has the Gaussian component ε) and at
least one retained column. By B0 (a) the model posterior computed from (X^r, y^r) equals the one computed from
(X^r, ỹ), ỹ := (y^r − α*1)/σ*. δ_n, PIP_j, HPM (with the same tie rule) and MPM are functions of the model posterior and of
S₀ = supp β* = supp β̃*, so they coincide for the two data sets. By B0 (e), (X^r, ỹ) follows the model of (A1) with
α* = 0, σ*² = 1, coefficients β̃*, and the same law of the rows. So it suffices to prove the three conclusions for the
unit-noise model; (A2) for β̃* reads b_lo/σ* ≤ |β̃*_j| ≤ b_hi/σ* on S₀, with σ* fixed, which is how Lemma B3w is written.

**Step 2 (events).** By Lemma B3w, for n ≥ n₁ the raw-design-measurable events 𝒜′_n (B3w Step 6) satisfy P(𝒜′_n) → 1,
lie inside {p_ret = p}, and on them |supp θ̃*| = s₀ and (E; M_E), (F_λ; φ₀), (F_w; g₀) and BM-∞ with the common envelope
M_n → ∞ hold, in regime R1, with ε independent of the raw design (hence of (X, θ̃*), which are functions of it).

**Step 3 (item 6 and the dimension).** Let (X°, θ°) be the replaced design and truth of B3w Step 6 (equal to (X, θ̃*) on
{p_ret = p}, a fixed admissible n × p pair otherwise), and let δ°_n, PIP°_j, HPM°, MPM° be the outputs of the posterior
computed from X° and the response Y° := X°θ° + Cε/σ* (on {p_ret = p}: Y° = Cỹ, the centred response the method uses, since
μ̃ = Xθ̃*). (X°, θ°) is a function of the raw design, so ε is independent of it; the events 𝒜′_n are (X°, θ°)-measurable
(on 𝒜′_n the pair equals (X, θ̃*)); and the posterior depends on the data only through (X°, Y°) ([W3P] §0 `:16-29`: the
target is a function of the standardised design and the centred, scaled response). Item 6 applies to (X°, θ°, ε) and
gives items 1–3 for the outputs with superscript °: δ°_n = O_P(r_n); P(HPM° = S₀) → 1 and P(MPM° = S₀) → 1; and
max_j |PIP°_j − 1{j ∈ S₀}| ≤ δ°_n. On {p_ret = p} every output equals its counterpart with superscript ° (no column is
removed, so the conventions of `STATEMENT.md` §0 for removed columns are not invoked), and P(p_ret ≠ p) ≤ P(𝒜′_nᶜ) → 0.

**Step 4 (conclusions).** (1) For every M > 0: P(δ_n > Mr_n) ≤ P(δ°_n > Mr_n) + P(p_ret ≠ p), so δ_n = O_P(r_n).
(2) P(HPM = MPM = S₀) ≥ 1 − P(HPM° ≠ S₀) − P(MPM° ≠ S₀) − P(p_ret ≠ p) → 1.
(3) For every data set with p_ret = p, max_j |PIP_j − 1{j ∈ S₀}| = max_j |PIP°_j − 1{j ∈ S₀}| ≤ δ°_n = δ_n; so for every
M > 0, P(max_j |PIP_j − 1{j ∈ S₀}| > Mr_n) ≤ P(δ°_n > Mr_n) + P(p_ret ≠ p), and the maximum is O_P(r_n).
By Step 1 these hold for the original data. ∎

*Constants.* Item 6 needs common constants only; here M = M_E, φ₀² = φ²/4, g₀ = φ²/8 and the envelope M_n depend on
(s₀, b_lo, b_hi, σ*², φ) and n; n₁ depends on (s₀, A, K). No constant depends on the law of the rows beyond K and φ.

## Proposition ExSG

*Claim* (`STATEMENT.md` §3). Let x = m + Lξ, m ∈ ℝ^p, L ∈ ℝ^{p×d} with LLᵀ = Σ a correlation matrix, ξ ∈ ℝ^d with independent
coordinates, E ξ_k = 0, Var ξ_k = 1, E exp(λξ_k) ≤ exp(K²λ²/2) for all k and λ. Then E x = m, Cov(x) = Σ and
E exp(λuᵀ(x − m)) ≤ exp(K²λ²uᵀΣu/2) for all u ∈ ℝ^p, λ ∈ ℝ. K = 1 for standard Gaussian, Rademacher and uniform on
[−√3, √3] coordinates.

*Proof.* E x = m + L E ξ = m; Cov(x) = L Cov(ξ) Lᵀ = L I_d Lᵀ = Σ. Fix u, λ and put v := Lᵀu ∈ ℝ^d. Then
uᵀ(x − m) = vᵀξ = Σ_k v_kξ_k, and by independence (each factor finite by hypothesis)
  E exp(λvᵀξ) = Π_k E exp((λv_k)ξ_k) ≤ Π_k exp(K²λ²v_k²/2) = exp(K²λ²‖v‖²/2),  ‖v‖² = uᵀLLᵀu = uᵀΣu.
*Examples (each has mean 0 and variance 1).* Standard Gaussian: E e^{λξ} = e^{λ²/2}. Rademacher: E e^{λξ} = cosh λ =
Σ_k λ^{2k}/(2k)! ≤ Σ_k (λ²/2)^k/k! = e^{λ²/2}, since (2k)! ≥ 2^k k! (true for k = 0; the ratio of consecutive terms of
the left side, (2k + 2)(2k + 1), is ≥ 2(k + 1), that of the right side). Uniform on [−√3, √3]: variance (2√3)²/12 = 1, and
for λ ≠ 0, E e^{λξ} = sinh(√3λ)/(√3λ) = Σ_k (3λ²)^k/(2k + 1)! ≤ Σ_k (λ²/2)^k/k! = e^{λ²/2}, since 3^k/(2k + 1)! ≤ 1/(2^k k!),
i.e. 6^k k! ≤ (2k + 1)! (true for k = 0; consecutive ratios (2k + 3)(2k + 2) ≥ 6(k + 1) because 2k + 3 ≥ 3); λ = 0 is
trivial. ∎

*Gaussian rows.* N_p(m, Σ) is the case L = Σ^{1/2} (d = p), ξ ~ N_p(0, I_p): (A4) holds with K = 1 for every u.
