# W3-PSHARP — council round R2, seat `opus` (Claude Opus 5.5, effort high, blind first read)

Content reviewed: everything listed in `reviews/MANIFEST_R2.txt`. I recomputed every SHA-256 in the manifest (ticket
files and the 8 external inputs): all 29 match. I read only the files the brief allows (none of `reviews/` other than
my brief, `MANIFEST_R2.txt` and `INPUTS.txt`; not `LOG.md` or `CHECKPOINT_*.md`). So the review-trail rows of REPORT §2
(L01, K01, KSA, KBC verdicts) were **not** verified by me. Scratch code: `reviews/R2_scratch_opus/`
(`chk_SB.py`, `chk_W.py`, `chk_C.py`).

## Summary

I re-derived every proof step of `S_one_step.md`, `A_log_factor.md`, `B_sparsity.md` and `C_counterexample.md`
and found no error: no FATAL, no MAJOR, no MINOR finding on the mathematics. Every constant of Claim C holds for all
n ≥ 200: I checked the elementary inequalities analytically and the cutoff and determinant bounds numerically on a dense
grid up to n = 10⁹. The statements match the proofs item by item. The numerics compute what they say: the target is the
coded one, the reductions are exact in law, and every number quoted in the STATEMENT, lemma remarks and REPORT
matches the `*_out.txt` files. The findings are five NITs about wording in the REPORT and ASSUMPTION_MAP and one
NIT about the domain of a STATEMENT item.

## Gate verdicts

### G1 correctness — PASS
**Lemma V.** The quadratic G + (G + I)/n = H/n, minimiser nH⁻¹z, value yᵀy − n zᵀH⁻¹z; the s_y-rescaling is correct.

**Lemma S.** (1) H_{S⁺} has corner (n+1)(n−1) + 1 = n² and (G_{S⁺}+I) has corner n. Both Schur complements are
positive, and the D-ratio identity follows. In the eigenvalue computation the numerator is
(n+1)²(λ+1) − n((n+1)λ + 1) = (n+1)λ + n² + n + 1 > 0, so the ratio is ≤ n, with equality iff g = 0. (2) The
block-inverse step gives v₂ − hᵀH⁻¹v₁ = x_jᵀρ̃_S and Schur complement s; with s ≤ n² this gives the stated lower bound.
(3) The prior ratio is C(2p−1, s₀)/C(2p−1, s₀+1) = (s₀+1)/(2p−1−s₀); 0 ≤ γ < 1 because b₀ > 0; and −log(1−γ) ≥ γ.
(4) The models are distinct and the other terms are nonnegative.

**Lemma W.** The Chebyshev constant (1+η′)√π/(2ϵ′²(1−η)²√log N) is correct.
- (i) The truncated mean √(2τ/π) is exact, and E W² ≤ √(2τ/π)N.
- (ii) The density c_d(1 − t²/d)^{(d−3)/2} is correct. From log-convexity of Γ, (d−1)/d ≤ c_d√(2π) ≤ √((d−1)/d).
  The two-sided bound on t²/2 + ((d−3)/2)log(1 − t²/d) is valid on t² ≤ d/2, using log(1−x) ≥ −x − x² on [0, ½].
- I checked these bounds by quadrature for d ∈ {3, …, 10⁴} and τ up to d/2: 0 violations (`chk_W.py`).

**Lemma R.** The inequality chain is correct: (1−ϵ)e^{ϵ/2} ≤ 1 − ϵ/2 ≤ (1 − ϵ/4)² ≤ (1 − ϵ/4)(1 − η); with ϵ′ = ϵ/4 this
gives the constant 8(1+η′)√π/(ϵ²(1−η)²√log N). No independence between κ and the ζ_j is needed.

**§3 (W-orth).**
- s = n², and x_jᵀy = √(n−1)σ*g_j/s_y.
- The bound on V uses Lemma V at ϑ = θ*. The term 2b₀s_y² ≤ 0.06M + 0.04‖Cε‖²/(n−1) holds because n/(n−1) ≤ 3/2.
- The Chebyshev event with x = n^{1/4} is correct, and e_n·2 log N → 0 because N ≤ n − 1.

**§4 (W-sph).**
- The spectral form of P_H is correct, with e_i(1−e_i)λ_i ≤ 1/(n+1).
- The identity Q − ‖ρ̃‖² = yᵀP_Hy/(n+1) + yᵀP_H(I−P_H)y holds (checked by expansion).
- The lower bound s_y²Q ≥ σ*²E₂ uses (I−P₀)C = C − P₀, with E₂ ~ χ²_{n−1−r₀}.
- The three probability bounds hold: Chebyshev 2/(n−1), 8/m ≤ 16/n since m ≥ n/2 by s₀ + 1 ≤ K ≤ n/2, and Markov 1/x.
- The constant C₀ and the choice of x_n are correct.
- The conditional rotation-invariance argument gives iid ζ_j unconditionally.

