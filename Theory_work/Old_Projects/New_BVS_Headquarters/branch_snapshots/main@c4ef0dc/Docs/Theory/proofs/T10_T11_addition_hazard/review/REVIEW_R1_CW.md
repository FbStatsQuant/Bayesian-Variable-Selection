# Review round 1 — CW reviewer (Claude Work, Opus 5.5 xhigh, native read-only Plan agent)
Packet: %TEMP%/T10_review/CW (STATEMENT.md v2, PROOF_v3.tex/.pdf, REPORT_FORMAT.md). Reply saved verbatim.

---

I found no mathematical error in the proof, but the verdict is **not verified**. Conclusion (iv-c) depends on budget formulas that are not in the packet, so I could not check them. That is finding F1; every other conclusion checks out, and the other eight findings are presentation issues.

# Review report: T10 (old T11), PROOF_v3

**Scope read:** `STATEMENT.md`, `REPORT_FORMAT.md`, `PROOF_v3.tex` and `PROOF_v3.pdf`, all in `<PC_TEMP_PATH>`. I compared all 7 PDF pages with the source; they match. Every check below was done by hand. I ran no simulations.

## Findings

**F1**
- **Location:** §6 (iv-c), tex lines 212–215. The sentence starts "By 00_COMMON §2 the final run has 4N_e particles …" and goes on to give N_e = 4^e max(2500,n,p), T_e = 4^e max(1000,ℓ²), ℓ = ⌈log₂(2n+1)⌉, L = max(4,⌈log₂(n+1)⌉) and Q_f = 4N_e(T+L+5).
- **Severity:** gap.
- **Claim:** (iv-c)(1) and (iv-c)(2) rest on these budget formulas. STATEMENT.md does not contain them. It only says "the declared budgets of 00_COMMON §2" and gives the count 4N_e(T+L+4) ≤ 4N_e(T_e+L+4). I have not seen the source, so the formulas are unverified, and (iv-c) is unverified with them.
- **Evidence:** the conclusion truly depends on how fast the budgets grow:
  - With p = n, h_k ≥ r_k/2 ≥ (k+1)/(4n√(n+1)).
  - So (2), h_k·R → 0, holds only if R = o(n^{3/2}).
  - STATEMENT.md says nothing about growth. If N_e were of order n², or T_e of order n, (2) would fail.
  - If the quoted formulas are correct, the proof's arithmetic is right:
    - For n ≥ 2500 and p = n, N_e = 4^e·n ≤ 4n.
    - T_e ≤ 4(1000+ℓ²).
    - L ≤ max(4,ℓ) ≤ ℓ+4, because n+1 ≤ 2n+1.
    - R ≤ 16n(4000+4ℓ²+ℓ+8) = 16n(4008+4ℓ²+ℓ).
    - (1): R·h_k/m ≤ 16(k+1)n^{−3/2}(…) → 0.
    - (2): h_k·R ≤ 16(k+1)n^{−1/2}(…) → 0, since ℓ = O(log n).
    - "Exactly one Gibbs-j step per particle-round" follows from the round definition.
  - Repair: put the budget definitions into STATEMENT.md, or check them against 00_COMMON §2.

**F2**
- **Location:** §4, "Data" paragraph, tex line 91; Remark 6(a), line 174.
- **Severity:** exposition.
- **Claim:** The proof says the example is admissible ("finite entries, no constant column, y^r non-constant", "sample SD 1"). Those conditions come from 00_COMMON §1, which is not reproduced in the packet. Remark 6(a), "p = 2 … production method takes the exact branch", is also unverified, but it is not used.
- **Evidence:** the example meets every condition STATEMENT.md does state:
  - n ≥ 400 ≥ 3, p = 2 ≥ 1, ‖y‖² = n−1 > 0.
  - The columns are centred and have squared norm n−1, so standardisation leaves them unchanged.
  - The divisor n−1 is supported by STATEMENT's own ‖y‖² = n−1.
  - The neighbour-graph rule as stated ("always including j's single largest-|r| partner") gives N(1) = {2} and N(2) = {1} even though r₁₂ = 0.
  - With B = min(⌊√n⌋, 1, 16) = 1, the blocks must be singletons.
  - This finding does not block the verdict.

