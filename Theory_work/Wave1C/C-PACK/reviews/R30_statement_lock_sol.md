# C-PACK statement-lock review

Verdict: **LOCK-WITH-CHANGES**

Reviewer: Codex gpt-6.1-sol, high; statement review only. Reviewed on 2026-11-08 (local clock checked). Read both Wave protocols, C-PACK STATEMENT.md and PLAN.md, the four named Wave-1 tickets' STATEMENT.md and REPORT.md files, the relevant TH01/TH04/TH05/TH09 source text, and the I1/I2/I4 drafts and SONG_LIANG_MAP.md for well-posedness. No proof verification, numerical verification, or status promotion is supplied by this review.

The five-item organization is the correct target for HQ's brief. The sources support the intended exact-arithmetic uniqueness reduction, the proposed replacement of the two candidate inputs in GEN's LH-iid instance, the need for dedicated SEL/L8 checks, and the exact-posterior corollaries. The project can proceed after the following changes are applied and recorded. No wholesale redesign is needed. Existing drafts do not substitute for the protocol's statement-lock and subsequent review gates.

## Required changes

### 1. Correct the audit quantifier and state the actual uniqueness lemma

STATEMENT.md:8–12 currently says every use, including premise lists and definitions, occurs on a probability event. Those textual occurrences plainly are not event-local deductions. Also the brief requests a lemma on the uniqueness event; mass greater than one half is a sufficient special case, not the definition of uniqueness.

Evidence: W1-PXN/FINAL_PROOF.md:51–53; W1-GEN/lemmas/L2_centre.md:19–20 and :57–59; W1-GEN/STATEMENT.md:43–44; I1's own audit distinguishes premise lists, search-move ties, and output ties. W1-N3/STATEMENT.md §3(c) covers N = 1 even when cap = 1 and the truncation flag is true.

Replace T1.a and T1.b with exactly:

> T1.a (audit) Catalogue every occurrence and substantive use of e4, N3 and start-mode tie selection in W1-PXN, W1-GEN and M5(b1-LH), including T38 Theorem b1 and Corollary b1-LH (`NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md`). Distinguish method definitions and premise lists from deductions, and distinguish start-mode ties from LS0 move ties and reported-HPM ties. The target audit conclusion is that the consistency deductions requiring identification of the LS0 centre with a reference R use that identification only on {π₀(R) > 1/2}, where R is feasible and deterministic given X (and the fixed model parameters). Any use outside this event must be listed and resolved or retained explicitly as an obligation.
>
> T1.b (Lemma UM) Use the instance, feasible set Ω_K, objective f and normalized start law π₀ of `W1/W1-N3/STATEMENT.md` §1. Under its (H1), (H2), (H3), (H4), if argmax_{S∈Ω_K} f(S) = {R}, then `start_mode(st, cap).S = R`. In particular this holds on {π₀(R) > 1/2}. The implication follows from N3(c) with N = 1 (also from N3(a)); it requires cap ≥ 1 and does not require a false truncation flag.

### 2. Separate floating-point uniqueness from exact-score uniqueness; do not remove global EX-A

STATEMENT.md:13–17 folds a local binary64 result into a consumer-premise replacement through the phrase “EX-A or (H2-FP)+FP-TAB.” This can be read as an alternative to the consumers' full EX-A assumption. The consumers use exact scores/arithmetic elsewhere; a start-mode lemma cannot discharge that assumption. Mathematical uniqueness alone also does not guarantee native-double correctness. N3(e) concerns the code evaluation ĝ, not the mathematical objective f*.

The finite γ_k error expression in the draft additionally needs ku < 1; H2-FP alone does not impose it. This is a statement-domain issue, not a request to review the rounding proof here.

Replace T1.c and T1.d with exactly:

