MANIFEST bf619625bf0880c6dd270771fcd0e9c94c9eeb268e75212cb918c8ab5a24dd61
Verdict: ACCEPT WITH CHANGES

Required changes:

1. **MAJOR — give the replacement toolkit the rate needed by its advertised consumer.** Location: `Theory_work/Wave3/W3-START/STATEMENT.md:173`, consumed at `STATEMENT.md:220` and used in the proof structure at `STATEMENT.md:246`.

   The newly explicit [TK] specifies only a deterministic relative RSS error bound tending to zero. Bridge (B-L) claims a pointwise step bound with an additive `o(1)` in the exponent, after linearising a gain of order log n. Relative RSS error `omega_n` contributes an error of order `omega_n log n`; convergence of `omega_n` to zero alone does not make this error vanish. For example, take tau_T^2 = 1, RSS_T = (n-1)(1-omega_n), a nested RSS decrease of log n, and omega_n = 1/sqrt(log n). These residual values satisfy the displayed relative approximation for both nested sets (up to an immaterial adjustment of the error envelope), but

   `nu log(RSS_T/RSS_(T+l)) - (log n)/2 ~ sqrt(log n)/2`,

   rather than o(1). The bounded score remainder does not fix that missing control. This is a gap in the explicit interface/event definition, not a counterexample to START-F under its primitive hypotheses: a suitable faster toolkit event is available under those hypotheses.

   **Exact required edit:** in the [TK] row replace `max|rho_U| <= omega_n -> 0 (deterministic omega_n)` by `max|rho_U| <= omega_n, where omega_n is deterministic and omega_n log n -> 0`. Require Lemma TK/B-TK to deliver that strengthened event. A valid explicit envelope is `O(n^(-1/3) + sqrt(log n/n) + log n/n)`, with constants depending on the fixed bounds. Prove the event locally as promised; do not import an unchecked RSS lemma as a premise. The source calculation at `Theory_work/Wave3/W3-RM/lemmas/L1b_rss.md:24-34` explicitly supplies the missing log-rate condition; it is evidence that this is a local repair. The original Gaussian concentration events in `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:25-38` also support that repair without a normalised Gram floor.

2. **MINOR — restrict the default-level identities to their domains.** Location: `Theory_work/Wave3/W3-START/STATEMENT.md:232-233`; definitions at `STATEMENT.md:95`, `STATEMENT.md:104-111`.

   T1 is stated for any Q containing S0. Its parenthesis then evaluates both L^0_n(h) and L_n(S0;h) using a level vector for Q. If Q is strictly larger than S0, that vector supplies no h_l for l in Q minus S0. Those expressions are undefined. The substantive clauses (b) and (c), and the second inequality of (d), correctly restrict to Q=S0; the parenthesis needs the same restriction.

   **Exact required edit:** replace the parenthesis by `(default: h_l = z_n for l outside Q, giving varrho_n(Q;h) = varrho_n(Q); when Q = S0 this also gives L^0_n(h) = L^0_n and L_n(S0;h) = L_n(S0))`, using the document's existing mathematical glyphs. No extension of h to Q minus S0 is needed.

Optional suggestions:

1. **Make the additional scope change explicit.** `STATEMENT.md:313-315` newly makes Proposition OVL provisional, whereas v1.2 asserted it without this proviso. This is a fourth substantive change, outside the three listed in this review brief and outside its enumerated editorial exceptions. It is consistent with the original lead brief's “if cheap” instruction (`Theory_work/Wave3/W3-START/BRIEF.md:19`), but the new lock should record a definite disposition. If OVL remains provisional, qualify the overview's interface promise (`STATEMENT.md:30-31`) and the “lower bound ... claimed” sentence (`STATEMENT.md:343`) accordingly. The deterministic AGG-c interface remains an unconditional target.

