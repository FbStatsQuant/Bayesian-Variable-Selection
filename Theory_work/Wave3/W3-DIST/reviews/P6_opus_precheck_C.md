# P6 pre-check, stream C: Lemma S, Lemma V, steps X1–X2 (same-family line check)

Checker: Claude Opus 5.5 (Claude Third), effort high. Date 2026-11-15. Read-only except this file. No git command, no agents.
Read: `briefs/PRECHECK_COMMON.md`, `briefs/BRIEF_P6_C_precheck.md`, `STATEMENT.md` v1.3.1 (§0, §3), `API_CARDS.md`
("Common definitions", Card V), `work/C_size/S.md`, `V.md`, `X12.md`, `c_checks.py`, `c_checks_out.txt`;
[P1] `PROOF_v3.tex` lines 36–370 (setting, `lem:slab`, `lem:spec`, `lem:prior`, `lem:chi`, `prop:closed`, `thm:T01i`,
`thm:T01ii`, `thm:T01iii`, `thm:Ta`, `lem:num`, `lem:den`, start of `thm:T02i`); `W3-POST2/lemmas/B_tail_approx.md` lines 30–55;
H1 `work/prior_probe/REPORT.md` §3 (lines 80–92) and A2 (lines 189–204); the comparison files S-a-1, S-b-1, S-c-1, V-a-1,
V-b-1, V-c-1. Not read (per the rules): `reviews/`, `LOG.md`, `CHECKPOINT_*`, `DEPS.*`. I did not open `L1a_size_tail.md`
or `D_hellinger.md`. They are not needed, because S.md and X12.md re-derive what they take from them.

Independent recomputation (scratch scripts, not in the repo):
(i) Lemma V (a) at the **worst-case** noise vector. sup_e[Q^c_{S₀} − Q^c_S − eᵀD′e] is computed in closed form as a concave
quadratic, over 3000 designs: i.i.d. columns, exact duplicates, 10⁻⁵-near-span J columns, 10⁻⁴-collinear pairs in S₀,
s₀ ∈ {0,…,3}, η ∈ {0.01, 0.2, 1, 5}, coefficients up to 30.
(ii) Lemma V (b) through the exact determinant formula on the same designs.
(iii) The (L₀) counter-configuration of V-c §3.3.
Results: (a) holds with the worst excess = 0, attained only at e = 0 when s₀ = 0. (b) holds with log-excess ≤ −1.8·10⁻⁴.
(iii) is confirmed: see C-7.

---

## 1. Lemma S (`S.md`)

### Line check
- **Setting G′.** μ := Cf ∈ 1^⊥, f₀ = N_N(Uᵀμ, σ*²I) > 0 is the density of y_c. [P1] `lem:num` (proof lines 318–322) uses only
  this: Tonelli, plus "f₀ > 0 is the density of y_c". `thm:T01i`, `thm:T01ii` and the first inequality of `thm:Ta` are
  deterministic in y_c (Ta's proof, lines 260–262, says so explicitly). The extension from G to G′ is therefore valid.
  Strict sparsity is the special case.
- **Constants.** b₋ = b₀σ*²/2, b₊ = b₀(2(σ*²+M)+1), κ and 𝓑_n agree verbatim with [P1] line 58. The lower bound on c_IG is
  correct: on [σ*², 2σ*²], v^{−1.51} ≥ (2σ*²)^{−1.51} and e^{−b₊/v} ≥ e^{−b₊/σ*²}. The bound in R5 on log c♯ is recomputed exactly:
  log c♯ = 1.02 log(b₊/b₋) − log c_IG − log σ*², and the terms collect to the stated expression.
- **(1.1).** Z^c_{b₊} ≥ ϖ(T)m^c_{b₊}(T) needs only T ∈ Ω. Correct.
- **(1.2).** f₀(y_c) = (2πσ*²)^{−N/2}e^{−E′/2}, and the ratio of the slab integrand to f₀ is (v/σ*²)^{−N/2}e^{E′/2}e^{−Q/(2v)}. Correct.
- **Step 2.** r ∈ 1^⊥ because μ and X_Tϑ are centred, so ‖Uᵀr‖² = rᵀCr = ‖r‖² and ε_cᵀUᵀr = εᵀCr = εᵀr. Also
  ϑᵀ(G_T+I)ϑ = ‖X_Tϑ‖² + ‖ϑ‖². Hence Q^c_T ≤ σ*²E′ + 2εᵀr + B_T(ϑ). Recomputed; T = ∅ is correct.
- **Step 3.** Recomputed term by term. −(N/2)log u ≥ −(N/2)(u−1). (E′/2)(1−1/u) − ρ″/(2σ*²u) = ((u−1)/2)(E′/u) − …, and
  1/u ≥ 2 − u. ((u−1)/2)(E′−N) ≥ −|E′−N|/(2√n) and −(u−1)²E′/2 ≥ −E′/(2n). The window [σ*², σ*²(1+n^{−1/2})] ⊆ [σ*², 2σ*²] has
  length σ*²n^{−1/2}. (3.1) is correct, and it is identical to [P1] `lem:den` with R_n → ρ″.
- **Step 4.** v_m = Σ_{k>m}^K q_k/W_K = R^T_mϖ(T) (W_K cancels). EΘ^{(1)}_m = 1 exactly by `lem:num` at the data-free rate b₋.
  (4.1) = κ²R^T_mΘ/(m^c_{b₊}(T)/f₀) ≤ R^T_m√D_T√n·c♯e^{Λ″}Θ. Correct. It matches Claim B's display (`B_tail_approx.md`
  Step 4).
