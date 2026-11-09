# R06 — Independent exhaustive sweep of FAC-BCS-R

Reviewed against STATEMENT v2.2 on 2026-11-09. **Counts: 0 fatal / 1 major / 11 minor / 7 editorial (19 findings).**

The Tier 1 argument is repairable without strengthening its statistical hypotheses or proving KL. The one major finding is a missing restriction in the definition of its probability event. With the intended block-local restriction restored, I found no further substantive gap in the reduction, start-mode argument, move comparisons, posterior-hypothesis verification, or delivery assembly. Tier 2 is explicitly unclaimed; the absence of a checked KL proof is not a finding against Tier 1.

Locations below use current, one-based repository line numbers. Paths beginning `lemmas/` or `numerics/` are relative to `Theory_work/Wave2/W2-FAC-S5/`. I did not read LOG.md or any existing reviews directory. References in the proof to earlier local reviews were not used as mathematical evidence or independently verified as review-history claims.

## Findings

1. **MAJOR — E_S is missing its block-local quantifier; its high-probability assertion is false under the unrestricted reading.**

   **Location:** `lemmas/L3_event.md:14-15`, with the unsupported pair count at `:22-23` and the use of P(E_n) → 1 at `lemmas/L5_assembly.md:30`.

   E_S says “for every U ⊇ S₀ and l ∈ C_b ∖ U in the block C_b ⊇ S₀”; it never states U ⊆ C_b. The subsequent count of at most 2¹⁵·16 pairs requires precisely that restriction. Calling these “zero pairs” suggests the intended interpretation through L2, but does not make the displayed quantifier unambiguous.

   The distinction is substantive. Take singleton BCS groups, so Σ = ρ_b11ᵀ + (1−ρ_b)I, S₀ = {0}, a method block containing 0 and a null l, and p = ⌊n^{1/5}⌋. Positive truth coefficient satisfies FS-BCS. If U may range outside that method block, choose U to contain 0 and the ⌈log p⌉ other nulls with the largest idiosyncratic Gaussian coordinates, excluding l. Their mean is (1+o_P(1))√(2 log p). The ridge-standardised residual of l given U has magnitude (1+o_P(1))√(2 log p), whereas E_S's threshold is only 2√(20+log log n). Thus the unrestricted E_S has probability tending to zero, rather than one. This affects the event lemma as written, not the intended block-local start proof.

   **Fix:** Write `for every S₀ ⊆ U ⊆ C_b ∖ {l}, l ∈ C_b ∖ S₀, in the (unique, if any) block C_b ⊇ S₀`. With that restriction the existing Gaussian variance calculation and finite union bound apply.

2. **MINOR — The final addition-gain bound omits its small-argument condition.**

   **Location:** `lemmas/L1_bcs_reduction.md:92-93`.

   The elementary logarithmic upper bound is stated for x ≤ ν/2, but the concluding displayed G_add inequality is not qualified by that condition. It is not an unconditional bound on all data and T: as x/ν approaches 1, −ν log(1−x/ν) exceeds the displayed polynomial upper bound. The L4 application is valid because `lemmas/L4_path.md:41` establishes x = O(log n).

   **Fix:** Append `provided x := M_T(τ_l+ε_l)² ≤ ν/2` to the addition inequality, and explicitly invoke L4.2's x = O(log n) when using it.

3. **MINOR — A displayed determinant-remainder inequality drops n/(n−1).**

   **Location:** `lemmas/L1_bcs_reduction.md:73-74`.

   From k ≤ p ≤ n^α, the printed bound 2k/((n−1)d) is at most 2n^α/((n−1)d), not at most 2n^{α−1}/d. For example, n a fourth power and k = p = n^{1/4} makes the asserted comparison between these two bounds strictly false. The o(1) conclusion is unaffected.

   **Fix:** Keep `2n^α/((n−1)d)` or use `4n^{α−1}/d` for n ≥ 2.

4. **MINOR — The linear-p multiplier example uses ≍ where it needs ∼.**

   **Location:** `lemmas/L3_event.md:28`.

   “For p ≍ n/2 … M_[p] → 1” is false: comparability includes p ∼ n/4. For p/n → c ∈ (0,1/2], the full-model residual has n−1−p noise degrees of freedom, and the L1 formula gives M_[p] → 1/[2(1−c)] in probability. The limit is 1 only for c = 1/2. This is an illustrative aside, not a failure of the sublinear-p estimate used by L4.

   **Fix:** Replace `p ≍ n/2` by `p/n → 1/2`, or state the general limit above.

