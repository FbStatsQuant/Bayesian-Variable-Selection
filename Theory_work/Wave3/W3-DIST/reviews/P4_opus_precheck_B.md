# W3-DIST — Pre-check P4, stream B: Lemma H, Lemma T, Theorem DIST-3

Checker: Claude Opus 5.5 (Claude Third), effort high, same-family independent line check. Read-only except this file.
Rules: `briefs/PRECHECK_COMMON.md`; brief: `briefs/BRIEF_P4_B_precheck.md`. Targets: STATEMENT.md v1.3.1 §3 Lemma H
(l. 291–295), Lemma T (l. 297–308), §1 Theorem DIST-3 (l. 93–104) with API_CARDS "Common definitions".
Files checked line by line: `work/B_transfer/H.md`, `T.md`, `DIST3.md`. Also read: `check_H.py`/`_out`, `check_T.py`/`_out`,
`check_DIST3.py` (first 40 lines)/`_out`, `W3-POST2/lemmas/D_hellinger.md` D0, D1, D4.0, ROUTES.md §2 Step 2 and §3,
comparison attempts `work/api_attempts/dist1/T-a-1.md`, `T-b-1.md`, `T-c-1.md`.
Not read (per the rules): `reviews/` (other files), `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*`.
Recomputations were done by hand, with a short Python evaluation of the numerical constants (values quoted below).
I did not re-run the Monte Carlo scripts.

---

## 1. Lemma H (`H.md`)

**Claim 1 (affinity of two normals).** Recomputed: √(φ₁φ₂) = (2π)^{−1/2}(s₁s₂)^{−1/4}exp(−α(y−m₁)² − β(y−m₂)²), α = 1/(4s₁),
β = 1/(4s₂); completing the square gives α+β = (s₁+s₂)/(4s₁s₂), αβ/(α+β) = 1/(4(s₁+s₂)); the Gaussian integral
(4πs₁s₂/(s₁+s₂))^{1/2} times the prefactor is √2(s₁s₂)^{1/4}(s₁+s₂)^{−1/2} = A. Correct.

**Claim 2 (joint = ν_x-average).** Tonelli on a non-negative Borel integrand with respect to ν_x ⊗ Leb; ν_x is a probability
measure. Correct. This matches STATEMENT §0 "Distance" (shared x-marginal).

**Step 3.** (a) 1 − AB = (1−A) + (1−B) − (1−A)(1−B) with A, B ∈ (0, 1]. Correct. (b) 1 − A ≤ 1 − A² =
(√v − σ*)²/(v + σ*²) = (√r − 1)²/(r + 1) ≤ (√r − 1)² = (r − 1)²/(√r + 1)² ≤ (r − 1)². Correct for every r > 0.
(c) 1 − e^{−z} ≤ min{1, z}, and Δ²/(4(v+σ*²)) ≤ Δ²/(4σ*²) because v > 0. Correct. This is (H.1), and integrating it gives
(H-pop), which is exactly the STATEMENT display. The second, untruncated form is a trivial addition.

**(H-id).** ȳ^r = α* + x̄ᵀβ* + ε̄, so Δ_i = ε̄ + (x_i − x̄)ᵀ(b − β*) = ε̄ + (CX^rb)_i − (CX^rβ*)_i. A dropped column has
Cx^r_j = 0, so μ = Xθ* and CX^rb = X_Sθ = μ̂, and 1ᵀ(μ̂ − μ) = 0. The cross term vanishes. The contrast-coordinate
isometry (UX_{c,S} = CX_S = X_S, Uμ_c = μ) is correct. The script's check [3] (dropped true column) agrees to 1e-15.

**(H-in).** (H.1) holds pointwise, so it holds at x = x_i; then use min{1, z} ≤ z and (H-id). Correct. It agrees with [D] D0
plus the D4.0 intercept term, with constant 1/(4σ*²) on both pieces.

**Edge cases.** s₀ = 0 (β* = 0 on retained columns, or all true columns dropped): covered, because (H-id) uses only
μ = CX^rβ*. Arbitrary ν_x: E_xΔ² = ∞ is allowed, and only the truncated form is informative then (Remark 1). Remark 2
gives supp(b − β*) ⊆ S ∪ supp β*, of size ≤ |S| + s₀^r, in raw coordinates. Correct, and it is what Lemma T needs.

