MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd

Proposals:

This is a better-statement review of the frozen v1.4, not a correctness review. All limits below are as n tends to infinity. Existing implementation premises, posterior-input qualifications and hypotheses not explicitly replaced remain in force. Paths beginning lemmas/ refer to this ticket. Example improvements belong in (C5), not in the design-agnostic theorem statements.

P1. Replace relative signal domination by an additive signal-width margin.

(i) Exact improvement. In (C1), replace (BM-W) by

    (sqrt(lambda_n) - d_n)/sqrt(log n) -> +infinity,
    lambda_n = (n-1) phi_0^2 theta_min*^2 / sigma^2.

All conclusions of (C1) remain. The same replacement works in Lemma TL-W whenever its addition-statistic hypothesis holds. A sharper, geometry-sensitive alternative replaces sqrt(lambda_n) by

    m_n = min_{(A,i) in the truth-removal family}
          |theta_i*| ||(I-P_A)x_i|| / sigma.

(ii) Proof/change. In lemmas/L2_width.md section 4, keep the event B_n and identity (4.1). On B_n every signal-plus-noise absolute value is at least m_n-d_n-sqrt(2 log n). Its square divided by log n tends to infinity under the proposed condition. Subtracting at most (2A+2) log n for a swap still leaves RSS_A-RSS_T much larger than log n. The existing score comparison then gives TL. Replace only the paragraph labelled Size and its final invocation of lambda_n/log n in Score; L3 assembly is unchanged. The old assumption implies the new one, whereas the new condition allows sqrt(lambda_n)/d_n to tend to a constant greater than one (even to one with a sufficient additive margin) when d_n is large. No weakening of T1-F's own beta-min assumption is claimed.

(iii) Confidence: HIGH. Main risk: the alternative m_n must include swaps as well as deletions, with the actual coefficient for each removed truth. The conservative lambda_n version avoids that bookkeeping.

(iv) Class: ADOPT NOW.

P2. Recover the full Gaussian-concentration exponent in (C3).

(i) Exact improvement. Under (C3)(a), with s_n=-w_n^0 -> infinity,

    P(Z_n^c) <= exp(-s_n^2/2 + O(1)),
    P(NA(L)^c) <= exp(-s_n^2/2 + O(1)) + P(E_n^c).

Under (C3)(b), with s_n=w_n^0 -> infinity,

    P(NA(L)) <= exp(-(1-o(1))s_n^2/2) + P(E_n^c).

Under (W-delta), the first bound in particular is

    P(Z_n^c) = O(n^{-delta_0^2/[8(2A+2)]}),

improving the displayed exponent by a factor of four. These are asymptotic bounds, not a proposed finite-n theorem.

(ii) Proof/change. In lemmas/L2_width.md section 1 put D=4 kappa_E+2 and

    e_n = max_{(T,l) in P} [a_n^0(|T|)-sqrt(a_n^0(|T|)^2-D)].

For large n, e_n=O(1/sqrt(log n)); Phi_n^0 <= -e_n implies Z_n. Concentrate at -e_n rather than at -s_n/2 to obtain exp(-(s_n-e_n)^2/2). The proof already shows s_n <= min_P a_n^0=O(sqrt(log n)), so the exponent is -s_n^2/2+O(1). For the converse in section 2, the written lower score bound is positive whenever Phi_n^0 >= C/sqrt(log n), for a sufficiently large fixed C: substitute Z>=a+C/sqrt(log n) and use n^{-1/3}a^2=o(1). Lower-tail concentration gives exp(-(s_n-C/sqrt(log n))^2/2). Since s_n diverges, this has the stated relative exponent. Conditional versions pass through L5 section 1 with the design-event failure probability retained.

(iii) Confidence: HIGH. Main risk: claiming the additive O(1) exponent error for the positive-gap converse without a bound on the positive gap; the proposal intentionally uses a relative o(1) there. Empty pair families remain vacuous.

(iv) Class: ADOPT NOW.

P3. Remove the unnecessary fixed-power envelope from the standalone lattice lemmas.

(i) Exact improvement. In (C3)(a),(b), replace “|Q| <= n^b for some fixed b<1” by

    |Q| log n/n -> 0,

