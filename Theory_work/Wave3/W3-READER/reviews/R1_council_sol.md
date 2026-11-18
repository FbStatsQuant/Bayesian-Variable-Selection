# R1 council review — sol

Freeze reviewed: MANIFEST `759a7dfd87ef7b958a0c8140b6cfa0158f4159cac31c62cf3cb0f1a75fdd7e09`.
The required verification command printed `verify: OK` for this exact manifest before the review. I read no earlier W3-READER review, disposition, checkpoint, log, forbidden gate/audit file, staged delta, helper, or ticket tool. No subagents were used. Only this review and files under `.rc_tmp/R1_scratch_sol/` were created.

Overall score: **7.4/10.0**. **Do not accept as is.** The main displayed statistical conclusions largely match their masters. The blocking defects are scope inflation in explanatory statements/card summaries, a stale bridge derivation, and inaccurate code descriptions. They are repairable without changing the main theorem displays. Editorial findings do not affect the score.

## Per-claim decisions

The RV decisions include the associated interpretation and card row, as required by D71; an ACCEPT of a displayed formula alone would not excuse a stronger accompanying reading. R3 is assessed as the currently stated claim targeting the current Theorems 6–7, even though it is labelled historical.

| id | decision |
|---|---|
| W3-READER:PoolZ | ACCEPT |
| W3-READER:R1 | ACCEPT |
| W3-READER:R2 | ACCEPT |
| W3-READER:R3 | REJECT |
| W3-READER:R4 | ACCEPT |
| RV/thm1 | REJECT |
| RV/thm1′ | ACCEPT |
| RV/thm2 | ACCEPT |
| RV/thm3 | ACCEPT |
| RV/thm4 | ACCEPT |
| RV/thm5 | ACCEPT |
| RV/thm6 | REJECT |
| RV/thm7 | REJECT |
| RV/thm8 | ACCEPT |
| RV/thm8′ | ACCEPT |
| RV/thm9 | ACCEPT |
| RV/thm9B | ACCEPT |
| RV/thm9C | ACCEPT |
| RV/thm10 | REJECT |

The rejections of RV/thm6, RV/thm7 and RV/thm10 do **not** identify an error in their main displayed statistical conclusions: see the specific card/provenance/interpretation findings below.

## Findings and exact corrections

### S1 — major — the universal lower-bound reading drops its domain

**Location:** `READER_VERSIONS.md:148` (“on every design the posterior miss is at least of order n^{-1/2}”) and `:161-162` (“on every design … forces …”).

Theorem 1 permits `p=s0`, including a fixed full true model. There is then no strict superset, and neither cited obstruction applies. `W3-PSHARP/STATEMENT.md:92-104` requires `s0<=K-1`; its growing-sparsity consequences additionally use `s0<=p/2`. The simpler LB master explicitly requires `1<=s0<p` and `s0+1<=K` (`W3-POST/lemmas/LB_rate_lower_bound.md:10-16`). Indeed, its own header flags the `p=s0` domain counterexample (`:6`).

For example, take `p=s0=2`, centred orthogonal columns, fixed nonzero coefficients and fixed Gaussian noise. These satisfy Theorem 1's assumptions eventually, but all competing models underfit. The log posterior odds of each underfit against the truth are `-c n+O_P(sqrt(n)+log(n))` with `c>0`; the miss is exponentially small in probability. My independent four-model enumeration gives median log misses about -29.3, -96.7 and -333.5 at n=100,300,1000. The numbers corroborate the analytic domain issue; they are not used as a proof.

**Exact correction:** replace the first sentence by “For true models with `s0<=min(K-1,p/2)`, on every standardised design the posterior miss is at least of order `n^{-1/2}` (Theorem 3(a)).” Add the same domain before the growing-sparsity implications in `:161-162`. Alternatively use LB's less restrictive domain for the fixed-s0 lower bound and retain PSHARP's domain for the sparsity consequences. Do not impose a new restriction on Theorem 1 merely to rescue its remark.

### S2 — major — card row 3.2 omits the stronger signal requirement in case (b)

**Location:** `CLAIMS_CARD.md:66`.

The row advertises the same conclusion with beta-min at the standard `sigma sqrt(log(n)/n)` scale and either logarithmic Q or polynomial Q plus local regressions. Its second alternative omits the separate signal clause of `READER_VERSIONS.md:825-826`:

`theta_min^2 >= C_Q sigma_*^2 (|Q|+log n)/(n phi0^2)`.

For genuinely polynomial Q this is stronger than the advertised standard scale. Local regressions alone do not supply the missing truth-removal assumption of the master. Compare `W3-RM2-R/STATEMENT.md:107-112,166-174` (BM-W+ and its BM-Q-flat sufficient form). The displayed reader Theorem 7 itself carries this condition correctly.

**Exact correction:** after “`|Q|<=n^b` plus local regressions”, add “and beta-min at `sigma_* sqrt((|Q|+log n)/(n phi0^2))` with a sufficiently large fixed constant, as in Theorem 7(A5)(b)”. State that the standard `sqrt(log(n)/n)` scale applies to case (a).

### F1 — major — potential-run unbiasedness is promoted to printed-output unbiasedness

**Location:** `CLAIMS_CARD.md:69` (“and hence the printed … Zhat”), with the same ambiguity at `:77` and `METHOD_INTUITION.md:122` (“printed … consistent / unbiased”).