No STATEMENT-CHANGE REQUEST. None is needed.

**Verdict, Lemma H: VERIFIED.**

---

## 2. Lemma T (`T.md`)

### 2.1 Elementary tools
- **T1 (Cantelli).** λ = V/t gives (V + V²/t²)/(t + V/t)² = V/(V + t²). Correct.
- **T2 (Hoeffding, Rademacher).** cosh x ≤ e^{x²/2} because (2j)! ≥ 2^j j!. Correct.
- **T3.** (k/m)^kΦ_k(m) ≤ (1 + k/m)^m ≤ e^k for 1 ≤ k ≤ m. Correct.
- **Traces and repetitions.** If z_i = z_j (i ≠ j), the pattern {i} is never realised, so a shattered index set corresponds
  to a shattered set of distinct points. Correct.
- **T4 (Sauer–Shelah).** The induction is checked. The k = −1 base (a non-empty family shatters ∅) and the m = 0 base are
  right. The fibre count |𝒞| = |𝒞₁| + |𝒞₂| is right. 𝒞₂ shattering T implies 𝒞 shattering T ∪ {m}. Pascal's rule
  closes the induction. The k = 0 step uses Φ_{−1} = 0 consistently.
- **T5 (Dudley).** With d+2 points and a (d+1)-dimensional space, some γ ≠ 0 annihilates every evaluation vector. The
  pattern I = {γ_i > 0} then gives a contradiction. Correct, including h ≡ const (∅ or ℝ^d).

### 2.2 Growth function (brief duty 2)
Fix a support T with |T| = d. Then A(a, u, r) = {u_Tᵀy + (a − r) > 0} ∪ {(−u_T)ᵀy + (−a − r) > 0}, because
|t| > r ⟺ t − r > 0 or −t − r > 0. Both pieces are positivity sets of the (d+1)-dimensional space span{1, y_j}. Hence there
are at most Φ_{d+1}(m)² traces per T and C(P, d)Φ_{d+1}(m)² in total. The step Φ_{d+1}(m) ≤ (em/(d+1))^{d+1} needs
m ≥ d + 1, and m = 2n ≥ d + 1 holds because d ≤ n − 1. The step C(P, d) ≤ (eP/d)^d needs 1 ≤ d ≤ P. So S(2n) ≤ e^L with
L = d log(eP/d) + 2(d+1) log(2en/(d+1)), exactly the STATEMENT's bound. Supports of size < d are enlarged with zero
coefficients, which needs d ≤ P. Correct.

**Claim nη² > 36.** On the range: d log(eP/d) ≥ d ≥ 1; 2(d+1) log(2en/(d+1)) ≥ 4 log(2e), because d + 1 ≥ 2 and
n/(d+1) ≥ 1; log(4/δ) > log 4. Hence nη² = 4[L + log(4/δ)] > 4(1 + 4 log 2e + log 4) = **36.636** (recomputed). The claim
is correct and uniform over every admissible (n, P, d, δ). All three bracket terms are ≥ 0 on the range (the S1-01 repair
holds).

### 2.3 Proposition R (brief duty 1): recomputed step by step
*Ghost step.* τ is the first index k with ν(A_k) > 2P_n(A_k) + η². {τ = k} is measurable in the sample. If P(τ = k) > 0
then p_k > η², since P_n ≥ 0 and the inequality is strict. Cantelli with t = np_k/5 gives

  (1 − p)/((1 − p) + np/25) ≤ 1/(1 + np/25) < 1/(1 + nη²/25) ≤ ½ for nη² ≥ 25.

Monotonicity of x/(x + c) and x = 1 − p ≤ 1 are used; the case p = 1 is handled separately. On {τ = k} ∩ {Z_k ≥ 4np_k/5}:
P'_n(A_k) ≥ (4/5)p_k > (4/5)(2P_n(A_k) + η²). Strictness comes from p_k > 2P_n + η², so the ghost event E₂ holds. τ
depends only on the sample and Z_k only on the ghost sample, so the factorisation and P(E₁) ≤ 2P(E₂) are correct.

