# Conditional terminal theorem after the protected-champion gate

This is a **conditional deterministic implication on an event of
probability tending to one**, not a proof that the gate is reached with
a small field. It does not use conditional symmetry of the random
retained set. Assume s0=4, arbitrary truth layout, and exact argmin.

## Statement

Use the gate of `04`: the first deletion decision for a protected
shell champion. Suppose the preceding history, including that parent,
satisfies `|e_T|/sqrt(a)<=.05H`. Then, on one event of probability
tending to one, all parents **from the gate onward**, including all
their one-null-deletion neighbours, satisfy CC_n(delta) whenever

    alpha_n=log p/log n <= alpha_hi < alpha_gate,
    alpha_gate = 1/[2 c(2+c)] = .412606129553...,
    w = 201/4000 = .05025,
    lambda_min = 217/57,
    c = w+2(1+w)/(lambda_min+1) = .487215328467... .         (1)

One valid choice is `delta=(1-R_gate)/2`, where

    R_gate = max{2 alpha_hi (1+w)^2,
                 [2 alpha_hi/(1+2 alpha_hi)](1+c)^2}.       (2)

Both terms are below one in the range (1); the bulk-only cutoff is
`1/[2(1+w)^2]=.453298856933...`, so (1) is the smaller cutoff.
For instance alpha_hi=.4 allows delta=.005.

The field restriction is required only **through the gate**. The
subsequent endpoint field is allowed to exceed `.05H`.

## Exact scalar reduction at the gate

Intersect the events in `04` with

    max_j |X_j| <= Hbar=sqrt(H^2+2 log log p),
    |B| <= log log p,

where the fixed truth-anchor offset B is the signed version of B0
in `02`; it has bounded Gaussian variance. Both added events have
probability tending to one. The gate contains at least
`2 floor(p^gamma)` nulls; using `k>=p^gamma` only weakens this fact.

By `04`, all null-containing groups at the gate are singleton, and
no null remains in a truth-intersecting group. From then on write

    x=-e_T/sqrt(a)=(sum_{retained nulls} X_j+B)/(m+lambda),
    lambda=lambda_0>=lambda_min.

All null deletion denominators coincide, so the process is exact
nearest-point deletion in this fixed, possibly data-dependent sample.
Its initial centre has `|x|<=.05H`.

At the gate every singleton statistic has magnitude at least
`tH`, t=.9495. Consequently each retained null satisfies

    |X_j| >= a_p H,
    a_p=t sqrt(1-K p^(-gamma))-.05 -> .8995.                 (3)

Here `K=23/7`; p is sufficiently large that the square root is real.
Together with the maximum event, its magnitude is in `[a_p H,Hbar]`.
Set

    w_p=(Hbar/H-a_p)/2 -> .05025=w;

in fact `w_p>=w>.05`. Initially all positive coordinates are above x
and all negative coordinates below x. The singleton no-crossing
lemma in `03` preserves these sides for their entire lifetimes.

## A deterministic band trapping bound

At every later visited state with m>=1,

    |x_m| <= F_m := w_p H+(Hbar+w_p H)/(m+lambda).           (4)

No concentration or balance of signs in the retained sample is needed.

Proof by induction. The initial bound follows from `.05<w_p`.
If `|x|<=w_p H`, deleting any point changes x by at most
`(Hbar+w_p H)/(m-1+lambda)`, which yields F_(m-1).
If `x>w_p H`, a positive point exists: otherwise
`sum X+B<=-m a_p H+|B|<0`, a contradiction. Its distance to x is
at most Hbar-x; every negative point has distance at least a_p H+x.
The definition of w_p makes the former strictly smaller. Thus a
positive is deleted. Sides do not cross, so its value exceeds x and
the new centre is smaller than x. Its upper bound is therefore
`F_m<=F_(m-1)`. For the lower bound,

    x_new=((m+lambda)x-X_j)/(m-1+lambda)
       >= w_p H-(Hbar-w_p H)/(m-1+lambda) >= -F_(m-1).

The negative case is the reflected deterministic argument (also
reflect B). This proves (4), including possible overshoots of zero.
The final state m=0 separately has `x=B/lambda=o(H)`.

For an arbitrary one-null-deletion neighbour of a parent with m>=2,

    |x_(T-j)| <= [(m+lambda)F_m+Hbar]/(m-1+lambda)
       = w_p H+2(Hbar+w_p H)/(m-1+lambda).                  (5)

For m=1 its only neighbour is the final anchor and has x=o(H).
Equations (4)-(5) imply, uniformly over all subsequent parents and
their neighbours,

    m>=ceil((log log p)^2): |x_T'| <= (w+o(1))H,
    m< ceil((log log p)^2): |x_T'| <= (c+o(1))H.             (6)

All o(1) quantities have deterministic bounds on the stated event;
they do not depend on which path-dependent scalar sample was selected.

## CC conversion and limitation

For the first line of (6), the CC denominator is at least log n-o(1).
For the second it is `log n+2 log p+o(log n)`. The additive terms in
`H_q^2-2 log p` are `O(log log n)=o(log n)`. Thus the CC ratios are
bounded by the two terms of (2), plus o(1), exactly as in `01`.
This also handles sequences with liminf alpha_n=0.

The unresolved inference remains proving that the field stays below
`.05H` until the first shell champion deletion, or constructing a
different unconditional start. Neither the lattice event nor (4)
applies before scalarization in a way that establishes this history
condition. The conditional exponent .412606 is not a whole-path result.
