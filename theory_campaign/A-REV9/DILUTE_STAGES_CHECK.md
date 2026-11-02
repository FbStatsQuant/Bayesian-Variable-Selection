# Independent analytic check: DILUTE, STAGES, WSTAB

Review only; no campaign status is changed. No numerical experiment, simulation, benchmark, or computational validation was run. Sources were read with `git show` at the following immutable branch heads:

- O-DILUTE: `abedf99c92a7b818e9fcdb81bded624335f2b741`, `theory_campaign/O-DILUTE/THEORY.md`.
- O-STAGES: `8d3c142502efea3eb6cc5fca257fd008b62c1329`, `theory_campaign/O-STAGES/REPORT.md`.
- O-WSTAB: `2ec30992adb12335e3cef3b0d9a88ca71c282d63`, `theory_campaign/O-WSTAB/REPORT.md` and `PROOF.md`.
- Common score and locked T22 statement read from the O-DILUTE head: `Docs/Theory/theorems/00_COMMON.md` and `Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md`. Methodology hash recorded there: `93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c`. The external methodology file itself was not inspected.

## DILUTE: exact claims and required corrections

**Theorem E:** the factorisation and size correction follow exactly by multiplying and dividing by `t^k prod e_b(t)`. This works for arbitrary positive tables; truncation must remain in the expectation. Restrict `A_t(k)` to feasible sizes (or include its zero indicator when defining it outside the cap). The supporting-line argument in E2 is valid at interior `1 <= s0 < p`; the displayed interval needs endpoint conventions when `s0=0` or `s0=p`.

**E1:** correct for BF tables, which have `r_b(empty)=1`. Its advertised arbitrary-positive-table scope needs that normalization, or an explicit preliminary replacement `r_b(U)/r_b(empty)`. Without it, `e_b-1-exp(lambda_b)` need not be nonnegative and the empty-block formula is false. E itself has no such problem. E2's sign is correct in its own section:

`log A_t(s0) <= -log P_t(N<=K)` and therefore `-log A_t(s0) >= log P_t(N<=K)`.

**Paper Proposition DM(i) has the opposite sign:** it states `-log A >= -log P_t(N<=K)`. That does not follow and is false in general. For example, take `p=2`, `K=1`, `s0=1`, singleton BF tables with BF values 1, and `t=t0=1`; then `P_t(N<=1)=3/4`, `g_t(0)=log 3`, and `A=4/5`. Thus `-log A=log(5/4) < log(4/3)`. The ceiling on `pi0(S0)` in DM remains valid because its displayed denominator uses the correct E2 bound. The approximate-zero interpretation must not turn a possibly negative size penalty into a nonnegative theorem.

**Theorem R:** coefficient extraction is exact. Both event identities hold with all sets intersected with Omega (the locked statement assigns zero mass outside Omega). Markov gives `P(M>d)<=E M/(d+1)` for integer `d>=0`; specify this domain. It does not imply a small Hamming distance, as the source correctly notes.

**Lemma N:** its core conditional Beta proof is correct under the explicitly written premise `x_l^raw independent of (y^raw,X_-l^raw)`, with nonconstant response. Conditioning after standardization is harmless under that premise. But the parenthetical claim that the premise is true for every Gaussian null having zero correlation with all truths is false: such a null can correlate with other null columns in `X_-l`. Zero correlation with the response implies independence of the response in the joint Gaussian model, sufficient for the *unconditional given y* marginal Beta law, not for independence from all other design columns or the displayed conditional law. Example: two correlated null columns, both independent of the truths and response; given the other null column the first is Gaussian with nonzero conditional mean and nonspherical centered direction. Their response correlations are also dependent. Further, an X-dependent selected block does not automatically preserve a marginal conditional calibration statement after conditioning on selection.

**N1 is not proved by Lemma N and its expectation bound fails for general blocks.** For a block law with coefficients `r0=1,r1,r2,r12`, the expected count is `(t r1+t r2+2t^2 r12)/(1+t r1+t r2+t^2 r12)`, not bounded generally by `t(r1+r2)`. Joint BF synergy is allowed by the actual scoring rule. Analytic BF example: two orthogonal standardized columns with singleton fit fraction `x` each, `0<x<1/2`; then `BF12/BF1^2 = [(1-x)^2/(1-2x)]^nu`, which grows exponentially in n. Taking t so that `t BF1` is small while `t^2 BF12` is large violates the bound. Such data configurations have positive-probability neighborhoods under a full-support Gaussian null model. A valid replacement must control *conditional addition ratios* over all submodels, as in locked T22's `u`, or restrict to singleton blocks. Even singleton blocks give the inequality only as an upper bound, not the asserted Theta lower bound. The index-one heavy-tail approximation also needs a joint growth regime for n and p and dependence control; fixed-n Beta-transformed BF has bounded support, and “iid-like” is not a mathematical hypothesis.

