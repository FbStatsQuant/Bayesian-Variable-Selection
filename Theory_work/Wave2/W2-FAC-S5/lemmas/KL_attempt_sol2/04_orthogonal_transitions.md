# Uniform Gaussian exception bounds and a conditional scalarization gate

These are full-S5 statements. Their high-probability events are unions
over a deterministic O(p) family of within-group coordinate/subset
configurations. They therefore hold simultaneously for every path.
The field and deletion-level assumptions below are explicit conditions,
not conclusions about the actual greedy path.

Use `a=.7`, `H=sqrt(2 log p)`, `d_1=sqrt(3/11)`, `K=23/7`,
and `X_l=y_l/sqrt(a)`. For u>=1 put

    d_u = sqrt(a)*kappa_u
        = sqrt[a d/((d+ub)(d+(u+1)b))] <= d_1.              (1)

For parent size k, `V_T/a<=K/k` by the variance bound in the first round.
The parent-field identity in `03` is used throughout.

## 0. All-history raw extreme exceptions (no deletion-level assumption)

The first-round maximum principle also gives a direct bound for ALL
extreme nulls deleted in multimember groups, including early deletions.
This is different from the high-current-level transition bound below.

Put `r=b/a=4/7`. Fix x>0 and `0<=E<(1+r)x/2`. Define

    J_raw = min{2x^2/(1+r),
                x^2+[(1+r)x-2E]^2/(1-r^2)} > x^2.         (R1)

On an event of probability at least `1-16 p^(-epsilon)-o(1)`, the following
holds for EVERY exact-argmin path, up to any time through which its
normalized field has stayed at most E H:

    #{null j deleted while a group-mate was retained,
      |X_j|>=xH} <= p^(1-J_raw+epsilon).                   (R2)

Here epsilon>0 is arbitrary and fixed; for the O(1) groups containing
truths one also intersects the event that their original coordinates
are o(H). That event has probability tending to one and excludes such
extreme exceptions there. If `J_raw>1`, a direct union bound instead
gives no such exceptions with probability `1-O(p^(1-J_raw))-o(1)`.

### Deterministic implication and Gaussian count

For a positive X_j>=xH deleted in a truth-free multimember group, the
maximum principle says that some retained group-mate l has
`|X_l+t|>|X_j+t|`, with `t=e_T/sqrt(a)` and `|t|<=E H`.
Because E<x, `X_j+t>0`. Therefore either

    X_l >= X_j >= xH,

or

    X_l <= -X_j-2t <= (2E-x)H.                            (R3)

For negative X_j reflect both coordinates. These are necessary original
pair events, independent of the selected subset and field history.

For standard normal pair correlation r, the first positive-pair event
has probability at most `p^[-2x^2/(1+r)]`, by the tail of X_j+X_l.
For the second let B=2E-x<r x. The Gaussian Chernoff multipliers at
`(x,B)` have positive first and negative second signs, and give rate

    x^2+(B-rx)^2/(1-r^2).

This is the second rate in (R1). There are at most 4p original ordered
within-group pairs, two reflected signs and two event types. Thus the
expected total count of qualifying signed pair events is at most
`16 p^(1-J_raw)`. Markov's inequality proves (R2); every exceptional
coordinate can be charged to a distinct pair event since its first
coordinate j is distinct. No per-history union is needed.

### Explicit exponentially small relative frequency

If `E<=x/2`, the second rate in (R1) is at least
`x^2/(1-r^2)=(49/33)x^2`, and hence

    J_raw=(14/11)x^2,
    J_raw-x^2=(3/11)x^2.                                 (R4)

For `0<x<1`, choose one designated coordinate per truth-free original
group. A binomial tail bound gives at least `p^(1-x^2-epsilon)`
coordinates of EACH sign beyond xH with probability tending to one.
Combining with (R2), the fraction of original raw xH-extremes that
can be deleted as non-singletons is at most

    p^[-(3/11)x^2+2epsilon].                              (R5)

For example choose `epsilon=(3/44)x^2`. The fraction is at most
`p^[-(3/22)x^2]=exp[-(3/44)(xH)^2]`, with probability tending to one.
This proves the proposed form of exponentially rare raw exceptions,
uniformly over all bounded-field histories. There is no requirement
that the deletion itself occurred at a high level.

At x=.8, E=.05, the absolute exception rate is at most
`p^(.185454546+epsilon)`, whereas the original extreme pool has order
`p^.36` up to polynomially negligible factors. At x=.9, E=.05,
`J_raw=1.03090909...>1`, so no .9H-coordinate can be deleted in a
multimember group under that history bound, with high probability.

Limit: this controls exceptions at a FIXED raw threshold. Connecting
the moving singleton-hole endpoints and their current deletion-level
deficit to that threshold still requires a path argument. In particular
(R5) cannot establish its own bounded-field premise.

## 1. Independent large-coordinate / conditional-residual pairs

For any deterministic within-group triple `(j,U,l)` with
`empty != U subset G(j) minus j` and `l in U`, the standard normals

    A_j(U), X_l

are independent. Indeed
`Cov(y_j-b sum_U y/(d+ub),y_l)=b-b(d+ub)/(d+ub)=0`.
There are at most

    p sum_{u=1}^4 u binom(4,u) = 32p                         (2)