N1 proves the identity for the **potential uninterrupted** records, localized to calibration success. It explicitly makes no statement conditional on completion (`W1-N1/STATEMENT.md:86-88,98-104,118`). PC identifies records on completed runs; that pointwise equality does not preserve an expectation after selecting completed runs (`W3-SAMP/STATEMENT.md:90-95`). For a simple illustration, an unbiased positive variable taking 0.5 and 1.5 equally often ceases to be unbiased when completion selects only its 0.5 realizations. No assertion that this particular two-point example is the production SMC law is needed: the proposed inference from PC is invalid, and N1 expressly excludes it.

PoolZ itself **passes**: `STATEMENT.md:24-32,36-37` correctly proves the potential identity and explains the completed-record comparison. The card must preserve that scope. Theorem 10's main intersection statements also preserve it correctly.

**Exact correction for row 3.5:** “On calibration success, given the frozen calibration and data, the equal-weight mean of the four potential uninterrupted evidence records has expectation Z. On completed runs this quantity equals the printed evidence. No unbiasedness conditional on completion is asserted.” Use the same potential-record qualification in row 4.1 and the method table. Do not replace this with an assertion that `E[1_completed Zhat]=P(completed)Z`.

### F2 — major — R3's current target is not proved by its old-master substitutions

**Location:** `lemmas/R3_delivery_assembly.md:10-13,28-29,48-52`; `REPORT.md:34-38`.

The target says “under the hypotheses of Theorem … 7”, but the premise table supplies the lattice/posterior interfaces by invoking the old `W3-RM2:RM2-F`. The current Theorem 7 allows fixed beta-min and fixed visibility constants (`READER_VERSIONS.md:813-818`), whereas RM2-F requires BM-infinity, diverging visibility, and BM-W (`W3-RM2/STATEMENT.md:128-139,206-207`). The new assumptions do not imply those old hypotheses. The historical label at R3:15-16 explains why this happened but does not repair a registered claim still stated with the current theorem as its antecedent. In particular, the old implication edge cannot be justified by merely calling the old result an input.

The repair is available: RM2-F-plus supplies exactly [SAND], [NA], [TL], [POST] at the constant level (`W3-RM2-R/STATEMENT.md:166-174`; `lemmas/Q6_assembly.md:18-38`). The current reader Theorem 7 uses that route correctly.

**Exact correction:** rewrite R3 as the current assembly: use RM2-F-plus/RM2-R-plus for the statistical interfaces, verify the current (S4) against (D), and invoke DLV-0 for delivery, with the two audit conditions carried. Update its REPORT dependency/conclusion block. A smaller valid alternative is to restrict the old R3 target explicitly to the former BM-infinity/diverging-visibility reader hypotheses, rename it a historical lemma, and cease listing it as a bridge needed for current Theorem 7. Replace references to nonexistent current “(S4)(v)” by “(S4)(i), IDEAL-W+”.

### F3 — major — the moderate-n posterior-shape reading is unsupported at its stated scope

**Location:** `READER_VERSIONS.md:153-156,1306-1307`; `CLAIMS_CARD.md:156-160`; repeated in `METHOD_INTUITION.md:107-110,143-145`.

These sentences assert a generic moderate-n description: posterior miss is carried mainly by one-variable supersets, whose combined mass is comparable to the truth, and the coded output has that shape. The masters provide asymptotic upper bounds, deterministic superset lower bounds and witness-design asymptotics; none establishes this description for the designs/data allowed by the reader theorems at moderate n. Even the existence of a null variable is not assumed in Theorem 1 (S1). A typical-regime empirical observation cannot become a uniform or generic finite-n theorem reading by being placed next to an asymptotic result. The untracked Engineering measurement cited in the card is identified as such, but the reader statement does not qualify the assertion by that measured setting.

**Exact correction:** move this to an explicitly empirical paragraph: “In the Engineering configurations measured in [specified experiment/provenance], substantial mass was observed on the truth and its one-variable supersets. No general finite-n posterior-shape or output-accuracy statement is proved here.” Remove “Theorem 1, remark (vii)” as theoretical support in Theorem 10's explanation. If giving the witness mechanism, use an **exponentiated** chi-square fit factor rather than an unexplained “chi-square factor”, and state its design/asymptotic scope.

### F4 — minor — several asserted code facts are inaccurate

**Locations and exact corrections:**

1. `METHOD_INTUITION.md:51-53`: the model prior alone does not charge the additional `0.5 log n`. Its exact log cost is `log((2p-1-k)/(k+1))`, from `cpp/v3_score.h:64-70`. Replace by “the beta-binomial model prior charges about `log(2p/(k+1))`; for a well-conditioned added direction, the marginal likelihood contributes an additional Occam cost about `0.5 log n`.”
2. `METHOD_INTUITION.md:76`: “each step keeps an effective sample size of 90%” ignores the forced pilot step floor. `cpp/v3_calib.h:25-44` explicitly replaces the ESS-selected step when it is smaller than `1/T_e`. Replace by “pilot steps target ESS at least 90%, except for recorded forced minimum steps; candidate-grid steps are checked against the restricted ESS criterion.”
3. `METHOD_INTUITION.md:78`: fallback uses the **last successful candidate construction** when available, otherwise the completed pilot schedule (`v3_calib.R:120-124,163-170`). Replace the categorical “pilot's own ladder … always proceeds” by that order and qualify continuation by absence of other stops and sufficient allocation.
4. `METHOD_INTUITION.md:91`: the product of incremental mean weights is missing its initial normalizer. The code initializes `logZ=log m(empty)+log Zbar0` (`cpp/v3_engine.h:299`), then adds increments (`:316-322`). Replace by “each island multiplies `m(empty) Zbar0` by the average reweighting factors; Zhat is the equal-weight mean of those four products.”
5. `NOTATION.md:121-122` and `METHOD_INTUITION.md:104-105`: “every model the run scores” / “every model scored anywhere” is broader than the coded statistical score-event set. The preflight timing routine scores models without a ledger (`cpp/v3_core.cpp:124-137`, called through `v3_fit.R:108-115`). Replace with “the best model among those offered to the run's statistical ledger, including the block tables, retained calibration models, particle/proposal score events and both local searches.” This matches SAMP:PC (`W3-SAMP/STATEMENT.md:93-95`) and the already careful Corollary 9C wording.
6. `METHOD_INTUITION.md:111`: preflight resource rejection can return before any statistical ledger/HPM exists (`v3_fit.R:115-118`). Replace by “On a resource stop, estimates are unavailable; the best recorded model is returned when such a record exists.”

