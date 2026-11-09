# Uniform endpoint results for the full S5 partition

These results apply to arbitrary groups of size <=qbar, including the
q=5 null groups in S5. No path assumption is used, so their uniformity
automatically covers all visited states and their one-deletion neighbours.

Assume `alpha_lo <= log p/log n <= alpha_hi` eventually, for constants
`alpha_lo>0`, `alpha_hi<1/2`. Set `a=1-rho_b`,
`H=sqrt(2 log p)`, and `H_q` as in the corrected brief.

## A. A fixed number of retained nulls

Let t_g=|S0 intersect G_g|, omitting zero t_g, and define

    lambda_0 = a[1/rho_b+sum_g t_g/(t_g b+d)].

For every fixed integer M0, uniformly over **all** sets T containing S0
with at most M0 nulls,

    kappa_0 |e_T| <= [M0/(lambda_0+M0)] H+o(H)               (17)

with probability tending to one. The uniform o(H) is deterministic on the
event in the proof below. If

    c0=M0/(lambda_0+M0),
    R0=[2 alpha_hi/(1+2 alpha_hi)](1+c0)^2 <1,

then every parent state with at most M0 nulls, together with all its
one-null-deletion neighbours, satisfies CC_n(delta0), with

    delta0=(1-R0)/2.

### Proof

There are at most s0 groups intersecting S0, with at most s0 qbar total
coordinates. On an event of probability 1-o(1), |h| and every y_j in these
groups are bounded by `L=log log p`, and all other coordinates obey
`|y_j|<=sqrt(a) Hbar`, where `Hbar=sqrt(H^2+2L)`. The latter assertion is
a direct union bound over Gaussian marginals, regardless of correlations.

For arbitrary T split its global weight into W_A from groups intersecting
S0 and W_N from the other groups. Write

    D_A=1/rho_b+W_A >= lambda_0/a,
    W_N=sum_{g not intersecting S0} u_g/(u_g b+d) <= M0/a.

The first inequality follows since `u/(ub+d)` increases with u; the second
since `ub+d>=b+d=a` for u>=1. The absolute contribution to the normal
equation numerator from h and all anchored groups is O(L), uniformly
over their finitely many possible subsets. All other group means have
absolute value at most sqrt(a) Hbar. Consequently

    |e_T|/sqrt(a)
      <= [W_N/(D_A+W_N)] Hbar+O(L)/(sqrt(a)(D_A+W_N))
      <= [M0/(lambda_0+M0)] Hbar+O(L).

Since `Hbar/H->1` and `L/H->0`, this proves (17). For parent k=s0+m with
m<=M0, the CC denominator is `log n+2 log p+O(1)`. Every deletion neighbour
also has at most M0 nulls and obeys (17). The ratio of the CC left and right
sides before the factor 1-delta is at most R0+o(1), proving the claim.

### S5 consequences

For s0=4, every truth layout gives

    lambda_0 >= (7/10)(10/3+40/19)=217/57.

Indeed each denominator t_g b+d is at most 4b+d, so the truth sum is at
least 4/(4b+d). Taking M0=2 gives

    c0 <= 114/331,
    R0 < (1+114/331)^2/2 = .9037203019... .

Thus **the entire final two-null region of the full S5 model satisfies
CC_n(.04) with probability tending to one**, uniformly over all sets in
that region, for every fixed alpha_hi<1/2. The constant .04 is permissible
because .903721<.96; it is more conservative than delta0 above.

If the four truths lie in distinct groups, `lambda_0=19/3`. Taking M0=4
gives `c0=12/31` and endpoint ratio at alpha=1/2 equal to
`(43/31)^2/2=1849/1922=.9620187...`. In that layout **the final four-null
region satisfies CC_n(.01)** with probability tending to one for all
fixed alpha_hi<1/2. Extra nulls in those four truth groups are allowed.

## B. An explicit dense-size range (lattice baseline)

Let `K=(qbar b+d)/a` and choose beta in (0,1). For any constant
`c>sqrt(K beta)`, with probability tending to one,

    kappa_0 |e_T| <= c H

simultaneously for every T of size at least `ceil(p^(1-beta))`.

For a deterministic T of size k, the Gaussian residual e_T has variance

    V_T=[1/rho_b+sum_g u_g/(u_g b+d)]^(-1)
       <= (qbar b+d)/k.

Therefore `P(kappa_0 |e_T|>cH)<=2 exp[-(c^2/K)k log p]`.
There are at most `(ep/k)^k` such T at size k. Uniformly for
`k>=ceil(p^(1-beta))`, the log of the count is at most
`k(1+beta log p)`. Since c^2/K>beta, summing the resulting exponentially
small bound over at most p sizes proves the assertion. Notice that no
conditional Gaussian assertion is made about a data-dependent T.

Thus, if `2 alpha_hi(1+c)^2<1`, there is a fixed delta>0 for which CC holds
for every parent with `k>=ceil(p^(1-beta))+1` and all its deletion
neighbours. One explicit choice is

    delta=[1-2 alpha_hi(1+c)^2]/2.

For S5, `K=23/7`. A nonempty dense range can always be obtained for any
alpha_hi<1/2 by taking

    beta < (7/23)[1/sqrt(2 alpha_hi)-1]^2

and then choosing c strictly between the two required bounds. This is
the lattice argument already identified in the brief, with constants
spelled out; it does not fill the intermediate-size gap.
