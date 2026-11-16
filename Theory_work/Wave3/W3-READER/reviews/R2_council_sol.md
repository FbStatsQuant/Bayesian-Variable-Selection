# W3-READER — council R2, seat sol

Frozen content reviewed: MANIFEST `3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b`.
The required verification command printed `verify: OK` before review. This is a fresh review of the R2 content, including a check of the R1 repairs against both permitted R1 reviews. No subagents, commits, or content edits were made. The only files created are this review and supplementary checks under `.rc_tmp/R2_scratch_sol/`. Excluded gate records, helpers, APIs, staged deltas, logs, checkpoints and other reviews were not read.

**Overall score: 9.3/10.0. Accept as is.** There are no C, S or F findings. The displayed conclusions and their substantive interpretive readings follow from the registered masters under the stated assumptions/conventions. Remaining suggestions are editorial and do not affect this score or the gates. Acceptance does not upgrade the quoted conditional or author-only input statuses.

## Per-claim decisions

The reader decisions include their remarks, interpretations and associated card rows. Prime statements and the additional distribution statements are listed separately to make coverage explicit. R3 is accepted only in its now-explicit historical scope.

| id | decision |
|---|---|
| W3-READER:PoolZ | ACCEPT |
| W3-READER:R1 | ACCEPT |
| W3-READER:R2 | ACCEPT |
| W3-READER:R3 | ACCEPT |
| W3-READER:R4 | ACCEPT |
| RV/thm1 | ACCEPT |
| RV/thm1′ | ACCEPT |
| RV/thm2 | ACCEPT |
| RV/thm3 | ACCEPT |
| RV/thm4 | ACCEPT |
| RV/thm5 | ACCEPT |
| RV/thm6 | ACCEPT |
| RV/thm7 | ACCEPT |
| RV/thm8 | ACCEPT |
| RV/thm8′ | ACCEPT |
| RV/thm9 | ACCEPT |
| RV/thm9B | ACCEPT |
| RV/thm9C | ACCEPT |
| RV/thm10 | ACCEPT |

Row 1.1 was reviewed in Form A. Its unused Form B is outside the brief. Row 3.7's frozen placement is form (a), and the frozen body Theorem 8′ is the plain A-inf statement; there is no additional live (b1) theorem text in this manifest to review.

## Findings — editorial only

### E1 — minor — finish separating the historical bridge labels from the current route

At [CLAIMS_CARD.md:68](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:68), the final column still says “NEW bridges R2, R3”, although R3 is now historical and the current delivery bridge is B6.6′. **Correction:** “NEW bridge R2; delivery identity B6.6′; R3 historical.”

At [READER_VERSIONS.md:883](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:883) and :884, B7.2/B7.3 still contain the old BM-∞/BM-Q-to-BM-W commentary. The current proof supplies BM-W⁺ through B7.2′/B7.3′; the width portions of the unprimed rows remain useful. **Correction:** label the BM-∞/BM-Q commentary “historical, under the former hypotheses”; retain the W-χ/W-loc implications as current and point to the primed rows for truth removal. These legacy comments are read in the explicitly retained previous-master context, not as a second proof of the current constant-level theorem. The current theorem and its active proof do not require the stronger old signal hypotheses.

### E2 — minor — small wording cleanup

At [CLAIMS_CARD.md:72](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:72), remove the repeated “Given the frozen calibration”: start “On calibration success, given the frozen calibration and the data, …”. The present sentence already carries the correct conditioning and potential-run scope.

At [READER_VERSIONS.md:1344](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1344), “slower … by a factor exp(C sqrt(log n))” is an informal comparison. **Correction for exactness:** write “its ratio to the posterior reference rate is exp(C sqrt(log n))/sqrt(log n)”. Both stated O_P rates are already correct; no claimed convergence changes.

## Re-derivation of PoolZ and R1–R4

**PoolZ.** N1, `Theory_work/Wave1/W1-N1/STATEMENT.md:94-104`, supplies the localised identity for each fixed island index. On A, R′=4. Intersecting four probability-one sets and averaging gives

`E[Zhat/Z | C] = (1/4) sum_r E[Zhat_r/Z | C] = 1` on A.

With the data fixed, Z is a strictly positive constant. Under the joint law, condition first on `(data,C)`, use H-U/SI's independence from data and calibration streams, multiply by the measurable indicator of A, then apply the tower property. This proves `E[1_A Zhat]=E[1_A Z]`; no completion event is inserted. No cross-island independence is needed. Code `v3_run.R:91,150-154` indeed uses four islands and the logarithm of their arithmetic evidence mean. The potential-versus-reported identification is exactly SAMP:PC, :90-95. ACCEPT.