These are factual corrections, not requests for new algorithmic guarantees or additional testing.

### F5 — minor — a family name does not discharge Theorem 6's conditions

**Location:** `CLAIMS_CARD.md:70`, “under its own conditions, which AR and block designs meet”.

The first qualification is correct; the appended blanket assertion is not. For example, one block of size p=n with fixed equicorrelation rho=1/2, one true predictor and all other predictors null has a positive population eigenvalue floor. But every null has covariance 1/2 with the truth already at U=empty. Theorem 6(A4)(i) therefore forces Q to contain all p variables, violating `|Q|<=n^b`, b<1/2. “Block designs” includes designs outside the theorem. Visibility can also fail for particular signal configurations.

**Exact correction:** delete “which AR and block designs meet”. Write “For particular AR or block designs that satisfy Theorem 6's visibility, leakage, floor and local-regression conditions, row 3.1 still gives the reported-model result.” No family-wide assertion is needed.

### F6 — minor — the frozen F-UNI source is misdescribed

**Location:** `READER_VERSIONS.md:743-745`; `CLAIMS_CARD.md:65` (“Prop-F/F-UNI used LS0 cap ell_n”).

The frozen `W2-UNI/lemmas/L5_delivery.md:8-12` explicitly uses the shipped cap `ell_n+|start mode|` and the amended score-count/allocation envelope. Its `:41-48` narrowing also explicitly addresses the shipped validators and allocation. The original C-DLV Prop-F cap is ell_n (`C-DLV/STATEMENT.md:32`), but the current frozen F-UNI statement is not the same claim with that cap. The combined historical sentence is therefore not faithful to the cited frozen source. Choosing DLV-0 as the active route is legitimate and does not require this false description of the alternative.

**Exact correction:** “The original C-DLV Prop-F configuration used cap ell_n. The frozen F-UNI@2.1.0 states the enlarged cap and amended allocation. The active reader delivery route here is RM2-R's DLV-0, whose shipped-code audit and conditions are carried explicitly.” If asserting something about a former F-UNI version, give its precise version and source rather than attributing it to the frozen version.

### E1 — minor — clean up stale carriers and line numbers

`R3_delivery_assembly.md:11,34,50` and `R4_printed_outputs.md:49` retain old split references to (S4)(v), although the current convention folds IDEAL-W+ into (S4)(i). R3's V/S/P source-line cells also lag the frozen F-UNI source by one or two lines: V is :15, S :16, P :17. `READER_VERSIONS.md:1370` still calls the superseded R3 route the main delivery bridge; update it together with F2. `CLAIMS_CARD.md:32-38` says **every** row has fixed variance/Gaussian-row alternatives, while rows 1.4 and 2.1 explicitly allow varying variance, and 2.1 has sub-Gaussian rows. Add the explicit exceptions rather than leaving a contradictory global setup.

### E2 — minor — specify the ridge gain exactly in Theorem 8′

At `READER_VERSIONS.md:949-952`, give the formula `gamma(t|S)=(x_t' R_S mu)^2/(x_t' R_S x_t+1/(n+1))`, with `R_S=I-X_S(G_S+I/(n+1))^{-1}X_S'`. The master has `gamma=((n+1)/n)(Q_S^mu-Q_{S+t}^mu)` (`W3-SCR/STATEMENT.md:51-56`), so describing it only as the decrease of “the method's … quadratic form” is ambiguous between R_S and the Q actually defined in NOTATION. The current asymptotic sufficient condition is not strengthened by using the smaller Q decrement, but the alleged identity bridge deserves an exact definition.

## Re-derivation of the new claims and headline implications

### PoolZ and R1–R4

