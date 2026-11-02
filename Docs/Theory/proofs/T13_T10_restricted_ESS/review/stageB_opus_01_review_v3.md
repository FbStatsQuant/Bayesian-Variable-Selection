# Stage B — Opus 5.5 (xhigh) reviewer, review of PROOF_v3 (reply saved verbatim, 2026-10-22)

**T13 (T10) restricted ESS: Stage B review of PROOF_v3**

I found no mathematical error. Everything I could check holds: the identities, the bounds, the construction argument, the witness sets and grids, and the seven numerical checks (rerun and recomputed independently). The verdict is still "not verified". The witnesses in (ii)(c)–(d) and Lemma 1 rely on method definitions that live outside the packet: the m(S) formula, the standardisation convention, the block construction and the budget formulas. I cannot confirm the proof copied them correctly (findings 1–4).

**Files reviewed (packet only)**
- <PC_TEMP_PATH>
- <PC_TEMP_PATH>
- <PC_TEMP_PATH> (8 pages; I read all of them and the text matches the .tex, including the Appendix A script and its output)
- <PC_TEMP_PATH>

**Computations run** (all read-only, `python -I -` on stdin, no files written)
- **C1. Appendix script rerun.** I piped PROOF_v3.tex lines 178–267 into Python 3.12.7 with mpmath 1.3.0. The output matches the printed output line for line, and all seven checks are True.
- **C2. Independent recomputation** (80-digit mpmath, plain arithmetic, not intervals), by a different route:
  - Z̄_ψ is summed by category counts C(38,k), C(38,k−1), C(38,k−2) instead of through σ(·).
  - V_c and V_d are built as explicit lists of sets and summed set by set.
  - Set checks: |V_c| = 117, and no member contains both j₁ and j₂. |V_d| = 782, with largest set size 4.
  - Witness (c) values: Z_c/P = 0.98416299568461360238; a_c(1) = 0.927103194144611; a_c(2) = 0.572683997289202; 1+χ²(q₁‖q₀) = 1.5330546700532342666.
  - Witness (d) values: α = 0.98416299568461360238; β = 0.99625078507155995086; β−α = 0.0120877893869463; ρ_{V_d}(0,½) = 0.97081344087164655662; ρ_{V_d}(½,1) = 0.91376273084997638413.
  - a_d at ψ = 0, ½, 1, 3/2: 0.98422638777161836561, 0.98437688076947620018, 0.98486382153002827334, 0.98626326532199482374.
  - Display-only values: re^D = 0.06154633259855; re^{2D} = 0.718509684822948.
  - All of these agree with the proof.
- **C3. Explicit data set.** I built an orthonormal basis of 1^⊥ in ℝ⁴² by QR, set x_j = √41·e_j, and formed y as in §5.1.
  - Column means are about 1e-16. Sample SDs (n−1 denominator) of every column and of y are 1.0000. The population SD (n denominator) of y is 0.98802.
  - I compared log BF(S) from the m(S) formula as written in Lemma 1 against the Lemma 4 closed form. Over 400 random S of size up to 9, many containing j₁ and/or j₂, the largest difference is 1.1e-13.
- **C4. Soundness of mpmath's interval arithmetic** (the script's `mpmath.iv`):
  - All numerators and denominators of ϖ(k) have at most 71 bits, so converting them at 50 digits is exact and the intervals contain them.
  - Over 300 random rational intervals, iv.log, iv.exp and iv.sqrt (900 tests) always contained the 200-digit reference value.
- **C5. Integer arithmetic.** C(40,20) = 137846528820. Σ_{k≤21} C(40,k) = 749961486698 > 502400 = (5·512 + 4·2500)·40. ⌈log₂ 83⌉ = 7. ⌊√42⌋ = ⌊√40⌋ = 6. 43·41 + 1 = 1764 = 42². t₁ + t₂ = 0.927807 < 0.928.

**Part-by-part coverage**
- **(i):** Verified. Lemma 2 with A = Ω and Lemma 3 with A = V give the identity for all real u, v. The χ² support condition holds by Lemma 1. Depends on Lemma 1 (finding 1) only for positivity.
- **(ii)(a):** Verified. ε_C < 1 gives (1−ε_C)² > 0, and a(v) ≤ 1.
- **(ii)(b):** Verified. Every appended point passes ρ_V(u, ·) ≥ 0.90 against the current left point, which is the previous grid point. Strict progress holds, and φ_{t−1}, φ_t, w_t lie in 𝓔_grid by definition. See finding 6.
- **(ii)(c):** The algebra, the set V_c, its method form, the grid, monotonicity and the certified inequalities are all verified (C1, C2). Whether this is a *method-class* witness depends on findings 1–4.
- **(ii)(d):** Same status as (ii)(c). In addition, a_d is strictly increasing because β > α (certified), so the minimum over 𝓔_grid is attained only at φ₀, and the minimum over {w₁, w₂} is at w₁ = 1, not w₂ = 3/2.
- **(iii):** Verified: the identity (factors checked), the W = V case, the bound (each factor bounded by 1 or by (1−ε_C)⁻², and ρ⁻¹ ≤ 10/9), and the grid consequence. There is no circularity: the proof of (ii)(b) does not use (iii).
- **(iv)(a):** Verified: V(𝒫) ⊆ 𝒫 ∪ {∅}, and ∅ ∉ 𝓜.
- **(iv)(b):** Verified: F′_V = F_V because V ⊆ Ω′; ρ′_V = ρ_V; the transcripts of the implementation coincide by induction, with comparisons exact under EX-A.
- **"No assertion derives particle mixing from ESS":** Remark 5; nothing in the proof does so.

