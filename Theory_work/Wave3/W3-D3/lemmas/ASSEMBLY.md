# ASSEMBLY — Theorem 2SG from Lemma B3w and W3-POST Theorem 1 item 6; Proposition ExSG

**Status: PROVED (by this seat, unchecked).** Ticket W3-D3 (Tier B). Targets: `STATEMENT.md` §1 (Theorem 2SG) and §3
(Proposition ExSG), v1.2 [K2-2] (symbols per [L1-1]: L = sub-Gaussian constant, K_cap = min(p_ret, ⌊n/2⌋)).

Aliases: [EB] = `Theory_work/Wave3/W3-DIST/work/E_bridges/`; [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`.

## Inherited results used (statuses verbatim; registry at main 029bb748)
- `W3-POST:Thm-1@1.0.1` ([W3P] `:61-100`) — "PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7
  PASS". Used: item 6 ([W3P] `:95-100`): "Let (X, θ*) be random with ε independent of (X, θ*), and suppose there are
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

**Step 1 (scale).** Fix n ≥ 3 [K1-5] and a data set with non-constant y^r (probability one: y^r has the Gaussian component ε) and
p_ret ≥ 1 (this contains {p_ret = p}, as p ≥ 2; on {p_ret = 0} the outputs are the conventions of `STATEMENT.md` §0 and
enter below only through P(p_ret ≠ p)). By B0 (a) the model posterior computed from (X^r, y^r) equals the one computed from
(X^r, ỹ), ỹ := (y^r − α*1)/σ*. δ_n, PIP_j, HPM (with the same tie rule) and MPM are functions of the model posterior and of
S₀ = supp β* = supp β̃*, so they coincide for the two data sets. By B0 (e), (X^r, ỹ) follows the model of (A1) with
α* = 0, σ*² = 1, coefficients β̃*, and the same law of the rows. So it suffices to prove the three conclusions for the
unit-noise model; (A2) for β̃* reads b_lo/σ* ≤ |β̃*_j| ≤ b_hi/σ* on S₀, with σ* fixed, which is how Lemma B3w is written.

**Step 2 (events) [L1-2].** By Lemma B3w (b), (c), for n ≥ n₁: the completed pair (X°, θ°) is a Borel function of the raw
design, independent of ε; the (X°, θ°)-measurable events 𝒜′_n satisfy P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0; and on 𝒜′_n the hypotheses of
item 6 hold for (X°, θ°, ε/σ*) in regime R1 with common constants (M_E, φ₀, g₀) and the common envelope M_n → ∞.
Also P(p_ret ≠ p) ≤ P(𝒜_nᶜ) → 0, since 𝒜_n ⊆ {p_ret = p}.

**Step 3 (item 6 and the dimension).** With the completed pair (X°, θ°) of B3w (c) (equal to (X, θ̃*) on {p_ret = p}), let δ°_n, PIP°_j, HPM°, MPM° be the outputs of the posterior
computed from X° and the response Y° := X°θ° + Cε/σ* (on {p_ret = p}: Y° = Cỹ, the centred response the method uses, since
μ̃ = Xθ̃*). (X°, θ°) is a function of the raw design, so ε is independent of it; the events 𝒜′_n are (X°, θ°)-measurable; and the posterior depends on the data only through (X°, Y°) ([W3P] §0 `:16-29`: the
target is a function of the standardised design and the centred, scaled response). supp θ° = S₀ on every outcome (B3w (c): on {p_ret = p}
because all ŝ_j > 0, off it by the choice of θ⁰), so item 6's outputs refer to S₀, and in 𝒜′_n (F_λ) and (F_w) are anchored
at supp θ° = S₀ [K1-1]. Item 6 applies to (X°, θ°, ε/σ*) and gives items 1–3 for the outputs with superscript °: δ°_n = O_P(r_n); P(HPM° = S₀) → 1 and P(MPM° = S₀) → 1; and
max_j |PIP°_j − 1{j ∈ S₀}| ≤ δ°_n. On {p_ret = p} every output equals its counterpart with superscript ° (no column is
removed, so the conventions of `STATEMENT.md` §0 for removed columns are not invoked), and P(p_ret ≠ p) → 0 (Step 2).

**Step 4 (conclusions).** (1) For every M > 0: P(δ_n > Mr_n) ≤ P(δ°_n > Mr_n) + P(p_ret ≠ p), so δ_n = O_P(r_n).
(2) P(HPM = MPM = S₀) ≥ 1 − P(HPM° ≠ S₀) − P(MPM° ≠ S₀) − P(p_ret ≠ p) → 1.
(3) For every data set with p_ret = p, max_j |PIP_j − 1{j ∈ S₀}| = max_j |PIP°_j − 1{j ∈ S₀}| ≤ δ°_n = δ_n; so for every
M > 0, P(max_j |PIP_j − 1{j ∈ S₀}| > Mr_n) ≤ P(δ°_n > Mr_n) + P(p_ret ≠ p), and the maximum is O_P(r_n).
By Step 1 (on {p_ret = p} the outputs for (X^r, y^r) and (X^r, ỹ) coincide) these hold for the original data. ∎

*Constants.* Item 6 needs common constants only; here M = M_E, φ₀² = φ²/4, g₀ = φ²/8 and the envelope M_n depend on
(s₀, b_lo, b_hi, σ*², φ) and n; n₁ depends on (s₀, A, L). No constant depends on the law of the rows beyond L and φ.

## Proposition ExSG

*Claim* (`STATEMENT.md` §3). Let x = m + Bξ, m ∈ ℝ^p, B ∈ ℝ^{p×d} with BBᵀ = Σ a correlation matrix, ξ ∈ ℝ^d with independent
coordinates, E ξ_k = 0, Var ξ_k = 1. (a) If E exp(λξ_k) ≤ exp(L²λ²/2) for all k and λ, then E x = m, Cov(x) = Σ and
E exp(λuᵀ(x − m)) ≤ exp(L²λ²uᵀΣu/2) for all u ∈ ℝ^p, λ ∈ ℝ; in particular (A4) holds with this L. (b) The scalar hypothesis
holds with L = 1 for standard Gaussian, Rademacher and uniform on [−√3, √3] coordinates, and with L = K when every ξ_k
takes its values in an interval of length 2K, the same K for all k [R1-opus-E4].

*Proof of (a).* E x = m + B E ξ = m; Cov(x) = B Cov(ξ) Bᵀ = B I_d Bᵀ = Σ. Fix u, λ and put v := Bᵀu ∈ ℝ^d. Then
uᵀ(x − m) = vᵀξ = Σ_k v_kξ_k, and by independence (each factor finite by hypothesis)
  E exp(λvᵀξ) = Π_k E exp((λv_k)ξ_k) ≤ Π_k exp(L²λ²v_k²/2) = exp(L²λ²‖v‖²/2),  ‖v‖² = uᵀBBᵀu = uᵀΣu.
This holds for every u, in particular for every u with at most 5(A + 1)(s₀ + 1) log n nonzero entries, which is (A4) when
m = m_n and Σ = Σ_n. ∎(a)

*Proof of (b).* Each example has mean 0 and variance 1. Standard Gaussian: E e^{λξ} = e^{λ²/2}. Rademacher:
E e^{λξ} = cosh λ = Σ_k λ^{2k}/(2k)! ≤ Σ_k (λ²/2)^k/k! = e^{λ²/2}, since (2k)! ≥ 2^k k! (equality at k = 0; going from k to
k + 1 multiplies the left side by (2k + 2)(2k + 1) and the right side by 2(k + 1)). Uniform on [−√3, √3]: variance
(2√3)²/12 = 1, and for λ ≠ 0, E e^{λξ} = sinh(√3λ)/(√3λ) = Σ_k (3λ²)^k/(2k + 1)! ≤ Σ_k (λ²/2)^k/k! = e^{λ²/2}, since
(2k + 1)!/(2^k k!) = Π_{i=1}^k(2i + 1) ≥ 3^k; λ = 0 is trivial.
*Bounded coordinates (Hoeffding's lemma, proved here for self-containment).* Let Y take values in [a, b], a < b, with
E Y = 0 (so a ≤ 0 ≤ b), and let λ ∈ ℝ. By convexity of y ↦ e^{λy}, e^{λy} ≤ ((b − y)e^{λa} + (y − a)e^{λb})/(b − a) on [a, b];
taking expectations, E e^{λY} ≤ (be^{λa} − ae^{λb})/(b − a). If a = 0 then b ≥ 0 = E Y forces Y = 0 a.s. and the bound below
is trivial; likewise if b = 0. Otherwise put θ := −a/(b − a) ∈ (0, 1) and h := λ(b − a); then
(be^{λa} − ae^{λb})/(b − a) = e^{−θh}(1 − θ + θe^h) = e^{ψ(h)}, ψ(h) := −θh + log(1 − θ + θe^h). ψ(0) = 0,
ψ′(h) = −θ + θe^h/(1 − θ + θe^h), so ψ′(0) = 0, and ψ″(h) = ρ(1 − ρ) ≤ ¼ with ρ := θe^h/(1 − θ + θe^h) ∈ (0, 1). By Taylor's
theorem with the Lagrange remainder, ψ(h) ≤ h²/8. Hence E e^{λY} ≤ exp(λ²(b − a)²/8). For ξ_k with values in an interval
of length b − a = 2K: E e^{λξ_k} ≤ exp(λ²(2K)²/8) = exp(K²λ²/2). (Hoeffding 1963, J. Amer. Statist. Assoc. 58, 13–30,
inequality (4.16), is this statement.) ∎(b)

*Gaussian rows.* N_p(m, Σ) is the case B = Σ^{1/2} (d = p), ξ ~ N_p(0, I_p): (A4) holds with L = 1 for every u.