- **PoolZ:** N1 with h=1 gives each conditional mean `E[Zhat_r/Z|C]=1` on A. Intersect the four full-measure sets and average. No island-to-island independence is used. Data are fixed for this identity; under the joint law condition on `(data,C)` first. A is measurable with respect to that conditioning field, so multiplication by its indicator and the tower property give the last identity. This does not use completion. The code's log-sum-exp minus log 4 is exactly the logarithm of the arithmetic mean. ACCEPT.
- **R1 B1.1:** triangle inequality gives `(n-1)s^2 theta_bar^2<=ns^2 theta_bar^2`. **B1.2:** `ceil((2A+1)s)+1<=(2A+1)s+2`. **B1.3:** `s+m#<=2s+1+(As+s/2+1)log(n)/log 2`; absorb `2s+1` into `(2s+1)log n`. The displayed positive coefficient difference proves the bound for real A>=1, not just the checked grid. **B2.1:** the identity `(1+d log 2)/log 3=d`, d=1/log(3/2), is exact. It yields `s+mbar<=d(As+1.5s+2)log n`, which is below the proposed floor range; the j0 branch is smaller too. **B4.1:** take the maximum of those branches. **B6.1:** the minimum A=s=1,n=3 already gives sufficient slack. **B3.2:** centred Gaussian null directions are independent uniform directions in the contrast sphere, independent of truth/noise; the polynomial bound gives both logarithmic restrictions. ACCEPT.
- **R2:** write `e_A=e_T+X_T d` (population analogue W_T d). Normal equations kill the cross term. Unit diagonal bounds the quadratic form by `||d||_1^2`. The conditional residual variance is at least the principal-block eigenvalue floor, by Schur complement/interlacing; the sample version has the same identity after dividing by n-1. Thus the multiplicative error is `L^2/c` or `L^2/phi0^2`. With L_n->0 it vanishes uniformly. ACCEPT.
- **R3:** union-bounding [SAND], [NA], [TL] and identifying [POST] with F-UNI(P) is valid. The delivery premises and enlarged-cap allocation can be supplied as assumptions. The failure is the current Theorem-7-to-old-RM2-F input step (F2), not the union bound. The direct replacement proof using plus masters is available but is not what the frozen registered lemma proves. REJECT pending the stated repair/scope restriction.
- **R4:** R1 supplies LSF and FL-R16. W2-APP explicitly covers deterministic standardized signals (`L1_POST.md:15-18`). Posterior miss tending to zero gives `o1<=2 delta` on an event of probability tending to one, hence the same O_P rate. START2-R IF-START gives localized `o0=O_P(n^{-1/2}exp(C_R sqrt(log n)))`. Increase C_R to a positive constant if necessary; this rate dominates `sqrt(log n/n)`, tends to zero, and is eventually decreasing (log derivative `-1/2+C_R/(2sqrt(log n))`). The maximum has that rate and SAMP(C-v) applies. PC transfers the fields to intersections with completion. ACCEPT.

Independent checks in `.rc_tmp/R1_scratch_sol/checks.py` passed **378** exact-ceiling configurations and **5,760** regression-identity/inequality cases (largest identity residual `5.6e-16`). These supplement the analytic derivations above. The toy script was read before running; its stdout reproduced `numerics/toy_example_out.txt` byte for byte, with output redirected into scratch. No production R build was needed for this mathematics/code-reading review.

### Reader-to-master checks

| statement | hypothesis and conclusion check |
|---|---|
| 1 | A3 gives E; A4 gives F0 and F-lambda through R1; A5 gives F-w; A6 is BM(c) with `c=C_beta^2 phi0^2`, or BM-infinity. POST2 C(i), :85-92, gives the design-uniform expectation bound and its envelope qualification. Markov and a union bound give the weaker displayed 4C HPM/MPM error bound. The deterministic PIP inequality is exact. Main displays pass; S1/F3 are accompanying overstatements. Form A's O_P route uses T03-sharp. Form B was not reviewed. |
| 1′ | A4′ is F0+ID; `L_S>=Delta_S` gives ID-M. A5 implies OS by A0, with constants depending only on the declared floors. POST2 E and C(iii), :128-133 and :85-92, give exactly the conclusions. It keeps A5 and does not claim design freedom. |
| 2 | R1's larger floor range supplies both LSF ranges. W2-APP POST(a),(b), :23-33, supplies common constants and the raw-coefficient event. POST item 6, :95-100, transfers the O_P/summary conclusions. The displayed conclusion does not claim a joint expectation rate. |
| 3(a) | PSHARP B, :92-104: the model-size domain is present, and `c(p,s)>=(s+1)/3` gives the stated deterministic inequality. |
| 3(b), remarks | R1 gives W-sph; all orthogonal nulls imply `p<=n-1+s0-rank(X_truth)<=2n` eventually, hence W-orth-E. Polynomial p supplies W-sph-E. AE A1-E, :74-84, gives the every-p expectation display; PSHARP A1, :71-73, gives the probability display only when p->infinity. Growing-s0 and critical-scale forms match AE :86-92 and A2C :94-100. Fully orthogonal fixed nonzero signals satisfy Theorem 1 with A=1, phi0=g0=1 eventually, providing its expectation upper half. No Gaussian-design expectation upper half is claimed. |
| 4 | A0 gives a Gaussian residual independent of the candidate design; one may take q=0 in CorGb-plus. R1 covers its floor range; A3 is the stronger divergent branch of its relative signal condition. CorGb-plus :96-107 gives both O(r_n) bounds. The Gaussian/pseudoinverse and linear-plus-noise examples are CorG-min(E1),(E2), :80-86. CorH-plus :112-130 and CorH-U :139-155 give precisely the centred in-sample Hellinger/KL and uniform-selection readings. |
| 5 | A3/A4/A5 give FL-R16, V-R and L-R++; the reference-set count and covariance conditions are carried. START-R :226-237 gives both the lattice probability bound and the no-leakage specialization. A6 implies L-gain-0 by the conditional covariance identity, giving its sharper rate. FLOOR's finite-n domain n>=4,s0<K is present. |
| 6 | R1 supplies T1-R and the small-set FL-R range; Q-union floors are explicit. A4 is exactly L-R^b plus feasibility and its 15rho+b budget. R2 gives the variance clause of D-loc^b; the declared population coefficient condition supplies the remainder. RM2's D-to-W gives W-R. RM2-R-plus :177-181 gives the common data event and, with (D), delivery/error split. Current S4 states the required machine/configuration/allocation premises. Main conclusion passes. |
| 7(a) | The revised beta-min constant includes c0, the truth-removal constant and `8(1+sqrt(D/2))^2`. With Q=O(log n), `d_n^2<=D log n` for fixed D>2+4A eventually. Thus BM-W+ holds. W-chi supplies W; choose a small positive polynomial exponent below beta(eta,A) to cover Q. V-flat and both floor ranges are explicit. RM2-F-plus applies. |
| 7(b) | The explicit additive signal bound in Remark (a) implies BM-Q-flat, hence BM-W+. R2.2 supplies W-loc's residual ratio, while `h+b<1/2` supplies the width budget. The constants and feasibility match RM2-F-plus. Delivery uses (D), not an unqualified resource claim. Main conclusion passes; the card must retain the stronger signal clause (S2). |
| 8 and placement (a) | Exactly SCR A1 :158-163, with the stronger full sparse floor. Fixed constants, q<K and the intersection event are all carried. The abstract repeats them. |
| 8′ | SCR A-infinity :87-90, with the same liminf margin and intersection conclusion. No growth in p or bounded support is used by that master. See E2 for the gain definition. The supplied brief's alternative b1 is not a second frozen statement here: this manifest adopts the plain body statement. |
| 9, 9B, 9C | After renaming raw/retained dimension and the sub-Gaussian constant, these are DIST Theorem A :185-207, Theorem B :209-215 and Corollary C :217-238. The fixed-level reordering retains the M<=sqrt(n)/log n condition, common n0/constants, same exceptional set and uniformity. The sample-mean intercept and conditional-Hellinger interpretation agree with DIST :42-52. The list-mass threshold, universal completed-run quantifier, exact-arithmetic premise and “not certified” qualification are retained. |
| 10 | R4 proves exactly SAMP(C-v)'s localized rates and intersections. The constant in rho can absorb the fixed number of fields/islands. No success-probability lower bound or conditioning on completion is introduced in the main theorem. PoolZ's body remark is read with S5's potential-run convention; its card promotion is F1. |

