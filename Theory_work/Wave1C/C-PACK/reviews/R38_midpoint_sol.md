# R38 — independent midpoint mathematical review

**Decision: CONTINUE.** The scoped mathematical programme is viable. I found no counterexample to UM, UM-FP, I2, SL0–SL2, or the corrected SEL/L8 arguments. EX-A is expressly retained; the native-binary64 claim is confined to the start-mode identification step. The four findings below are local completeness/proof-presentation repairs, not reasons to redirect the research or invoke a mathematical stop rule. This is not a final acceptance or an item-5 fidelity certificate.

Reviewer: Codex gpt-6.1-sol, xhigh; fresh independent review, 2026-11-08. Paths below are relative to the repository; `CP` means `Theory_work/Wave1C/C-PACK/`, `W1` means `Theory_work/Wave1/`, and `SoP` means `Theory_work/State_of_Project/sections/`.

## Numbered findings

1. **MINOR — CP/patches/P_e4_consumers.md:7,19,31: make the premise patch match the sources and amend the method definitions.**

   The replacement string at lines 19–21 exists in GEN's STATEMENT but does not exist in `W1/W1-GEN/lemmas/00_MAIN.md:10`, which actually says `e4 [N3 OPEN]`. GEN STATEMENT:28 also continues to define the start by the size-then-lex rule. PXN STATEMENT:33 retains its old exact-mode/tie definition with an appended annotation. The mathematical distinction matters on tied, truncated instances: e4′ specifies the coded output and intentionally does not prove the prescribed lex choice. M5's unquoted explanatory text at SoP/04_theory.tex:505,515 would likewise retain stale N3/e4 wording. The positive proofs remain valid, but the patches are not yet a complete, internally consistent premise replacement.

   **Exact fix text:** add the following instructions to P-e4:

   > In `W1/W1-GEN/lemmas/00_MAIN.md:10`, replace `e4 [N3 OPEN]` by `e4′ (C-PACK I1 §4)`.
   > In `W1/W1-GEN/STATEMENT.md:28`, replace `start mode S̃₀ = argmax_Ω γ₀ with the size-then-lex tie rule` by `coded start centre S̃₀ := start_mode(st, cap).S under e4′ (C-PACK I1 §4); on {π₀(S*) > 1/2}, Lemma UM identifies it with S*`.
   > In `W1/W1-PXN/STATEMENT.md:33`, replace `centred at the exact start mode S̃₀ = argmax π₀ (max-plus convolution of block tables, deterministic tie rule)` by `centred at S̃₀ := start_mode(st, cap).S under e4′ (C-PACK I1 §4); on {π₀(S°) > 1/2}, Lemma UM identifies it with S°`.
   > In the unquoted explanatory prose of `SoP/04_theory.tex:505,515`, replace the requirement for the prescribed e4/N3 centre by `the emitted coded centre under e4′ (C-PACK I1 §4), identified with S° on {π₀(S°) > 1/2} by Lemma UM; EX-A and LS0 integration remain premises`. Preserve the verbatim historical status rows, including N3 “OPEN”, and identify this as a C-PACK addendum.

   These instructions supplement, rather than remove, P-e4's retained EX-A, H1, H3–H4, OP-LS0 and complete-scan contracts.