retaining |Q|<=K, all other assumptions and the same conclusions. Lemma TL-W, with either its existing signal condition or P1, has this same size range. This does not extend the full reporting theorem to b>=1/2.

(ii) Proof/change. lemmas/L0_toolkit_b.md section 4(ii) verifies its hypotheses under precisely q log n/n -> 0. This is already the standing hypothesis (F0) of lemmas/L2_width.md. Sections 1, 2 and 4 use no fixed b. Only the statement wrapper needs broadening; L1 and L4 sandwich budgets are left intact. For example, q of order n/(log n)^2 lies in this extension without lying under any fixed power n^b, b<1.

(iii) Confidence: HIGH. Main risk: accidentally applying this larger range to (C3)(c)'s power-budget corollaries or to the sandwich; neither extension is proposed.

(iv) Class: ADOPT NOW.

P4. Spend the unused entropy budget in the Gaussian-row lattice reference condition.

(i) Exact improvement. In the sufficient condition (D-R^b) for (W-R), permit

    log N_n <= log p + h log n + o(log n),
    h >= 0 fixed, h+b < 1/2,

instead of h=0. Keep fixed frame dimension and all other reference/atom conditions. Then (W-delta) on the realised design holds with probability tending to one for every fixed

    0 < delta_0 < 1-2b-2h.

Correspondingly, (D-loc^b) can replace nu_n=o(log n) by

    nu_n log 2 <= h log n + o(log n), h+b<1/2.

All conclusions of (C2) follow when this enlarged sufficient condition supplies (W-R).

(ii) Proof/change. In lemmas/L5_formR.md P9a Step 2 retain the same frame tail event with x'_n=2 log N_n+(m_0+2)log log n. Steps 3-5 now give max Z^2 <= 2 log p+2h log n+o(log n); sample/population errors are unchanged. In P9 replace gamma=1-2b-delta_0 by 1-2b-2h-delta_0>0. The conditional mean argument is identical. The D-loc proof already counts at most p 2^{nu_n} frames, so only its last entropy comparison changes.

(iii) Confidence: HIGH. Main risk: confusing this h, which counts lattice reference frames, with 15rho, which counts sandwich conditioning sets. Both budgets must be satisfied separately.

(iv) Class: ADOPT NOW.

P5. State a direct quantitative reference budget, allowing growing frame dimension and non-negligible approximation errors.

(i) Exact improvement. In (C3)(c), retain the decomposition in (W-ref), but allow deterministic dimension bound m_n and arbitrary nonnegative approximation bounds eta_n,L_n,rho_n. Define, with the atom term zero for an empty atom set,

    B_n = (1+eta_n)(sqrt(m_n)+sqrt(2 log |V_n|))
          + L_n sqrt(2 log(2|A_n|))
          + rho_n(sqrt(q+1)+sqrt(2 log p)).

Replace its separate fixed-dimension, entropy and vanishing-error budgets by the single sufficient condition

    min_{(T,l) in P} a_n^0(|T|) - B_n -> +infinity.

Then (W) holds. The old (W-ref) remains a corollary. In particular, with its original strict h+b<1/2 budget, m_n=o(log n) is allowed in place of fixed m_0. Small nonvanishing relative errors are also allowed whenever the displayed budget remains positive with a diverging margin.

(ii) Proof/change. The first bound in lemmas/L2_width.md section 3(iv) is exactly E max_P |u'g| <= B_n; hence w_n^0 <= B_n-min_P a_n^0. No new probabilistic estimate is needed. The original hypotheses make B_n <= sqrt(2 log p+2h log n)+o(sqrt(log n)), so imply the proposed condition. Handle an empty pair family separately, as already done in the statement. This proposal avoids forcing every approximation term to be little-o when a fixed fraction of the available margin would suffice.

(iii) Confidence: HIGH. Main risk: the reference decomposition, unit-atom requirement and subspace restriction on the remainder remain essential; the scalar budget replaces only their size bounds, not those structural conditions.

(iv) Class: ADOPT NOW.

P6. Allow a sufficiently small fixed leak at the exact Gaussian-row noise scale.