5. **MINOR — Proposition SHARP is cited for a stronger swap comparison than it proves.**

   **Location:** `lemmas/L4_path.md:81-84`.

   The sentence says an actual swap beating the best deletion is “proved … (FACA Prop SHARP)”. Copy-check: `Theory_work/Wave2/W2-FAC-A/lemmas/L6_sharp.md:12-13` asserts failure of NA on the full lattice; `:43-47` proves F(T ∪ {l}) > F(T) for an explicit addition witness. It does not compare a swap at T with the best deletion at T. Positive addition gain and swap dominance are different claims. This incorrect attribution does not enter L4.1–L4.5.

   **Fix:** Say only that SHARP proves failure of full-lattice NA above 1/6. If the stronger swap assertion is retained, supply a separate proof controlling the addition at T ∖ j for a best-deletion j.

6. **MINOR — The claimed 18-path, n ≥ 10⁶ gain-error bound has the wrong sample count.**

   **Location:** `lemmas/L1_bcs_reduction.md:11`; evidence `numerics/S3_summary.txt:1-18`.

   There are 18 rows in total, but rows 13–15 have n = 10⁴. Their errors are 0.01846, 0.03292, and 0.04279 times log n, exceeding 0.002 log n. Only 15 rows have n ≥ 10⁶; their maximum unrounded error in `s3b_out/` is 0.0017669394884135415 log n.

   **Fix:** State “along 15 deletion paths with n ≥ 10⁶; 18 paths total, including three n = 10⁴ runs with larger errors.” Do not assign the small error bound to all 18.

7. **MINOR — The leakage experiment does not validate the claimed two-term bound, and cancellation corrupts its reported rate diagnostic.**

   **Location:** `lemmas/L1_bcs_reduction.md:8`; `numerics/l1_leak.py:1-2,22-26`; `numerics/l1_leak_out.txt:1-3`.

   The script verifies an algebraic reconstruction of t̃ using ε, then prints n^{3/2} times only the signal-leakage component √(n−1)σ_j/(σ√ṽ). It does not calculate either a bound for that component or the two-term bound for total ε. The lemma's wording conflates scaled total ε with the unscaled signal component. Moreover, σ_j is computed by subtraction of order-one terms at line 22, although its size is O(n⁻²). At n = 10⁸ this produces the printed zero; at n = 10⁶ even the scaled value is inaccurate.

   I recomputed the leakage in memory using the proved stable identity σ_j = a⁻¹β̃ᵀϑ^R, keeping the same designs. The scaled values at n = 10⁴, 10⁶, 10⁸ are respectively 0.0074596655850334296, 0.007460034735914825, and 0.007460038428622267, versus the stored 0.007459705208301575, 0.007807795424064408, and 0.0. The symbolic identity in L1.4 itself is correct.

   **Fix:** Distinguish total ε from its signal component, compute the latter using a⁻¹β̃ᵀϑ^R (or higher precision), and actually output/assert the proposed bound ratios before claiming numerical verification of the bounds. Regenerate the cited output or narrow the claim to the reconstruction check it currently supports.

8. **MINOR — The identity experiment checks 361 instances, not 400.**

   **Location:** `lemmas/L1_bcs_reduction.md:5-7`; `numerics/l1_identities.py:6,13-14,23`.

   The loop makes 400 draws, but skips those with |T| < 2. Instrumenting the existing seeded script in memory gives 361 tested instances. Its reproduced maxima agree with `l1_identities_out.txt`; the numerical tolerance claim is supported. The present wording overstates the number actually tested, and the residual tests cover j ∈ T.

   **Fix:** Say “400 generated instances, 361 retained after the |T| ≥ 2 filter, testing every retained j ∈ T”, or generate until 400 instances have actually been checked. Include the tested count in the output.

9. **MINOR — The numerical path simulator does not implement the stated lexicographic tie rule.**

   **Location:** `numerics/s1_path.py:59-76`; `numerics/bcs_core.py:285-287`; specification `STATEMENT.md:94-96` and `Theory_work/State_of_Project/sections/02_method.tex:480-484`.

   `np.argmax(gdel)` selects the first, smallest outgoing index among tied deletion gains. For a fixed sorted T, the lexicographically smallest resulting deletion set instead removes the largest tied outgoing index. Swap ties likewise use array order, and ties across move types are resolved by deletion/addition/swap branch priority. Consequently “production local search” in `bcs_core.py:117` is not literally accurate on exact ties. This need not change the continuous random examples already stored, and the mathematical Π definition uses the correct rule.

   **Fix:** Form the resulting sorted index sets for all exactly tied maximisers and select their lexicographic minimum, including ties across move types. Use the same helper for the null-deletion path in `s3_cc.py:35`.

