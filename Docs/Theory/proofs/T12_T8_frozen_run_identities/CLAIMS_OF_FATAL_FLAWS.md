# CLAIMS_OF_FATAL_FLAWS — T12 (T8)

Every fatal or gap finding, copied verbatim, with the lead's answer. Stage A (Astra #1 on PROOF_v2) had no fatal or gap findings, only 3 exposition findings, all fixed in PROOF_v3. The entries below are from Stage B round 1 on PROOF_v3. The fixes are in PROOF_v4 and STATEMENT v2.2.

---

## Claim 1 (Astra #2, finding 1, gap)

> **Location:** §8.2, `PROOF_v3.tex` lines 185–214; §8.5, lines 227–231; Appendix A, `helpers/p2_exact.py` lines 58–84.
>
> **Severity:** gap.
>
> **Claim:** The computational examples are not sufficiently linked to the marginal likelihood specified in the theorem.
>
> **Evidence:** The helper's `log_bf` function asserts that it computes the v3 target's Bayes factors. It uses \(a_0=b_0=0.01\), \(H=(n+1)X_S^\top X_S+I\), a determinant ratio involving \(X_S^\top X_S+I\), and exponent \(a_0+n/2\). None of the permitted documents supplies the target formula or derives these expressions from it. `STATEMENT.md` refers to `00_COMMON §1`, whose contents are not supplied in the permitted materials, and says that only positivity of \(m\) and \(\varpi\) is used.
>
> Positivity alone does not determine these Bayes factors or the numerical conclusions. In particular, the finite-state enumeration and saved intervals establish results for the scores implemented by `log_bf`; they do not establish that those scores equal the theorem's \(m(S)/m(\emptyset)\). Consequently, the bias bounds in **(iv.b)** and the instance-specific diagnostic conclusions in **(iv.e)** remain unverified against the stated target. This is not evidence that the implemented formula is false; its required identification is unsupported here.

## Claim 2 (Opus xhigh reviewer, G1, gap). Same issue as Claim 1, found independently.

> **G1**
> - **Location:** §8.2, "The instance" and the interval-computation paragraph; §8.5; `helpers/p2_exact.py`, `log_bf` (lines 58–84) and `setup` (line 98).
> - **Severity:** gap.
> - **Claim:** The (iv.b) bias bounds (−0.17 and −0.15) and the (iv.e) result E[Ẑ_r·PIP̂_{r1} | F] ≠ Z·PIP₁ depend on the exact formula for m(S), on a₀ = b₀ = 0.01, and on the prior weights w(k). None of these is stated or justified in the proof or in STATEMENT.md, so I cannot verify that the computation is about the v3 target.
> - **Evidence:**
>   - The formula exists only in code, as log BF(S) = −½ log(det H / det(G+I)) − ν[log(2b₀ + yᵀy − n zᵀH⁻¹z) − log(2b₀ + yᵀy)], with H = (n+1)G + I and ν = a₀ + n/2. Its only justification is the comment "for the v3 target".
>   - STATEMENT §0 defers the formula to 00_COMMON §1, which is not in the packet. It also says "only m > 0 and ϖ > 0 are used", which is not true for this instance.
>   - The prior values w(0) = ½, w(1) = w(2) = 1/6, W_K = 1 match the standard BB(1,2) beta-binomial (I recomputed them), but that definition is also not in the packet.
>   - The margins are small: at the method column, 0.0040 for the primary bound and 0.0097 for the secondary.
>   - A diagnostic only: with ν = a₀ + (n−1)/2 the bounds still hold (primary −0.179106, secondary −0.164769, D = 7.7534). So the conclusion may well survive, but I could not verify the formula itself.
>   - The qualitative (iv.e) facts (P(F) > 0, E[Ẑ_r | F] < Z, E[Ẑ | F] < Z) need only D > 4/√3 and a < ½. Both of those numbers come from the same unverified formula.

