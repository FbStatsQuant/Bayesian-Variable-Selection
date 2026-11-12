MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd
Verdict: SWEEP WITH FINDINGS (counts: 0 FATAL / 2 MAJOR / 4 MINOR / 1 NIT)

The central mathematical route survives this sweep. I found no counterexample to RM2-F, RM2-R, or the width lemmas under their actual hypotheses. The findings concern an explicit hypothesis/example mismatch and the accuracy of the supporting records. They should be repaired before the package is declared clean. VERIFIED below means verified subject to the expressly retained external posterior inputs and implementation premises, not an upgrade of their statuses.

All paths below are worktree-relative; RM2 abbreviates Theory_work/Wave3/W3-RM2. All 56 SHA-256 file entries in the frozen manifest match the current files. No git operation was performed, no subagent was started, and this review is the only file written.

## Findings

1. **MAJOR — the advertised unrestricted fixed signal examples do not satisfy the literal energy-constant range.** RM2/STATEMENT.md:114 restricts both M and phi_0 to (0,1]. The imported H0 also says this explicitly at Theory_work/Wave1C/C-GROW/STATEMENT.md:84. But RM2/lemmas/L6_examples.md:287 takes M=C s0 theta_hi^2+1, :349 takes M=theta^2+1, and :399 again takes M=theta^2+1. These choices exceed 1. More substantively, the allowed example theta=2 in E4 or E5 has ||mu||^2=4(n-1), so no M<=1 can establish the claimed H0 verification. Thus “every C1 hypothesis” at :378 and :459 is false for part of the advertised class as written. The same ambiguity is inherited from the parent's convention; that does not remove it here.

   **Correction:** distinguish M>0 from phi_0 in (0,1] in the ticket's constant declarations (including L1:21), and explicitly justify the bounded-energy extension of the imported posterior hypothesis. A short response-rescaling lemma suffices: if ||mu||^2<=B n, choose a fixed a>0 with a^2 B<=1 and apply the restricted-energy theorem to (aY,a theta*,a sigma). The standardized response, every D0 score, block table, start mass and search path are identical; delta^2/tau^2 and theta_min^2/sigma^2 are unchanged; visibility is preserved with M_n replaced by a^2 M_n. Alternatively retain the restricted range and restrict the examples' energies, but that would withdraw the asserted arbitrary fixed nonzero signal range. Do not merely change the local range while continuing to import H0 outside its literal statement without this argument.

2. **MAJOR — B2 is presented as a certified isolated width violation, although that is not established, and its “leakage untouched” explanation is false at eta=0.** RM2/REPORT.md:25 and :116 say the width condition was violated; RM2/SHARPNESS.md:60 says “violated by design.” The evidence in RESULTS.md is an observed improving addition at selected lattice sets, not the expected-width condition on the realized design or an asymptotic failure of W. SPEC.md:34 supplies only a heuristic width formula, yet also claims (V),(L) are untouched because outside columns are independent of truths.

   Marginal independence is insufficient for L's conditional quantifier. In the actual B2 population construction (rm2_common.R:191-197), let H be truth 1, P_t=r H+sqrt(1-r^2) E_t a proxy, and O=sqrt(1-s) W+sqrt(s/m) sum E_t an outside column. Then

       Cov(O,H | P_t) = -r sqrt(s(1-r^2)/m) != 0.

   Therefore the exact zero-leak population analogue used as the B1 baseline is not preserved by B2. It may satisfy a small positive leak budget eventually; that requires an argument, not marginal independence. Nor does one sampled NA failure refute a condition that only guarantees high-probability NA asymptotically.

   **Correction:** consistently say “nominal/heuristic width-stress design; observed NA violations,” including the REPORT flags and registry discussion. Replace SPEC's independence justification by the displayed conditional covariance and distinguish zero leakage from a possibly vanishing positive leakage scale. If an isolated asymptotic width counterexample is desired, supply the width lower bound and the other full hypotheses for the actual design sequence. Keep the verified counts and the LS0-only scope unchanged. The existing disclaimer at SHARPNESS:4 is helpful but does not justify its stronger affirmative wording at :60.

