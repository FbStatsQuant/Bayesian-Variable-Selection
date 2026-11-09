# R07 — Exhaustive sweep review

**Verdict: REVISE.** I found no fatal defect in the intended compound-symmetry argument, but the written hypotheses need one substantive repair and the frontier contains an incorrect blanket claim. The remaining findings concern scope, intermediate wording, citations, notation, and the accuracy of numerical evidence. This is not an approval of the current text.

Paths below are relative to `Theory_work/Wave2/W2-FAC-B/`, unless a full repository path is given. Each numbered finding is counted once, including findings with multiple affected locations.

## Findings

### 1. MAJOR — The stated sampling model never identifies θ* with the raw-model coefficients

**Location:** `STATEMENT.md:42-44`; first consequential use: `lemmas/L1_cs_reduction.md:25-27`.

**What is wrong:** G specifies the actual mean through X^rβ, but introduces μ := Xθ* without stating μ = CX^rβ or θ* = D_xβ. L1 then assumes Y := Cy^r = μ + e. That identity does not follow from the displayed hypotheses. The distinction matters because the noise variance and fixed coefficients used throughout the proof are on the scale before response standardisation.

Taken literally, the stated assumptions allow β = 0 and an unrelated, nonzero θ*. For p = s₀ = 1, fixed positive ρ, and θ* = 1, all the displayed CS/P/θ/FS conditions hold, but the response is pure noise. The asserted nonempty start and posterior truth then need not be recovered; indeed the empty model is favoured asymptotically. This is a missing model identification, not an objection to the intended result.

**Fix:** Define the column-scale matrix D_x and write X = CX^rD_x⁻¹, θ* := D_xβ, μ := CX^rβ = Xθ*, and Y = μ + Cε before defining y = Y/s. The corresponding definition already appears in `Theory_work/Wave1/W1-GEN/STATEMENT.md:29-30`.

### 2. MAJOR — p > n/2 alone does not force a size-saturated start

**Location:** `STATEMENT.md:23-25`, `STATEMENT.md:123-124`; `METHOD_REQUIREMENTS.md:9-12`.

**What is wrong:** These passages present “p > n/2: size-saturated start” as a general mechanism. N2 establishes saturation for one particular data set. Neither p > K nor FS by itself establishes the blanket assertion, even asymptotically.

The ticket's own N₀ mechanism gives an obstruction to that assertion. Take p = K + 1, s₀ = 1, and a partition whose truth-containing block has 16 members. Then |N₀| = 15 and |S*| = p − 15 = K − 14. The positive/zero block-increment argument of L2 still applies to the unconstrained start with p of order n and makes S* its unique mode with probability tending to one. Since S* is feasible under the cap K, it is also the constrained mode, which is not saturated. The condition p > n/2 does not remove the possibility that p − |N₀| < K.

**Fix:** State saturation as the observation in N2, with its layout and N₀ information. Any general asymptotic saturation claim needs additional hypotheses, at least addressing the unconstrained mode's size relative to K, and a proof. The existing single-data-set cap failure remains valid evidence.

### 3. MINOR — “Every partition of size ≤ 16” is too broad for the finite-n delivery assertion

**Location:** `STATEMENT.md:45-46`, `STATEMENT.md:115-122`; `lemmas/L5_assembly.md:52-58`.

**What is wrong:** The arbitrary-partition argument is valid for the asymptotic statistical part once K = p. The finite-n delivery proof instead inherits the actual method's feasibility and construction invariants. A partition with blocks of size ≤ 16 need not satisfy |C_b| ≤ K on a finite prefix allowed by the eventual condition (P). For example, n = 3, p = 2 permits a two-member block under the stated arbitrary-partition rule, but K = 1. Its full block table includes an infeasible model. The actual method avoids this through B ≤ K.

L5 verifies the new class's raw-data and scorer inputs; it does not establish Proposition F's entire implementation/resource contract for arbitrary replacements of the partition routine.

**Fix:** Limit the arbitrary-partition assertion to the statistical claims at indices where K = p. State C4 for the specified method's partition, or separately require cap-feasible blocks and the inherited construction/resource premises for an alternative partition.

### 4. MINOR — Reaching S₀ does not by itself imply certified termination there

**Location:** `STATEMENT.md:52-53`.

**What is wrong:** The general explanation says that a path which reaches S₀ after d moves ends at S₀ certified whenever a ≥ d. That conclusion also requires S₀ to have no improving neighbour. Otherwise the search can continue past S₀ or return an improving neighbour with local_limit. The scoring assertion a ≥ d − 1 is correct.

L4 eventually proves the missing terminal property, so this does not defeat C2 or L5.

**Fix:** Replace “reaches S₀ after d moves” with “terminates at S₀ after d moves,” or explicitly add the no-improving-neighbour condition to the certification clause.

