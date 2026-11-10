# W3-POST — Council C2, seat B (Claude Opus 5.5, high, claudeAgent)

Date 2026-11-09. I was briefed to break the package. I did **not** use earlier verdicts, dispositions or status lines as
evidence; I re-derived every item below from the sources. I did **not** read `C2_council_astra.md` or `C2_scratch_astra/`.

**Files changed during the round.** The package changed while I was reviewing it: STATEMENT, REPORT, ASSUMPTION_MAP,
L1a′ and post_exact.py all have 17:42–17:43 mtimes (LOG 17:55 entry: fixes after C2 seat A). This review covers the
files **as they stand at 17:43**. I re-read every changed passage in that state: the R_m zero-extension, the LB domain
qualifiers, the NH14 Cond. 4.5 parameters and the E5 "deterministic leading coefficients" sentence.

**Writes.** I wrote only this file and `reviews/C2_scratch_opus/`. No git state changed.

**Read in full or in the relevant part:**
- STATEMENT.md (v1.3), lemmas/LB_rate_lower_bound.md, lemmas/L1a_size_tail.md, ASSUMPTION_MAP.md, REPORT.md;
- numerics/post_exact.py with post_exact_out.txt, and numerics/lb_check.py with lb_check_out.txt;
- citecheck.py, reviews/C1_* (both seats and the disposition), LOG.md;
- [T03R] PROOF.md, lines 1–20, 40–56, 74–100, 140–175;
- [P1] PROOF_v3.tex `lem:slab`, `lem:spec`, `lem:prior`, `thm:Ta`, `lem:num`;
- [P3] PROOF_v2.tex `lem:det`, `lem:prior`;
- `v3_score.h` (K, a₀, b₀, ν, log w, H/A, log m) and `v3_preprocess.R:105-128`;
- Narisetty–He arXiv:1405.6545 (pp. 5–6, 10–13), Yang–Wainwright–Jordan arXiv:1505.07925 (pp. 6–9) and Song–Liang (2015)
  pp. 952–955. I extracted the text with pdftotext into my scratch folder.

**My own computations (in `reviews/C2_scratch_opus/`):**
- `lb_adv.py` → `lb_adv_out.txt`: adversarial near-tight cases for Proposition LB.
- `lb_outside.py` → `lb_outside_out.txt`: LB outside its domain.
- Re-run of `lb_check.py`: identical output, min 1.012988.
- Full re-run of `post_exact.py` → `post_exact_rerun.txt`: **byte-identical** to `numerics/post_exact_out.txt`.
- `citecheck_copy.py`, a copy redirected to my scratch folder → `CITECHECK_c2.txt`: 53 checks, 0 failures; identical
  to `reviews/CITECHECK.txt`.

---

## 1. Verification record

### Proposition LB (`lemmas/LB_rate_lower_bound.md`): correct, line by line, and essentially tight
- **Setup.** S := S₀ ∪ {j} ∈ Ω because |S| = s₀ + 1 ≤ K, and S₀ ∈ Ω too. With m ∝ D^{−1/2}(2b₀ + Q)^{−ν} and
  ϖ ∝ w(|·|) (W_K cancels), the displayed ratio π(S)/π(S₀) is exact. ✓
- **(i) Prior factor.** w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k), as in [P1] `lem:prior`(b) (PROOF_v3.tex:116,
  126). ✓
- **(ii) Determinant factor.** [P3] `lem:det` (PROOF_v2.tex:122-128) gives D_T/D_S ≤ (n+1)^j for S ⊆ T, with no rank
  condition. I also re-derived the direct Schur-complement proof:
  - det H_S = det H_{S₀}·[1 + (n+1)uᵀ(I − P_H)u] and det A_S = det A_{S₀}·[1 + uᵀ(I − P_A)u];
  - on col(X_{S₀}) the eigenvalues of I − P_H are 1/((n+1)λ+1) ≤ 1/(λ+1), and both operators are 1 off it;
  - so a := uᵀ(I−P_H)u ≤ b := uᵀ(I−P_A)u, and [1+(n+1)a]/(1+b) ≤ [1+(n+1)b]/(1+b) ≤ n+1. ✓
  (In fact b ≤ ‖u‖² = n − 1, so the ratio is ≤ n. This is harmless.)