2. **Sharpen the example, not the sufficient condition.** At `STATEMENT.md:337`, F4 does not imply that default-level (AL) fails for every leaking column below 1+2 A_lower. Small enough gains still satisfy default (AL). Say “an isolated leaking column in a regime where default-level (AL) fails, but F4 applies,” and eventually exhibit the example. Likewise the J2 comparison at `STATEMENT.md:270-272` is a threshold for the displayed upper bound to vanish, not a necessary threshold for the actual default functional.

3. State explicitly in T3(a) that the optional rate envelope r_bar_n is deterministic and nonnegative (`STATEMENT.md:283-284`). The intended reading is clear from the uniform-envelope construction, but this makes the transfer quantifiers self-contained.

Checks performed:

**Frozen inputs and review boundary.** Read the designated brief first. Independently recomputed SHA-256 for all 33 file entries in MANIFEST_SC3.txt: **33 matched, zero mismatches**. This checks the listed bytes, including all 23 external inputs; it is not a claim to have run the manifest utility or independently recomputed its aggregate digest. Used read-only `git diff HEAD -- Theory_work/Wave3/W3-START/STATEMENT.md` to compare the locked v1.2 with v1.3. No other review, LOG or CHECKPOINT file was read. No git mutation, delegation, production run or source edit was performed.

**A. Complete inventory of the statement diff.** All changed regions are accounted for below; locations refer to v1.3.

1. `STATEMENT.md:3-4`: lead descriptor and v1.2 LOCKED header become the v1.3 header.
2. `STATEMENT.md:18-27`: overview substitutes the unnormalised floor, introduces column levels and adds design-measurable random-design transfer.
3. `STATEMENT.md:94-115`: adds h, its admissible range/dependence, b_n(h), default convention, J_h and J_n alias; replaces J0-J3 by their h forms; adds levels to both partition-free and block-relative leakage functionals and varrho; treats s0=0 by averaging h_l; retains the z_n allowance for a block containing all truths; explains the column-specific truncation.
4. `STATEMENT.md:122-131`: substitutes g_* for the global floor constant, reserves phi_0 for F2, replaces FL-16/A:START-FL by GF-16/A:START-GF, and explains its relation to a normalised floor and close columns.
5. `STATEMENT.md:144-149`: AL becomes existence of h with vanishing tail budget and leakage rate; adds the default equivalence and F4 reference. The small-gain consequence is retained.
6. `STATEMENT.md:173-175`: explicitly restates [TK] and replaces its registry-consumption route by local Lemma TK; adds h and b_n(h) to [LEAK(Q)], restricting its T1 clause to Q=S0.
7. `STATEMENT.md:199-204`: adds h and its tail premise to C1 and replaces all its rates by their h forms.
8. `STATEMENT.md:218-223`: B1 uses GF-16 and level functionals; B-TK is now a local proof including s0=0 and the two scalar bounds; B-L uses column truncations and counts their tail; B-R explicitly retains a normalised sample floor, implies GF-16, and specifies default levels. B-V1/B-V2 themselves are unchanged.
9. `STATEMENT.md:231-245`: T1 substitutes GF-16, carries h through (a)-(c), and rewrites (d)'s uniform class, constant list and inequalities with h and exceptional probability epsilon+b_n(h).
10. `STATEMENT.md:248`: predecessor comparison now says Gram floor.
11. `STATEMENT.md:252-272`: T2's heading substitutes GF-16 and reserves default levels for F1-F3; F2 explicitly declares its own fixed normalised floor constant; F4 and its default-level comparison are new. F1 and F3 conclusions are unchanged.
12. `STATEMENT.md:275-286`: T3(a) replaces deterministic beta/support/Q by design-measurable alpha/beta/support/Q/h, states the conditional Gaussian law, supplies uniform design sets and two vanishing envelopes, and changes both rates to their level forms. T3(b) is unchanged.
13. `STATEMENT.md:295`: T4 substitutes GF-16. Its N1-N4 conclusions are unchanged.
14. `STATEMENT.md:308-310`: IF-START's fixed-design rate now carries h; the Gaussian-row rate and consumer conclusion are unchanged.
15. `STATEMENT.md:313-315`: OVL substitutes GF-16 **and newly becomes provisional**. This proviso is the additional substantive scope change identified above. Its quantitative bound is unchanged.
16. `STATEMENT.md:326-332`: T6 substitutes GF-16 and replaces the deterministic-only random-candidate restriction with conditional GR and design-measurable coefficients/support/Q, excluding response selection.
17. `STATEMENT.md:334-339`: examples add close null columns and the F4 regime.
18. `STATEMENT.md:345-352`: Not claimed substitutes GF-16/level-vector language, names O1-O3 and excludes response-selected targets.
19. `STATEMENT.md:355-358`: dependencies switch to “Consumed: none,” mark the GROW toolkit as sources only, and promise local TK under GF-16 for s0>=0. The remaining dependency entries are unchanged.