3. **MINOR — the numerical implementation is not literally LS0's returned-archive semantics at the cap, and uses a nonzero improvement tolerance.** RM2/numerics/SPEC.md:13 and rm2_common.R:9, :111 call this LS0 “as coded”/“exactly as coded.” In rm2_common.R:137 the move test is best>F(S)+1e-9; production v3_engine.h:408 uses best>F(S). At the cap, rm2_common.R:138 breaks and :146 returns the current centre S; production v3_engine.h:410 sets returned=best.S, the improving neighbour from the final completed scan. The documented tie difference is a third distinction, already disclosed in RESULTS:95. Validation's four paths do not establish equivalence of these unexercised boundary branches.

   **Correction:** state all three departures and label the recorded final_size on capped probes “current centre at the cap,” not production archive returned size. Alternatively align the implementation and explicitly test the cap branch and strict-improvement rule before calling it exact. The 204/208 certified-success count and four cap interruptions remain supported as observations of the stated reimplementation. Indeed their current centre sizes are 60,22,11,6 versus s0=2, so even one production neighbour cannot equal S0. This discrepancy does not undo that particular cap-obstruction observation, and does not affect the theoretical nonbinding-cap proof.

4. **MINOR — the assumption map still describes an obsolete, unproved version of the package.** RM2/ASSUMPTION_MAP.md:3 names v1.3; :5-7 says only two rows were updated, nothing else changed, and “Nothing is proved yet.” Its :33 already contains v1.4; :16 still describes TL as a lattice-cardinality toolkit argument rather than the exact identity/width proof; :39 calls W-conv a target. These conflict with the actual completed proofs and REPORT's current status.

   **Correction:** label the map v1.4, distinguish historical provenance from present status, replace “planned”/“target” claims by references to L0-L5, and describe TL as L2 §4's identity plus truth-removal width and the addition envelope. Retain the implementation premises and conditional posterior statuses rather than upgrading them. The conclusion and numerical scope paragraphs otherwise correctly avoid a delivery claim.

5. **MINOR — L6's source ledger carries a removed posterior dependency and a stale line pin.** RM2/lemmas/L6_examples.md:493 cites STATEMENT:276-282 as the dependency record and :496-497 includes W3-RM:B9 among inherited conditions. Those lines now concern the limits/numerics remark. STATEMENT:289-298 explicitly removes B9, and L5 §3 proves p=1 locally; REPORT:216 and :219 correctly list the remaining posterior and BC/IR conditions.

   **Correction:** replace the pin by STATEMENT:289-302, remove B9 from the inherited conditions, and state E2 is conditional on W2-APP:POST and BC/IR, E3 on SOP:TH09 and BC/IR. This is an overrestrictive/stale ledger, not an unacknowledged mathematical dependency or a reason to withdraw P10.

6. **MINOR — the sharpness record drops a logarithm from the sufficient sample-floor condition.** RM2/SHARPNESS.md:16 says the Gaussian-row lattice comparison needs q/sqrt(n)->0 and cites L5 (S2) and P9a Step 4 together. P9a's additive comparison does have that sufficient rate (plus log(n)/sqrt(n)), but the entrywise proof in L5:21-23 uses q sqrt(log(n)/n)->0 for the sample floor. The former alone does not justify S2: q=sqrt(n)/(log n)^(1/4) separates these conditions.

   **Correction:** separate the two uses: “entrywise sample floors require q sqrt(log(n)/n)->0; P9a's additive residual comparison requires (q+log n)/sqrt(n)->0; both hold for fixed b<1/2.” ASSUMPTION_MAP:25 already gives the correct floor rate. No theorem with fixed b<1/2 is affected.

7. **NIT — shifted versus unshifted width in E5.** RM2/lemmas/L6_examples.md:451 calls the bound at :453 an “unshifted width.” That bound subtracts sqrt(3-2b)sqrt(log n) and tends to minus infinity. An unshifted E max |u'g| is nonnegative.

   **Correction:** replace “unshifted width” by “width gap w0_n.” The calculation and the b<3/10 cutoff are correct.

## Claim-by-claim table