> T1.c (Lemma UM-FP) Under W1-N3 (H1), (H2-FP), (H3), (H4), let ĝ(S) be the coded `st.log_gamma0(S)`. If argmax_{S∈Ω_K} ĝ(S) = {R}, then `start_mode(st, cap).S = R`, by N3(e). To relate this to the mathematical objective f*, let f̂ be the exact-real evaluation of the stored double tables, η = max_{Ω_K}|f̂−f*|, and let ε be a finite uniform bound on |ĝ−f̂|. For feasible R, define Δ(R) = f*(R) − max_{S∈Ω_K\{R}} f*(S), with maximum of an empty set equal to −∞. The sufficient condition FP-TAB is Δ(R) > 2(η+ε). If ε is supplied by the recursive-summation γ_k formula in I1 §3, explicitly assume every index used satisfies ku < 1, where u = 2^−53. No claim is made that FP-TAB holds for the coded scorer, or with probability tending to one under fixed binary64 precision.
>
> T1.d (premise replacement) Supply a source-by-source replacement of the mathematical e4 obligation by W1-N3(c) + uniqueness, together with the retained integration premise: LS0 starts from and emits the coded `start_mode(st, cap).S`, on correctly encoded tables (H1), with cap ≥ 1 and execution hypothesis (H4). Under the consumers' existing EX-A, their events {π₀(R) > 1/2} give uniqueness and T1.b identifies that centre with R. Supply the replacement text and affected locations as patches inside C-PACK. LS0 integration remains an implementation obligation for C-ENG. T1.c is a separate conditional native-binary64 start-mode result; it does not replace EX-A elsewhere in PXN, GEN or M5(b1-LH), and does not establish those theorems for floating-point execution.

Propagate this distinction to I1 and any summary. If a particular integration/tie requirement is adopted for C-ENG, record it in METHOD_REQUIREMENTS.md and flag it in REPORT.md as required by the Wave-1C protocol. I1 currently refers to METHOD_REQUIREMENTS.md, but that file was absent when inspected.

### 3. Give Item 2 its precise retained regime and meaning of “unconditional”

STATEMENT.md:20–22 says “under identical hypotheses” without stating the compared domain or making explicit that the rest of GEN remains conditional on its implementation premises. GEN L6(b)'s complete X-event has five components; Theorem R and CONC′ supply particular components, not its entire verification. The I2 draft correctly identifies a rate substitution that should be part of the locked target rather than hidden behind “identical.”

Replace all of T2 with exactly:

> T2 (LH-iid without the two candidate inputs) Work in precisely the common LH-iid family of `W1/W1-PXN/STATEMENT.md` §1 and `W1/W1-GEN/lemmas/L6_instances.md` (b): fixed g, c, v, ρ, ψ_i, nonzero signal coefficients and σ² with the restrictions in PXN §1; iid Gaussian raw design rows, independent Gaussian noise; 18 ≤ p_n = gG_n ≤ n^A, p_n → ∞, fixed A ≥ 1; and eventual SIZE g ≤ B_n < 2g for the actual method's B_n and complete-linkage/top-down-cut/next-fit partition. Retain GEN's method, implementation and random-design hypotheses, including its uniform constants and deterministic envelopes. Compare Theorem B as used by GEN with PXN's repaired Theorem R, including partition definitions, parameter domain, SIZE onset and exact-branch convention. Prove that repaired (R-c), or the independently checked route (R′), supplies P(blocks ≠ groups) → 0. Replace the [CONC] correlation-rate use by [CONC′]'s δ_n = 32√(2(A+1)log n/(n−1)), giving uniform operator error O(log n)δ_n = o(1). Combine this with GEN's fixed-signal SLLN arguments for the remaining components of 𝒞_n and retain GEN's separate verification of its other X-event components. Conclude GEN (C5)(b) under the joint law of (X,ε), without assuming candidate Theorem B or [CONC] as additional inputs. “Unconditional” means removal of these two input conditions, not removal of GEN's remaining assumptions or a delivery claim. Record any domain mismatch explicitly and prove an extension or state the resulting common-domain restriction. Deliver Lemma I2 and exact citation/replacement patches.

This does not require an extension to varying within-group correlations: the cited LH-iid source has a common fixed ρ. Any broader version would need a separate stated extension.

### 4. Make Item 4's hypotheses and reported-PIP scope part of the locked statement

STATEMENT.md:32–36 is a list of names rather than explicit statements for several promised conclusions. It does not specify threshold conditions, the uniform-summary class, the other hypotheses retained in the no-beta-min clause, or M1(i)'s restriction to a fixed finite declared list. The latter matters if “reported quantities” is interpreted as simultaneous accuracy over a growing number p_n of PIPs. The chair's integration note at SoP/04_theory.tex:110 expressly separates that configuration from the larger stacking configuration.

Replace T4.b and the following misspecification sentence with exactly:

> T4.b Define π to be the exact D0 posterior, PIP_j = π(j∈S), and δ_n = 1−π(S₀), with π(S₀)=0 outside Ω. For every n, prove max_j|PIP_j−1{j∈S₀}| ≤ δ_n and max_{j∈S₀}(1−PIP_j)+max_{j∉S₀}PIP_j ≤ 2δ_n (maxima over empty index sets are zero). Any attainment example must state its feasible support and is a sharpness example among probability laws on Ω, not a claim that a D0 posterior generated by data attains equality. When S₀∈Ω, prove the uniform bound sup_{h:Ω→[0,1]}|π(h)−h(S₀)| ≤ δ_n. If δ_n = O_P(r_n), r_n→0, then these posterior errors are O_P(r_n); {j:PIP_j>q_n}=S₀ with probability tending to one when r_n=o(min(q_n,1−q_n)); exact MPM and every exact-posterior MAP/HPM are consistent. Here HPM in this clause means the posterior maximiser, distinct from the method's best-scored reported model.
>
> Instantiate r_n=√(log n/n) only under all T03♯ hypotheses R1, G, R, SE_λ(j₀), SE_w(m♯_n;g₀), and BM-∞ or BM(c>c₀), as defined in the TH09 card, under its fixed-design noise law; or under all W1-PXN (P) hypotheses with its joint data law. Any further random-design instance must exhibit the required uniform design events and envelopes. Without beta-min, retain the other hypotheses of T03♯'s large-signal clause and obtain only max_{j∈J_n(c)}(1−PIP_j) ≤ π(S⊉J_n(c)) = O_P(√(log n/n)), with J_n(c) and c>c₀ as in TH09; no specificity or full-support recovery follows from that clause alone.
>
> Reported summaries retain their own premises and statuses. Quote M1(i)'s status verbatim, “(h), (i): PROVED (by this seat, unchecked)”; retain its T03♯ hypotheses, osc d ≤ D*=O_P(1), declared summaries, implementation premises and pending IND-T extension audit. Its logarithmic stacking R′_n=4⌈log₂(n+p+1)⌉ is for a fixed finite declared list, and does not assert simultaneous sure screening over growing p_n reported PIPs. Quote separately the card's larger stacking configuration if used for a growing declared list. W1-N1 gives the islandwise evidence-weighted bound under its named premises on the successful-calibration/island-existence event; it does not establish consistency of pooled shipped R′=4 PIPs. Reported-HPM consistency remains joint with output, with no delivery claim.
>
> SL2 is conditional on M4(b),(c), exact score ordering, a positive-capacity store updated as top_c(T_old∪S_added), truth discovery with output, and δ_n=O_P(r_n) under the chosen law: P(O∩{max_j|PIP^T_j−1{j∈S₀}|>2δ_n})→0; consequently the same probability with threshold t_n tends to zero whenever r_n=o(t_n). State the input statuses verbatim; store-restricted PIPs are distinct from the sampler's reported PIPs. Misspecification (Song–Liang Thm 4/Cor 2) is routed to C-MIS and is not proved here.

The deterministic inequalities are plausible elementary targets. This review does not certify the drafted SL2 proof or any asserted extra random-design rate.

### 5. Qualify completeness of the Song–Liang map where the actual source is unavailable

T4.a promises each result, while SONG_LIANG_MAP.md says the exact Theorem S and its hypotheses are not available in the supplied main-paper PDF. That honest limitation must survive in the locked target. Do not turn a main-text mention into a hypothesis-level comparison of an unseen theorem.

Replace T4.a with exactly:

> T4.a `SONG_LIANG_MAP.md` maps Song & Liang (2015) Thm 1–2, Cor 1, Thm 3, thresholded ξ_q, Thm S, Thm 4/Cor 2, Conditions 3/5 and §6 to our corresponding result or explicit gap. Each entry records the original conclusion and hypotheses actually inspected, our regime, important differences, verbatim status and source location. Inspect the online supplement for Thm S if accessible; otherwise mark its exact statement/hypotheses NOT INSPECTED and compare only the MAP-consistency description in the main paper. Selection consistency does not supply their Hellinger/predictive theorem, exponential probability rates, exponential-p regime, or algorithmic equivalence. Thm 4/Cor 2 is referred to C-MIS.

### 6. Specify the fidelity baseline for Item 5