**F3**
- **Location:** §4, "Comparison chain", tex line 125.
- **Severity:** exposition.
- **Claim:** "β replaced by 0" is not literally well defined. At β = 0, γ ∝ (½,0,0,0), so the G₁ inclusion ratio at b is 0/0, and so is the U/N acceptance ratio γ(b)/γ(a).
- **Evidence:** the explicit description that follows ("G_j removes j surely …; I moves to ∅ surely") does define valid kernels, and that is what the argument uses. The total-variation bounds hold:
  - G_j: β/(3+β) or β/(1+β), both < β.
  - U and N: 0.
  - I: 1−π₀(∅) = (2β+β²)/(3+2β+β²) ≤ β. This holds for every β ≥ 0, since it reduces to 0 ≤ β+β²+β³. So "because β ≤ 1" on line 100 is true but not needed.

**F4**
- **Location:** §5, "Model of a run", tex line 179: "using a stream variate not yet consumed, hence independent of 𝓕_{u⁻}".
- **Severity:** exposition.
- **Claim:** The "hence" is not spelled out. It needs two facts:
  - the number of variates consumed before step u's draw is a stopping time for the stream filtration, and 𝓕_{u⁻} is the stopped σ-field;
  - an i.i.d. sequence has the strong Markov property at such a time, so the next variate is uniform and independent of 𝓕_{u⁻}.
- **Evidence:** both facts are standard and hold for a sequential algorithm under EX-S. Given them, (7), (iii-a) and (iii-b) follow as written: (iii-b) uses Tonelli, the tower property, and the measurability of φ ↦ o_j(S,φ) since it is continuous.

**F5**
- **Location:** §5, "Conditional form", tex line 192.
- **Severity:** exposition.
- **Claim:** 𝓘 is called "a set of step indices". In the global enumeration, though, the indices of final-run steps depend on how long the pilot and calibration ran, which may be random. The example quietly re-indexes the final run. Also, "φ_u is σ(𝓒)-measurable" relies on the final-run design in 00_COMMON, which is not in the packet.
- **Evidence:**
  - The identity still holds term by term when 1{u∈𝓘} is 𝓖-measurable, by conditional monotone convergence.
  - The formal clause of (iii-b) ("with 𝓖 trivial and non-random φ_u") is proved completely: E[1_{A_u} o_j(S,φ_u)] = P(A_u)·o_j(S,φ_u).
  - STATEMENT.md itself offers the final-run case only as an "e.g.".

**F6**
- **Location:** §6 (iv-d), tex line 220: "no other kernel leaves Ω".
- **Severity:** exposition.
- **Claim:** This is asserted without argument.
- **Evidence:** it is true from STATEMENT's kernel definitions:
  - Both swaps propose S′ = S − j + l, so |S′| = |S| ≤ K.
  - The independence step proposes from π₀, which is zero off Ω because ϖ is.
  - So no kernel moves a size-K state S to S+j, which has size K+1.
  - o_j(S,φ) = 0 also uses γ_φ(S) > 0 in the denominator (T22 Lemma 1), which the proof uses without saying so.

**F7**
- **Location:** §2, Part (i), tex lines 53–66.
- **Severity:** exposition.
- **Claim:** The proof divides by γ_φ(S) and takes real powers [∏r_b]^{1−φ} and BF^φ. Both need γ_φ(S), r_b and BF to be positive. T22 Lemma 1 supplies this, but it is not cited at that point.
- **Evidence:** T22 Lemma 1, as quoted in STATEMENT.md, gives positivity and finiteness of all of these.

**F8**
- **Location:** Remark 1 (line 68) and "Hypothesis use" (line 223).
- **Severity:** exposition.
- **Claim:** Both describe what the T22 lemmas need ("beyond yᵀy > 0", "only b₀ > 0 and ν > 0", "any real X"). These go beyond the cited statements in the packet and are unverified. They are outside the statement and not used, so they do not block.
- **Evidence:**
  - I checked the "For the reader" sketch. ‖y−X_Tβ‖² + n⁻¹(‖X_Tβ‖²+‖β‖²) = yᵀy − 2βᵀz_T + n⁻¹βᵀH_Tβ. Its minimiser is β = nH_T⁻¹z_T, with value Q_T, so the identity is correct.
  - The determinant-lemma ratio (1+(n+1)ξ)/(1+ζ) ≤ n+1 holds, because ξ ≤ ζ in the Loewner order.

