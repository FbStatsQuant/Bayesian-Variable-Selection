# Checked obstruction to further all-set improvement

This refutes an all-set extension, **not** the CC assertion along the
greedy path. It also proves that the leading constant one in `01`
cannot be reduced.

Fix `0<theta<1`, `m=ceil(p^theta)`, and `k=m+s0`. In the full block
model, with any fixed truth layout,

    max_{T contains S0, |T|=k} |e_T|/(sqrt(a)*H)
         -> sqrt(1-theta) in probability.                 (1)

Here `a=1-rho_b`, `H=sqrt(2 log p)`, and qbar is fixed. The upper
bound is already the simultaneous grouped lattice bound of `01`.

## Lower bound

Discard the O(1) groups meeting S0. In each remaining group choose
one deterministic designated coordinate. The standardized values
`X_j=y_j/sqrt(a)` so chosen are iid N(0,1). There are
`N>=p/qbar-O(1)` of them.

Fix `0<x<sqrt(1-theta)`. By Mills' bound, the expected number exceeding
xH is at least

    c p^(1-x^2)/H >> p^theta.

A binomial Chernoff bound shows that at least m exceed xH with
probability tending to one. Choose any m qualifying coordinates,
one per original group, and retain them together with S0. Their
groups are singleton **in this set**, although the original partition
can have exactly five coordinates per group.

Let

    lambda_0 = a[1/rho_b+sum_truth_groups t/(d+tb)],
    B0 = sqrt(a)[h/rho_b-sum_truth_groups sum_{S0 in g} y_j/(d+tb)].

Then `B0~N(0,lambda_0)` and is independent of the designated
truth-free observations. Its variance follows by the same calculation
as the normal equation. The exact identity at the chosen set is

    e_T/sqrt(a) = [B0-sum_{chosen} X_j]/(m+lambda_0).

Consequently `|e_T|/(sqrt(a)H)>=x-o_P(1)`. Letting x increase to
`sqrt(1-theta)` proves (1), without invoking any symmetry for a
path-dependent subset.

## Exact CC obstruction

If `log p/log n -> alpha>0`, the maximum CC ratio among parents of
this size converges in probability to

    R(alpha,theta)
      = 2 alpha (1+sqrt(1-theta))^2/[1+2 alpha(1-theta)].     (2)

Indeed (1) controls the maximum field, the denominator is the same
for all parents of this size, `H_q/H->1`, and
`log((2p-k)/(k+1))=(1-theta)log p+O(1)+o(1)`.

When

    alpha > 1/[2+4 sqrt(1-theta)],

with probability tending to one there is a parent at that size
violating even CC_n(0). This is a sharp obstruction for all-set
arguments at every fixed polynomial size.

The same lower-bound proof with `m=ceil(log p)` and fixed x<1 gives
maximum normalized field tending to one; the upper bound is again
`01`. Its CC ratio tends to `8 alpha/(1+2 alpha)`. Thus **no all-set
CC theorem can cover the full size range for any alpha>1/6**.

Example: `alpha=.17`, `theta=.01` gives the limit
`1.012413180631828... >1`. The explicit Gaussian-tail benchmark in
`numerics_summary.json` takes `log p=10000`, threshold `.99H`, and
`m approximately exp(100)`. Its expected qualifying count is roughly
`exp(191.53)`, far above 2m; with `|B0|<=50`, its CC ratio is at least
`1.00807`. Integer rounding and discarding four groups have negligible
effect on these strict inequalities. This benchmark uses an allowed
layout with four truths in distinct groups, `lambda_0=19/3`.

It is not claimed that this extremal set can be reached by greedy
elimination. Proving that it cannot be reached is exactly the sort of
path information still required.
