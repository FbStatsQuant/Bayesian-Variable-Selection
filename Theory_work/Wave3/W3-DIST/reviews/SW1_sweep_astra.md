MANIFEST de9ccec7bb2a07d5cc36fa8a0ab13eb4e78ae697d30b4b3ddcd296fde7ac5957
Summary: 0 CRITICAL / 0 MAJOR / 9 MINOR findings; the package is ready for council after the local statement, map and records corrections below.

# SW1 exhaustive sweep — Astra

This first part was written before opening REPORT.md, DEPS.tsv or any previous review. Findings SW1-01–06 and the mathematical assessments below are the blind-pass findings. The second pass appended below audits the records without revising those findings in response to previous reviewers. Paths without a prefix are relative to Theory_work/Wave3/W3-DIST. Appended amendments within proof files are treated as part of the current proof, not as unresolved defects in their superseded paragraphs.

## Findings — blind pass

### SW1-01 — MINOR / F: the statement describes an obsolete proof of X

Location: STATEMENT.md:359–364 and :421; compare lemmas/X.md:8–16, :100–136 and :138–150.

The route summary says X4 uses truncated Occam moments, Lemma V, an exp(||P_S0 e||²/(2 sigma²)) payment and a truncation surcharge, and uses Lemma S for the outer size tail. The adopted proof instead uses an untruncated fractional moment, re-proves its instance of V(a), and proves its own outer size bound. Its header expressly removes the dependence on the stream-C files. The consumes row for POST2:A0/A1 likewise incorrectly describes t-scaled truncated weights as the content used by X4. This does not invalidate X: the adopted argument supplies the needed estimates itself.

Repair: replace the structure paragraph by the actual route: the noise event; conditional Gaussian/IG bounds for good models; score suppression of small models with large ridge loss; a lambda=(4A+1)/(4A+2) moment of superset Bayes factors plus the union-with-truth comparison; and the independently re-derived numerator/denominator size tail. In the A0/A1 row retain A0's determinant-interface motivation/implications, and remove the assertion that A1's truncated weights are consumed by the current X proof. Identify S and V as separately proved companion lemmas/templates, not required proof-file dependencies of X.

### SW1-02 — MINOR / S: the assumption maps conflate coefficient cost with ridge loss

Location: TARGET.md:16 and ASSUMPTION_MAP.md:15; compare STATEMENT.md:56–59 and lemmas/X.md:23, :105–111.

The summary groups '(C; M′) / (L0; B)' together as entering X3 and S through L_S0. That suggests the weaker ridge-loss bound can replace (C) throughout. The current statement correctly says that X uses rho′=(||mu||²+||theta*||²)/n, not merely L_S0<=B. The variational comparison's 3rho′ payment is an actual use of the stronger bound.

Repair: distinguish (E)+(C), which bound rho′ for X/X′ and their superset comparison, from (L0), which suffices for DIST-3 and for the size-tail argument with an appropriate reference. Copy the distinction already made in STATEMENT.md:56–59 into both maps. Do not describe a replacement of (C) by (L0) in DIST-1 as established.

### SW1-03 — MINOR / C: the DIST-2 predictive specialization omits ell_n

Location: STATEMENT.md:289–295; compare work/D_output/P6_DISTC.md:414–415.

DIST-C is introduced for either (1.1) or (1.2), but its displayed predictive bound is C²t/n+exp(-(c-lambda)t) in both readings. For (1.2), convexity gives C²t ell_n/n+exp(-(c-lambda)t). The proof file explicitly makes this substitution. The introductory 'with its rate' indicates the intended reading, but the displayed conclusion should not leave that substitution implicit.

Repair: write epsilon_n²+exp(-(c-lambda)t), with epsilon_n²=C²t/n for DIST-1 and C²t ell_n/n for DIST-2, or state the two cases explicitly. The domination and exceptional-probability bounds are unchanged.

### SW1-04 — MINOR / F: B3's copied beta-min assumption drops positivity

Location: work/E_bridges/B3.md:10–11 and :69–72; compare STATEMENT.md:211–212 and :411.

The reader statement explicitly requires b_n>0, but B3's restatement of (A6)(b) omits it. Squaring the lower bound in Step 5 requires this sign. The reference to the named (A6) supplies the intended hypothesis, so this is a local copy repair, not a new missing assumption in Theorem B. Taken as a standalone displayed hypothesis, a negative b_n would make the displayed lower bound vacuous while b_n²n/log n could still diverge.

Repair: insert 'b_n>0' in B3 line 11, preserving the common deterministic envelope and the rest of Step 5.

### SW1-05 — MINOR / E: the maps have not incorporated NEC's resolution of the exponential stretch

Location: ASSUMPTION_MAP.md:16, :41–46; TARGET.md:17, :29; API_CARDS.md:78–89. Compare STATEMENT.md:120–124 and lemmas/NEC.md:153–185.