2. **MINOR — CP/patches/P_GEN_LHiid.md:18: the broad dependency-list edit leaves explicit candidate-condition sentences behind.**

   `W1/W1-GEN/STATEMENT.md:129–131` is a claim paragraph, not merely a dependency list. Replacing the two input names does not specify what happens to its final sentence, `Conditional on the candidate inputs; labelled so.` L6:4–5 likewise expressly says `conditional on`. Since the deliverable requests exact replacement patches, provide complete replacements for these two locations.

   **Exact fix text:** replace the instruction for GEN STATEMENT:129–131 by:

   > Replace the whole (C5)(b) paragraph by: “(b) *LH-iid* in the common family of W1-PXN STATEMENT §1 and L6(b), with eventual SIZE, 18 ≤ p_n ≤ n^A, p_n → ∞, and fixed A ≥ 1: (C4) applies on the X-event constructed in L6(b). Partition recovery and the correlation bound are supplied by repaired W1-PXN Theorem R (or R′) and Lemma CR/[CONC′], as proved in C-PACK Lemma I2. Blocks and start objects have I2's exact-branch convention. The separate verifications of (H1), (H2), and all other components of the X-event, with their common constants and deterministic envelopes, are retained. Neither candidate Theorem B nor [CONC] is an additional assumed input; all other method and implementation premises remain.”

   > In the L6(b) header at L6_instances.md:4–5, retain `PROVED (by this seat, unchecked)` and replace `conditional on W7-PART Theorem B (candidate) and [CONC]` by `using repaired W1-PXN Theorem R (or R′) and Lemma CR/[CONC′] via C-PACK Lemma I2, with GEN's remaining hypotheses unchanged`.

   The untouched Wave1 authorship/check statuses must not be upgraded by applying this dependency repair.

3. **MINOR — CP/lemmas/I4_SL_corollaries.md:98,101: make SL2's standalone proof valid without an implicit convergence premise.**

   SL1 explicitly assumes r_n → 0, whereas SL2 restates only δ_n = O_P(r_n). Its proof then concludes `2Eδ_n → 0`. That inference requires δ_n →_P 0 and does not follow from a positive rate sequence alone. The intended applications have a vanishing rate, so none is refuted. In fact, SL2's first conclusion needs no posterior-concentration assumption: when δ_n ≥ 1/2 the alleged error threshold 2δ_n is at least one. This observation repairs the proof without strengthening the hypotheses.

   **Exact fix text:** replace SL2's proof at lines 100–101 by:

   > On O ∩ {S₀ ∈ S⁺} ∩ {δ_n < 1/2}, retention gives S₀ ∈ T, and M4(b) with SL0(i) gives max_j |PIP^T_j − 1{j ∈ S₀}| ≤ 2δ_n. If δ_n ≥ 1/2, that inequality holds automatically because every coordinate error is at most one. Consequently
   > P(O ∩ {max_j |PIP^T_j − 1{j ∈ S₀}| > 2δ_n}) ≤ P(O ∩ {S₀ ∉ S⁺}) → 0.
   > For deterministic t_n > 0 with r_n = o(t_n), add P(2δ_n > t_n) → 0, since δ_n/t_n = O_P(r_n/t_n) = o_P(1). ∎

4. **MINOR — CP/SONG_LIANG_MAP.md:7: record the paper's standing lower growth assumption.**

   The inspected article, §2.1, journal p. 950, assumes P_n/n^θ → ∞ for some θ > 0. The map lists the priors and upper-growth differences but omits this standing condition. This is relevant because I2 deliberately permits much slower growth. It does not invalidate our results, but T4.a calls for inspected hypotheses and important domain differences.

   **Exact fix text:** append to the introductory Song–Liang setting paragraph:

   > “For the correctly specified asymptotics, §2.1 (journal p. 950) also assumes P_n/n^θ → ∞ for some θ > 0. Our LH-iid results impose p_n → ∞ and p_n ≤ n^A with no positive-power lower growth bound. These are different domains; the map does not identify the two sets of assumptions. The fixed-subset result in row 10 is recorded separately.”

## Item-by-item determination

