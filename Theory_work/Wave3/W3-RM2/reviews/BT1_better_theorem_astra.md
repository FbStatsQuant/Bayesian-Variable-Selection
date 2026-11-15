MANIFEST 65ee6108be26dc13108a18e0b4a9032f25d3092c50bcc17044beb84730e6bec7

# BT1 — better-theorem review, W3-RM2

Scope: proposals only, against the frozen target. These are mathematical proof sketches, not certifications of the locked theorem. All hypotheses below concern (X, theta*) or (Sigma_n, theta*) and deterministic Q; none concerns the method's partition. No method change or path-level assumption is proposed. Existing toolkit and posterior inputs retain their recorded conditional status.

## P1 — Replace BM-Q by the Gaussian width of truth-removal directions

**Statement.** In STATEMENT §3.1 and (C1)/(P2), retain all other hypotheses, including (W), and replace (BM-Q) by the following condition. Define the deterministic unit-vector family

    D_n = {u_{A,i}: T in [S0,Q], i in S0,
            A = T\{i} or A = (T\{i}) union {l}, l outside T,
            A a feasible neighbour of T},
    d_n = E sup_{v in D_n} |v' g|,  g ~ N(0,I_n),
    lambda_n = (n-1) phi0^2 theta_min^2 / sigma^2.

Require

    lambda_n / (d_n^2 + log n) -> infinity.                  (BM-width)

Then [TL(Q)] and all (C1) conclusions still hold. In particular, if d_n = O(sqrt(log n)), BM-infinity suffices. Here the family MUST include directions after truth-removing swaps, not just truth deletions.

**Why strictly better.** There are at most s0(1+p)2^{q-s0} directions, so the elementary Gaussian maximum bound gives d_n^2 = O(q + log n). Consequently BM-Q implies BM-width without any new hypothesis. Conversely d_n can be O(1) while q is polynomial. For example, with orthogonal columns, truth-removal directions are just the s0 truth directions, even after a swap. Taking n theta_min^2 of order (log n)^2 and q of polynomial order separates the two signal requirements. This is already a strict improvement of the TL module; the full theorem continues to require its original T1-F and visibility hypotheses. The orthogonal example also has visibility of order n theta_min^2 and satisfies the addition-width condition. This is more than exchanging one unrelated assumption for another: it contains the old condition by a deterministic cardinality bound.

**Proof sketch.** Reuse Toolkit-b for uniform RSS upper/lower bounds and the bounded score remainders, but do NOT use its O(q) bound for the contrast RSS_A-RSS_T. That contrast has an exact two-square representation.

For a swap A=(T\{i}) union {l}, put B=T union {l}. Although B need not be feasible in a general version of the lemma, it is an algebraic regression set covered by the same Q union {l} floor; in (C1), q=o(K) makes this issue immaterial. Since T contains S0,

    RSS_A - RSS_T
      = (theta_i ||(I-P_A)x_i|| + sigma Z_{A,i})^2
          - sigma^2 Z_{T,l}^2.                            (1)

For a deletion the second term is absent. This follows by computing RSS_A-RSS_B and RSS_T-RSS_B separately. The Schur floor gives |theta_i| ||(I-P_A)x_i|| / sigma >= sqrt(lambda_n).

Gaussian concentration for the 1-Lipschitz supremum gives, for any fixed r>0,

    sup_{v in D_n} |v' epsilon|/sigma
       <= d_n + sqrt(2r log n)

except on an event of probability n^{-r}. On the addition-width event supplied by (W), uniformly Z_{T,l}^2 <= C_A log n. No independence of these two suprema is needed. By BM-width, the noise in the first square is o(sqrt(lambda_n)), and (1) is at least sigma^2 lambda_n/4 eventually, uniformly over truth-removing neighbours. The exact numerical fraction is immaterial.

Now use the score comparison in C-GROW L2.1, with the same C_R and kappa_E:

    F(A)-F(T) <= (A+1) log n + O(1)
                         - (RSS_A-RSS_T)/(2 C_R) < 0.

Thus [TL(Q)] follows. Toolkit-b still sees an exponentially large family, but its O(q) charge is used only to establish uniform regularity of scores/RSS, where q log n/n -> 0 suffices in the target range. It is no longer charged against the signal. New ingredient: the exact common-supermodel identity (1), replacing the generic contrast bound of RM L1_fixed, B3.

**Risk / refutation test.** Omitting swap directions would invalidate the argument: controlling u_{T\{i},i} does not control u_{(T\{i})+l,i}. An algebraic test on an arbitrary full-rank Q union {l} is to compare both sides of (1) for correlated columns and signed theta_i; equality must hold to numerical precision. A proof implementation must also retain Toolkit-b's full score family and RSS upper bound after weakening beta-min. The estimate is an implication jointly with (W), not an independent TL theorem under BM-width alone.

**Rating: ADOPT NOW (cheap and safe).**

## P2 — A diverging additive width gap, and an explicit NA failure rate