- **Step 5.** The two (LM) sides give 2e^{−x}, and (G) with s = σ*‖r‖ gives 2e^{−x}. On 𝒜_x: |E′−N|/(2√n) ≤ √x + x/√n,
  E′/(2n) ≤ ½ + √x + x/√n, and ρ″/(2σ*²) ≤ B/(2σ*²) + (√(2B)/σ*)√x (‖r‖² ≤ B). The coefficients sum to (½ + B/(2σ*²), 2 + √(2B)/σ*, 2).
  Because C₁ ≥ 2, (5.1) is correct.
- **Step 6 (brief duty: response-scale bracket).** Recomputed. Under G′, Ns_y² = ‖μ‖² + 2μᵀε + σ*²E′.
  - Lower inclusion: s_y² < σ*²/2 ⇒ Δ_n < −σ*²/2.
  - Upper inclusion: ‖μ‖²/N ≤ 3M/2 for n ≥ 3, so s_y² > 2(σ*²+M)+1 ⇒ Δ_n > σ*² + M/2 + 1 > σ*²/2. This is the same as
    [P1] line 249.
  - Split: {|Δ_n| > σ*²/2} ⊆ {|E′−N| > N/4} ∪ {|μᵀε| > Nσ*²/8}.
  - (LM) with x = N/100: 0.2N + 0.02N = 0.22N ≤ N/4. With x = N/64: 2√(N·N/64) = N/4.
  - (G): s√(2x) = Nσ*²/8 ⇔ x = N²σ*²/(128‖μ‖²) ≥ N²σ*²/(128nM) ≥ Nσ*²/(192M), using N/n ≥ 2/3.
  - With N ≥ 2n/3: N/100 ≥ n/150 and Nσ*²/(192M) ≥ nσ*²/(288M).
  - Result: **P(𝓑_nᶜ) ≤ 4e^{−c_Bn}, c_B = min{1/150, σ*²/(288M)}, verified for every n ≥ 3.** M = 0 makes the Gaussian event empty.
- **Step 7.** log c♯ + C₁(·) ≤ C_S(·) because (·) ≥ 1 and C_S ≥ C₁ + log₊c♯. The failure count 4e^{−c_Bn} + 4e^{−t} + e^{−t} is correct.
- **Nesting.** R^T_m is non-increasing because q_k > 0 for k ≤ K ≤ p. For m ≤ −1, R^T_m = W_K/w(|T|) ≥ 1 since W_K ≥ ½ ≥ w(k), so
  (S-hyp) fails and m* ≥ 0. Monotonicity of π(|S| > m) gives the simultaneous claim. Correct (see C-2).
