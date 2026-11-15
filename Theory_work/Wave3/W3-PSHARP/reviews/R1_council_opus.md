# W3-PSHARP — council R1, seat `opus` (Claude Opus 5.5, effort high; blind first read)

Content reviewed: the frozen manifest `ce522b1f5ea1ec7ae390559678e4e58eb35a38d6248e59bd590148739a0ebb6a`. I re-hashed every
file listed in `reviews/MANIFEST_R1.txt`, including the eight external inputs. All digests match, and the working tree
was clean before I started. Read: the manifest files, `reviews/INPUTS.txt`, the eight inputs it lists, and
`Scripts/SMC_BVS/core/cpp/v3_score.h` lines 40-71 and 196-224. Not read: any other file under `reviews/`, `LOG.md`,
`CHECKPOINT_*.md`. Scratch code: `reviews/R1_scratch_opus/check_constants.py` and `rerun.py`.

## Summary

All four proof files are correct. I re-derived every identity, inequality and constant by hand, and I re-checked the
numerical constants independently (see G5). I found no counterexample and no gap in a proof. The findings concern
wording and labels: one sharpness label in the registry is inflated, one numerics sentence in the REPORT lacks a
qualifier, and there are a few small notation and wording issues.

## Gate verdicts

### G1 correctness — PASS
- **Lemma V.** The penalty identity G + (G + I)/n = H/n holds, the minimiser is nH⁻¹z, and Q ≥ 0. The s_y-scaling
  holds.
- **Lemma S(1).** The bottom-right entries are (n+1)(n−1) + 1 = n² and n. The Schur complements are right. The
  eigenvalue of (n+1)²H⁻¹ − nA⁻¹ has numerator (n+1)²(λ+1) − n((n+1)λ+1) = (n+1)λ + n² + n + 1 > 0. So the D ratio is
  at most n, with equality iff g = 0. The iteration to n^{|J|} uses no membership in Ω.
- **Lemma S(2).** The block-inverse step gives v₂ − hᵀH⁻¹v₁ = x_jᵀρ̃_S and d − hᵀH⁻¹h = s.
- **Lemma S(3)–(4).** The prior ratio is C(2p−1,s₀)/C(2p−1,s₀+1) = (s₀+1)/(2p−1−s₀), and −log(1−γ) ≥ γ.
- **Claim A, Lemma W.** The Chebyshev constant is (1+η′)√π/(2ϵ′²(1−η)²√log N). The χ²₁ truncated mean
  √(2τ/π) is exact.
- **Claim A, sphere case (ii).** The bounds hold:
  - c_d√(2π) ∈ [(d−1)/d, √((d−1)/d)], via Gautschi through log-convexity;
  - −x − x² ≤ log(1−x) on [0, ½];
  - the exponent window is [−τ²/(2d), 3τ/(2d)].

  I checked them numerically by quadrature for d from 3 to 10⁵: the worst ratio is 0.999997 ≤ 1.
- **Claim A, Lemma R.** The chain (1−ϵ)e^{ϵ/2} ≤ 1 − ϵ/2 ≤ (1−ϵ/4)² holds on (0, 1).
- **Claim A, (W-orth) proof.**
  - s = n² and x_jᵀρ̃ = x_jᵀε/s_y.
  - κ_n = 2ν(n−1)σ*²/(nV), and V ≤ σ*²E(1 + 0.04/(n−1)) + 1.06M + M′.
  - With x = n^{1/4}, r·2 log N ≤ 2C_σn^{−1/4} log n → 0.
- **Claim A, (W-sph) proof.**
  - P_H = Σe_iv_iv_iᵀ.
  - Q − ‖ρ̃‖² = yᵀP_Hy/(n+1) + yᵀP_H(I−P_H)y, which uses 2 − n/(n+1) = 1 + 1/(n+1).
  - e_i(1−e_i)λ_i ≤ 1/(n+1).
  - E₁ ~ χ²_{r₀} and E₂ ~ χ²_{n−1−r₀}.
  - The three events have the stated probabilities, and m ≥ n/2 because s₀ + 1 ≤ K ≤ n/2.
  - C₀ is right, and the choice x_n = √(n/((r₀+1)log N)) gives (1−κ′)2 log N ≤ 2C₀ log N/n + 4√((r₀+1)log N/n).
  - The conditional law of the ζ_j does not depend on ε, so the ζ_j are iid unconditionally. Lemma R needs no
    independence between κ and the ζ_j.
- **Corollaries A1 and A2.** x/(1+x) ≥ x(1−x) is used correctly. The subsequence arguments in A2(i) and A2(ii) are
  valid.