### 5. MINOR — The redundant b ≤ 0 subcase contains a false description of the retained set

**Location:** `lemmas/L4_path.md:128-129`.

**What is wrong:** The parenthetical “all kept above x lie in (b, 0]” does not follow from b ≤ 0. Here b is the smallest retained coordinate above x, not an upper bound on that side. Positive retained coordinates can lie above b; in fact the interval-hole property retains all positive nulls when the hole has negative endpoints.

The preceding inequality at line 126 already gives b ≥ (1 − 3ε_b)H > 0 under the hypothesised last-lower-point deletion. Thus the extra subcase is unnecessary. Its final magnitude inequality can also be justified using b > x ≥ −ε_bH; the parenthetical is the error.

**Fix:** Delete the redundant b ≤ 0 sentence, or replace its parenthetical and explicitly use b > x ≥ −ε_bH.

### 6. MINOR — The small-regime summary states incorrect asymptotic orders

**Location:** `STATEMENT.md:130-133`, especially line 132.

**What is wrong:** “Null statistics O(log p) + O(L_n) ≪ log n” does not describe the proof.

First, the uniform squared-null bound includes O(L_n²), because E1 permits the common factor/offset and the finitely many exceptional coordinates to have magnitude O(L_n). Second, for p near n^{1/200}, log p is a fixed positive fraction of log n, not o(log n). L4.2 correctly uses a sufficiently small fixed coefficient, obtaining τ² ≤ 0.1 log n; it does not prove uniform little-o behaviour in this entire regime.

**Fix:** Use “O(log(p + 1) + L_n²), bounded by a sufficiently small fixed multiple of log n for n ≥ n₀.” State the uniform onset as applying at indices satisfying p ≤ ⌊n/2⌋; an arbitrarily delayed finite prefix before (P) holds cannot have a sequence-independent onset.

### 7. MINOR — The cited CAP lemma does not state the full small-cap range claimed here

**Location:** `STATEMENT.md:109`; `lemmas/L4_path.md:208`.

**What is wrong:** The ticket claims the deterministic prefix/scoring conclusions for any cap a ≥ m₀ − 1, and cites CAP(a) for caps ≥ m₀. The cited integration lemma formally assumes ℓ_n ≤ a ≤ a′: `Theory_work/Wave1C/FINAL/sections/s7_impl.tex:36,46-48`. The asserted ranges can include caps below ℓ_n, particularly for bounded p or m₀ = 0. The loop argument does extend to such caps, but that extension is not the statement being cited. Also, a cap must be a nonnegative integer; the literal inequality a ≥ m₀ − 1 alone allows a = −1 when m₀ = 0.

**Fix:** Specify nonnegative integer caps and derive the single-search prefix property directly from CAP's structural rule (L3), which works for every such cap. Keep the integration/monotonicity theorem within its recorded domain. L5's use with a_n ≥ ℓ_n is already within that domain.

### 8. MINOR — L2 repeats the superseded universal N1 full-start description

**Location:** `lemmas/L2_start.md:7-8`.

**What is wrong:** The parenthetical says N1 has S̃₀ = [p] for S5/F1/F2 at n ≥ 10⁶ when no block holds all truths. N1 contains the contrary cases already acknowledged by the locked statement: F2, p = 200, c = 0.5, n = 10⁶ has start size 193 in all five runs; S5, p = 400, c = 0.5 has size 396–397 in all three runs. Their truths are not all in one block.

**Fix:** Match the qualified wording in `STATEMENT.md:17-21`: full in most sampled cases at 10⁶, with exceptions, and full in all sampled cases at 10⁸. This is an evidence-description correction, not an asymptotic counterexample to L2.

### 9. MINOR — The self-test cited as path agreement compares only endpoint and length

**Location:** `lemmas/L1_cs_reduction.md:4-6`; `numerics/cs_selftest.py:20-25`.

**What is wrong:** L1 reports agreement of the closed-form and general scanner's paths in 4/4 cases. The script's “same” test is only equality of the final model and the number of moves. Despite the comment about reconstructing paths, it neither reconstructs nor compares the intermediate centres or ordered moves. Equal endpoint and length do not establish equal paths.

**Fix:** Describe the existing output as endpoint-and-move-count agreement, or compare the full ordered centre/move sequences and regenerate the diagnostic. No proof conclusion should depend on this test.

### 10. MINOR — N2 conflates the final scanned centre with the returned improving neighbour

**Location:** `numerics/N2_summary.md:9-11`, used by `STATEMENT.md:24-25` and `METHOD_REQUIREMENTS.md:11-12`.

