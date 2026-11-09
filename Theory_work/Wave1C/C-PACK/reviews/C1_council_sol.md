# C1 council review — sol

Independent assessment: **ACCEPT for the scored items 1–4; all six gates PASS.** I found no blocking mathematical issue or counterexample to the repaired statements. One documentation-completeness issue is non-blocking and has exact proposed text below. Score: **9.0/10**, without a score cap.

Reviewer: Codex council seat sol, 2026-11-08 CST / 2026-11-09 UTC. This review follows `reviews/COUNCIL_BRIEF.md`. I did the review myself and did not consult or coordinate with the other council seat. Only files in `Theory_work/Wave1C/C-PACK/reviews/` were written; no git command was run. `C1_sol_snapshot.sha256` identifies the ten scored source files. Paths below use CP = `Theory_work/Wave1C/C-PACK/`, W1 = `Theory_work/Wave1/`, SoP = `Theory_work/State_of_Project/sections/`, NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`, and CODE = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.

**Item 1 — PASS, with the documentation note below.**

UM is an immediate valid consequence of N3(c): a unique global maximiser gives N=1≤cap. N3(a) supplies a second route. The probability-mass condition π₀(R)>1/2 implies global uniqueness, rather than merely uniqueness within one cardinality. Neither route needs `truncated=false`; the cap=1 flag behaviour is correctly preserved. I checked the hypotheses and conclusions directly in `W1/W1-N3/STATEMENT.md:92-132`, its floating-point proof, and `CODE/cpp/v3_start.h:183-240`.

UM-FP correctly separates the mathematical tables, stored-table objective, and rounded fold. The finite uniform encoding error η and evaluation error ε both enter the strict margin Δ(R)>2(η+ε). The fold uses at most m rounded additions after the exact initial addition from zero, so the γ_m bound is appropriate. Cancellation and gradual underflow do not invalidate the addition bound. The capped table domains, K=0, finite-intermediate premise, and ku<1 restriction are explicit (`CP/lemmas/I1_e4_replacement.md:86-119`). This conditional start-mode result supplies no native-binary64 theorem for scoring, subsequent search, ordering, or the complete method.

The audit resolves the substantive off-event uses. PXN's unordered-partition identity cannot identify capped coded centres on tied inputs; I1 §1.1 replaces it by the valid uniqueness-event bound. GEN's structural closure still needs the deterministic emitted centre and scan/guard contracts on all potential output runs. GEN (C6) separately uses N3(a)'s global maximality under EX-A, and the optional T38 data-dependent-centre sketch is excluded. These distinctions match `W1/W1-GEN/lemmas/L5_assembly.md:11-16`, `L7_counterexample.md:60-75`, and `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:247-266`. The current P-e4 Note (0) preserves that distinction. The positive consistency deductions need no smallest-size/lexicographic start tie property. LS0 integration remains an explicit premise, not an accomplished code change.

**Item 2 — PASS.**

The common-domain restriction is correct: the same fixed-parameter, raw-coefficient LH-iid family, actual B_n, eventual SIZE, and complete-linkage/top-down-cut/next-fit partition are used. This does not extend the repaired probabilistic input to every heterogeneous exact-Gram LH instance of GEN. The hypothetical-partition convention handles exact-dispatch indices without imposing a lower polynomial growth bound on p. On that branch feasible truth is already enumerated.

I independently checked both probability substitutions against `W1/W1-PXN/lemmas/R_branch_repair.md:9-40` and `CR_corr_tails.md:11-50`. The strict-margin argument avoids the defective A0(c) formulation; route R′ alone would suffice. At the stated δ_n, the union bound is exactly 3n^−2. Interlacing and the symmetric row-sum bound give λ_min(R̂_T)≥λ₀−L′_nδ_n, uniformly over the required subsets. Here L′_nδ_n=O((log n)^(3/2)/sqrt(n))→0. The energy and sample-scale assertions concern finitely many fixed signal columns and are unaffected SLLN steps. GEN's other X-event components, constants, envelopes, implementation premises and de-randomisation remain necessary and are retained (`CP/lemmas/I2_LHiid_unconditional.md:61-85`; `W1/W1-GEN/lemmas/L6_instances.md:53-84`).

Replacing log p by log n can weaken the rate for slow p; the current text says so and does not infer their equivalence. The corresponding squared errors and S2 domination step are also addressed. The P-LHiid edits now remove the old candidate-conditioning sentences from the claim, lemma header, and report prose, rather than only renaming a dependency.

**Item 3 — PASS.**

For SEL, the deterministic enlarged family T₀(l) is essential: the Gaussian residual is independent of the conditioning columns and truth columns, including the truth-column sample scales used by this generator. Conditional isotropy yields the fixed-pair Beta law with dimension n−1−|T₀|. Its exponential moment is O(n^(1/4)) uniformly because |T₀|≤15. Adding the selected other-null-group columns perturbs partial correlations by O(log n/n); after the uniform fixed-pair tail bound the exponent error is o(1). P-SEL.1 correctly localises domination to F_n while taking an unconditional moment of the fixed-family sum. The resulting bound retains P(F_nᶜ), the factor 2^75, and the n^−1/8 Markov term. It does not assert a conditional Beta moment after partition selection or a finite-n leakage guarantee. The positive-scale convention and 14-coordinate embedding are correct; the signed alternative includes the extra absolute-value edits.

For L8, projection cancellation proves zero leakage for the exact support; the Schur-complement eigenvalue floor proves VIS. For the thresholded split, the reverse triangle inequality gives VIS with the stated same M_n and the small-part energy bounds every leakage residual. The patched compatibility condition η/2+sqrt(2η(A+ε₀))<1/2, with κ at most the remaining positive gap, is the correct condition for NL_avg. It agrees with the original calculation at `NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T22iii_T16_start_aggregation/PROOF_v2.tex:404-425`. The W coefficient θ(1+ε_n/3) gives the required disjoint-support split; θe_j alone would not. The other GEN hypotheses, feasibility, and bounded-certificate restrictions remain separate obligations (`W1/W1-GEN/lemmas/L8_certificate.md:7-10`).

The procedural records exist: R31 and R32 give the dedicated checks; R37 independently rechecks the patches, with its signed-scale/rate amendments now incorporated. I inspected the numerical scripts and outputs. In particular, the SEL finite-n exceedances are disclosed as finite-n failures of the asymptotic target inequality, not suppressed or called asymptotic counterexamples.

**Item 4 — PASS.**

SL0 is valid on the finite capped model space, including infeasible truth via δ=1 and empty coordinate sets. The uniform [0,1] summary error equals δ when truth is feasible. The two-point swap proves arbitrary-law sharpness only; the current text correctly disclaims D0 attainment. SL1 follows from these deterministic bounds, and boundedness gives expectation convergence without an expectation rate. Moving thresholds require r_n=o(min(q_n,1−q_n)). SL1′ retains the other T03♯ hypotheses and gives sensitivity only on the large-signal set.

The T03♯ instantiations match the recorded hypotheses at `NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-60` and `SoP/04_theory.tex:775-788`. The additional GEN instance needs, and explicitly invokes, every-sequence tightness transfer through common X-events/envelopes; pointwise conditional convergence would not suffice. Fixed-list logarithmic stacking, the separate larger-list polynomial configuration, islandwise evidence-weighted records, and the shipped pooled estimator remain distinct.

SL2's retention argument is valid with exact score ordering, a positive-capacity union-then-top-c store, and truth discovery on output. On δ<1/2, discovered truth is the strict global maximiser and is retained. On δ≥1/2, every coordinate error is automatically at most 2δ. Thus the first failure probability is bounded by the with-output discovery failure alone; the deterministic tolerance conclusion then adds P(2δ_n>t_n). This does not require conditioning on successful output or assuming delivery. The store PIPs are not identified with the sampler's reported PIPs.

I opened the supplied Song–Liang PDF directly and read the theorem/condition pages, the standing §2.1 setting, and §6; I also inspected the existing journal-p.955 page image for relation signs. The current map correctly distinguishes Hellinger contraction, screening, MAP, misspecification and conditional cost accounting. It retains the positive-power lower dimension-growth assumption of their correct-specification setting and the fixed-subset/nonbinding-cap limitation of Thm 4/Cor 2. I could not obtain the supplement: the [publisher article endpoint](https://academic.oup.com/jrsssb/article/77/5/947/7040600) redirected to an inaccessible endpoint, and the [Wiley supplementary-PDF endpoint](https://rss.onlinelibrary.wiley.com/doi/suppl/10.1111/rssb.12095/supinfo/rssb12095-sup-0001-supinfo.pdf) was inaccessible. Exact Theorem S hypotheses remain **NOT INSPECTED**, as permitted by the locked target. The main-paper description is not substituted for its missing theorem statement.

**Gate verdicts**

| Gate | Verdict and reason |
|---|---|
| G1 | **PASS.** The current UM/UM-FP, I2, repaired SEL/L8 and SL0–SL2 steps survive independent re-derivation and the finite checks below. No blocking false step found. |
| G2 | **PASS.** The used hypotheses match the statements: common LH-iid domain, exact-branch convention, common design events/envelopes, admissible ε₀/κ, fixed signal scale, arithmetic and operational contracts. |
| G3 | **PASS.** No hidden partition-conditioning, logarithmic-growth equivalence, delivery premise, D0 attainment claim, expectation-rate inference, or complete-method floating-point guarantee is needed. |
| G4 | **PASS.** Input qualifications are adequate and no upgrade is made. N3's ticket status is "PROVED-CHECKED"; T03♯ is "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; PXN/GEN ticket results are "PROVED-CHECKED", not adopted by HQ. M1(i) retains "(h), (i): PROVED (by this seat, unchecked)". M4(a) retains "candidate: not reviewed, not adopted" and "AUTHOR-ONLY", M4(b) retains "same as (a); W1PC1 §3 B.D3(b) COUNTEREXAMPLE repaired with ‖h‖$_{∞}$", and M4(c) retains "N13: PROVED (PC1 claim 5)". SL2 assumes these inputs and its finite-set steps are also checked directly here. Historical N3 "OPEN", the excluded iid conflict, and SAME-FAMILY-ONLY inputs remain distinguished from the new addenda. |
| G5 | **PASS.** The strict 2(η+ε) margin, γ_k restrictions, correlation constants, λ₀/2 onset, O((log n)^(3/2)/sqrt(n)) error, SEL constants/exceptional events, and L8 admissibility inequality track correctly. O_P is not turned into an expectation rate or a numerical onset guarantee. |
| G6 | **PASS.** I checked the frozen start fold/DP, full-response tables, capped BB prior and partition implementation against CODE. e4′ explicitly preserves the all-data emitted-centre and scan/guard contracts. LS0/fallback integration remains a C-ENG premise. Native-binary64 UM-FP covers only start identification; shipped R′=4 pooled PIP consistency is not claimed. |

The status quotations above were compared with `W1/W1-N3/REPORT.md:11-13`, `W1/W1-PXN/REPORT.md:3-8`, `W1/W1-GEN/REPORT.md:18-25`, and `SoP/04_theory.tex:130,410-412,491,788`. In particular, preserving the historical status ledger is compatible with proving a separately labelled premise replacement; it does not certify implementation integration.

**Blocking issues: none.** No blocking fix text is required.

**Non-blocking issue — complete the occurrence inventory in the consumer reports.**

`CP/lemmas/I1_e4_replacement.md:20-40` covers the substantive proof uses, but T1.a literally asks for every occurrence. GEN REPORT has additional explanatory premise mentions at :16, :30 and :97-98; PXN REPORT:47 and ERRATA:17 repeat the historical bypass wording. P-e4 does not explicitly catalogue these report/erratum occurrences. This does not change a deduction, hide a hypothesis, or invalidate the operative proof patches. It is a small residual documentation omission.

Exact suggested addition to the I1 audit:

> G9: `W1/W1-GEN/REPORT.md:16,30,97-98` — D, explanatory summaries of the e4/N3 implementation premise; no additional deduction. Read the current premise as e4′ of I1 §4; EX-A, the deterministic emitted coded centre, OP-LS0 and completed scans remain. Preserve historical quotations and verdicts.
>
> P7: `W1/W1-PXN/REPORT.md:47` and `lemmas/ERRATA.md:17` — D, historical descriptions of the original P5 bypass. Preserve those historical review statements and append a C-PACK addendum pointing to Lemma UM and the off-event transfer repair in I1 §1.1.

Exact suggested addition to P-e4:

> In GEN REPORT:16,30,97-98, add the C-PACK premise addendum: "The positive consistency claims now use e4′ (C-PACK I1 §4); Lemma UM discharges start-mode identification on the uniqueness event. The all-data deterministic/emitted centre, EX-A, OP-LS0, guards and completed-scan contracts remain premises, with integration pending." Do not rewrite quoted historical statuses. In PXN REPORT:47 and ERRATA E-10, retain the historical bypass description and append the corresponding C-PACK Lemma UM/I1 §1.1 pointer.

**Independent numerical and citation evidence**

`CP/reviews/C1_sol_checks.py` and `C1_sol_checks_out.txt` record this seat's fresh tests. They execute the pre-existing W1-N3 compiled harness, without rebuilding it. The checks passed for 600 abstract tables with p≤8, shuffled ordered partitions, K including zero, caps 1/2/10^6 and widely separated binary64 magnitudes: 600 rounded value/membership checks, 468 unique-rounded-mode cases, 277 unique exact-mode integer-table cases, 423 sufficient FP-TAB cases with η=0, and 20,221 exact-fraction fold-error comparisons. Integer-weight calculations checked 1,792 truth/law pairs and 1,014 truth-containing stores. Twelve Gaussian-design seeds supplied 576 VIS inequalities and 384 leakage comparisons for L8; no positive excess occurred. The ε₀ positive/negative controls also passed. These are finite falsification checks, not asymptotic proofs or scorer-error certification. Existing R33 covers nonzero encoding-error examples; I did not rerun every historical numerical campaign.

I also executed the current citation-check function without its overwrite entry point. `CP/reviews/C1_sol_citecheck.txt` reproduces the saved generated summary: 142 range checks, two short-form resolution misses and 14 quote flags. The two short forms and the flagged semantic/status passages are addressed by the lead's current manual dispositions in CITECHECK.txt and by the direct source comparisons above. This automated scan is not a semantic-proof certificate.

Item 5 is context only under this council brief. Its independent fidelity record is R36, "FAITHFUL-WITH-FIXES"; INDEX now identifies that check and keeps I1/I2 as separate addenda. I assign no new mathematical council score to the consolidated supplement and do not upgrade its inherited or fidelity statuses. The acceptance above applies to the specified items 1–4 and their patches, under their stated premises.

SCORE: 9.0; GATES: G1 PASS; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 PASS