**§5–§6.**
- The transfer to random (X_{S₀}, θ*) is correct.
- A1 is correct: x/(1+x) ≥ x(1−x), and the expectation bound follows.
- A2 (i) and (ii) are correct, including the O_P → deterministic step.
- The example θ*_j = s₀^{−1/2} gives ‖μ‖² = n − 1 and ‖θ*‖² = 1.

**Claim B.**
- Iterating Lemma S(1), (2) gives D-ratio ≤ n^{|J|} and a fit factor ≥ 1.
- The product of C(p−s₀, j) with the prior ratio equals C(s₀+j, j)Π(p−s₀−i)/(2p−1−s₀−i).
- Constants: (s₀+1)(p−s₀) − (2p−1−s₀) = (s₀−1)(p−s₀−1); the 1/3 bound holds iff p + 1 ≥ 2s₀.
- At the critical scale each term tends to (λ/2)^j/j!. Fatou-type truncation gives liminf 𝒪^{lb} ≥ e^{λ/2} − 1.
- B2: P(δ ≤ Cρ_n) ≥ ½ makes a deterministic a_n ≤ 2Cρ_n.

**Claim C.**
- (F1)–(F4) are correct.
- X_Tθ = μ exactly, with ‖θ‖² = (b²n⁴/k)(2 + η²k).
- Lemma P: the projection onto span{x_j : j ∈ T′∖S} is correct. Two facts used there, Πx₂ = −cηΣx_j and
  min_x A(β+γx)² + x²/n = Aβ²/(1+nAγ²), are correct. nAγ² ≤ k/n² ≤ 1.
- Reference cost: b²(n−1)/2 ≤ min B_T ≤ b²(n−1); the cost of T′ is b².
- Item 2: q_j ≤ (2/3)2^{−j}, R^T_m ≤ (8/3)p²2^{−m}, and 2^{−⌊k/2⌋} ≤ √2 n^{−6 log 2}. At n = 200 the envelope is
  3.78·66.58²/200^{2.158} ≈ 0.181, and it decreases (24/(12L+3) < 2.158).
- D_T: from the 2×2 determinant formula D_T ≤ (2n² + 2k)/(2n − 1) ≤ 2n, so A ≤ √2/n.
- Item 3, Steps 1–5: the ½-weighting (2ab ≤ a²/2 + 2b²) is correct. The constant 0.0078 equals
  48/(1200·5.298) + 8/(1200·28.07) = 0.00779. Then 0.1243 − 0.0078 − 0.005 ≥ 0.1, and 40/0.975 ≤ 42.
- In Step 5, (3p−1)log 2 + (k/2)log n ≤ 6L² + 25.5L + 5.6 ≤ 12L² (the root is at L = 4.459), and 1/42 − 1/100 = 1/72.4,
  which gives c₁ = 1/73.
- Independent brute-force check (`chk_SB.py`, my own implementation of π): 3,548 (design, data, S₀) cases. The designs
  are iid, strongly equicorrelated and near-duplicate, with Cauchy responses, n ∈ {6, …, 100} and p ∈ {2, …, 7}. Results:
  min odds / (Lemma S(4) right side, all nulls) = 1.041, and min odds/𝒪^{lb}_n = 1.029.
- Lemma P and Step 1, by exact minimisation on small instances (`chk_C.py`): see G5.

### G2 hypotheses used = stated — PASS
Each STATEMENT item (Lemma S 1–4, Prop. A, Cor. A1–A2, Cor. B with B1–B3, Prop. C 1–3 and "what fails") has a proof
using exactly its hypotheses:
- Prop. A uses G, (E), (C), N_n → ∞, s₀ + 1 ≤ K (in Lemma S(4) and in m ≥ n/2), and the witness condition. Under
  (W-sph) it also uses the two logarithmic conditions and the deterministic (X_{S₀}, θ*).
- Corollary B uses only s₀ ≤ K − 1, and B1–B2 use s₀ ≤ p/2 for the 1/3 constant. Claim C uses only its design.

The "columns outside S₀ ∪ 𝒩_n arbitrary" clause is justified: Lemma S(4) is deterministic and sums over 𝒩_n only.
Remark A3 is labelled as a reading, outside the claim. Its two example sequences satisfy the witness and (E)/(C)
conditions as stated (A_log_factor §7.2), and they are in the scope of Theorem 1 (A = 1) and of Cor‑1R (Σ_n = I,
ψ_n = 1, A = max(a, 1)). I checked this against `W3-POST/STATEMENT.md` lines 62-76 and 106-118.

