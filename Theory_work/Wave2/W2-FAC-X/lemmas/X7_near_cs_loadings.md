# X7 — Target 2, first result: one-factor designs with polynomially vanishing loading dispersion (Corollary FAC-NCS)

Status: **PROVED (by this seat, unchecked)** for iid rows (R); lemma check R12: (R) VERIFIED-WITH-AMENDMENTS (applied), (G) FAILED as
written → withdrawn (STATEMENT_T2 v2.1); not part of locked STATEMENT v3; supports Corollary FAC-NCS in the separately locked STATEMENT_T2.md v2.1 — iid rows (R)
only (R16 item 4). Falsification numerics: numerics/N2X_summary.md (fixed-dispersion loadings, 64/64 paths fine — the
present corollary covers only vanishing dispersion).

## Setting

Σ_n = Υ_nΣ⁰_nΥ_n, Σ⁰_n = λλᵀ + diag(1 − λ_j²) (unit diagonal), λ = λ^{(n)} ∈ (0, 1)^p with
  Δ_n := max_j |λ_j − λ̄| with **(NCS) Δ_nH̄_n ≤ n^{−1/3}**, for a fixed λ̄ ∈ (0, 1)
(narrowed after R10 item 3: with only Δ_n ≤ n^{−c₂}, small c₂, the enlarged scale ϖ′ can make X4's regime-(S) spacing event
D8(S) fail with probability → 1 — e.g. p = n^{0.004}, Δ_n = n^{−0.001} — and D7's exponent and B3 Case B's bound change).
ρ := λ̄², ℓ̄ := λ̄/√(1 − λ̄²), ℓ_j := λ_j/√(1 − λ_j²) (so |ℓ_j − ℓ̄| ≤ C_λΔ_n), ψ_j := 1 − λ_j². Hypotheses (P-½), (θ),
(FS) (with this ρ) as in STATEMENT v3; s₀ ≥ 1. Two designs:
* **(R) iid rows** with covariance Σ_n (model R of STATEMENT v3 §1);
* **(G) exact Gram** XᵀX = (n − 1)Σ_n (model G of FACB STATEMENT §1).

**Corollary FAC-NCS (iid rows (R) only — STATEMENT_T2 v2.1).** Claims (C1)–(C4) of STATEMENT v3 hold for (R), with
ϖ_n replaced by ϖ′_n := (1 + C₇)ϖ_n (C₇ = C₇(λ̄)). **(G) is withdrawn from this corollary (R12 item 1):** the transfer
below used X4's iid multiplier bound M_T ≤ ½(1 + C/n), which is false for exact Gram (√n(2M_T − 1) ⇒ N(0, 2) even at
Δ = 0), and did not replace X1.4's ε^d/(g5) terms and X4.6's q-based projection bound. R12 supplies a repair route
(|M_T − ½| ≤ C(n^{−1/3} + pH̄²/n), ε^d ≡ 0, M_Tψ_T independent of T, ‖P_Ue‖² = σ²Φ(U)); not carried out here — the (G)
paragraphs below are retained only as notes. Under (NCS), C₇′H̄_nΔ_n ≤ C₇′n^{−1/3} ≤ C₇′ϖ_n, so
the perturbation bound below is of **exactly Target 1's form** C·H̄√(p log n/n) + C·n^{−1/3}: every event and every rate
condition of X4 (D6–D8 with their exponents c_w, T₀; the regime-(S) spacing; B3 Case B's pw² + w log n = o(1); the band
absorption) is stated for scales of this form and holds with the constant C₀ replaced by (1 + C₇)C₀ and the floor n^{−1/3}
by (1 + C₇)n^{−1/3} — only constants change (R10 item 3).

## Proof (modifications of X1–X6)

**Representation.** (R): g_j := Cx^r_{·j} = λ_jf + √ψ_j u_j (centred columns, f = CF, u_j = CU_{·j} as in X1.1; R16 item 2); with the same frame (e₁, e₂) as X1.1,
g_j = (λ_jη + √ψ_jξ_j)e₁ + (λ_jφ + √ψ_ja_j)e₂ + √ψ_ju_j^⊥, and G^r_T = Ψ_T^{1/2}[ṽ1ṽ1ᵀ + ṽ2ṽ2ᵀ + W_T]Ψ_T^{1/2} with
ṽ1_j := ξ_j + ℓ_jη, ṽ2_j := ℓ_jφ + a_j. Column scalings do not change spans, so X1.2 holds verbatim (q_T, ω_j with
these ṽ1, ṽ2). (G): with g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ_n) = λη + Ψ^{1/2}ξ, RSS_T = ‖e‖² − σ²g_TᵀΣ_TT⁻¹g_T (FACB
L1.5(b)) and, whitening, g_TᵀΣ_TT⁻¹g_T = ṽ1_Tᵀ(I + ℓ_Tℓ_Tᵀ)⁻¹ṽ1_T; the deletion statistic is
RSS_{T∖j} − RSS_T = σ²ω_j(T)², ω_j := ((I + ℓℓᵀ)⁻¹ṽ1)_j/√(((I + ℓℓᵀ)⁻¹)_jj) — the structure of X1.2 with
"A_T/N" replaced by I + ℓ_Tℓ_Tᵀ and without the (1 + q) factors. X1.4's gain formulas hold for (G) with
M_T := ν(n/(n + 1))σ²/(s²ψ_T) (the (1 + q)-factors equal 1) and the same absolute ridge/determinant errors (they use
only λ_min(G_T) ≥ c₀(n − 1), here c₀ := min_j ψ_j/2 ≥ (1 − λ̄²)/3 eventually).