- **Uniformity.** Every constant depends only on (σ*², M, B). No step uses p ≤ n^A, n large, or κ₀. So "every n ≥ 3, every
  t > 0" is correct. This is stronger than the STATEMENT, and it implies the STATEMENT form with C := C_S ≥ 5 ≥ 4, c := c_B,
  n₀ := 3.
- **Corollary S.1 (cutoff arithmetic; brief duty).**
  - T = S₀ ∈ Ω for n ≥ 2s₀^r. B_{S₀}(θ*) = (‖μ‖² + ‖θ*‖²)/n ≤ M + M′. θ* is X-measurable through D_x.
  - If m_n(t) = K, then R = 0 (cap). Otherwise m log 2 ≥ s₀ log 2 + A ≥ A.
  - Σ_{k>m}q_k ≤ 2^{−m}: [P1] line 128 with q₁ = p/(2(2p−1)) ≤ ½ and ratio ≤ ½ for k ≥ 1.
  - 1/w(s₀) = 2C(2p−1, s₀) ≤ 2(2p)^{s₀} and D_{S₀} ≤ (n+1)^{s₀} (`lem:spec`(e)).
  - Sum: log 2 − ½ log(n+1) − 3t ≤ −3t since ½ log 4 = log 2.
  - Then n ≥ 4C_S² gives C_St/√n ≤ t/2, and t ≥ (2C_S+1)² gives C_S(1+√t) < t/2. All recomputed and correct.
  - s₀ = 0: T = ∅, μ = 0, B_∅ = 0, R^∅_m ≤ 2·2^{−m}. Covered.
- **Corollary S.2.** t ≤ n^{1−κ₀} ≤ c_Bn ⇔ n^{κ₀} ≥ 1/c_B. Correct (see C-3).

**STATEMENT-CHANGE REQUEST:** none. The file proves a strengthening of STATEMENT §3 Lemma S: every n ≥ 3 and t > 0,
constants free of κ₀, under G′. It also proves the corollary sentence for T = S₀ in the form "n ≥ n_S, every t ≥ log n".

### Findings
- **C-1 (MINOR; S.md, Corollary S.1).**
  - Problem: n_S contains ⌈exp((2C_S+1)²)⌉. Since C_S ≥ 5, this is n_S ≥ e^{121}. The proof is correct and the STATEMENT only
    asks for some n₀, but the corollary is vacuous at any real sample size. The size is forced only by anchoring the range
    at t ≥ log n. Lemma X uses t ≥ M₀ log n with M₀ free, so it does not need the corollary in this form.
  - Repair (same proof): add "for every n ≥ max{3, 2s₀^r, ⌈4C_S²⌉} and every t ≥ max{log n, (2C_S+1)²}". The present form then
    follows for n ≥ e^{(2C_S+1)²}.
  - Optional: S-b-1's closed-form route has no t/√n term and gives a smaller threshold. See §4.
- **C-2 (NIT; S.md, Step 7 "Nesting").**
  - Problem: if the least qualifying m* has R^T_{m*} = 0 (m* = K), then v_{m*} = 0 and Θ^{(1)}_{m*} is undefined.
  - Repair: read {Θ^{(1)}_{m*} ≤ e^t} as the sure event in that case, since π(|S| > m*) = 0.
- **C-3 (NIT; S.md, Corollary S.2, "equivalently" sentence).**
  - Problem: applying S.1 and the absorption at t′ = ct also needs t′ ≤ n^{1−κ₀} and n ≥ n_S′. Both are implicit.
  - Repair: state them.
- **C-4 (NIT; S.md, definition of R^T_m).**
  - Problem: STATEMENT writes Σ_{k>m}, which leaves the upper limit open. S.md sums to K.
  - Repair: add one line saying that the K-reading gives the weaker hypothesis, so both readings are covered. S-a-1 makes
    this remark.

**Verdict, Lemma S (incl. Corollaries S.1, S.2): VERIFIED-WITH-AMENDMENTS** (C-1 to C-4 are presentation and range-statement
amendments; no mathematical error).