## D71 interpretive-sentence inventory

This inventory includes explanatory readings of conclusions in the reader sections (including remarks and condition explanations) and the theorem/card summaries. Literal numbered assumptions, displayed conclusions already checked above, status quotations, update logs and workflow instructions are not additional interpretive sentences. Multiple adjacent sentences with the same reading are identified together; every listed clause has its own judgment. `RV` means READER_VERSIONS; `Card` means CLAIMS_CARD. Sources below are paths under `Theory_work` unless a code path is given.

| location / interpretive sentence or clause | judgment and supporting master line(s) |
|---|---|
| RV:116-122, “consequently … HPM/MPM … PIPs”; noise-only expectation; envelope-dependent onset | SUPPORTED — POST2/STATEMENT:85-92; POST/STATEMENT:82-85. |
| RV:133-140, A5 can be weakened to an Occam condition/determinant growth; margin replaces A4 off truth and beta-min; containment only above c1 | SUPPORTED — POST2/STATEMENT:35-48,54-56,128-137. |
| RV:140-141, sensitivity and specificity uniformly in j at the rate | SUPPORTED — POST/STATEMENT:84-85 and POST2 C. |
| RV:142-144, without beta-min no strict-superset mass, strong-coordinate recovery, possible specificity failure | SUPPORTED with the numerical label retained — POST/STATEMENT:87-94. |
| RV:145-147, coefficient bound used through energy; large-model mass O_P(n^-1/2) without a design floor | SUPPORTED — POST/STATEMENT:52-58 and R1 B1.1/B1.3. |
| RV:148-152, every-design lower obstruction; witnesses attain the extra logarithm; expectation-vs-probability/open distinctions | First clause OVERSTATED (S1). Witness and open-scope clauses SUPPORTED — PSHARP/STATEMENT:71-88,92-104; PSHARP-R/STATEMENT:74-84,104-114. |
| RV:153-156, moderate-n mass mainly on one-variable supersets, jointly comparable to truth | UNSUPPORTED at generic finite-n scope (F3). |
| RV:159-160, Gaussian fluctuations and polynomial dimension enter the proof | SUPPORTED as sufficient proof mechanism — POST/STATEMENT:63-75,87-100. No necessity is proved. |
| RV:161-162, fixed sparsity close to necessary “on every design” | OVERSTATED without the size domain (S1). |
| RV:163-175, energy/anchored floors/Occam penalties and detection-scale explanations; claimed necessity based on numerics/heuristic, not a theorem | SUPPORTED as labelled proof-role/limits statements — POST/STATEMENT:52-58,68-75,87-94; POST2/STATEMENT:46-48,128-138. Assertions explicitly labelled numerical/open remain such, not accepted as mathematical necessity. |
| RV:277-289, no upper eigenvalue bound, fixed nonzero signals need no separate beta-min, population floors transfer, sub-Gaussian extension not claimed | SUPPORTED — W2-APP/lemmas/L1_POST:23-33,49-57,71-84. |
| RV:348-351, “rate … cannot be improved … for every p” on the stated null-column witnesses; every-design order only n^-1/2 | SUPPORTED within part (a)'s domain and s0<p in part (b) — PSHARP-R/STATEMENT:74-84; PSHARP/STATEMENT:92-104. |
| RV:354-365, sparsity implications under the stated size restriction; named expectation/probability exactness cases | SUPPORTED — PSHARP/STATEMENT:98-104; PSHARP-R/STATEMENT:74-84; orthogonal bridge B3.8 re-derived above. |
| RV:367-368, bounded-p logarithm comes from rare fit-factor tails | SUPPORTED — PSHARP-R/STATEMENT:104-114. |
| RV:370-377, growing-sparsity expectation obstruction; critical-scale e^-lambda | SUPPORTED — PSHARP-R/STATEMENT:86-100. The critical-scale condition implies feasibility eventually. |
| RV:379-384, general-design/log-small-p and Gaussian expectation upper bounds not settled | SUPPORTED as non-claims — PSHARP/STATEMENT:79-88,109; PSHARP-R/STATEMENT:104-128. |
| RV:387-392, deterministic mechanism; independent witness competitors/truncated factors; energy keeps scale | SUPPORTED on the specified witnesses — PSHARP/STATEMENT:34-42,48-60 and PSHARP-R/STATEMENT:104-114. |
| RV:464-472, omitted Gaussian and linear-plus-noise examples, including pseudoinverse | SUPPORTED — MISR-R/STATEMENT:80-86. |
| RV:473-475, conditional law is the KL projection; selection targets best candidate predictor's support | SUPPORTED for the stated conditional linear-Gaussian model/centred interpretation — MISR-R/STATEMENT:123-130; CorGb-plus:96-108. This does not identify the support with full-model truth. |
| RV:475-481, fitted mean/variance contraction, centred reference, fixed-design selection-only and uniform forms | SUPPORTED — MISR-R/STATEMENT:112-155; MISR/STATEMENT:110-114. |
| RV:482-484, distinct masters and no asserted implication between rows 2 and 4 | SUPPORTED as a non-claim — POST fixes variance; MISR-R permits varying parameters (:96-107). No impossibility of a new implication is asserted. |
| RV:487-499, contrast law sufficient/necessary under independent Gaussian noise; Gaussian rows for transfer; rescaling invariance | SUPPORTED — MISR-R/STATEMENT:56-74,96-107; MISR/STATEMENT:36-43,57-58. |
| RV:594-601, start exponent optimal up to sqrt(log n); leakage lattice reading | SUPPORTED with its finite-n/domain qualification — START/STATEMENT:241-243; START2-R/STATEMENT:226-237. |
| RV:604-617, block well-posedness/visibility, sharp threshold reading, reference-set counting, truncated-envelope mechanism, zero-correlation improvement | SUPPORTED as sufficient mechanisms/labelled open necessity — START2-R/STATEMENT:51-86,217-245 and START/STATEMENT:230-237. |
| RV:635-641, zero null-truth correlation alone does not replace localization; internal-object placement | SUPPORTED — START2-R/STATEMENT:70-86,234-239. Placement is editorial. |
| RV:691,838, code ceilings, sufficient bounded domain, idealization needed for every n | SUPPORTED with approximate “about” thresholds — RM2-R/STATEMENT:80-93; code v3_run.R:96 and cpp/v3_core.cpp:473-474. “No feasible problem size” is an engineering assessment, not a further mathematical guarantee. |
| RV:693-700, error terms = posterior-mode/search errors; deletion-only descent/cap; polylog special case; examples labelled unchecked where applicable | SUPPORTED — RM2-R/STATEMENT:126-142,166-181; RM2/STATEMENT:236-240. The family names alone are not verified hypotheses. |
| RV:703-715, fixed signals supply posterior/removal, visible truths enter start, Q captures extras, b threshold is heuristic, locality/floors/width proof roles | SUPPORTED as asymptotic proof explanations, with the stated heuristic/open qualifications — RM2/STATEMENT:174-202,223-234,254-257; RM2-R/STATEMENT:166-181. “Never” here must be read on the high-probability event, not as a new finite-n assertion. |
| RV:840-846, explicit sufficient constants; mode-error plus search-error split | SUPPORTED — RM2-R/STATEMENT:101-112,135-140; Q2_TL_c:64-72. |
| RV:849-859, visibility/leakage exclude missing truths/outside-Q start variables; small Q or local regression makes no-addition feasible; floors make regressions well posed | SUPPORTED in the theorem's asymptotic/event sense — RM2-R/STATEMENT:166-175; RM2/STATEMENT:128-168,231-234. Case (b) still needs its signal condition (S2 concerns the card). |
| RV:885-893, sample-level scope, masking, route condition, no theorem without it/b>=1/2 | SUPPORTED as a limit of the cited route — RM2/STATEMENT:33-45,126-168; no claim of mathematical impossibility outside the route is made. Example-specific numerical checks are not independently upgraded here. |
| RV:929, certified = flag; RV:933-936 and :939-945, polynomial-p specialization and absence of start/leakage/visibility assumptions | SUPPORTED — SCR/STATEMENT:31-47,158-163. |
| RV:949-952, verbal definition of gain and “every missing-truth model has some missing truth with gain >=Gamma” | SUPPORTED after choosing the master's exact gain; definition ambiguity E2 — SCR/STATEMENT:51-60. |
| RV:957-962, no p/support/start/leakage/null-collinearity restrictions beyond margin; finite-n companion | SUPPORTED — SCR/STATEMENT:79-90. |
| RV:966-971, weaker directional floor, fixed constants, different varying-signal result, union-bound proof role | SUPPORTED — SCR/STATEMENT:69-75,150-166. |
| RV:984-991, intersection not conditional guarantee; no certification-frequency theorem; one-sided not exact recovery | SUPPORTED — SCR/STATEMENT:80-90,217-222. |
| RV:993-1001, observed certification frequencies/sizes and illustrative required n | Empirical statements explicitly marked “not a theorem”; NOT-EXAMINED as external experiment results (the cited other-ticket review/measurement record is not a frozen master). They supply no support for mathematical conclusions in this review. |
| RV:1050-1059, fitted conditional law, x not estimated, Hellinger averaged over new x | SUPPORTED — DIST/STATEMENT:42-52. |
| RV:1070-1072, window is the jointly constrained range; RV:1085-1086, no beta-min/fixed eigenvalue floor | SUPPORTED — DIST/STATEMENT:164-183. |
| RV:1095-1106, probability reading, fixed-level rate, common exceptional set/uniformity, size not identity | SUPPORTED — DIST/STATEMENT:185-198. |
| RV:1108-1112, slower-radius and size fallback | SUPPORTED — DIST/STATEMENT:200-202. |
| RV:1122-1140, sampler/list description, exact conditional mixture, list mass sufficient, true scored high-mass model retained, no mass certificate | SUPPORTED — DIST/STATEMENT:217-238; SAMP/STATEMENT:90-95 and code ledger. |
| RV:1142-1152, examples, exact-posterior versus conditional sampler premises, selection removes logarithm | SUPPORTED — DIST/STATEMENT:204-238,100-108. |
| RV:1155-1162, abstract fixed-level restatement and body placement | SUPPORTED — DIST/STATEMENT:174-202. |
| RV:1166-1197, Song–Liang comparison, display (i) analogue, strengths/weaknesses/incomparability, (iii) exponent distinction | SUPPORTED as the stated comparison; current-result parts: DIST/STATEMENT:50-52,74-98,128-238. Original-paper clauses checked against the published paper, as noted below. Sparsity constants are expressly conditional on holding the interface energy/cost bounds fixed, not an unqualified uniform-in-s rate. |
| RV:1200-1211, scale invariance, proof roles of dimension/tails/geometric condition/bounded signal, detectable signal removes logarithm | SUPPORTED — DIST/STATEMENT:54-108,174-215; code score/preprocessing. Necessity not asserted. |
| RV:1273-1277, no-leakage coverage excludes fixed null-truth leakage; Theorem 6 only under own conditions; unbiasedness for every design | SUPPORTED for the first two clauses — START2-R/STATEMENT:70-77; RM2-R/STATEMENT:177-181. Evidence clause SUPPORTED only for potential records under S5/N1, not completion-selected printed fields (F1). |
| RV:1280-1295, potential fields vs printed fields, rho <=n^-c eventually, intersections not conditioning | SUPPORTED — SAMP/STATEMENT:29-58,90-95,158-163; elementary comparison of exponents. |
| RV:1297-1301, exact branch excluded; calibration-conditional evidence identity | SUPPORTED under S5 potential convention — N1/STATEMENT:86-104; PoolZ derivation above. |
| RV:1304-1310, posterior/start inputs, vanishing mass to transport independent of ladder length, overlap alternative | SUPPORTED — SAMP/STATEMENT:153-177; R4. The moderate-n parenthesis is UNSUPPORTED at generic scope (F3). |
| RV:1330-1335, no success probability claim, extra delivery link, narrower design scope, slower start-controlled rate and open assemblies | SUPPORTED — SAMP/STATEMENT:158-186; RM2-R/STATEMENT:144-148; R4. “Slower by a factor” is qualitative; exact rate ratio is `exp(C sqrt(log n))/sqrt(log n)`, not simply the exponential alone. |
| Card:49, row 1.1 results/variant and benefits | SUPPORTED — POST2/STATEMENT:85-92,128-138, with A5 retained. Literature comparison checked below. |
| Card:50, row 1.2 “same”, random rows, no upper floor bound, p>>n | SUPPORTED — W2-APP/lemmas/L1_POST:23-33,71-84. “Same” is explicitly followed by probability-only conclusions. |
| Card:51, row 1.3 optimality/witness/every-design obstruction and sparsity frontier | SUPPORTED within the displayed model-size domain — PSHARP/STATEMENT:71-104; PSHARP-R/STATEMENT:74-92. |
| Card:52, row 1.4 best candidate support/uniform residual variance and Gaussian reader | SUPPORTED with reader assumptions and conditions — MISR/STATEMENT:110-123; MISR-R/STATEMENT:96-130. |
| Card:58, row 2.1 conditional-law distance, fixed/variable level, size fallback, parametric rate and list consequence | SUPPORTED — DIST/STATEMENT:185-238. “Size <=” is a posterior concentration bound, not a deterministic cutoff; row 9's explicit displays retain this. |
| Card:59, row 2.2 centred in-sample distance and selection/no-margin alternatives | SUPPORTED — POST2/STATEMENT:101-119. |
| Card:65, row 3.1 common event, extra delivery premises, error split, code size ceilings | SUPPORTED — RM2-R/STATEMENT:126-148,177-181; inaccurate combined Prop-F/F-UNI history is F6. Novelty sentence is a bounded “known to us” literature assessment, not a proved exclusivity claim. |
| Card:66, row 3.2 fixed-design summary/standard signal scale with either Q alternative | OVERSTATED — omitted case-(b) signal clause (S2). |
| Card:67, row 3.3 start mass/lattice/exponent and uncorrelated-null sharpening; explains start | SUPPORTED — START2-R/STATEMENT:226-245; START/STATEMENT:241-243. |
| Card:69, row 3.5 island means “hence printed” unbiased | OVERSTATED — N1/STATEMENT:86-104,118 (F1). Classical SMC attribution is background, not a stronger new theorem. |
| Card:70, row 3.6 localized rates, intersection interpretation, on completion equality | SUPPORTED — SAMP/STATEMENT:90-95,158-163; R4. “AR and block designs meet” the other theorem is OVERSTATED (F5). |
| Card:71, row 3.7 certified intersection, fixed constants, no visibility/leakage/start/block assumptions | SUPPORTED — SCR/STATEMENT:31-47,158-163,217-222. It may cover examples outside the recovery route; it does not assert every strong-factor design satisfies its floor/budget. |
| Card:77, row 4.1 equal-weight error <=worst island and pooled identity | SUPPORTED for potential records — SAMP/STATEMENT:134-138; PoolZ. Add the F1 scope clarification. |
| Card:78, output-identical parallel engine inherits guarantees; tested byte identity | Logical inheritance SUPPORTED **if** output identity holds. The row explicitly labels the tested identity empirical and the note unfinished, not a general parallel-engine theorem. The external tests are NOT-EXAMINED. |
| Card:79,85-87, census, simulation and scaling rows | Explicitly empirical/planned/open, not headline theorems; NOT-EXAMINED as external measurements. They cannot discharge any hypothesis. |
| Card:102-122, proposed abstract/body paraphrases and restrictions | SUPPORTED by the corresponding rows except the findings already identified; screening keeps fixed constants and intersection, distribution row keeps fixed M, recovery abstract excludes delivery. |
| Card:156-160, moderate-n posterior and coded-output mixture reading | UNSUPPORTED as generic theorem interpretation (F3), despite identifying its empirical origin. |