These current summaries still present S-FIT's sharp exponential fixed-design core as open/pending an attack. NEC now disproves that precise uniform exponential strengthening. The historical N4 observations remain legitimate finite-sample observations; they do not reopen the question NEC answers. Conversely NEC does not settle the random-design integrated-Hellinger strengthening or the general in-probability fit question.

Repair: add a current-status note to Card F and both maps: the fixed-design exponential version is false by NEC; the general in-probability version and an iid random-design counterexample remain open. Label N4's 'improvable' assessment as historical evidence about that family, with the subsequent NEC qualification. In TARGET's P2-without-ND row specify which random-design question remains open rather than presenting the whole fixed-design stretch as unresolved.

### SW1-06 — MINOR / E: active internal line pins point to superseded locations

Location: work/E_bridges/B0.md:14–16, :28–29, :56, :108–116; B1.md:20, :64–65; B2.md:26–29; B3.md:26, :46, :55, :93; ASSEMBLY.md:11–23, :64, :88, :93, :125, :128, :153, :197; work/D_output/COR_C.md:33, :89–90, :138. The target headers also retain old coordinates, sometimes explicitly labelled v1.3.1.

The mathematical objects are identifiable by name, but many bare STATEMENT.md line citations no longer land on them in the frozen file. For example B3 cites STATEMENT.md:94 for TR0 (now :101), :95 for the four DIST-3 events (now :103), and :62 for the cutoff (now :68); ASSEMBLY cites :68–71 for (1.1) (now :74–77) and :86–88 for (1.2) (now :93–98). B0's posterior pin :29–32 now lands on the retained-dimension discussion; the posterior is at :34–40. This is distinct from an explicitly historical reference to an old version.

Repair: refresh the active bare pins against this freeze, preferably replacing volatile line numbers by section/claim identifiers. In particular use STATEMENT §0 for objects, (1.1)/(1.2)/DIST-3 for the master displays, §1R Theorem A/B/Corollary C for reader claims, and §3 B0–B3 for bridge targets. Current reader claims begin at :185, :209 and :217; the current lemma blocks H/T/S/V/X/X′ begin at :322/:328/:342/:350/:355/:366. Clearly label any deliberately retained historical pins as historical. No mathematical repair is needed.

## Per-claim assessment — blind pass

'Proved' here is this review's mathematical verdict, not an upgrade of a registry status or a discharge of an expressly inherited premise.

| Claim | Verdict | Qualification |
|---|---|---|
| DIST-1 | proved as stated | Includes (c), the law-uniform constants and the common n0 over t. |
| DIST-2 | proved as stated | The exponent is in t, not in t ell_n; no ND is used. |
| DIST-3 | proved as stated | Conditional oracle bound; additive delta_n and the TR0 event remain explicit. |
| DIST-C | proved after the listed repairs (SW1-03) | DIST-2 predictive display only; all delivery premises remain conditional. |
| Theorem A | proved as stated | Both displays on one event, capped window, at most s, and the no-A4 version. |
| Theorem B | proved as stated | Conditional on POST:Thm-1 as labelled; b_n>0 is already in its statement. |
| Corollary C | proved as stated | The strengthened reported-HPM conclusion is valid. |
| H | proved as stated | Arbitrary predictor law; dropped true columns allowed. |
| T | proved as stated | Deterministic d; simultaneous in the affine coefficients and scale. |
| S | proved as stated | Exact capped R_m, arbitrary reference, and positive response variance. |
| V | proved as stated | No rank or eigenvalue-floor assumption is hidden. |
| X | proved as stated | SW1-01 corrects the description, not the theorem or adopted proof. |
| X′ | proved as stated | The enlarged n0 absorbs the variance displacement uniformly in t. |
| P6 | proved as stated | Positive threshold a; arbitrary output-dependent mixture weights. |
| NEC | proved as stated | Fixed-design fit obstruction only; it changes no TC clause. |
| B0 | proved as stated | Uses the supplied R′ equivariance as labelled. |
| B1 | proved as stated | Includes null truth and arbitrary response scale. |
| B2-core | proved as stated | Singular covariance handled on its range, with the intercept included. |
| B2 | proved as stated | Capped cardinalities and the exact reader window matter. |
| B3 | proved after the listed repairs (SW1-04) | Its standalone copy of (A6); its named upstream assumption is already correct. |
| TC1 | proved as stated | Joint-law Hellinger, not an empirical-only distance. |
| TC2 | proved as stated | Radius, inner/outer probabilities and full t range agree. |
| TC3 | proved as stated | Radius constant is independent of raw sparsity for fixed A,sigma²,M,M′. |
| TC4 | proved as stated | No additional design-law condition in the transfer. |
| TC5 | proved as stated | The coded prior and posterior identification are preserved. |
| TC6 | proved as stated | Extra logarithm in the radius and reduced exponent in epsilon notation. |
| TC7 | proved as stated | Oracle display under E,L0,TR0 with delta_n additive. |
| TC8 | proved as stated | The deterministic clauses and joint-with-completion form are sound; SW1-03 clarifies the accompanying predictive specialization. |
| TC9 | proved as stated | Primitive reader assumptions, both simultaneous displays and no-A4 clause. |