---

## 2. Lemma V (`V.md`)

### Line check
- **Definitions.** D′ = M^{(1/c)}_S − M^{(c)}_{S₀} with M^{(a)}_T = X_{c,T}(G_T + aA_T/n)⁻¹X_{c,T}ᵀ, and ρ′ = θ*ᵀA_{S₀}θ*/n
  = (‖μ‖² + ‖θ*‖²)/n. These are identical to H1 §3/A2 and Card V. ‖μ_c‖ = ‖μ‖ holds because μ ∈ range U.
- **(0.i).** K = G + aA/n ≻ 0 for every design. For a = 1, K = H/n, so M^{(1)} = M_T. Correct.
- **(0.ii).** WK = ((1+a/n)B + (a/n)I)W, so M^{(a)} = h_a(B) with h_a < n/(n+a). 1 − h_a(λ) = a(λ+1)/(nλ+aλ+a) ∈ (0,1) for λ > 0.
  Recomputed; correct. R₀'s eigenvalues lie in (0,1), not (0,1] as H1 and V-b write. Immaterial.
- **(0.iii).** (α) holds pointwise in a. (β) holds because the T×T block of A_{T′} is A_T. Neither needs invertibility of G.
  Correct.
- **Step 1.** Young (Y1) with κ = η and (Y2) with κ = η/(1+η) were re-expanded; 1 − κ = 1/(1+η) and 1 − 1/κ = −1/η. The upper
  bound on Q^c_{S₀} gives (1 + 1/η)ρ′ and the lower bound on Q^c_S gives −ρ′/η, using θ̄ᵀA_Sθ̄ = nρ′ by zero-padding. Subtracting
  gives (1 + 2/η)ρ′. Correct and pathwise. D′ ⪰ 0 from (α) then (β). ‖D′‖ ≤ λ_max M^{(1/c)}_S < cn/(cn+1). Correct.
- **(2.i) Woodbury.** The direct product check was recomputed: (I + CG) = C(C⁻¹ + G). Correct.
- **(2.ii) Sylvester.** g_a(λ) = (1 + (1+n/a)λ)/(1+λ) and g_1 = f of [P1] `lem:spec`(e), so D^{(1)} = D. g_a(0) = 1. Correct.
- **(2.iii).** The Gaussian MGF needs λ_max(D′) < 1, which (a) gives. Correct.
- **(2.iv).** D′ = Σ₀⁻¹ − Σ_S⁻¹, and I − Σ₀^{1/2}D′Σ₀^{1/2} = Σ₀^{1/2}Σ_S⁻¹Σ₀^{1/2} ≻ 0. FFᵀ and FᵀF are isospectral (F square).
  D′^{1/2}Σ₀D′^{1/2} ⪰ D′. By Weyl, factor-wise 0 < 1 − λ_i(D′^{1/2}Σ₀D′^{1/2}) ≤ 1 − λ_i(D′), so
  det(I − D′) ≥ D^{(c)}_{S₀}/D^{(1/c)}_S. Correct. This is the step H1 leaves unproved; V.md supplies it.
- **(2.v).** Both eigenvalue inequalities reduce to 1 + λ ≤ c(1+λ). Zero eigenvalues contribute 1, so the rank form
  c^{r_S}, c^{r₀} follows. Correct.
- **(2.vi).** c^{(r₀+r_S)/2} ≤ c^{s₀+|J|/2}. Correct.
- **Step 3 / (c).** M^{(1/c)}_S ⪯ P_S and 0 ⪯ R₀ ⪯ P_{S₀}. P_S − P_{S₀} is the projection onto col X_{c,S} ⊖ col X_{c,S₀}, of rank
  d_J ≤ |J|. The chi-square laws and their independence follow from orthogonality. Correct.
