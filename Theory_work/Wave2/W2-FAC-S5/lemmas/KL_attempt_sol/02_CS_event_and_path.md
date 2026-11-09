# Probability event and complete scalar path argument

This proves (4) of `01`. It follows the interval, signed-top comparison,
and majority-deletion structure of the requested FAC-B L3/L4 template,
with a general fixed positive anchor lambda.

Throughout, there are `M=p-s0` iid `z_j~N(0,1)`, and

    x_K = (sum_K z_j+B)/(m+lambda),  m=|K|,

where lambda>0 is fixed and B is Gaussian of bounded variance. Nulls are
deleted by exact minimization of `|z_j-x_K|`. No probabilistic independence
between B and the z's is needed for the union bound below.

Put `L=log log p`, `H=sqrt(2 log p)`, `Hbar=sqrt(H^2+2L)`,
`m1=ceil(L^2)`, `d_e=20L/H`, and `epsilon_p=L^(-1/4)`. All assertions below
are for sufficiently large p, so L>1 and m1<M/3. Ties at any subset are
excluded on a probability-one event: the relevant equalities are nontrivial
linear equations in Gaussian variables; there are finitely many subsets
for each p. Alternatively none of the inequalities below requires a
particular rule for ties of distinct closest points.

## A. An explicit event of probability 1-o(1)

For `Top(J)` the J largest absolute observations, write
`D_J=sum_{Top(J)}z_j` and `P_J=#{j in Top(J):z_j>0}`. Define
`u_J=2 log(J+1)+L`, also for real J>=1. The event is:

1. `|B|<=L` and `max_j |z_j|<=Hbar`.
2. Each sign has at least M/3 observations.
3. For every integer `1<=J<=M`,

       |D_J| <= Hbar sqrt(2J u_J),
       |P_J-J/2| <= sqrt(J u_J/2).

4. Each sign has at least m1 observations of magnitude at least `H-d_e`.
5. Every consecutive gap in the positive observations, every consecutive
   gap in the negative magnitudes, and the gap from the smallest negative
   observation to the smallest positive observation, is at most `2L`.

**Proof of the probability claim.** B has bounded variance, so its bound
fails with probability o(1). The maximum bound fails with probability at
most `2M exp(-Hbar^2/2) <= 2 exp(-L)=o(1)`. Sign counts follow from Hoeffding.
Conditional on all magnitudes, signs are independent Rademachers. Hoeffding
gives failure probability at most `4 exp(-u_J)` for the two J-th assertions,
on the maximum event. The union costs at most
`4 exp(-L) sum_{J>=1}(J+1)^(-2)=o(1)`.

For the tail claim set `t=H-d_e`. For large p, t>=1,
`t^2/2 <= log p-19L`, and the Gaussian lower tail bound
`P(Z>=t)>=phi(t)/(2t)` shows that the expected number of either sign beyond
t is at least `C exp(19L)/H`. This grows faster than m1 and than any fixed
power of L, so a binomial Chernoff bound proves assertion 4. More explicitly
`exp(19L)/H = (log p)^(37/2)/sqrt(2)`.

For assertion 5, use grid cells of width L/4 that lie in [0,t]. Every
interval of length L/2 within [0,t] contains such a full cell. Each cell
has probability at least `(L/4) phi(t)` under either signed sample. Since
`M L phi(t)/4 >= C L exp(19L)`, the probability that any of the
`O(H/L+1)` cells lacks either sign is o(1). Assertion 4 provides observations
in [t,Hbar] for each sign, an interval of length
`d_e+(Hbar-H)=O(L/H)=o(L)`. The cells also provide observations near zero.
These facts bound the one-signed gaps and the cross-zero gap by 2L.
All constants in this paragraph are deterministic for large p. This proves
the event claim.

## B. Exact interval structure

For a state K define a as the largest kept z<=x and b as the smallest kept
z>x, allowing infinite endpoints. Put `L_K=x-a`, `R_K=b-x`,
`d_K=min(L_K,R_K)` and, when both endpoints are finite,
`Delta_K=|R_K-L_K|`.

The deleted observations form exactly the open interval (a,b) of the
original sample. A side that becomes empty remains empty. If a<0<b, K is
the union of the largest positive observations and largest negative
magnitudes, with its respective sign counts.

Indeed, the first state has an empty gap. If b is deleted, (3) gives
`x_new=x-R_K/(m-1+lambda)`. When m>=2, the denominator is >1 and
`R_K<=L_K`, so the new centre stays strictly between a and x. Thus a stays
fixed and b moves to its next kept neighbour. The argument is symmetric
when a is deleted. The last deletion leaves no points and needs no gap
assertion.

When both sides exist before and after a step, let g be the spacing from
the deleted endpoint to its next kept observation on that side. Then

    Delta_new <= max{Delta_old, g+2d_old/(m-1+lambda)}.          (7)

For example after deleting b, the signed difference R-L changes from a
number in [-Delta_old,0] by `g+2R/(m-1+lambda)`. Its absolute value is at
most the right side of (7). In particular g<=2L on the event in A.

## C. Bulk: m>=m1

We prove by induction, in the order (i), (ii), (iii),

    (i) both sides exist;
    (ii) Delta<=epsilon_p H/2;
    (iii) |x|<=epsilon_p H.                                  (8)

At the initial state `|x| <= [L+Hbar sqrt(2M u_M)]/(M+lambda)=o(H)`.
The two signed tail observations give (i), and the consecutive-gap bound
gives `Delta<=2L=o(epsilon_p H)`.