- **(iii) Fit factor.** [P1] `lem:spec`(d) (PROOF_v3.tex:96, 107). Alternatively, `lem:slab`'s variational form
  Q = min_ϑ{‖y − Xϑ‖² + ϑᵀ(G+I)ϑ/n}, with ϑ_j = 0 admissible, gives Q_S ≤ Q_{S₀}. Since Q ≥ 0 and b₀ > 0, the factor is
  ≥ 1. ✓
- **Summation.** The p − s₀ models S₀ ∪ {j} are distinct, so δ ≥ (p − s₀) r (1 − δ). ✓
- **Monotonicity.** d/dp[(p − s₀)/(2p − 1 − s₀)] has the sign of s₀ − 1 ≥ 0. The minimum, at p = s₀ + 1, is 1/(s₀+1).
  Hence (p − s₀) r ≥ (n+1)^{−1/2}, and δ(1 + (n+1)^{−1/2}) ≥ (n+1)^{−1/2} gives δ ≥ 1/(1 + √(n+1)). ✓
- **Hypotheses used.** Only the stated ones: 1 ≤ s₀ < p, s₀ + 1 ≤ K, the coded π, and s_y > 0 (§0). No noise law, design
  or signal condition is used.
- **Domain is necessary.** The domain restriction matters: at p = s₀ = 2, n = 20, orthogonal columns and θ = (2, 2),
  δ = 2.6·10⁻⁵ < 0.179 (`lb_outside_out.txt`). The statement, REPORT:18, 66-69, 127 and ASSUMPTION_MAP:124 now carry
  the domain.
- **Tightness.** With p = s₀ + 1, x_j orthogonal to X_{S₀} and to y, and y in span X_{S₀}, the ratio
  (1 − π(S₀))(1 + √(n+1)) is 1.128 (n = 6), 1.0005 (n = 1000) and **1.00005 (n = 10⁴)**. It is never below 1
  (`lb_adv_out.txt`). So the constant is essentially sharp for its own mechanism, and the falsification harness genuinely
  probes the bound.
- **Consequences.** "Sharp up to √log n" is correct as stated, on sequences with s₀ < p and s₀ + 1 ≤ K: the lower bound
  is ≍ n^{−1/2} and Theorem 1's upper bound is O_P(√(log n/n)). The growing-p √log n factor is labelled a conjecture
  everywhere (STATEMENT:97, LB Remark 3, ASSUMPTION_MAP:124-128, REPORT:129-130, 179). My heuristic agrees: e^{Z²/2} has
  infinite mean, and a sum of p copies is ≍ p√(log p), so the superset mass is ≍ n^{−1/2}√(log p). It is still only a
  heuristic, correctly not claimed.

### Lemma 1a′ and Lemma 1a: correct
- **Statement against [T03R].** I re-checked T02(i♯) ([T03R]:74-99) against STATEMENT:42-49: constants b±, κ, c_IG, C_Λ,
  c♯, the display, and the consequence (1+1/n)^{s₀/2}e^{−ω}Θ♯.
- **Hypotheses of the remark.** The remark ([T03R]:99) uses only ‖μ‖² ≤ nM, λ_min(R_{S₀}) ≥ φ₀² and s₀ ≤ K. ✓
- **L1a′ changed step.** Under G, y_c = Uᵀμ + ε_c and X_{c,T}θ = Uᵀμ, so ϑ = θ in `lem:slab`'s variational form gives
  Q^c_T ≤ σ*²E′ + (‖μ‖² + ‖θ‖²)/n deterministically. ✓
- **Assembly.** `thm:Ta` (PROOF_v3.tex:255-264): the last inequality needs only Z^c_{b+} ≥ ϖ(T)m^c_{b+}(T), i.e. T ∈ Ω.
  `lem:num` (l. 317-322) holds for any design with data-free b. ✓
- **Uniformity.** The display depends on X only through (M, M′). ✓
- **Growing t.** (1+1/n)^{t/2} ≤ e^{1/4} because t ≤ K ≤ n/2. ✓
- **Zero-extension (new in this round).** q_k := 0 outside 0 ≤ k ≤ K and R_m := Σ_{k=max(m+1,0)}^K (STATEMENT:35,
  L1a′:11). This is consistent with "for every integer m". For m < 0, π(|S| > m) = 1 and R_m = W_K/w(s₀), so Θ is
  deterministic and the bound is trivial. ✓