- **Edge cases (brief duty).**
  - Singular G and duplicated columns: only A and K are inverted.
  - s₀ = 0: (a) reduces to eᵀM_Se ≤ eᵀM^{(1/c)}_Se.
  - J = ∅: D′ = M^{(1/c)}_{S₀} − M^{(c)}_{S₀} ⪰ 0 and the bound is c^{s₀}.
  - |S| ≤ p with S ∉ Ω: nothing uses Ω.
  - All correct. My worst-case-e recomputation (header) confirms (a) and (b) on adversarial families.
- **Remarks V.1–V.2.** Correct. V.1's threshold ε ≫ 1/n agrees with V-b §5.4 and V-c §3.4 (ε ≥ 1/(cN) with one column).

**STATEMENT-CHANGE REQUEST:** none. V.md reads STATEMENT's (c) as the pathwise inequality with an exactly χ²_{d_J} first term.
That reading is correct and is what STATEMENT means.

### Findings
- **C-6 (NIT; STATEMENT §3 Lemma V wording, used by V.md).**
  - Problem: STATEMENT writes "Q_{S₀} − Q_S". V.md and Card V use Q^c, the response-scale contrast quantity. On the
    standardised scale, Q_S = Q^c_S/s_y², and the inequality with ρ′ in response units would be dimensionally wrong.
  - Repair: write Q^c in STATEMENT §3. X12.md already sets Q_S := Q^c_S.
- **C-7 (MINOR; STATEMENT §0, outside the three files, surfaced by V-c-1 §3.3 and confirmed here).**
  - Problem: STATEMENT §0 says (C; M′) is "used only through (L₀; B)". That is false for Lemma V(a) and hence for the X4
    superset route. V(a) genuinely needs ρ′ (the coefficient cost), not L_{S₀}.
  - Recomputation, design of V-c Attack 3 at n = 100, η = 1, α = 10⁻³:
    sup_e[Q^c_{S₀} − Q^c_S − eᵀD′e] = 131.6τ², while L_{S₀} = 0.995τ² and (1+2/η)ρ′ = 606τ².
  - Impact: none on the current lemma statements. Lemma X keeps (C; M′) explicitly, and V.md and X12 F3/F6 use ρ′ ≤ M + M′
    correctly.
  - Repair: restrict the §0 sentence to Lemma S and DIST-3 (reference-cost uses), and say that X4/Lemma V use ρ′ (or
    min{(‖μ‖² + ‖ϑ‖²)/n : X_{S₀}ϑ = μ}, per V-a and V-b Remark 3).

**Verdict, Lemma V: VERIFIED** (C-6 and C-7 concern STATEMENT text, not V.md).

---

## 3. Steps X1–X2 and facts F1–F7 (`X12.md`)

### X1 (brief duty: P(𝓔_tᶜ) ≤ e^{−t}, constants, range)
- **(i).** (LM) with x = 2t gives thresholds 2√(2Nt) + 4t and 2√(2Nt). Failure ≤ 2e^{−2t}. Correct.
- **(ii-a).** r + 2√(rx) + 2x ≤ 2r + 3x. With x_k = k log p + k + 2t: 2k + 3x_k = 3k log p + 5k + 6t ≤ 3kℓ_p + 6t. The union is
  Σ p^k p^{−k}e^{−k}e^{−2t} = e^{−2t}/(e−1). Correct for every T ⊆ [p]; rank deficiency and r = 0 are covered.
- **(ii-b).** Same count with d_J ≤ |J| and C(p−s₀, k) ≤ p^k. Correct.
- **(iii).** a_S is design-measurable. With x_k = k log p + k + 2t + log 2: 2x_k ≤ 2kℓ_p + 6t needs 2 log 2 ≤ 2t, which t ≥ 2 gives.
  Union e^{−2t}·e/(e−1). Correct.
- **Total.** 2 + (2+e)/(e−1) = 4.746 ≤ 4.75, and 4.75e^{−2t} ≤ e^{−t} ⇔ e^t ≥ 4.75, true for t ≥ 2. Correct.
- **(iv).** 2‖μ‖²/N ≤ 3M and 2(1 + 2/√32 + 1/16) = 2.83 ≤ 3. Correct. It uses t ≤ N/64; the probability bound itself needs only t ≥ 2.
- **Range.** n^{κ₀} ≥ 128 ⇒ n^{1−κ₀} ≤ n/128 ≤ N/64. n ≥ e^{2/M₀} ⇒ M₀ log n ≥ 2. So there is one n₁ for all
  t ∈ [M₀ log n, n^{1−κ₀}], and p ≤ n^A is not used. Correct.

