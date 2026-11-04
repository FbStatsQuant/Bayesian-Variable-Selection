# Statement check request — T01 and T02 (wave 3)

You are the statement checker and counterexample referee. Inputs (read only these):
- the proposed precise statement: `..\STATEMENT.md`;
- the original conjectures: `..\..\..\theorems\T01_A0_contrast_reduction.md` and `..\..\..\theorems\T02_A1_dimension_supersets.md` (ignore their "Proof-route hint" paragraphs);
- the shared definitions: `..\..\..\theorems\00_COMMON.md`;
- this change report.

## What changed, and why

No hypothesis was added or removed, and no conclusion was weakened. The lead claims every item below is either a renaming or the precise form of a clause the conjecture states informally.

1. **T01(iv), notation.** The second model is written S′ instead of R, because R also names the assumption bundle. Renaming only.
2. **T01(i), "joint transformed posterior".** Read as the image of the v3 working-model posterior of (S, β_S, σ²), evaluated at the standardised data, under (β_S, σ²) ↦ (s_yβ_S, s_y²σ²). The contrast data use any U with UᵀU = I, UUᵀ = C. The identity claims "posterior of the contrast model with rate b₀s_y²", meaning the fixed-rate contrast posterior Π_b evaluated at b = b₀s_y². The rate is data-dependent, which is why (ii) and (T) exist.
3. **T01(ii).** I_b(E), Z^c_b and Π_b are defined explicitly: the joint numerator integral over a parameter event E, with prior ϖ on Ω, its total, and their ratio. The original says "nonnegative joint numerator integrals I_b(E) over parameter events E". The inequality κ⁻¹I_{b₊}(E) ≤ I_b(E) ≤ κI_{b₋}(E) is stated as the "same domination".
4. **T01 "event of (iii)".** 𝓑_n = {σ*²/2 ≤ s_y² ≤ 2(σ*²+M)+1}, with b₋ = b₀σ*²/2, b₊ = b₀(2(σ*²+M)+1) and κ = (b₊/b₋)^{0.51}, all fixed constants.
5. **T01 transfer rule.** The original sentence is: "a target bound holds for v3 on the event of (iii) at multiplicative cost κ² only in the mixed-endpoint form (numerator sums at b₋, S₀-denominator at b₊); same-rate bounds alone do not establish it. Errors are never treated as Gaussian conditional on s_y." It is formalised as:
   - (T)(a), the positive content. On 𝓑_n, Π(E|y) ≤ κ²I_{b₋}(E)/Z^c_{b₊} ≤ κ²I_{b₋}(E)/(ϖ(S₀)m^c_{b₊}(S₀)). Hence a high-probability or O_P bound on the fixed-rate mixed quantity transfers to the v3 posterior at cost κ².
   - (T)(b), the negative content ("only … ; same-rate bounds alone do not establish it"), as stated in STATEMENT.md (revised version). On 𝓑_n itself, with s_y² fixed in the interior of the interval and p = 2, there are inputs where Π_{b₋}(E) → 0 but Π(E|y) → 1, and inputs where Π_{b₊}(E′) → 0 but Π(E′|y) → 1. So same-rate bounds at either endpoint do not establish bounds for v3.
   - The clause on Gaussian errors is recorded as a discipline on the proofs, not as a mathematical claim.

   Question for you: is (a)+(b) a faithful precise form, neither stronger nor weaker in substance than the informal sentence? If you think "only in the mixed-endpoint form" requires a different negative statement, say which.
6. **T02(i).** Θ_{n,m} is defined by the displayed equality. The content is then the tightness lim_{L→∞} limsup_n sup_m P₀(Θ_{n,m} > L) = 0, uniform in m with sup_m outside P₀, as the original writes it. m ranges over all deterministic integers. S₀ ∈ Ω is needed only for large n, which is part of R ("eventually s₀ ≤ K").
7. **T02(ii).** SE is read with m_n = m_n(½ log n), the definition fixed in 00_COMMON §1. "Π(S ⊋ S₀ | y)" is read as the π-mass of the strict supersets of S₀ in Ω.
8. **Setting.** α* is arbitrary, and P₀ is over ε only with the design fixed. These are as in 00_COMMON §1 (G).

## What to return

Write your full reply to `STATEMENT_CHECK_R1.md` in this folder (`review\`). If your tool cannot write files, return it inline.
1. For each item 1–8: **approved** or **rejected**, with your reason.
2. Any place where STATEMENT.md misstates the original conjectures or 00_COMMON (a definition, quantifier, constant or hypothesis). Quote both texts.
3. As counterexample referee: if you believe any part of the precise statement is false as written, give the counterexample. Otherwise say none.
4. An overall verdict: **approved** (STATEMENT.md may be used as is), or **changes required** (list them).

Do not write a proof. Read only the files listed. Run no commands, builds or jobs.
