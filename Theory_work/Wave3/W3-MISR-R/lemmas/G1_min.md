# G1 — Corollary G-min (W3-MISR-R:CorG-min)

Status (verbatim source for the registry):
- CorG-min: **PROVED (by this seat, unchecked)**
(The pointer "Hence BASE MIS-R (ii) applies" in STATEMENT §2(a) is an application of W3-MISR:MIS(ii), which keeps its
own status; the content of CorG-min is (GR^c | σ(X^r_𝒞)) and clauses (b)–(e).)

Statement: `../STATEMENT.md` §2 (v1.2). Notation: `../STATEMENT.md` §1; BASE = `Theory_work/Wave3/W3-MISR/`.
Write X := X^r_𝒞, Z := Uᵀ(X^r_𝓜β_𝓜 − Xγ(X)) ∈ ℝ^N (a Borel function of (X, X^r_𝓜)), N = n − 1, and N_k(m, 0) := δ_m.
Standard facts used: (F1) ℝ^k is Polish, so every random vector Z has a regular conditional law K(X, ·) given X, and
E[h(X, Z) | X] = ∫ h(X, z) K(X, dz) a.s. for every bounded Borel h (disintegration; Kallenberg, *Foundations of Modern
Probability*, 2nd ed., Thm 6.3–6.4). (F2) A probability on ℝ^k is determined by its characteristic function, and a
characteristic function is continuous with modulus ≤ 1. (F3) Cramér's decomposition theorem (STATEMENT §7).

## G1.0 Two preliminaries

**(P1) Conditional convolution.** Let ε be independent of (X, X^r_𝓜), with law L on ℝⁿ, and let L_U be the law of Uᵀε.
Let K be a regular conditional law of Z given X. Then for every bounded Borel h on ℝ^{n×p} × ℝ^N,
  E[h(X, Z + Uᵀε) | X] = ∫∫ h(X, z + e) K(X, dz) L_U(de)   a.s.
*Proof.* (X, Z) is a Borel function of (X, X^r_𝓜), so Uᵀε is independent of (X, Z). Hence
E[h(X, Z + Uᵀε) | X, Z] = h̃(X, Z) with h̃(x, z) := ∫ h(x, z + e) L_U(de), a bounded Borel function (Tonelli). Take
E[· | X] and apply (F1) to h̃. ∎
Under (N), L_U = N_N(0, σ²UᵀU) = N_N(0, σ²I_N).
**(P2) Under (OV^c)** the convention of STATEMENT §1 says K(X, ·) = N_N(0, τ²(X)I_N) a.s. may be taken as the kernel in (P1).

## G1.1 Proof of (a) (sufficiency)

y^r − Xβ^𝒞(X) = α1 + X^r_𝓜β_𝓜 − Xγ(X) + ε, and Uᵀ1 = 0, so Uᵀ(y^r − Xβ^𝒞(X)) = Z + Uᵀε (whatever α is). Put
σ_𝒞(x) := (σ² + τ²(x))^{1/2} > 0 (Borel) and W := (Z + Uᵀε)/σ_𝒞(X). For bounded Borel g on ℝ^{n×p} and f on ℝ^N,
(P1), (P2) with h(x, u) := g(x)f(u/σ_𝒞(x)) give, a.s.,
  E[g(X)f(W) | X] = g(X)∫∫ f((z + e)/σ_𝒞(X)) N_N(0, τ²(X)I)(dz) N_N(0, σ²I)(de) = g(X)∫ f dN_N(0, I),
because N_N(0, τ²I) ∗ N_N(0, σ²I) = N_N(0, σ_𝒞²I) and its image under u ↦ u/σ_𝒞 is N_N(0, I). Taking expectations,
E[g(X)f(W)] = E[g(X)]·∫ f dN_N(0, I) for all such g, f: W is independent of σ(X) and W ~ N_N(0, I_N).
The map x ↦ (x, β_𝒞 + γ(x), σ² + τ²(x)) is Borel from 𝔛_n(p) into the configuration space (stratum p; BASE `STATEMENT.md:28-31`),
so κ_n is σ(X)-measurable (the null event {X ∉ 𝔛_n(p)} is handled as in BASE `lemmas/G_corollaries.md:32-34`). The
normalised contrast residual W_n of BASE `STATEMENT.md:147`, formed with the components of κ_n, equals W off that null
event; so W_n is independent of σ(X) with law N_N(0, I_N): this is (GR^c | σ(X^r_𝒞)). ∎

## G1.2 Proof of (b)