## Unharvested strength

Some items are already mentioned inside proofs but are stronger than the headline statements; none is needed to validate the targets.

1. X uses ND only for ceil(32t/log n)<j<=min(m_n(t),p-s0), and only through a lambda-power-mean bound (X:113–136). Thus the stated full-range ND is sufficient but stronger than this proof needs.
2. T's constants actually leave an outer bound delta/2 in the proved relative-event calculation. Keeping delta is harmless.
3. S's basic inequality is valid for every n>=3 and t>0 with its displayed finite-n terms; the asymptotic t-window is a convenient specialization. Its nested size events also permit simultaneous control over eligible cutoffs, as the proof notes.
4. V's Gaussian determinant calculation can retain actual ranks in place of cardinality upper bounds. No full-rank assumption is necessary.
5. B2's standardization calculation gives the stronger unnormalised lower bound c_psi/4 on its event; the published c_psi/8 is conservative.
6. The conditional oracle calculation in DIST-3 does not use p<=n^A. It needs the true-model dimension bound, the named energy/ridge/transfer events and the coded conditional posterior.
7. P6's domination statement is pathwise for any data/run-dependent probability law on models with exact conditional kernels. Independence of that law or of its retained mass from the data is unnecessary; thresholds can be evaluated pathwise as well.

## Checks performed — blind pass

### Statements and interfaces

- **STATEMENT.md — read first line to last.** Checked the data convention, the plug-in intercept, response units, retained-model prior, raw support used in transfer, random retained sparsity, all master displays and reader versions, every named bridge, conditional alternatives, consumes table and changelog. Findings SW1-01/03 concern local descriptions/displays. The current rho′/L0 distinction and S-FIT/NEC scope are correct in this file. The theorem statements themselves cover p=2 and s0=0 without an implicit full-rank assumption.
- **TARGET.md — read first line to last.** Matched TC1–TC9 against the actual proof; checked the companion-result scope. A read-only exact string comparison found the complete reader block identical to STATEMENT (9,888 characters each). Findings SW1-02/05 concern the maps. The Song–Liang table distinguishes metric, prior, rate, exponent, dimension and moment restrictions rather than asserting containment of assumption classes.
- **API_CARDS.md — read first line to last.** The common contrast definitions and matrix identities agree with the proofs. Cards are candidate interfaces, not additional established conclusions. Card F needs SW1-05's current-status note; S-APX/S-EXP remain expressly stretches.
- **ASSUMPTION_MAP.md — read first line to last.** Findings SW1-02/05. Boundary numerics are correctly identified as finite-n diagnostics, with pooled-tail and restricted-family limits; I did not use them as proof.

### Proofs