**R1.** Put t=log n>1, d=1/log(3/2).

- B1.1: `||X theta|| <= sum_j |theta_j| sqrt(n-1)` gives the stated energy bound.
- B1.2: `s+ceil((2A+1)s)+1 <= (2A+2)s+2`, including noninteger A.
- B1.3: the quoted cutoff bound gives `s+m# <= 2s+1+(As+s/2+1)t/log 2`. Absorbing the first term into `(2s+1)t` leaves the positive coefficient difference printed in R1. It therefore covers every anchored union required by F_w, not merely feasible models.
- B2.1: `(1+d log 2)/log 3=d` exactly. Thus `s+mbar <= d(As+1.5s+2)t`; the decimal upper coefficients and their slack against `5(A+1)(s+1)` are correct. The j0 branch is smaller as well. A constant population floor meets LSF's growth condition.
- B4.1: use the maximum of the preceding m# and j0 branches. B6.1 is already strict at A=s=1,n=3 and its slack increases thereafter.
- B3.2: centring an independent isotropic Gaussian column and normalising it gives an independent uniform direction in the contrast sphere. Polynomial p and fixed s imply both logarithmic restrictions. For random truth columns this is applied conditionally; the master's random-configuration transfer then supplies the joint-law claim.

ACCEPT. These arguments establish the inequalities analytically; the numerical grid is supplementary.

**R2.** Normal equations give `e_A=e_T+X_T d` with zero cross term; in population notation,

`v_A=v_T+d' Sigma_TT d <= v_T+||d||_1^2 <= v_T+L^2`.

A unit diagonal implies `|Sigma_ik|<=1`. The Schur complement and interlacing give `v_T >= lambda_min(Sigma_{T union {l}}) >= c`. Division yields `v_A <= (1+L^2/c)v_T`. The sample identity has a factor n−1 in both the quadratic-form upper bound and the residual-variance lower bound, giving `1+L^2/phi0^2`. All choices of T,l share the same bound, and L_n→0 supplies the required uniform vanishing multiplicative error. The reader's extra L_n→0 condition legitimately gives up the master's separate-variance-clause alternative. ACCEPT.

**R3.** Its antecedent is now explicitly the former hypotheses, namely RM2-R/RM2-F's hypotheses, including the old signal and visibility assumptions where needed. Those masters supply [SAND], [NA], [TL], [POST]. A union bound supplies F-UNI(S), [POST] is F-UNI(P), and the corresponding setting supplies (V). Its premise table carries the operational assumptions; it does not infer them from statistical conditions. F-UNI@2.1.0, `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:8-21`, has exactly the enlarged cap, fallback, allocation, bounded-domain alternative and IDEAL-W⁺ alternative stated here. The unbounded-n consistency clause is attached to IDEAL-W⁺. The claim is no longer offered as a bridge from current constant-level Theorem 7 assumptions to the old master. ACCEPT in this historical scope.

For current Theorems 6–7, I separately compared S4(i)–(iv) with `W3-RM2-R/STATEMENT.md:71-93` and the allocation in `Wave1C/FINAL/sections/s6_delivery.tex:29-44`. Exact unit-cost arithmetic, MACH, the shipped search/fallback configuration, tie selection/cost premise, random numbers, guards, valid input/seed and the amended allocation are carried. The registered A:IDEAL-W+ lifts only the two specified application-level ceiling predicates. The two delivery audits remain explicit conditional inputs. Hence B6.6′/B7.5 correctly supply DLV-0 without R3.

**R4.** R1 supplies LSF and FL-R16. W2-APP's `L1_POST.md:11-18,27-33` expressly permits deterministic standardised signals, so posterior miss is `O_P(sqrt(log n/n))` under the joint law. On an event of probability tending to one it is at most 1/2, and then `o1<=2 delta`; hence o1 has the same rate. START2-R IF-START, :241-245, under the stated no-leakage hypotheses gives `1_A o0=O_P(rho_n)`. Choose the rate constant C positive (increasing it is harmless). Then `sqrt(log n)/exp(C sqrt(log n))→0`, so rho_n dominates the posterior reference rate. Also rho_n→0 and is eventually decreasing: its logarithmic derivative with respect to log n is `−1/2+C/(2 sqrt(log n))`. Thus `1_A max(o0,o1)=O_P(rho_n)`. SAMP(C-v), :158-162, supplies precisely the localised rates and intersection conclusions; PC transfers them to completed printed fields. ACCEPT.

## Independent checks and code reading