(i) Exact improvement to pursue. There is a finite D depending only on the fixed regularity constants A,c,s_0,theta_hi,sigma (not on b,rho,kappa) such that (C2) remains valid if its leak condition is replaced by

    varpi_n <= kappa sqrt(log n/n), 0<=kappa<=1 fixed,
    b+15rho+D kappa < 1/2,

with r_n->0 and the other assumptions unchanged. This is a non-sharp frontier, not a claim that D is optimal.

(ii) Proof/change. In lemmas/L4_sandR_b.md Lemma 2, zeta_n becomes O(kappa sqrt(log n/n))+o(sqrt(log n/n)); the comparison on sqrt(h) costs C_2 kappa sqrt(log n)+o(sqrt(log n)). The proof's constants can be chosen uniformly for kappa<=1, since it only needs varpi_n<=sqrt(log n/n) to bound the unshifted correlations. Lemma 3's mean norm is now O(kappa sqrt(log n)); its denominator comparison still works, and its tail incurs exp(C_3 kappa log n). In Lemma 4 use t'=(sqrt(t)-C_2 vartheta_n)_+^2 and t'>=t-2 C_2 vartheta_n sqrt(t), avoiding the current unnecessary positive-root restriction. For a sufficiently enlarged fixed D this gives the same count with exponent -t/2+(D kappa+o(1))log n. Replace 15rho by 15rho+D kappa in (4.2), the ladder, the choice of T_n and section 6(b). The claimed budget leaves positive slack in every step. L5 does not change.

(iii) Confidence: HIGH for existence of a conservative D; MEDIUM for any sharp frontier. Main risk: tracking one uniform D through the reference comparison and the full threshold interval rather than silently retaining an o(log n) loss. This is already suggested by L4 section 7(4); the proposal specifies a usable statement and the missing proof edits.

(iv) Class: WORTH A TICKET.

P7. Extend the equicorrelated example to b<3/8, and separate the width obstruction above it.

(i) Exact improvement to pursue, confined to (C5)/L6 E5. For the existing construction with p=floor(n/3), q=floor(n^b), fixed a in (0,1) and fixed nonzero truth, (W), and hence all the existing reporting conclusions, hold for 0<b<3/8. For 3/8<b<1/2 the same construction has w_n^0 -> +infinity, so whole-lattice NA fails with probability tending to one. The latter is not a failure theorem for the reported model. No claim at b=3/8.

(ii) Proof/change. Keep the exact residual formula in lemmas/L6_examples.md E5, but compare to a_n^0(t) at each t instead of minimising the level before maximising the projections. Apart from the common O_P(1) g_0 term, its absolute projection is bounded by

    max_{j<=q}|g_j| + max_{|T|=t} |sum_{j in T}g_j|/t.

The second term has mean at most sqrt(2 log(2 binom(q,t))/t). For t=n^{u+o(1)}, this gives leading coefficient sqrt(2b)+sqrt(2(b-u)) in units sqrt(log n), against level sqrt(3-2u). Their squared difference has sign determined by

    4b+4 sqrt(b(b-u)) < 3,

which holds uniformly for 0<=u<=b when b<3/8. To make this uniform without an extra sqrt(log q) loss, split t<=n^epsilon (use the original bound 2 max|g_j| and the small-size level) from t>n^epsilon. On the latter range the subset-average maximum is 1/sqrt(t)-Lipschitz, so a union over t costs only O(sqrt(log q/n^epsilon)) in its concentration error. Choose epsilon small using the strict b<3/8 margin. Outside-Q directions have maximum sqrt(2 log n)+o_P(sqrt(log n)) and minimum level sqrt((3-2b)log n)+O(1), leaving slack for b<1/2. Gaussian tail integration turns these bounds into a negative expected gap of order sqrt(log n).

For the positive-gap half, choose t tending to infinity subpolynomially (e.g. ceil(log q)); include truth 1, take the other t-1 indices among the most negative g_j, and choose l with maximal positive g_l outside T. Gaussian order statistics give both extremes at sqrt(2 log q)(1+o_P(1)); t A_t->1 and v_t->1-a. Thus this particular projection is (2 sqrt(2b)+o_P(1))sqrt(log n), whereas its level is (sqrt(3)+o(1))sqrt(log n). Control expectations by the existing Gaussian maximum envelope. This yields a positive gap for b>3/8. These sketches develop the open direction explicitly recorded in SHARPNESS section 4; no other review file was consulted.

