# Sharp leading constant for the grouped lattice; explicit CC range

All statements concern the corrected CC target in KL_BRIEF section 6.
Write `a=1-rho_b=b+d`, `H=sqrt(2 log p)`, `q=qbar`, and
`L=log log p` (p sufficiently large). No greedy-path assumption is used
in this file. Truths can occupy any fixed layout.

## 1. Uniform grouped lattice bound

Let `G` be the number of original groups, `Q=2^q-1`, and
`C_q=e Q q`. With probability at least

    1 - 2 exp(-L) sum_{ell=1}^infinity (ell+1)^(-2),          (1)

simultaneously for EVERY nonempty `T subset [p]`, `k=|T|`,

    |e_T|/sqrt(a)
      <= sqrt(2 log(C_q p/k) + 2L + 4 log 2).                (2)

In particular, the leading constant in front of
`sqrt(2 log(p/k))` is **one**, rather than `sqrt((qb+d)/a)`.
The constants `C_q` and `4 log 2` are inessential but explicit.

### Proof

For a deterministic T, the normal equation gives

    D_T = 1/rho_b + sum_g u_g/(d+b u_g),
    e_T = [h/rho_b - sum_g sum_{j in U_g} y_j/(d+b u_g)]/D_T.

The numerator is centered Gaussian of variance D_T: the h term has
variance `1/rho_b`, different groups are independent, and

    Var(sum_{U_g} y_j)/(d+b u_g)^2 = u_g/(d+b u_g).

Thus `Var(e_T)=1/D_T` exactly. If ell groups meet T, then

    a D_T >= a/rho_b + ell,                                 (3)

since `u/(d+bu)>=1/a` for each integer u>=1. The number of T meeting
exactly ell groups is at most

    binom(G,ell) Q^ell <= (e Q G/ell)^ell.                   (4)

For each such T apply the Gaussian tail bound with

    (|e_T|/sqrt(a))^2
      > 2[ell log(e Q G/ell)+L+2 log(ell+1)]/(ell+a/rho_b).

By (3), its probability is at most twice the exponential of minus
the square-bracketed expression. Union over (4) and then ell gives
(1). This is an ordinary finite union over deterministic sets.

On its complement the squared bound is at most

    2 log(e Q G/ell) + 2L/ell + 4 log(ell+1)/ell
      <= 2 log(C_q p/k) + 2L + 4 log 2,

using `ell>=k/q`, `G<=p`, and `(ell+1)<=2^ell`. This proves (2).
The count (4), together with (3), is the improvement over counting
arbitrary k-coordinate subsets while using the worst block variance.

## 2. Conversion to size-dependent CC

Fix `0<theta<1` and an eventual upper bound
`log p/log n <= alpha_hi < 1/2`. It is enough that p tends to infinity;
no positive lower bound on `log p/log n` is needed. Define

    R_theta = 2 alpha_hi (1+sqrt(1-theta))^2
                         / [1+2 alpha_hi(1-theta)].         (5)

If `R_theta<1`, then with probability tending to one, every parent
T with `|T|>=ceil(p^theta)` and all its one-null-deletion neighbours
satisfy CC with

    delta_theta = (1-R_theta)/2.                            (6)

This includes every such state of every greedy or perturbed path.

### Proof, including neighbours and uniform error terms

For parent size k put `beta=log(p/k)/log p`, so
`0<=beta<=1-theta+o(1)`. The size of a deletion neighbour is k-1;
`log(k/(k-1))=o(1)` uniformly in this range. Bound (2) therefore gives
for the parent and all those neighbours

    |e_T'|/sqrt(a) <= sqrt(2 beta log p + O(log log p+1)).    (7)

Here and below all big-O constants are deterministic and independent
of T and of the path. Moreover

    H_q = sqrt(2 log p + O(log log n+1)),
    log n+2 log((2p-k)/(k+1))
       >= log n+2 beta log p -2 log(1+1/k).                 (8)

Since `log p=O(log n)`, expansion of the squared sum in (7)-(8)
has error `o(log n)` uniformly, even when beta or `log p/log n`
tends to zero. Writing `alpha_n=log p/log n`, the CC ratio is at most

    2 alpha_n(1+sqrt(beta))^2/(1+2 alpha_n beta)+o(1).       (9)

For `alpha_n<=alpha_hi<1/2`, this increases in alpha_n and in beta
on `[0,1]`: after putting `t=sqrt(beta)`, the derivative in t has
the sign of `1-2 alpha_n t`, which is positive. Thus (9) is at most
`R_theta+o(1)`, proving (6).

The exact exponent condition is

    alpha_hi < alpha_crit(theta)
             := 1/[2+4 sqrt(1-theta)].                     (10)

For `alpha_hi>1/6`, it is equivalently

    theta > 1 - [(1/(2 alpha_hi)-1)/2]^2.                  (11)

## 3. Concrete full-S5 partial result

Take `alpha_hi=17/100`, `theta=3/50=.06`. Then

    alpha_crit(.06) = .1701217287982847...,
    R_theta = .999457760388467...,
    delta_theta = .0002711198057664... .

Consequently **CC_n(1/10000) holds simultaneously for all parents
with k>=ceil(p^.06) and all their deletion neighbours**, with
probability tending to one, whenever eventually
`log p/log n<=.17`. These are arbitrary full-S5 sets, not a restricted
partition. The statement is valid, in particular, in the requested
regime `1/6<limsup log p/log n<.17`.

For comparison, at alpha_hi=.17 the first-round dense bound required
approximately `k>=p^.844416`; (10) permits every fixed theta above
`.0579584775086508...`.

### Endpoint specialization at this exponent

Assume s0=4 and arbitrary truth layout, so the anchor from the first
round satisfies `lambda_0>=217/57`. Its elementary all-set proof gives,
uniformly over parents with at most M0 nulls and their neighbours,

    |e_T'|/sqrt(a) <= [M0/(lambda_0+M0)]H+o(sqrt(log n)).

For completeness: bound h and the O(1) coordinates in truth-intersecting
groups by `log log p`; bound every other coordinate by
`sqrt(a)*sqrt(H^2+2 log log p)`. In the normal equation, truth-intersecting
groups have total denominator at least `lambda_0/a`, and other groups
have total weight at most `M0/a`. Their weighted means lie inside the
coordinate envelope, giving the display. The finite anchored numerator
is `O(log log p)=o(sqrt(log n))`. All bounds hold on one event with
probability tending to one.

At `M0=250`, the endpoint ratio is bounded by

    (34/134) [1+14250/14467]^2
      = .9997589302313648... < .9998.                       (12)

The CC denominator for these bounded parent sizes is
`log n+2 log p+O(1)`. Thus **CC_n(1/10000) also holds for the final
250-null region**, uniformly over all sets, at alpha_hi=.17.

Combining the two assertions leaves precisely the unproved range

    251 <= number of retained nulls,
    parent size k < ceil(p^.06).

There is no asserted whole-path exponent greater than 1/6.