[checks.py](/home/fb31/BVS-wt/W3-READER/.rc_tmp/R2_scratch_sol/checks.py), with [output](/home/fb31/BVS-wt/W3-READER/.rc_tmp/R2_scratch_sol/checks.out), passed **1,872** exact-ceiling envelope configurations, including noninteger A, and **500** population/sample regression configurations. The largest population normal-equation identity residual was `3.33e-16`. These do not replace the analytic arguments above.

I directly read the frozen production code for preprocessing, prior/score, start tables/normalisation/drawing, pilot steps, fallback selection/freezing, final SMC, search, ledger retention, pooling and output flags. In particular:

- `v3_preprocess.R:19-32,37-68,97-127`: retained-column dimension, centring/scaling, cap, B≤16 and production budgets.
- `cpp/v3_score.h:39-71,175-223`: the beta-binomial weights, normalised prior, ridge g-prior score, n/2 shape and determinant ratio. Direct prior-ratio algebra gives `(2p-1-k)/(k+1)`; the extra half-log-n cost belongs to the marginal likelihood.
- `cpp/v3_start.h:68-137,153-176`: block-score product, capped size-profile DP, normaliser and exact categorical draws under the named idealisations.
- `cpp/v3_calib.h:25-44` and `v3_calib.R:84-190`: ESS targeting with forced minimum pilot steps, last successful construction before pilot fallback, tier escalation and freezing.
- `cpp/v3_engine.h:285-331,370-418`, `cpp/v3_core.cpp:453-480`: initial `m(empty) Zbar0`, reweight/resample/move, full deletion/addition/swap scans, strict improvement, shipped LS0 cap, extra scan and certification; guards prevent complete output after interruption.
- `v3_run.R:106-163,178-195` and `v3_fit.R:79-85,113-118`: equal-weight evidence/PIP pooling, MPM threshold, public certificate tied to the reported model, unavailable estimates on stops, preflight before a statistical record exists.
- `cpp/v3_ledger.h:78-112` and `cpp/v3_core.cpp:124-137`: the offered statistical ledger defines the reported model; timing-only scores do not enter it.

No production build or simulation campaign is needed to validate these mathematical implications and source descriptions. The empirical certification counts, engineering D-17 observation and scaling/parallel experiments are explicitly empirical; I did not independently reproduce those experiments or read their excluded/non-frozen source records. They discharge no theorem hypothesis in this review.

## Reader-to-master checks

Here and below, RV means `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`; Card means the adjacent `CLAIMS_CARD.md`. Master short names denote `Theory_work/Wave3/<name>/STATEMENT.md`, except APP = `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`, N1 = `Theory_work/Wave1/W1-N1/STATEMENT.md`, and F-UNI = the delivery lemma cited above. Line numbers refer to the frozen files.