### X2 (brief duty: simultaneous bound and constants)
- **Bookkeeping.** ℓ_p ≤ 4 log p holds for p ≥ 2; it is tight at p = 2 (2.693 ≤ 2.773). So |S|ℓ_p ≤ C₃t, 2|S| ≤ C₃t and
  w_S ≤ (2C₃+6)t. Correct.
- **Step 2.** ‖M_Sy_c − μ_c‖² ≤ σ*²t(6C₃ + 12 + 2C″) and |Q_S − ‖e‖²| ≤ σ*²K_Qt. Recomputed. β_S/ν = (2b+Q_S)/(n+0.02).
  N − (n+0.02) = −1.02. The constants 0.06 + 1.02 = 1.08 plus 4 give 5.08 in K_β; this uses t ≥ 1 and t ≤ n. Correct.
- **(Γ) Gamma tails.** Re-derived: the cumulant bound νλ²/(2(1−λ)), λ = s/(ν+s), s² ≥ 2x(ν+s); and the lower tail with
  log(1+λ) ≥ λ − λ²/2. Correct. β/v ~ Gamma(ν,1). Correct.
- **Step 3.** x = 2t ≤ ν/8 (t ≤ n/32) gives G > ν/2 on 𝒢. Then |ν/G − 1| ≤ 2√(2x/ν) + 2x/ν ≤ 5√2√(t/n) ≤ 5/4, using 8/√32 = √2.
  |aβ − 1| ≤ (9/4)K_β√(t/n) + 5√2√(t/n) ≤ C_v√(t/n). Correct.
- **Step 4.** Cov Z = vM_S. (LM) with a_i = λ_i ∈ [0,1) gives r_S + 2√(2r_St) + 4t ≤ 2|S| + 6t. v ≤ 2σ*² needs t ≤ n/C_v².
  C_μ = 4(C₃+6) + 2(6C₃+12+2C″) = 16C₃ + 48 + 4C″. Recomputed; correct.
- **Step 5.** The bad set is contained in 𝒢ᶜ ∪ {‖Z‖² > v(2|S|+6t)}, so the bound is 3e^{−2t} ≤ e^{−t}. Correct.
- **Simultaneity.** Every bound is deterministic on 𝓔_t, so the bound holds for all good S at once. Correct.
- **Instance for Lemma X.** d_t log p ≤ A(s₀^r+1)log n + AC′t ≤ A(C′ + (s₀^r+1)/M₀)t. Correct. n₂ ensures t ≤ n/C_v². Correct.

### Facts F1–F7 (brief duty)
- **F1 (a)–(f).** Correct. (b) and (c) were re-expanded; (e) uses `lem:slab` with Y = μ_c and the exact representation.
- **F2 (a)–(e).** Correct. AM-GM forms: 2σ√(Lw) ≤ L/2 + 2σ²w and ≤ L + σ²w; min_L(L − 2σ√(Lw)) = −σ²w. The constants
  7, 18 / 2, 6 / 5, 12 / 5, 12 were recomputed.
- **F3.** Correct (18 + 6 = 24). The second display holds under |S|ℓ_p ≤ C₃t, p ≤ n^A and t ≥ M₀ log n. These are stated as
  conditions; correct.
- **F4.** (a) and (b) are correct (n + 0.02 − 𝔇_S recomputed). (c): 0.1 + 0.015 + 0.385 ≤ ½ and 4√2·√(3/2) = 6.93 ≤ 7. Correct
  (see C-8).
- **F5.** (N + 0.02)s_y² ≤ 3n(M+σ*²), ν ≥ n/2, log(1−x) ≤ −x. Correct.
- **F6.** Correct. ε_S ≥ 0 when 𝔇_S > 0. The surcharge is paid pathwise through V(c) and (ii-a). The second exponential depends
  on S only through |S|. E[X·1_{𝓔_t}] ≤ E X, so V(b) applies.