- **Headline.** ‖Xθ*‖² ≤ s₀²θ_hi²(n−1) and ‖θ*‖² ≤ s₀θ_hi² ≤ nθ_hi²/2. The caveat that (E) is a real condition for
  growing s₀ is present. ✓

### Theorem 1: hypotheses used = hypotheses stated
- **Items 1 and 5(b).** T03♯ ([T03R]:162-175): R1 + G + R + SE_λ(j₀) + SE_w(m♯_n; g₀) (+ BM for (i)-(iii)).
  - STATEMENT R1 + (E) + (F_λ) (J = ∅ gives R's floor) + (F_w) + (BM) is the same set.
  - p ≥ 2 is now explicit (STATEMENT:62, matching [T03R]:9).
  - c₀ = max{4C_*, 32[s₀(A+1)+2]} matches. Conclusion (iv) gives 5(b), including the PIP form. ✓
- **Item 5(a).** T02(ii♯) ([T03R]:147-149): "R1 under G, R and SE_w(m♯_n; g₀)". This matches the reduced list in
  STATEMENT:86-87. ✓
- **Items 2–4.** Re-derived:
  - HPM: on {δ < ½}, π(S₀) > ½ exceeds every other model, so any tie rule picks S₀. Markov then gives
    P(HPM ≠ S₀) ≤ 2Eδ_n, and Eδ_n → 0 by bounded convergence.
  - MPM: on {δ < ½}, PIP_j ≥ 1 − δ for j ∈ S₀ and PIP_j ≤ δ otherwise.
  - ξ_{q_n}: needs δ_n < min(q_n, 1 − q_n), which holds w.p. → 1 since r_n = o(min).
  - Items 3–4: π(|S| = s₀) ≥ 1 − δ, and sup_h |π(h) − h(S₀)| ≤ δ, with equality at h = 1{S ≠ S₀}. ✓
- **Item 6 (interface form).** The diagonal argument is valid. If for some ε and every C there are infinitely many n with
  a design in 𝒜_n where P(δ > C r_n) > ε, choose n_k ↑ with C = k. The resulting deterministic sequence violates the
  fixed-design O_P statement, a contradiction. The argument needs every sequence in 𝒜_n to satisfy R1 with common
  constants, which is what is assumed (see N2 for the s₀ point).
- **Item 7.** = Proposition LB, with its domain stated in the item. ✓
- **Corollary 1R.** No new mathematics. The structure was checked in C1 and is unchanged. The no-beta-min extension is
  valid: [POST] steps (2)–(4) use θ_hi only.

### Fidelity to the code (G6)
- `v3_score.h:14`: a₀ = b₀ = 0.01.
- `:40`: K = std::min(p, n/2) (integer division, i.e. ⌊n/2⌋).
- `:57`: ν = a₀ + n/2.
- `:65`: log w(k) = −log 2 − lchoose(2p−1, k).
- `:175, 189-193`: H = (n+1)G + I and A = G + I.
- `:222-223`: log m = logC_n − ½(ldH − ldA) − ν log(2b₀ + Q).
- `v3_preprocess.R:111-127`: constant columns are dropped before p is formed; y is standardised; `dup_components` is
  diagnostic only and does not change the target.
- STATEMENT §0 matches. LB uses exactly this π: the cap enters through s₀ + 1 ≤ K, and w through the prior ratio.
- `post_exact.py`'s `Post` implements the same score: logw, H, A, Q, ν, B0 and K = min(p, n//2) all agree.

### Numerical claims: every quote re-checked against the (reproduced) output
| Quote | Where | Output | ✓ |
|---|---|---|---|
| E0 median δ√n ≈ 2.1–2.6 | AM:125, REPORT:129, LB Rem. 2 | 0.2612·10 = 2.61, 0.1035·20 = 2.07, 0.0603·40 = 2.41, 0.0327·80 = 2.61 | ✓ |
| E1 c = 0.5, 1 fail, δ 0.93–0.99 | AM:20, REPORT:132 | 0.927–0.993 | ✓ |
| E1 c = 2: δ 0.66 → 0.13, δ/r_n 3.1–6.7 | same | 0.664 → 0.132; 3.09–6.74 | ✓ |
| E1 c = 4: δ/r_n 1.54 → 0.70; c = 8: 1.02 → 0.64 | same | 1.536 → 0.704; 1.020 → 0.638 | ✓ |
| E2 δ/r_n 0.94 → 0.67, HPM 100% | AM:19, REPORT:138 | 0.937 → 0.672; 1.00 | ✓ |
| E3 HPM ≥ 95%, δ/r_n 0.81–1.12 | AM:18 | 0.95–1.00; 0.806–1.116 | ✓ |
| E4 γ = .5: 1.08 → 0.64; γ = .8: δ .40 → .06, HPM wrong 10–20%; γ = 1: δ .37–.50, wrong 25–30% | AM:18, REPORT:141 | all match | ✓ |
| E5 c = 0.8: 0.26, 0.49, 0.82, 0.92, 0.988; c = 0.5: 0.10 → 0.57 | AM:22, REPORT:147 | 0.257, 0.488, 0.820, 0.916, 0.988; 0.104 → 0.574 | ✓ |
| L1a(b),(c) max sup_m Θ ≤ 1.1·10⁻³; L1a′(e) ≤ 1.5·10⁻⁵ (Remark 2: ≤ 2·10⁻⁵) | AM:16-17, L1a′ Rem. 2 | 1.040e-3; 1.419e-5 | ✓ |
| LB min ratio 1.013 over 34 920 cases | STATEMENT:96-97, REPORT, AM:124 | 1.012988, 34920 (re-run identical) | ✓ |
| E5 population λ_min ≈ 0.106 | AM:22 | 1 − 2a with a = √0.2: 0.1056 | ✓ |

**E5 leading-order sketch (labelled "unchecked"; I checked it independently).** Units of log n, c = 0.8, a² = 0.2.
- {5}: 1.6c − ½ = 0.78.
- {i}: c/2 − ½ = −0.1.
- S₀: 2c − 2 = −0.4.
- {5, i}: uᵀΓ⁻¹u = (1 + 8a²)/(1 − a²) = 3.25, so 1.625c − 1 = 0.30.
- {5, i, j}: (2 + 4a²/(2a² + 0.2))·c/2 − 1.5 = −0.17.
- {i, j}: −0.2.
- Sets with added independent nulls are lower still.

So the margin of {5} is ≥ 0.48. The sketch is correct as written; keeping its "unchecked" label is the lead's call (N5).

### Literature: checked against the PDFs, nothing invented
- **NH14 (arXiv pp. 5–6, 10–13).**
  - Conditions 4.1–4.5 are quoted as printed, including the new parameters "ν < δ, κ < (K − 1)δ/2".
  - m_n(ν) = p_n ∧ n/((2+ν) log p_n) and λ^n_m(ν) is the infimum of the minimum *nonzero* eigenvalue (p. 6). ✓
  - Condition 4.4: residual signal > 5σ²|t|(1+δ) log(√n ∨ p_n). ✓
  - Theorem 4.1 is for known σ² (p. 12). Theorem 4.2 needs a dimension restriction; it is correctly flagged "not re-read".
- **YWJ16 (arXiv pp. 6–9).** Prior (5a–d) with the cap I[|γ| ≤ s₀] ✓; regime p ≥ n ✓; RE(s)/SI(s) ✓;
  g ≍ p^{2α} and κ + α ≥ C₁(L + L̃) + 2 ✓; D(s*) "s₀ := p" ✓; Theorem 1 gives π_n(γ*|Y) ≥ 1 − c₁p⁻¹ w.p.
  ≥ 1 − c₂p^{−c₃} ✓. The "per-variable penalty (κ + α) log p ≥ 2 log p" reading is correct: prior p^{−κ} times g-prior
  Occam factor (1+g)^{−1/2} ≈ p^{−α}.
- **Song–Liang.**
  - Theorem 1: |x_i| ≤ 1 (p. 952) ✓.
  - Theorem 2: Condition 1, (9)–(14), strict sparsity (4), r_n ≻ 1 (p. 953) ✓.
  - Condition 3 sufficient condition for mean-0 bounded predictors (p. 955) ✓.

### C1 findings: each genuinely fixed?
| C1 finding | Fixed? | Evidence |
|---|---|---|
| A-F1 rate/YWJ overclaim | **yes** | YWJ rewritten correctly. Growing-p optimality is labelled a conjecture. LB is proved (above). |
| A-F2 NH14 | **yes** | Matches the PDF (above). |
| A-F3 Song–Liang qualifications | **yes**, one residue (N3) | AM:38-66. AM:15 still says the bounded-SNR setting "is the setting of Song–Liang Condition 2 too". |
| A-F4 REPORT drops conditions | **yes** | REPORT:33-45. |
| A-F5 numerical labels / scale | **yes** | post_exact.py `run()` standardises X before forming μ = Xθ*. Quotes are medians and match. |
| A-F6 p ≤ 10 | **yes** | P_DEF = 10. The output header says p=10. No "p = 12" remains except the historical LOG entry. |
| A-F7 design family in Thm 1 | **yes** | Item 6 is the interface form; Corollary 1R is separate. |
| A-F8 boundary terms | **yes** | AM:20: margin η, n^{a+½−c/2+o_P(1)}, "deletion obstructions". Sign convention re-derived. |
| A-F9 citecheck coverage | **yes** | The docstring now says "SELECTED checks". |
| B-F1 stale numbers | **yes** | Table above. |
| B-F2 heuristic as fact | **yes** | AM:20, 104-106; REPORT:131. |
| B-F3 p ≥ 2 | **yes** | STATEMENT:43, 62; REPORT:37, 46. |
| B-F4 counterexample label | **yes** | Labelled everywhere. The E5 sketch has been added and is correct. |
| B-N1…N7 | **yes** | N2: REPORT:33 has Σ_{k=m+1}^{K}. N4: check record in L1a′:3-5. N5: STATEMENT:116-117. N6: AM:42 attributes r_n ≻ 1 to Theorem 2 (correct, p. 953). N7: done. |

---

## 2. Gates

| Gate | Verdict | Reasons |
|---|---|---|
| G1 correctness of every step | **PASS** | LB is correct line by line and essentially tight; numerically it reaches 1.00005, never below 1. L1a′, Lemma 1a and items 1–6 follow from the cited steps. The zero-extension and the domain qualifiers are consistent. No claim labelled heuristic, conjecture or sketch is used as proved. |
| G2 hypotheses used = stated | **PASS** | Theorem 1's set equals T03♯'s, including p ≥ 2. 5(a)'s list equals T02(ii♯)'s. LB uses only 1 ≤ s₀ < p, s₀ + 1 ≤ K and the coded π, and it states exactly these. L1a′ uses only G, the representation, T ∈ Ω and (M, M′). |
| G3 no hidden assumptions | **PASS** (N2) | ε ⫫ (X, θ*), retained p, s_y > 0, n ≥ 3, positivity of floors and coefficient bounds, and the raw/standardised conventions are all explicit. Item 6 relies on R1's "s₀ fixed" for the random support size (N2); this is stated globally, but it is worth one clause. |
| G4 cited lemmas have adequate status | **PASS** (N6) | Statuses are verbatim (`04_theory.tex:771`; L1_POST:3). LB and L1a′ are honestly "PROVED (by this seat, unchecked)". LB's cross-family line check is this council round, which should be recorded in its file (N6). Nothing is upgraded. |
| G5 constants/rates tracked | **PASS** | The LB constant is explicit and sharp to O(n^{−1/2}) relative error. C′_Λ, c♯, the 𝓑_n bound, the R_m cutoff and c₀ are explicit. The rate gap (√log n) is identified and labelled a conjecture. |
| G6 fidelity to the method as coded | **PASS** | §0 and LB match `v3_score.h`/`v3_preprocess.R` exactly. The numerics enumerate the coded score, and the outputs reproduce byte for byte. |

**Score: 8.8 / 10** (uncapped). Pass condition for this seat: ≥ 8.0 and all gates PASS — **met**.

I found no false step. Every C1 finding is genuinely fixed. The new Proposition LB is correct, uses exactly its stated
hypotheses, and is sharp in its constant. All numbers and literature claims check against their sources. Points are
lost for:
- one provenance misstatement in REPORT (F1);
- small loose ends: item ordering, an AM residue of C1A-F3, a broken table row, an uncited minimax remark, evidence cited
  from a reviewer scratch folder, and LB's missing check record.

---

## 3. Findings (0 FATAL / 0 MAJOR / 1 MINOR / 7 NIT)

**F1 — MINOR — REPORT.md:11-12 (provenance misstated).** The text says "Two fresh **cross-family** reviewers re-checked
it adversarially: R01 (gpt-6-astra high) and R02 (Claude Opus 5.5 high)". The lead is Claude Opus 5.5 (STATEMENT:1,
REPORT:3), so R02 is a **same-family** reviewer. Wave 1 PROTOCOL makes cross-family review the requirement for
lemma-by-lemma checks, so the word matters for the anti-hallucination record. (L1a′'s own check record is correct: it
has R01 as the cross-family check.)
**Fix:** "Two fresh reviewers re-checked it adversarially: R01 (gpt-6-astra high, cross-family) and R02 (Claude Opus 5.5
high, same family)".