T5 is appropriately scoped, but “self-contained” and “nothing added” need to distinguish ordinary exposition from the two new C-PACK replacements. The supplement must preserve the council-passed PXN result, not silently substitute this ticket's results and label the result the same checked version.

Replace T5 with exactly:

> T5 Produce a consolidated supplement in `item5_PXN_consolidated/` for every clause (R),(S),(E),(T),(P),(C),(K) of `W1/W1-PXN/STATEMENT.md` v2, with its superseding §5 notes, as mapped by FINAL_PROOF.md and REPORT.md. Apply E-1..E-22 and every later council/sweep correction recorded by that baseline. Include the definitions, hypotheses, repaired arguments and dependency-status ledger needed to read the proof without consulting API-PXNGAP PROOF.md for omitted steps; explicitly name any retained external theorem inputs. Preserve all method/integration premises, exact-branch convention, onsets, joint events, rate and cost qualifications, and exclusions. Provide a clause/repair-to-location manifest. One fresh Codex xhigh fidelity check compares the consolidated text against this complete baseline for omissions, strengthened claims and changed premises. Expository additions are allowed; C-PACK's new e4 and LH-iid replacements are separately identified addenda with their own review status, not silently incorporated as council-passed PXN claims.

### 7. Restore the mandatory review order and coverage in PLAN.md

The plan omits the fresh independent mid-point checkpoint and explicitly excludes Item 5 from the exhaustive sweep/council. Both conflict with the binding protocol for finished ticket work. Item 3 also needs a specified disposition if the checks require a patch: an unreviewed repair is not VERIFIED. Item 2's numerics cannot be waived wholesale; existing evidence can be reused with exact applicability documented.

Replace PLAN.md's final two lines with exactly:

> Review gates: apply and record the statement-lock changes before further proof work. For each new lemma and each repaired SEL/L8 claim, record falsification evidence (exact small cases or simulations with ≤20 seeds, local compute only) and a fresh cross-family line-by-line check before downstream use. Reused Wave-1 numerical evidence must be named with its exact tested scope; Item 2 also checks the CONC′/operator-error substitution and the relevant onset/domain conditions, not only partition recovery. Numerical experiments are falsification attempts, not proofs of tail bounds. Any SEL/L8 repair is supplied as a patch and independently re-checked; an actual counterexample triggers the protocol's stop-and-report rule.
>
> Once the key lemma is ready, request a fresh independent Codex xhigh mid-point review using only STATEMENT.md and proof files, not the lead's conclusion or log. Continue only on CONTINUE; on REDIRECT/STOP, stop and report to HQ. Before final review, run the citation-check script on every cited path:line/quotation and save reviews/CITECHECK.txt, correcting every miss. Then perform an exhaustive sweep of the whole ticket, including the Item-5 consolidated supplement and its fidelity manifest; fix findings, followed by council review of the same complete package (Sol xhigh and Opus high). Pass requires both scores ≥8.0 and all gates passing in the same round; at most three rounds, with unresolved findings and exact scope reported honestly. R36's dedicated fidelity check is additional evidence, not a substitute for these ticket-wide gates. Preserve all input statuses verbatim, link every verified/checked assertion to its actual review file, and update LOG.md at each step.
>
> Check the local clock at major steps. CHECKPOINT.md is due 01:30 CST and final REPORT.md/final message 04:30 CST; if gates or targets remain open, report PARTIAL with the exact frontier. No edits outside C-PACK and no git state changes.

Update the individual track descriptions to follow these gates; the sentence “all started” is a historical log entry, not evidence of approval or completion.

### 8. Define the missing path alias

STATEMENT.md uses NBH/ without defining it. Append exactly this sentence to its alias paragraph:

> `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

## Optional suggestions

- Give each deliverable a clause-level acceptance table (target, source, patch, numerics, reviewer, remaining premise). This will prevent a review of one component from being reported as a proof of the entire ticket.
- Mark future review filenames as planned until the actual reply exists. I1/I2/I4 currently use “PROVED (by this seat)” rather than the protocol's exact unchecked wording; use “PROVED (by this seat, unchecked)” pending the applicable checks, and cite completed reviews by filename once obtained.
- Keep the Item-1 consumer edits and Item-2 dependency edits small and separately reviewable. No mutation of Wave-1 sources is needed.

Verdict: **LOCK-WITH-CHANGES**