### G3 no hidden assumptions — PASS
- Domains are explicit:
  - n ≥ 3, p ≥ 2, S = ∅ allowed, s₀ = 0 covered in B.
  - s₀ + 1 ≤ K in S(3)-(4) and A; N ≤ n − 1 − r₀ under (W-orth).
  - Lemma W needs τ ≤ d/2, which holds eventually by (log N)² = o(n).
  - Claim C uses n ≥ 200 for the elementary bounds. The STATEMENT also notes that the signal condition forces
    n ≥ C_b(1 + σ*²/b̄²)(log n)².
- What is random is explicit: in (W-orth) only ε; in (W-sph), ε and the null directions, with the conditional law
  argument written out.
- Uniformity: both bounds depend only on the listed quantities.
- Rank-deficient X_{S₀}: §4 uses r₀ = rank, and G + I and H stay positive definite.
- One domain NIT (N1 below).

### G4 statuses and citations — PASS
- Every lemma file carries "PROVED (by this seat, unchecked)", and STATEMENT and REPORT state it verbatim.
- Nothing is labelled checked.
- The registry blocks say `correct:PENDING`.
- `citecheck.py`: 42 checks, 0 MISS (re-run). I also read the cited ranges myself:
  - [W3P] §0 and line 104 (the conjecture);
  - [L1a′] lines 10-16 and Remark 2 at lines 50-55 (the coefficient bound marked "open");
  - [LB] lines 25 and 28;
  - [P2S] lines 44 and 58-62;
  - [1a″] lines 7-14;
  - W3-POST REPORT line 190 and W3-POST2 REPORT line 189-190.
- The "what fails" reading of Claim C (§4) is accurate:
  - [L1a′]'s bound is uniform in (σ*², M, M′). On 𝔇_n, Θ^T_{n,m_n} ≥ (1 − e^{−c₁nb²})n²/((n+1)√n) → ∞, so no
    M′-free version holds.
  - The file correctly notes that [L1a′] remains true with M′_n = ‖θ‖²/n, so there is no contradiction.
  - For [1a″], Θ″ ≥ (1 − ·)n/2 → ∞ with zero approximation error. The B_n/(log n)² → ∞ construction is valid:
    b_n² = C_bV₀(log n)²/n ≤ b̄² eventually, and min B_T ≤ b_n²(n−1) ≤ B_n.
- Remark A3 and REPORT §1(a) keep the upper bounds conditional on `W3-POST:Thm-1` and `Cor-1R`.
- Numerical observations are labelled as such: (O3), STATEMENT §5, the a_boundary qualification.
- Small wording NITs N2–N5.

### G5 constants and rates — PASS
- Λ_n = P_n n^{−1/2}N√(2τ/π) with τ = 2 log N, which equals (s₀+1)[2N/(2p−1−s₀)]√(log N/(πn)). The 1/√π is the
  Gaussian truncated mean 2√(log N/π), and the truncated second-moment asymptote N/√(π log N) is also correct.
- c(p, s₀), 𝒪^{lb}_n and the e^{−λ/2} limit are correct.
- Claim C, for all n ≥ 200:
  - k = ⌈12 log n⌉, with p ≤ 12L + 3 ≤ n/2.
  - C_b = 1200 and c₁ = 1/(73V₀), both re-derived; the cutoff bound n²R^T_{m_n} ≤ 1 holds.
  - `chk_C.py` evaluates exactly (mpmath): RESULT_C.
  - It also checks Step 5's 12L² bound and 4(k+1) ≤ 48L + 8 on the same grid, and Lemma P and Step 1 by exact
    minimisation over all |S| ≤ k/2 at (n, k) ∈ {(30, 6), (50, 8), (200, 10)}: RESULT_P.

### G6 fidelity to the coded target and to the numerics — PASS
- `numerics/core.py` implements exactly the target of `v3_score.h:40-71, 196-224`: K = min(p, n/2), ν = a₀ + n/2,
  H = (n+1)G + I, A = G + I, Q = yᵀy − n zᵀH⁻¹z, log w(k) = −log 2 − log C(2p−1, k), score −½(log det H − log det A)
  − ν log(2b₀ + Q).
- `a_orth.py` is correct: Q_S = (n−1) − Σz²/n and D_S = n^{|S|} on XᵀX = (n−1)I. The Gamma-mixture identity for
  (1 − x)^{−ν} with rate 2b₀ + Q_{S₀}, and the elementary-symmetric DP in the u = log t variable, are right. It is
  validated against brute force (1.4e-13).
