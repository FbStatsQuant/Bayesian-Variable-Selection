# W3-DIST — Lemma H (Hellinger reduction; deterministic) — stream B

**Status: DRAFT (by this seat, unchecked).** Author: stream B (Claude Opus 5.5, Claude Third). Target: STATEMENT.md
v1.3.1 §3 "Lemma H" (lines 291–295). Notation: STATEMENT §0 and API_CARDS "Common definitions" (binding).
No statement change is requested for Lemma H. The computations of `W3-POST2/lemmas/D_hellinger.md` D0 (lines 8–18)
and D4.0 (lines 84–88) are re-derived here, not cited as premises.

Numerical sanity check: `check_H.py` → `check_H_out.txt` (pointwise inequality on a grid, closed-form affinity versus
quadrature, the in-sample identity with a dropped true column).

---

## H.0 Objects (from STATEMENT §0, made explicit)

- Raw design X^r ∈ ℝ^{n×p_raw} with rows x_iᵀ; column means x̄ := n⁻¹X^{rT}1; centring matrix C := I − 11ᵀ/n.
- Column j is *retained* iff Cx^r_j ≠ 0 (x^r_j the j-th raw column), otherwise *dropped*. For retained j,
  ŝ_j := ‖Cx^r_j‖/√(n − 1) > 0 and x_j := Cx^r_j/ŝ_j (so ‖x_j‖² = n − 1, 1ᵀx_j = 0). X is the matrix of the retained
  standardised columns; X_S its sub-matrix on S ⊆ {retained}.
- Truth: y^r = α*1 + X^rβ* + ε, ε ∈ ℝⁿ; ε̄ := n⁻¹1ᵀε; μ := CX^rβ*; θ*_j := ŝ_jβ*_j for retained j.
- A posterior draw is (S, θ, v) with S a set of retained columns, θ ∈ ℝ^S, v > 0. Raw coefficients b ∈ ℝ^{p_raw}:
  b_j := θ_j/ŝ_j for j ∈ S, b_j := 0 otherwise (in particular on dropped columns). Plug-in intercept â := ȳ^r − x̄ᵀb,
  ȳ^r := n⁻¹1ᵀy^r. Fitted centred mean μ̂ := X_Sθ.
- Densities with respect to the σ-finite measure λ_ν := ν_x ⊗ Leb on ℝ^{p_raw} × ℝ:
  f_{S,θ,v}(x, y) := φ(y; â + xᵀb, v),  f*(x, y) := φ(y; α* + xᵀβ*, σ*²),
  φ(y; m, s) := (2πs)^{−1/2}exp(−(y − m)²/(2s)). Both integrate to 1 against λ_ν (Tonelli: integrate y first).
- d_H²(f, g) := 1 − ∫√(fg) dλ_ν (independent of the dominating measure; we fix λ_ν). For one-dimensional normals,
  H²(N(m₁, s₁), N(m₂, s₂)) := 1 − ∫√(φ(y; m₁, s₁)φ(y; m₂, s₂)) dy.
- Δ(x) := (â + xᵀb) − (α* + xᵀβ*), x ∈ ℝ^{p_raw}; Δ_i := Δ(x_i).

E_x denotes integration in x against ν_x, with (S, θ, v) and the data held fixed (x is a new point, independent of
the data); for fixed data Δ is an affine, hence Borel, function of x.

## H.1 Statement

**Lemma H.** For every data set, every set S of retained columns, every θ ∈ ℝ^S and every v > 0:
  (H-pop)  d_H²(f_{S,θ,v}, f*) ≤ (v/σ*² − 1)² + E_x[min{1, Δ(x)²/(4σ*²)}]  ≤ (v/σ*² − 1)² + E_x[Δ(x)²]/(4σ*²)
(the last expression may be +∞).
**In-sample identity.** For the same objects, whether or not some columns of supp β* are dropped,
  (H-id)   Δ = ε̄1 + (μ̂ − μ) ∈ ℝⁿ,  1ᵀ(μ̂ − μ) = 0,  n⁻¹Σ_{i=1}^n Δ_i² = ε̄² + ‖μ̂ − μ‖²/n,
and ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖ in contrast coordinates (X_{c,S} := UᵀX_S, μ_c := Uᵀμ).
**In-sample Hellinger bound (corollary).**
  (H-in)   n⁻¹Σ_i H²(N(â + x_iᵀb, v), N(α* + x_iᵀβ*, σ*²)) ≤ (v/σ*² − 1)² + (ε̄² + ‖μ̂ − μ‖²/n)/(4σ*²).