- **Claim B.** The product of the prior ratio and C(p−s₀, j) is C(s₀+j, j)Π(p−s₀−i)/(2p−1−s₀−i). The constants (i)–(iv)
  hold; in particular (s₀+1)(p−s₀) − (2p−1−s₀) = (s₀−1)(p−s₀−1). At the critical scale the j-th term tends to
  (λ/2)^j/j!, and Fatou applies termwise. Numerically, at λ = 1 and λ = 4 the partial sums reach 0.64882 (limit
  0.64872) and 6.3898 (limit 6.3891). B2's step a_n ≤ 2Cρ_n is valid.
- **Claim C.** Every step checks:
  - (F1)–(F4) hold, and θ = (b/(η√k))(1, −1/c) represents μ exactly.
  - Lemma P: min_x A(β+γx)² + x²/n = Aβ²/(1+nAγ²), and nAγ² ≤ k/n² ≤ 1.
  - q_j ≤ (2/3)2^{−j}.
  - det G_T = (n−1)²η²k/(1+η²k), and D_T ≤ 2n.
  - Step 2: the inequality 2ab ≤ a²/2 + 2b² is applied correctly.
  - Step 3 holds.
  - Step 4: Δ ≥ 0.111nb², the denominator is at most 2nV₀, and log(1+x) ≥ 0.975x on [0, 1/20].
  - Step 5: the prior ratio is at most 2^{2p−1}, D_{T′} = n^k, D_S ≥ 1, and the count is at most 2^p.
  - The final constant holds because 1/42 − 1/100 = 0.01381 ≥ 1/73.

  In 50-digit arithmetic at n = 200, k = 64, min_ϑ B_T/(b²(n−1)) = 0.9992, inside the claimed [½, 1]. Over 25 random S
  with |S| ≤ k/2, the smallest L_S/((n−1)b²/4) is 2.13 ≥ 1.

### G2 hypotheses used = stated — PASS
- Each proof uses exactly its statement's hypotheses:
  - Lemma S uses only the definition of π and |S| + 1 ≤ K.
  - Claim A uses G, (E), (C), s₀ + 1 ≤ K, N_n → ∞, and (W-orth) or (W-sph) with its two rate conditions.
  - Claim B uses s₀ ≤ K − 1, and adds s₀ ≤ p/2 only for the 1/3 constant.
  - Claim C uses n ≥ 200 and nb² ≥ 1200V₀L².
- Every item of STATEMENT v1.2.1 is covered:
  - Lemma S(1)–(4).
  - Proposition A, including the uniformity and random-(X_{S₀}, θ*) clauses (§5).
  - A1 and A2.
  - Corollary B with B1 (including the critical scale), B2 and B3; B3 is a reading of B1, B2 and A2.
  - Proposition C, items 1–3, and the "what fails" paragraph.
- Remark A3 is correctly marked "not part of the claim". Its hypothesis check against [W3P] §2 and Cor-1R holds:
  - (i): φ₀ = 1, g₀ = 1 and A = 1 are valid, and M′ = ‖θ*‖²/3 is valid for n ≥ 3.
  - (ii): Cx^r_j ~ N(0, C) is rotation-invariant in 1^⊥. The bound ‖μ‖² ≤ s₀(n−1)‖θ*‖² gives M = s₀M′(n−1)/n.

### G3 no hidden assumptions — PASS
- **Randomness.** What is random is explicit. In (W-orth) only ε is random. In (W-sph) it is ε and the null block,
  with X_{S₀} and θ* fixed. §5 conditions on (X_{S₀}, θ*).
- **Columns outside S₀ ∪ 𝒩_n.** They never enter the lower bound. Lemma S(4) sums only over 𝒩_n, and each term
  depends on (X_{S₀}, x_j, y, p) only.
- **Empty S.** S = ∅ is handled.
- **s₀ = 0.** It is handled: Claim B covers it and Lemma S allows S = ∅.
- **Rank deficiency.** It is handled through r₀ = rank X_{S₀}, and Lemma S(1) needs no rank condition.
- **Uniformity claims.** They match the bounds' dependence: (ϵ, (M+M′)/σ*², n, N_n) under (W-orth); additionally
  (r₀+1)log N/n and (log N)²/n under (W-sph).
- **Domain of Claim C.** The admissibility condition nb² ≥ 1200V₀(log n)² with b ≤ b̄ can only hold once
  n ≥ 1200(1 + σ*²/b̄²)(log n)², which needs n ≳ 1.8·10⁵. So n₀ = 200 is never the binding constraint (NIT-6). This is
  not hidden: the statement says "n large", and every bound is proved for all n ≥ 200 anyway.