**Statement.** In §3.1, (C1), and (C3)(a), allow the following replacement of (W). Use exactly the sufficient score thresholds already defined in (C3)(a):

    c_n(k) = log(n+1) + 2 log p - 2 log(k+1) - 4 kappa_E - 2,
    m_n = E max_{(T,l) in P} (|u_{T,l}'g| - sqrt(c_n(|T|))).

The radicands are positive eventually in the stated range. Replace the fixed-delta condition by

    m_n <= -t_n, for some deterministic t_n -> infinity.   (W-gap)

Empty P is treated as a vacuous condition. Then, for all sufficiently large n,

    P(exists (T,l): Z_{T,l}^2 > c_n(|T|)) <= exp(-t_n^2/2),
    P(NA(L)^c) <= exp(-t_n^2/2) + P(E_toolkit^c).           (2)

Under the ORIGINAL (W), one can add the explicit conclusion

    P(NA(L)^c) <= n^{-c_*} + O(n^{-1}),
    c_* = delta0^2 / [32(2A+2)],                           (3)

with n0 depending on the same rate envelopes as Toolkit-b. The constant is deliberately conservative, not optimal. For Gaussian rows, the analogous bound includes the failure probability of the conditional design event; it does not imply a polynomial rate for W-R itself.

**Why better.** Fixed positive fractional slack in log n is replaced by an additive gap that merely diverges in standard-deviation units. The old W implies W-gap with t_n of order sqrt(log n). W-gap allows the formal boundary regime -m_n -> infinity but -m_n=o(sqrt(log n)); no claim is made here that this characterizes every possible NA-consistent design. Independently of whether a particular boundary design is constructed, (3) is a strictly stronger conclusion than (C3)(a)'s unquantified convergence. This is an NA rate, not an unsupported polynomial rate for the entire reported-model theorem.

**Proof sketch.** The random function

    M(g)=max_{(T,l) in P} (|u_{T,l}'g|-sqrt(c_n(|T|)))

is 1-Lipschitz, despite the different deterministic shifts. Gaussian concentration gives P(M>0)<=exp(-t_n^2/2) when E M<=-t_n. The score conversion is precisely C-GROW L2.2 with its size-dependent version in target (P3). This proves (2).

To recover (3), uniformly over pairs put a=a_{n,delta0}(|T|). For large n,

    c_n(|T|)-a^2 >= (delta0/2) log n,
    sqrt(c_n(|T|)) + a <= 2 sqrt((2A+2)log n).

Hence sqrt(c_n)-a >= delta0 sqrt(log n)/(4 sqrt(2A+2)). Subtract this uniform gap inside the maximum and use E max(|u'g|-a)<=0. Its square divided by two gives c_* in (3). Toolkit-b gives D2 and D3 failures O(n^{-1}); its remaining Gaussian norm event has exponentially small failure. This rate uses no independence across lattice pairs.

**Risk / refutation test.** Do not replace the expectation of the shifted maximum by the maximum of expectations. Also, a bounded additive gap only gives a fixed concentration bound and is not sufficient by this argument. Algebraically check the displayed minimum gap at k=q and at k=s0, including the constant -4 kappa_E-2. If Toolkit-b is supplied only qualitatively, retain the explicit P(E_toolkit^c) in (2) until its quoted D1 bound is carried through. Near-threshold realizability is not needed for (3), but a claim of a sharp necessary-and-sufficient width threshold would require new work.

**Rating: ADOPT NOW (cheap and safe).**

## P3 — Gaussian-row leakage and localisation need only sub-logarithmic losses

**Statement.** In §3.2 (L-R^b), (C2), and (P7), keep deterministic H_l, the same quantifiers and covariance floors, and the same strict budget 15 rho+b<1/2. Make both of the following replacements:

1. Replace C_L n^{-1/2} in (L-gain-R) by a deterministic envelope a_n satisfying

       a_n sqrt(n/log n) -> 0.

2. Replace r_n(n log n)^{1/4}->0 in (L-loc-R) by

       r_n (n/log n)^{1/4} -> 0.

All other hypotheses, including W-R, remain. Then [SAND(Q)] and consequently all (C2) conclusions continue to hold. These are little-o statements; arbitrary fixed multiples of the displayed critical scales are not claimed.

**Why strictly better.** The original leakage scale satisfies the new condition, while a_n=n^{-1/2}(log n)^{1/4} is newly admitted. Likewise r_n=n^{-1/4} satisfies the new localisation condition but violates the old one. These are independent weakenings of the population assumptions. No family-specific geometric description or knowledge of the selected partition is introduced.

**Proof sketch.** This is a quantitative delta to RM L3_SANDR §§3–7 and L3b_rate, not an appeal to their statements beyond their range.

Let h=sqrt(log n/n), g_n=r_n+h. The same augmented covariance event and Schur formulas give uniformly over all l,U, and the coefficient box used for sample standardisation,

    |z0|=O(a_n+h)=O(h),
    ||a||+||d||=O(g_n),  ||R^{-1}||=O(1).

Here a,d denote the partial-correlation vectors of the existing proof, not the new scalar envelope a_n. The exact partial-correlation recursion yields

    |z_U-z0| <= C g_n^2,
    |n z_U^2-n z0^2| <= C n g_n^2(h+g_n^2) = o(log n).    (4)

Indeed the potentially largest terms divided by log n are

    sqrt(n/log n) r_n^2  and  n r_n^4/log n,

and both vanish under the proposed rate. The old proof required (4) to be o(1); its counting and exclusion margins only need o(log n). Also h_{U,l}=O(log n), so the score expansion h/2+o(1) in L3_SANDR §6 remains valid: its own Taylor error is O((log n)^2/n), unrelated to the larger comparison error in (4).

For the reference spherical tail, the conditional mean shift now has norm O(sqrt(n)a_n)=o(sqrt(log n)), rather than O(1). On the same raw-column norm event and conditioning sigma-field as L3_SANDR §5, the comparison of sqrt(h_{U0,l}) with the spherical statistic incurs this shift plus a relative o(1) denominator error. Thus at thresholds t of order log n its tail is

    exp(-t/2 + o(log n)) + O(exp(-c sqrt(n))),             (5)

uniformly over references. For smaller t a trivial bound can be used; all counting thresholds used below are of order log n. This follows by squaring sqrt(t)-o(sqrt(log n)), not by asserting a sphere law conditional on the full covariance event. Sample-standardisation is handled exactly through the existing coefficient-box and innovation conditioning argument.

Multiplying (5) by at most p n^{15 rho+o(1)} references, and shifting t by the o(log n) error (4), gives

    E[1_{E_cov} J(t_n(k))] <= k n^{-1/2+15 rho+o(1)}.

The dyadic ladder therefore still excludes k>2(q+16s0). For final junk exclusion choose any fixed epsilon with

    0<epsilon<1-2b-30rho

and the threshold

    T_n=2 log p+(30rho+epsilon)log n.

The union failure is n^{-epsilon/2+o(1)}. On its complement the deletion margin for a far null is at least

    [1/2-15rho-epsilon/2-b]log n-o(log n)>0.

Truth inclusion and feasibility are unchanged. This proves the improved sandwich with the same exponent region. W-R, TL, and POST are separate retained inputs, so no automatic weakening of their assumptions is asserted.

**Risk / refutation test.** The key risk is uniformity of (5) when the conditional mean shift grows. Recheck the actual sphere comparison on the raw-column norm event with shift norm sqrt(n)a_n; its loss divided by log n must tend to zero, including the denominator correction. An algebraic stress test is a_n=n^{-1/2}(log n)^{1/4}, r_n=n^{-1/4}: the shift contribution to the exponent is O((log n)^{3/4}) and the localisation loss in (4) is O(sqrt(log n)+1), both sub-logarithmic. A derivation producing an order-log-n loss for these envelopes would refute the proposal. Constants at the critical scales require a new explicit budget and are deliberately excluded.

**Rating: WORTH A TICKET.** The inequalities are concrete, but the uniform noncentral spherical-tail delta deserves its own checked lemma before adoption.

## No credible improvement found for

- **Removing the b/eta coupling or the 15rho reference-count cost.** The fixed-design terminal obstruction is that one outside coordinate suffices to violate containment. Counting its expected number with a worst-case noncentral Gaussian bound reproduces the same leading threshold as the maximum argument. In Form R, the present deterministic reference family still has n^{15rho} elements. P3 improves logarithmic scales, not that polynomial count.
- **b at or above 1/2 for a deterministic sandwich.** The number of outside pure-noise entrants can cease to vanish near this scale. A reported-model result might survive failed containment, but controlling subsequent additions/swaps within the shipped cap is not supplied by the descent lemma. The boundary numerics do not prove such control.
- **Removing BM-Q with no replacement geometric control.** P1 uses truth-removal width; W controls addition directions, and I do not have an implication bounding all swap-removal directions from W alone. Using only deletion directions breaks at (1).
- **A materially weaker descent condition that tolerates whole-lattice improving additions.** The deterministic lemma compares every extra-removing swap to the corresponding deletion at the smaller set. Simply dropping NA at those smaller sets leaves precisely that comparison unsupported. No complete path argument is proposed.
- **A general common-factor primitive that is certified broader than W-ref/W-loc.** A shared low-dimensional component can be charged by a projection norm, but fixed-dimensional components can already be absorbed into the reference subspaces. I do not claim a strict new theorem from that observation without verifying an example outside the existing sufficient forms.
- **An exact converse threshold or asymptotic coded-LS0 failure from violation of W alone.** Mean-width concentration supplies robust one-sided gaps, not a necessary gap at the transition. An improving move somewhere in the lattice need never be visited by the coded search.
- **A polynomial failure rate for the whole reported-model theorem.** P2 supplies an NA rate. An O_P posterior contraction statement or qualitative W-R does not itself supply the required polynomial tail for the common reporting event.
- **An unconditional old-cap result at polynomial q.** L1.2 already gives the deterministic refinement: S0 is scored when the actual number of start extras is at most ell_n+1, and certified when it is at most ell_n. No new partition-free population/design bound proving that small realised start count is established here.

Proposal labels and ratings: P1 — ADOPT NOW; P2 — ADOPT NOW; P3 — WORTH A TICKET.
