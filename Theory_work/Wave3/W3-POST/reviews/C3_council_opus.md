# W3-POST — Council C3 (final round), seat B (Claude Opus 5.5, high, claudeAgent)

Date 2026-11-09. I was briefed to break the package. Earlier verdicts, dispositions and status lines were treated as
claims to check, not as evidence: every item below was re-derived from the sources or re-computed. Writes: this file and
`reviews/C3_scratch_opus/` only. No git state changed, no subagents.

**Verdict: PASS for this seat. Gates G1–G6 all PASS. Score 8.7 / 10 (uncapped).**
Counts: **0 FATAL / 0 MAJOR / 2 MINOR / 8 NIT.** No step of any formal claim is false or unsupported. The two MINOR
findings are a REPORT summary that drops the noise–design independence hypothesis (F1) and a review-trail
transparency gap (F2). Both are text fixes.

## 0. What I read and ran

**Read**
- Package: STATEMENT.md (v1.3 + C2 edits), lemmas/L1a_size_tail.md, lemmas/LB_rate_lower_bound.md, ASSUMPTION_MAP.md,
  REPORT.md, LOG.md, PLAN.md, citecheck.py, numerics/*.py, and all three output files.
- Review trail: C1/C2 reviews and dispositions, in full; R01/R02 verdict tables.
- Proof chain:
  - [T03R] PROOF.md, all of it (§1 E1–E3, §2 T02(i♯) + Lemma den′, §3 Prop D, §4 Lemma B, §5 T02(ii♯), §6 T03♯ C1–C10).
  - [P1] PROOF_v3.tex: `lem:slab`, `lem:spec`, `lem:prior`, `lem:chi`, `prop:closed`, `thm:T01i`, `thm:T01ii`,
    `thm:T01iii`, `thm:Ta`, `lem:num`, `lem:den`, `thm:T02i`.
  - [P3] PROOF_v2.tex: the definition of C_* (l. 194), `lem:signalgain` (l. 304-311), and the BM constants (l. 344-385).
  - [POST] L1_POST.md:1-80, [SL] I4_SL_corollaries.md:1-70, [UNI] STATEMENT.md:85-92.
  - Registry card `State_of_Project/sections/04_theory.tex:765-795`.
- Code: `v3_score.h:1-72, 170-230` and `v3_preprocess.R:100-130`.
- Literature (via pdftotext, in `C3_scratch_opus/lit/`): Song–Liang printed pp. 951-956; NH14 arXiv pp. 5-6 and 10-13;
  YWJ16 arXiv pp. 6-9.

**Ran** (outputs in `reviews/C3_scratch_opus/`; `-B`, no bytecode written)
- `lb_check.py` → `lb_check_rerun.txt`: **identical** to `numerics/lb_check_out.txt` (34 920 pairs, min 1.012988).
- `lb_domain.py` → `lb_domain_rerun.txt`: **identical** to `numerics/lb_domain_out.txt`.
- `post_exact.py` (full, 19 s) → `post_exact_rerun.txt`: **byte-identical** to `numerics/post_exact_out.txt`.
- `citecheck.py` copy redirected to scratch → `CITECHECK_c3.txt`: 53 checks, 0 failures, **identical** to
  `reviews/CITECHECK.txt`.

## 1. Verification record (independent)

### Lemma 1a (= T02(i♯)) — correct, hypotheses exact
- **Statement.** STATEMENT:42-49 matches [T03R]:76-85 exactly: the constants b±, κ, c_IG, C_Λ (with 1{s₀ ≥ 1} and the
  (1 + 1/(2φ₀²))(M + σ*²) term) and c♯ = κ²/(c_IG σ*²), the display, and the consequence
  (1 + 1/n)^{s₀/2}e^{−ω}Θ♯.
- **Hypotheses.** I traced the proof ([T03R]:93-97 → [P1] `lem:num`, `thm:Ta`, `thm:T01iii`, `lem:den`). It uses
  exactly G, ‖μ‖² ≤ nM (through 𝓑_n and b₊), λ_min(R_{S₀}) ≥ φ₀² (only in `lem:den`'s bound on Q^c_{S₀}) and s₀ ≤ K
  (so that S₀ ∈ Ω in `thm:Ta`). This matches [T03R]:99 and STATEMENT:43-44. p ≥ 2 is a standing convention of
  [T03R]:9; it is not used.
- **Status.** The quotation "T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED" is verbatim at `04_theory.tex:771`.

### Lemma 1a′ (new) — correct line by line
- **Changed step.**
  - `lem:slab` gives Q = min_ϑ{‖Y − Aϑ‖² + ϑᵀ(G + I)ϑ/n}.
  - With Y = y_c = Uᵀμ + ε_c (`thm:T01iii`) and X_{c,T}θ = UᵀX_Tθ = Uᵀμ, the choice ϑ = θ gives
    Q^c_T ≤ ‖ε_c‖² + (‖Uᵀμ‖² + ‖θ‖²)/n.
  - ‖Uᵀμ‖ = ‖μ‖ because μ = Cμ.
  - So ρ ≤ M + M′ holds deterministically, with no rank or floor needed. It also holds for T = ∅ (μ = 0).
- **Rest of `lem:den`.** The exponent bound in [P1] (`lem:den`, "Lower bound on the exponent") uses only
  Q^c ≤ σ*²E′ + (a nonnegative term). Hence E Λ′ ≤ √(2n)/(2√n) + (n−1)/(2n) + (M + M′)/(2σ*²) ≤ C′_Λ.
  D_T ≤ (n + 1)^t holds by `lem:spec`(e), with no condition.
- **Assembly.** v_m = ϖ(E_m) = R^T_m ϖ(T). The ϖ(T) factors cancel, which gives
  Θ^T ≤ κ²e^{Λ′}Θ^{(1)}/(c_IG σ*²) = c♯e^{Λ′}Θ^{(1)}. Then:
  - Markov on Θ^{(1)} (with E Θ^{(1)} = 1 by `lem:num`, since b₋ is data-free);
  - Markov on Λ′ ≥ 0;
  - P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n − 1).
  Together these give the display. The bound depends on X only through (M, M′), so it is uniform. ✓
- **Headline (STATEMENT:54-57).**
  - ‖Xθ*‖² ≤ (n−1)(Σ|θ_j|)² ≤ (n−1)s₀²θ_hi².
  - ‖θ*‖² ≤ s₀θ_hi² ≤ nθ_hi²/2, because s₀ ≤ K ≤ n/2.
  - So M′ is fixed even for growing s₀. The caveat that (E) is real for growing s₀ is present. ✓
- **Remarks.**
  - Remark 1: F0 ∧ E ⇒ ‖θ*‖² ≤ nM/((n−1)φ₀²) ≤ 1.5M/φ₀².
  - Remark 2: the near-collinear signal part is 2L²g(g+1)/((n+1)g+1); I re-derived it from M = h(XXᵀ).
  - Remark 4: E2(ii) with ω = ½ log n, using log C(p, t) ≤ t log p.
  All three check.

### Theorem 1 items 1-5 — hypotheses used = hypotheses stated
- **Items 1 and 5(b) = T03♯(i), (iv)** ([T03R]:162-175; registry `04_theory.tex:771, 780-788`, read verbatim).
  - The hypothesis set R1 + G + R + SE_λ(j₀) + SE_w(m♯_n; g₀) (+ BM) equals STATEMENT R1 + (E) + (F_λ) (J = ∅ gives
    R's floor) + (F_w) (+ BM).
  - BM-∞ "M_n → ∞" is equivalent to "θ²_min nφ₀²/(σ*² log n) → ∞".
  - c₀ = L_* = max{4C_*, 32[s₀(A+1)+2]}.
  - I checked (iv) without beta-min. (C10) uses only θ_j for the missing strong coordinate. The |J′| > j₀ part goes
    through (C6)(a) and Υ^{>j₀}, which need no beta-min and no floor on S′. The tail goes through (C9). ✓
- **Item 5(a) = T02(ii♯)** ([T03R]:147-149): "R1 under G, R and SE_w(m♯_n; g₀)" is exactly STATEMENT:86-87's reduced
  list. ✓
- **Items 2-4** were re-derived directly from δ (they equal [SL] SL0/SL1):
  - on {δ < ½}, HPM = S₀ for any tie rule;
  - {HPM ≠ S₀} ⊆ {δ ≥ ½}, so Markov gives the 2Eδ bound, and Eδ → 0 by bounded convergence;
  - ξ_{q_n} needs δ < min(q_n, 1 − q_n);
  - |PIP_j − 1{j ∈ S₀}| ≤ δ;
  - π(|S| = s₀) ≥ 1 − δ;
  - the supremum over [0,1]-valued h equals δ, attained at 1{S ≠ S₀}. ✓
- **Interlacing consequences** (STATEMENT:68-72). For |S| ≤ j₀, take J = S ∖ S₀. Then S ⊆ S₀ ∪ J, and R_S is a principal
  submatrix. ✓
- **c₀ arithmetic (ASSUMPTION_MAP:20, REPORT:138).** C_* = 2s₀ + 3[Aj_* + s₀ + log(j_* + 1) + 1] ([P3]:194). At
  s₀ = A = 1, j_* = 4, this gives C_* ≈ 24.8 and 4C_* ≈ 99.3 < 128. So "c₀ = 128 at s₀ = A = 1" is exact, and "32-64×"
  (128/4, 128/2) is right.

### Item 6 (interface form) and Corollary 1R — correct
- **Diagonal transfer.** Suppose sup_{x∈𝒜_n} P_ε(δ > C r_n) does not become small. Then there are n_k ↑ and
  x_{n_k} ∈ 𝒜_{n_k} with probability > η at C = k. Complete them with arbitrary points of 𝒜_n (nonempty eventually).
  The resulting deterministic R1 sequence has common constants, so this contradicts the fixed-design O_P.
  - This needs ε ⫫ (X, θ*) and |supp θ*| = s₀ on 𝒜_n; STATEMENT:94-95 states both.
  - s₀ ≤ K is automatic for n ≥ 2s₀, since S₀ ⊆ [p].
- **Corollary 1R vs [POST]:20-69.**
  - LSF (i)/(ii), m̄_n and k̄_n match verbatim.
  - Step (1): R_m ≤ 2(2p)^{s₀}(2/3)^m ≤ n^{−(s₀+2)/2} at m = m̄_n (re-derived). Hence m♯_n ≤ max(s₀, m̄_n), so every
    S₀ ∪ J has size ≤ s₀ + max(j₀, m̄_n) (as j₀ > s₀), i.e. ≤ k̄_n.
  - Step (3), Weyl: |S|·O(√(log n/n)) = O((log n)^{3/2}/√n) = o(ψ_n). This gives φ₀² = φ²/2 and g₀ = 1.
  - Step (4) uses θ_hi only. So part (b) (5(a)-(b) without θ_lo) is valid.
  - Status "PROVED (by this seat, unchecked)" is verbatim at L1_POST:3. UNI-P at [UNI]:87-91 is indeed the restatement.

### Item 7 / Proposition LB — correct, and essentially sharp
- **Odds identity.** The common factor and W_K cancel.
- **Prior factor.** w(s₀+1)/w(s₀) = (s₀+1)/(2p−1−s₀) by [P1] `lem:prior`(b).
- **Determinant factor.** D_S/D_{S₀} ≤ n + 1, re-derived by interlacing: D = Π f(λ_i), f increasing in [1, n+1), and
  λ_i(G_{S₀}) ≥ λ_i(G_S). So D_S/D_{S₀} ≤ f(λ_{k+1}(G_S)) < n + 1. No floor is needed.
- **Fit factor.** Q_S ≤ Q_{S₀} by `lem:spec`(d), so the fit factor is ≥ 1.
- **Summation.** The p − s₀ one-variable extensions are disjoint, so δ ≥ (p − s₀)r(1 − δ).
- **Monotonicity.** The derivative has numerator s₀ − 1 ≥ 0, and the value is 1 at p = s₀ + 1.
- **Conclusion.** δ ≥ 1/(1 + √(n+1)).
- **Tightness.** Take p = s₀ + 1, x_j ⊥ (X_{S₀}, y) and y ∈ span X_{S₀}. Then the odds are exactly n^{−1/2}, so
  δ ≈ 1/(1 + √n) and the constant is attained to O(n^{−1/2}) relative error.
- **Consistency with the numerics.** At E1 c = 8, n = 6400, δ = 0.0236 ≥ 1/81 = 0.0123. ✓
- **Domain.** The hypotheses used are exactly 1 ≤ s₀ < p, s₀ + 1 ≤ K and the coded π (s_y > 0). The domain is stated
  at STATEMENT:100-101, LB:76-83, REPORT:19-20, 67-70, 129, 175 and AM:124. Outside it the bound fails: at
  p = s₀ = 2, n = 20, δ = 6.5·10⁻¹⁰ (re-run). ✓

### G6 — fidelity to the code
- `v3_score.h`:
  - :14 has a₀ = b₀ = 0.01;
  - :40 has K = min(p, n/2) with integer division;
  - :57 has ν = a₀ + n/2;
  - :65 has log w(k) = −log 2 − lchoose(2p−1, k);
  - :181-182 has H = (n+1)G + I and A = G + I;
  - :217 has Q = yᵀy − n zᵀH⁻¹z;
  - :223 has log m = log C_n − ½(ldH − ldA) − ν log(2b₀ + Q).
- `v3_preprocess.R:111-127` drops constant columns before p is formed, and refuses a constant y (s_y > 0).
- STATEMENT §0 matches, and `post_exact.Post` implements the same score.
- The Q < 10⁻⁸yᵀy recomputation is floating-point only, which the package excludes explicitly.

### Numerical claims — every quoted number checked against the (reproduced) output
| Quote (where) | Output |
|---|---|
| E0 median δ√n ≈ 2.1-2.6 (AM:125, REPORT:131, LB Rem. 2) | 2.61, 2.07, 2.41, 2.61 ✓ |
| E1 c = 0.5, 1 fail, δ 0.93-0.99; log log n: δ ≥ 0.98 | 0.927-0.993; 0.9865-0.9976 ✓ |
| E1 c = 2: δ 0.66 → 0.13, δ/r_n 3.1-6.7; c = 4: 1.54 → 0.70; c = 8: 1.02 → 0.64 | 0.664 → 0.132, 3.09-6.74; 1.536 → 0.704; 1.020 → 0.638 ✓ |
| E2 δ/r_n 0.94 → 0.67, HPM 100% | 0.937 → 0.672; 1.00 ✓ |
| E3 HPM ≥ 95%, δ/r_n 0.81-1.12 | 0.95-1.00; 0.806-1.116 ✓ |
| E4 γ = .5: 1.08 → 0.64; γ = .8: δ .40 → .06, HPM wrong 10-20%; γ = 1: δ .37-.50, wrong 25-30% | all match ✓ |
| E5 c = .8: .26, .49, .82, .92, .988; c = .5: .10 → .57 | .257, .488, .820, .916, .988; .104 → .574 ✓ |
| E5 population λ_min ≈ 0.106 | 1 − 2a, a = √0.2: 0.1056 ✓ |
| L1a(b),(c) max ≤ 1.1·10⁻³; L1a′(e) ≤ 1.5·10⁻⁵ (Rem. 2: ≤ 2·10⁻⁵) | 1.040e-3; 1.419e-5 ✓ |
| LB 34 920 cases, min 1.013 | identical re-run ✓ |

The script respects the compute cap (P_DEF = 10, 20 seeds). The signal is generated after standardising X, so the θ
labels are literal.

**Leading-order sketches (labelled; I re-derived them).**
- R03 §5A, p = 3:
  - {3}: 2·0.9·0.75/2 − ½ = 0.175;
  - {1, 3}: 0.75·(1 + 0.45/0.55)/2 − 1 = −0.32;
  - S₀: −0.25;
  - Gram floor 1 − √0.9.
- E5:
  - {5}: 1.6c − ½ = 0.78;
  - {5, 1, 2, 3}: 3.5c/2 − 2 = −0.6;
  - margin ≥ 0.48.
- Deletion benchmark: the log-odds (√λ + Z)²/2 − log(2p/s₀) − ½ log n give n^{a+½−c/2}, with thresholds 2a + 1 and
  2a + 2. ✓

All of these are correctly labelled as heuristic or sketch, and none is used as a premise.

### Literature — checked against the PDFs (untrusted data; only quoted content compared)
- **Song–Liang.**
  - Theorem 1 (p. 952): |x_i| ≤ 1 and (8)-(14), including (10) r̄_n ln P_n ≺ nε_n².
  - Theorem 2 (p. 953): Condition 1, (9)-(14), (4) and r_n ≻ 1.
  - Corollary 1: P_n < exp(Cn^α) and ε_n = O(n^{−(1−α)/2}log^{k/2} n).
  - Condition 2 (p. 954) concerns second moments and gives convergence in probability (16).
  - Condition 3 (p. 955): the eigenvalue sufficiency is stated for mean-0 bounded predictors, plus the standard-normal
    variant.
  - Theorem 3: "the specificity is not controlled" (p. 956).
  - The ridge prior uses c_n ∝ 1/n (p. 953).
  - The cap argument is right: (10) fails when K = ⌊n/2⌋. ✓
- **NH14.**
  - Conditions 4.1-4.5 are as printed, including ν < δ, κ < (K−1)δ/2, MNEV (p. 6), and the 4.4 residual-signal scale
    log(√n ∨ p_n).
  - Theorem 4.1 is for fixed σ² (p. 12).
  - Theorem 4.2 adds a dimension restriction and is correctly marked "not re-read". ✓
- **YWJ16.**
  - Prior (5) with the cap |γ| ≤ s₀; regime p ≥ n.
  - A-C as summarised: g ≍ p^{2α}, κ + α ≥ C₁(L + L̃) + 2.
  - D(s*) sets s₀ := p.
  - Theorem 1 uses D(s*) and gives π_n(γ*|Y) ≥ 1 − c₁p⁻¹ w.p. ≥ 1 − c₂p^{−c₃}.
  - Theorem 2 uses D(s₀). ✓

### C1 and C2 findings — each genuinely fixed (checked on disk, not from the dispositions)
- **C2A.**
  - F1: the LB domain appears at all six REPORT/AM sites.
  - F2: AM:77-78.
  - F3: AM:21.
  - F4: STATEMENT:35, L1a′:11.
  - F5: post_exact.py:140, 223.
- **C2B.**
  - F1: REPORT:12-13.
  - N1: items reordered.
  - N2: STATEMENT:95.
  - N3: AM:15.
  - N4: AM:21 is one row with escaped pipes.
  - N5: recorded.
  - N6: LB:69-72.
  - N7: `lb_domain.py` added; Wainwright marked "recalled".
- **C1.**
  - A-F1/F2/F3: literature verified above.
  - A-F4: REPORT:42-46, 72-74.
  - A-F5/F6: script and output.
  - A-F7: item 6 is the interface form.
  - A-F8: AM:20.
  - A-F9: citecheck docstring.
  - B-F2/F4: labels.
  - B-F3: p ≥ 2 at STATEMENT:43, 62.
  - B-N5: STATEMENT:116-117.
  - B-N6: r_n ≻ 1 is printed on p. 953.
- All fixed.

## 2. Gates

| Gate | Verdict | Reasons |
|---|---|---|
| G1 correctness of every step | **PASS** | Lemma 1a, Lemma 1a′, Theorem 1 items 1–7, Corollary 1R and Proposition LB each follow from the cited steps (re-derived above). No heuristic, sketch or conjecture is used as a premise. F1 is a summary omission in REPORT; the claim itself (STATEMENT item 6) is correct. |
| G2 hypotheses used = stated | **PASS** (F1) | The hypothesis sets match their sources: T03♯ ↔ items 1/5(b), T02(ii♯) ↔ 5(a), T02(i♯) ↔ Lemma 1a. L1a′ uses only G, the representation, T ∈ Ω and (M, M′). LB uses only 1 ≤ s₀ < p and s₀ + 1 ≤ K. Corollary 1R matches [POST]. REPORT drops ε ⫫ (X, θ*) in its item-6 and Corollary 1R summaries (F1, MINOR; see there why this is not a gate failure). |
| G3 no hidden assumptions | **PASS** | Retained p, s_y > 0, n ≥ 3, ε ⫫ (X, θ*), \|supp θ*\| = s₀ on 𝒜_n, the raw vs standardised conventions and positivity of the constants are all explicit in STATEMENT. |
| G4 cited lemmas have adequate status | **PASS** | Registry statuses are verbatim (`04_theory.tex:771`) and the [POST] status is verbatim. The new L1a′ and LB keep "PROVED (by this seat, unchecked)", each with a cross-family line check (R01; C2 seat A) and a falsification run. Prop D and E3 are used only in remarks and the sharpness record (N6). Nothing is upgraded; N4 is wording only. |
| G5 constants/rates tracked | **PASS** | C_Λ, C′_Λ, c♯, the 𝓑_n bound, R_m and the cutoff bounds, c₀ (= 128 at s₀ = A = 1, verified from C_*), LB's constant (sharp to O(n^{−1/2})), the deletion thresholds 2a + 1 and 2a + 2, and the √log n gap (labelled conjecture) are all tracked. |
| G6 fidelity to the method as coded | **PASS** | §0 matches `v3_score.h` and `v3_preprocess.R` line by line. The numerics enumerate the coded score and reproduce byte for byte. |

**Score 8.7 / 10.** The mathematics is clean, the hypotheses are exact, the numerics reproduce, the literature
summaries are accurate, and every earlier council finding is genuinely fixed. Points are lost for the REPORT-level
omission F1, the silent review-layer substitution F2, and the stale and loose wording N1-N8.

## 3. Findings (0 FATAL / 0 MAJOR / 2 MINOR / 8 NIT)

**F1 — MINOR — REPORT.md:66-67 and 72-74 (item 6 and Corollary 1R summaries drop noise–design independence).**
- **What is missing.**
  - Item 6 reads: "Interface form for random (X, θ*): if (E), (F_λ), (F_w) and (BM) hold on events of probability → 1
    with common constants, then 1–4 hold under the joint law".
  - The Corollary 1R summary likewise omits "ε independent of the design".
  - STATEMENT:94-95 and 106 state "ε independent of (X, θ*)", "(X, θ*)-measurable events" and "|supp θ*| = s₀". This
    hypothesis is load-bearing, because the diagonal transfer needs the conditional law of ε given X to be N(0, σ*²I).
- **Why it matters.** Read literally, the REPORT sentence is false. Take p = 2, iid N(0, 1) raw columns, β* = (1, 0)
  and ε := σ*x₂^r. Then ε ~ N_n(0, σ*²I) marginally (so G holds), and (E), (F_λ), (F_w) and BM all hold w.p. → 1. But
  {1, 2} fits y exactly, so π(S₀) → 0.
- **Why MINOR, not a gate FAIL.** The claim of record (STATEMENT item 6, Corollary 1R) carries the hypothesis. In a
  random-design regression summary, "Gaussian noise" is conventionally read as independent of the covariates (all three
  cited papers use that convention). Unlike C2A-F1, the omitted condition is not a regime a reader would naturally take
  to be included. It must still be fixed, because REPORT feeds the INFRA registry.
- **Fix.**
  - REPORT:66: "Interface form for random (X, θ*), with ε independent of (X, θ*): if on (X, θ*)-measurable events of
    probability → 1, |supp θ*| = s₀ and (E), (F_λ), (F_w), (BM) hold with common constants …".
  - REPORT:72: add "iid raw rows N(m, Σ_n), ε independent of the design".

**F2 — MINOR — REPORT.md:76-86 (review trail; Wave1 PROTOCOL final-report item 4, Wave3 PROTOCOL:3-5).**
- The protocol's layers are a statement lock, lemma checks, a mid-point and an exhaustive sweep, and the final report
  must give the "statement-lock verdict; … mid-point verdict; sweep counts".
- The trail lists none of these. PLAN.md:4-6 replaced them by the R01/R02 adversarial re-checks, which is reasonable for
  a re-check ticket of already-verified results. But the REPORT does not say so, so a reader cannot tell whether the
  layers were skipped or substituted.
- **Fix:** one sentence in §2: "Statement lock, mid-point and exhaustive sweep were replaced by the two independent
  adversarial re-checks R01/R02 (PLAN step 2); no separate mid-point was run (HQ to confirm)."

**N1 — NIT — STATEMENT.md:1, 4-5; ASSUMPTION_MAP.md:1 (stale scope and version).**
- STATEMENT says "it proves nothing new except Lemma 1a′", but Proposition LB is also new.
- STATEMENT's version line is "v1.3 … = council C1" although C2 edits are in the file ([C2A-F4] at l. 35, [C2B-N2] at
  l. 95). AM's version line has the same problem: "v1.1 (council C1 …)".
- **Fix:** "… except Lemma 1a′ and Proposition LB"; bump to v1.4 / v1.2, "C2 amendments".

**N2 — NIT — REPORT.md:187-192 (Files).** The list omits `reviews/C2_*`, `R01/R02_disposition.md` and the C3 files.
**Fix:** "`reviews/R01*`, `R02*`, `R03*`, `C1_*`, `C2_*`, `C3_*`".

**N3 — NIT — REPORT.md:144.** "What matters is θ²_min·n·φ₀²/log n." is stated as fact. AM:18 has the right wording:
"Consistent with BM in product form … which the proof does not allow".
**Fix:** "(numerical trend, not proved)".

**N4 — NIT — REPORT.md:129, ASSUMPTION_MAP.md:123 (status wording).** "(proved)" and "**Proved lower bound**" sit
beside results whose status word is "PROVED (by this seat, unchecked)". The contrast with "heuristic" is legitimate,
but the bare word can read as an upgrade.
**Fix:** "(proved; status PROVED (by this seat, unchecked), line-checked by C2 seats)".

**N5 — NIT — STATEMENT.md:109-111 (Corollary 1R(a), raw convention).** M = s₀²θ_hi² + 1 and the θ_lo envelope are
written in θ, but in the raw-slope case θ_lo, θ_hi are b_lo/2, 2b_hi on the sd-ratio event ([POST]:14). The pointer
to [POST] lines 12-18 makes this recoverable.
**Fix:** add "(raw case: θ_lo = b_lo/2, θ_hi = 2b_hi)".

**N6 — NIT — ASSUMPTION_MAP.md:22 (POST-DIM).**
- "needs m♯_n − s₀ ≳ (s₀A + (s₀+2)/2) log₂ n" holds for p ≍ n^A. [T03R] E3 gives s₀a with p ≥ n^a.
- The row also leans on Prop D and E3, which REPORT:103 lists as not checked by this ticket.
- **Fix:** "(p ≍ n^A; [T03R] E3/Prop D, not re-checked here)".

**N7 — NIT — REPORT.md:6-10 (RESULT line).** The protocol's one-line RESULT category (PROVED-CHECKED / PARTIAL / …) is
missing. It should be filled once C3 closes, e.g. "RESULT: PROVED-CHECKED (Theorem 1 chain re-checked; L1a′, LB new,
council-passed C3)" if both seats pass.

**N8 — NIT (optional) — lemmas/LB_rate_lower_bound.md:91-93.** The Schur form gives D_S/D_{S₀} ≤ n, since
b = uᵀ(I − P_A)u ≤ ‖u‖² = n − 1. So the bound improves to 1/(1 + √n). This is cosmetic, because the stated bound is
correct.

## 4. Bottom line
- I found no false or unsupported step in Theorem 1 items 1-7, Corollary 1R, Lemmas 1a/1a′ or Proposition LB.
  Hypotheses used equal hypotheses stated. Statuses are verbatim and not upgraded.
- All numerics and the citation check reproduce byte for byte. Literature claims match the PDFs. Every C1 and C2
  finding is genuinely fixed.
- Before the final REPORT: add ε ⫫ (X, θ*) to the two REPORT summaries (F1), state the review-layer substitution (F2),
  and tidy N1-N8.

**Gates G1-G6: all PASS. Score 8.7.**