### G4 statuses and citations — PASS (one MINOR label finding)
- The status "PROVED (by this seat, unchecked)" is given verbatim in all four lemma files and in the registry blocks.
- No parent result is presented as proved here. Remark A3 and REPORT §1(a) say "conditional on" Thm-1 and Cor-1R.
- The boundary numerics are described honestly: one-step evidence only, with the full conclusion "not established".
- All cited ranges I checked say what is claimed:
  - [W3P] 16-39 and line 104 ("conjecture");
  - [W3P] 63-76 for (F_λ), (F_w), BM;
  - [W3P] 106-118 for LSF;
  - [L1a′] lines 10-16 and Remark 2 (line 50, "open");
  - [LB] lines 25 and 28;
  - W3-POST REPORT:190 (item 8);
  - [P2S] line 44 for B_T;
  - [1a″] lines 7-14 and line 10 for A^T_m;
  - P2S A2 at lines 58-62.
- The "what fails" reading of Lemma 1a′ and Lemma 1a″ is accurate:
  - Θ^T_{n,m_n} ≥ (1 − e^{−c₁nb²})n²/((n+1)√n) and Θ″ ≥ (1 − e^{−c₁nb²})n/2.
  - For each n, 1a′ applies with M′_n ≍ b²n³/k and becomes vacuous; it is not contradicted. [KBC-2] is stated
    correctly.
- MINOR-1 below concerns the registry label NECESSARY.

### G5 constants and rates — PASS
- **Λ_n and the 1/√π constant.** Λ_n = P_n n^{−1/2}N√(2τ/π) = (s₀+1)[2N/(2p−1−s₀)]√(log N/(πn)) checks out. The
  constant 1/√π is the exact truncated mean 2√(log N/π) of e^{χ²₁/2} at level N. This is also the right first-order
  size of the sum: the tail is ~1/(w√(π log w)), so the sum is relatively stable. The lower bound therefore has the
  right constant, consistent with the numerics' ratio → 1.00.
- **c(p, s₀), 𝒪^{lb}_n and e^{−λ/2}.** All verified (see G1).
- **Claim C constants, exact k = ⌈12 log n⌉, every integer n in [200, 2·10⁴], plus 4,000 log-spaced n up to 2·10⁶.**
  Zero violations of:
  - p ≤ ⌊n/2⌋ and k + 1 ≤ n − 1;
  - exact n²R^T_{⌊k/2⌋} ≤ 1 and the 3.78(12L+3)²n^{−2.158} envelope ≤ 1;
  - D_T ≤ 2n and A^T_{m_n} ≤ n^{−1/2};
  - (3p−1)log 2 + (k/2)log n ≤ 12L²;
  - 4(k+1)/(1200L²) ≤ 0.0078, (n−1)/(8n) ≥ 0.1243 and 1/n ≤ 0.005.

  Beyond 2·10⁶ the proof's monotone envelopes apply. The constants c₁ = 1/(73V₀) and C_b = 1200 are confirmed.

### G6 fidelity to the coded target and to the numerics — PASS
- **Coded target.** In `v3_score.h:40-71` and `196-224`: K = min(p, n/2) (integer), ν = a₀ + n/2, log w(k) =
  −log 2 − log C(2p−1, k), Q = yᵀy − n zᵀH⁻¹z with H = (n+1)G + I, and log m = const − ½(log det H − log det A) −
  ν log(2b₀ + Q). This is exactly [W3P] §0 and `numerics/core.py`. W_K and log C_n cancel in every ratio used.
- **Validations re-run (seeds as in the scripts).** I re-ran a_orth V1, c_counter V1 and E2, and b_check F1 and T1;
  every number agrees with the frozen outputs (1.37e-13; 1.9e-13 and 1.4e-15; 3.564e-04 and so on; 8064 pairs, 7.8e-13;
  T1 identical).
- **Reductions checked by reading.**
  - a_orth's Gamma-mixture identity (1−x)^{−ν} = E e^{xc*t} with the elementary-symmetric DP.
  - a_sph's exact-in-law reduction: projections of Cx^r_j on span(X_{S₀}, ρ̃) are iid N(0, I_{s₀+1}), and the
    remainder is χ²_{n−2−s₀}.
  - c_counter's control arm: a₁ = √(n−1)(b/2)(1+c) + g and a_j = −√(n−1)(b/2)cη + g_j.
- **Numbers quoted in the REPORT.** They match the outputs: 0.97–1.09; 1.003 and 1.007; ≥ 0.93 and ≥ 0.99; 0.71, 0.72
  and 0.61; 55,740 cases with minimum 1.033; 0.1353. The exception is MINOR-2.

## Findings

**FATAL:** none. **MAJOR:** none.