**Findings**

1. **Location:** Lemma 1 (Positivity) and its proof; Lemma 4 and its proof; §5.1.
   **Severity:** gap.
   **Claim:** The proof uses a specific formula for m(S) that I cannot check against its source. STATEMENT.md defines m(S) only by reference to 00_COMMON §1, which is not in the packet. The formula the proof uses is:
   - m(S) = (2b₀)^{a₀} Γ(ν) / (π^{n/2} Γ(a₀)) · D_S^{−1/2} (2b₀ + Q_S)^{−ν}
   - H_S = (n+1)G_S + I, and D_S = det H_S / det(G_S + I)
   - Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S
   - b₀ = a₀ = 0.01, and ν = a₀ + n/2

   The proof never states the definition of Q_S or the values of a₀ and b₀. b₀ = 0.01 appears only implicitly in "2b₀ + Q_S ≥ 0.02", and a₀ only through ν = 0.01 + n/2 in Lemma 4.

   This formula carries real weight. The statement requires positivity to be "derived from these definitions" (Lemma 1), and Lemma 1 supports every part. Lemma 4 and every witness number also depend on it.

   **Evidence:** The formula is internally consistent:
   - The displayed identity in Lemma 1 is correct: expanding gives yᵀy − 2n zᵀH⁻¹z + n zᵀH⁻¹z.
   - The formula is exactly the marginal likelihood of the model β | σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(a₀, b₀). The ratio of prior to posterior determinants gives D_S^{−1/2}, and the constant comes out as (2b₀)^{a₀} Γ(ν) / (π^{n/2} Γ(a₀)).
   - C3 confirms the Lemma 4 closed forms against this formula to 1e-13.

   The only open question is whether this is the m(S) of 00_COMMON. Positivity itself would hold for any proper marginal likelihood, so the risk sits mainly in (ii)(c)–(d).

2. **Location:** §5.1, "Input conditions and standardisation".
   **Severity:** gap.
   **Claim:** The step "‖x_j‖² = 41 = n−1, so every sample SD equals 1 … standardisation returns X and y unchanged" assumes 00_COMMON standardises with the n−1 denominator. That convention is not in the packet.
   **Evidence:**
   - C3: with the n−1 denominator every SD is 1. With the n denominator the SD of y is 0.98802, so standardisation would rescale X and y by √(42/41).
   - Rescaled data would give G_S = 42I, H_S = 1807I and G_S + I = 43I. Then t_i, D and the per-variable factor (D_S^{−1/2} per variable) all change, and Lemma 4 as written would be false.
   - I recomputed the witness under that convention (60 digits, not certified): a_c(1) = 0.92708057, a_c(2) = 0.57234528, 1+χ² = 1.5338714, β−α = 0.0120823, ρ(0,½) = 0.97078743, ρ(½,1) = 0.91366114.
   - Every required inequality still holds, so this is plausibly fixable. But the proof as written depends on the convention.

3. **Location:** §5.1 ("The method's blocks are a deterministic function of X alone (METHODOLOGY §6.3), each of size at most B = min(⌊√42⌋, ⌊√40⌋, 16) = 6"); proof of Lemma 4 ("Σ_b |S ∩ C_b| = |S|, and each j_i ∈ S lies in exactly one block"); proof of Lemma 1 ("|U| ≤ B ≤ K").
   **Severity:** gap.
   **Claim:** The proof uses three properties of the method's block construction that the packet does not contain. STATEMENT.md says only "blocks C₁, …, C_J".
   - (a) The blocks depend on X only, not on y. This is needed so j₂ can be chosen after the blocks are fixed and before y is defined.
   - (b) The blocks partition [p]. This is needed for γ₀(S) = ϖ(S) n^{−|S|/2} ∏_{i∈I(S)} g_i: a variable outside every block would drop out of γ₀ and change d.
   - (c) Block size is capped at B = min(⌊√n⌋, ⌊√p⌋, 16). This is needed for a j₂ outside j₁'s block to exist.

   **Evidence:** I checked by hand that the product over blocks gives Lemma 4's γ₀ and d for any partition separating j₁ and j₂. So the closed forms hold once (a)–(c) hold, and the proof's "pick j₂ outside the block of j₁" then suffices without exhibiting the blocks. If (a) failed, for example through screening or ordering that depends on y, the choice of j₂ would be circular and would need a different argument.