**What is wrong:** After 19 swaps and 292 deletions, scan centre C₃₁₁ has four extras. Under the specified cap rule, its complete final scan scores the improving next deletion C₃₁₂, with three extras, and returns that neighbour with local_limit. CAP's structural rule explicitly distinguishes the move-count centre from the returned neighbour: `Theory_work/Wave1C/FINAL/sections/s7_impl.tex:40`.

Thus “stops (local_limit) at a set with 4 extras” is inaccurate if it describes the returned search model. The main conclusion that S₀ is not scored is unaffected: that scan reaches no model smaller than s₀ + 3.

**Fix:** State that the last scanned centre has four extras and its best scored/returned neighbour has three, while S₀ remains unscored.

### 11. MINOR — N3's reported maximum NA margin does not match its raw data

**Location:** `numerics/N3_summary.md:83-84`, cited by `lemmas/L4_path.md:4-6`.

**What is wrong:** “NA margin max −0.13 log n over all runs” is not the recorded maximum. Reading the 468 raw records gives max_add_gain_over_logn = −0.013627166707809698 over all runs, and −0.2370872426548659 over the runs with n ≥ 10⁵. Neither interpretation produces −0.13. The all-run interpretation also makes the purported bound false.

**Fix:** Specify the population of runs and report the corresponding value, with suitable rounding. The counts of 468 data sets, 10 path violations, and zero such violations at n ≥ 10⁵ do agree with the raw records.

### 12. MINOR — N5 advertises a numerical centre comparison it does not perform

**Location:** `numerics/n5_invariants.py:1-4,37,58-60`; related descriptions: `lemmas/L3_event.md:4-5`, `lemmas/L4_path.md:7-8`.

**What is wrong:** The driver says the exact centre is cross-checked against the scan centre. Its centre_err field instead records whether the chosen deletion index equals the closest null to the formula-derived centre, assigning 0 or 1. It never computes a numerical difference between that centre and the scanner's centre. Agreement of one argmin does not establish equality of centres.

The L4 warning that this is exploratory and does not test m₁ or the proof constants is correct and should remain.

**Fix:** Rename/document centre_err as a closest-deletion disagreement indicator, or actually reconstruct the z-unit scan centre, transform it to ξ units, and record the numerical discrepancy.

### 13. MINOR — N1's “moves − symdiff” is not generally the number of non-deletion moves

**Location:** `numerics/N1_summary.md:3`; underlying definition: `numerics/n1_run.py:41-44`.

**What is wrong:** The summary equates moves minus the initial symmetric difference with “extra (non-deletion) moves.” A swap can fix two membership errors at once, and a necessary truth addition is a non-deletion without being an extra move. The statistic can consequently be negative; the summary itself records −1, for example in the F10.3, p = 200, c = 1, n = 400 row. It is not a generic non-deletion count.

This does not invalidate the separately recorded swap/addition/deletion counts or the observed pure backward paths from the sampled full starts.

**Fix:** Label the statistic literally as move count minus initial symmetric difference. Use the actual move-type counts to describe swaps and additions.

### 14. EDITORIAL — κ₀ changes meaning between the reduction and the path proof

**Location:** `lemmas/L1_cs_reduction.md:36`; `lemmas/L4_path.md:24,31,181`.

**What is wrong:** κ₀ denotes the data-dependent common component of z in L1, but denotes the deterministic limit (1 − ρ)/ρ of κ_n in L4. Meanwhile L4 imports κ₁ from L1 and introduces λ_θ in place of L1's λ₁/κ₁. The formulas are locally recoverable, but the same κ₀ symbol denotes incompatible quantities across a dependency boundary.

**Fix:** Rename L1's common z component or call the limiting shrinkage parameter κ_∞. Explicitly identify λ_θ = λ₁/κ₁. The η/ε_bal separation and the distinction between H and H̄ are otherwise consistent in the proof.

### 15. EDITORIAL — ϑ is declared as an ordered vector but then indexed by arbitrary original column labels

**Location:** `STATEMENT.md:68-74`; corresponding uses in `lemmas/L2_start.md:27-33`.

**What is wrong:** The fixed vector ϑ has coordinates 1,…,s₀ by the “in increasing index order” definition, while ϑ_l and Σ_{i∈V}ϑ_i are subsequently written for original labels l and V ⊆ S₀(n). Those labels can exceed s₀. The intended rank-to-support identification is clear but unstated, and matters when support positions vary with n.

**Fix:** Define the ordered support map i_r(n) and ϑ_{i_r(n)} := ϑ_r, or formulate FS over subsets of {1,…,s₀} and explicitly map them to support positions. This preserves the fixed finite collection of FS constants used in L2.

### 16. EDITORIAL — C1's deterministic-looking consequence needs its event qualifier

**Location:** `STATEMENT.md:96-97`.

**What is wrong:** After the probability limit, “So S̃₀ = S* …” is written as an unconditional equality. L2 proves it on E_n^S for n ≥ n₀, hence with probability tending to one, not on every data set. The finite-n misses in N4 reinforce the distinction.