**Reference and perturbation.** Use the CS reference with ℓ̄: x_T := (Σ_Tξ − ϱ)/(k + κ), κ := N/(ℓ̄²φ²),
ϱ := Nη/(ℓ̄φ²) for (R) (κ := 1/ℓ̄², ϱ := η/ℓ̄ for (G)), with the exact drift identity. Write ṽ1 = ξ + ℓ̄η1 + (ℓ − ℓ̄)η and
ṽ2 = ℓ̄φ1 + α̃√N with α̃ := (a + (ℓ − ℓ̄)φ)/√N (for (G): b := ℓ, b⁰ := ℓ̄1, α̃ := ℓ − ℓ̄, R := 0). Then the proof of
Proposition X2 goes through with ‖α‖_∞ ≤ 2√(log n/N) replaced by ‖α̃‖_∞ ≤ τ_n := 2√(log n/N) + 2C_λΔ_n, and with one new
term from ṽ1's extra part u := (ℓ − ℓ̄)η: its contribution to c is u − b(bᵀu)/(1 + ‖b‖²), of sup-norm ≤ 3‖u‖_∞ ≤
3C_λΔ_n|η| ≤ 3C_λΔ_nH̄. Steps (i) and (v) give |c_j − c⁰_j| ≤ Cτ_n(H̄ + |x_T|) + 3C_λΔ_nH̄ and a normalisation error
O(r_n + τ_n); step (iv)'s term ‖R‖‖c − c⁰‖ ≤ r_n√k·C(τ_n + Δ_n)(H̄ + |x_T|) ≤ C(p/√n + √(p log n/n))(√(log n/n) + Δ_n)H̄ (R12 item 2:
r_n's log term retained), which is ≤ CΔ_nH̄ + C√(p log n/n)H̄ for p ≤ √n (also for bounded p). Hence, on 𝔈_n (with D3 for a; D4; and for (G) all W-terms absent),
  |δ_j(T)| ≤ C_X(H̄ + |x_T|)[√(p log n/n) + (#Band + 17)√(log n/n)] + C₇′Δ_nH̄   (R),
  |δ_j(T)| ≤ C₇′Δ_n(H̄ + |x_T|) + C n^{−1}H̄                                         (G).

**Path (X3, X4).** X3 is deterministic and uses only (R_ϖ′) and the drift identity of the reference centre. X4 is
re-run with ϖ′_n = (1 + C₇)ϖ_n, a scale of Target 1's form (see above), so its events D6–D8 (regime-(S) spacing:
P ≤ p²c₁ϖ′ ≤ n^{1/100}(1 + C₇)c₁ϖ_n → 0; D7: ϖ′ ≤ n^{−(½−A₁)/2+o(1)} as before), B3 Case B and the band absorption hold
with changed constants; Corollary X4.1's budget max|δ| ≤ ¾ϖ′ holds by choosing C₇ ≥ 2C₇′ (the Δ-term of δ is
≤ C₇′n^{−1/3} under (NCS)). The constants c₁ = 9 + 8/κ_∞, c_D, K₁, m₁ use
κ_∞ := (1 − ρ)/ρ = 1/ℓ̄² (κ = κ_∞(1 + O(n^{−1/3}))). The truth-move bound X4.6 uses λ_min(G^r_U) ≥ min_jψ_j·N/2. The
crude bulk addition bound (A₁ < ½) is unchanged. So Lemma X4 holds with ϖ′.

**Start mode (X5).** The population partial covariance c_n(U, l) under Σ⁰_n is a Lipschitz function of the ≤ (16 + s₀)²
entries of Σ⁰_V: diagonal entries equal 1 in both matrices, off-diagonal ones satisfy |λ_jλ_k − λ̄²| ≤ 2Δ_n (R16 item 3), so |c_n(U, l) − c(U, l)| ≤ CΔ_n → 0 and the
nonzero CS values (FS) stay ≥ c_FS/2; zero pairs are exactly zero. For (R) add Lemma CR's sample deviation (X5.1);
for (G) R̂ = Σ_n exactly and the noise part is as in FACB L2.2. The rest of X5 is unchanged.

**Assembly (X6).** (H0): λ_min(Σ_n) ≥ min_jψ_j ≥ (1 − λ̄²)/2 eventually; energy and BM-∞ as before. (R): X6 verbatim;
(G): FACB L5 verbatim (fixed design). ∎

**Remarks.** (1) For (G) the exponent restriction A₁ < ½ enters only through the crude bulk addition bound of X4.4; for
exact CS, FACB's finer bulk analysis gives p ≤ n/2 — extending it to vanishing dispersion is plausible but not done.
(2) For fixed dispersion (Δ_n ↛ 0) the extra term (ℓ_j − ℓ̄)X_T in the statistic is of order Δ·|X_T|, and the proof's
centre bound only gives |X_T| ≤ ε_bH; the resulting "band" has width ≍ Δε_bH, so D7's window count is a fixed fraction
of the kept tail and the balance argument (B3) fails: this is the obstruction of the technique (the method itself
behaves in N2X).
