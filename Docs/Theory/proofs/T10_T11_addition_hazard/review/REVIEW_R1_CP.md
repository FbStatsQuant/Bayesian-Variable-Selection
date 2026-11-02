# Review round 1 — CP reviewer (Claude Personal, Opus 5.5 xhigh, T3 delegate_task, clientRequestId T10-review-CP-round1)
Packet: %TEMP%/T10_review/CP (STATEMENT.md v2, PROOF_v3.tex/.pdf, REPORT_FORMAT.md). Reply saved verbatim.

---

**Reviewer report: T10 (old T11), PROOF_v3, checked against STATEMENT.md**

I read STATEMENT.md, REPORT_FORMAT.md, PROOF_v3.tex and PROOF_v3.pdf (the PDF matches the source). I wrote nothing to the packet folder and ran nothing.

## What I checked by hand

- **Part (i).**
  - The prior ratio is correct: w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k). It needs k ≤ p−1, which follows from k < K ≤ p.
  - Display (3) is correct: γ₀e^{d} = ϖ·BF, so γ_φ = ϖ·(∏r_b)^{1−φ}·BF^φ.
  - Only block b changes when j is added, and r_b(U+j)/r_b(U) = m(U+j)/m(U).
  - Lemma 2 is applied correctly with T = U and with T = S, and raising a ratio that is at least (n+1)^{−1/2} to a nonnegative power keeps the bound. This gives a_j ≥ r_k.
  - o_j = a_j/(1+a_j), and x/(1+x) is increasing, so o_j ≥ h_k.
  - The π₀ clause is the same bound at φ = 0. Positivity comes from Lemma 1.
  - The "for the reader" sketch is also correct:
    - The ridge minimum is y'y − z'(H/n)^{-1}z = Q_T.
    - The determinant ratio is (1+(n+1)ξ)/(1+ζ) ≤ n+1, because ξ ≤ ζ.
- **Part (ii).**
  - Path law (4) holds.
  - The number of orders whose first a labels are the Gibbs labels of J is a!(m−a)!, and a ≤ K−k ≤ p ≤ m.
  - Each step size satisfies |S_{i−1}| ≤ k+a−1 < K.
  - Summing the trailing kernels to 1 and summing over the disjoint orders gives C(m,a)^{−1}∏h_{k+i}.
  - The case a = 0 is trivial.
  - The intermediate claim (that the bound also covers the event "the first a labels are J's Gibbs labels and each adds") is also proved.
- **Example: data and method objects.**
  - G_T = (n−1)I and z_T = 0.
  - H_T = ((n+1)(n−1)+1)I = n²I, so D_T = n^t and BF = β^t.
  - B = min(⌊√n⌋, 1, 16) = 1, so the blocks are forced to be singletons.
  - The neighbour rule gives N(1) = {2} and N(2) = {1}.
  - m = 5, w = (1/2, 1/6, 1/6), and d ≡ 0.
  - 1 − π₀(∅) ≤ β holds for every β ≥ 0.
  - The two Gibbs inclusion probabilities are β/(3+β) and β/(1+β), both below β.
  - The U, N and I kernels are as stated, including N rejecting at ab and the factor |N(1)∖a|/|N(2)∖b| = 1.
  - r₁ = (n+1)^{−1/2}, so h₁ = β/(β+√(1+β²)).
- **Example: coupling and counting.**
  - The hybrid argument in Lemma 2 (coupling) is sound.
  - The step-wise total-variation distances are o < β for the Gibbs steps, 0 for U and N, and 1 − π₀(∅) ≤ β for I.
  - I recounted Lemma 3 by enumerating the possible label sets before G₂ and before G₁:
    - P⁰(E₂) = (24 + 4 + 2)/120 = 30/120.
    - P⁰(E₁) = (12 + 4)/120 = 16/120.
  - Concrete checks: the order U G₁ N gives a→b→b→a, which is in E₂. The order U N G₁ gives a→b→a→∅, which is not.
- **Proposition 4 ((ii-neg)).**
  - The first-visit decomposition is valid.
  - The constants are right: β²/3 + β(23/60 + 10β) = 23/60·β + 31/3·β².
  - f(1/20) = 0.9 × 1.05125 = 0.946 < 1, and f is increasing.
- **Proposition 5 ((iv-a)).**
  - The three cases, split by where I falls relative to the two Gibbs steps, partition the orders.
  - Each case is bounded by at most 4/3·β².
  - The ratio bound (20/3)·β·(β+√(1+β²)) = 1.05125/3 = 0.350 at β = 1/20.
  - Independent corroboration: here d ≡ 0, so every one of the five kernels leaves π₀ invariant, and I outputs an exact π₀ draw. So X₅ ~ π₀ exactly, and P(X₅ = ab) = β²/(3+2β+β²). At n = 400 this is 0.0025/3.1025 = 8.058·10⁻⁴. That matches Remark 6(c) and is below the 4/3·β² bound.
- **Part (iii).**
  - A_u is 𝓕_{u⁻}-measurable.
  - Display (7) is the content of EX-S.
  - φ ↦ o_j is continuous, so o_j(S,φ_u)·1_{A_u} is measurable.
  - Tonelli and the tower property are used correctly, and the bound h_k does not depend on φ.
- **Part (iv-b).**
  - k+i+1 ≤ p gives p ≤ 2p−k−i−1 ≤ 2p, so 1/(2p√(n+1)) ≤ r ≤ 1/√(n+1) < 1 and h ≥ r/2.
  - m ≤ 2p+2 ≤ 4p, and C(m,a) ≤ m^a/a!.
  - 16p²√(n+1) ≤ 16√2·n^{2A+1/2}.