Apart from the OVL proviso, there is no additional substantive change outside the three advertised changes and the specified editorial exceptions. No unintended old FL-16 premise or old phi_0 toolkit constant remains in the statement: residual normalised-floor references are explanatory, F2-specific, B-R-specific, or historical dependency descriptions. ASSUMPTION_MAP.md intentionally retains its v1.2 map and appends an explicit v1.3 delta at lines 48-60; that is not a silently stale claim.

**B. Levels, elementary bounds and domination.** All the following were checked algebraically.

For a fixed design, h can depend on X, theta*, sigma and Q; it cannot depend on epsilon or the response. For transfer those objects are fixed after conditioning on the design. The default budget is exactly bounded by

`2^16 (p-|Q|)/(2^21 p log n) <= 1/(32 log n)`.

The Gaussian integral can be written

`J_h(d,t) = exp(d^2/(2t^2))/sqrt(2*pi) * integral[-h,h] exp(d*sigma*z/t^2 - (1-sigma^2/t^2)z^2/2) dz`.

* J0: retain [0,1] when d>=0 or [-1,0] when d<0. On this interval the cross term is nonnegative and the original integrand is at least exp(d^2/(2t^2)) times the standard normal density. Phi(1)-1/2 is about 0.3413, exceeding 1/4. Thus h>=1 suffices for every d and t>=sigma.
* J1: remove the truncation and complete the square, for t>sigma. This gives the displayed full Gaussian moment exactly as an upper bound.
* J2: in the integral above drop its nonpositive quadratic term and bound the linear term by |d|sigma h/t^2. The interval length supplies sqrt(2/pi) h.
* J3: at d=0,t=sigma the two quadratic exponents cancel, giving sqrt(2/pi) h exactly.

Supplemented the algebra with composite Simpson integration, 4,000 panels, for 240 combinations: sigma in {0.2,1,3}, h in {1,1.1,2,5,10}, t/sigma in {1,1.01,1.5,5}, d/sigma in {0,0.1,-1,3}. No violations of J0-J3 (comparison tolerance 1e-7). SciPy was unavailable; the integration used only the Python standard library and wrote no file.

The block-relative maximum in L^b_n(Q;h) ranges over subsets of the partition-free maximum, so its domination is immediate. For L^{b,0}, if the block's truth subset is proper, it occurs in L^0's maximum. If it equals all S0, delta=0 and tau=sigma, and at most 16-s0<=15 null columns can be in that block when s0>=1. Their total is at most `15 sqrt(2/pi) z_n/p`, even with nonuniform h. If s0=0, every truth subset is empty, delta=0 and tau=sigma, so L^{b,0}_n(h)=L^0_n(h) exactly. No missing full-truth-block term was found.

J0 still gives `exp(delta^2/(2 tau^2)) <= 4p L_n(Q;h)`. AL therefore implies the stated `delta^2/tau^2 <= (1+2A+o(1)) log n`, uniformly in the allowed pairs. This does not rely on h=z_n. Each column has at most 2^15 within-block conditioning sets. The two-sided normal bound contributes the factor 2, yielding exactly the stated `2^16 sum exp(-h_l^2/2)`; independence is unnecessary.

