# A proved restricted version of the corrected CC target

Status: **PROVED in the regime stated below; no claim for the full S5 partition.**
The corrected target in section 6 of the brief is used throughout.

## Statement

Write `a = 1-rho_b = b+d`, and suppose **every group containing a null is a
singleton**. Groups containing only truths may have arbitrary sizes bounded
by qbar. Start at all p indices and use exact argmin null deletions
(`delta_n=0`). The truth set is fixed, of size s0, and is never deleted.
For the truth-only groups let t_g be their sizes and set

    D0 = 1/rho_b + sum_g t_g/(t_g b+d),
    lambda = a D0,
    c_* = 2/(lambda+2).

The sum includes singleton truth groups. For definiteness assume their sizes
are fixed as n changes; the proof also works with a fixed positive lower
bound on lambda and a fixed upper bound on lambda.

Suppose for constants `0 < alpha_lo <= alpha_hi` that, eventually,

    alpha_lo <= log(p)/log(n) <= alpha_hi,
    R := max{2 alpha_hi,
             [2 alpha_hi/(1+2 alpha_hi)](1+c_*)^2} < 1.

Then the brief's **CC_n(delta)** holds with probability tending to one, with
the explicit choice

    delta = (1-R)/2 > 0.

Here `H_q = sqrt(2 log(2^qbar p)+2 log log n)` exactly as in the brief, and the
bound includes **every one-null-deletion neighbour**, not just visited
sets. Equivalently the permissible exponent bound is

    alpha_hi < min{1/2, 1/[2 c_*(2+c_*)]}.

### S5 constants

For `(rho_b,rho_w,qbar)=(.3,.7,5)` and `s0=4`, even if all four truths are in
one truth-only group,

    lambda >= (7/10)(10/3+40/19) = 217/57,
    c_* <= 114/331 = 0.3444108761...,
    (1+c_*)^2/2 <= 198025/219122 = 0.9037203019... .

Consequently the theorem covers **every fixed alpha_hi < 1/2** in this
restricted partition regime. Use `c_*=114/331` in R for a single constant
valid for every truth layout. If the truths are singleton groups,
`lambda=19/3` and `c_*=6/25=.24`.

This is not a theorem for q=5 null groups. It isolates exactly the part of
the CS template that survives unchanged when the truth anchor is grouped.

## Exact reduction to scalar CS

For null j put `z_j=y_j/sqrt(a)`. These are iid standard normals, independent
of the finite-dimensional truth data and h. Let m be the number of retained
nulls and K their set. The exact normal equation gives

    x_T := -e_T/sqrt(a) = [sum_{j in K} z_j+B]/(m+lambda),
    B := sqrt(a)[sum_g t_g/(t_g b+d) ybar_g - h/rho_b].             (1)

B is a centered Gaussian of bounded variance; it is fixed along the path.
In particular `P(|B| <= log log p) -> 1`. The null block of the precision
matrix has diagonal `1/a - V_T/a^2`, where
`V_T=a/(m+lambda)`. Its product with g has coordinate `(y_j+e_T)/a`.
Therefore

    tau_j(T) = (z_j-x_T)/sqrt(1-1/(m+lambda)).                    (2)

The denominator is positive when m>=1 since lambda includes `a/rho_b`
and the truth information; more generally positivity follows from the
Gaussian precision matrix. In fact m+lambda>1 for m>=1 and lambda>0.
Thus exact argmin deletion is nearest-point deletion in the z-coordinates.
Deleting null j changes the centre by

    x_{T-j} = x_T - (z_j-x_T)/(m-1+lambda).                     (3)

The event and the bulk/end arguments are proved in
`02_CS_event_and_path.md`. They establish, uniformly along the path,
with `H=sqrt(2 log p)` and `m1=ceil((log log p)^2)`,

    m >= m1: max_{T' in {T} union {T-j}} |x_{T'}| = o(H),
    m <  m1: max_{T' in {T} union {T-j}} |x_{T'}| <= c_* H+o(H). (4)

The o(H)'s in this display have deterministic rates on events with
probability tending to one. The second constant is 2/(lambda+2), not
1/(lambda+1): an arbitrary neighbour of a visited state with m=3 and
imbalance 1 can have m'=2 and imbalance 2.

## Conversion from (4) to CC_n(delta)

Since `k=m+s0 <= p`,

    log n + 2 log((2p-k)/(k+1)) >= log n - 2/p.

For m>=m1, (4) and the assumed polynomial growth of p imply uniformly

    (H_q+max |x_T'|)^2 / [log n+2 log((2p-k)/(k+1))]
       <= 2 alpha_hi + o(1).                                 (5)

Here `H_q/H -> 1`, because qbar is fixed and
`log log n=o(log p)`. For m<m1, `k=O((log log p)^2)`, so the denominator is

    log n+2 log p+o(log p).

It follows that the ratio in (5) is now at most

    [2 alpha_hi/(1+2 alpha_hi)](1+c_*)^2 + o(1),               (6)

because `t -> 2t/(1+2t)` is increasing. Both bounds are at most R+o(1).
For sufficiently large n this is at most `(1+R)/2=1-delta` on the event
from `02`. Since `kappa_0|e_T'|=|x_T'|`, this is precisely CC_n(delta).

## Scope limits

* Exact argmin only. No near-argmin robustness claim is made.
* Polynomial p is assumed explicitly. No assertion is needed here about
  subpolynomial sequences.
* All null-containing groups are singletons. The protected-champion lemma
  in `03` applies to the full partition, but does not remove this assumption.
* No git state was changed and no files outside this directory were written.