## H.2 Step 1: the Hellinger affinity of two normals

**Claim 1.** For m₁, m₂ ∈ ℝ and s₁, s₂ > 0:
  ∫√(φ(y; m₁, s₁)φ(y; m₂, s₂)) dy = A·B,  A := (2√(s₁s₂)/(s₁ + s₂))^{1/2},  B := exp(−(m₁ − m₂)²/(4(s₁ + s₂))).
*Proof.* √(φ₁φ₂) = (2π)^{−1/2}(s₁s₂)^{−1/4}exp(−α(y − m₁)² − β(y − m₂)²) with α := 1/(4s₁), β := 1/(4s₂). For all y,
α(y − m₁)² + β(y − m₂)² = (α + β)(y − m̄)² + (αβ/(α + β))(m₁ − m₂)², m̄ := (αm₁ + βm₂)/(α + β) (expand both sides:
the y², y and constant coefficients agree; for the constant: αm₁² + βm₂² − (αm₁ + βm₂)²/(α + β) = αβ(m₁ − m₂)²/(α + β)).
Here α + β = (s₁ + s₂)/(4s₁s₂) and αβ/(α + β) = 1/(4(s₁ + s₂)). Since ∫exp(−(α + β)(y − m̄)²) dy = (π/(α + β))^{1/2}
= (4πs₁s₂/(s₁ + s₂))^{1/2}, the integral equals (2π)^{−1/2}(s₁s₂)^{−1/4}(4πs₁s₂/(s₁ + s₂))^{1/2}·B
= (2(s₁s₂)^{1/2}/(s₁ + s₂))^{1/2}·B = A·B. ∎

## H.3 Step 2: the joint distance is the ν_x-average of the conditional distance

**Claim 2.** d_H²(f_{S,θ,v}, f*) = E_x[H²(N(â + xᵀb, v), N(α* + xᵀβ*, σ*²))] = E_x[1 − A·B(x)], with
A := (2√(vσ*²)/(v + σ*²))^{1/2} and B(x) := exp(−Δ(x)²/(4(v + σ*²))).
*Proof.* (x, y) ↦ √(f_{S,θ,v}f*) is non-negative and Borel. By Tonelli,
∫√(f_{S,θ,v}f*) dλ_ν = ∫ν_x(dx) ∫√(φ(y; â + xᵀb, v)φ(y; α* + xᵀβ*, σ*²)) dy = ∫ν_x(dx) A·B(x) by Claim 1 with
m₁ − m₂ = Δ(x). Since ν_x is a probability measure, 1 − ∫A·B dν_x = ∫(1 − A·B) dν_x. ∎

## H.4 Step 3: the pointwise bound

Put r := v/σ*² > 0. Fix x. Then A ∈ (0, 1] and B(x) ∈ (0, 1]: A ≤ 1 because 2√(vσ*²) ≤ v + σ*² (AM–GM), and
B(x) ≤ 1 because its exponent is ≤ 0.
(a) 1 − A·B = (1 − A) + (1 − B) − (1 − A)(1 − B) ≤ (1 − A) + (1 − B), because (1 − A)(1 − B) ≥ 0. [identity: expand.]
(b) Since 0 < A ≤ 1, A ≥ A², so 1 − A ≤ 1 − A² = (v + σ*² − 2√(vσ*²))/(v + σ*²) = (√v − σ*)²/(v + σ*²)
   = (√r − 1)²/(r + 1) ≤ (√r − 1)² = (r − 1)²/(√r + 1)² ≤ (r − 1)²,
   using (√r − 1)(√r + 1) = r − 1, r + 1 ≥ 1 and (√r + 1)² ≥ 1.
(c) For z ≥ 0, 1 − e^{−z} ≤ min{1, z} (1 − e^{−z} ≤ 1 trivially; 1 − e^{−z} ≤ z since e^{−z} ≥ 1 − z). With
   z = Δ(x)²/(4(v + σ*²)) ≤ Δ(x)²/(4σ*²) (as v > 0) and min{1, ·} non-decreasing:
   1 − B(x) ≤ min{1, Δ(x)²/(4(v + σ*²))} ≤ min{1, Δ(x)²/(4σ*²)}.
Hence, for every x:  H²(N(â + xᵀb, v), N(α* + xᵀβ*, σ*²)) ≤ (r − 1)² + min{1, Δ(x)²/(4σ*²)}.   (H.1)

## H.5 Proof of (H-pop)