**C. Gram floor and changed claims.** Read the pinned score formula at `Scripts/SMC_BVS/core/cpp/v3_score.h:204-224`. With eigenvalues lambda_i>=g_*,

`det H/det(G+I) = (n+1)^k product_i [(lambda_i+1/(n+1))/(lambda_i+1)]`.

Each factor lies between g_*/(g_*+1) and 1, proving both eta bounds in B-TK. Also

`Q-RSS^y = (G^(-1/2) z)' [(G+I) H^(-1)] (G^(-1/2) z)`.

The middle matrix has eigenvalues `(lambda+1)/((n+1)lambda+1) <= (1+1/g_*)/(n+1)`. Since `z'G^(-1)z=||P_U y||^2<=n-1`, this proves `0<=Q-RSS^y<=1+1/g_*`. The empty set gives zero. A 36-case scalar grid over n in {4,20,1000}, g_* in {1e-6,0.01,1,100}, and lambda/g_* in {1,10,10000} also found no violations.

Under E the standard Gaussian projection and linear-form concentration bounds give uniform RSS approximation for the at most 2^16 p block subsets, irrespective of small nonzero singular values. Together with the scalar bounds and RSS^y>=c_E n, these give a bounded score remainder: the determinant contribution is at most `8 log(1+1/g_*)`, and the ridge-plus-0.02 contribution is bounded by a constant times `(1.02+1/g_*)/c_E`. Thus the new primitive toolkit route is plausible, including s0=0. The required rate repair above makes its small-gain consumer explicit.

F2 does still need a normalised floor, and now states it expressly at `STATEMENT.md:258`. The Schur-complement/minimisation argument gives Delta_U>=phi_0^2 theta_lo^2 for U properly inside S0, even if S0 has more than 16 elements. B-R expressly supplies its own normalised sample floor at line 223. Neither is inferred from GF-16. C2/T4 use one-step score comparisons plus TK; their polynomial thresholds do not require a further normalised floor. OVL's bounded set of exceptional columns can use individual Gaussian bounds with growing thresholds o(sqrt(log n)) and the same bounded score remainder, so its displayed exponent does not visibly require that stronger floor either. These are plausibility checks, not completed proofs of these targets.

F4: for isolated columns its truncated J2 contribution is at most `n^(c/2+o(1))`, because h_l=O(sqrt(log log n)), the cross exponent is O(sqrt(log n log log n)), and the prefactor is subpolynomial. Dividing by p sqrt(n) gives `n^(-(1+2 A_lower-c)/2+o(1))`. Summing a bounded number preserves the exponent. The isolated-column budget is bounded by a constant times `1/(log n)^2 + 1/(p log n)`; the others contribute at most 1/(32 log n). All vanish. The minimum with z_n and the requirement h>=1 are valid for n>=4.

Checked limiting cases p bounded (A_lower=0, admissible c<1), p much larger than n, one isolated column, and c just below 1+2 A_lower. The gap is positive but can be arbitrarily small, as the stated condition on |Q| requires. Q different from S0 only multiplies the bound by |Q|+1 and changes which columns enter the tail sum; no absent levels are used in F4 itself. For log p/log n -> A>0 and bounded |Q|, the default J2 contribution exponent is `(c-1)/2+sqrt(2Ac)-A`; solving its negativity yields exactly `(sqrt(4A+1)-sqrt(2A))^2`, strictly below 1+2A. For growing Q the extra |Q|+1 factor must still be paid, as F4's main assertion already requires.

**T1(d), T3(a), T6.** T1(d) is a finite-n uniform assertion over the displayed class; it does not assume b_n(h)->0 at that particular n, and epsilon+b_n(h) may be vacuous for a bad h. This is well-posed. The constants may be chosen independently of h, Q and the individual design. Subject to the toolkit repair, the probability accounting has the correct form.