- **F7.** Correct: e^{ℓ_p} = e²p ≤ n^{A+2} when p ≤ n^A.

### Findings
- **C-8 (NIT; X12.md F4(c), last sentence).**
  - Problem: the identification with ε_{n,t} for |S| ≤ m_n(t) + s₀ needs t ≤ N/800 and |S|ℓ_p ≤ N/13. On t ≤ n^{1−κ₀} these
    hold only for n ≥ some n₀(A, s₀^r, κ₀), which is not stated.
  - Repair: state that n₀. For example, m_n(t) + s₀ ≤ C(s₀^r, A)·t and t ≤ n^{1−κ₀} give |S|ℓ_p ≤ C·n^{1−κ₀}log n ≤ N/13
    for n ≥ n₀.
- **Not checked:** the claim in the file header that ROUTES' constants would give failure ≈ 4.7e^{−t}. It is a remark about
  ROUTES, not used in the proof.

**STATEMENT-CHANGE REQUEST:** none. The departures from ROUTES are strengthenings: ℓ_p in place of log n, all T ⊆ [p], and
explicit constants.

**Verdict, X1: VERIFIED. X2: VERIFIED. F1–F7: VERIFIED** (C-8 is an n₀ statement, a NIT).

---

## 4. Comparison with the independent attempts (brief duty 4)

**S.md vs S-a-1, S-b-1 (and S-c-1).**
- **Statement.** All four prove at least the STATEMENT form with n₀ = 3 (S-c: n₀ = max(7, 4M+1)), every t > 0, and constants
  free of κ₀.
  - S-a: the same hypothesis as S.md; failure 5e^{−t} + 3e^{−n/16}.
  - S-b: a strictly stronger result. Hypothesis (H) has no t/√n term, failure is 2e^{−t} + 3e^{−n/64}.
  - No disagreement on the statement.