**Proposition S: proof GAP (root independently identified noninjectivity).** The singleton ranking and equal-size prior cancellation are correct, but different replacement assignments can produce the same final support. For two truths with identical candidate sets of three null blocks, the proof counts `(1+3)(1+2)=12` paths, whereas these replacements yield only `1+2*3+choose(3,2)=10` supports. For example, assigning truths 1,2 to nulls a,b or b,a has the same leaf. Thus the claimed product denominator is not established by this counting argument. This disproves injectivity, not necessarily the final inequality for the complete capped BB start: contributions of other sizes could conceivably supply a different proof. A safe counting replacement is to retain one fixed assignment per resulting missing-truth/null-block support, or prove a matching enumeration bound that accounts for multiplicities. Numerical study interpretations were not independently checked.

## STAGES: Theorem M and nearby scope

The exact-frontier monotonicity and greedy argument are sound for finite positive tables and a fixed candidate set. They do not prove that finite-precision 60-step bisection or the empirical pilot returns that frontier. The source generally acknowledges this distinction.

For **Theorem M**, the log-odds change of coordinates is valid and removes the crossing slope: the domain is simply `[-A0,A1]`. The proposed upper construction works: while approaching sigma0=-log 9, use steps with extrapolated endpoint sigma0; bounded-curvature steps then cross the central window; once `s>=log 9`, the reference-S0 deficit is at most c, allowing any terminal jump. This establishes `T*=log2 A0+O(1)` uniformly for `A1>=2.2`.

The lower proof's useful inequality for an endpoint `v in (-3,0]` is justified by convexity: `ell(v+h)-2ell(v) >= ell'(v)h-ell(v) >= exp(v)(h/2-1)`. An interval from `u<=-3` to `v>0` indeed has a cost bounded away from c; its exact expression is minimized at v=0 for fixed u. The early valid steps must have extrapolated endpoint at most `sigma3=log(exp(c+2exp(-3))-1)` and hence cannot shrink the distance to sigma3 faster than a half per step. Combining the last early step with a central entry and a final crossing gives a logarithmic lower bound.

**Displayed decimal constants need conservative rounding or exact expressions.** The proof yields the additive lower constant `2-log2(sigma3+3+2+2 c exp(3))`, approximately -0.955, rather than the stronger -0.95. Likewise replace `A0-1.48` with exact `A0+sigma3`. Using `log2(A0+sigma3)-0.96` avoids this bookkeeping issue. This is a gap in the stated proof of the decimal bound, not an exhibited counterexample to the theorem itself. The upper endpoint `A0-2.2` similarly needs exact sigma0 handling or an explicit margin argument. Retain the asymptotic claim pending an exact-constant cleanup.

PAIR on `[0,2]` is genuinely needed for transfer to full families; concentration at the two endpoints does not supply it. Ideal-grid counts do not imply the method's final count without control of the finite pilot and restricted candidate grid.

## WSTAB: analytic checks of W(a)-(f), W prime

Under the expressly restricted H-ORTH (`p log p=o(n)`, fixed nonzero truths, bounded blocks), the main proof chain is coherent:

- SEP's F2 follows by moving each deletion increment to the right in an increasing derivative and tiling `[a,s]`. The prior denominators used in the bound stay at least p because `e<=p-s0`; dropping feasibility only enlarges a nonnegative sum. The Gamma integral SEP-prime is the exact factorial identity before domination.
- The common random coefficient in S2 and the event `max Z_j^2<=2 log m` make the heavy-tail bound simultaneous in w. The error times `log p` vanishes under `p log p=o(n)`. This proves the proposed upper control without taking an infinite expectation.
- W(a),(b) follow from SEP. W(c)'s extreme-null lower bound is uniform over `[1,2]`, with its order-one random factors absorbed in U_n.
- W(d)'s subtraction of the posterior endpoint defect is legitimate because the extreme-null lower bound dominates `sqrt(log p/n)` by a power of p. The additional `sqrt(log p)` condition on the upper half is essential and is present in this version.
- W(e)'s choice `k=floor(exp((L_n-C1-1)/r))` diverges, is feasible, and is at most order `sqrt(n)`. Thus its uniform Taylor error multiplied by `log p` vanishes. The binomial order-statistic probability tends to one because k diverges. This supports the multi-extra obstruction to the earlier logarithmic prediction, conditional on the explicit H-ORTH scope; no study numerics were checked.
- W(f)'s TV and KL deductions are valid. Set `theta=1/log p` in the tilted KL bound and apply W(b) at `1+theta`; this yields the displayed KL rate even when q2 is unstable.
- W-prime obtains brackets near `G_n` only when they lie in `[0,1]`, where W(b),(c) apply; otherwise the lower bound `g_minus>=1` supplies one step. Since `G_n>=1/(2r)>1/2`, the stated ideal count at most two follows. Exact transition assertions require strict `2Ar<1` or `>1`; no equality conclusion follows. The statement's random delta can be chosen nonnegative to contain both one-sided error terms.

I found no fatal algebraic defect in these restricted W(a)-(f)/W-prime arguments. This is an analytic review, not a reproduction of their saved outputs and not a certification of general BO, `p` comparable to n, the actual hybrid particle system, or the empirical/restricted grid. Those extensions remain explicit hypotheses or open obligations. The theorem lists W(g) out of alphabetical order; I inspected its integral construction, but did not independently audit every numerical prefactor.