- **lemmas/X.md — read first line to last, including §9 and lead notes.** Re-derived the variational comparison, Gaussian fractional moment, concavity step, prior multiplicity, interlacing determinant bound, geometric sum, powered Markov step, integrated-numerator size tail, small-model score suppression and conditional Gaussian/IG tails. In particular A(1-lambda)-lambda/2=-1/4; after exp(s0)q<=n^(-1/8), the sum is at most 2exp(-4t), without a hidden K_s. The union multiplicity is paid by M0>=(A+1)s. The noise events and subsequent Markov events yield the stated c=1/2. Clean mathematically.
- **TC3 calculation.** C_d=34, C_x,C_P,Lambda,C_Q,C_v,C_X are independent of s=s0^r for fixed (A,sigma²,M,M′). log C5=log 2+(s+1)log 4+3(M+M′)/(2sigma²)+(s/2)log(8A+4), bounded as stated. Therefore M0<=16+4(1+s)(A+1)+3(M+M′)/(2sigma²). In DIST12, d1 log n<=34t gives C_T=4[34(A+7)+8], also independent of s. Thus C_DIST1²=C_X²+C_X/2+1+C_T has the promised sparsity dependence. n0 may depend on s,c_D,kappa0; no claim hides that dependence.
- **X/X′ uniformity.** The n0 conditions are imposed for every n>=n0 at the largest t, and their t-dependent left sides are monotone or bounded by the largest-t envelope. The X′ condition sqrt(t/n)log n<=1 absorbs its Q displacement. Checked s0=0, empty sums, m=K, comparison unions outside Omega, c_D replaced by min(c_D,1), and the denominator's fixed b_- before expectation. No circular use of S or V.
- **lemmas/DIST12.md — read first line to last.** Deterministic d1,d2 use raw p and raw s; neither is selected after observing dropped columns. The intercept contributes its own 2exp(-t) event. No independence between interface and transfer events is used. Checked C′=33 for the rounding inclusion, the 3exp(-t/2) probability budget, D.4's constants, and D.6's additional ell_n. Clean.
- **work/B_transfer/H.md — read first line to last.** Re-derived the normal affinity and truncated mean bound, including arbitrary discrete/singular predictor laws. The empirical identity is epsilon-bar²+||mu-hat-mu||²/n; sample-constant true columns disappear from the centred mean but remain in the raw affine error. Clean.
- **work/B_transfer/T.md — read first line to last.** Checked countable rational reduction/measurability, layer cake, the two-half-space growth bound, ghost-sample Cantelli step and swap argument. The swap inequality 13W>3N+8n eta² and 48/169>=1/4 give the advertised exponential constant. The displayed entropy ensures n eta²>=25 on the stated d-range. No moment assumption or sample-independent coefficient choice is needed. Clean.
- **work/B_transfer/DIST3.md — read first line to last.** Re-derived the true-model Gaussian mean fluctuation, ridge-bias bound and IG concentration; no eigenvalue floor is used. TR0 concerns raw true directions including the intercept. The fixed-law finite-second-moment consequence follows by a finite-dimensional covariance law of large numbers on the covariance range, including degenerate directions; it is not silently extended to triangular arrays. Checked arbitrary M_n by truncating the auxiliary u to the admissible window. Clean.
- **work/C_size/S.md — read first line to last.** Re-derived the approximate-reference denominator, fixed-b numerator expectation, random-b sandwich, cross-term tail, response-scale bracket, 5exp(-t)+4exp(-c_B n) budget, and sufficient cutoff with the sum stopping at K. The reference can depend on design, not noise. The appended withdrawal of the earlier independent-simulation wording is observed. Clean.
- **work/C_size/V.md — read first line to last.** Checked the two variational inequalities, strict spectral bound for D′, determinant cancellation and rank bound, and projection domination. Singular Gram matrices and empty S0 cause no inverse of an unregularized Gram matrix. Clean.
- **work/D_output/P6_DISTC.md — read first line to last, including amendments.** Checked finite-mixture domination, conditioning on the positive-mass store, Hellinger convexity, top-store invariant, HPM ordering, discovery bounds and localized delivery clauses. The current amendments correctly avoid an unconditional claim that the empty model must remain in the store. The DIST-2 proof uses the correct radius; SW1-03 is in the copied statement only. Clean mathematically.
- **work/D_output/COR_C.md — read first line to last.** Checked the exact-arithmetic identification, original-index mapping, returned list versus a parameter distribution reconstructed from it, and C1/C2. On a completed run with pi(S_true)>1/2, every other model has smaller pi and hence smaller F. Once scored/offered, S_true is the unique store leader and ledger HPM; v3_run.R:142 returns that HPM and pi(T)>=pi(S_true)>1/2. Strict inequality removes all tie-rule concerns; the numerical near-ties diagnostic is not a replacement for exact ordering. The event is joint with completion, not conditional on completion. Clean mathematically; stale pins are SW1-06.
- **work/E_bridges/B0.md — read first line to last.** Checked positive affine response transformation, posterior pushforward, common-density Jacobian in Hellinger distance, predictive mixtures and signal-to-noise interfaces. The supplied MISR:R′(a′),(b) are used within their domain. Clean; SW1-06 applies to pins.
- **work/E_bridges/B1.md — read first line to last.** Re-derived scalar sub-Gaussian sample-mean/second-moment concentration, sample/population variance ratios, retention of all columns, energy and coefficient bounds; constants are uniform over the law and permit null truth. Clean.
- **work/E_bridges/B2core.md — read first line to last.** Checked whitening only on the covariance range, adjoining the intercept, the net cardinality 21^(rank+1), lower empirical quadratic bound and the entropy condition. The intercept is necessary for the centring step and is present. Clean.
- **work/E_bridges/B2.md — read first line to last.** Checked sample-standardization, interlacing, the determinant-ratio implication, the cap min(p,m+s0), window calculation and exponential failure probability. For q_n=p one must use the cap, not the generally false m+s<=p; the current amendments do. Checked one n_B works for all 1<=M<=sqrt(n)/log n. Clean.
- **work/E_bridges/B3.md — read first line to last and both amendments.** Checked the capped window for m-sharp, the bounded-size floor, TR0, beta-min and item-6 conditioning. The replacement outside the full-retention event preserves the fixed raw dimension required by the imported theorem; it is independent of noise. SW1-04 repairs the local assumption copy; SW1-06 repairs pins. No new selection theorem is inferred without the labelled POST premise.
- **work/E_bridges/ASSEMBLY.md — read first line to last and amendments.** Checked response normalization, maxima over 0<=s0^r<=s, levels t=M log n/C², size cutoffs, uniform n0, the no-A4 route and its different constants, and the common success event. The final constant/threshold choices absorb all fixed prefactors. Checked Theorem B through B3 and the oracle theorem, and the example's spectral/sub-Gaussian hypotheses. Clean mathematically; SW1-06 applies.
- **lemmas/NEC.md — read first line to last.** Checked the centred near-copy Gram eigenvalues, critical tau² scale, orthogonal noise coordinates, event probability bounded below, null posterior mass bound, aggregate singleton comparison, conditional fit lower bound and the resulting c(k)/n mass. For fixed C,c choose T>=2/c and then fixed k>24CT; this contradicts the proposed exponential core for sufficiently large n without requiring uniformity in k. At j=2 a proportion tending to one of pairs exhibits the insufficient determinant growth. The concluding list correctly excludes iid random-design integrated-Hellinger impossibility, in-probability inconsistency, and refutation of any TC. Clean.