Condition on X^r in T3(a). Alpha, beta, S0, Q and h are then fixed, the noise has the required fixed-design Gaussian law, and the conditional bounds have the same constants. Integrating gives a bound by epsilon+b_bar_n+P(X^r outside X_n). For the displayed little-o remainder at exponent kappa, apply T1(d) at a larger exponent kappa' strictly between kappa and kappa_V; then n^(-kappa')=o(n^(-kappa)). The same argument applies to the odds envelope. A tail budget merely tending to zero suffices; it need not decay polynomially. No response information can enter the target choices under these hypotheses. Setting R is included by beta(X^r)=D_x^(-1)theta* on retained columns.

The random-candidate clause of T6 supplies the same conditional model after adding the independent Gaussian residuals: epsilon'=epsilon+xi has conditional covariance (sigma^2+tau^2)I, fixed and positive. `Theory_work/Wave1C/C-MIS/STATEMENT.md:54-58` states precisely this GR reduction, with tau^2 fixed. Beta_C is fixed in that setting; adding design-measurable gamma makes beta^C design-measurable. T3(a) consequently covers the new clause, with all substituted design-set hypotheses and fixed support cardinality still required. Response-selected candidates are expressly excluded.

**D. Dependencies, statuses and consumers.** The statement treats TK, the tau-form RSS facts, Gaussian-row sample facts, aggregation and the MIS reduction as local proof obligations. I found no silent invocation of an unchecked external theorem as an established premise in the frozen target. “Consumed: none” is therefore consistent with `Theory_work/Wave3/PROTOCOL.md:86-90` at this stage; future proofs must honour that promise.

Compared registry rows directly (version/status/state columns): C-GROW:L0.1@1.0.0 and L0.2@1.0.0 are PROVED-CHECKED (rows 96,278); W3-SAMP:C@1.1.1 and D@2.1.1 are PROVED-CHECKED (355,352); W1-PXN:Thm-PXN(S)@1.0.0 is XF VERIFIED (19); C-MIS:LemR@1.0.0 is `R02 VERIFIED; council R07/R08 PASS` (75); W3-RM:B1, B2tau and SAND-R@1.0.0 are `PROVED (by this seat, unchecked)` (373,376,381). All are ACTIVE. The quoted statuses in section 7 match verbatim. SOP:TH116@1.0.0 is listed there without a purported full status quotation; the predecessor description at line 247 matches its clause-(iii) status substring, not its much longer aggregate status (registry row 13).

T5 still supplies P-START at `Theory_work/Wave3/W3-SAMP/STATEMENT.md:76-77`, and its deterministic vanishing rate combines with posterior concentration as required by SAMP C-v (`:158-162`). For Q=S0, L^0_n(h)<=L_n(S0;h)+15 sqrt(2/pi)z_n/p when s0>=1, so the IF-START rate really vanishes under AL; for s0=0 use the exact formula already checked. The OVL exponent condition gives a positive polynomial margin over max(1,log p/log n), hence the production overlap criterion at SAMP `:103-105`. It supplies computational P-OVL (`:82-83`), not the different global P-OVL-infinity interface (`:79-81`). OVL's new provisional status is the scope caveat identified above; neither P-MAP nor delivery is silently supplied.

**E. Design-agnostic form.** Theorem hypotheses remain partition-free conditions on the design and signal (or population covariance and signal). No particular design family has become a hypothesis. Family names occur in the examples, overview descriptions of settings, and explicitly excluded regimes. Component lemmas and intermediate block-relative interfaces necessarily mention the actual partition, consistently with the ticket's declared architecture.

Not checked:

1. Full proofs of the unproved targets, especially aggregation, the V-m visibility bridge, the averaged Gaussian-row leakage bound B-R, and Proposition OVL. No claim here certifies those proofs.
2. Production numerics, simulation scripts and recorded numerical results were not rerun or used as proof evidence. Manifest hashing verified their frozen bytes only.
3. External lemmas not in the permitted input list, literature comparisons, git history beyond the permitted statement diff, other review records and checkpoint/LOG material. Registry evidence strings were read only as registry data; their referenced review files were not opened.
4. Binary64 behavior, sampler correctness, calibration success, reported-model guarantees, delivery, non-Gaussian noise and response-selected targets.
