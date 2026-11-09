# R39 — exhaustive sweep of the current C-PACK deliverable

Reviewer: Codex gpt-6.1-sol. Read-only source audit; only this report is written. No git commands or git state changes. Line numbers refer to the current files read in this review. `CP/` = `Theory_work/Wave1C/C-PACK/`; `C/` = `CP/item5_PXN_consolidated/`; `W1/` = `Theory_work/Wave1/`; `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`; `CODE/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.

The findings below concern the current text, including errors inherited faithfully from the baseline. An earlier favourable fidelity verdict does not establish the correctness of an inherited claim. Findings are grouped by root defect, with affected repetitions identified rather than counted again.

1. **MAJOR — `C/03_start.md:110`: the added finite-n centring rate is false in the permitted slow-p domain.** Also recorded as an applied addition at `C/APPLIED_ERRATA.md:44`.

   The sentence says the finite-n centring error is `log π₀(S°) + o(1), which is O_P(√(log n/n))`. The unquantified `o(1)` cannot be absorbed into that rate. In fact, the prior-ratio calculation at :101 has a deterministic correction

   `d_p := log[w(s+c)/w(s)] + c log p − Σ_{i=1}^c log((s+i)/2)
        = Σ_{i=1}^c log[2p/(2p−s−i)]
        = [cs+c(c+1)/2]/(2p) + O(p^−2).`

   This is positive and of order 1/p. For example, take c=1, v=0, g=9 and an eventually admissible sequence `p_n=9 max{9,ceil(log₂ log₂ n)}`. SIZE holds eventually and p→∞, but `1/p_n` is much larger than `sqrt(log n/n)`. The singleton expansion also has a stochastic O_P(1/n) remainder relative to `(n−1)r̂²/2`; it does not remove d_p. Thus the displayed rate, unlike the limit law itself, is not valid on the theorem's full domain. R36 explicitly traced this sentence to the earlier Opus council remark; inheritance does not repair it.

   **Exact fix text:** replace :110 by:

   > On partition recovery, put `V_n := (n−1)Σ_i r̂²_{j_{b_i},y}` and `d_p := Σ_{i=1}^c log[2p/(2p−s−i)] = O(1/p)`. The exact singleton expansion gives `Mstat_n = Σ_i log((s+i)/2) + V_n/2 + log π₀(S°) + d_p + O_P(1/n)`. Consequently its remainder relative to this finite-n statistic is `O_P(√(log n/n) + 1/p)`. All terms beyond `V_n/2` vanish, which suffices for the stated limit law; no rate of convergence to the limiting chi-square law is asserted.

   Replace `C/APPLIED_ERRATA.md:44` by:

   > The baseline council's finite-n centring remark is included with the additional O(1/p) prior correction; its asserted O_P(√(log n/n)) remainder alone does not hold for arbitrarily slowly growing p (R39 finding 1).

2. **MINOR — `CP/patches/P_GEN_LHiid.md:29-31`: the REPORT edits leave candidate-conditioning language in place.**

   Item 4c treats all destinations as dependency lists and asks to drop two input names. But `W1/W1-GEN/REPORT.md:22` says `(conditional on the candidate W7-PART Theorem B)`, and :65 says `**conditional on W7-PART Theorem B (candidate)** and [CONC]`. Removing/replacing the names alone leaves a conditional claim or malformed prose. R38 repaired the analogous STATEMENT and L6-header sentences, but these REPORT sentences remain unresolved in the executable patch instructions. The literal input names at REPORT:22 and :98 also differ from the quoted strings in item 4c.

   **Exact fix text:** append to item 4c:

   > In `W1/W1-GEN/REPORT.md:22`, replace `(conditional on the candidate W7-PART Theorem B)` by `(using repaired W1-PXN Theorem R and Lemma CR/[CONC′] via C-PACK Lemma I2, with GEN's remaining hypotheses retained)`. In REPORT:65 replace `**conditional on W7-PART Theorem B (candidate)** and [CONC]` by `using repaired W1-PXN Theorem R and Lemma CR/[CONC′] via C-PACK Lemma I2; GEN's other hypotheses are unchanged`. In REPORT:98 replace `W7-PART Theorem B for LH-iid` by `the repaired partition-recovery and correlation inputs of C-PACK Lemma I2 for LH-iid`. Preserve historical review verdicts and label these as C-PACK dependency addenda.

3. **MINOR — `CP/patches/P_e4_consumers.md:24-25`: the replacement Note (0) contradicts the retained all-data integration requirement.**

   `Premise e4′ is used only on {π₀(S*) > ½}` is false for the full e4′ premise. The centre-identification argument is localized to that event, but e4′(iii)'s deterministic emitted centre and OP-LS0 contracts are used for the structural closure on all potential output runs. I1 correctly makes this distinction at `CP/lemmas/I1_e4_replacement.md:32,42-47,144-147`. Replacing GEN's note by the proposed sentence loses that distinction and conflicts with the adjacent closure argument at `W1/W1-GEN/lemmas/L5_assembly.md:11-16`.

   **Exact fix text:** replace the proposed Note (0) in patch item 7 by:

   > The mathematical centre-identification part of e4′ is used on `{π₀(S*) > ½}` (L2 step 9), where Lemma UM identifies the coded centre with S*. The all-data deterministic-centre, emitted-centre, OP-LS0, guard and complete-scan contracts remain in force for the closure argument, including outside that event. Their implementation remains an obligation for C-ENG.

4. **MINOR — `C/00_statement_and_conventions.md:26-27`: the n=200 SIZE specialization omits a condition on p.**

   `at n = 200 it means 8 ≤ g ≤ 14` is true when `floor(sqrt p)≥14`, hence p≥196. The allowed finite-n domain includes smaller p. For instance, n=200, p=18, g=3 gives B=4 and satisfies `g≤B<2g`, contrary to the stated specialization. The asymptotic 9≤g≤16 conclusion is correct. The same unqualified finite-n remark occurs in the quoted source family at `NBH/branch_snapshots/API-PXNGAP/PROOF.md:52-53`, cited in I2; it should not be propagated as a general domain fact.

   **Exact fix text:** replace the parenthesis at :27 by:

   > (at n=200 and p≥196, B_n=14 and SIZE means 8≤g≤14; for smaller p use B_n=min(14,floor(sqrt p)))

   Use the same p qualification wherever the finite-n source remark is restated. The statement's asymptotic SIZE domain needs no change.

5. **MINOR — `C/00_statement_and_conventions.md:13-21,94,106`: the every-n theorem needs its finite-input domain stated explicitly.**

   The family describes groups 1 through 2c+v but states only G_n=p_n/g and p≥18. It does not explicitly require G_n≥2c+v. Nor does it explicitly carry D0's n≥3/nonconstant-input domain into its every-n formulation. The asymptotic condition p→∞ supplies enough groups eventually, but does not make an initially undefined truth/design meaningful at every n. The cited D0 source does specify n≥3 (`Theory_work/State_of_Project/sections/04_theory.tex:70`), while the consolidated theorem presents its setting as self-contained. This is a missing standing domain qualification, not a need to strengthen the asymptotic theorem.

   **Exact fix text:** append to the Design paragraph:

   > The sequence is indexed only by admissible sample sizes n≥3 with integer G_n≥2c+v, so all named signal groups exist. Standardization is on the probability-one event of nonconstant columns and response. Every-n assertions below mean every such admissible n; changing or omitting a finite initial segment has no effect on the asymptotic conclusions.

6. **MINOR — `C/03_start.md:51-52`: “each term explicit” overstates what the displayed citations establish.**

   The event union bound is explicit, and CR, E and Tr-J give numerical bounds for several terms. But `P(ℰ♯_nᶜ)` also contains the sample signal-energy and coefficient-scale failures. `C/02_design_events.md:34-35` proves their vanishing by SLLN only and supplies no explicit finite-n tail bounds. Thus the claim that each term is explicit is unsupported. The exact constants of the event and the asymptotic proof are otherwise sufficient; no finite-n rate for these remaining terms is needed.

   **Exact fix text:** replace the parenthesis beginning `each term explicit` by:

   > (the partition, correlation, Lemma E and Tr-J contributions have the displayed explicit bounds; the remaining finitely many signal-energy and sample-scale contributions vanish by Lemma 2.2's SLLN argument)

7. **MINOR — `C/02_design_events.md:81`: the numerical source artifact is absent.**

   The text cites `W7-PART/results/union_bound.txt`. There is no such file in `NBH/branch_snapshots/W7-PART/results/`, and a search under Theory_work found no `union_bound*` artifact. The numerical values can be reproduced from the displayed formulas, so the absent artifact is unnecessary. Direct evaluation gives t*=0.6096117967977923, I*=0.012587152788782677 and K_200,500=1128102.9509839164. Those agree with the rounded numbers in the proof. The separate Monte Carlo claim in :82 is a report attribution, not an independently available numerical result in that missing file.

   **Exact fix text:** replace :81 through the first clause of :82 by:

   > With ρ=0.7 and ψ̄=0.5, direct substitution in the displayed formulas gives t*=0.6096117968 and I*=0.0125871528. At (n,p)=(200,500), K_n=1.128102951×10⁶, hence the bound is vacuous.

   Retain the Monte Carlo sentence only as an explicitly attributed historical W7 report claim, with a source containing that claim; do not imply that the missing results artifact was inspected.

8. **MINOR — `C/05_posterior_output.md:57`: the exact-enumeration implementation citation has no unambiguous base and is wrong for the requested frozen core.** Also `C/03_start.md:127` and `C/04_search.md:136` use bare header names without a local path alias.

   `core/cpp/v3_core.cpp:504-524` does describe enumeration in `Scripts/SMC_BVS/`, but not in the frozen `CODE/` core: CODE:504-518 concerns inherited HPM provenance/output assembly and :523-524 only begins the exact-branch section. The frozen enumeration invocation is at :558. The explicit `Scripts/SMC_BVS/...:447` pointer in Part 0 is accurate for that other copy; it must not silently establish a base for bare `core/` citations in another file. Correcting the pointers changes no mathematics.

   **Exact fix text:** define `CODE/` in Part 0 as above, and use these full aliases:

   > In Part 3, cite `CODE/cpp/v3_start.h:183-240`. In Part 4, cite `CODE/cpp/v3_engine.h:400-420`. In Part 5's exact-branch paragraph, cite `CODE/cpp/v3_core.cpp:523-558`. If retaining the alternative source-copy locations, write their full `Scripts/SMC_BVS/core/...` paths explicitly and label them as that copy.

9. **MINOR — `CP/reviews/CITECHECK.txt:14,16-32` and `CP/numerics/citecheck.py:15-17`: the final citation ledger is stale and does not cover item 5.**

   The saved summary has 122 successful citation references and 13 quote flags. Running the current checker function without its write entry point yields 129 references, 14 flags, and changed source-line numbers (e.g. SONG_LIANG_MAP:18 rather than :15). Its FILES list excludes all seven consolidated proof files and their manifests, despite the whole-deliverable scope. Furthermore, its bare-STATEMENT resolution for P-e4 resolves CP's STATEMENT rather than PXN's; the existing manual disposition acknowledges that false context resolution. Existence of a numbered line is not confirmation that a citation supports a claim. Thus `0 unresolved misses` should not be presented as a current complete-deliverable certificate.

   **Exact fix text:** add this qualification at the head of the ledger until regeneration:

   > Historical partial citation-check snapshot, preceding the latest R38 edits. This output is not a current whole-deliverable certificate: item5_PXN_consolidated is excluded from the checker. The current pre-item5 automated scan finds 129 citation references and 14 quote flags; manual dispositions must be matched to the current source lines. Semantic support and status fidelity require manual checking.

   Then extend FILES to include the seven item-5 proof files plus INDEX/MAP/APPLIED_ERRATA/OPEN_QUESTIONS, add their source aliases/context maps, resolve P-e4's PXN and GEN sections separately, regenerate the output, and replace the historical dispositions with current path:line dispositions. Preserve the distinction between generated range-existence checks and manual semantic checks.

10. **NIT — `C/INDEX.md:33`: the review-status sentence contradicts the appended R36 record at :41-42.**

    `The consolidated text itself has not been reviewed` is now false as an unqualified present-tense statement. R36 reviewed it and all six proposed fixes are recorded as applied. This is stale metadata, not a reason to upgrade the supplement to a new council-passed status.

    **Exact fix text:** replace the final sentence of :33 by:

    > The consolidation subsequently received the R36 fidelity review recorded below; that review is distinct from the baseline theorem's council pass and does not constitute a council pass of C-PACK's new addenda.

## Audit boundary and non-findings

I inspected the locked target, method requirements, map, three lemmas, four patch files, the seven consolidated proof files and manifests, the saved numerical outputs, and the citation checker. Source comparisons included PXN STATEMENT/FINAL_PROOF/REPORT/ERRATA and its replacement lemmas; GEN's statement, centre/assembly/search/counterexample/instance/certificate sources and report; N3's hypotheses, clauses (a)/(c)/(e), floating-point proof and frozen start code; N1's reported premises and Corollary E; the relevant SoP cards and method rules; T22's external statement, T03♯'s external statement, W6 T38 statements/proof, W2 replay lemma, W7's algorithm and tail derivation, and W3-PXN's population calculations and heuristic. I read the supplied Song–Liang main article directly using pdftotext, including the theorem/condition pages and §6. The supplement's exact Theorem S remains NOT INSPECTED, as explicitly permitted by the locked target; this review does not upgrade it. The missing W7 numerical artifact is finding 7.

The main arguments checked here do not supply a counterexample to UM, UM-FP, I2, repaired SEL/L8, SL0–SL2, or the headline PXN theorem. In particular: the indicator-localized SEL Markov bound retains its exceptional event; L8's ε₀/κ range and W coefficient are correct; SL2 handles δ≥1/2 without an unstated convergence argument; and the coded-centre off-event transfer repair is sound. Item 5 deliberately presents the older mathematical centre convention and identifies I1 as a separate addendum in INDEX:43-45; that separation is not itself a status upgrade or an unacknowledged incorporation. The quoted N3 OPEN and registry W7 GAP statuses are historical source statuses and should remain so. Numerical tests are finite evidence, not proofs of the asymptotic conclusions.

This is a mathematical/source sweep, not a certification that every historical numerical campaign was rerun or that all transitive archive references were re-reviewed. Existing outputs were inspected; the citation checker was evaluated in memory, without overwriting CITECHECK.txt. No changed code or production integration was tested or claimed.

Counts: **FATAL 0 / MAJOR 1 / MINOR 8 / NIT 1** (10 findings).

Overall assessment: **REVISE — the core theorem route survives, but the false slow-p centring rate and the identified patch/citation/domain defects should be repaired before final acceptance.**