*Swap step.* After Ψ_σ the first half holds Σ[k_i(1+σ_i)/2 + k'_i(1−σ_i)/2] = (N − W)/2 points of A (checked for
σ_i = ±1), and the second half holds (N + W)/2. The E₂ condition is (N+W)/(2n) > (4/5)((N−W)/n + η²). Multiplying by 10n
gives 5N + 5W > 8N − 8W + 8nη², i.e. 13W > 3N + 8nη². Correct. ‖a‖² = #{k_i ≠ k'_i} ≤ N. By AM–GM,
w² ≥ 4·3N·8nη²/169, so the exponent is w²/(2N) ≥ 96nη²/(2·169) = **48nη²/169 = 0.28402·nη²** ≥ nη²/4 (recomputed).
The event depends on A only through its trace on Ξ, so the union runs over ≤ S̄ traces. Ψ_σ preserves ν^{⊗2n}, and
averaging over σ is a finite sum. Correct.

*Slack (the author's "0.284 against 1/4").* With a general ghost factor ρ in place of 4/5, the swap exponent is
4ρ(2ρ − 1)/(1 + 2ρ)². It is ≥ 1/4 iff 28ρ² − 20ρ − 1 ≥ 0, i.e. ρ ≥ 0.7612 (recomputed). Cantelli needs
(1 − ρ)²nη² ≥ 1, which at ρ = 0.7612 means nη² ≥ 17.54. Lemma T supplies nη² > 36.6. The constant choice therefore has
real margin on both sides: ρ = 4/5 needs 25 and has 36.6, and any ρ ∈ [0.762, 0.834] also works. "Little slack" is a fair
description of the exponent but not of the overall argument. **No defect.**

*Conclusion.* P(E₁) ≤ 2S̄e^{−48nη²/169} ≤ 2S̄e^{−nη²/4}. With S̄ = e^L and η² = (4/n)(L + log(4/δ)), this is
2e^L·e^{−L}·δ/4 = δ/2. Correct.

### 2.4 From sets to the truncated quadratic loss (brief duty 3)
- **Step 2 (real thresholds).** Rational r_k ↓ r gives A(a, u, r_k) ↑ A(a, u, r). Continuity from below of ν and of P_n
  passes the inequality to the limit. Correct. The sets A(a, u, r_k) lie in 𝒜₀ because a, u, r_k are rational and
  |supp u| ≤ d.
- **Step 3 (layer cake).** For s ∈ (0, 1), {min{1, z} > s} = {z > s}, so {g > s} = A(a, u, √(sc)) with √(sc) > 0 real.
  Step 2 covers it for every real c > 0. ∫₀¹ of the right side is 2P_ng + η², by linearity with no Cauchy–Schwarz step.
  Joint measurability of (x, s) ↦ 1{g(x) > s} is fine. Correct.
- **Step 4.** Rational (a_k, u_k) → (a, u) with the support kept inside T; pointwise convergence and domination by 1.
  Correct.
- **Step 5.** Every u with |supp u| ≤ d lies in some T of size d. Correct.
- **Step 6 (measurability).** (a, u, c) ↦ νg − 2P_ng is continuous on each ℝ × ℝ^T × (0, ∞) by dominated convergence.
  There are finitely many T, and the countable dense 𝒬 gives the same supremum. Ω_T is an event. Correct.

Everything happens on the single event E₁ᶜ, so the conclusion holds **simultaneously** in (a, u, c). The lemma is
proved as stated, with failure probability δ/2 ≤ δ.

### 2.5 Appendix T.A (ratio form; not needed)
- Ghost step. q < p − η√p forces √p > η. Cantelli with t = nθη√p gives ≤ 1/(1 + nθ²η²) ≤ ½. h(x) = (x−q)/√(x+q) has
  h′ = (x + 3q)/(2(x+q)^{3/2}) > 0. Also p' − q > (1−θ)η√p and p' + q < 2p, so h(p') > γ. Correct.
- Swap step. W > γ√(nN) and the bound e^{−γ²n/2} = e^{−(1−θ)²nη²/4}. Correct.
- Prefactor-6 route. nθ²η₆² ≥ 6·9.159/49 = 1.12 ≥ 1 and (6/7)²·(3/2) = 54/49 ≥ 1, so the failure probability is ≤ δ/2.
  Cauchy–Schwarz and AM–GM then give νg ≤ 2P_ng + η₆². Correct.

### 2.6 Comparison with T-a-1, T-c-1 (and T-b-1) (brief duty 4)
| | intermediate inequality | external facts | failure prob. | final statement |
|---|---|---|---|---|
| T.md | one-sided multiplicative: P(∃A: ν(A) > 2P_n(A) + η²) ≤ 2S̄e^{−48nη²/169}, nη² ≥ 25 | none (Cantelli, Hoeffding, Sauer–Shelah, Dudley all proved) | δ/2 | STATEMENT exactly |
| T-a-1 | ratio form ≤ 4S(2n)e^{−nη²/4} (Thm RD), then Cauchy–Schwarz | **(BIN)** Greenberg & Mohri (2014), Statist. Probab. Lett. 86, 91–98, Thm 1: P(Bin(m, p) ≥ mp) > 1/4 for p > 1/m; **(SS)** Sauer (1972) | δ | STATEMENT exactly |
| T-c-1 | ratio form ≤ 16S(2n)e^{−nη²/4} for nη² > 36, then Cauchy–Schwarz | (SS) only (proved in T.md T4). Step 0 (P(B ≥ np) ≥ 1/16 for np ≥ 36) is proved in the file | (16/e³)δ = 0.797δ | STATEMENT exactly |
| T-b-1 | Bousquet + peeling | Bousquet (2002) Thm 2.3 / BLM Thm 12.5; (SS) | δ | **different**: 4/n → 240/n (or 192Λ_n + (124/3)log(1/δ)) |

Checks of the comparison material, at the steps the final statement depends on:
- **T-a.** The ghost step is right: F(x, y) = (y − x)/√((x+y)/2) is increasing in y and decreasing in x, and
  F(x₀, p*) = η√p*/√(p* − η√p*/2) > η. The swap exponent η²nΣ_A/(4Σa_i²) ≥ nη²/4 is right. So P(E) ≤ 4S(2n)e^{−nη²/4}
  and the final failure probability δ are right, **conditional on (BIN)**. From memory, (BIN) is the main theorem of
  Greenberg–Mohri with that hypothesis (p > 1/m), but it needs a source check before T-a could be used. Remark 2's
  variant (1 + 2√L′)² ≤ 6L′ for L′ ≥ 7 is right: 1/7 + 4/√7 + 4 = 5.66.
- **T-c.** I recomputed Step 0.
  - Case σ² ≥ 1: EZ⁴ ≤ σ² + 3σ⁴ ≤ 4σ⁴. Hölder with exponents (3/2, 3) gives E|Z| ≥ σ/2, and EZ₊ ≤ σP(Z > 0)^{1/2} then
    gives ≥ 1/16.
  - Case σ² < 1: λ < 36/35 and λ/n < 1/35, so p^n ≥ e^{−18/17} = 0.347.
  - Trace count: N_k(2n) ≤ (2/e)(2en/k)^k uses 2n ≥ 2k, i.e. d ≤ n − 1, and k! ≥ e(k/e)^k. With C(P, d) ≤ e^{−1}(eP/d)^d
    this gives S(2n) ≤ (4/e³)S̄.
  - Hence the failure probability is ≤ 16·(4/e³)·δ/4 = 0.797δ.
  - Correct, and self-contained except for Sauer–Shelah.
- **Agreement.** All three files prove the STATEMENT display with η²_n(d, δ) exactly as written, on the same range
  1 ≤ d ≤ min(P, n − 1). Only the failure probabilities differ: δ/2, δ and 0.797δ, all ≤ δ. The derivations do not
  disagree on any step they share: the growth bound, the Dudley lemma and the layer-cake extensions are identical in
  substance. T-b reaches a weaker constant (240 in place of 4). It is not a counter-indication, only a different route.
- **External facts that would need a citation check.** If T-a is used: Greenberg–Mohri Thm 1 (essential to T-a) and
  Sauer (1972) / van der Vaart–Wellner Cor. 2.6.3 (standard). If T-c is used: only Sauer–Shelah. Anthony & Shawe-Taylor
  (1993) Thm 2.1, quoted in the STATEMENT route text, is **used by none of the three** and does not need checking for
  Lemma T.
- **Preference.** T.md's route is preferable. It is fully self-contained (no external probability fact, and Sauer–Shelah
  is proved). It avoids Cauchy–Schwarz because the multiplicative form is linear under the layer cake. Its constants have
  real margin (§2.3), and its failure probability is the smallest. T-c is a valid independent second proof and could serve
  as a cross-check in the cross-family round. T-a is the closest to the literature, but it rests on (BIN).

### 2.7 STATEMENT-CHANGE REQUESTS / notes in T.md
There is no STATEMENT-CHANGE REQUEST, correctly: the statement is proved as written. The EDITORIAL NOTE asks to replace
the route sentence of STATEMENT §3 (the ratio inequality "4S(2n)e^{−nη²/4} … to be verified", then Cauchy–Schwarz). It is
**justified**. The quoted inequality is not proved in-house: T.md's own ratio form R′ has the weaker exponent
(1−θ)²nη²/4, and T-a proves the quoted form only modulo (BIN). The route text should name the inequality actually used.
The note does not weaken the statement. See finding P4B-02.

**Edge cases.**
- Atoms and heavy tails: only traces and exchangeability enter (Remark 1).
- d = n − 1: the growth bound needs only 2n ≥ d + 1, and the lemma is empty there (η² ≥ 8 log 2e ≈ 13.5 at d + 1 = n).
- P = d: the range allows it.
- Repeated sample points: handled through traces on tuples.
- u = 0: gives ∅ or ℝ^P, which are in the class.

**Verdict, Lemma T: VERIFIED** (editorial amendment P4B-02 to the STATEMENT route text only).

---

## 3. Theorem DIST-3 (`DIST3.md`) (brief duty 5)

### 3.1 Tools
- **G1** (Gaussian tail 2e^{−x²/2}). Correct.
- **G2.** E e^{λξ²/4} = (1 − λ/2)^{−1/2} ≤ √2 for λ ∈ [0, 1]. Correct.
- **G3.** The upper-tail cumulant bound is αλ²/(2(1−λ)) ≤ αλ² for λ ≤ ½. With λ = t/(2α) the exponent is −t²/(4α). For
  the lower tail, λ − log(1+λ) ≤ λ²/2, and λ = t/α gives −t²/(2α). Correct.
- **G4.** α = N/2 and t = √(2Nu). t ≤ α ⟺ 8u ≤ N. The upper tail is e^{−t²/(4α)} = e^{−u} and the lower tail is
  e^{−t²/(2α)} = e^{−2u}. Correct.
- **M1.** SVD with λ_k = ns_k²/((n+1)s_k² + 1) ∈ (0, 1). The orderings 0 ⪯ M ⪯ P, M² ⪯ M and (I−M)² ⪯ I − M follow.
  Correct, including rank-deficient X_{c,S₀} (singular Gram).
- **M2.** Mean X_cθ̂ = My_c and covariance vM. Correct given the premise P-T01. P-T01 (shape ν = a₀ + n/2, rate b + Q/2,
  slab covariance nvH⁻¹) is taken from API_CARDS and [D] D0 as the locked T01 identification. I did **not** re-derive it
  from [P1]. It is the declared sole inherited premise (STATEMENT l. 388–391).

### 3.2 Fixed-design step
- **Step 0.**
  - n ≥ ⌈C_v^{2/κ₀}⌉ gives n^{κ₀} ≥ C_v² ≥ 32, so u/n ≤ n^{−κ₀} ≤ 1/32.
  - u ≤ n/32 ≤ (n−1)/8, since n ≥ 4/3.
  - 4u ≤ n/8 ≤ ν.
  - (iii) holds for 1 ≤ u ≤ n.
  - (iv): C_v√(u/n) ≤ C_vn^{−κ₀/2} ≤ 1, so (C_ρ + 2√2)√(u/n) ≤ ½.
  - All correct. s₀ ≤ s₀^r ≤ ⌊n/2⌋ by n ≥ 2s₀^r, so S₀ ∈ Ω.
- **Step 1 (noise event).**
  - 𝓔¹: 2e^{−u}.
  - 𝓔²: 2^{r₀/2}e^{−u}2^{−s₀^r/2} ≤ e^{−u}.
  - 𝓔³: 2e^{−u} by G4, since u ≤ N/8.
  - 𝓔⁴: ‖a₀'‖² = μ_cᵀ(I−M)²μ_c ≤ L ≤ B, so σ*√(2Bu) ≥ σ*‖a₀'‖√(2u), giving 2e^{−u}.
  - 𝓔⁵: probability 1.
  - Total 7e^{−u}. Correct. Everything depends only on (X^r, ε). U is fixed.
- **Step 2.**
  - (D1) uses 2√(2Nu) ≤ N.
  - (D2): s_y² ≤ 2nM/N + 4σ*² ≤ 3M + 4σ*² ≤ 4(M + σ*²), so b ≤ b̄.
  - (D3): Q = ‖e‖² − eᵀMe + 2eᵀ(I−M)μ_c + L, which is D1(d) of [D]. The four-term bound holds.
  - (D4): 2β − 2νσ*² = 2b + (Q − Nσ*²) − (2a₀+1)σ*², with 2ν = N + 2a₀ + 1. Dividing by 2νσ*² ≥ nσ*² and bounding
    termwise (1/n, √(Nu)/n, u/n, √u/n ≤ √(u/n)) gives exactly C_ρ = 2b̄/σ*² + 2a₀ + 1 + 2√2 + k_s + 2√(2B)/σ* + B/σ*²
    with k_s = 4 + 2s₀^r log 2 (recomputed).
  - (D5) is [D] D1(b). Its last step uses 4u + 2s₀^r log 2 ≤ k_su for u ≥ 1.
  - (D6) is 𝓔¹.
  - All correct.
- **Step 3.**
  - G = β/v ~ Gamma(ν, 1), and t = 2√(νu) ≤ ν ⟺ 4u ≤ ν. The tails are e^{−u} and e^{−2u}.
  - On 𝒱: |g − 1| ≤ 2√(2u/n) ≤ ½. Then |ρ/g − 1| = |ρ − g|/g ≤ 2(|ρ−1| + |g−1|) ≤ C_v√(u/n) ≤ 1.
  - 𝒲 has conditional probability ≤ e^{−u} by G2, with λ_k ∈ (0, 1) and r₀ ≤ s₀^r.
  - On 𝒱 ∩ 𝒲: ‖X_c(θ − θ̂)‖² ≤ 2σ*²k_su, so ‖μ̂ − μ‖² ≤ 2·2σ*²k_su + 2(2σ*²k_su + 2B) = 8σ*²k_su + 4B ≤ C_μu.
  - Transfer: b is supported on S₀ ⊆ R ∩ {retained}, so supp(b − β*) ⊆ R. (TR₀) quantifies over all (a, w)
    simultaneously, so data-dependent (â − α*, b − β*) is admissible. Then E_xΔ² ≤ C_T(ε̄² + ‖μ̂ − μ‖²/n) by (H-id).
    E_xΔ² is finite on (TR₀).
  - Lemma H (second form): d_H² ≤ C_v²u/n + (C_T/(4σ*²))(2σ*² + C_μ)u/n = C_rad²u/n.
  - Hence 𝔅_u ∩ {S = S₀} ⊆ 𝒱ᶜ ∪ 𝒲ᶜ, with mass ≤ 3e^{−u}. Correct.
- **Step 4.** The mixture bound ≤ δ_n + 3e^{−u}. Correct.
- **Constant c = 1.** Confirmed. With C := max{C_rad, 7}: {d_H > C√(u/n)} ⊆ 𝔅_u, 3e^{−u} ≤ Ce^{−u}, and the noise
  probability 7e^{−u} ≤ Ce^{−u}. Both STATEMENT displays follow. Numerical constants (σ*² = 1, s₀^r = 3, M = B = 1,
  C_T = 2, κ₀ = ½), recomputed: C_ρ = 15.996, C_v = 37.648, C_μ = 69.271, C_rad = 38.119, n₀ = 2 009 014. These agree
  with `check_DIST3_out.txt` [0].
- **Dependence of n₀.** n₀ = max{3, 2s₀^r, ⌈C_v^{2/κ₀}⌉}, and C_v involves only (σ*², M, B, s₀^r) and the fixed
  a₀ = b₀ = 0.01. So n₀ depends on (s₀^r, σ*², M, B, κ₀), not on C_T, A, p_raw or p_ret, as claimed. C_rad depends also
  on C_T. Remark 5's per-u condition n ≥ max{3, 2s₀^r, 32u, C_v²u} is right, since C_v² ≥ 32.

**Edge cases.**
- s₀ = 0 (S₀ = ∅; M = P = 0, r₀ = 0, μ̂ = 0) goes through every step.
- Dropped true columns: S₀ excludes them. (TR₀) then forces such x_j to be a.s. constant, which is consistent.
- Singular Gram: M1.
- p_ret < 2 and p ≤ n^A are not used.
- C_T < 1 makes (TR₀) empty (a-only directions), so this is harmless.

### 3.3 Integration over the design
- **Measurability of (TR₀).**
  - If E x_j² = ∞ for some j ∈ R, the event is empty.
  - Otherwise (TR₀) = {C_TΣ_n − Σ ⪰ 0}, which is closed in the Borel matrix Σ_n.
  - Correct. With R = ∅ this reduces to C_T ≥ 1.
- **Corollary DIST-3(R).**
  - 𝔈 is Borel. P_{S₀} and a₀' are Borel in X^r: finitely many retained-column patterns, plus Borel pseudo-inverses.
  - The bad event lies inside 𝔈.
  - Fubini with ε independent of X^r gives ≤ 7e^{−u}P*(𝒢_n).
  - Correct.
- **Measurability of the posterior functionals.** By Tonelli through Claim 2 of H.md. Adequate.
- **Corollary DIST-3(P).**
  - u_n = min{(M_n/C_rad)², n^{1−κ₀}} → ∞.
  - {d_H > M_n/√n} ⊆ 𝔅_{u_n}.
  - The three-term bound P*(𝒢_nᶜ) + 7e^{−u_n} + P*(δ_n > η'/2) → 0.
  - Correct.

### 3.4 Notes (i)–(iii) and the three requested clarifications
- **Note (i).** Confirmed. The design inputs are only L_{S₀} ≤ B, ‖μ‖² ≤ nM (through b) and (TR₀). There is no floor,
  no beta-min and no coefficient claim.
- **Note (ii), proof in Remark 2.** Checked.
  - zᵀξ = 0 a.s. for z ⊥ V = range Σ, so Σ_nz_⊥ = 0.
  - Weak LLN entrywise, with integrability from |x_jx_k| ≤ (x_j² + x_k²)/2.
  - On ‖Σ_n − Σ‖_op ≤ λ(1 − 1/C_T): zᵀΣ_nz ≥ z_VᵀΣz_V/C_T = zᵀΣz/C_T.
  - V ≠ {0} because ξ contains the constant 1.
  - Correct for any fixed C_T > 1.
- **Note (iii).** It is a wording note only. Consistent.
- **Clarification 1 (letter clash u/w).** Justified. EQUAL.
- **Clarification 2 (constants).** Justified, and in fact **necessary**; see P4B-01.
  - STATEMENT DIST-3 reads "There are c, C such that for every n ≥ n₀" without quantifying n₀.
  - §0's convention lists the admissible dependence as (s₀^r, A, σ*², M, M′ or B, κ₀), which does not include C_T.
  - The radius constant cannot be independent of C_T. If the population second moment on R exceeds the sample one by a
    factor C_T, then on (TR₀; C_T) the out-of-sample term E_x min{1, Δ²/4σ*²} is of order C_T·u/n while C_T ≪ n/u.
  - So the theorem as literally read with the §0 convention is not what is proved, nor what can be proved.
  - The repair does not weaken a target clause: C_T is a hypothesis parameter. Tag EQUAL (intended meaning).
- **Clarification 3 (in-probability corollary).** Justified. P* of the intersection of the four events → 1 is equivalent
  to each event's probability → 1, since there are four of them. EQUAL.

**Verdict, Theorem DIST-3: VERIFIED-WITH-AMENDMENTS** (P4B-01: write the constant dependence into the statement).
Inherited: premise P-T01 is not re-derived here, as declared.

---

## 4. Findings

**P4B-01 — MINOR — DIST3.md "Clarifications" item 2 / STATEMENT §1 Theorem DIST-3 (l. 95–97) and §0 constants convention
(l. 62–63).**
- **Problem.** The STATEMENT does not quantify n₀ in DIST-3, and its global constants convention does not allow C to depend
  on C_T. The proof's C (through C_rad) depends on C_T, and this is unavoidable (§3.4). DIST3.md records the issue only as
  a "wording clarification".
- **Minimal repair.** Insert into DIST-3: "There are c, C, n₀, with c = 1, n₀ depending only on (s₀^r, σ*², M, B, κ₀) and
  C depending in addition on C_T, such that …". Record it in the changelog as EQUAL (intended meaning).
- The theorem is proved in this form.

**P4B-02 — MINOR (editorial, STATEMENT route text) — STATEMENT §3 Lemma T "Route" (l. 302–306); T.md "EDITORIAL NOTE".**
- **Problem.** The route text cites the ratio inequality "≤ 4S(2n)e^{−nη²/4} (attribution and constant to be verified)"
  followed by Cauchy–Schwarz. None of the in-house proofs that reach the stated constants relies on it unconditionally:
  - T.md uses the multiplicative Prop. R;
  - T-c uses a ratio form with 16;
  - T-a proves the quoted form only modulo Greenberg–Mohri.
- **Minimal repair.** Replace the route sentence as T.md suggests: "multiplicative VC inequality, proved in
  `work/B_transfer/T.md` Prop. R; layer cake (linear)". Drop the unverified attribution.
- No statement change.

**P4B-03 — NIT — T.md header ("the Cantelli step has little slack: 0.284 against 1/4").**
- **Problem.** The slack is only in the swap exponent at the fixed choice ρ = 4/5. Overall the argument has margin:
  - any ρ ∈ [0.762, 0.834] works with nη² > 36.6;
  - ρ = 4/5 needs only nη² ≥ 25.
- **Repair (optional).** Add one sentence so that a later reader does not over-read the fragility.

**P4B-04 — NIT — DIST3.md §3 Step 1, 𝓔⁵.** 𝓔⁵ has probability 1. Including it costs nothing, and it is correctly used to
make b > 0 and π(S₀) > 0 hold surely on 𝓔_u. No change needed. It is recorded only because the count "7e^{−u}" omits it,
correctly.

No CRITICAL or MAJOR finding. No counterexample was found. Every inequality, constant, event and limit in the three files
was recomputed. Not checked: the premise P-T01 against [P1] (declared inherited); the external citations of T-a and T-b
(Greenberg–Mohri Thm 1, Bousquet 2002 Thm 2.3), which the preferred route does not use; and the remaining 43 lines of
`check_DIST3.py`. I relied only on its printed output [0] for the constants, and I recomputed those independently.

## 5. Verdicts
- **Lemma H (`H.md`): VERIFIED.**
- **Lemma T (`T.md`): VERIFIED** (STATEMENT route-text amendment P4B-02, editorial). The comparison attempts T-a-1 and
  T-c-1 reach the same final statement with the same η²_n(d, δ). T-c-1 is valid and self-contained modulo Sauer–Shelah.
  T-a-1 is valid modulo (BIN). T.md's self-contained route is preferable.
- **Theorem DIST-3 (`DIST3.md`): VERIFIED-WITH-AMENDMENTS** (P4B-01: write the dependence of C on C_T and the dependence
  of n₀ into the statement; c = 1 confirmed).

**Overall: VERIFIED-WITH-AMENDMENTS (two MINOR, two NIT; no CRITICAL or MAJOR). Ready for the cross-family line check.**