(i) If, conditionally on X, X^r_𝓜β_𝓜 ~ N_n(a(X)1 + Xγ(X), τ²(X)I_n), then Z = Uᵀ(X^r_𝓜β_𝓜 − a(X)1 − Xγ(X)) (Uᵀ1 = 0) is
the image of that conditional law under the X-measurable affine map w ↦ Uᵀ(w − a(X)1 − Xγ(X)); the image of
N_n(a1 + xγ, τ²I_n) under it is N_N(0, τ²UᵀU) = N_N(0, τ²I_N). In the form of STATEMENT §1: for bounded Borel h,
E[h(X, Z) | X] = E[h̄(X, X^r_𝓜β_𝓜) | X] with h̄(x, w) := h(x, Uᵀ(w − a(x)1 − xγ(x))), and the (OV) convention gives the
integral against N_n(a(X)1 + Xγ(X), τ²(X)I_n), which equals ∫ h(X, z) N_N(0, τ²(X)I_N)(dz). So (OV^c) holds.
(ii) With α = α(X): y^r = α(X)1 + Xβ_𝒞 + V + ε, V := X^r_𝓜β_𝓜. (P1) applied with Z replaced by V (a Borel function of
(X, X^r_𝓜)) and U replaced by I_n gives the conditional law of V + ε given X as N_n(a(X)1 + Xγ(X), τ²(X)I) ∗ N_n(0, σ²I) =
N_n(a(X)1 + Xγ(X), σ_𝒞²(X)I); adding the X-measurable vector α(X)1 + Xβ_𝒞 gives the stated law. ∎

## G1.3 Proof of (c) (necessity under (N))

Let W_n := Uᵀ(y^r − X(β_𝒞 + γ(X)))/√v(X) = (Z + Uᵀε)/√v(X) (off the null event), independent of σ(X), N_N(0, I).
For t ∈ ℝ^N, by independence ("freezing": E[F(X, W_n) | X] = ∫ F(X, w) N(0, I)(dw) for bounded Borel F, as in BASE
`lemmas/M_misr.md:143-145`) with F(x, w) := exp(i√v(x) tᵀw):
  E[e^{itᵀ(Z + Uᵀε)} | X] = e^{−v(X)‖t‖²/2}   a.s.
By (P1) with h(x, u) := e^{itᵀu} (real and imaginary parts) and L_U = N_N(0, σ²I):
  E[e^{itᵀ(Z + Uᵀε)} | X] = φ(X, t)e^{−σ²‖t‖²/2},  φ(x, t) := ∫ e^{itᵀz} K(x, dz).
So φ(X, t) = e^{−(v(X) − σ²)‖t‖²/2} a.s. for each t; on one event of probability one this holds for all t ∈ ℚ^N, and
both sides are continuous in t (F2), hence for all t ∈ ℝ^N. On that event |φ| ≤ 1 at any t ≠ 0 forces v(X) ≥ σ², and
then φ(X, ·) is the characteristic function of N_N(0, (v(X) − σ²)I_N), so K(X, ·) = N_N(0, (v(X) − σ²)I_N) a.s. (F2).
With τ²(x) := (v(x) − σ²)₊ (Borel), τ²(X) = v(X) − σ² a.s., and by (F1) E[h(X, Z) | X] = ∫ h(X, z) N_N(0, τ²(X)I)(dz)
a.s.: (OV^c) holds; σ² + τ²(x) = max(v(x), σ²) > 0 for every x since v > 0. Conversely (a) gives (GR^c | σ(X)) at
(X, β_𝒞 + γ(X), σ² + τ²(X)), whose last component equals v(X) a.s. Hence the equivalence. ∎

## G1.4 Proof of (d) (Cramér partial converse)

Now ε is independent of (X, X^r_𝓜) with an arbitrary law; L_U := law of Uᵀε. As in G1.3, the conditional law of
Z + Uᵀε given X is N_N(0, v(X)I) a.s.; by (P1) it is also K(X, ·) ∗ L_U. So there is a Borel set 𝔅 with P(X ∈ 𝔅) = 1
and K(x, ·) ∗ L_U = N_N(0, v(x)I) for x ∈ 𝔅. Fix x ∈ 𝔅 and t ∈ ℝ^N. The images under u ↦ tᵀu satisfy
(K(x, ·)∘(tᵀ)⁻¹) ∗ (L_U∘(tᵀ)⁻¹) = N(0, v(x)‖t‖²): the sum of two independent real random variables is Gaussian, so by
Cramér's theorem (F3) L_U∘(tᵀ)⁻¹ is Gaussian (possibly degenerate). All one-dimensional projections of L_U are Gaussian,
so L_U = N_N(b, Σ_ε) with b ∈ ℝ^N, Σ_ε ⪰ 0 (Cramér–Wold; the mean and covariance exist since every projection has finite
second moment; deterministic since L_U does not involve x). Then for x ∈ 𝔅 and all t,
  φ(x, t) = e^{−v(x)‖t‖²/2}·e^{−itᵀb + tᵀΣ_εt/2} = e^{−itᵀb − ½tᵀ(v(x)I − Σ_ε)t}.
