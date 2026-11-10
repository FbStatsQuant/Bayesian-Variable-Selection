# W3-POST — Council C1, seat B (Claude Opus 5.5, high, claudeAgent)

Date 2026-11-09. Briefed to break the package. Earlier verdicts (R01, R02, R03, CITECHECK) and status lines were **not**
used as evidence; every item below was re-derived from the sources. I did **not** read `C1_council_astra.md` or
`C1_scratch_astra/`. No file outside `reviews/C1_council_opus.md` and `reviews/C1_scratch_opus/` was written; no git
state changed.

**Read in full:** STATEMENT.md (v1.2), lemmas/L1a_size_tail.md, ASSUMPTION_MAP.md, REPORT.md, numerics/post_exact.py
and post_exact_out.txt (**both versions**, see F1), R01/R02 dispositions, R03 in full, R01/R02 verdict sections,
CITECHECK.txt; [T03R] PROOF.md (all 215 lines); [P1] PROOF_v3.tex §§1–5 (lines 40–384: `lem:slab`, `lem:spec`,
`lem:prior`, `lem:chi`, `thm:T01i`, `thm:T01iii`, `thm:Ta`, `lem:num`, `lem:den`, `thm:T02i`); [P3] proof paragraphs
(i)–(v) (lines 334–385); [POST] L1_POST.md (all); [SL] §§0–2; [UNI] lines 80–95; 00_COMMON §§1, 3;
`04_theory.tex:771, 780-788`; `v3_score.h:14, 36-75, 190-230`; `v3_preprocess.R:37-62, 100-135`; Song–Liang (2015) PDF
pp. 947–956 (text extracted with pdftotext into my session scratchpad). W2-APP REPORT RESULT line.

**My own numerics:** `reviews/C1_scratch_opus/p3_counterexample.py` → `p3_counterexample_out.txt` (b² = 0.75) and
`p3_counterexample_b095_out.txt` (b² = 0.95): exact coded posterior for R03 §5A's p = 3 construction, n ≤ 10⁶, 20 seeds.

---

## 1. Verification record (what I re-derived)

### Lemma 1a′ (new; `lemmas/L1a_size_tail.md`), line by line — **correct**
- **Changed step (l. 25-30).** [P1] `lem:slab` gives Q^c_T = min_ϑ{‖y_c − X_{c,T}ϑ‖² + ϑᵀ(G_T+I)ϑ/n} with
  G_T = X_{c,T}ᵀX_{c,T} = X_TᵀX_T (eq. UX). Under G, y_c = Uᵀμ + ε_c ([P1] `thm:T01iii`) and X_{c,T}θ = UᵀX_Tθ = Uᵀμ, so
  ϑ = θ gives Q^c_T ≤ ‖ε_c‖² + (‖X_Tθ‖² + ‖θ‖²)/n = σ*²E′ + ρ with ρ = (‖μ‖² + ‖θ‖²)/n ≤ M + M′, **deterministically**.
  t = 0 case correct.
- **den′ with R_n → ρ (l. 32-35).** I re-checked [P1] `lem:den` (PROOF_v3.tex:339-353): the exponent bound uses only
  Q^c ≤ σ*²E′ + R with R ≥ 0 (the step −R/(2σ*²u) ≥ −R/(2σ*²) needs u ≥ 1 and R ≥ 0); f₀(y_c) = (2πσ*²)^{−(n−1)/2}e^{−E′/2}
  holds for any design; D_T ≤ (n+1)^t is `lem:spec`(e) with no condition. E Λ′ ≤ √(2(n−1))/(2√n) + (n−1)/(2n) + ρ/(2σ*²)
  ≤ C′_Λ. ✓ (ρ deterministic, so this is cleaner than [P1]'s E R_n bound.)
- **Assembly (l. 37-40).** `thm:Ta`'s last inequality needs only T ∈ Ω (Z^c_{b+} ≥ ϖ(T)m^c_{b+}(T)); v_m = ϖ(E_m) =
  R^T_m ϖ(T) (W_K cancels); `lem:num` with data-free b₋ gives E Θ^{(1)} = 1 for any design; hence on 𝓑_n,
  Θ^T ≤ c♯e^{Λ′}Θ^{(1)} with c♯ = κ²/(c_IG σ*²) depending on (σ*², M) only; the three-way split needs L > c♯²;
  P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n−1) uses only ‖μ‖² ≤ nM. Uniformity over (X, T) with fixed (M, M′) is correct.
