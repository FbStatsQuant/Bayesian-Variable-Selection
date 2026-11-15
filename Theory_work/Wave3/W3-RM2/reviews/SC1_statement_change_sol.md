MANIFEST 9af7889ee7da1292df93b4e802ce07e440a12e18c115428c33749bfd9fdae3dc

Hunks: numbered, classified (a)/(b)/(c)/(d).

Compared the complete locked v1.2 text with v1.3 using `git diff --no-index`. The following are ALL 14 unified-diff hunks (three context lines); coordinates are old -> new. Mixed hunks are split by content below. No (d) change was found. Code pins, posterior inputs, leakage budgets, and implementation premises are unchanged.

1. `-1,7 -> +1,13`: (c), version/header and adoption history; records the two changes and containment claim.
2. `-19,11 -> +25,12`: (a), BM-Q becomes BM-W in the summary; (b), diverging-gap description and opposite-divergence route converse replace the fractional-slack description.
3. `-58,16 -> +65,25`: (b), defines a0, w0, retains a_delta and w_delta, removes the old plus-level notation, and adds the uniform level-gap inequality; (a), adds the complete deletion/swap truth-removal family, d_n, its subspace inclusion and explicit upper bound.
4. `-85,7 -> +101,8`: (b), delta0 is needed only for the named fixed-fraction sufficient form.
5. `-101,13 -> +118,17`: (a), replaces BM-Q by BM-W and records BM-Q/BM-infinity sufficiency; (b), replaces W, names W-delta, and redirects W-unif and the other sufficient forms through W-delta.
6. `-141,10 -> +162,11`: (b), replaces the random-design fixed-fraction event by a deterministic diverging t_n with high-probability design control; records the old sufficient event and retains its D-R-b quantifiers.
7. `-153,7 -> +175,7`: (a), C1 assumes BM-W.
8. `-166,20 -> +188,26`: (b), C3 defines the common threshold/event, gives the two concentration bounds and c*, states the old converse as a special case, and updates the sufficient chains; (a), C4 explicitly supplies BM-W from the parent hypotheses. The RM-R containment sentence is retained.
9. `-189,14 -> +217,14`: (a), P2 replaces its signal hypothesis and generic contrast argument by the full truth-removal width argument with a uniform addition-noise premise; P8 derives BM-W from fixed coefficient bounds. (b), P3 adds the NA rate, P5 labels the divergence converse, and P9 explicitly delivers the old sufficient conditional-width event before W-R. P0, P1, P4, P6, P7 and P10 are unchanged.
10. `-215,7 -> +243,12`: (c), adds the limits observation. This permitted record addition needs the scope correction below.
11. `-243,11 -> +276,13`: (b), replaces the old approximate-equivalence wording by the two divergence regimes and explicitly excludes the bounded-gap regime and a reported-model failure rate; (a), changes BM-Q to BM-W in the necessity exclusion.
12. `-256,6 -> +291,9`: (c), adds CANDIDATE ingest state and CP3 supersession decision.
13. `-265,19 -> +303,19`: (a), fixed-design registry assumption/sharpness becomes BM-W; (b), A:W records w0 -> -infinity and qualified route sharpness; (c), both theorem status_source references become 4-10. The R assumption row remains unchanged and therefore retains an obsolete event reference: required change 3.
14. `-289,33 -> +327,33`: (c), all remaining status_source references become 4-10; (b), W-suff adds W-delta and redirects the alternatives through it; (a), adds BM-Q => BM-W to the implication record. Other dependency edges and D-to-W alternatives are unchanged.

Checks: per item of the task, what was verified and how.

1. Freeze and scope.

Manifest verification returned exactly:
`verify: OK MANIFEST 9af7889ee7da1292df93b4e802ce07e440a12e18c115428c33749bfd9fdae3dc`.
Read the authorized locked statement, current statement, assumption map, plan/brief, proposal/disposition, numerical results and addendum README, and relevant manifest-listed parent/toolkit/NA-R sources. No LOG, CHECKPOINT, other review, or memo-worktree material was read. The detailed BRIEF.md operational instructions are lead instructions, not an expansion of this review's expressly limited brief.

2. BM-Q => BM-W, with constants: PASS.