10. **MINOR — The data representation incorrectly absorbs the sampler's independent randomness.**

    **Location:** `STATEMENT.md:79-80`.

    “Every quantity the method computes is a function of (g,r) and the deterministic design/θ*” is false for the stochastic sampler: particles, proposals and Monte Carlo summaries also depend on its ideal uniforms. The sufficient-statistic representation is valid for scores, tables, start mode, deterministic LS0 and the data events used here. The proof's deterministic discovery step does not need the stronger assertion.

    **Fix:** Restrict the sentence to those deterministic statistical quantities, and say the full method is a function of these sufficient statistics together with the independent algorithmic uniforms/declared randomness.

11. **MINOR — The fixed response-scale envelope used in constants is not defined.**

    **Location:** `lemmas/L2_start.md:33,43`; `lemmas/L4_path.md:63`.

    Both c₁ = c_FS/(2s_max) and c₃ = ϑ_min²d/(4s_max²) use s_max without defining it in this ticket. L3(c1), `lemmas/L3_event.md:26`, supplies an upper bound but does not name a fixed s_max. Since truth group incidences can vary with n, θ*ᵀΣθ* need not itself be constant; the fixed envelope should be stated, not silently imported from the CS case.

    **Fix:** Set, for example, `s_max² := 2[(1+s₀)‖ϑ‖²+σ²]` and `s_min² := σ²/2` before L2.2. L3(c1) proves these bounds uniformly for large n. Then c₁ and c₃ are explicitly fixed positive constants.

12. **MINOR — S4's production-code provenance is overstated.**

    **Location:** `lemmas/L2_start.md:3-5`; `numerics/s4_start.py:1-5,22-23`.

    S4 is described as using “the method's coded partition and start-mode routine”. It imports the Python numerical replica `Theory_work/Wave2/W2-FAC-B/numerics/bvs_core.py`, whose own description at `:10-13` specifies DP/backtracking ties within 10⁻¹² and a separate complete-linkage implementation with correlation ties within 10⁻¹⁰. That is not a test executing the production start DP or its exact equality and partition rules. All 36 S4 output rows do support start = S* and n_optimal = 1 for the replica. The theorem's validity for arbitrary deterministic partitions also avoids any mathematical dependence on reproducing the production partition.

    **Fix:** Label S4 explicitly as testing the FACB Python numerical replica and disclose these tie conventions. Claim a production-code test only if the actual production routines are run and their results recorded.

13. **EDITORIAL — The displayed implementation-premise list is incomplete relative to the source it incorporates.**

    **Location:** `STATEMENT.md:52-55`.

    The text says the premises are named “exactly as FACB STATEMENT §1”, but its parenthetical leaves out IND-T and the extra c₄ search for R′ > 4. Those appear explicitly in `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:66-68`; M5's source also requires that extension (`Theory_work/State_of_Project/sections/04_theory.tex:478,487`). The broad incorporation by reference supplies them, so I do not treat this as an additional missing hypothesis in C3-R.

    **Fix:** Add “for R′ > 4, IND-T and the c₄ search” to the displayed list, or label that parenthetical non-exhaustive.

14. **EDITORIAL — G_n denotes three different objects across the proof.**

    **Location:** `STATEMENT.md:60`; `lemmas/L1_bcs_reduction.md:80`; `lemmas/L3_event.md:6`.

    It is respectively the number of BCS groups, the random maximum max_i|g_i|, and the deterministic threshold √(2 log(2p)+2L_n). L2 uses G_n in bounds obtained from E1, so the random-maximum/threshold collision is particularly easy to misread.

    **Fix:** Use, for example, J_n for the group count, G_n^obs for the random maximum, and G_n^bd for its deterministic envelope, with E1 saying G_n^obs ≤ G_n^bd.

15. **EDITORIAL — Several diagnostic/algebraic symbols are never defined locally.**

    **Location:** `lemmas/L1_bcs_reduction.md:64,67` (`quad_T`); `STATEMENT.md:26` (`H`, `κ_∞`).

    `quad_T` is inferable as z_TᵀH_T⁻¹z_T, but is used before any definition. H and κ_∞ in the near-end heuristic are not defined in the statement or lemmas. The numerical script uses H = √(2 log(2p)) (`numerics/s1_path.py:21`), while the formal condition uses H_q; these should not be silently interchanged. A CS κ constant is also not automatically a BCS end-stage constant.

    **Fix:** Define quad_T explicitly. Define the heuristic H and any intended κ_∞ with its model-specific justification, or replace that heuristic formula by the directly supported observation that the sampled maximum occurs at 2–5 retained nulls.