- **Shared steps.**
  - (1) Numerator: Markov on Θ^{(1)} at the data-free rate b₋, through properness of m^c_{b₋}(S). Identical in all four.
  - (2) Reference bound Q^c_T ≤ σ*²E′ + B + 2εᵀr. Identical in all.
  - (3) Rate envelope κ² (S.md, S-a, S-c), or a direct b₋/b₊ comparison of the closed forms (S-b). Both correct.
  - (4) Denominator: the v-window of `lem:den` (S.md, S-a, S-c), or the closed form plus Stirling,
    ν^νe^{−ν}/Γ(ν) ≤ √(ν/2π) (S-b). I recomputed S-b's Step 4 (ue^{1−u} ≤ 1, b₋^{−0.51}σ*^{1.02} = 200^{0.51}); it is correct.
    S-b's route shows that S.md's t/√n term, and its need for n ≥ 4C_S² in S.1, are artefacts of the v-window. This is not
    an error in S.md.
  - (5) Bracket: each attempt uses a different bracket and all are correct for their own endpoints. S.md keeps [P1]'s 𝓑_n
    (so c♯ is [T03R]'s), as the brief requires. S-a and S-b use wider brackets with different κ and c_IG. S-c's upper side
    needs n ≥ 4M+1; S.md's does not.
- **Scope remark (S-c §3).** The lemma fails if the design may depend on the noise. S.md's fixed-design hypothesis with (T, ϑ)
  design-measurable excludes this. Random-design consumers must condition on X with ε ⫫ X, which STATEMENT (RD) provides.
- **Where they disagree, who is right.** S-c's §2E says m < |T| forces (S-hyp) to fail. S.md says only m* ≥ 0. Both are true
  (S-c's is sharper), and no step depends on it.

**V.md vs V-a-1, V-b-1, V-c-1.**
- **Statement and definitions.** D′, ρ′ = (‖μ‖² + ‖θ*‖²)/n and the constant 1 + 2/η are identical in all four.
  - (b): V.md, V-b and V-c give the sharper rank exponent (r₀ + r_S)/2. V-a gives (s₀ + |S|)/2. All are consistent.
- **Shared step (a).** The same Young shift in all four, with the same constants. V-c Attack 3 shows that 1 + 2/η cannot drop
  below 1 + 1/η, so the constant is near-optimal.
- **Step (b), determinant comparison.** V.md, V-a and V-c use FFᵀ/FᵀF and Weyl. V-b uses a convolution identity (𝓘 ≤ 1 for
  Σ₁ ⪰ Σ₀ ⪰ I) and needs neither Weyl nor the order fact.
  - I re-derived V-b's P4 (Σ₁ − Σ₀ = n(c − 1/c)Z_SA_S⁻¹Z_Sᵀ + (n/c)(Z_SA_S⁻¹Z_Sᵀ − Z₀A₀⁻¹Z₀ᵀ) ⪰ 0) and its 𝓘 computation; both
    are correct.
  - The two routes give the same inequality det(I − D′) ≥ D^{(c)}_{S₀}/D^{(1/c)}_S.
- **Only discrepancy.** H1 and V-b say R₀ has eigenvalues in (0,1]. V.md and V-a say (0,1). (0,1) is correct, because
  1 − h_c(g) < 1 for g > 0. Immaterial.
- **V-c §3 items.** (1) A sharper form of (b), consistent with V.md. (3) (L₀) cannot replace ρ′: see C-7. (4) No surcharge
  inside the moment: consistent with V.md V.1. (5) (b) and (c) cannot be chained inside an expectation: consistent with
  X12 F6 and F7, which use (c) only pathwise on 𝓔_t.

---

## 5. Check script
- `c_checks.py` matches the files' formulas: the D^{(a)} eigen-formula, M^{(a)}, the (4.1) assembly by enumeration using w
  in place of ϖ (W_K cancels), and the 𝓔_t components.
- Its output is consistent with the claims.
- It is a falsification check only. My own worst-case-e check of V(a) is stronger than its random-draw check of (a) and
  agrees with it.

## 6. Summary of findings
| id | severity | file / section | one line |
|---|---|---|---|
| C-1 | MINOR | S.md Cor. S.1 | n_S ≥ e^{(2C_S+1)²} ≥ e^{121}: correct but vacuous; add the form t ≥ max{log n, (2C_S+1)²} for n ≥ max{3, 2s₀^r, 4C_S²} |
| C-7 | MINOR | STATEMENT §0 (outside files) | "(C) used only through (L₀)" is false for Lemma V(a)/X4 (131.6τ² vs L_{S₀} ≈ τ²); restrict the sentence |
| C-2 | NIT | S.md Step 7 nesting | Θ^{(1)}_{m*} undefined if R^T_{m*} = 0; take the sure event |
| C-3 | NIT | S.md Cor. S.2 | "equivalently" form also needs ct ≤ n^{1−κ₀} and n ≥ n_S′ |
| C-4 | NIT | S.md R^T_m | note that summing to K is the weaker hypothesis (both readings covered) |
| C-6 | NIT | STATEMENT §3 Lemma V | write Q^c, not Q (scale) |
| C-8 | NIT | X12.md F4(c) | the n₀ for t ≤ N/800, |S|ℓ_p ≤ N/13 on the range is not stated |

No CRITICAL or MAJOR finding. Every inequality, constant, probability bound and citation in S.md, V.md and X12.md was
recomputed. The one exception is the ROUTES remark in the X12 header, which was not checked.

## 7. Verdicts
- Lemma S (S.md, incl. Corollaries S.1–S.2): **VERIFIED-WITH-AMENDMENTS** (C-1 to C-4)
- Lemma V (V.md): **VERIFIED**
- Lemma X1 (X12.md): **VERIFIED**
- Lemma X2 (X12.md): **VERIFIED**
- Facts F1–F7 (X12.md): **VERIFIED** (C-8 NIT)

**Overall verdict: VERIFIED-WITH-AMENDMENTS. No mathematical error in stream C. The amendments are range and n₀ statements
(S.1, F4(c)), two NITs in S.md, and two STATEMENT-text corrections (C-6, C-7). Ready for the cross-family line check.**