### External inputs and code

- **Locked [P1] PROOF_v3.tex — read in full.** Checked contrast dimension N=n-1, shape 0.51 before updating, posterior shape 0.01+n/2, the response-scale identification, spectral/slab identities, prior ratios/tails, fixed-b density expectation and random-b sandwich. The uses in S/X match their domains; denominator arguments are explicitly re-derived when the reference hypothesis changes. Clean for the consumed material.
- **W3-POST/STATEMENT.md and lemmas/L1a_size_tail.md — read in full.** Checked R1's s0>=1 restriction for Theorem B, E/F0/F_lambda/F_w/BM, item 6's common constants and envelope, and the data-free cutoff. The no-floor size lemma is a template, not a silently upgraded external premise. Clean use.
- **W3-POST2/STATEMENT.md; A_occam.md; B_tail_approx.md; D_hellinger.md; E_visibility.md — read in full.** Checked the exact ADG/DG/OS definitions and union ranges; the cost of an approximate reference; D0/D1 computations; selection versus no-selection oracle claims; and the ridge-margin comparison. Local computations are re-derived in this ticket. D(b)'s distinct fallback status is retained; it is not needed for the proved main chain. SW1-01 concerns the stale consumes description, not an invalid imported inequality.
- **W3-MISR/STATEMENT.md — read in full.** R′(a′),(b) provide the positive-scale parameter-posterior transformation used by B0. Checked that projective model-posterior invariance alone would not justify parameter equivariance; the actual import is the stronger stated result. No misuse found.
- **W2-APP/lemmas/L1_POST.md — read in full.** The Gaussian-row/LSF result and its conditional status are not generalized to arbitrary sub-Gaussian rows by citation; the reader bridges supply their own concentration proof. Clean use.
- **W1-N1/STATEMENT.md — read in full.** Checked exact arithmetic, ideal streams, START/KERNEL, localization and potential-versus-completed record distinctions. No completion probability is inferred. Clean use.
- **W3-SAMP/STATEMENT.md and lemmas/CC_code_check.md — read in full.** Matched D-i/P-OVL, LT-e, C-v and TR-d to the delivery alternatives and their named premises. CC supplies the engine-level facts outside the permitted direct-code packet. No claim that pip_primary is a model probability law or that completed outputs are unbiased conditionally on completion. Clean use.
- **W3-RM2/STATEMENT.md — read in full.** The fixed/Gaussian design regimes, LS0 configuration and inherited POST qualifications differ from unconditional discovery. DIST-C explicitly marks the completion/reporting links unchecked and no proof here uses that alternative; I do not discharge those links.
- **C-PACK I4_SL_corollaries.md and SONG_LIANG_MAP.md — read in full.** SL0(iv)'s strict-majority uniqueness and the distinction between exact, measured and store-restricted summaries are preserved. The map is historical, not evidence that later Hellinger results are absent.
- **T04_A3_contraction/STATEMENT.md — read in full.** Treated only as a route guide; its H-T02 and fixed-design/in-probability limitations are not imported as a proved exponential result.
- **Song–Liang article — inspected journal pp. 950–955 using pdftotext to stdout.** Checked the joint-law metric normalization; prior cap and Bernoulli parameter; conditions (9)–(14); strict versus approximate sparsity; Theorem 2's diverging r_n; Corollary 1's two branches; and second-moment display (16). TARGET's comparison is a comparison of rates/forms with qualifications, not a proof that the coded prior satisfies their conditions. The supplement was not consulted.
- **Scripts/SMC_BVS/core/v3_run.R and cpp/v3_ledger.h — read in full.** Checked completed-status gating, hpm return, top_store return, original-index mapping, capacity 40p_ret+1, exact score/size/lexicographic top ordering, deduplication, and offer_stores feeding both HPM and top store.
- **Scripts/SMC_BVS/core/cpp/v3_core.cpp — inspected the pinned reporting/ledger/final-run region :330–510, exact enumeration :530–568, calibration setup :602–618 and export :725–739.** Checked empty cache, table ingestion, inherited model cap, final local-search centre, LS0, irreversible failure status, returned summaries, and inherited stores. The exceptional direct HPM offer occurs only on numerical failure, so does not invalidate completed-run retention. The exact branch calls top.offer but has a distinct status. No defect found in these pins.
- **Docs/Experiments/P1M/DECISIONS.md — D-17 row only.** It supports the stated measurement-methodology description, not a universal store-mass or posterior-dominance premise. No experimental claim was used in a proof.
- **Manifest — read-only verification succeeded**, using nice python3 -B and one-thread environment limits. Reader-block comparison was read-only and nice. No numerical simulation, cluster job, agent, git operation or temporary file was used.

## Not checked — scope of this review