- `a_sph.py`: the reduction (projections of Cx^r_j on span(X_{S₀}, ρ̃) iid N(0, I_{s₀+1}), remainder χ²_{n−2−s₀}) is
  exact in law.
- `c_counter.py`: the arm means are right, and the structured Schur formulas are validated (1.9e-13 float64 and
  1.4e-15 mpmath).
- Every quoted number matches the outputs:
  - medians 1.23–1.51 at n = 100 and 1.003/1.007 at n = 25600;
  - P(≥ 0.75Λ) ≥ 0.93;
  - spherical medians 0.968–1.089, with P ≥ 0.99;
  - boundary 0.713/0.719/0.613;
  - E2 1.26–1.37 (min 0.983);
  - B: 55,740 cases, min 1.033; 8,064 pairs;
  - λ = 4 cap 0.1353;
  - C: 0.997/1.000, 0.95/0.47, control ≤ 3.149e-13, and n²R = 3.564e-4.
- The scope is reported honestly:
  - "restricted odds" is a lower bound;
  - "exact formula evaluated by quadrature, not a certified enclosure";
  - one-step odds only for p ≫ n and for the boundary;
  - Claim C runs use scaled-down k and are "far below the theorem's signal constant".

## Findings

No FATAL, MAJOR or MINOR findings.

- **N1 (NIT) `STATEMENT.md:73` (Corollary A1, last sentence).** "With p = ⌊n^a⌋, a > 0". Under (W-orth) with
  𝒩_n = [p]∖S₀, this sequence exists only for p ≤ n − 1 − r₀, so only for a < 1, not a = 1, since ⌊n⌋ = n > n − 1.
  The claim is vacuous rather than false there, and Remark A3 already uses p = min(n − 1, ⌊n^a⌋).
  *Correction:* append "(under (W-orth) this needs p ≤ n − 1 − r₀, e.g. p = min(n − 1 − s₀, ⌊n^a⌋); under (W-sph) any
  a > 0)".
- **N2 (NIT) `REPORT.md:9`.** "all are asymptotic statements about the exact coded target π". Lemma S, Corollary B and
  Proposition C items 1–2 are deterministic finite-n statements.
  *Correction:* "Lemma S and Corollary B are deterministic (every n, design and data set); Propositions A and C are
  asymptotic; all concern the exact coded target π."
- **N3 (NIT) `REPORT.md:46-47`.** "with p = s₀ + 1 … π(S₀) → 1 is possible with s₀ ~ √n" is asserted without proof or
  pointer. I believe it is true: the single superset has prior ratio 1, and strong signals suppress the subsets. But
  the REPORT should not state it as fact.
  *Correction:* add "(heuristic, not proved here)" or cite where it is shown.
- **N4 (NIT) `REPORT.md:111` (sharpness table, first row).** "Settled (attained) on the witness classes of Claim A".
  The √(log p) lower bound is proved on the witness classes. The two-sided reading "rate exact" holds only on the
  sequences of Remark A3, where `Thm-1`/`Cor-1R` apply, and is conditional on them.
  *Correction:* "Settled: the √(log p) factor is present (lower bound, proved here) on the witness classes of Claim A;
  the rate r_n is exact on the two sequences of Remark A3 (upper bound from W3-POST:Thm-1 / Cor-1R)."
- **N5 (NIT) `ASSUMPTION_MAP.md:16`.** The row labels (log N_n)² = o(n) an "ARTEFACT-threshold of the route". It also
  asserts that beyond it "the sphere law is lighter than Gaussian and the constant changes". That second claim is not
  shown, and if true it would make the threshold genuine rather than an artefact.
  *Correction:* "route threshold; behaviour of the constant beyond it not determined (outside R1 anyway)".
- **N6 (NIT) `REPORT.md:88-89`.** "all sizes ≤ K against sizes ≤ s₀ + 60: 3·10⁻¹³". The maximum in
  `a_orth_out.txt` V2(i) is 3.5·10⁻¹³.
  *Correction:* "≤ 3.5·10⁻¹³".

Counts: FATAL 0, MAJOR 0, MINOR 0, NIT 6.

## Score

9.3 / 10. The mathematics is correct, and I re-derived it line by line. The statuses are honest, the citations are
accurate, and the numerics are faithful. The remaining points are wording NITs in the REPORT, ASSUMPTION_MAP and one
STATEMENT corollary.

COUNCIL-VERDICT round=R2 manifest=4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14 seat=opus score=9.3 gates=PASS