| reader | hypotheses, quantifiers and conclusion checked |
|---|---|
| 1, Form A | A3→E; A4→F0/F_lambda by R1; A5→F_w; A6 is BM(c) with c=C_beta² phi0² or BM-∞. POST2:C :83-94 gives the uniform expectation bound, with the stated envelope-dependent onset. The 4C joint HPM/MPM error follows by a union bound of two 2E(delta) bounds; Markov gives O_P and the deterministic PIP inequality supplies uniform-in-j error. The abstract uses the checked O_P root, while the expectation route keeps its conditions. |
| 1′ | A4′ is F0+ID; L_S≥Delta_S implies ID^M. A5→F_w→OS through A0, with common constants. POST2:E :126-137 and C(iii) give the stated conclusions; A5 is retained, so there is no design-free claim. |
| 2 | R1→both LSF ranges; APP :11-18 covers raw coefficients; :27-33 supplies common sample events/constants and joint-law transfer. Only the probability rate is asserted; no random-design expectation rate is added. |
| 3(a) | PSHARP:B :90-104 is deterministic for every subset, hence the renaming to S is valid. The domains |S|≤K−1 and |S|≤p/2 are present in the display and sparsity readings. |
| 3(b), remarks | Fixed s0 and s0<p give feasibility eventually. N-orth→W-orth-E since p≤n−1+s0; N-gauss with polynomial p→W-sph-E, using the random-configuration clause as necessary. PSHARP-R:AE :61-92 gives the every-p expectation bound and growing-sparsity obstruction; PSHARP:A :71-77 gives the probability bound only when p→∞. A2C :94-100 gives the orthogonal critical-scale bound. B3.8 independently re-derived: a fully orthogonal design meets Theorem 1 with A=1, phi0=1,g0=1 and fixed nonzero signals. The two-sided expectation statement keeps that witness scope. |
| 4 | A0 supplies independent Gaussian residuals conditional on candidates (B4.0, with no explicit omitted columns). R1 supplies CorGb-plus's floor range; A3 uses its diverging beta-min branch. MISR-R :96-108 gives both displayed O(r_n) bounds with arbitrary n-dependent residual variance. Examples are :80-86; the KL/centred contraction and uniform fixed-design remarks are :112-155. No full-model support or non-Gaussian residual claim is inferred. |
| 5 | A3–A5 match FL-R16,V-R,L-R⁺⁺ with Q=S0. START2-R :226-237 supplies the first and sharper rates. A6→L-gain-0 by the Gaussian conditional-covariance identity. FLOOR, START :241-243, has the same n≥4,s0<K restriction. The leakage form changes only l outside S0 to l outside Q and retains truths/reference sets as the master does. |
| 6 | A3=V-R; A4=L-R^b including feasibility and 15rho+b<1/2; A5→T1-R/FL-R; A6+A5→D-loc^b by R2 and thence W-R. RM2-R-plus :177-181 and RM0-plus :118-142 give the common data event, every admissible seed/calibration quantifier, output intersection and error split. S4 supplies DLV-0's extra delivery premises. The chosen event in remark (i) includes MODE,Sand,NA,TL and supports the deletion/certification assertion. |
| 7(a) | A1→T1-F-flat; A2=FL; A3=V-flat; A4=L-gain/feasibility. Logarithmic Q permits any sufficiently small positive b<beta(eta,A); W-chi supplies W. The displayed constants give BM-W⁺ using d_n²≤D log n for D>2+4A and n large. RM2-F-plus :166-175 gives the claimed common event and additional delivery conclusion. |
| 7(b) | The separate signal condition and Remark (a)'s BM-Q-flat form supply BM-W⁺ (:107-112). Local regression plus R2.2 gives the variance clause of W-loc; |N_l|≤h log_2 n is exactly nu_n log2≤h log n, with h+b<1/2. RM2:W-suff :231-234 supplies W. No BM-∞ is needed by the live primed route. |
| 8, abstract form (a) | SCR:A1 :158-163 with the stronger full sparse floor. Constants fixed in n, q<K, budget c1 and the intersection event all match. No conditional-on-certification or output-frequency guarantee is introduced. |
| 8′ | Exact gamma formula and its (n+1)/n relation to Q agree with SCR :51-60. The liminf margin and intersection conclusion are SCR:A-inf :87-90, with no hidden polynomial-p or fixed-sparsity requirement. S1's fixed noise only narrows its master. |
| 9, 9B, 9C | Renamings of raw/retained dimension and sub-Gaussian constant give DIST:Theorem A :185-207, B :209-215 and Corollary C :217-238. The fixed-level reordering retains the common constants/n0 and M≤sqrt(n)/log n condition. Exceptional sets, uniformity, slower-radius fallback, detectable-signal window, exact-arithmetic list weights, list-mass premise and universal completed-run quantifier match. The conditional-Hellinger identity is DIST :42-52. |
| 10 and PoolZ remark | R4 establishes exactly SAMP:C-v :158-162. S5 carries the sampler contract and potential-record convention; A includes SMC dispatch and calibration success, with no lower bound on its probability. Rates/intersections transfer to completed printed fields by PC. The exact branch is excluded. PoolZ's remark inherits data-fixed conditioning and S5. |

## D71 — interpretive-sentence inventory

This inventory covers substantive readings in the reader statements, remarks, assumption explanations and card rows, including the adopted abstract paraphrases. Adjacent clauses are grouped only when the same source supports each. Literal assumptions/displays are checked above; status quotations are checked below. Update logs, placement recommendations and workflow notes are editorial. Empirical observations are identified explicitly and are not treated as theorem consequences.

