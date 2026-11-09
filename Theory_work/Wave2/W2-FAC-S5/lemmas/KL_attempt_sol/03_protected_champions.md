# Protected champions in the full block model

Status: **PROVED for exact argmin deletion.** These statements apply to
q=5 null groups and do not assume the restricted partition from `01`.
They are structural lemmas, not a proof of full CC.

## 1. Exact within-group maximum principle

Let T be any retained set, and consider a group with v>=2 retained members,
all null. Set `z_j=y_j+e_T` for these members. If one member is the unique
maximum of |z_j|, it **cannot be a minimizer of |tau_j(T)| within its group**,
and hence cannot be the next exact greedy deletion globally.

### Proof

Write `B_T=direct_sum_g(d I+b J)` and
`V_T=(1/rho_b+sum_g u_g/(d+b u_g))^(-1)`. Sherman--Morrison gives

    Sigma_TT^(-1)g_T = B_T^(-1)(y_T+e_T 1),
    (Sigma_TT^(-1))_jj
       = (1-b/(d+vb))/d - V_T/(d+vb)^2,

for each retained member of this group. The diagonal is common and positive
within the group. Since `tau_j=(Sigma_TT^(-1)g_T)_j /
sqrt((Sigma_TT^(-1))_jj)`, the ranking is exactly the ranking of

    |z_j-x_g|,    x_g=b sum_group z_j/(d+vb).                 (15)

Reflect all z's if needed, so the unique maximum of |z| is `z_*=M>0`.
Suppose it minimizes (15). The coefficient `vb/(d+vb)` is strictly below
one, and all z_j<=M, so x_g<M. Every other z_j<M must then satisfy

    z_j <= 2x_g-M,

because otherwise its distance to x_g would be less than M-x_g. Since
also z_j>-M by uniqueness of the absolute maximum, x_g>0. Summing residuals
now gives two incompatible inequalities:

    sum_group(z_j-x_g) <= (2-v)(M-x_g) <= 0,
    sum_group(z_j-x_g) = (d/b)x_g > 0.

This contradiction proves the assertion. The strict gap can be arbitrarily
small, so this proof does not establish protection for near-argmin rules.

## 2. A path-uniform protected extreme shell (S5 constants)

Put `a=1-rho_b=.7`, `r=b/a=4/7`, `H=sqrt(2 log p)`, and
`X_j=y_j/sqrt(a)`. For S5 take the explicit constants

    A=1999/2000=.9995,
    B=51/100=.51,
    C=3/4=.75,
    gamma=(1-A^2)/2 = .000499875.

With probability tending to one there are at least `floor(p^gamma)`
truth-free groups with a positive group maximum `X_j>=A H`, and at least
that many with a negative group minimum `X_j<=-A H`. For each such group
maximum/minimum the following pathwise statement holds simultaneously:

> As long as `kappa_0 |e_T| <= C H` at every visited state through the
> current deletion decision, this
> extreme coordinate cannot be deleted while another member of its group
> is retained. It can only be deleted as its group's last member.

The assertion remains true for every exact-argmin path and every history
of fields within the indicated bound. It is not necessary to condition on
the actual path.

### Proof of the high-probability event

Every pair X_j,X_l in one group has standard normal marginals and
correlation r. The Chernoff exponent for
`X_j>=A H, X_l<=B H` is

    J=A^2+(B-r A)^2/(1-r^2)
     =132600769/132000000=1.004551280303... >1.               (16)

Indeed the optimizing linear Chernoff coefficients are
`(A-rB)/(1-r^2)>0` and `(B-rA)/(1-r^2)<0`; scaling by H and applying the
Gaussian mgf yields probability at most `exp(-J H^2/2)=p^(-J)`.
There are at most `(qbar-1)p` ordered within-group pairs. A union bound
shows that, simultaneously for all j with X_j>=A H, all their group
companions satisfy X_l>B H. Reflecting signs gives the negative assertion.

The O(1) groups intersecting S0 have O(1) coordinates, so with probability
1-o(1) none has a coordinate in either extreme shell. Among the remaining
groups choose one deterministic coordinate each. There are at least
`p/qbar-O(1)` such independent standard normals. Mills' lower bound gives
expected positive shell count at least

    c p^(1-A^2)/H >> p^gamma.

The same is true for the negative shell. A binomial Chernoff bound proves
the required two lower counts. Replacing each successful designated
coordinate with its group's maximum (or minimum) only increases its
extremeness. No requirement that each shell coordinate be its own group's
maximum is imposed.

### Proof of protection on this event

Consider one positive group maximum X_*=M>=A H. All original companions
exceed B H. Suppose the field satisfies `|e_T|/sqrt(a)<=C H` and put
`t=e_T/sqrt(a)`. While the maximum remains retained, it is the largest
shifted coordinate and

    X_*+t >= (A-C)H > 0,
    (X_*+t)+(X_l+t) >= (A+B-2C)H = .0095 H > 0.

Thus its positive shifted value is strictly larger than the absolute
value of every negative shifted companion. Its value is also strictly
larger than that of every positive shifted companion, by uniqueness of
the Gaussian group maximum. Therefore it is the unique maximum of
`|y_j+e_T|` among the retained group members. Part 1 protects it whenever
at least two group members remain. This holds at every state, so induction
proves protection for an arbitrary history of fields bounded by C H.
The negative case follows by reflection.

## 3. What this does not prove

The bound `kappa_0 |e_T|<=.75 H` used above is a stopping condition, not a
conclusion. The shell lemma can be used up to its first violation, but
does not show such a violation is unlikely. In particular it does not
control when protected champions are deleted as singletons, nor the gap
between current deletion level and its running maximum.

It is false that the original maximum of |y_j| in every group is protected.
The numerical counterexample in `numerics_summary.json` has a retained
truth-free pair

    y=(.3269801004001033,-.3905010986040817),
    e_T=.0640948975639751.

The original negative absolute maximum becomes the *smaller* shifted
absolute value `(.3910749979640784,-.32640620104010665)` and can be deleted.
The counterexample refutes only that candidate invariant, not CC.