Integrate (H.1) against ν_x (both sides are non-negative Borel functions of x; the first term is constant) and use
Claim 2: d_H²(f_{S,θ,v}, f*) ≤ (r − 1)² + E_x[min{1, Δ(x)²/(4σ*²)}]. The second inequality of (H-pop) follows from
min{1, z} ≤ z for z ≥ 0 and monotonicity of the integral. ∎

## H.6 Proof of (H-id) (dropped true columns allowed)

(i) *μ and μ̂ in raw terms.* For a dropped column, Cx^r_j = 0; for a retained one, Cx^r_j = ŝ_jx_j. Hence
  μ = CX^rβ* = Σ_{j ≤ p_raw} β*_j Cx^r_j = Σ_{j retained} ŝ_jβ*_j x_j = Xθ*,
so a dropped column of supp β* contributes 0 to μ (whatever β*_j is). Likewise, since b vanishes off S and S consists
of retained columns,
  CX^rb = Σ_{j∈S} b_j Cx^r_j = Σ_{j∈S} (θ_j/ŝ_j)ŝ_jx_j = X_Sθ = μ̂.
(ii) *Δ_i.* ȳ^r = α* + x̄ᵀβ* + ε̄ (average the model equation over i). Therefore
  Δ_i = ȳ^r − x̄ᵀb + x_iᵀb − α* − x_iᵀβ* = ε̄ + (x_i − x̄)ᵀb − (x_i − x̄)ᵀβ*.
Since the vector ((x_i − x̄)ᵀc)_{i≤n} equals CX^rc for every c ∈ ℝ^{p_raw}, Δ = ε̄1 + CX^rb − CX^rβ* = ε̄1 + μ̂ − μ by (i).
This uses the raw coordinates of *all* columns, dropped ones included; on a dropped column (x_i − x̄)_j = 0 for every i,
which is exactly why such a column disappears from the in-sample residual but not from Δ(x) at a new x.
(iii) *Orthogonality.* μ̂ − μ = C(X^rb − X^rβ*) and 1ᵀC = 0, so 1ᵀ(μ̂ − μ) = 0. Hence
  Σ_iΔ_i² = ‖ε̄1‖² + 2ε̄·1ᵀ(μ̂ − μ) + ‖μ̂ − μ‖² = nε̄² + ‖μ̂ − μ‖²;
divide by n.
(iv) *Contrast coordinates.* U ∈ ℝ^{n×N}, UᵀU = I_N, UUᵀ = C. The columns of X_S and μ lie in 1^⊥ = range C, so
UX_{c,S} = UUᵀX_S = CX_S = X_S and Uμ_c = Cμ = μ; thus μ̂ − μ = U(X_{c,S}θ − μ_c) and ‖Uz‖² = zᵀUᵀUz = ‖z‖². ∎

Remark (only the definitions of x_j and b_j matter). Step (i) uses only x_j = Cx^r_j/ŝ_j and b_j = θ_j/ŝ_j with the same
ŝ_j > 0; the normalisation of ŝ_j (n − 1 or n) is irrelevant to (H-id).

## H.7 Proof of (H-in)

Apply (H.1) at x = x_i for each i (H.1 is a pointwise statement, valid at every point of ℝ^{p_raw}), average over i,
and use min{1, z} ≤ z and (H-id):
n⁻¹Σ_iH²(…) ≤ (r − 1)² + n⁻¹Σ_iΔ_i²/(4σ*²) = (r − 1)² + (ε̄² + ‖μ̂ − μ‖²/n)/(4σ*²). ∎
(This is D0 of [D] with the intercept term of [D] D4.0 included; it is not used by DIST-1/2/3, which use (H-pop).)

## H.8 Remarks for the users of Lemma H

1. **No condition on ν_x.** Lemma H holds for every law ν_x; E_xΔ² may be infinite, in which case only the truncated
   form is informative. The truncated term is exactly the quantity Lemma T controls with g = min{1, (a + uᵀx)²/c},
   a := â − α*, u := b − β*, c := 4σ*² (Δ(x) = a + uᵀx; supp u ⊆ S ∪ supp β*).
2. **Supports.** Δ(x) depends on x only through x_{S ∪ supp β*}; with S ⊆ retained columns and supp β* possibly
   containing dropped columns, |supp(b − β*)| ≤ |S| + s₀^r. This is the support size fed to Lemma T (raw dimension p_raw).
3. **Constants.** No constant depends on anything; (b) could be sharpened to (r − 1)²/((√r + 1)²(r + 1)), not needed.