For a deletion, A union {i}=T subset Q. For a swap, A union {i}=T union {l} subset Q union {l}. Thus interlacing of FL-Q makes X_A and X_{A union {i}} full rank and the residual nonzero. Moreover u_{A,i} is a linear combination of x_i and X_A, so belongs to span(X_{Q union {l}}). Deletion directions belong to span(X_Q), covered by choosing any l in Q (Q is nonempty). There are at most p covering subspaces, of rank at most q+1.

For their projectors Pi_l, |v'g| <= ||Pi_l g||. Each norm is 1-Lipschitz and has expectation at most sqrt(q+1). The sub-Gaussian maximum bound gives E max_l ||Pi_l g|| <= sqrt(q+1)+sqrt(2 log p); the displayed sqrt(2 log(2p)) is a valid looser bound, including p=1. Squaring gives exactly the advertised d_n^2 <= 2(q+1)+4 log(2p). For n>=3, this implies

    d_n^2+log n <= [5+4A+4 log(2)/log(3)](q+log n).

Consequently the BM-W ratio is at least (1-1/n)/[5+4A+4 log(2)/log(3)] times the BM-Q ratio, and diverges. If d_n^2=O(log n), BM-W is equivalent to BM-infinity with the same fixed sigma and phi0, since its denominator is bounded above and below by constant multiples of log n and (n-1)/n -> 1. Orthogonal columns give a useful non-refutation test: d_n is bounded for fixed s0 even for polynomial q, so weakening the signal floor is real.

3. W-delta => W and sufficient/containment chains: PASS.

Put L=log n. For n>=3 and k<p, a0^2-a_delta^2=delta L+log(1+1/n)>=delta L. Both levels are at most sqrt((2A+2)L), since log(n+1)<=2L and log p<=A L. Rationalizing therefore gives precisely

    a0-a_delta >= delta sqrt(L)/(2 sqrt(2A+2)).

Subtract the uniform positive gap inside the maximum and take expectations, with the stated empty-family convention. The direction of the inequality is correct.

For W-unif, k<=q<=n^b gives log(k+1)<=bL+log 2. The smallest a_delta(k)^2 is at least 2 log p+(1-2b-delta)L-2 log 2. Its difference from the W-unif squared bound is delta L-2 log 2>0 eventually; hence W-unif implies W-delta with delta0=delta.

For W-chi, the GROW L2.3(a) common projection decomposition gives max Z^2 <= max of at most p normal squares plus chi^2_{q-s0}. Taking expectations (using Gaussian maximum and chi-square maximum estimates, then Jensen) yields E max Z^2 <= 2 log p+(1-delta1)L+o(L). As q=O(L), the smallest a_delta0(k)^2 equals at least 2 log p+(1-delta0)L-O(log L). For delta0<delta1 this gives E max(|Z|-a_delta0)<=0 eventually. The sets of pairs restricted to k<K only make this easier.

For W-ref, the reference contribution is at most sqrt(2 log p+2hL)+o(sqrt L), since m0 is fixed and eta_n->0. The atom maximum times L_n is o(sqrt L), and the remainder is bounded in expectation by rho_n[sqrt(q+1)+sqrt(2 log(2p))]=o(sqrt L). With delta=(1-2b-2h)/4>0, the W-unif squared budget exceeds the leading reference squared budget by (1-2b-2h)L/2, a strict positive margin. For W-loc, write the residual as its N_l-reference minus X_Q times the difference of zero-padded regression coefficients, and divide by its residual norm. FL-Q gives the atom coefficient sum <=L_n/phi0; the reference norm is <=sqrt(1+eta_n). The reference count is <=p 2^{nu_n}, m0=1 and rho_n=0. These are the advertised chains.

For RM-F, polylog q fits n^b for any fixed positive b eventually. Select b<min(beta(eta,A),1/2-h). N-D(i) supplies the W-ref reference lines, with unit v and remainder in span(X_{Q union {l}}). N-D(ii) supplies BM-Q and hence BM-W. Under N-chi, q=O(log n) gives d_n^2=O(log n), and T1-F's BM-infinity suffices. For RM-R, choose positive b,rho sufficiently small that 15rho+b<1/2; polylog Q and H fit these budgets, and D-R supplies P9. Thus C4's mathematical containment, including the BM chain, survives the changes.

4. C3(a) and the explicit rate: PASS.