For the literature comparison, I checked the primary [Song–Liang published paper](https://doi.org/10.1111/rssb.12095): pp. 950–954, conditions (3), (4), (9)–(14), Theorems 1–2 and Corollary 1; pp. 955–957, Condition 3, Theorems 3–4 and Corollary 2; and its sampler discussion. The card's distinctions between screening, supplementary MAP consistency, and conditional-law contraction agree with those passages. The comparisons do not establish SMC-output guarantees for their implementation. I did not read the excluded local review files that purport to check these comparisons.

## Status/citation audit

I read the frozen registry's status column directly for the cited POST/POST2, W2-APP, PSHARP/PSHARP-R, MISR/MISR-R, START/START2/START2-R, RM/RM2/RM2-R, SAMP, SCR, DIST, N1, F-UNI, TH09/TH128 and auxiliary summary/delivery rows. The current quoted statuses and versions match, allowing the document's declared ellipsis convention. POST2 C/E/A1 conditions, MISR's further conditions, RM2-R's two audit conditions, N1's sampler premises and the root-versus-restatement distinction are carried. No numerical check or code-reading audit is upgraded to a proof by this review. The registered A:IDEAL-W+ text indeed lifts exactly the two application-level cap predicates, leaving the other validators and tie-enumeration cap in force. The problem under G4 is the inaccurate description of the frozen F-UNI method (F6), not a discovered registry-status mismatch.

## Six gates

| gate | decision | reason |
|---|---|---|
| G1 correctness | FAIL | PoolZ, R1, R2 and R4 re-derived successfully. R3's old-master substitution does not derive its current Theorem 7 target (F2). |
| G2 hypotheses used = stated | FAIL | R3 still needs old BM-infinity/diverging visibility for the theorem it invokes; the current reader does not assume them (F2). The direct plus-master route is correctly available elsewhere. |
| G3 faithfulness / F | FAIL | S1 and S2 omit material domains/hypotheses; F1 promotes potential unbiasedness to printed-output unbiasedness; F3 and F5 overread finite-n/design-family scope. See the D71 inventory. |
| G4 statuses and citations | FAIL | Statuses are honestly quoted, but the frozen F-UNI source is described as having a different cap from its explicit :8-12 statement (F6). R3 citations/carriers also need updating. |
| G5 finite-n and scope | FAIL | Theorem 1's all-design obstruction omits the strict-superset domain (S1), and the generic moderate-n posterior/output shape is not supplied by a master (F3). The witness-specific two-sided rates and fixed-constant screening theorem are otherwise carefully scoped. |
| G6 code fidelity | FAIL | Prior/Occam attribution, pilot ESS, fallback order, evidence initial normalizer and score-event/stop reporting need the factual corrections in F4. Equal-weight pooling, coded prior/score formulas, start DP, search neighborhood and certification flags otherwise agree with the pins. |

The score reflects C/S/F findings only. No new theorem proof or experiment campaign is needed to repair the main problems: retain the valid displays, restore the omitted domains, qualify the potential/empirical statements, and update R3's derivation and the code facts.

FIDELITY: NOT-FAITHFUL

COUNCIL-VERDICT round=R1 manifest=759a7dfd87ef7b958a0c8140b6cfa0158f4159cac31c62cf3cb0f1a75fdd7e09 seat=sol score=7.4 gates=FAIL