| location and interpretive sentence(s) / clause(s) | judgment and support |
|---|---|
| RV:116-122: consequent HPM/MPM recovery, uniform PIP error, noise-only expectation and divergence-dependent onset | SUPPORTED — POST2:C :83-94; POST :80-85. |
| RV:133-140: weakening A5 to OS/DG; margin replaces off-truth A4 and beta-min; containment above c1 and coexistence below | SUPPORTED — POST2 :35-48,54-56,126-137. |
| RV:140-144: sensitivity/specificity rate; no strict-superset mass and strong-coordinate inclusion without beta-min; possible specificity failure | SUPPORTED — POST :84-94; counterexample is expressly numerical. |
| RV:145-147: coefficient bound supplies energy; large-model posterior mass vanishes without a design floor | SUPPORTED — POST :52-58; R1 B1.1/B1.3. |
| RV:148-152: all-design obstruction with the restored size domain; logarithmic factor on witnesses only; general expectation lower bound open | SUPPORTED — PSHARP :92-104; PSHARP-R :74-84,104-128. |
| RV:153-155: D-17 moderate-n mass on truth and one-variable supersets; no general finite-n statement | SUPPORTED as an explicitly attributed empirical observation/non-claim. It is not inferred from the masters; the external measurement is not independently revalidated here. |
| RV:158-161: Gaussian proof mechanism; polynomial model counting; fixed sparsity and necessary sparsity consequences on the stated domain | SUPPORTED — POST :63-100; PSHARP :98-104. No necessity of Gaussianity/polynomial p is asserted. |
| RV:162-174: energy, floors, Occam penalty and beta-min proof roles; numerical/heuristic necessity and open improvements | SUPPORTED with those labels — POST :52-58,68-94; POST2 :46-48,126-137. The unnormalised A5 floor indeed vanishes on the correlation scale. |
| RV:277-289: no upper eigenvalue bound, slowly vanishing floor possible, fixed signals exceed detection scale, sample transfer and unclaimed sub-Gaussian extension | SUPPORTED — APP :23-33,49-57,71-84. |
| RV:349-352: optimality under the upper theorem's assumptions, expectation lower bound for every admissible p on witnesses, only n^-1/2 on general designs | SUPPORTED — PSHARP-R :74-84; PSHARP :92-104; B3.8. “Every p” keeps s0<p from part (b). |
| RV:355-366: sparsity consequences within the stated domain; expectation exactness on fully orthogonal designs; probability exactness on named growing-p witnesses | SUPPORTED — PSHARP :71-88,98-104; PSHARP-R :74-84; B3.8. |
| RV:368-369: bounded-p expectation logarithm is a tail effect, not a competitor-count effect | SUPPORTED — PSHARP-R :104-114. |
| RV:371-378: growing-sparsity expectation obstruction and orthogonal critical-scale bound | SUPPORTED — PSHARP-R :86-100. For the latter, p→∞, s0/p→0 and the critical scaling ensure eventual feasibility and many null columns. |
| RV:380-393: open general-design/small-log-p/Gaussian expectation questions; deterministic superset-odds mechanism, witness fit factors and energy bounds | SUPPORTED — PSHARP :34-44,48-60,79-88,92-104; PSHARP-R :104-128. The probability reading is not promoted to a bounded-p logarithmic rate. |
| RV:466-474: omitted Gaussian and linear-plus-Gaussian examples, including Moore–Penrose extension | SUPPORTED — MISR-R :80-86. |
| RV:475-483: conditional law is the KL projection; best candidate support; centred Hellinger/KL contraction; selection-only/uniform fixed-design forms | SUPPORTED — MISR-R :96-155; MISR :110-114. “Best” refers to the conditional candidate law, not the full truth. |
| RV:484-501: separate theorem routes; contrast residual sufficiency and Gaussian-noise necessity; Gaussian rows only for transfer; scale invariance | SUPPORTED — MISR-R :56-74,96-107; MISR :36-58. The possible implication between theorem settings remains a non-claim. |
| RV:596-603: optimal start exponent up to sqrt(log n), deterministic floor, leakage-lattice interpretation | SUPPORTED — START :241-243; START2-R :226-237. |
| RV:606-619: block well-posedness, visibility threshold, reference-set union count, truncated-envelope mechanism and zero-correlation improvement | SUPPORTED — START :160-167,232-243; START2-R :51-86,217-245. Numerical/open necessity remains labelled; the threshold is an asymptotic proof reading. |
| RV:636-643: A6 does not replace A5, localisation is separate, and the result concerns an internal start object | SUPPORTED — START2-R :70-86,226-239. The placement advice is editorial. |
| RV:694-695,842: two code ceilings, sufficient domain D, idealisation for all n, guard stops without estimates | SUPPORTED — RM2-R :80-93,144-148; code `v3_run.R:95-98,143-148`, `cpp/v3_core.cpp:473-480`. Approximate billion-variable thresholds and “feasible” are engineering descriptions, not extra mathematical guarantees. |
| RV:697-704: mode/search error reading, deletion-only descent/certification/cap, polylog special case, examples | SUPPORTED — RM2-R :126-142,166-181; RM2 :236-240. Example names carry qualifications and do not alone discharge reader A6. |
| RV:707-719: fixed signals supply posterior/removal; visibility admits truths; Q confines extras; b threshold heuristic; locality/floor/width roles | SUPPORTED — RM2 :174-202,223-234,254-257; RM2-R :166-181. “Never” in these explanations is read on the theorem's high-probability event, not as a finite-n certainty. The b-threshold extrapolation is explicitly heuristic/open. |
| RV:762-771: local-regression l1 bound supplies a variance ratio; polylog bounded-L alternative is given up | SUPPORTED — R2 re-derived above; RM :154-156; RM2 :201-202. |
| RV:775-780: population assumptions mean visibility, confined imitation and local regressions; proposed abstract wording | SUPPORTED — RM2 :172-202. This is a qualitative summary with the complete conditions retained in the theorem. |
| RV:844-850: explicit sufficient constants and posterior-mode/search error split | SUPPORTED — RM2-R :101-112,135-140. The replacement in :845-846 is the master's additive BM-Q-flat condition, not a claim that every constant C_Q works. |
| RV:853-863: visibility/start inclusion, bounded leakage, deletion of extras, no-addition through small Q or local regression, well-posed floors | SUPPORTED in the asymptotic/event sense — RM2-R :166-175; RM2 :128-168,231-234. Case (b)'s separate signal clause is retained in the theorem and card. |
| RV:889-899: sample-level scope, masking, search-route limitation, population analogue and example status qualifications | SUPPORTED — RM2 :126-168,259-275; RM2-R :166-181. Theorem 6 is an alternative sufficient population statement; no equivalence of complete hypothesis classes is asserted. |
| RV:936-943: certified means public flag; polynomial-p specialisation; no start/leakage/block/visibility condition; weaker directional floor exists | SUPPORTED — SCR :31-47,69-75,158-163. |
| RV:946-952: adopted screening abstract with fixed constants, cap and intersection event | SUPPORTED — SCR :158-163. It asserts no probability of producing/certifying a small model. |
| RV:957-970: noiseless gain definition, some missing truth achieves Gamma, no p/s0/start/leakage/null-collinearity restriction, finite-n companion | SUPPORTED — SCR :51-60,79-90. The exact Q decrement factor is now correct. |
| RV:974-979: directional floor suffices, fixed constants are essential to this version, separate varying-signal result, union-bound role | SUPPORTED — SCR :69-75,150-168. |
| RV:992-999: intersection rather than conditional guarantee; certification frequency not proved; screening is one-sided rather than exact recovery | SUPPORTED — SCR :80-90,217-222. |
| RV:1001-1009: measured certification/support frequencies and sample-size illustration | Explicitly empirical, not a theorem consequence; external measurements NOT-EXAMINED. They cannot supply a missing theoretical premise. |
| RV:1047-1068: original/retained dimension, exceptional inputs, sample-mean intercept, x-law not estimated, Hellinger averaged over a fresh x | SUPPORTED — DIST :42-52,136-156. |
| RV:1075-1095: window size, no beta-min/fixed eigenvalue lower bound, possible near-collinearity | SUPPORTED — DIST :164-183. |
| RV:1104-1121: probability reading, contraction rate, common exceptional set, uniformity, size rather than identity, fallback without A4 | SUPPORTED — DIST :185-202. Size concentration is not a deterministic support-size cutoff. |
| RV:1131-1149: completed sampler/list description, hypothetical conditional mixture, list-mass premise, retained high-posterior truth and lack of list-mass certification | SUPPORTED — DIST :217-238,273-287; code `cpp/v3_ledger.h:78-112`. No sampler draws or posterior-mass certificate are invented. |
| RV:1151-1161: Gaussian/independent examples; exact-posterior versus delivery premises; selection yields the parametric result | SUPPORTED — DIST :100-108,204-238. |
| RV:1164-1171: adopted fixed-level distribution abstract | SUPPORTED — DIST :174-202. It retains the hypotheses and fixed-M meaning. |
| RV:1175-1206: Song–Liang distance, prior/rate/dimension/sparsity comparisons, exponential-form distinction and incomparability | SUPPORTED — current-result portions: DIST :50-52,74-108,128-238; external comparison checked against the published primary paper, as recorded below. Interface energy/cost constants are explicitly held fixed for the sparsity discussion. |
| RV:1209-1220: scale invariance and proof roles of dimension, tails, geometry, bounded signal and detectability | SUPPORTED — DIST :54-108,174-215; code preprocessing/score. No unproved necessity is promoted. |
| RV:1282-1286: no-leakage regime, exclusion of fixed null-truth leakage, alternative reported-model route under its own conditions, evidence needs no design condition | SUPPORTED — START2-R :70-77; RM2-R :177-181; N1 :86-104. Evidence is read with S5's potential convention. |
| RV:1288-1310: sampler branch, potential/printed equality, rho_n≤n^-c eventually, intersections rather than conditioning, exact branch exclusion, unbiased potential evidence and guard qualification | SUPPORTED — SAMP :29-58,90-95,158-163; N1 :86-104; PoolZ. Elementary exponent comparison supplies rho_n≤n^-c. |
| RV:1313-1319: posterior/start supply vanishing mass to transport, T-free evidence consistency, overlap alternative, idealised sampler premises | SUPPORTED — SAMP :153-177; R4. The moderate-n parenthesis is now explicitly an observation. |
| RV:1339-1345: no calibration-success lower bound; additional delivery link; no-leakage scope; start-controlled rate; unchecked assemblies | SUPPORTED — SAMP :158-186; RM2-R :144-148; R4. Exact wording of the rate-ratio comparison is an editorial suggestion E2. |
| Card:52 / row 1.1: expectation uniformity, HPM/MPM/PIP consequences, margin variant and A5 retained | SUPPORTED — POST2 :83-94,126-137; R1. Its abstract is the O_P form; status conditions are retained. |
| Card:53 / row 1.2: “same” under Gaussian rows, no upper eigenvalue bound, p≫n | SUPPORTED — APP :23-33,71-84. The row explicitly states probability conclusions, not an expectation rate. |
| Card:54 / row 1.3: witness optimality, every-design size-domain obstruction and sparsity frontier | SUPPORTED — PSHARP :71-104; PSHARP-R :74-92; B3.8. |
| Card:55 / row 1.4: best-candidate support, variance-uniform fixed-design rate and Gaussian-row result | SUPPORTED — MISR :110-123; MISR-R :96-130. The best-candidate interpretation keeps the stated linear-Gaussian law. |
| Card:61 / row 2.1: conditional-law target, level-M exceptional probabilities, model-size concentration, fallback, parametric rate, conditional list result | SUPPORTED — DIST :185-238. Neither deterministic size truncation nor sufficient list mass on every run is asserted. |
| Card:62 / row 2.2: centred in-sample Hellinger oracle and no-beta-min forms, with energy/truth floor/OS premises | SUPPORTED — POST2 :99-123. Squared-distance and distance rates are distinguished. |
| Card:68 / row 3.1: common good event and every-seed recovery; extra delivery assumptions; error split and ceiling/guard explanation | SUPPORTED — RM2-R :126-148,177-181; code pins above. Novelty is limited to “known to us”; no exhaustive novelty theorem is asserted. R3's stale final-column label is E1. |
| Card:69 / row 3.2: two Q alternatives with different beta-min scales; delivery as row 3.1 | SUPPORTED — RM2-R :101-112,166-175; RM2 :128-168,231-234. The R1 missing case-(b) signal premise is repaired. |
| Card:70 / row 3.3: start/lattice mass with probability tending to one; uncorrelated-null sharpening; exponent optimality | SUPPORTED — START2-R :226-245; START :241-243. Probability qualification is now explicit. |
| Card:72 / row 3.5: unbiased potential mean given calibration/data; equality with printed field on completion; no completion-conditioned identity | SUPPORTED — N1 :86-104; SAMP:PC :90-95; PoolZ. Classical SMC attribution is background. |
| Card:73 / row 3.6: localised rates and intersections; completed-field equality; particular AR/block designs only under Theorem 6's conditions | SUPPORTED — SAMP :90-95,158-163; R4; RM2-R :177-181. The family-wide implication from R1 is removed. “Every number” in the benefits cell is a summary of the named inferential outputs, not a theorem about arbitrary diagnostics. |
| Card:74 / row 3.7: fixed-constant certified intersection and assumptions potentially holding outside the search route | SUPPORTED — SCR :31-47,158-163,217-222. It does not promise certification, exact support, or coverage of every strong-factor design. |
| Card:80 / row 4.1: pooled PIP error bounded by worst island; pooled potential evidence identity; no unbiasedness conditional on completion | SUPPORTED — SAMP:LT# :134-138; PoolZ under its calibration-success convention. |
| Card:81 / row 4.2: an output-identical engine inherits output guarantees | SUPPORTED as a logical implication assuming identity. The tested identity itself is empirical and NOT-EXAMINED; the unfinished note is not presented as a theorem. |
| Card:82,88-90 / rows 4.3,5.1–5.3: census, simulation, strong-factor and scaling observations/plans | Explicitly empirical/open/planned; external measurements NOT-EXAMINED. No theorem support is drawn from them. |
| Card:97-126: adopted Form A and abstract/body paraphrases, screening/distribution placements and printed-output restriction | SUPPORTED by the corresponding master mappings above. In-force Form A keeps the expectation/variant conditions in the body; recovery abstract excludes unconditional delivery. Unused Form B is outside review. |
| Card:129-135,149-158: open questions, remaining conditional inputs and excluded example routes | SUPPORTED as stated limits/status descriptions — POST2 :35-48,126-137; PSHARP-R :104-128; SCR :217-222; registry statuses. |
| Card:159-164: D-17 moderate-n shape and output mass | SUPPORTED as an explicitly attributed empirical observation, not a master implication; the external measurement remains NOT-EXAMINED. No finite-n guarantee follows. |