- No prohibited route drafts, API attempts, X12, logs, checkpoints, plans, or alternative proof files were read. In particular no conclusion is based on the unchecked in-probability API attempt mentioned in STATEMENT.
- No underlying proofs beyond the allowed input packet were audited: e.g. the W3-RM2 output-event bridge, SAMP's engine proofs, registry/HQ adoption history and the Song–Liang supplement. Their stated premises/status qualifications are not discharged by this review.
- Direct source-code verification is limited to the three permitted code files and the regions described above. Pins to v3_engine.h, v3_util.h, v3_preprocess.R, v3_fit.R, v3_score.h, etc. were checked against the supplied CC/input statements where covered, not by opening those files. This includes hpm_better's secondary tie order; the strict-majority conclusion also makes its secondary rule immaterial.
- Numerical scripts/results and the descriptive D-17 measurements were not independently reproduced. No floating-point, PRNG, resource-guard delivery-probability or computational mixing guarantee is asserted.
- External quoted registry statuses that are not independently printed in the allowed statements cannot be authenticated against the live registry within this packet. This is a limitation of the permitted evidence, not a discovered mathematical defect.

## Pass 2 — records

The blind-pass text above was written before reading the records. I then read REPORT.md and DEPS.tsv in full and inspected only the named review files needed for the checks below. The following are additional records findings; they do not revise the blind mathematical verdicts.

### SW1-07 — MINOR / F: registry summaries need synchronization with their cited statements

Locations and exact repairs:

- **REPORT.md:121:** at t=M0 log n the radius is C sqrt(M0 log n/n), not C sqrt(log n/n) with the same C. The latter is an order statement only after absorbing sqrt(M0). Preserve the explicit M0 factor, or use a differently named constant and say it depends on s. This matters because TC3 deliberately distinguishes C from M0.
- **REPORT.md:139:** the scope says 'no polynomial bound on p', whereas the pinned STATEMENT still places DIST-3 in (RD), including p_raw<=n^A. The proof does permit removing that restriction (recorded above as unharvested strength), but the generated registry must not silently do so. Retain the stated scope or first adopt the strengthening in STATEMENT. In the same line, restore the condition that the four design events have probability tending to one before the 'hence' in-probability conclusion, as at STATEMENT.md:106–108.
- **REPORT.md:146–148:** the DIST-C registry lists ND for the combined theorem and omits its DIST-2 alternative from both conclusion and depends_on, although STATEMENT.md:290 and the proof's Remark 6.6 include it. Record the alternatives separately: DIST-1 interfaces; DIST-2 without ND; and the selection/oracle alternative with its own premises. The deterministic domination clause needs none of those contraction hypotheses by itself. Add DIST-2 to the appropriate dependency branch.
- **REPORT.md:155:** the two separate probability inequalities omit Theorem A's stronger common-event assertion. Add that one data event of probability at least 1-n^(-cM) supports both posterior bounds, including the qualified no-A4 variant, as in STATEMENT and the amended assembly.
- **REPORT.md:185–188:** Lemma S is reference-adaptive, but its assumption list uses A:COEF-REP and points only to the exact-truth setting at STATEMENT.md:17–70. Replace that assumption by the actual condition T in Omega and B_T(vartheta)<=B from :342–345, with a design-measurable reference and the fixed-design Gaussian mean setting. A bounded true coefficient vector is sufficient for a particular reference, not the general lemma's hypothesis. Include the explicit cutoff and t-range by pointer to :342–348.
- **REPORT.md:25 and :220–222:** the P6 record includes the predictive-convexity clause, but the claimed STATEMENT span :379–380 contains only (a) and (b); (c) is in the proof file. Either add that already-proved clause to the master lemma statement or supply a separate statement pointer to work/D_output/P6_DISTC.md §3 P6(c).
- **REPORT.md:83:** 'no statement of this ticket assumes a posterior close to a point mass' is too broad. DIST-3's consequence and Theorem B use selection consistency, and the discovery-based retention alternative uses pi(S0)>1/2. Replace this by 'the store-BMA domination/contraction transfer does not require a posterior close to a point mass; the selection-based alternatives retain their named premises.'

These are local repairs to derived metadata and commentary. The corresponding mathematical arguments and the primary STATEMENT's qualifications are available; no new proof is requested.

### SW1-08 — MINOR / S: implication and sharpness metadata overstate the evidence

Location: REPORT.md:123–124, :157 and :248; compare TARGET.md:30 and the stated scope of NEC.