- **Remarks.** R1: ‖μ‖² = θ*ᵀG_{S₀}θ* ≥ (n−1)φ₀²‖θ*‖² ⇒ ‖θ*‖² ≤ 1.5M/φ₀² ✓. R2: x₁ − x₂ is the G-eigenvector with
  eigenvalue g, 1 − h(g) = (g+1)/((n+1)g+1), so the signal part is 2L²g(g+1)/((n+1)g+1) ✓. R4: E2(ii) with
  log C(p,t) ≤ t log p ✓. R5: A t log n + ((t+2)/2) log n = [(A+½)t + 1] log n ✓; Prop D's consequence ✓.
- **Headline (STATEMENT:55-57).** ‖Xθ*‖ ≤ Σ|θ_j|‖x_j‖ ≤ s₀θ_hi√(n−1) ✓. Observation (not a defect): with |θ*_j| ≤ θ_hi,
  ‖θ*‖² ≤ s₀θ_hi² ≤ nθ_hi²/2 because s₀ ≤ K ≤ n/2, so the coefficient bound holds with M′ = θ_hi²/2 **even for growing s₀**;
  only (E) is a real condition then — the statement says exactly this.

### Lemma 1a (= T02(i♯)) — **correct, faithfully quoted**
STATEMENT:42-49 matches [T03R]:76-85 (C_Λ, c♯, display, consequence) and its proof [T03R]:89-97; remark [T03R]:99
(uses only ‖μ‖² ≤ nM, λ_min(R_{S₀}) ≥ φ₀², s₀ ≤ K). Status string verbatim at `04_theory.tex:771`.