### Static centre bound, once (i)-(ii) hold

If a<0<b and `x>Delta/2`, then `b>|a|`. K is contained in
`Top(J)={j:|z_j|>=|a|}` for some J, and the omitted observations from Top(J)
are all positive. Thus

    sum_K z_j <= D_J,
    J <= 2m+sqrt(2J u_J).                                    (9)

The second inequality follows because all negative observations of Top(J)
are kept, and the signed count bound applies. The function u_J/J is
decreasing for J sufficiently large. For m>=m1, if J>=5m then eventually
`u_J/J<=1/8`; (9) would imply `J<=2m+J/2<=.9J`, a contradiction.
Consequently J<=5m and

    x <= L/m + Hbar sqrt(10 u_(5m)/m)
      <= L/m1 + Hbar sqrt(10 u_(5m1)/m1) = O(H/sqrt(L)).        (10)

The last bound is o(epsilon_p H). The case `x<-Delta/2` is the sign
reversal, including reversal of B. Otherwise `|x|<=Delta/2` suffices.
If instead a>=0, every negative original observation is kept, m>=M/3,
and all deleted observations are positive. Since x>=a>=0,

    x <= [L+|D_M|]/(M/3) = o(epsilon_p H).

If b<=0 use the reflected inequality. This proves (iii).

### Induction step

First prove (i). If the lower side were to disappear while the new m is
still >=m1, its last point is the minimum original observation a, with
`a<=-H+d_e`. At the preceding state, nearest deletion requires
`x-a<=b-x`, hence, using its bound (iii),

    b >= H-d_e-2 epsilon_p H >= (1-3 epsilon_p)H.

The other `m_old-1` retained points are all at least b. Since
`a>=-Hbar`, identity (1) then implies

    x_old >= [(m_old-1)(1-3 epsilon_p)H-Hbar-L]/(m_old+lambda)
          >= (1-4 epsilon_p)H,

for large p, contradicting (iii) at the preceding state. Here
`1/m1=o(epsilon_p)` and lambda is fixed. The upper-side case is symmetric.

Now prove (ii) by (7), the induction hypothesis, and

    2L+2(Hbar+epsilon_p H)/(m_old-1+lambda)
       = o(epsilon_p H).

Finally prove (iii) using the static argument above. This completes the
induction. For every arbitrary deletion neighbour in this bulk,

    |x_(K-j)| <= |x_K|+(Hbar+|x_K|)/(m-1+lambda) = o(H),       (11)

uniformly in j and the state. Notice that this neighbour need not be the
greedy choice.

## D. End phase: m<m1

At first entry, `m_e=m1-1`; (3) and the last bulk bound give `|x_e|=o(H)`.
Since m<m1<M/3, any nonempty sign side consists of the largest observations
of its sign: a gap wholly on one side of zero would retain all observations
of the other sign and contradict the sign count bound. The same statement
holds after a side becomes empty. Thus every retained z has its signed
magnitude in `[H-d_e,Hbar]`.

Write `I=N_+-N_-`. Uniformly over all end states,

    sum_K z_j+B = I Hbar+E_K,
    |E_K| <= L+m1[d_e+(Hbar-H)] = O(L),
    x_K = (I Hbar+E_K)/(m+lambda).                            (12)

Indeed the second summand in the error is `O(L^3/H)=o(1)`.

If I>=1, (12) gives
`x >= (Hbar-O(L))/(m+lambda)`. In particular x>0 and

    x >> d_e+(Hbar-H),

uniformly for m<m1, since `H^2/(m1 L)->infinity`.
All positive kept points are above x and all negative kept points are
below x. To see this even in one-sided states, use

    Hbar-|x| >= [lambda Hbar-O(L)]/(m+lambda)
               >> d_e+(Hbar-H),

where lambda>0 is fixed and |I|<=m. The closest positive therefore has
distance at most Hbar-x, while every negative has distance at least
`Hbar-[d_e+(Hbar-H)]+x`, which is strictly larger. So a positive null is
deleted. For I<=-1 the symmetric statement holds; when I=0 the next
imbalance has absolute value 1. Consequently

    |I_new|=|I|-1 when |I|>=1,
    |I_new|=1 when I=0.                                     (13)

The entry bound and (12) imply `|I_e|/m_e=o(1)`. Before |I| first reaches
1 or 0, at most |I_e| deletions occur; hence every state with |I|>=2 has
`m>=(1-o(1))m_e`, and at these states (12) and (3) bound both the visited
centre and all its deletion neighbours by o(H).

Once |I|<=1 it stays so. At such a state the visited coefficient of Hbar is
at most `1/(m+lambda)<=1/(1+lambda)` (or zero if m=0). An arbitrary
one-deletion neighbour has new imbalance I'=I-sign(z_j). If m=1, I'=0.
If m=2, parity forces I=0, so |I'|=1 and the coefficient is
`1/(1+lambda)`. If m>=3, the coefficient is at most

    2/(m-1+lambda) <= 2/(2+lambda).

Errors after an arbitrary deletion are still at most O(L), by the signed
tail interval, and the denominator is at least lambda>0. Since
`1/(1+lambda)<=2/(2+lambda)` and `L=o(H)`, the uniform end bound is

    max_{T' in {T} union {T-j}} |x_T'| <= 2H/(lambda+2)+o(H).  (14)

This proves both bounds (4) used by `01`. Every random inequality has been
placed on the single explicit event in A; no union over path histories
or conditional symmetry of path-dependent thresholds is used.