such triples. For fixed x,y>0, let N_xy count those satisfying
`|X_l|>=xH` and `|A_j(U)|>=yH`. Gaussian tails and independence give

    E N_xy <= 128 p^(1-x^2-y^2).                            (3)

In particular, if `J=x^2+y^2>1`, then `N_xy=0` with probability
at least `1-128 p^(1-J)`. More generally, for any epsilon>0,

    P(N_xy > p^(1-J+epsilon)) <= 128 p^(-epsilon).           (4)

If the threshold on the left is below one, (4) means the count is zero
on that event. These bounds contain no conditioning on a selected set.

### Path consequence

Fix theta>0, E>=0, t>0, and a margin nu>0 such that
`y=t-d_1 E-nu>0`. For sufficiently large p, every deletion at a parent
with

    k>=p^theta,  |e_T|/sqrt(a)<=E H,  |tau_j(T)|>=tH         (5)

that leaves a group-mate l with `|X_l|>=xH` uses a triple counted
in N_xy. This is because (03.1) implies

    |A_j(U)| >= [t sqrt(1-K/k)-d_u E]H >= yH.               (6)

Thus (3)-(4) uniformly bound these transitions, including births of
extreme singleton survivors. Each deletion uses a distinct j, and
cannot use one deterministic triple twice.

For example, take `x=t=.8`, `E=.05`, `nu=.001`. Then

    J=.64+(.8-.05 sqrt(3/11)-.001)^2
      =1.237356404049...>1.

With probability tending to one, there are **no** transitions meeting
(5) that leave a group-mate of magnitude at least `.8H`.

This is not a bound for all nulls previously deleted in a multimember
group: early, low-level deletions need not meet (5). That distinction
is essential for any use of this result as an exception estimate.

## 2. Number of retained multimember groups at a high current level

For a deterministic retained group subset W of size v>=2, put
`u=v-1`. Its two conditional standardized residuals have correlation

    Corr(A_j(W-j),A_l(W-l)) = -b/(d+ub) =:-r_u,
    0<r_u<=4/7.                                          (7)

One verification is to use the block precision:
`a_j=(B_W^-1 y_W)_j/(B_W^-1)_jj`, and divide its covariance with a_l
by the common residual variance. The ratio is
`(B_W^-1)_jl/(B_W^-1)_jj=-b/(d+ub)`.

For any fixed pair, if both absolute A's exceed yH, split into their
four sign choices and apply the Gaussian tail to their signed sum.
Its variance is at most `2(1+r_u)`. Therefore

    P(|A_j|>=yH, |A_l|>=yH)
       <=4 p^[-2y^2/(1+r_u)] <=4 p^[-(14/11)y^2].          (8)

The number of deterministic `(W,{j,l})` configurations is at most
`80p`: within one group of size at most five it is at most
`binom(5,2)2^3=80`, and there are at most p groups. Let N_y count
the configurations in (8). With `J2=(14/11)y^2`,

    E N_y <=320 p^(1-J2),
    P(N_y>p^(1-J2+epsilon))<=320 p^(-epsilon).               (9)

At any set with `k>=p^theta`, normalized field at most E H, and
all retained **null** statistics at least tH, choose
`y=t-d_1 E-nu>0` as in (6). Every truth-free multimember retained group
contributes at least one counted configuration. Its number of retained
coordinates is therefore at most `5 N_y`, simultaneously for all such
sets. If `J2>1`, no such group is present, with probability tending to one.

Example: `t=.8,E=.05,nu=.001` gives `J2=.760271786971...`.
Taking epsilon=.001 bounds their coordinate count by
`5 p^.240728214`, with probability tending to one. It gives a vanishing
fraction whenever the total retained count is at least `p^.26`.
It gives no domination conclusion for a much smaller retained count.

## 3. Conditional exact scalarization from protected champions

Let `A=1999/2000`, `gamma=.000499875`, and use the first-round protected
shell of at least `floor(p^gamma)` groups of EACH sign. Set E=.05.
On an event of probability tending to one, the following implication
holds for every exact-argmin path starting at [p]:

> If `|e_T|/sqrt(a)<=.05H` through its first deletion of a protected
> shell champion, then at that deletion decision EVERY null-containing
> retained group is a singleton.

The first such deletion occurs while at least
`2 floor(p^gamma)` shell champions are retained. Its size is therefore
at least `p^gamma` for large p.

Proof: protection in the first round applies since `.05<.75`, so the
champion must be deleted as a singleton. Its absolute statistic is
at least

    (A-E)H=.9495H.

Thus the current minimum null statistic is at least tH for t=.9495.
In (9), with nu=.001,

    J2=(14/11)(.9495-.05 sqrt(3/11)-.001)^2
      =1.082836708774...>1.

No truth-free multimember group remains. For groups intersecting S0,
all O(1) original coordinates are bounded by `log log p` on another
event of probability tending to one. Any null still in such a group
has u>=1 and hence, by (03.1),

    |tau_j|/H <= d_1 E+o(1) < .9495,

uniformly over the finitely many possible group subsets; the denominator
is `1+o(1)` since k>=p^gamma. This contradicts the minimum level.
Hence such a group has no retained null. The claimed scalarization follows.

This yields a useful exact dichotomy: either the field exceeds `.05H`
before this gate, or the remaining null path becomes scalar CS. It does
**not** rule out the first alternative, even though the field starts small.
Removing that alternative is the still-missing startup argument.