(iii) Confidence: HIGH for the strict ranges; endpoint unresolved. Main risk: establishing uniformity over subset sizes and expectation control, and retaining the required truth in the lower-bound subset. A proof merely using (5.2) cannot justify the extension.

(iv) Class: WORTH A TICKET.

No credible improvement:

- General b>=1/2 in (C1)/(C2): no credible extension of the full reporting theorem from these arguments. P3 concerns only lattice lemmas. The sandwich exclusion margins and, for Form R's supplied sufficient condition, the sample/population comparison still bind. The observed LS0 successes do not prove cap-controlled asymptotic descent.
- Removing the lattice-width condition: no credible short extension. An improving addition away from the realised path need not matter, but the present assembly explicitly consumes whole-lattice NA; a path argument with swap and cap accounting is missing.
- Bounded-gap regime: no universal zero-one conclusion follows from the mean gap and unit Lipschitz concentration alone. P2 improves tails but does not establish necessity of negative divergence or classify bounded gaps.
- Count n^{15rho}: no uniform reduction of 15 is justified for arbitrary X-measurable partitions and every conditioning set of size at most 15. The number of such subsets can have this order. An actual smaller reference-family count could be substituted, but no mechanism here ensures it. P4 changes a different entropy budget.
- Conditioning size 15: it is the worst case of a shipped block of size 16. Smaller actual blocks permit the corresponding smaller conditioning size and reference count by the same proof, but do not weaken the theorem for all allowed partitions. No method change is proposed.
- Gaussian-row leak scale kappa sqrt(log n/n): a credible conservative extension is P6; no credible sharp analogue of beta(eta,A) is obtained by the existing norm and comparison inequalities.
- Polynomial-decay cutoff alpha>2 in (C5): no credible few-line improvement using the supplied Lemma IR. Its inverse/regression envelope (1+d)^{1-alpha} log(2+d)^{alpha-1} is not summable at alpha<=2; improving only bounded-conditioning leakage does not repair this. Extending to alpha>1 would require a sharper uniform inverse-decay result, including arbitrary principal subsets and the refitting bound. I do not count an unproved replacement of that input as an adoptable proposal.
- Equicorrelation beyond b=3/10: P7 gives a credible route to b<3/8; no credible whole-lattice extension to b>3/8, and no assertion about the endpoint or path-level reporting there.
- A rate for the reported-model event: the existing assembly yields P(G_n^c)<=P(pi(S_0)<=1/2)+P(Sand^c)+P(NA^c)+P(TL^c), or its bound by 2 E[1-pi(S_0)] plus search failures. L1's maximum tail can be made polynomial and P2 sharpens the lattice term, but O_P(sqrt(log n/n)) for posterior error does not itself give a polynomial expectation or fixed-threshold tail rate. Bare (W-R) likewise supplies no rate for its design event. No universal polynomial reporting rate, or delivery rate, is justified without new quantitative input.
- Removing T1/POST, the spectral floors, or visibility: no credible unconditional replacement from these proofs. POST is stronger than the final-score-ranking property used by the assembly, but merely substituting that unverified property would not establish a new primitive theorem. Visibility could be assigned sufficient fixed constants using the proof's margins, but no sharp constant or material joint gain over the retained T1 hypotheses is established here.
- Form F eta/b frontier: no general larger fixed-exponent range is justified by the written maximum-based argument. Replacing the upper envelope A by a tighter known envelope for log p/log n is already available by choosing A appropriately; a leak-profile theorem needs additional work beyond this review's concrete proposals.
- Existing conclusion uniformity, archive certificate and move count: every admissible output run, every seed and calibration outcome, and the exact deletion count are already harvested. Nothing stronger about delivery or the old move cap follows.

Summary line: 5 ADOPT NOW / 2 WORTH A TICKET / 0 SPECULATIVE.
