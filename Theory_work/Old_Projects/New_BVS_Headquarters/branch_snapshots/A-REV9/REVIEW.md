# A-REV9 independent cross-family review

The authoritative scope is W8-SYNTH §8 task 7. Source heads are pinned in SNAPSHOT.txt; readable source copies are under sources/ (Git blobs at those heads remain authoritative). Review verdicts do not alter author statuses or adopt results. Analysis is symbolic; no simulation or benchmark has been run locally or remotely.

## Certificate findings

- Lemma M: VERIFIED in exact arithmetic. The push-through identity gives Q=y'y/(n+1)+n/(n+1)y'(I+(n+1)XX')^-1 y. Inversion reverses PSD order. For a column addition D'/D=h(n+1)/h(1), h'(c)=x'(I+cM)^-2 x>=0. BB weight ratio is (k+1)/(2p-1-k)<=1.
- C1(a): ERROR as literally quantified. It includes S=HPM in the claimed ratio <=exp(-g). Any strict best score with g>0 gives 1<=exp(-g)<1. Repair: exclude HPM, as C3(c) already does. The Z_T bound itself is VERIFIED.
- C1(b): VERIFIED simultaneous Markov implication under fixed-data frozen-run unbiasedness and stop-only output coupling. Original unscored-mass wording: ERROR; O-VCERT R1 correctly replaces it with mass outside T. This does not upgrade the original statement.
- C1(c): VERIFIED as a non-implication from unbiasedness alone; it does not exclude deterministic upper bounds on Z.
- C2: VERIFIED as a conditional implication with PW2, independent islands and frozen calibration. Cantelli gives B_T/(B_T+4 epsilon^2). It does not establish PW2 or completion probability.
- C3: VERIFIED ratios and fully rescored regions in exact arithmetic. Apply local certification to the returned/scanned centre; identifying it with the reported HPM requires checking identity, especially under exact ties.
- C4: VERIFIED exact-arithmetic box inequalities. w and D at L and Q at U give the maximum bound; summing the exact size weights gives the mass bound. The displayed mass lower bound is conservative even if the HPM leaf is not isolated. FP clause remains GAP without certified errors for the mixed-endpoint bound Phi, not merely errors for complete scores F.
- C5: ERROR if interpreted as a tie-aware posterior-miss certificate from a weak score inequality. Duplicate columns give equal-size equal-score models; if the unscored truth wins lexicographic ties, scoring it changes the report. The displayed probability inclusion for strict F(S0)>F(HPM) is VERIFIED. Repair the prose with strict inequality or the total HPM order and S0 feasible.
- C6: GAP pending R1, FP inflation R2, and explicit local/region certificate validation. Its exact-arithmetic union-of-claims argument is valid for the repaired claims under statistical-field stop-only coupling, not for the original card.

Initial certificate subset (superseded by the final LOCKABLE list below): Lemma M; the deterministic Z_T inequality; C1(c); conditional C2; C3 ratios; exact C4 bounds; strict-score C5 probability inclusion. No original GAP is upgraded.

## Final scope and verdict register

Reviewer: A-REV9, GPT-6 Astra, 2026-11-02. Two GPT-6.1 Sol helpers supplied analytical checks in MASKED_PW2_CHECK.md and DILUTE_STAGES_CHECK.md. I inspected their findings and the underlying proof passages; the verdicts here are mine. Source statuses (PROVED, PROOF SKETCH, OPEN, etc.) remain unchanged. VERIFIED means the specified mathematical implication passes this review; it does not mean adopted. GAP includes explicitly identified unfinished review obligations, which are distinguished from mathematical proof gaps below.

Priority followed: certificates, masked outputs, evidence variance, dilution, then separation/partition and stage/weight results. O-SWAP and W7-SEC are additional user-requested items outside the task-7 item list. No experiments were executed; all counterexamples below are explicit analytic constructions. Historical numerical claims were not independently reproduced. No remote job was necessary for this symbolic review, and no local computation substituted for one.

| Result | Final verdict and scope |
|---|---|
| O-CERT Lemma M | VERIFIED, exact arithmetic |
| O-CERT C1(a) | ERROR in self-inclusive gap inequality; deterministic normalizer bound VERIFIED |
| O-CERT C1(b), R1 | VERIFIED repaired outside-store implication, conditional on frozen-run unbiasedness and statistical-output coupling; original unscored wording ERROR |
| O-CERT C1(c) | VERIFIED non-implication from first moments |
| O-CERT C2 | VERIFIED conditional PW2/Cantelli implication |
| O-CERT C3 | VERIFIED exact ratios; GAP for identifying local returned centre with HPM without an identity/tie check |
| O-CERT C4 | VERIFIED exact boxes; GAP in claimed FP certification from SC alone |
| O-CERT C5 | ERROR tie-insensitive prose; VERIFIED displayed strict-score event inclusion |
| O-CERT C6 | GAP original card; repaired exact implication requires the conditions below |
| F-MASKPIP M1(a-c) | VERIFIED under locked exact frozen-run assumptions |
| F-MASKPIP M2(a-e) | VERIFIED intersection bounds, not completion-conditioned guarantees |
| F-MASKPIP M3 | ERROR probability-one counterexample; conditional means VERIFIED for 0<kappa<1 |
| F-MASKPIP N-a | GAP literal finite-index/rate wording; VERIFIED finite-index inequality with actual non-crossing probability |
| O-PW2 A1-A4 | VERIFIED |
| O-PW2 B1-B3 | VERIFIED, asymptotic O(N^-3/2) only for fixed inputs/grid or uniform constants |
| O-DILUTE E | VERIFIED with feasibility/cap retained |
| O-DILUTE E1, three-term identity | VERIFIED for production BF tables; GAP arbitrary-positive-table scope without normalization |
| O-DILUTE E2 | VERIFIED supporting-line bound with interior-size/end-point conventions |
| O-DILUTE R | VERIFIED, integer d>=0 and feasible supports |
| O-DILUTE N | VERIFIED under explicit joint independence; ERROR parenthetical implication from zero truth correlation |
| O-DILUTE S | GAP: replacement assignments are not injective |
| O-DILUTE DM(i), size sign | ERROR; explicit construction below |
| W7-SEP SEP(A), SEP(B1-B3) | VERIFIED as implications from its imported tight start-mass and posterior-concentration premises |
| W7-SEP GU | GAP in this review: descent and superset argument checked, imported uniform score-comparison Lemma M not independently audited here |
| W7-PART A1-A4 | VERIFIED deterministic no-tie statements, with A2's extra premise |
| W7-PART B-exact | VERIFIED Gaussian pair-law/union-bound statement |
| W7-PART B-explicit, L2 density constants | GAP in this review: classical density normalization not independently established; do not lock the explicit constants on this review |
| O-STAGES M | GAP explicit decimal constants; VERIFIED logarithmic order for ideal two-state exact-frontier grid |
| O-WSTAB W(a), W(b), W(c), W(d), W(e), W(f) | VERIFIED under H-ORTH exactly as stated, including W(d)'s stronger upper-side premise |
| O-WSTAB W prime | VERIFIED ideal full-space grid under H-ORTH; production-grid transfer remains GAP |
| O-SWAP predicted rates | GAP: additional approximations and data reproduction remain; PA alone does not give the displayed add law |
| W7-SEC T05, T33, T32(i) | GAP in this review: deferred detailed proof/code audit, no mathematical rejection asserted |

A-REV6 at ee3f3c68dc4c16ff631236c16afe2f82c75a5d15 and A-REV7 at 2d672a08a32b570aabedef01527bf047fffc1f77 have no files under their respective review directories (checked with git ls-tree) and no REVIEW.md. Neither supplies a completed review to import. No coverage credit is assigned from their branch names.

## Certificate repairs and explicit counterexamples

C1(a): take any two scored models with strict gap g>0 and set S=HPM. The displayed inequality becomes 1<=exp(-g). Exclude HPM; define g only when a competitor exists (or specify the empty-maximum convention).

R1: let a positive finite posterior have all states scored, let Zhat=Z, and choose a reported subset T with pi(T)<alpha. Unscored mass is zero, whereas 1-Z_T/(alpha Z)>0. The corrected statement is about Omega minus T. O-VCERT's optional unscored bound also requires a genuine upper bound on the entire logical scored set: a final-run fresh-score count that omits calibration is insufficient. Use a full store and Nbar covering every phase, with unreported scores bounded by F_min.

C5: identical predictor columns 1 and 2 give F({1})=F({2}). Let the truth be {1}, the reported/scored alternative be {2}, and restrict the verified box to U={1,2} with singleton models maximizing (choose a response fit where one inclusion beats empty but redundant inclusion is penalized). The lexicographic rule prefers {1}. Weak score domination alone cannot exclude a tie-related search miss. The C5 event inclusion only concerns strict score superiority and survives unchanged.

C3/C6 local identity: v3_engine.h local_search marks A.returned as certified when its frozen-centre scan has no strict improvement. The ledger can update the HPM on an equal-score neighbour without moving the centre (explicit code comment and strict best.F>C.F test). Therefore check returned==HPM, certify the returned support by name, or rescan HPM. Local flags alone cannot be silently transferred across distinct supports.

C4/C6 floating point: SC bounds computed complete scores F(S). Phi(L,U) combines log D_L and log(2b0+Q_U); errors in complete scores do not separately bound these mixed ingredients. Require interval bounds for each ingredient (including summation) and prune only when an upper bound for Phi is below a lower bound for F(HPM). R2 then correctly supplies

    u_fp(S)=exp(F_fp(S)+eta_F)/max(exp(-eta_F) Z_T_fp, alpha Zhat_fp),
    outside-store lower bound = 1-exp(eta_F) Z_T_fp/(alpha Zhat_fp).

The statistical failure probability is at most alpha exp(eta) P(A)+epsilon under VAL-FP. This is a conditional validation contract, not a measured production guarantee. Local and region claims must only be emitted after their own checks. Under exact arithmetic, those checks plus R1 give the C6 union bound directly from the single bad event Z<alpha Zhat. We do not upgrade the original GAP card or GUARD's broader implementation claims.

Reference audit: methodology sections 5 and 6.13 match the common Q,D definitions; expanding the scorer's nonnegative fallback with beta=n H^-1 z gives y'y-z'beta, the same Q. v3_ledger.h stores distinct models by deterministic score/support and uses size then lexicographic HPM ties. v3_engine.h:202-216 draws each particle's round separately; the final loop uses multinomial resampling before independent mutations. These support the exact component model, not a universal floating-point assertion.

## Masked PIPs and evidence variance: proof checks

Put delta=1-pi(S0), W=Zhat_r/Z and f_s equal to the terminal outside-truth fraction. Locked T12 gives E(W f_s)=delta and EW=1. For a measured path, B<=1{start outside}+1{start at truth}D, with conditional departure probability rho. W is measurable before the terminal round. Thus E(W Bbar)<=delta+rho, and locked T23 gives E(W err)<=delta+rho+u_pi. This proves M1. Markov and Wbar err_secondary <= (1/4)sum W_r err_r prove all M2 clauses. Equal-weight pooling instead requires control of min W_r. None justifies conditioning on passing diagnostics.

M3 counterexample to the literal statement: kappa=1/2, delta=1/10 forces E(W|C)>=1.6; W<c<1 almost surely on C is impossible. Repair: choose a<c, a*kappa<1-delta, split C into masses kappa-kappa' and kappa', assign W=a and W=[1-delta-a(kappa-kappa')]/kappa'; on C-complement put f=1,W=delta/(1-kappa), and on C put f=0. Then W>0, EW=1, EWf=delta, and P(W<c|C)=1-kappa'/kappa tends to one. This proves the intended moment non-implication, not realizability of this law by the BVS engine. Omit E(W|C-complement) at kappa=1.

N-a's valid bound is P(f>1/2,W<sqrt(delta))>=P(f>1/2)-2sqrt(delta). A liminf hypothesis yields a liminf conclusion, not the printed finite-n kappa bound. T03's O_P rate supplies a high-probability constant depending on the requested confidence; it does not supply the printed unit constant in delta^-1/2 >= (n/log n)^(1/4)(1+o(1)).

For PW2 define M_s=W_s qhat_s(h_sT), M_-1=1. Conditional iid children give E(M_s|F_s-1)=M_s-1 and conditional increment variance W_s^2 Var_mu_s(h_sT)/N. Orthogonality proves A2. If e_s=E[W_s^2 mu_s(h_sT^2)] and m_s=E M_s^2, then m_s-1 = (1-1/N)*(m_{s-1}-1)+(e_s-1)/N, proving A3. A4 follows by squaring W_t=W_{t-1}qhat_{t-1}(g_t).

Weighted unbiasedness splits e_s into 1+sigma_sT^2 plus E[W_s(W_s-1)mu_s(h_sT^2)]. Cauchy-Schwarz bounds the remainder by H_sT^2 sqrt(V_s(1+V_s)); B1 follows, then monotonic induction gives B2. B3 is the induction U_t<=x+y sqrt(2x(1+2x))<=2x. The /4 is conditional on frozen calibration. The constants can be huge along growing n,p,T; this review does not establish study-scale precision. Detailed checks and full corrected constructions are in MASKED_PW2_CHECK.md.

## Dilution: exact results versus unsupported extensions

E follows by multiplying product block probabilities by w(k)t^-k and normalizing over N<=K. E1 needs r_b(empty)=1, which holds for the actual BF tables. For arbitrary positive tables normalize each block by its empty entry first. Without that, C need not be nonnegative and the formula for truth-free blocks is wrong. R is coefficient extraction in the bivariate generating function followed by the integer Markov inequality.

DM(i) reverses a sign. The correct consequence is -log A >= log P_t(N<=K), not >= -log P_t(N<=K). Explicitly p=2,K=s0=1, singleton table BFs=1,t=1 gives P_t(N<=K)=3/4,A=4/5, and log(5/4)<log(4/3). E2's own upper bound for pi0 is correct. The source's o(1) ceiling additionally needs P_t(N<=K)->1; it is not a finite-data conclusion without a tail bound.

N's rotational-invariance proof is correct only under its strong explicit independence premise. Two correlated Gaussian nulls, both independent of truths and response, refute the parenthetical implication that zero truth correlations imply independence of (y,X_-l). Conditional on the other null, the first has a nonzero conditional mean. Conditioning only on y recovers the marginal Beta law; conditioning on the selected partition or all X_-l requires a separate argument.

N1's singleton bound does not control a multi-variable block. Its exact two-variable expected count is (t r1+t r2+2t^2 r12)/(1+t r1+t r2+t^2 r12). Strong joint fit can make this close to two while t(r1+r2) is small. For orthogonal columns with singleton fit fractions x in (0,1/2), r12/r1^2=[(1-x)^2/(1-2x)]^nu grows exponentially; choosing t r1 small but t^2 r12 large gives the violation. Gaussian null designs/responses have full support around such configurations. This is an ERROR in the pointwise expectation bound; the 'iid-like' heavy-tail rate remains GAP without a specified growth regime and dependence control.

S's proof counts assignments, not supports. With two replaceable truths and the same three eligible null blocks, it claims at least (1+3)(1+2)=12 distinct supports; only 1+6+3=10 distinct replacement supports exist. Swapping the assignment of two chosen nulls changes no support. This is a counterexample to injectivity, not a counterexample to the final BB inequality; verdict GAP. A safe repair is to count distinct missing-truth/null-block pairs admitting a matching, once each. A simpler weaker ceiling is pi0(S0)<=1/(1+max_j M_j), using just one truth's replacements. Do not retain the product denominator without a new proof.

## Separation, partition and stage counts

SEP(A): conditional miss probability is (1-pi0(S0))^Q. With pi0(S0)=Qstar^-1 exp(O_P(1)), Q/Qstar tending to zero or infinity yields the two sides by bounded convergence; table discovery must be excluded by the imported partition event. SEP(B): chi-square >= pi(S0)^2/pi0(S0)-1, KL >= pi(S0)log(1/pi0(S0))-log 2, and the iid truth-indicator relative variance is (1/pi0(S0)-1)/Q. On no truth draw, both normalized and unnormalized estimates vanish. These are VERIFIED conditional implications; they do not independently discharge the LH statistical premises or prove a PIP statement. GU's Schur-complement descent and extra-deletion comparison are coherent, but I leave its imported uniform score-comparison event as an explicit unfinished audit.

PART A: before the first nonlaminar merge, each group's merges follow its own dendrogram. The C* condition precludes merging a partial group with either another partial group or a union of completed groups. A2 uses its extra no-early-completed-union premise; without it the converse is not claimed. Laminarity plus gmax<=B<2gmin forces the cut and packing to preserve exactly the groups. A global within/cross margin implies C*. For B-exact, a union bound over within and cross correlation failures suffices, using the regression representation T=(Z+a sqrt(W))/sqrt(V/(n-2)) and monotonicity in |a|. I have not certified the Hotelling-density normalization/exponent convention needed for L2 and B-explicit; those numerical constants remain out of LOCKABLE. The source's incidental exact-branch cutoff claim is not adopted.

STAGES M: after transforming temperature to log odds s in [-A0,A1], accepted early steps can shrink distance to a fixed extrapolated log-odds level at most geometrically. A halving construction reaches a bounded central window in log2 A0+O(1) steps; bounded curvature crosses that window in O(1); from s>=log 9 one final jump is valid. Thus the ideal two-state order is VERIFIED uniformly for A1>=2.2. The displayed decimal finite bounds are GAP: the supplied lower argument gives 2-log2(sigma3+5+2c exp(3)), approximately -0.955, with sigma3=log(exp(c+2exp(-3))-1), not the rounded stronger -0.95. Keep exact constants and recheck the upper rounding too. General-family transfer requires PAIR on [0,2]; actual-grid transfer requires pilot/candidate/bisection control. Neither is supplied by the two-state theorem.

## Weight stability: restricted affirmative verdict

I checked O-WSTAB REPORT sections 3.5-3.7 against the helper's analysis. Under H-ORTH, D_S=n^|S| and fit fractions add. Convexly moving each deletion interval rightward proves SEP's F2; the prior ratios are bounded by (2p)^m(s0+e)!/(s0! p^e). Summation yields the separable geometric bound. The common null coefficient error is O_P(n^-1/2+p/n); its product with log p vanishes under p log p=o(n). Truncating max Z_j^2 at 2 log p and integrating exp(Z^2/2) up to that point gives one uniform O_P(p sqrt(log p)) bound, proving W(a,b). The largest null in a truth-free block yields W(c). Its contribution dominates endpoint defects by p^r/polylog(p), justifying the subtraction in W(d); the upper half requires the explicitly stronger p^r sqrt(log p)/sqrt(n)->0.

For W(e), choose k=floor(exp((L_n-C1-1)/r)); it diverges but stays <=sqrt(n). The k-th order-statistic lower-tail event holds with probability tending to one, and the Taylor error O_P(k log^2 p/n) vanishes. The factorial prior gain produces the stated multi-extra lower bound. W(f)'s TV bound follows from common-atom concentration; the tilted KL bound at theta=1/log p plus W(b) gives O_P((log p)^(3/2)/sqrt(n)). W prime brackets the sublevel endpoint near G_n=log n/(2r log p); G_n>1/(2r)>1/2 implies at most two ideal steps. Strict 2Ar<1 and >1 give one and two, respectively; equality is not resolved. W(g), outside the authoritative a-f list, is not included in this verdict.

These statements require exact ORTH, fixed nonzero signals, bounded blocks, p->infinity and p log p=o(n). They establish neither general correlated-block BO nor the empirical pilot/candidate grid. No original OPEN extension is upgraded.

## Additional requested items and remaining work

O-SWAP rates: GAP. Its projection remainder formula is an exact algebraic identity, but replacing the fitted energy W_S0 by its expectation is an additional approximation beyond PA. In Proposition 2 the exact PA event uses E+W_S0/(n+1)+btilde, whereas the displayed law uses deterministic Omega0. W_S0 is a nondegenerate noncentral chi-square quantity; varying the Gaussian component in span(X_S0) changes the exact threshold while keeping the orthogonal residual components fixed. Thus the displayed event identity is ERROR if asserted under PA alone. Restore the random fitted-energy term and integrate it, or explicitly label the extra approximation. A random Gaussian quadratic-form error is not uniformly bounded by 10^-3 nats merely because a typical error is small. The predicted aggregate rates and regenerated-data agreement require a separate saved-output/data-provenance audit; they are not LOCKABLE here.

W7-SEC T05/T33/T32(i): GAP meaning review incomplete, not a discovered counterexample. I read REPORT and the relevant score/local-search/stage code for other items, but did not audit PROOF_T05, PROOF_T33, the floating-point library hypotheses, or the complete cost recount. In particular I do not endorse 'numerical_failure impossible for every p,y' without its stated FP/NOUF/LIB/SMALL domain. These deferred items, GU's imported comparison lemma, PART L2 constants, and empirical rate validation are the next work; they must not inherit a VERIFIED label from this report.

## LOCKABLE (review recommendation only)

- O-CERT Lemma M; deterministic normalizer inequality and C1(c); C1(b) only as the explicit R1 statistical-output implication; C2 conditional PW2; exact C3 ratios and exact C4 inequalities; C5 strict-score event inclusion.
- F-MASKPIP M1-M2; M3 conditional means restricted to 0<kappa<1; N-a's corrected finite-index inequality. Exclude original M3 counterexample and unit-constant rate claim.
- O-PW2 A1-A4 and B1-B3, with fixed-calibration scope and explicit fixed-input qualification on asymptotic rates.
- O-DILUTE E and R; E1 for normalized BF tables; E2 with cap probability; N under its literal joint-independence premise. Exclude N1, S's product ceiling, DM's reversed size sign, and unsupported numerical predictions.
- W7-SEP A/B as conditional implications; W7-PART A and B-exact only.
- O-STAGES ideal two-state logarithmic order, excluding printed decimal constants and family/production transfer.
- O-WSTAB W(a-f) and W prime under H-ORTH and ideal-grid scope only.

No branch status, locked source, method, or registry was edited. All writes are under theory_campaign/A-REV9. No empirical table or chart is presented as freshly validated data.
