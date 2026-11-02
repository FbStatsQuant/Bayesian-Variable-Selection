# W5-VPGD: Verify and complete the asymptotic repair theorem (W3-PGD Theorem W), and check PGD on the study's designs

**Paper role:** Thm 3(iii), the asymptotic clause of the repair theorem (refined T37(iii)). W3-PGD proved Theorem W
in `PROOF.md` but left `REPORT.md` as a stub, and no referee has read it.

Fetch and read: `origin/theory/W3-PGD` (PROOF.md in full, PLAN.md, scripts, results), `origin/theory/W1-T37R`
(PROOF: Lemma 0, Lemma 2, Lemma 3, Theorem A, Theorem B, Theorem C and the PGD/LD definitions; Exp 3),
`origin/theory/W3-VT37R` (REPORT §4.3 EXP3-R; REPAIRS R4, R5), `origin/theory/W1-T03R` (PROOF §4: SE_λ, SE_w),
`origin/theory/W4-T38FULL` (`T38_PROOF.md` §3.4 Prop. LH-LAT, for consistency). Also 00_COMMON and
`Scripts/Data_generators/` (reimplement S1–S6 in Python; R is not available).

Goals, in order:
1. **Referee Theorem W and its lemmas** line by line: Lemma 1.1–1.3, Prop P1 (GERC + TRC ⇒ PGD; the five
   non-progress move types), Prop P2 (block iff criteria (B1)–(B3)) and Cor P2′ (equicorrelated formula), Prop P3
   (TRC sufficient conditions), Prop P4 (sharpness), Lemma P5/Cor P6 (stability, random designs; the cited
   Bickel–Levina bound), Lemma Q/R/G/U (noise side; the score representation with the ridge; the pair geometry
   ‖r_A − r_B‖² ≤ C₁g), Lemma LD and Lemma S ((α), (β), (γ) under (H1)/(H2)/(H3)), Theorem W, Cor W′, Prop C-LD.
   Record VERIFIED / GAP / ERROR per step; repair what you can.
2. **The constant in (★).** W3-PGD notes its threshold is off by a factor 3–4 from C-LD's 1/(2A). Sharpen (★) or
   show why the gap is intrinsic to the local/far decomposition.
3. **PGD on the study's population covariances.** For S1, S3, S4, S6 (block-orthogonal at population level, one
   truth per group of 5, the β pattern of `gen_dev_data.R`) compute η*(d) from Cor P2′ for d ∈ {1, 2, 3} and check
   it by direct enumeration of (B1)–(B3). For S2 (AR) and S5 (common factor), which are not block-orthogonal,
   evaluate GERC and TRC numerically on R_{2,2} at the population Gram and say whether PGD(η) holds for some η > 0.
   Then check the realised-design transfer (Cor P6) at n ∈ {200, 800, 3200}, p = 500: fraction of designs with
   PGD(η/2) on R_{2,2}(𝒟) for 𝒟 = nulls in the truth blocks, and the realised TD′_P(R_{2,2}(𝒟)) frequency.
4. **Consistency with Prop. LH-LAT.** On LH exact Gram, Theorem W's PGD(η) on Lat(S°) should be implied by
   POP-LAT(S°, m₀). Show the implication or the discrepancy.
5. **Write the missing REPORT** for W3-PGD's results in the protocol format (headline, statements, proofs cited by
   label, evidence, what fails, escalation, confidence card), so that Thm 3(iii) has a citable source.

Deliverable: `theory_campaign/W5-VPGD/REPORT.md` (verdict table + the completed report of Theorem W), `REPAIRS.md`,
scripts, results, confidence card. Numerics at p ≤ 30 exact where enumeration is needed (R_{2,2} has ≤ C(s₀,2)·p²
states).

---

_Source: theory_campaign/F-REFINE/NEXT_TASKS.md on branch theory/F-REFINE (Fable, 2026-11-02). Read F-REFINE's CARDS.md and ARCHITECTURE.md first: `git fetch origin theory/F-REFINE`._