|φ(x, t)| ≤ 1 for all t gives tᵀ(v(x)I − Σ_ε)t ≥ 0, i.e. v(x)I ⪰ Σ_ε; then φ(x, ·) is the characteristic function of
N_N(−b, v(x)I − Σ_ε), and K(x, ·) is that law (F2). With (F1) this is the conditional-law statement. ∎

## G1.5 Proof of (e)

**(E1).** Joint law N(m, Σ) of a row (x_𝒞, x_𝓜), Σ ⪰ 0. If w ∈ ker Σ_𝒞𝒞 then Var(wᵀx_𝒞) = 0, so
Cov(wᵀx_𝒞, x_𝓜) = Σ_𝓜𝒞w = 0: ker Σ_𝒞𝒞 ⊆ ker Σ_𝓜𝒞, hence range Σ_𝒞𝓜 ⊆ (ker Σ_𝒞𝒞)^⊥ = range Σ_𝒞𝒞 and
Σ_𝒞𝒞Σ_𝒞𝒞⁺Σ_𝒞𝓜 = Σ_𝒞𝓜 (Σ_𝒞𝒞Σ_𝒞𝒞⁺ is the orthogonal projection onto range Σ_𝒞𝒞; Σ_𝒞𝒞⁺ is symmetric). Put
ζ := x_𝓜 − m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁺(x_𝒞 − m_𝒞). Then Cov(ζ, x_𝒞) = Σ_𝓜𝒞 − Σ_𝓜𝒞Σ_𝒞𝒞⁺Σ_𝒞𝒞 = (Σ_𝒞𝓜 − Σ_𝒞𝒞Σ_𝒞𝒞⁺Σ_𝒞𝓜)ᵀ = 0, and
(ζ, x_𝒞) is jointly Gaussian, so ζ is independent of x_𝒞; Cov(ζ) = Σ_𝓜𝓜 − 2Σ_𝓜𝒞Σ⁺Σ_𝒞𝓜 + Σ_𝓜𝒞Σ⁺Σ_𝒞𝒞Σ⁺Σ_𝒞𝓜 =
Σ_𝓜𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁺Σ_𝒞𝓜 (Σ⁺Σ_𝒞𝒞Σ⁺ = Σ⁺). Rows are iid, so the n × q matrix of the ζ_i is independent of X, with iid rows;
x_{𝓜,i}ᵀβ_𝓜 = a + x_{𝒞,i}ᵀγ + ζ_iᵀβ_𝓜 with the stated a, γ, and ζ_iᵀβ_𝓜 iid N(0, τ²), τ² as stated. So
X^r_𝓜β_𝓜 = a1 + Xγ + ξ with ξ ~ N_n(0, τ²I_n) independent of X: (OV) with constant (a, γ, τ²) (the conditional law is
the law of ξ shifted by a1 + Xγ). Each candidate column has iid N(m_j, Σ_jj) entries with Σ_jj > 0, so for n ≥ 2 it is
non-constant a.s.: P(X ∈ 𝔛_n(p)) = 1. (N) is the noise assumption of the setting (ε independent of all rows). If
Σ_𝒞𝒞 ≻ 0 then Σ_𝒞𝒞⁺ = Σ_𝒞𝒞⁻¹ and (γ, a, τ²) are those of BASE `lemmas/G_corollaries.md:28-29`, so β^𝒞 and σ²_𝒞 are BASE's
(`STATEMENT.md:166`). ∎
**(E2).** X^r_𝓜β_𝓜 = (m′ᵀβ_𝓜)1 + X(Γβ_𝓜) + Zβ_𝓜 with Zβ_𝓜 ~ N_n(0, β_𝓜ᵀΣ_Zβ_𝓜·I_n) independent of X: (OV). ∎
**(E3).** For deterministic X ≡ x ∈ 𝔛_n(p), σ(X) is trivial; (a) says Uᵀ(y^r − x(β_𝒞 + γ(x)))/σ_𝒞(x) ~ N_N(0, I), i.e.
BASE's (GR^c) (`STATEMENT.md:36-37`) at (x, β_𝒞 + γ(x), σ² + τ²(x)). ∎
**Remark (STATEMENT §2).** UᵀX^r_𝓜β_𝓜 = Z + UᵀXγ(X); under (OV^c) the regular conditional law of Z given X = x has
mean 0, so that of UᵀX^r_𝓜β_𝓜 has mean Uᵀxγ(x).