1. The unqualified registry edge 'implies: W3-POST2:D' is not an implication of that whole source theorem on its original hypotheses. Lemma X supplies an in-sample sharp-rate counterpart under its own ND interfaces; POST2:D(b) assumes OS, and the package itself distinguishes those assumptions. Its D(a) is an oracle statement as well. Repair: remove the whole-claim implication edge, or replace it by a precisely identified restricted common-hypothesis consequence. Keep the valid metric/rate comparison in prose. Similarly, B2's edge to the whole Cor-1R should target only its F_w/determinant-floor subclaim, as the current parenthesis already intends, not the complete selection corollary.
2. Theorem A's A4 is marked NECESSARY-FOR-ROUTE with NEC as evidence. NEC is a fixed-design counterexample to deleting all relevant geometry from X; it is not an iid random-design necessity result for the reader's particular population floor. Nor is this sufficient population floor the only way to obtain ND. Repair: label A4 as a sufficient primitive bridge to ND, with necessity for the reader theorem unestablished, and put NEC's negative result only on the fixed-design core with its precise scope.
3. A3 and A5 are marked WEAKENABLE with ASSUMPTION_MAP.md:59 as evidence. That passage gives finite-family numerical evidence for A3 and explicitly says an A5-violation experiment has not been done; it does not establish a replacement hypothesis preserving the reader's probability bound. Repair: distinguish 'candidate weakening / numerical evidence only' from a proved weakening, or state and cite an actual proved replacement. Likewise the coefficient-cost NECESSARY-FOR-ROUTE entry at :124 should preserve :79–80's explicit 'unchecked' qualification on the cited API counterexample. I did not open that prohibited attempt or assess its validity.

No claim that ND is logically necessary for every consistent design should be inferred from NEC: it establishes failure of the uniform theorem after wholesale deletion of the hypothesis. These corrections keep the records within the results actually stated and checked.

### SW1-09 — MINOR / F: two DEPS descriptions bind historical verdicts to the current checked hash

Location: DEPS.tsv:2 and :26.

The TC/DIST-1 row says L6's NOT VERIFIED consequence-(c) verdict was 'at checked_sha', but checked_sha is the current 9b468ca7d9e4d185. L6's actual first line names c05fb3f082fcb938; D1 verifies the current hash. The NEC row says L7 verified 'at checked_sha (v0.2)', but checked_sha is current v0.3, 48cb55be4d967f3e. L7's actual first line names v0.2, 54340e87b89336a1; D3 verifies the current hash. The later checks do support both current OK states, so there is no unreviewed proof revision implied by this finding.

Repair: replace the two historical uses of 'at checked_sha' by the actual historical digest and version, retaining the current sha/checked_sha fields and the D1/D3 recheck descriptions. This makes the audit trail literal rather than requiring the reader to infer which hash each clause means.

### REPORT §1 and registry audit

Every §1 row's STATEMENT line range and proof-file locator lands on the intended current claim. The P6 row's additional convexity description needs the statement-source clarification in SW1-07. The line-check statuses are supported by the review trails sampled below, including final amendment checks; none is presented as a council pass of this ticket. The qualified SOP:TH09, W3-POST and sampler dependencies remain explicit.

I checked every registry block, including its statement/premise spans, assumptions, conclusion, rate, scope, dependencies, implication and sharpness fields where present:

| Registry block | Result |
|---|---|
| DIST-1 | Display, event remainder, t-range and core dependencies agree. Explicit rate factor and implication/sharpness metadata need SW1-07/08. |
| DIST-2 | Display/radius and removal of ND agree. The rate's use of p rather than p_raw is harmless at fixed polynomial A as an order statement; use p_raw for literal notation consistency. |
| DIST-3 | Oracle bound agrees; restored design-event qualification and formal dimension scope needed, SW1-07. TR0 has its own correct assumption pointer at :100–112. |
| DIST-C | Domination and completion scope agree. Alternative-specific interfaces and the DIST-2 edge need SW1-07. |
| Thm-A | Reader setup/assumptions, level window and rates agree. Common event and sharpness labels need SW1-07/08. |
| Thm-B | Clean: exactly s>=1, positive beta-min sequence, selection conditionality and parametric consequence agree. |
| Cor-C | Clean: mass premise is a property of the run; strengthened HPM conclusion and EX-A are retained. |
| H | Clean: deterministic reduction and dropped-column scope agree. |
| T | Clean: arbitrary iid law, deterministic d-range and simultaneous transfer agree. |
| S | Reference hypothesis/source span needs SW1-07; bound and absence of a polynomial-dimension restriction otherwise agree. |
| V | Clean: variational inequality and determinant moment agree; singular designs allowed. |
| X | Clean core statement and self-contained P1 dependency list. Interpret NECESSARY-FOR-ROUTE only as the fixed-design uniform-deletion obstruction, not a pointwise necessity assertion. |
| X′ | Clean: larger mean threshold, m_n(t) size cut and absence of ND agree. |
| NEC | Clean: fixed-design null-truth example, 0.6 probability and c(k)/n mass; no target refutation is claimed. |
| P6 | Correct proved content; statement-source mismatch for clause (c), SW1-07. |
| B0 | Clean: positive-scale pushforward, defined-posterior domain, n-dependent noise and R′ dependency agree. |
| B1 | Clean: factor-two sample variance bound and its energy/cost consequences agree. |
| B2core | Clean: augmented/intercept quadratic bound, entropy restriction and failure probability agree. |
| B2 | Core bound and dependencies agree; scope the Cor-1R implication to its intended subclaim, SW1-08. |
| B3 | Clean: common selection interface events, exactly s>=1 and inherited posterior theorem qualification agree. |