For the literature passages, I consulted the [published Song–Liang paper](https://doi.org/10.1111/rssb.12095), pp. 950–957 and §3.2. Its prior, contraction conditions/rates, screening, supplementary MAP discussion, misspecification and SAMC discussion support the scoped comparisons. The current-result side of those comparisons was checked against the frozen masters. No broad claim that all competing literature lacks an output theorem was proved or needed.

## R1 repair audit

All material findings from both seats are resolved: the lower-bound domain is restored; card case (b) carries its own signal scale; evidence wording preserves potential/completed distinctions; R3 has a precise former-hypothesis antecedent; D-17 is empirical; prior/Occam attribution, pilot forced steps, fallback order, initial evidence factor, ledger scope and preflight stops match the code; the AR/block sentence makes no family-level claim; the frozen F-UNI cap is described correctly; start probability qualifiers and screening benefits are narrowed; Theorem 7's population analogue no longer asserts equivalence; BM-Q-flat and the exact ridge gain are stated accurately; example statuses and active delivery identities are carried. E1 concerns residual historical labels, not recurrence of the old R3 antecedent defect.

## Status and citation audit

I read the frozen registry's status column for the cited posterior/refinement, APP, sharpness, misspecification, START2-R, RM/RM2/RM2-R, SAMP, screening, distribution, N1, F-UNI, root and delivery-audit entries. Current quotations agree under the declared ellipsis convention. In particular:

- T03-sharp's checked root is distinguished from the unchanged older W3-POST:Thm-1 label; the expectation/variant routes preserve POST2:C/E/A1 conditions and the author-only Prop-LB/L1a′ inputs.
- MISR and MISR-R retain their POST2 and C-MIS conditions; D's conditional status is not silently upgraded.
- RM2-R's plus/core/delivery rows retain both code-reading audit conditions, with the audits labelled AUDITED rather than proved.
- SAMP and APP have the recorded checked versions; START/KERNEL remain named sampler idealisations with their inherited qualifications. New reader bridges and PoolZ remain author-only in the deliverable.
- The historical F-UNI source actually states the shipped larger cap, amended allocation and two-ceiling narrowing. Its old proof-file status header is honestly noted separately from the registry status.

The active cited master/bridge line ranges contain the claimed assumptions and conclusions. Approximate historical source references and stale historical labels do not change the active proof. No excluded audit record was used to discharge a condition. Empirical sources excluded from this review remain observations rather than checked theorem inputs.

## Gates

| gate | decision | reason |
|---|---|---|
| G1 correctness | PASS | PoolZ and R1–R4 re-derived; R3 accepted only with its repaired historical antecedent. |
| G2 hypotheses used = stated | PASS | Current posterior, search, delivery and sampler routes receive their required hypotheses via the listed bridges and S1–S5; operational premises are carried explicitly. |
| G3 faithfulness / F | PASS | All reader conclusions, substantive readings and card summaries preserve the masters' quantifiers, branch, events, probability/expectation distinction and conditional-input scope. |
| G4 statuses and citations | PASS | Current registry qualifications and active source ranges agree; no unchecked proof or code-reading audit is promoted to checked status. |
| G5 finite-n and scope | PASS | The universal lower-bound domain is retained; witness exactness remains witness-specific; screening constants stay fixed; D-17 and experiment frequencies are empirical; no completion-selected unbiasedness is asserted. |
| G6 code fidelity | PASS | Prior/score, preprocessing, start law, calibration/fallback, initial evidence factor, searches, equal pooling, offered-ledger model and completed/stopped outputs agree with the frozen pins under the stated idealisations. |

The score reflects C/S/F only. The two editorial suggestions are nonblocking.

FIDELITY: FAITHFUL

COUNCIL-VERDICT round=R2 manifest=3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b seat=sol score=9.3 gates=PASS