### Theorem 1 — hypotheses used vs stated
- R in 00_COMMON:36 = {s₀ fixed, p ≤ n^A (A ≥ 1), ‖μ‖²/n ≤ M, λ_min(R_{S₀}) ≥ φ₀², s₀ ≤ K eventually}; T03♯ ([T03R]:162-168)
  = R1 + G + R + SE_λ(j₀) + SE_w(m♯_n; g₀) (+ BM for (i)-(iii)). STATEMENT R1 + (E) + (F_λ) (J = ∅ gives R's floor) + (F_w)
  + (BM) is the same set — **except p ≥ 2** (F3). BM(c), c₀ = max{4C_*, 32[s₀(A+1)+2]} match `04_theory.tex:780-788`.
- Interlacing consequences (STATEMENT:68-72): for S with |S| ≤ j₀, J := S∖S₀ has |J| ≤ j₀ and S ⊆ S₀∪J ✓.
- Items 1 = T03♯(i); 2–4 = SL0(i)–(v)/SL1(a)–(e) (re-derived: Markov for P(HPM ≠ S₀) ≤ 2Eδ_n; bounded convergence for
  Eδ_n → 0; ξ_{q_n} needs δ_n < min(q_n, 1 − q_n)); 5(a) = T02(ii♯) with exactly the listed hypotheses ([T03R]:149);
  5(b) = T03♯(iv) + SL1′ — I checked [P3] (iv) (PROOF_v2.tex:366-378): no BM, U_j uses θ*_j only, union over |J_n| ≤ s₀.
- Item 6 vs [POST]: LSF (i)/(ii), m̄_n, k̄_n, φ₀² = φ²/2, g₀ = 1, M = s₀²θ_hi² + 1 verbatim from [POST]:20-30. I re-checked
  m̄_n ≥ m♯_n two ways ([POST] step (1)'s (2/3)^k bound, and independently from E2(ii): (X + (s₀+1)log 2)/log 1.5 ≥
  X/log 2 + s₀ + 1 with X = s₀A log n + ((s₀+2)/2) log n).
- **Item 6 without beta-min (lead's extension) — valid.** [POST] step (3) (floors on 𝒢_n) and step (4) (energy:
  ‖μ‖² ≤ (n−1)s₀‖θ*‖² ≤ s₀²θ_hi²n) use θ_hi only; θ_lo enters only in the BM-∞ envelope. On 𝒜_n every deterministic
  design sequence satisfies T02(ii♯)'s and T03♯(iv)'s hypotheses with common constants, and step (5)'s contradiction
  argument transfers O_P(r_n) to the joint law verbatim; [POST]:33 already asserts the J_n(c) clause "without beta-min".
  Only wording gap: J_n(c) is design-measurable (random) under the raw-scale convention (N5).
- Statuses (G4): "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" and "T02(i♯), T02(ii♯): PROVED; SF/XF
  VERIFIED" verbatim at `04_theory.tex:771`; [POST] "PROVED (by this seat, unchecked)" + R02 VERIFIED-WITH-AMENDMENTS
  verbatim at L1_POST.md:3-4, inside W2-APP whose REPORT:3 is "PROVED-CHECKED" (council r3 passed). Adequate. Nothing upgraded.

### Fidelity to the code (G6)
`v3_score.h`: a₀ = b₀ = 0.01 (l. 14); K = std::min(p, n/2) (integer); ν = a₀ + n/2; log w(k) = −log 2 − lchoose(2p−1, k);
H rows √(n+1)x plus I, A rows x plus I (QR form of H = (n+1)G + I, A = G + I); Q = yᵀy − n zᵀH⁻¹z; log m = logC_n −
½(log det H − log det A) − ν log(2b₀ + Q). `v3_preprocess.R:111-115`: constant columns dropped before p (and hence K, w)
are formed. STATEMENT §0 matches; the "real-arithmetic target" caveat is stated. ✓

### Literature (Song–Liang PDF) — no invented citation found
JRSSB 77 Part 5, pp. 947–972 (p. 947 header) ✓; P_n ≻ n^θ and strict sparsity (4) p. 950 ✓; prior (6) λ_n = r_n/P_n with
cap r̄_n, IG(a₀, b₀), N(0, σ²V_ξ) p. 951 ✓; Theorem 1 Hellinger, (8)–(14), (10) r̄_n ln P_n ≺ nε_n² p. 952 ✓; ridge prior
c_n ∝ 1/n and Condition 1 + Gaussian remark p. 953 ✓; Corollary 1 (P_n < exp(Cn^α), ε_n = O(n^{−(1−α)/2} log^{k/2} n) for
r̄_n ≺ log^k n) and Condition 2 + (16) p. 954 ✓; Condition 3 and the λ_min ≻ r̄_nε_n² sufficient condition p. 955 ✓;
Theorem 3 sure screening and "the specificity is not controlled", Theorem S in the supplement, p. 956 ✓. One loose item (N6).
NH14 (AoS 42(2) 789–817) and YWJ16 (AoS 44(6) 2497–2532) bibliographic data are correct to my knowledge and are
labelled "recalled, not re-read" — acceptable.

### Numerical claims — verified against the p = 12 output, now superseded (F1)
I first read `post_exact_out.txt` in its p = 12 form (header "p=12"). Against it every quoted number in ASSUMPTION_MAP and
REPORT matched, except two over-tight quotes (N1). During this review both `numerics/post_exact.py` (now `P_DEF = 10  #
Wave1 PROTOCOL compute rule: exact enumeration p <= 10 (C1-A F6)`) and `post_exact_out.txt` were rewritten
(mtimes 16:49 / 16:50; ASSUMPTION_MAP/REPORT/STATEMENT are from 16:35–16:37). Against the **current** p = 10 output all
qualitative conclusions survive, but many quoted numbers are no longer in any file (F1).

### R03 §5A p = 3 counterexample — independent check (F4)
Leading-order arithmetic re-derived: scores (units log n) {1}: b²/2 − L, {1,2}: b² − 2L, {3}: r²b² − L, {1,3}:
b²/(2 − r²) − 2L (I re-derived the fraction 1/(2 − r²)), triple b² − 3L; normalised λ_min = 1 − r = 0.051. Asymptotically
{3} wins by 0.175 log n (b² = 0.75), against O(√log n) fluctuations. **But the exact coded posterior shows no visible
convergence up to n = 10⁶**: median PIP₃ = 0.17, 0.17, 0.27, 0.10, 0.50 and P(HPM = {3}) = 0.30–0.50 at n = 10²…10⁶
(`p3_counterexample_out.txt`); with b² = 0.95, median PIP₃ 0.27 → 0.78 at 10⁶ (`p3_counterexample_b095_out.txt`). The
mechanism is real but its margin is too small to observe; E5 is the convincing evidence. By my own leading-order
computation, E5's design (s₀ = 4, c = 0.8, a² = 0.2) gives {5} a score of 0.78 log n over ∅ and a margin ≥ 0.48 log n over
every competitor (S₀: −0.4; {i}: −0.1; {5, i}: 0.3; any set of ≥ 3 variables ≤ 0.1), which matches PIP₅ → 0.99.

---

## 2. Gates

| Gate | Verdict | Reasons |
|---|---|---|
| G1 correctness of every step | **PASS** | L1a′ proof correct line by line; Lemma 1a, items 1–6 follow from the cited steps; the item-6 no-beta-min extension is valid. The sharpness sentences in F2 are evidence-labelling problems in the sharpness record, not proof steps. |
| G2 hypotheses used = stated | **PASS** (with F3) | Theorem 1's hypothesis set = T03♯'s; 5(a)'s reduced list = T02(ii♯)'s; L1a′ uses only G, ‖μ‖² ≤ nM, the representation, T ∈ Ω. Only gap: p ≥ 2, assumed by [T03R]:9 and not stated in R1 (F3). The theorem is still true at p = 1, so this is a citation gap, not a false statement. |
| G3 no hidden assumptions | **PASS** (with F3, N5) | Positivity of φ₀, g₀, φ, θ_lo; retained p; s_y > 0; ε ⫫ X; and the raw/standardised conventions are all explicit. |
| G4 cited lemmas have adequate status | **PASS** | Statuses verbatim; [T03R] items carry SF/XF VERIFIED; [POST] sits inside the PROVED-CHECKED W2-APP package. L1a′ is honestly "PROVED (by this seat, unchecked)" plus R01/R02 (the lemma file's own status line is stale, N4). |
| G5 constants/rates tracked | **PASS** | C_Λ, C′_Λ, c♯, c_IG, b±, κ, the 𝓑_n bound and the cutoffs are explicit and depend only on the stated quantities; c₀ is given by formula; O_P constants are inherited with the stated dependence ([T03R]:170). |
| G6 fidelity to the method as coded | **PASS** | §0 matches `v3_score.h`/`v3_preprocess.R` exactly (cap, ν, H/A, w(k), retained columns); the numerics enumerate the coded score. |

**Score: 8.4 / 10** (uncapped). Pass condition for this seat: ≥ 8.0 and all gates PASS — **met**. Mathematically the
package is in good shape: I found no false step in the chain or in the new lemma. Points are lost for: (i) stale numerical
quotes after the mid-council numerics rerun (F1), which must be re-synced before the report is final; (ii)
heuristic sharpness claims stated as facts (F2); (iii) the p ≥ 2 gap (F3); (iv) a counterexample with no status label
whose cited analytic support is numerically invisible (F4).

---

## 3. Findings (0 FATAL / 0 MAJOR / 4 MINOR / 7 NIT)

**F1 — MINOR — ASSUMPTION_MAP.md:5-6, 15-19, 74; REPORT.md:64, 76-90 (numerical quotes vs `numerics/post_exact_out.txt`).**
The docs say "p = 12" and quote p = 12 numbers. The script and output on disk are now p = 10 (rewritten 16:49–16:50, after
the docs). Examples now in no file: E0 "δ√n ≈ 2.3–2.9" (current 2.6, 2.1, 2.4, 2.6); E1 c = 2 "δ 0.86 → 0.43" (current
0.66 → 0.13); E1 c = 4 "δ/r_n 1.35 → 0.78" (current 1.54 → 0.70); E2 "δ/r_n 0.87 → 0.64, HPM 90–100%" (current 0.94 → 0.67,
100%); E4 γ = 0.5 "0.93 → 0.62" (current 1.08 → 0.64), γ = 1 "δ ≈ 0.35–0.57" (current 0.37–0.50); E5 c = 0.8 "0.14, 0.42,
0.94, 0.79, 0.99" (current 0.26, 0.49, 0.82, 0.92, 0.99), c = 0.5 "0.05 → 0.64" (current 0.10 → 0.57). Every conclusion
(fail/borderline/consistent, the E5 counterexample, the L1a′ falsification) survives. **Fix:** re-sync every quote and
"p = 12" to the p = 10 output (or keep the p = 12 run as a separate dated file, if the compute rule allows it); add a LOG
entry for the rerun; re-run citecheck.

**F2 — MINOR — REPORT.md:79, 90-92; ASSUMPTION_MAP.md:18 (verdict column), 78-79, 97-99 (heuristic sharpness stated as fact).**
"No uniform o(√(log n/n)) beta-min is possible for this prior", "Order √(log n/n) is necessary" and "Not improvable for
the coded prior (prior-limited)" rest on fixed-p numerics (p ≤ 12, n ≤ 6400) and on R03 §1A's leading-order expansion
(an unproved sketch by a reviewer). The ≍ n^{−1/2} superset mass at p = n^A is labelled heuristic only in the
ASSUMPTION_MAP. **Fix:** label each "numerical + heuristic (R03 §1A), not proved". Optionally prove the fixed-p lower bound
δ_n ≥ c n^{−1/2} w.p. bounded below. It is short: one superset S₀ ∪ {j} has π(S₀∪{j})/π(S₀) ≳ n^{−1/2} on a
constant-probability event.

**F3 — MINOR — STATEMENT.md:62-63 (R1), also 40-49 (Lemma 1a) and REPORT.md:29 (p ≥ 2 not stated).**
[T03R]:9 assumes p ≥ 2 ("for p = 1 every statement below is trivial or void"), and E1(b)'s ρ₀ bound divides by 2p − 2.
For p = 1 and s₀ = 1, item 1 is not trivial: it is the one-variable deletion odds. It is true under BM, but no cited
proof covers it. L1a′ states "any p ≥ 2" (L1a_size_tail.md:8); Theorem 1 does not. ([POST]:10 also excludes p = 1.)
**Fix:** add "p ≥ 2" to R1 (and to Lemma 1a for uniformity), or add the one-line p = 1 argument.

**F4 — MINOR — STATEMENT.md:89-91; REPORT.md:37-38, 86-88; ASSUMPTION_MAP.md:19 ("False in general" without a status; weak analytic support).**
The counterexample has no status label and no proof file. Its analytic support, R03 §5A with b² = 0.75, is
asymptotically right, but the exact coded posterior does not show it up to n = 10⁶ (§1 above: median PIP₃ ≤ 0.50,
non-monotone). Calling it "the analytic p = 3 version" of E5 overstates what it shows at finite n. **Fix:** label it
"COUNTEREXAMPLE (numerical, E5; leading-order analytic sketch, unchecked)". Better, write the leading-order computation
for **E5's own design** as a short lemma: {5} beats ∅ by 0.78 log n and every competitor by ≥ 0.48 log n, so fluctuations
are visibly dominated. Cite R03 §5A only as a mechanism with slow convergence.

**N1 — NIT — ASSUMPTION_MAP.md:15, 16.** Two quotes were over-tight even against the p = 12 output. "sup_m Θ ≤ 10⁻³"
in L1a′(b): the max is 1.043·10⁻³ (p = 12) and 1.040·10⁻³ (p = 10). "HPM wrong in 25–50%" at γ = 1: it is 15–50% at p = 12
(25–30% at p = 10). **Fix:** "≲ 10⁻³" and the correct range.

**N2 — NIT — REPORT.md:24.** The cutoff is written Σ_{k>m} without the cap; it must be Σ_{k=m+1}^{K} (STATEMENT:35).
Without K the sum, and hence m♯_n, changes. **Fix:** add the upper limit K.

**N3 — NIT — REPORT.md:26-27, 33.** "Automatic for fixed s₀" drops "|θ*_j| ≤ θ_hi". "s₀ may grow" drops STATEMENT:57's
caveat that (E) is then a real condition. Item 2's summary omits the condition on q_n (deterministic, with
r_n = o(min(q_n, 1 − q_n))). **Fix:** restore these three qualifiers.

**N4 — NIT — lemmas/L1a_size_tail.md:3.** The status line still says "pending the checks listed in ../LOG.md". **Fix:**
add a check record as [POST]:3-5 does: R01 (Astra) VERIFIED-WITH-AMENDMENTS (applied), R02 (Opus) VERIFIED; the status
word stays "PROVED (by this seat, unchecked)".

**N5 — NIT — STATEMENT.md:101-105 (item 6 without beta-min).** Under the raw-scale convention, θ* = D_xβ* is
design-measurable, so J_n(c) is a random set. **Fix:** say "J_n(c) is design-measurable; the diagonal transfer of
[POST] step (5) applies along every deterministic sequence in 𝒜_n" (I checked that it does).

**N6 — NIT — ASSUMPTION_MAP.md:39.** "and r_n ≻ 1" is not among Song–Liang (8)–(14) as printed (p. 952: (12) is
1 ≤ r_n ≤ r̄_n < P_n, (13) is r_n ≺ P_n; the theorem's premise is nε_n² ≻ 1). r_n growing is used only to make (8)
redundant under (4) (p. 953, "for large n, r_n > |ξ_t|"). **Fix:** cite (12)–(13), or drop "r_n ≻ 1".

**N7 — NIT — STATEMENT.md:92-99 (Wave-3 protocol rule 4).** Item 6 names a design law (iid Gaussian rows) inside
Theorem 1. The interface paragraph (l. 111-113) already treats [POST] as the bridge LSF ⇒ AF. **Fix:** state item 6 as a
separate "Corollary 1 (Gaussian-row bridge)" consuming AF. ASSUMPTION_MAP:18's "~30–60×" should also say which benchmark
it uses (128 vs 2a + 2 ∈ [2, 4] for the rate gives 32–64×).

---

## 4. Bottom line
No FATAL or MAJOR defect. The new Lemma 1a′ is correct and its uniformity claim is right. Theorem 1 items 1–6, including
the no-beta-min extension of item 6, follow from the cited, adequately-statused steps under exactly the stated
hypotheses, plus the unstated p ≥ 2. The code fidelity is exact. Before the final REPORT: re-sync the numerical quotes to
the p = 10 rerun (F1), label the heuristic sharpness claims (F2) and the counterexample (F4), and add p ≥ 2 (F3).
**Gates: G1–G6 all PASS. Score 8.4.**