**MINOR-1 (G4, inflated sharpness label).** `REPORT.md:161` registry `sharpness: A:COEF-REP = NECESSARY` and
`REPORT.md:108` ("**NECESSARY** (in kind)").
- What Proposition C proves is a failed removal: exact representation by T plus (E), with no coefficient control,
  does not give the conclusion.
- The coefficient bound ‖θ‖² ≤ nM′ itself is *not* necessary for Lemma 1a′'s conclusion. Lemma 1a″ with any
  bounded-cost ϑ gives it, because A^T_m ≤ R^T_m(n+1)^{t/2}√n, so Θ^T ≤ Θ″.
- Concrete case. Take T = {1, 2} with corr(x₁, x₂) = 1 − n⁻⁴ and μ = L(x₁ − x₂), L² = n³/2. Then ‖μ‖² ≈ 1, so
  B_T(0) = O(1), while ‖θ‖²/n = n² → ∞. Here 1a′'s conclusion holds although its hypothesis fails for every fixed M′.
- The same REPORT already uses FAILED-REMOVAL for the identical kind of evidence on A:POST2-AR (`REPORT.md:109`).
- **Correction.** Replace with `A:COEF-REP = FAILED-REMOVAL (evidence: lemmas/C_counterexample.md:100)`. In §4, write
  "FAILED-REMOVAL: some ridge-cost control is necessary; the bound ‖θ‖² ≤ nM′ itself is weakenable to 1a″'s bounded
  cost". Optionally add the same parenthesis after "necessary in kind" at `STATEMENT.md:140` and `REPORT.md:56`.

**MINOR-2 (G6, scope of a numerics sentence).** `REPORT.md:97` says "π(|S| > cutoff) = 1.000 for n ≥ 100 on the
counterexample arm".
- That holds only for the b = 3 rows.
- `c_counter_out.txt` has b = 1 (n = 400) with median 0.949 (min 0.372), and b = 0.5 (n = 1600) with median 0.466
  (min 0.0078).
- `C_counterexample.md:118` states the qualifier correctly.
- All E1 rows lie far below the theorem's signal condition; for example nb² = 14,400 at n = 1600, b = 3 against
  1200V₀(log n)² ≈ 6.5·10⁵.
- **Correction.** Write "(b = 3; at b = 1 and 0.5 the medians are 0.95 and 0.47 — all rows are far below the
  theorem's constant C_b, they show the mechanism only)".

**NIT-1.** `STATEMENT.md:109` says "With log p = o(log n) the rate r_n can survive a slowly growing s₀". This is an
existence assertion that nothing in this folder proves. Reword to "the obstruction does not apply when log p =
o(log n); no claim is made there", or mark it as a reading.

**NIT-2.** `ASSUMPTION_MAP.md:12` contains the garbled phrase "(W-orth: = o(√n)-free, see proof)". Replace it with
"both witnesses need only (M + M′) log N_n = o(n)", which is what §3 and §4 give.

**NIT-3.** `numerics/b_check.py:51` (F1 header) prints "equality iff orthogonal", but F1 checks only (D_{S⁺}/D_S)/n ≤ 1,
not the iff. Drop "iff" from the printed header or add the check.

**NIT-4.** Notation clashes:
- `lemmas/A_log_factor.md:65-68` writes r_n(x), which clashes with r_n = √(log n/n). Rename it e_n(x).
- `lemmas/C_counterexample.md:72` uses P := ‖P_𝒳ε‖²/σ*², which clashes with the probability P. Rename it E_𝒳.

**NIT-5.** `REPORT.md:149` (registry "rate: (s0+1)/(2 sqrt n)") and `ASSUMPTION_MAP.md:21` give the rate as
(s₀+1)/(2√n). The proved bound is c(p, s₀)/√n ≥ (s₀+1)/(3√n) for s₀ ≤ p/2, and it tends to (s₀+1)/(2√n) only as
s₀/p → 0. Add "(as s₀/p → 0)".

**NIT-6.** `STATEMENT.md:118-122`: say that 𝔇_n is admissible only once n ≥ 1200(1 + σ*²/b̄²)(log n)², so n₀ = 200
only fixes the range of the elementary bounds.

## Score

9.0. The mathematics is correct throughout, re-derived step by step and checked numerically, and it is honestly
reported. Remaining issues: one inflated registry label (MINOR-1), one numerics sentence missing a qualifier
(MINOR-2), and six NITs.

COUNCIL-VERDICT round=R1 manifest=ce522b1f5ea1ec7ae390559678e4e58eb35a38d6248e59bd590148739a0ebb6a seat=opus score=9.0 gates=PASS