**F9**
- **Location:** Remark 6(c), line 174.
- **Severity:** exposition.
- **Claim:** The enumeration numbers are corroboration only and are not used. I did not re-derive the visit probability 0.01978.
- **Evidence:** the terminal-occupancy figure 8.06·10⁻⁴ is consistent:
  - Every round has exactly one I step, which outputs a draw from π₀.
  - Here d ≡ 0, so γ_φ ∝ π₀, and every elementary kernel preserves γ_φ. So X₅ ~ π₀.
  - P(X₅ = ab) = π₀(ab) = β²/(3+2β+β²) = 1/1241 ≈ 8.058·10⁻⁴ at n = 400.
  - This is within Proposition 5's bound (4/3)β² ≈ 3.33·10⁻³.

## How each conclusion was checked

- **(i): proved.**
  - γ_φ = ϖ[∏r_b]^{1−φ}BF^φ, because γ₀e^{d} = ϖ·BF.
  - Only the block containing j changes, so a_j = [w(k+1)/w(k)]·[m(U+j)/m(U)]^{1−φ}·[m(S+j)/m(S)]^φ.
  - C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k).
  - Each bracket is ≥ (n+1)^{−1/2} and the exponents are ≥ 0 and sum to 1, so a_j ≥ r_k.
  - o_j = a_j/(1+a_j), and x ↦ x/(1+x) is increasing, so o_j ≥ h_k.
  - At φ = 0 this gives π₀(S+j)/π₀(S) ≥ r_k.
- **(ii) and its "event" sentence: proved.**
  - Path law (4).
  - The set 𝓔 has a!(m−a)! orders, with a ≤ K−k ≤ p ≤ m, so P(σ ∈ 𝓔) = C(m,a)⁻¹.
  - Step i acts at |S_{i−1}| = k+i−1 < K with j_i ∉ S_{i−1}, so part (i) gives each step probability ≥ h_{k+i−1}.
  - Summing over σ₀ ∈ 𝓔 is a sum over disjoint events, and that union is exactly the stated event.
  - a = 0 is trivial, and a = 1 gives h_k/m.
- **(ii-neg): proved.**
  - Scores: G_T = (n−1)I, z_T = 0, H_T = n²I, D_T = n^t, BF = β^t, d ≡ 0.
  - Weights: w = (½, ⅙, ⅙); π₀(ab) = β²/(3+2β+β²).
  - All kernel descriptions check out.
  - h₁ = 1/(1+√(n+1)) = β/(β+√(1+β²)).
  - The hybrid argument in Lemma 2 is correct.
  - I recounted Lemma 3 by enumerating every possible set of labels before G₂, and before G₁:
    - E₂ (sets before G₂): ∅ gives 24 orders; {U,N} gives 2·2 = 4; {G₁,U,N} allows only UG₁N or NG₁U, giving 2; every other set fails. Total 30.
    - E₁ (sets before G₁): {U} or {N} gives 2·6 = 12; {G₂,U} or {G₂,N} allows only the order G₂, flip, giving 2·2 = 4; every other set fails. Total 16.
  - First-entry union bound: β²/3 + β(23/60 + 10β) = (23/60)β + (31/3)β².
  - f(1/20) = 0.9·(1+√401)/20 ≈ 0.94612 < 1, and f is increasing.
- **(iii-a) and (iii-b): proved**, subject to the presentation points F4 and F5.
- **(iv-a) and the supplementary ratio: proved.**
  - The three cases (I after the later Gibbs step G*, between the two Gibbs steps, before the earlier one G°) partition the orders; I checked the bounds β²/3, β² and (4/3)β².
  - The ratio bound is (20/3)β(β+√(1+β²)) ≈ 0.3504 < 1 at β = 1/20. It increases in β and tends to 0.
- **(iv-b): proved.**
  - p ≤ 2p−k−i−1 ≤ 2p, so r ≥ 1/(2p√(n+1)); r < 1, so h ≥ r/2.
  - m ≤ 2p+2 ≤ 4p and C(m,a) ≤ m^a/a!.
  - √(n+1) ≤ √2·n^{1/2}.
- **(iv-c): not verified** (F1). The arithmetic is correct if the quoted budgets are.
- **(iv-d): proved**, with F6 as a presentation point.

## Files reviewed
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`
- `<PC_TEMP_PATH>`

**VERDICT: not verified**