4. **Location:** §5.1, "SMC branch" and "Budget".
   **Severity:** gap (low risk).
   **Claim:** The formulas N₀ = max(2500, n, p), H₀ = ⌈512·2500/2500⌉, ℓ = ⌈log₂(n+p+1)⌉ and T₀ = max(1000, ℓ²), and the constants in the exact-branch condition, come from 00_COMMON §2 and cannot be checked in the packet. The H₀ expression as printed (2500/2500) does not show which of the two 2500s is N₀.
   **Evidence:** The arithmetic is correct (C5). The conclusions do not depend on the exact formulas: the left side of the branch condition is 7.50e11 against 5.02e5, and the witnesses only need T_e ≥ 2. Any plausible variant gives the same result, but the formulas remain unchecked.

5. **Location:** §5.2 "Grid" and §5.3 "Grid" ("any implementation as in STATEMENT §0").
   **Severity:** exposition.
   **Claim:** The witness definition asks for "a fixed deterministic implementation". The proof shows that every implementation following the §0 rules outputs the stated grid, but it neither names one nor notes that one exists.
   **Evidence:** Existence is immediate (for example, midpoint bisection that appends the largest passing midpoint). In both witnesses ρ_V(u, b) ≥ 0.90 at every pilot step, so no bisection, endpoint choice or stopping rule ever applies. The "any implementation" claim is therefore correct.

6. **Location:** §4, (ii)(b): "the output grid is 0 followed by the appended points in order".
   **Severity:** exposition.
   **Claim:** STATEMENT §0 does not define the output grid in terms of the appended points; the proof adopts this reading without saying so. Separately, the parenthetical in (ii)(b) about "the frozen grid of a calibration" is covered only by the general claim, which presupposes that the frozen grid is such an output.
   **Evidence:** This is the only reading consistent with "Start at u = 0 … continue from the appended point" and with 0 = φ₀ < … < φ_T = 1. Under it, the acceptance argument is correct. The statement's "in particular" makes the general claim enough for the parenthetical.

7. **Location:** §5.1, "Numerical values and their certification".
   **Severity:** exposition.
   **Claim:**
   - (a) "Every strict or non-strict inequality used in §§5.2–5.3 is decided by comparing interval endpoints … seven checks" overstates what the checks cover. Several inequalities are not among the seven: t₁ + t₂ < 1 is an exact Fraction `assert` (and a hand computation); |V_c| ≤ 800, |V_d| ≤ 800, 1 ≤ T_e, 2 ≤ T_e and the branch inequality are integer facts; P > 0 and R > 0 follow analytically. All of them are correct.
   - (b) The displayed values re^D ≈ 0.0615463326 and re^{2D} ≈ 0.718509685 fall under the proof's definition of "≈" (certified enclosure within one unit of the last digit), but the script prints no enclosure for them.

   **Evidence:** C2 gives re^D = 0.06154633259855 and re^{2D} = 0.718509684822948, which match the displays. Neither value is used in any inequality.

8. **Location:** §5.2 (Z_c/P ≈ 0.984162996) and §5.3 (α = A/P ≈ 0.984162996).
   **Severity:** exposition.
   **Claim:** Two distinct quantities have identical displayed values, which may confuse a reader.
   **Evidence:** Z_c − A = ϖ(1)n^{−1/2}(38 + g₂) + 38ϖ(2)n^{−1}g₂ > 0 is of the order of ϖ(0), while P is about g₁σ(1) with g₁ ≈ 6.70e22. The two ratios therefore differ by about 5e-22. The printed enclosures ([…023762, …023763] and […023757, …023758]) are disjoint and consistent with this. There is no error.

9. **Location:** Proof of Lemma 1, parenthetical "(U ⊆ C_b, |U| ≤ B ≤ K for n ≥ 3, so U ∈ Ω)".
   **Severity:** exposition.
   **Claim:** B and C_b are used before they are defined (B first appears in §5.1), and the step is not needed. As written, the m(S) formula gives m(U) ∈ (0, ∞) for every U ⊆ [p], whatever |U| is.
   **Evidence:** H_U and G_U + I are positive definite for every U. Given the B formula, B ≤ K is in any case correct for n ≥ 3: ⌊√n⌋ ≤ ⌊n/2⌋ when n ≥ 3, and ⌊√p⌋ ≤ p.

**What would change the verdict:** confirming findings 1–4 against 00_COMMON §1–2 and METHODOLOGY §6.3. That means confirming:
- the m(S) formula with a₀ = b₀ = 0.01;
- standardisation with the n−1 SD;
- blocks that depend on X only, partition [p], and are capped at B = min(⌊√n⌋, ⌊√p⌋, 16);
- the budget and branch formulas.

Either quote these definitions verbatim in the proof or packet, or have a reviewer with access to the sources confirm them. With that done, every part of the statement, including the method-class witnesses in (ii)(c)–(d), would be established.

Verdict: not verified