**N1 — NIT — STATEMENT.md:94-103 (item order).** Item 7 is printed before item 6.
**Fix:** move item 7 after item 6, or renumber.

**N2 — NIT — STATEMENT.md:98-103 (item 6, random θ*).** With θ* random, S₀ = supp θ* is random. The diagonal transfer
needs every deterministic sequence in 𝒜_n to satisfy R1 with the *same* s₀, because j₀, m♯_n, c₀ and n₀ depend on s₀.
R1's "s₀ fixed" covers this only implicitly.
**Fix:** add "with |supp θ*| = s₀ (the R1 value) on 𝒜_n" (S₀ itself may vary).

**N3 — NIT — ASSUMPTION_MAP.md:15 (residue of C1A-F3).** POST-E's evidence cell says "Bounded signal-to-noise is the
setting of Song–Liang Condition 2 (second moments, M) too". AM:52-53 correctly says Condition 2 is a predictor-moment
condition and only *analogous* to POST-E under bounded coefficients.
**Fix:** "Song–Liang Condition 2 (a predictor second-moment condition) is only analogous (AM:52-53)."

**N4 — NIT — ASSUMPTION_MAP.md:21-22 (formatting).** The POST-BM′ table row is split by a hard line break inside the cell
("… in this fixed-p experiment — the⏎coefficients below …"). Markdown ends the row there, so the rest renders as a
stray paragraph.
**Fix:** join the two lines.