For nonempty P, let H(g)=max_P(|u'g|-a0(k)) and m=-E H=-w0. H is 1-Lipschitz. Let C=4 kappa_E+2>0 and a_min=min_P a0>=sqrt L. Eventually all c_n(k)>0 and

    e_n=max_P[a0(k)-sqrt(a0(k)^2-C)] <= C/sqrt L -> 0.

Choose n0 so that m>0 and e_n<=m/2, in addition to the toolkit/score requirements. A violation of Z_n implies H>-e_n, so Gaussian upper concentration gives P(Z_n^c)<=exp(-(m-e_n)^2/2)<=exp(-m^2/8). No independence across pairs or between events is used. If P is empty, Z_n and NA are sure, w0=-infinity and the exponential is read as zero; no finite-valued concentration argument is applied in that case.

There is no hidden requirement that m be smaller than the smallest level: for nonempty P, choosing a pair attaining a_min gives E H>=sqrt(2/pi)-a_min, hence m<=a_min-sqrt(2/pi). In any event the proof uses the additive correction e_n, not the potentially negative level a0-m.

On the toolkit event use the exact prior upper bound log((k+1)/(2p-1-k))<=log(k+1)-log p. The likelihood upper bound is Z^2/2+1/2 uniformly when Z^2<=c_n(k)=O(L); its excess vanishes because omega_n L->0. With remainder <=2 kappa_E, the score increment is <=-1/2. Thus the stated event-to-NA implication is valid.

Under W-delta, m>=delta0 sqrt L/(2 sqrt(2A+2)), and m^2/8>=delta0^2 L/[32(2A+2)]. The displayed c* is correct. For the bare concentration bound n0 depends on kappa_E and the divergence envelope of m (or delta0 for W-delta); for score conversion it also depends on A, sigma, M, phi0, the toolkit rate envelopes, and b through q<=n^b. A universal n0 independent of the divergence envelope is not justified, but none is asserted in v1.3.

5. C3(b), including the opposite gap and old converse: PASS.

Let m=w0->+infinity. Gaussian lower concentration gives P(H<m/2)<=exp(-m^2/8). Off that exceptional event some feasible addition pair has |Z|>=a0(k)+m/2. For T containing S0, RSS_T=||(C-P_T)epsilon||^2<=||C epsilon||^2. On D1 put alpha_n=2 nu sigma^2/||C epsilon||^2; alpha_n>=1-r_n with r_n=O(n^(-1/3)), so r_n L->0. The lower prior ratio is (k+1)/(2p-1-k)>=(k+1)/(2p). Since -log(1-x)>=x and RSS_T>0, the score increment satisfies

    F(T+l)-F(T) >= [alpha_n Z^2-a0(k)^2]/2-log 2-2 kappa_E.

The right side is positive eventually at the witness: alpha_n(a+m/2)^2-a^2 >= -r_n a^2+(a m+m^2/4)/2 -> infinity, using a>=sqrt L and a^2<= (2A+2)L. This works even if m is much larger than a; no Taylor upper bound on Z is used for the converse. Hence NA is impossible outside the union of the toolkit failure and the lower-concentration exception, exactly as claimed.

For the v1.2 plus-level a_plus, a_plus^2-a0^2=delta1 L+2 log 2-log(1+1/n)>=delta1 L eventually. Rationalizing with both levels bounded by sqrt((2A+3)L) gives a_plus-a0>=delta1 sqrt L/[2 sqrt(2A+3)] eventually. The old nonnegative expected plus-gap therefore implies w0>=that positive diverging quantity. Its parenthetical treatment is correct. Neither direction decides bounded gaps or establishes necessity for reported-model success.

6. P2 truth removal, including |T|=K: PASS.

For a swap put B=T union {l}=A union {i}. Since T contains S0, residualizing Y on A gives u_{A,i}'Y=theta_i||(I-P_A)x_i||+sigma Z_{A,i}, while u_{T,l}'Y=sigma Z_{T,l}. Compute RSS_A-RSS_B and RSS_T-RSS_B by these one-dimensional projection identities and subtract. This proves the displayed identity for either sign of theta_i. Deletions give the first square alone.

The Schur complement gives ||(I-P_A)x_i||^2>=(n-1)phi0^2. Gaussian concentration gives sup_D |v'epsilon|/sigma <=d_n+sqrt(2r log n) except with probability n^(-r), for any fixed r>0. Put lambda=(n-1)phi0^2 theta_min^2/sigma^2. BM-W makes this supremum o(sqrt lambda) and log n=o(lambda). Thus the first square is at least sigma^2 lambda/4 eventually and subtraction of sigma^2(2A+2)log n leaves at least sigma^2 lambda/8. Consequently RSS_A-RSS_T>= (n-1)phi0^2 theta_min^2/8, hence at least n phi0^2 theta_min^2/16 eventually.

The retained toolkit controls score regularity and RSS ceilings. GROW L2.1's score comparison now gives F(A)-F(T)<=(A+1)log n+O(1)-(RSS_A-RSS_T)/(2C_R)<0. It does not charge an O(q) contrast error against the weakened signal.

For k<K, P3 gives Z^2<=c_n(k)<=(2A+2)log n eventually. A lattice set with k=K must equal Q, so at most p extra normal variables cover all remaining (Q,l) pairs; their probability of exceeding (2A+2)log n is <=2p n^(-(A+1))<=2/n. FL-Q defines these directions even when the auxiliary B has K+1 members: B is an algebraic regression set, not a scored feasible model. The family D contains every removal direction used, including all swaps; feasible truth-removing neighbours are deletions or swaps, since an addition cannot remove a truth.

7. W-R, C2, P8, P9: mathematical PASS; registry correction required.

The deterministic t_n condition in W-R permits direct conditional use of C3(a): on the good design event the conditional NA error is <=exp(-t_n^2/8)+the toolkit error. Conditional truth-removal bounds are uniform on the same Gram event. With fixed theta_lo, theta_hi and s0, ||mu||^2<=s0^2 theta_hi^2(n-1), while d_n^2=O(q+log n)=o(n), so BM-W holds uniformly there. The entrywise Gram error times q vanishes for b<1/2. Integrating gives the joint-law C2/P8 conclusions.

For P9, NA-R's population/frame proof can be re-run with sample/population additive error O((q+log n)/sqrt n)=o(1). It gives a joint-law upper bound max|Z|<=sqrt(2 log p+o(log n)). For any fixed delta0<1-2b, the minimum a_delta0(k) exceeds this level by a constant times sqrt(log n). To pass to conditional means, use Markov on the conditional failure probability, then a conditional median-to-mean bound for the 1-Lipschitz maximum. The O(1) median/mean difference is absorbed by that diverging margin. This supplies the explicitly stated fixed-delta design event, which implies W-R by the already checked level gap. No polynomial rate for the probability of that design event is implicit.

8. Records and numerical limits.

The new A:BM-W and A:W registry formulas match the mathematical statement. The W-suff alternatives correctly express separate sufficient hypotheses; its BM-Q implication is independently verified above, rather than treating BM-Q as a sufficient condition for W. The CANDIDATE/CP3 note records state without claiming a proof or completed supersession. The fixed-design sharpness text properly qualifies the positive-divergence obstruction and leaves bounded gaps undecided. However the R assumption still refers to W_n, deleted from section 3.2, and the unqualified binding/old R sharpness labels need the same divergence qualifications (required changes 3-4).

The two [v1.3] assumption-map rows correctly record BM-W, W, and the positive-gap obstruction. The later unharvested W-conv bullet also retains the removed w-plus notation (required change 3). Elsewhere the map's 'unharvested' rate bullet still claims a polynomial rate under the newly weaker W. It must be brought forward to the actual v1.3 rate; no fixed delta0 is part of bare W (required change 2).

RESULTS B4 records 3/5 cap failures for eta=1,n=1600; the authorized addendum supplies the sixth run and therefore 4/6, with failing swap counts 19,24,35,73 and successes 6,12. The combined start-size range is 522-743, not literally 520-740. Slack 15 is correct. The successful B1/B2/B4 probe summaries are consistent with the source counts, but the conditions are nominal and only an LS0 re-implementation was tested. In particular RESULTS sections 2-3 explicitly say the sampler/posterior/full reported-model method was not probed. Labeling the remark an observation does not make 'the conclusion can fail' evidence for reported-model failure: not reaching S0 in this LS0 probe need not imply the full method fails to report S0. Required change 1 preserves the observation and makes its precise scope explicit.

Required changes: numbered, classified, with location and exact text.

1. MAJOR ? STATEMENT.md (C6), lines 246-251: replace the entire new limits remark, starting at '**Limits remark' and ending 'item O1.', with:

   **Limits remark (an observation, not a claim; HQ CP1 decision):** in the boundary-violation LS0 probes (`numerics/RESULTS.md` B4 and `reviews/post_BT1_addendum/README.md`), at nominal outside-column leak level eta = 1 the validated LS0 re-implementation stopped at its shipped move cap before reaching S0 in 4 of 6 runs at n = 1600, p = 3200 (start sizes 522-743; failing runs made 19, 24, 35 and 73 swaps against cap slack ell_n + s0 = 15). The corresponding probes reached S0 in every run with b up to 0.75 (B1), with nominal width-condition violation (B2), and with eta <= 0.2 (B4). These observations concern LS0 from the start mode; the sampler, posterior input and full method's reported model were not tested, and no asymptotic failure follows. The cap obstruction motivates the path-level item O1.

2. MAJOR ? ASSUMPTION_MAP.md, lines 62-64: replace the entire first bullet under 'Unharvested conclusions' (ending 'no rate for [POST];', preserving the subsequent bullets) with:

   * The no-addition rate is now harvested in STATEMENT v1.3 (C3)(a): under (W), P(NA(L)^c) <= exp(-(w0_n)^2/8) + P(toolkit event fails) for all sufficiently large n. Under the stronger (W-delta), P(Z_n^c) <= n^(-c*), c* = delta0^2/[32(2A+2)]. Bare (W) supplies no fixed polynomial rate through this bound. For [SAND(Q)] the ladder gives O(sqrt(log n) n^(-xi)) plus 1/log n terms from the maxima (the latter can be made polynomial); no rate for [POST] or the common reporting event is claimed.

   Placement note: this replacement bullet explicitly identifies its rate as already harvested, even though the retained heading covers the other, still-unharvested bullets.

3. MINOR ? STATEMENT.md line 319, registry A:W-R field: replace the exact field

   `A:W-R (new | lattice width on the realised design | P(W_n) -> 1 | STATEMENT.md ?3.2 | shared yes | P8 F-to-R)`

   with

   `A:W-R (new | lattice width on the realised design | exists deterministic t_n -> infinity: P(W0_n intersect {w0_n <= -t_n}) -> 1 | STATEMENT.md ?3.2 | shared yes | P8 F-to-R)`.

   Also replace ASSUMPTION_MAP.md line 67's entire W-conv bullet, which uses the removed w-plus notation, with:

   `* W-conv in v1.3 (C3)(b) gives an improving addition at some feasible lattice set with probability tending to one when w0_n -> +infinity; this is a whole-lattice obstruction, not a path-level or reported-model failure statement.`

4. MINOR ? STATEMENT.md line 313 and line 324, and ASSUMPTION_MAP.md binding-map A:W bullet: qualify the route shorthand consistently. Replace the A:W clause of line 313 with

   `A:W route obstruction via Lemma W-conv: gap -> +infinity forces P(NA(Q)) -> 0; gap -> -infinity is sufficient; bounded gap undetermined [whole-lattice route only]`.

   Replace the A:W-R sharpness clause of line 324 with

   `A:W-R = ROUTE-OBSTRUCTION (target; conditional positive diverging width gaps obstruct whole-lattice no-addition; negative diverging gaps are sufficient; bounded gaps undetermined; no necessity for reporting claimed)`.

   Replace the assumption-map binding bullet beginning '* A:W' with

   `* A:W and P:NA(Q): negative diverging width gaps are sufficient; positive diverging gaps force failure of whole-lattice no-addition by W-conv (target); bounded gaps and necessity for reporting are undetermined.`

   Reason: C3(b) excludes positive divergence, but does not prove NA consistency requires negative divergence. These records must not strengthen the precisely qualified new converse into a necessity theorem.

Verdict: ACCEPT WITH CHANGES

The two adopted mathematical changes and their dependent mathematical bridges pass this statement-change review. The four repairs above are required before accepting the records as an accurate v1.3 target. No CRITICAL defect or mathematical refutation was found; no proof-completion certification is given.

Not checked:

* Full proofs of the still-target C1-C5/P0-P10, their future implementations, or any unasserted sharpness/necessity theorem.
* Exhaustive re-review of unchanged hypotheses, posterior results, engine proofs, registry status history, or production code behavior. Code pins were checked for equality across the statement diff; manifest verification checks file hashes, not correctness of all pinned source claims.
* Numerical reruns, numerical raw-row audits, binary64 behavior, sampler behavior, [POST], delivery, or the full method's empirical reported-model success/failure. Counts were checked against RESULTS and the authorized addendum README only.
* Existence/classification of all bounded-gap designs, an optimal concentration exponent, path-level guarantees without W, or the candidate example computations.
* Any forbidden LOG/CHECKPOINT/review/memo content. No external literature gate was attempted.