**Fix:** Write “On this event, S̃₀ = S* …,” or append “with probability tending to one” to the displayed consequences.

### 17. EDITORIAL — The “not claimed” section contradicts C4's explicit finite-n claim

**Location:** `STATEMENT.md:137`, versus `STATEMENT.md:119`.

**What is wrong:** “Finite-n statements” are categorically excluded, although C4 expressly claims P(no output) = 0 for every admissible n ≥ 3 under Proposition F's premises and allocation.

**Fix:** Exclude finite-n statistical discovery/recovery bounds, while retaining the explicitly stated finite-n ideal-machine delivery guarantee.

## Checks that did not produce an additional finding

I checked the score algebra and both prior ratios, the sign conjugation, the Gaussian sufficient-statistic representation, the common-centre deletion/addition/swap identities, the Q-versus-RSS inequalities, and the multiplier bounds. I found no incorrect constant in these steps under the intended sampling model.

The FS condition is sufficient for the nonzero block increments, including U = ∅; the zero pairs are confined to one deterministic truth-complete block. The proof uses arbitrary deterministic partitions asymptotically, not a favourable linkage outcome. Positive-pair gains dominate the global size penalty uniformly for p ≤ n/2, while zero-pair additions are penalised.

I checked E1–E7, including the conditional sign argument for all Top(j), the dyadic E4 union, the constants in the E6 quantile bound, and the E7 grid argument. No union over exponentially many retained sets is needed. After the parameter-dependent onset, the growing regime uniformly has m₀ > m₁, H² ≥ (log n)/100, δ_e = O(L_n/H), and m₁δ_e = O(L_n²/√log n). The small regime is handled independently by L4.2.

For the growing-regime path, the bulk imbalance recursion, the adaptive threshold-set reduction to Top(J), the bound J ≤ 5m, the Young inequalities and the bulk gain margins check out. The end-phase argument uses H̄ for its deterministic envelopes, not H; E1 also places N₀ inside that envelope eventually. The centre offset must change sign in the reflected argument, as the text now states. The majority-side deletion argument controls imbalance without accumulating an error over the path.

The uniform end-phase errors can be taken of order O(L_n√log n + H̄²|ε′| + L_n) = o(log n), with a uniform ε′ → 0 from the multiplier bounds. In the bulk, γ = O(1/L_n) and the multiplier/log-expansion errors are uniformly negligible relative to log n. Thus I found no additional failure of uniformity along the path or for bounded, divergent, or oscillating sequences p_n ≤ n/2. This does not make the inaccurate small-regime summary in finding 6 correct.

The truth-loss bound, negative truth-out swaps, positive best null deletion, and comparison against null-out swaps are consistent. The proof correctly avoids a negative-log-n assertion for swap gains themselves. Its probability-one nondegeneracy exclusions are nontrivial Gaussian linear equalities for fixed 0 < ρ < 1. No theorem uniform in ρ approaching 0 or 1, growing sparsity, or vanishing fixed coefficients has been established or claimed.

For the actual cap a_n, the extra complete scan, emitted centre, all-scored retention, lexicographic neighbour ties, size-then-lex HPM ties, and exact-branch convention are consistent with the cited method. The legacy-cap non-discovery condition m₀ ≥ ℓ_n + 2 has the correct off-by-one threshold. Certified LS0 termination is correctly distinguished from the public flag of the reported HPM.

L5 verifies the normalised and unnormalised eigenvalue hypotheses at all required anchored sizes; the cutoff m_n♯ need not have a new upper-size bound here. It obtains an expectation limit by boundedness, not an expectation rate from O_P. The CAL-bearing M5 route and the CAL-free pathwise delivery route are kept separate. The latter uses discovery directly and does not reverse the operational-closure inequality.

The quoted dependency statuses match the permitted sources: M5-0 is “PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))”; S-T is “PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)”; [OP] remains “PROVED (by this seat, unchecked)”; CAP is “PROVED (by this seat)” with its recorded council check; A2 is “PROVED (A2), checked by A3.” The A4 “OK-WITH-FIXES” preflight qualification is kept separate from the earlier council approval. The delivery extension retains Proposition F's exact-real/unit-cost, resource, implementation-premise and code-reading-audit qualifications. I did not treat any of these recorded statuses as independent approval of the new FAC-CS extension.

The numerical records were inspected as diagnostics, not used as proofs. N4's 66/72 matching unique starts, the locations of its six misses, N3's 468/10 counts, and N6's 72 runs agree with the records. N6's note that the two non-pure runs check only the prefix before their first swap is material and is already disclosed.

**Counts: fatal 0; major 2; minor 11; editorial 4. Total: 17 findings.**