**N5 — NIT — ASSUMPTION_MAP.md:21-22 (status of the E5 sketch).** The sketch is labelled "unchecked". I re-derived every
listed coefficient independently, and also the ones not listed:
- {5,i} = 0.30 exactly, from uᵀΓ⁻¹u = (1+8a²)/(1−a²) = 3.25;
- {5,i,j} = −0.17;
- {i,j} = −0.2.
So the margin ≥ 0.48 log n is right.
**Fix (optional):** record "leading coefficients re-derived by C2 seat B". Keep the status word, since the O_P(√log n)
control of the remainder is still a sketch.

**N6 — NIT — lemmas/LB_rate_lower_bound.md:3 (check record).** The status line has no check record. Wave1 PROTOCOL
lemma step (b) requires a cross-family line-by-line check; here the council supplies it, because LB entered at C1 → C2.
**Fix:** after C2, add "Check record: C2 seat A (gpt-6-astra) and seat B (Opus 5.5) line by line; falsification
`numerics/lb_check_out.txt`". Keep "PROVED (by this seat, unchecked)", as was done for L1a′.

**N7 — NIT — REPORT.md:68-69 and ASSUMPTION_MAP.md:124 (evidence location).**
- REPORT.md:68-69 cites a numeric ("δ ≈ 6.5·10⁻¹⁰ at n = 20") whose only evidence is another reviewer's scratch folder,
  `reviews/C2_scratch_astra/`. The scratch folder is not package numerics.
- ASSUMPTION_MAP.md:105 also has an uncited claim: "at p = n^A it coincides with the minimax √(log p/n) scale".

**Fix:**
- Either move a 10-line script into `numerics/` (e.g. p = s₀ = 2, orthogonal columns; my `lb_outside.py` gives
  δ = 2.6·10⁻⁵ at θ = (2,2), n = 20), or drop the number. The failure at p = s₀ is evident: no superset is available.
- Cite a source for the minimax scale (e.g. Wainwright 2009, information-theoretic limits of support recovery), or
  mark it "standard; not re-read".

---

## 4. Bottom line
- No FATAL or MAJOR defect, and every C1 finding is genuinely fixed.
- Proposition LB is correct as stated: deterministic, only its stated hypotheses, constant essentially attained.
- Theorem 1 items 1–7, Corollary 1R and Lemmas 1a/1a′ follow from the cited, adequately-statused steps under exactly the
  stated hypotheses.
- Code fidelity is exact. Numerics and citecheck reproduce identically. Literature claims match the sources.
- Before the final REPORT: fix the provenance wording (F1) and tidy N1–N7.

**Gates: G1–G6 all PASS. Score 8.8.**