| Target | Independent determination |
|---|---|
| T1.a | Substantively satisfied. I1 distinguishes definitions, deductions, move ties, output ties and off-event uses. GEN (C6)'s use of global maximality is explicitly retained through N3(a); the optional T38 data-dependent-centre sketch is excluded. PXN's off-event coded-centre transfer is expressly repaired. Apply finding 1 to finish the source-level replacement. |
| T1.b | Proved. N = 1 ≤ cap gives UM directly from N3(c); N3(a) is an independent immediate route. π₀(R) > 1/2 implies uniqueness. No false truncation flag is needed. |
| T1.c | Proved conditionally. N3(e) gives membership in argmax ĝ; the strict gap inequality transfers uniqueness. The stored-table and evaluation errors are distinguished, capped table domains are specified, and every γ_k index is required to satisfy ku < 1. No fixed-precision asymptotic guarantee follows or is claimed. |
| T1.d | Correct mathematical replacement with EX-A preserved. H1, H3–H4, deterministic measurable centre/cap, hypothetical exact-branch objects, emitted centre, scans and guards remain. Integration stays open. The shortened patch texts must incorporate full I1 §4 rather than be read as complete standalone contracts; finding 1 supplies missing source edits. |
| T2 | Proved in the common domain, retaining GEN's remaining hypotheses. The family is the same raw-coefficient LH-iid family, not GEN's broader heterogeneous exact-Gram LH family. Eventual SIZE with actual B_n implies 9 ≤ g ≤ 16 asymptotically. I2's exact-branch convention handles arbitrarily slow p growth. Apply finding 2 to make the advertised dependency change unambiguous. |
| T3 | The supplied SEL/L8 patch mathematics checks out against L6/L8. Dedicated-review identity, historical numerical counts and independent repair re-checks are asserted in the supplied patches, not independently certified here: the requested blind-review restrictions exclude their review records. This review must not be used as proof that those procedural requirements occurred. |
| T4.a | Main-article map is materially accurate, subject to finding 4. It distinguishes Hellinger contraction, screening, exact MAP, algorithmic output, misspecification and costs. Supplement hypotheses remain NOT INSPECTED; see accessibility note below. |
| T4.b | SL0, SL1 and SL1′ are correct under the named source hypotheses. SL2 is correct; finding 3 makes its proof self-contained. Reported-HPM claims stay joint with output. Fixed-list logarithmic stacking, larger-list polynomial stacking, islandwise weighted PIPs and store-restricted PIPs remain distinct. No shipped pooled-R′=4 consistency theorem is manufactured. |

## Specific proof stress checks

**PXN centre transfer.** I1 §1.1's abstract example is valid: with p = 2, K = 1, singleton scores 1 and λ = (−10,0), the singletons are tied global modes, each with mass below 1/2, and cap = 1 chooses different sets after reversing block order. This refutes unordered-partition transfer of a coded centre, not UM or a D0-data consistency theorem. The replacement bound

P(C₀ ≠ S°) ≤ P(A_nᶜ) + P(π̃₀(S°) ≤ 1/2)

is correct under EX-A and the retained execution/encoding contracts. Mathematical π₀/tables/aggregation transfer survives reordering; the coded centre is identified only on the uniqueness event. Later PXN search and output steps use the actual centre through that event, so no off-event centre identity is needed.

**UM-FP.** Checked the frozen `v3_start.h:54–69,183–239` against I1 and N3's LFP proof. Monotonicity of rounded addition is sufficient for the DP value/membership claim, although not for lexicographic completeness. The summation bound handles signed summands and gradual underflow; the first addition from zero is exact, leaving at most m rounded additions. The gap proof uses both η and ε and a strict inequality. These facts do not validate scoring, search ordering or other full-method computations in native binary64.

**I2 and GEN.** Rechecked R_branch_repair §1–3 and CR_corr_tails directly. The independent strict-margin route gives recovery without the defective A0(c) statement. CR's union bound gives 3n^−2, and the symmetric row-sum bound gives L′_n δ_n = O((log n)^(3/2)/sqrt(n)) → 0. Principal-submatrix eigenvalue floors and the fixed-signal SLLN then establish C_n. L6(b)'s other events are still needed: SEP, leakage tails/average and VIS are not consequences of I2 alone. Their fixed-family Beta/moment arguments and the final intersection preserve GEN's common envelopes. No conditional Beta law given partition recovery is used.

**SEL after patching.** The deterministic family T₀(l), rather than the selected block family, supports the fixed-pair Beta moment calculation. The localization in P-SEL.1 is essential and sufficient: domination holds on F_n, while the moment bound for B_n^leak is unconditional. The exceptional-event term must remain. Replacing both square-root and squared concentration errors by the log n versions retains ω_n → 0 and the n^−1/8 Markov factor. Fixed c > 0 and the 14-coordinate embedding are correctly restored. No finite-n guarantee is established.