| Claim | Verdict | Basis / qualification |
|---|---|---|
| C1 RM2-F | VERIFIED | L0-L3 prove the theorem on its stated hypothesis domain; SOP:TH09 remains conditional. Finding 1 concerns extending the examples to arbitrary energy. |
| C2 RM2-R | VERIFIED | L4-L5; W2-APP:POST remains conditional; no conditional-on-sample-scales law is used. |
| C3 width lemmas | VERIFIED | Both diverging-gap implications, failure rate and all sufficient forms check; no bounded-gap conclusion inferred. |
| C4 containment | VERIFIED | Choose b below beta(eta,A) and 1/2-h in F; choose small b,rho in R and use the localized sufficient leak form. |
| C5 examples | VERIFIED-WITH-AMENDMENTS | Findings 1,5,7. E2's BC/IR verification and E3's geometric/width verification check; literal unrestricted-energy H0 verification needs repair. |
| C6 sharpness record | VERIFIED-WITH-AMENDMENTS | Findings 2-6; actual counts agree, but affirmative width claims and simulator fidelity must be qualified. |
| P0 Toolkit-b | VERIFIED | Explicit family/vector cardinalities; same score constants as GEN/GROW. |
| P1 SAND-F^b | VERIFIED | Uniform size ladder and positive beta(eta,A)-b margin. |
| P2 TL-F^b | VERIFIED | Exact two-square identity, BM-W and supplied addition envelope. |
| P3 NA-W | VERIFIED | Lipschitz upper tail, squared-threshold slack, score conversion. |
| P4 W-suff | VERIFIED | Chi-square, frame/atom/remainder and local regression implications. |
| P5 W-conv | VERIFIED | Lipschitz lower tail and lower score bound. |
| P6 POST-F | VERIFIED | Conditional import of SOP:TH09 exactly through T1-F; bounded convergence-in-probability argument is valid. |
| P7 SAND-R^b | VERIFIED | Product-form selection removal, mean-shift spherical bound, counting, feasibility and junk margin. |
| P8 F-to-R | VERIFIED | Deterministic envelopes give uniform conditional n0 and failure probabilities. |
| P9 D-to-W | VERIFIED | Polynomial-size joint bound, Markov conditionalization and Gaussian lower-tail concentration. |
| P10 POST-R | VERIFIED | APP import for p>=2; p=1 direct calculation closes endpoint without B9. |

## Independent derivations

### Toolkit and fixed-design sandwich

For rank d<=J, the mgf at 1/4 gives P(||P_A eps||^2/sigma^2>t)<=2^(d/2)e^(-t/4). With t=4(log|F|+2log n+J), the family union is <=n^-2. The vector union at h^2=2(log|VV|+log n) is <=2/n, including the zero-vector convention. Completing the square Lambda-2sigma h sqrt(Lambda)>=-sigma^2 h^2 gives RSS>=sigma^2 n(1-omega). Thus omega log n->0 at the claimed cardinality, with no hidden factor 2^q in a probability bound.

For eigenvalues g_i>=(n-1)phi0^2, write D_A=(n+1)^|A| product(1-n/((n+1)(g_i+1))). This gives determinant remainder between -2|A|/((n-1)phi0^2) and zero. The quadratic adjustment 0.02+Q_A-RSS_A^y lies in [0.02,1.03] eventually. Therefore R_A lies in [-0.52/c_E,|A|/((n-1)phi0^2)], yielding the stated kappa_E. The lattice family has log cardinality O(q+log n), including all truth swaps and additions used only as auxiliary RSS sets; it is legitimate to evaluate the score formula for an auxiliary set of size K+1.

In L1 Step 2(b), z_n^2=2log p+O(log log n). The fit charge is at most (eta/2)log n+log p+sqrt(2eta log p log n)+o(log n). Subtracting it from log p-log k+0.5log n leaves [0.5-eta/2-sqrt(2A eta)-b]log n-o(log n). The ladder uses a positive Young margin 0.5-A epsilon-(1+1/epsilon)eta/2; minimizing the loss gives eta/2+sqrt(2A eta). Its dyadic union is geometric, independent of which maximizer is selected. The feasibility dichotomy provides a spare slot for every missing truth. All final comparisons hold simultaneously for all maximizers, not merely the emitted one.

### Width, its converse, and truth removal

