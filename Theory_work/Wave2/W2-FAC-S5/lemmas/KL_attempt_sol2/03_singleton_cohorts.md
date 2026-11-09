# Deterministic no-crossing and interval holes for fixed singleton cohorts

Exact argmin deletions only in this file. All comparisons are among
deletable nulls. The result does **not** apply to protected truths.
S5 constants are `a=.7`, `b=.4`, `d=.3`, `rho_b=.3`.

## 1. Parent-field formula and drift

At a retained set T let `V=1/D_T`, and let j have u retained group-mates.
Put `kappa_u=c_u/s_u`. The exact formula, using the **parent** field, is

    tau_j(T) = [A_j(U)+kappa_u e_T]/sqrt(1-kappa_u^2 V),
    e_(T-j)-e_T = kappa_u V tau_j(T)/sqrt(1-kappa_u^2 V).     (1)

To verify it directly, write `B_T=direct_sum(dI+bJ)` and
`Q=Sigma_TT^(-1)=B_T^(-1)-V B_T^(-1)11'B_T^(-1)`.
For this j, `(B_T^-1)_jj=1/s_u^2` and
`(B_T^-1 1)_j=c_u/s_u^2`, so

    (Q g_T)_j = [a_j(U)+c_u e_T]/s_u^2,
    Q_jj = [1-kappa_u^2 V]/s_u^2.

This gives the first identity. Alternatively updating the conditional
mean of h by the residual at j gives
`e_(T-j)-e_T = c_u V_(T-j) tau_j/sqrt(s_u^2+c_u^2 V_(T-j))`;
using `V=V_(T-j)/(1+kappa_u^2 V_(T-j))` yields the second.
These formulas also establish the signs, which matter below.

## 2. A null singleton cannot cross the global centre

Write `X_l=y_l/sqrt(a)`, `x_T=-e_T/sqrt(a)`, and `z=V/a`.
If l is a null singleton retained after the greedy deletion of j,

    tau_l(T) = (X_l-x_T)/sqrt(1-z),
    |tau_l(T)| >= |tau_j(T)|.

Since `kappa_u<=1/sqrt(a)` and
`r -> r/sqrt(1-r^2 V)` increases for positive admissible r, (1) gives

    |x_(T-j)-x_T|
       <= z |tau_j(T)|/sqrt(1-z)
       <= [z/(1-z)] |X_l-x_T|.                             (2)

For S5, `V<=rho_b` implies `z<=3/7`, hence `z/(1-z)<=3/4<1`.
Thus the centre cannot cross l. This argument is deterministic and
does not presume anything about the group where j is deleted.
Zero/tie equalities can be excluded on the usual probability-one
event of finitely many nontrivial Gaussian equalities.

In particular, **the side of a null singleton, once it becomes a
singleton, is fixed until that null is deleted**. A truth singleton
is absent from the argmin comparison, so the same statement for truths
is neither asserted nor generally true.

## 3. Fixed cohort interval theorem

At an arbitrary path time t0 choose any cohort C of retained null
singletons. C can depend on all data and on the preceding path.
Its coordinates stay singleton for their remaining lifetimes.
At later times define

    a_t=max{X_l:l in C intersect T_t, X_l<=x_t},
    b_t=min{X_l:l in C intersect T_t, X_l>x_t},

with infinite endpoints for empty sides. The deleted members of C
are **exactly** the original cohort points in `(a_t,b_t)`.
Once a side of C is empty it remains empty.

Proof: at t0 no cohort point is deleted and the endpoints are consecutive.
A deletion outside C leaves its retained points and endpoints unchanged;
(2) prevents the centre from crossing any such point. A deletion in C
is one of the two closest cohort endpoints, by the global argmin rule;
again (2) prevents crossing any other cohort point. Induct.

This is an interval statement for C, not a statement that C is a
sign-symmetric or iid sample. Conditional Rademacher concentration for
this data-dependent C would require a separate argument.

## 4. Explicit error term for asymmetry

As long as both sides of C exist, put
`Delta_t=|(b_t-x_t)-(x_t-a_t)|`. If a cohort point is deleted, let
`d_t=|X_j-x_t|` and let g_t be its gap to the next cohort point on
that side. Set `A_T=a/V`. A singleton deletion changes `A_T` to
`A_T-1` and satisfies

    x_(T-j) = x_T - (X_j-x_T)/(A_T-1).

Exactly the CS calculation gives

    Delta_(t+1) <= max{Delta_t, g_t+2d_t/(A_T-1)}.           (3)

If a point outside C is deleted, the endpoints do not change and

    Delta_(t+1) <= Delta_t+2|x_(t+1)-x_t|.                 (4)

Combining (3)-(4), through any segment where both sides exist,

    Delta_t <= max{Delta_t0, sup_C_steps(g_s+2d_s/(A_s-1))}
                 +2 sum_nonC_steps |x_(s+1)-x_s|.          (5)

Thus the only new forcing in the CS asymmetry estimate is an explicit
sum of centre drift due to deletions outside the fixed cohort.
Small cardinality of those deletions alone does not bound (5) near the
end: their locations along the path and the factors V_s also matter.
No probabilistic bound on this forcing sufficient to close the middle
range is claimed here.