**L8 after patching.** The Schur-complement floor, projection cancellation and reverse triangle inequality prove the certificate. The admissible η range allows some sufficiently small ε₀, not arbitrary preassigned ε₀ and κ; P-L8.1 makes this explicit. The W coefficient is θ(1 + ε_n/3), since the nine-variable equicorrelation matrix at 1/4 maps the all-ones cross-covariance vector ε_n 1 to (ε_n/3)1. This preserves the disjoint-support split; θe_j does not. The reported four-column warning concerns the unqualified implication, not a counterexample to the corrected certificate or GEN.

**Posterior and reported summaries.** SL0 follows from concentrating all discrepancy off S₀; it remains trivial with δ = 1 when S₀ is infeasible. The two-point swap is a legitimate arbitrary-law sharpness example, and is correctly separated from a positive D0 posterior. SL1 does not infer an expectation rate from O_P. GEN's additional posterior-rate instance uses every-sequence tightness transfer with common events/envelopes; mere pointwise conditional convergence would not suffice. SL1′ proves sensitivity only for J_n(c). M1(i)'s quoted status and the two stacking configurations match SoP/04_theory.tex:111,115–117,130. M4(b),(c) and their quoted status fragments match :397–401,410–412. I found no substantive status upgrade in those comparisons.

**New independent numerical checks in this review.** Standard-library Python, seed 3808: 280 laws on capped subset spaces with p = 1,…,7, 10,160 truth/law pairs (including infeasible truths and zero masses), and 3,169 truth-containing stores; integer cross-multiplication found no violation of SL0's two PIP bounds, unique-mode retention or the sharper stored-posterior error bound. A separate Python transcription of the frozen max-plus/backtracking algorithm tested 2,000 abstract binary64 instances, p ≤ 8, shuffled block order, K including zero, caps 1/2/10^6, and score scales 2^−50,…,2^50: 1,888 had a unique rounded maximum, with zero value/membership/unique-mode violations. This is a transcription test, not compiled-C++ validation, scorer-error validation, or a replication of the SEL/L8 numerical campaigns. Direct evaluation also reproduces the L8 warning: A = 1, η = 0.1 gives η/2 + sqrt(2η(A+ε₀)) = 0.68246 at ε₀ = 1, but 0.49744 at ε₀ = 0.001.

## Source limits and finish plan

I read the ten requested ticket files and the cited mathematical/code sources used above, including the supplied Song–Liang article. I did not read LOG.md, REPORT files, existing reviews or dispositions. Consequently ticket-level report quotations, council scores and historical review/numerics metadata are not independently authenticated here; no contrary status is inferred. Source-level N3, CR, repaired R, T03♯, M1, M4, M5 and registry qualifications remain intact. The historical onset disclosure in I4 §4 must not be read as a universal T03♯ onset over its entire design class; SoP :787 explicitly disclaims such a universal onset.

The [publisher article](https://academic.oup.com/jrsssb/article/77/5/947/7040600) identifies supplementary file `rssb12095-sup-0001-Supinfo`. Attempts to fetch the publisher supplementary section and the Wiley supplementary-PDF endpoint failed (publisher redirect inaccessible; direct article request HTTP 403; Wiley PDF inaccessible). I did not obtain the supplement. Its exact Theorem S statement and hypotheses remain **NOT INSPECTED**, as the locked target permits; only the main article's MAP-consistency description is compared.

The remaining work is viable: apply the local fixes, conduct the independent item-5 fidelity comparison against the complete authorized baseline, finish the citation/status check, sweep the resulting full patch set and consolidated text, then run council on that final version. The fidelity reviewer must have access to the baseline REPORT/repair history required by T5; this restricted midpoint review does not replace that check. Preserve the distinction between council-passed Wave1 baseline material and C-PACK's new addenda, and keep all integration, output-event and arithmetic qualifications visible. A re-check of the changed passages is sufficient before the planned final sweep; no research redirection is indicated.

**CONTINUE — FATAL 0 / MAJOR 0 / MINOR 4 / NIT 0.**