The primary premise pointers sometimes refer to the common setup while a specialized assumption is supplied by a second pointer or named claim (notably TR0 and A6); I checked those together, rather than treating the first range as the complete hypothesis list. The S reference condition is genuinely different and is singled out above.

### DEPS spot checks — nine rows, including all eight required subjects

For each row, a read-only, nice python3 -B calculation recomputed SHA-256 of the named proof file; its first 16 hexadecimal characters match both sha and checked_sha. All named review paths exist. I inspected the review headers, relevant verdicts and amendment-chain passages, not just filenames. 'OK' below describes the recorded completed-check state, not immunity from this sweep's minor findings.

| DEPS row | Current SHA-256 prefix | Review evidence inspected | State assessment |
|---|---|---|---|
| X | 15d23ee7a05e96a1 | L1_astra_X:1–9, :168–183 verifies v0.3; D1_sol_diff:1, Part A items 1–5 verifies current v0.4 constants and surviving X′ argument. | OK supported. |
| TC/DIST-1 | 9b468ca7d9e4d185 | L6_sol_DIST12:1, :7–23, :73–79 distinguishes verified displays from the old TC3 gap; D1_sol_diff:1, :50–84 verifies the repaired constants and EQUAL-on-TC3 claim. | OK supported; fix historical hash wording, SW1-09. |
| T | 193cdc8145e724e8 | L3_sol_B:1, :19–30, :50–56 gives the matching hash and VERIFIED verdict, including the delta/2 slack. | OK supported. |
| S | 956fdbb925c113a5 | L5_astra_SV:1, :7–43, :88–97 verifies the mathematics with local repairs; D1_sol_diff:2, :88 checks A-5–A-7 at the current hash. | OK supported. |
| B2 | 5c1328b5bad99922 | L4_sol_E:1, :7–11, :89–99 has the current B2 hash and VERIFIED-WITH-AMENDMENTS verdict. Its requested capped-window wording is present at current STATEMENT.md:400–405. | OK supported. |
| P6 | 0b0b1556cfba806b | L2_sol_D:1, :105–117 verifies P6(a)–(c); D1_sol_diff:8–26 identifies the intervening normalization/event repairs; D3_sol_diff:1, :9–40, :93–118 verifies the current file and resolves them. | OK supported. |
| NEC | 48cb55be4d967f3e | L7_sol_NEC:1–15, :152–168 verifies v0.2; D2_sol_NEC_diff:1–17, :52–61 records the remaining numerical-remark issue; D3_sol_diff:1, :80–101, :114 verifies the v0.3 repair. | OK supported; fix historical hash wording, SW1-09. |
| R/Theorem-A | e2bb6ed765be030f | L4_sol_E:63–73, :89–99 records the common-event amendment; D1_sol_diff:2, :92 verifies A-6–A-8 at the current hash and the stated constant/range qualifications. | OK supported. |
| R/Corollary-C | 55d8b14f968de040 | L2_sol_D:113; D1_sol_diff:2, :90; D3_sol_diff:1, :50–64, :116 verifies retention and the actual returned-HPM conclusion. | OK supported. |

The older L1/L5/L6/L7 headers intentionally name older proof hashes; the newer D1/D3 checks close those transitions. No current hash mismatch was found. The unchanged B2 file is already at L4's hash. Unchecked fallback, stretch and unused independent-version rows remain labelled as such and were not treated as proved dependencies.

### Further checks and limits of pass 2

- Spot-check review files inspected: L1_astra_X.md, L6_sol_DIST12.md, L3_sol_B.md, L5_astra_SV.md, L4_sol_E.md, L2_sol_D.md, L7_sol_NEC.md, D1_sol_diff.md, D2_sol_NEC_diff.md and D3_sol_diff.md. These were read only after the blind pass had been written. D3 expressly uses the same intended DIST-2 rate substitution noted in SW1-03; this corroborates that the proposed repair is an explicit display clarification, not a new mathematical objection.
- As a final code-pin check, I also read v3_core.cpp:1–61, confirming the original/internal index conversion at :24–41. It does not alter any blind finding.
- I did not authenticate the BR1 'not broken' claim against BR1 itself or read every earlier review/disposition: the required current-hash chains above are the spot-check scope. I did not inspect mkreport.py, REPORT_extra.md, the live registry, HQ records, forbidden alternatives or experimental result files.
- REPORT's old 'not verified by a reviewer' sentence at :94 should be read narrowly: D1 and D3 explicitly inspected T01's affected identification passage, and the present sweep read the permitted P1 file in full. No blanket fresh audit of every upstream theorem or its adoption status follows from those checks.
- The present per-claim mathematical table is unchanged by the records pass. SW1-07–09 require only metadata/wording repairs, not alterations to the protected target clauses.

Summary: 0 CRITICAL / 0 MAJOR / 9 MINOR findings; the package is ready for council after the local statement, map and records corrections above.