16. **EDITORIAL — The sufficiency sentence names the unobserved noise means instead of the observed group means.**

    **Location:** `lemmas/L1_bcs_reduction.md:45-46`.

    The sentence calls ȳ_g “sufficient for h”. These are the latent group noise means and are independent of h. The statistics sufficient for h from g_R are the observed group means m_g = h+ȳ_g, conditionally N(h,1/ω_g). The posterior formula on the following line already uses the correct m_g.

    **Fix:** State that, conditional on h, the observed group means m_g are independent N(h,1/ω_g) and are sufficient for h in g_R; then retain the existing posterior calculation.

17. **EDITORIAL — Empty-set conventions needed by the uniform identities are not recorded.**

    **Location:** `lemmas/L1_bcs_reduction.md:27-28,43-44,64-65`; `lemmas/L3_event.md:29`.

    L1.2(a) writes λ_min for every T ⊆ [p], including T = ∅; an empty matrix has no ordinary minimum eigenvalue. When R = ∅, the maximum over occupied group means in L1.3(i) is also empty. These cases occur for a one-truth terminal model and its truth deletion. STATEMENT defines e_∅ = h, and the intended extensions are straightforward, but the displayed all-set bounds need conventions.

    **Fix:** Restrict eigenvalue statements to nonempty T; define empty inverse products and quadratic forms as zero, det H_∅ = det(G_∅+I) = 1, and the maximum of these nonnegative absolute-value quantities over no occupied groups as zero. State the R = ∅ normal equation separately or under those conventions.

18. **EDITORIAL — “Measurable only on the enlarged space” is too categorical.**

    **Location:** `lemmas/L5_assembly.md:27-28`.

    The intended distinction is that E_n and CC_n need not be data-measurable. Positive conditional variance of h does not prove that every event involving h is non-data-measurable. For example, take p ∼ n^{2/5}, N₀ = ∅ and δ = 1/2: H_q² ∼ (4/5)log n exceeds (1−δ)Λ_p ∼ (1/2)log n, so CC_n is the empty, hence data-measurable, event for all sufficiently large n. The enlarged-space union-bound argument is nevertheless correct.

    **Fix:** Replace the categorical sentence by “E_n and CC_n are defined on the enlarged space and are not assumed to be data-measurable; in general CC_n is not data-measurable.”

19. **EDITORIAL — The self-test's docstring says every swap is compared, but only the best swap is compared.**

    **Location:** `numerics/bcs_selftest.py:1-2,38-45`.

    The code reduces both scanners' swap arrays to their maxima before comparison. Agreement of maxima does not test every individual swap value. L1's own description at `lemmas/L1_bcs_reduction.md:9-10` correctly says “the best exhaustive swap gain”; the inconsistency is in the cited script's documentation.

    **Fix:** Change the docstring to “every flip gain and the best exhaustive swap gain”, or compare the reference swap matrix against `Path.swap_pairs` for every outgoing/incoming pair and report the maximum pairwise error.

## Checks and limits of this review

- Read STATEMENT v2.2, L1–L5, the named numerical scripts and outputs, all 15 exhaustive-path JSON records, the 27 candidate-path records, and the 18 S3b records. Checked the cited FACB statement, reduction/start/event/assembly material, report and N1 summary; the direct SoP/FINAL setting, score, posterior, HPM and cap/delivery sources; GEN's [OP] statement; A2; and the additional A1/A4 and FAC-A SHARP sources needed to check their direct claims. Existing reviews and LOG.md were excluded throughout.
- Reproduced the L1 identity maxima and all five BCS-vs-general-scanner self-test outputs using Python 3.13. Instrumentation was in memory, with local bytecode writing disabled for the imported numerical modules. Independently recomputed the stable leakage diagnostic. No numerical or proof source file was changed.
- The 15 exhaustive records support pure null deletion to S₀ and the reported worst swap margin of −0.43610166910377085 log n. The 27 candidate-restricted records support their stated endpoints. The S3b maxima support the 0.05 bulk and 0.23 overall e-part ratios. All 36 S4 rows support their stated replica start-mode result. These are finite numerical checks, not a proof of KL.
- The imported M5(0), T03♯, [OP], CAP, FAC-CS and Proposition F/F-GROW statuses match the direct cited statement/report sources, with the preserved audit and post-council qualifications. I found no additional status upgrade. The enlarged-space probability bookkeeping in L5, the separate truth-removal argument, the inclusion of N₀ among outside nulls, the terminal index in CC, and the cap/last-scan argument are sound after finding 1's event-definition correction.
- This report creates only `reviews/R06_sweep_sol.md`; it does not amend the locked statement, the proof, the evidence, or the claimed Tier 2 status.