Phi=max(|u'g|-a0) is 1-Lipschitz. If E Phi=-s<0, then P(Phi>-s/2)<=e^(-s^2/8), and s<=min a0. Hence on its complement Z^2<=(a-s/2)^2<=a^2-(3/4)as. Once (3/4)s sqrt(log(n+1))>=4kappa_E+2, this is c_n(k). The likelihood fit is <=Z^2/2+1/2, uniformly because vartheta log n->0; the prior upper bound and remainder leave exactly -1/2. The fixed-fraction gap yields c*=delta0^2/[32(2A+2)].

Conversely E Phi=s>0 gives Phi>=s/2 except with probability e^(-s^2/8). For the witnessing pair, the prior lower ratio (k+1)/(2p), the likelihood lower bound and Z^2>=a^2+as give

    Delta F >= as/4 -1-log 2-2kappa_E >0

under s sqrt(log(n+1))>=8kappa_E+8 and the common large-n threshold. This proves a whole-lattice obstruction only. The empty-pair convention is harmless.

The W-chi Pythagorean bound uses the common projector P_Q-P_S0 and at most p full-regression directions; its expected square is <=2log p+O(log log n)+|Q-S0|. Frame/atom/remainder bounds give sqrt(2log p+2h log n)+o(sqrt(log n)); the W-unif choice delta=(1-2b-2h)/4 has a strictly positive margin. For W-loc, the padded coefficient difference gives an exact decomposition, atom norm <=L_n/phi0, and the orthogonality identity gives variance inflation <=1+L_n^2/phi0^2. No truth need be in the local conditioning set.

For removal of truth i, A=T-i or T-i+l, B=A+i, the signal remaining outside A is exactly theta_i x_i. Consequently RSS_A-RSS_T=(theta_i||(I-P_A)x_i||+sigma Z_Ai)^2-sigma^2 Z_Tl^2 for a swap. On the width event, |Z_Ai|<=d_n+sqrt(2log n)<=sqrt(lambda_n)/2. The first square is >=sigma^2 lambda_n/4 and the swap subtraction <=sigma^2 lambda_n/8 eventually. The likelihood loss is >=sigma^2 lambda_n/(16 C_R), dominating the O(log n) prior/determinant benefit. Auxiliary |T|=K pairs, when present, number at most p. This explains the extra 2/n bound without assuming additions are feasible there.

### Gaussian-row sandwich and transfer

The covariance event comes from polarizing chi-square deviations with x=(2A+3)log n: a union over at most 4n^(2A) coordinate pairs gives 16n^-3. Uniform bounded coefficient boxes legitimately handle theta_j/t_j. For U=U0 union V, the population cross product c_l' S_VV^-1 c_y equals the difference of the two leak covariances, bounded by 4s0 theta_hi varpi_n. Perturbing both vectors and the inverse gives O(r_n h_n+h_n^2). Denominator changes are O((r_n+h_n)^2) times an O(h_n) numerator. Thus the error on sqrt(h) is O(sqrt(n)varpi_n+r_n sqrt(log n)+log(n)/sqrt(n))=o(sqrt(log n)), uniformly over selected sets.

For the deterministic reference tail, condition on (W_(U0 union S0),eps), not E_cov. The response, including its truth-column sample scales, is measurable there, while the innovation is independent Gaussian. Its projected dimension is d>=n-16. The regression mean has norm <=2s0 sqrt(n)varpi_n/c. A chi-square lower norm bound fails with probability <=e^(-sqrt(n)/8); on its complement sqrt(h)<=(1+4n^-1/4)|Z|+(4/sqrt(c))M_n. Squaring the positive-part threshold loses at most

    8s0 c^(-3/2) sqrt(2A+3) sqrt(n log n) varpi_n + O(1)

in the exponent, which is o(log n). No independence of Z and the innovation norm is required.

The reference family has at most n^(15rho) members per column. At t_n(k)=log(n+1)+2log(p/k)-(4kappa_E+1), the expected count is O(k n^(-1/2+15rho+o(1))). The ladder has O(log n) rungs. With epsilon*=(1-2b-30rho)/2 and T_n=2log p+(30rho+epsilon*)log n, the exclusion probability tends to zero and the deletion margin is exactly (epsilon*/2)log n-O(1). Hence 15rho+b<1/2 is sufficient. The localized leak implication is varpi=varpi'+15r_n^2/c, with the stated (n/log n)^(1/4) rate.

For P8, sample floors, energy and the BM-W ratio have deterministic envelopes, so integrating conditional failure probabilities is justified with one n0. Widths are measurable: finite maxima of continuous residual-direction functions on the full-rank locus, followed by Gaussian integration. The latent extension in P9 is deterministic and independent of eps. Its union bounds use x,v=O(q+log n); the residual-statistic comparison error is 2sqrt(2)sqrt(v(q+log n)/(n-1))=o(1) for b<1/2. Frame and atom terms are sqrt(2log p)+o(sqrt(log n)).

To pass from joint law to width, if a joint exceptional probability is pi_n->0, Markov gives conditional failure <=sqrt(pi_n) outside a design event of probability O(sqrt(pi_n)). On its complement the shifted Gaussian maximum is <=-s_lower with probability >=1/2, where s_lower=(1-2b-delta0)sqrt(log n)/(5sqrt(2A+1)). If its mean exceeded -s_lower+2, Gaussian lower-tail concentration would make that probability <=e^-2<1/2. This establishes the conditional expectation bound without assuming uniform conditional convergence from joint convergence alone. The p=1 posterior calculation gives determinant n, Q_1=(n-1)(1-rhat^2(n-1)/n), and a score advantage of order n over the empty model.

### Examples, assembly, pins and numerical record

BC's cofactor/path estimate preserves decay exponent alpha for bounded conditioning. IR's inverse envelope f(d)=(1+d)^(1-alpha)log(2+d)^(alpha-1) is summable for alpha>2. Refitting matters: beta_A=beta_T,A+B_AA^-1 B_AE beta_T,E yields the required full padded difference bound (1+JD)F(r), not just an omitted-coefficient tail. Radius sqrt(log n) supplies o(log n) reference entropy. For Q radius n^(1/(2alpha))/(log n)^(1/(4alpha)), leak is O(n^-1/2 log(n)^1/4), and the logarithmic saving absorbs size constants even at b=1/(2alpha). The feasibility enlargement is valid for all p sequences. E3's separation condition supplies V and its leak gain is O(sqrt(log n)), below every fixed positive eta log n eventually.

E4 has Gram distance <=r sqrt(q-1)+r^2 q=o(1). Given the truth, a remaining proxy residual is sqrt(1-r^2)e_l; local regressions therefore agree exactly. E5 has A_t=a/(1-a+ta), v_t=(1-a)(1+a/(1-a+ta)), and normalized projections bounded by 2max_{j<=q}|g_j|+sqrt(a/(1-a))|g_0|. Comparing max(sqrt(8b),sqrt(2)) with sqrt(3-2b) proves b<3/10, without proving any of the sketched 3/8 claims. These verifications leave only Finding 1's literal energy issue for the fixed-design example class.

RM-0 is used within its stated arbitrary-deterministic-Q domain. Its proof uses NA at an extra-deletion child to dominate any swap, TL to exclude truth removal, and exact E4 maximization for the centre. The cap exceeds the number of deletions; the completed terminal scan certifies S0. The common event K_n intersect {pi(S0)>1/2} is a data event, and Markov supplies its reporting bound uniformly over run parameters. E4's encoding/inverse-map, execution and arithmetic hypotheses are imported by STATEMENT §1, not silently dropped. No delivery or public-final-model certificate follows or is needed. No named design family is imposed in the general theorems; the examples are separately labeled.

The pinned core lines 394-404 and 465-476 implement the stated option, unmodified start_mode centre and additive cap. Engine lines 392-414 confirm complete feasible flips/swaps, lexicographic neighbour ties, strict improvement, completed scan, and the distinct certification/cap branches. The caveat in Finding 3 is in the probe, not these theorem pins.

I independently aggregated results_raw.csv: 208 rows, 204 certified successes; B1 boundary cells 48/48, B2 48/48, B3 32/32, B4 eta=0.05 or 0.2 32/32; all four failures are eta=1,n=1600. Their swap counts are 73,35,24,19 and current-centre sizes 60,22,11,6. The 202/202 count outside that six-run cell is correct. RESULTS §§1-3 deliberately retain the earlier 207-run snapshot; §4 correctly reconciles it to 208. The K1-K13 output values quoted in RESULTS agree with the frozen outputs at their reported precision; K10 explicitly does not exercise a substantial mean shift. Source scripts, including the test sampling repair, were inspected, not executed.

## Not checked

- No simulation, production build, or benchmark was rerun; doing so could write additional worktree files. CSV counts were recomputed in memory, and frozen numerical scripts/outputs were inspected. Monte Carlo estimates are not mathematical certification.
- No other review, log or checkpoint was read. Statements about prior reviewers' actual reports cannot be authenticated from the permitted corpus; their quoted endorsements were not used as evidence for the new proofs.
- Registry claims.tsv, the primary SOP:TH09 proof, RM's standalone L5_E4 proof, and several transitive example proofs are not manifest inputs. Their full proof audits and registry-wide status authentication are not claimed. Their available statement/interface and status records were checked, and the explicit posterior conditions were retained. Historical commit provenance was not independently authenticated through git; current pinned file hashes and line content were checked.
- External literature comparisons in ASSUMPTION_MAP:78-96 remain explicitly memory-based and pending the literature gate. No outside paper or web source was consulted, in accordance with the manifest-only review boundary.
- No necessity beyond the positive-diverging-gap whole-lattice obstruction, no bounded-gap characterization, no b>=1/2 theorem, and no sharper equicorrelation cutoff were established or assumed by this review.