- **Part (iv-c), arithmetic only.**
  - h_k ≤ (k+1)n^{−3/2} and h_k/m ≤ (k+1)n^{−5/2}.
  - T + L + 4 ≤ 4(1000+ℓ²) + ℓ + 8 = 4008 + 4ℓ² + ℓ.
  - So R·h_k/m ≤ 16(k+1)n^{−3/2}(…) and h_k·R ≤ 16(k+1)n^{−1/2}(…). Both tend to 0.
- **Part (iv-d).** Correct, by T09(ii) and ϖ = 0 off Ω.

## Findings

**1.**
- **Location:** §6, paragraph (iv-c), the sentence beginning "By 00_COMMON §2 the final run has…".
- **Severity:** gap (verification only; no error found).
- **Claim:** The proof of (iv-c)(1)–(2) relies on budget definitions that appear neither in STATEMENT.md nor among the cited results:
  - N_e = 4^e·max(2500, n, p);
  - T_e = 4^e·max(1000, ℓ²);
  - ℓ = ⌈log₂(2n+1)⌉;
  - L = max(4, ⌈log₂(n+1)⌉);
  - Q_f = 4N_e(T+L+5).

  STATEMENT.md gives only the count 4N_e(T+L+4) ≤ 4N_e(T_e+L+4). From the packet I cannot confirm that these formulas are quoted correctly.
- **Evidence:** The conclusion depends on them. Conclusion (2) needs N_e(T_e+L) = o(n^{3/2}), and conclusion (1) needs N_e(T_e+L) = o(n^{5/2}). Both would fail if, for example, N_e grew like n·p = n². Assuming the formulas are as quoted, every inequality in the paragraph checks out (see above).
- **To close it:** confirm the quoted formulas against 00_COMMON §2, or copy them into STATEMENT.md.

**2.**
- **Location:** §4, "Data" paragraph.
- **Severity:** exposition.
- **Claim:** Two things are taken from 00_COMMON §1, which is not in the packet: the admissibility list (finite entries, no constant column, y non-constant) and the column scaling of X (sample SD 1). STATEMENT.md fixes only n ≥ 3, p ≥ 1 and ‖y‖² = n−1.
- **Evidence:** The example satisfies every condition STATEMENT.md lists, and sample-SD scaling matches ‖y‖² = n−1. The existential conclusions (ii-neg) and (iv-a) do not depend on the scaling. Any standardisation of an orthogonal, centred design is again orthogonal and centred with ‖x_j‖² = c, which gives BF({j}) = √((c+1)/((n+1)c+1)). For c = n this is below n^{−1/2}, so the stated bounds hold unchanged. For c = 1 it is about √2·n^{−1/2}, and the bounds still hold for large n because 23/60·√2 < 1. Only the explicit threshold n ≥ 400 depends on the convention, and that threshold is not part of the statement.

**3.**
- **Location:** Remark 6(a).
- **Severity:** exposition.
- **Claim:** The counterexample uses p = 2, where (per the remark, which I could not check) production takes the exact branch.
- **Evidence:** This is enough for (ii-neg) and (iv-a) as worded, since they only require admissible data. It is worth saying plainly that the example does not show the failure in the regime where SMC rounds actually run. The remark's claim about the exact branch is unverified but carries no weight in the proof.

**4.**
- **Location:** §5, "Conditional form".
- **Severity:** exposition.
- **Claim:** Two points:
  - The final-run example uses method facts that are not in the packet: 𝒞 is realised before every final-run step, and the frozen grid fixes the stage and φ_u of each re-enumerated final-run step. These are unverified but carry no weight, because the statement itself gives this case only as an "e.g.".
  - Moving the countable sum inside the conditional expectation needs conditional monotone convergence, which the proof does not state. It is standard.

**5.**
- **Location:** §6, paragraph (iv-d).
- **Severity:** exposition.
- **Claim:** "No other kernel leaves Ω" is asserted without its one-line reason.
- **Evidence:** The two swaps preserve |S|, and the independence proposals are π₀ draws, which are supported on Ω. So the claim is true.

**6.**
- **Location:** Remark 1 and "Hypothesis use".
- **Severity:** exposition.
- **Claim:** Two side remarks are not part of the statement and cannot be checked from the cited statements alone:
  - part (i) holds for any real X;
  - T22's Lemmas 1–3 use only b₀ > 0 and ν > 0.

  The "for the reader" sketch, which I checked, supports both. Neither is needed.

**7.**
- **Location:** Remark 6(c).
- **Severity:** exposition.
- **Claim:** The enumeration figures are partly unverified; they are not used in the proof.
- **Evidence:**
  - I confirmed h₁ = 1/(1+√401) = 0.04756 and h₁/5 = 0.00951.
  - The terminal occupancy 8.06·10⁻⁴ equals π₀(ab) exactly (invariance argument above).
  - I did not check the visit probability 0.01978. A first-order estimate is (46/120)·β/(1+β) + π₀(ab) ≈ 0.0191, plus O(β²) corrections, which is consistent with it.

No mathematical error was found in any numbered result, lemma, proposition or explicit constant. The only reason the verdict is not "verified" is Finding 1: (iv-c) depends on budget formulas I cannot see. If those formulas match 00_COMMON §2, the proof establishes every conclusion of STATEMENT.md.

**VERDICT: not verified**