**Lead's answer to Claims 1–2: accepted and fixed.** The finding is right. STATEMENT.md delegated the target formulas to a file outside the packet, and its remark "only m > 0 and ϖ > 0 are used" was false for the instance. Fixes:
1. STATEMENT §0 (v2.2) now writes out the fixed v3 target, copied from METHODOLOGY_v3 §5 and 00_COMMON §1: H_S, D_S, Q_S, m(S) with C_n, BF(S) = D_S^{−1/2}[(2b₀+Q_S)/(2b₀+yᵀy)]^{−ν}, ν = a₀ + n/2, a₀ = b₀ = 0.01, w(k) = B(1+k, 2p−k)/B(1,p) = ½/C(2p−1,k), W_K. The positivity remark is restricted to everything except the instance. This adds no assumption and changes no conclusion: these are Felipe's fixed target, which the statement always referred to.
2. PROOF_v4 §8.2 has a new paragraph, "The scores". It derives the 1×1 and 2×2 expressions that `log_bf` computes from the STATEMENT §0 formula (C_n cancels; explicit 2×2 determinant and inverse; ν = 10.01), states that `standardise` implements the §0 standardisation, and computes the prior values from w(k) = ½/C(3,k).
3. The certificate was re-run after cosmetic helper changes (E6), with no change to any value. It now prints exact endpoint comparisons (CHECK lines), and its output is reproduced in a new Appendix B.

## Claim 3 (Opus xhigh reviewer, G2, gap, minor)

> **G2**
> - **Location:** §6, the paragraph after Lemma 6.1 ("the joint measurability of Φ is part of the stream model").
> - **Severity:** gap (minor).
> - **Claim:** The proof assumes Φ is jointly measurable in (c, u). STATEMENT.md does not state this; EX-S, CAL and Success only say that Φ(c, ·) realises I(c).
> - **Evidence:** Two steps need it. Lemma 6.1 is applied to g(Φ(c,u₁),…,Φ(c,u₄))·1_𝒜(c), which must be measurable on E×Υ. The (iv.c) characterisation needs c ↦ law of I(c) to be a probability kernel. The assumption is standard and true for any algorithmic implementation, but it is imported rather than given.

**Lead's answer: accepted and fixed.** STATEMENT (v2.2) now says explicitly, under EX-S, that the stream model includes joint measurability of (c, u) ↦ Φ(c, u) with values in a Polish space; PROOF_v4 §6 cites it. This states what EX-S ("independent ideal uniform streams") already presupposes, since the island record is produced from uniform streams by finitely many measurable operations. It restricts no input and changes no conclusion.

---

## Exposition findings (not fatal/gap; recorded for completeness)

- Astra #2 finding 2 = Opus E1 (broken \ref, log not in appendix): fixed. The reference is repaired and the log is reproduced in Appendix B.
- Opus E2 (ε_U temperature): fixed. Lemma 1.4(a) now defines the temperature-free ε_S = π₀(S)e^{−R_d}, valid for every φ ∈ [0, 1].
- Opus E3 ((iv.c) implicit step): fixed. Added the explicit sentence: the hypotheses admit a calibration law with mass on (grid, N) and (grid, 4N); the (iv.b) instance has a unique maximiser of d; no claim is made about the actual calibration procedure.
- Opus E4 ("only the averaged form"): fixed. STATEMENT (iv.d) now gives an exact remark instead of "only … in general random". PROOF_v4 §8.4 proves that Z_tq_t(1{S}) = m(∅)γ₀(S)e^{φ_t d(S)} is non-constant when φ_t takes two values.
- Opus E5 (block/graph facts rely on method rules): the proof now cites the STATEMENT appendix, where these facts are recorded.
- Opus E6 (helper cosmetics): fixed. Endpoint display, the prior comment and the `__main__` block are corrected; the certificate was re-run with identical values (certify_iv.log; previous log kept as helpers/certify_iv_v1.log).
- Opus, (iv.e) "extension from r = 1 to every r by exchangeability is implicit": made explicit in §8.5.

## Rulings by the Stage B reviewers (round 2, on PROOF_v4 / STATEMENT v2.2)

- **Astra #2** (review/A2_call2_stageB_r2_ruling_REPLY.md): agrees with the answers to Claims 1, 2 and 3; each fix works. No remaining fatal or gap findings. Two exposition items: (a) the log displayed rounded endpoints, so the width claim was not visible; (b) the Appendix B description wrongly called the log row condF_Elog "divided by Z₀". **Verdict: verified.**
- **Opus xhigh** (review/OPUS_stageB_r2_ruling.md): agrees with all three answers; each fix works, checked term by term and numerically. Two exposition items: X1, certify_iv_v1.log was not in its packet (packaging; the file is in the project's helpers/); X2, an unneeded remark about the method's max-abs scaling. **Verdict: verified.**
- Lead: all four exposition items were fixed in PROOF_v5 (exposition only, no mathematical change from the verified v4). The certificate now prints an exact width CHECK (max width 1.92·10⁻⁵³ < 10⁻⁵²); the Appendix B row descriptions are corrected; the X2 remark is removed. No dispute remains, so the Astra judge was not needed.
