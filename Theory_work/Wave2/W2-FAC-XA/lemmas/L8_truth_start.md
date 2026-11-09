# L8 — Independent truth protection and near-full start

Status: **PROVED (by this seat, unchecked)**. Research-helper contribution only;
no independent reviewer or council was run (the task explicitly prohibits
subagents). This file does not certify XA X2–X4 or delivery. Falsification code
and results: `../numerics/N9_truth_start.py`, `N9_results.json`.

## 0. Interface and sources

Read: XA `STATEMENT.md` (locked v1), `GENERAL_ASSUMPTIONS.md`; Wave1,
Wave1C and Wave2 `PROTOCOL.md`; FAC-B `STATEMENT.md`, `lemmas/L2_start.md`
and `lemmas/L5_assembly.md`; FAC-A `lemmas/L1_uniform_add.md`,
`lemmas/L3_NA_TL.md` and `lemmas/L5_random_instances.md`.
The arguments below prove their inputs directly: no XA lemma is an input.
FAC-A L3.0/L3.2 supplies a useful comparison, but its Gaussian envelope,
factor assumptions and dimension exponent are not imported.

Production sources (repository-relative):
`Scripts/SMC_BVS/core/cpp/v3_score.h:39` (`data_init`),
`:147` (`q_nonneg`), `:176` (`try_chol`), `:204` (`finish_from_factors`);
`Scripts/SMC_BVS/core/cpp/v3_start.h:69` (`log_gamma0`),
`:76` (`build_tables`); and `Scripts/SMC_BVS/core/v3_preprocess.R:37`
(`v3_standardise`), `:97` (`v3_preprocess`).
These implement precisely the following real-arithmetic target. Floating-point
implementation premises remain those in the locked statement.

Let C=I-11'/n, X=CX with ||x_j||²=n-1, R=X'X/(n-1),
Y=X theta+C epsilon, epsilon~N(0,sigma² I) independently of X, and
y=Y/s, s²=||Y||²/(n-1). Here sigma>0, s0>=1 is fixed,
supp(theta)=S0, min_{i in S0}|theta_i|>=b>0, ||theta||_1<=B<infinity.
All constants are common over designs and truth positions. For A subset [p],

    G_A=X_A'X_A, z_A=X_A'y, H_A=(n+1)G_A+I,
    Q_A=n-1-n z_A'H_A^{-1}z_A, nu=n/2+0.01,
    D_A=1/2[log det H_A-log det(G_A+I)],
    F(A)=log w(|A|)-D_A-nu log(0.02+Q_A)+constant,
    w(k)=1/[2 choose(2p-1,k)], K=min(p,floor(n/2)).

Empty inverses/quadratic forms/determinants have their usual empty conventions.
The composite start objective is

    J(S)=log w(|S|)+sum_blocks [log m(S intersect C_b)-log m(empty)].

In every result below p=o(n), hence K=p eventually.

## 1. Exact ridge bounds valid on the entire lattice

Suppose **GLOBAL** R>=g I for a fixed g>0. Set h=1/(n+1),
RSS_A=||(I-P_A)y||², with P_A the orthogonal projection onto span X_A.
For every A simultaneously,

    D_A=|A|/2 log(n+1)+r_A,
    -|A|/[2(n-1)g] <= r_A <=0,                         (1)
    Q_A=RSS_A+omega_A,
    0<=omega_A <= (n-1)/(n+1) [1+1/((n-1)g)] <=2       (2)

for all sufficiently large n. Proof: every nonzero eigenvalue t of G_A
is at least (n-1)g. The corresponding determinant summand is
log(n+1)+log[(t+h)/(t+1)], whose second term belongs to [-1/t,0].
Also n H_A^{-1}=(1-h)(G_A+hI)^{-1}; hence

    omega_A=z_A'{G_A^{-1}-(G_A+hI)^{-1}
                        +h(G_A+hI)^{-1}}z_A
            <=h[1+1/((n-1)g)] z_A'G_A^{-1}z_A,

and the final quadratic form is <=y'y=n-1. Both matrices in braces
are positive semidefinite. For A empty, omega_A=r_A=0.
These are bounds on the exact production ridge score, not an OLS replacement.

## 2. Truth deletion and truth-out swap: uniform negative order n

**Theorem T.** For every deterministic centered standardized design with
R>=g I, p=o(n), and the signal/noise assumptions in section 0, there is a
constant c>0 such that, uniformly in these designs,

    P( max_{T superset S0, i in S0, A=T\{i} or
                    A=(T\{i}) union {l}, l notin T}
             [F(A)-F(T)] <= -c n | X ) ->1.           (3)

An empty maximum imposes no condition. Thus (3) covers the full
truth-containing lattice, not just a proposed adaptive path. No factor model
or block visibility is needed here.

Proof. Write e=C epsilon, P=P_[p], Z=||Pe||². Since all design columns
are centered and full rank, conditionally on X,

    Z/sigma² ~ chi²_p, ||(C-P)e||²/sigma² ~ chi²_{n-1-p}.

In particular Z=O_P(p), uniformly over X: Markov gives
P(Z>M p | X)<=sigma²/M. This remains the correct assertion for bounded p;
Z<=constant*p need not hold with probability tending to one.
Also Z/n ->0 uniformly when p=o(n). For example,
P(Z>sqrt(np)|X)<=sigma² sqrt(p/n).
On events of uniform probability tending to one,

    Z=o(n), ||e||²<=2 sigma² n, ||(C-P)e||²>=sigma² n/2,
    sigma²/2 <= s² <= S²:=2(B+sqrt(2)*sigma)².          (4)

For the chi-square assertions, diagonalize the orthogonal projections in
the centered space; the squared coordinates are independent squared standard
normals. Their sums have mean their rank and variance twice their rank.
Chebyshev therefore gives the two energy bounds in (4), uniformly over X,
since p=o(n). Indeed ||X theta||<=sqrt(n-1) B, giving the upper bound; projection
onto the orthogonal complement of the full design gives the lower bound.

Fix a T,i,A in (3). Since A retains all other truths,
v=(I-P_A)X theta=theta_i(I-P_A)x_i. The variational form of a Schur
complement, or minimization of ||x_i-X_A a||², yields

    ||v||² >= b²(n-1)g,   ||v||<=B sqrt(n-1).

This uses the floor on A union {i}, potentially of size p. As v belongs
to span X, |v'e|<=||v|| sqrt Z. Expanding both residual sums gives exactly

    s²(RSS_A-RSS_T)=||v||²+2v'e+e'(P_T-P_A)e
      >= b²(n-1)g-2B sqrt(n-1) sqrt Z-2Z.             (5)

The quadratic bound follows by bounding each of e'P_T e,e'P_A e by Z;
the conservative constant 2 is harmless. In particular all cross terms in
(5) are uniformly O_P(sqrt(np)); the noise terms are O_P(p). There is no
union over 2^p models. Equations (4)–(5) imply, on a common event,

    RSS_A-RSS_T >= d n,    d=b²g/(4 S²)>0.             (6)

By (2), Q_A-Q_T>=d n-2 and 0.02+Q_T<=n+1.02. Consequently for large n

    log[(0.02+Q_A)/(0.02+Q_T)]>=log(1+d/3)>0.

For deletion log[w(k-1)/w(k)]=log[(2p-k)/k]<=log(2p);
for swaps this term is zero. Equation (1) bounds any favorable determinant
change by (1/2)log(n+1)+p/[(n-1)g]. These terms are o(n), whereas the
likelihood penalty is at least (n/2)log(1+d/3). Taking, for example,
c=(1/4)log(1+d/3) proves (3). All events and constants used above are
independent of T,i,l and of the particular design. QED.

Random-design corollary: if P(R>=g I)->1, (3) holds jointly by conditioning
and integrating the displayed uniform probability bounds. This is stronger
than a merely pointwise conditional-convergence assertion.

## 3. A deterministic-design start lemma with an explicit visibility margin

For |U|<=15 and j notin U define

    v_R(U,j)=1-R_jU R_UU^{-1} R_Uj,
    c_R(U,j)=R_j,S0 theta-R_jU R_UU^{-1} R_U,S0 theta.

Then v_R in [g,1] by the same minimization argument. With
u_Uj=(I-P_U)x_j/sqrt((n-1)v_R),

    u_Uj'X theta=sqrt(n-1)c_R(U,j)/sqrt(v_R).          (7)

Assume **V_R**: |c_R(U,j)|>=c0>0 for every such pair with either
j in S0 or U not superset S0. For j null and U superset S0,
c_R(U,j)=0 exactly for every design (the signal is already in span X_U).

**Theorem S.** Under R>=g I, V_R, p=o(n), log p=O(log n), and section 0's
assumptions, for every X-measurable error-independent partition into blocks
of size <=16, let

    N0=union {C_b\S0 : S0 subset C_b}, S*=[p]\N0.

Then S* is the unique maximizer of J with conditional probability tending
to one, uniformly over all qualifying designs and partition rules.
There is at most one truth-containing block, so |N0|<=16-s0<=15.
If no block contains every truth then N0 is empty. In particular a full
start is not asserted for every partition.

Proof with explicit uniform events. Conditional on X the partition is fixed.
Among its block pairs U subset C_b, j in C_b\U, there are at most 16*2^15*p
pairs. Each u_Uj'e/sigma is N(0,1), irrespective of signal and without any
independence among pairs. Let L=log log(n+e^e). Gaussian tails and a union
bound give, with conditional failure <=exp(-L),

    max_actual_pairs |u_Uj'e|/sigma
       <=sqrt(2 log(2*16*2^15*p)+2L).                 (8)

There are at most M0=16*2^15 zero pairs (U superset S0,j null), all in the
single block containing all truths, if it exists. With another failure
<=exp(-L),

    max_actual_zero_pairs |u_Uj'e|/sigma
       <=sqrt(2 log(2 M0)+2L).                        (9)

These bounds hold with the same probabilities for every X and partition;
they do not select a truth block using the noise. Intersect with (4).
The tail bound used here is P(|G|>t)<=2 exp(-t²/2), obtained by applying
Markov to exp(+-tG), whose expectation is exp(t²/2).
For any block increment from U to U+j, the exact OLS identity is

    RSS_U-RSS_{U+j}=(u_Uj'Y)²/s².                     (10)

If the pair is visible, (7)–(8) give (10)>=c0²(n-1)/(4 S²)>=h0 n
for a constant h0>0 and large n, uniformly. By (2),
Q_U-Q_{U+j}>=h0 n-2. Since 0.02+Q_{U+j}<=n+1.02,
the log ratio (0.02+Q_U)/(0.02+Q_{U+j}) is bounded below by a fixed
positive constant. Thus

    log m(U+j)-log m(U) >= h1 n-O(log n),             (11)

for h1>0. For any global model size k<p, the exact prior increment is
log[(k+1)/(2p-1-k)]>=-log(2p); therefore adding a missing visible
coordinate strictly increases J by order n. This includes U empty.

For a zero pair, U contains S0, so u_Uj'Y=u_Uj'e exactly and (9)–(10)
give RSS_U-RSS_{U+j}<=C(1+L). Both sets contain S0, and (4) gives
RSS_{U+j}>=||(C-P)e||²/s²>=sigma² n/(2 S²).
Using (2) and log(1+x)<=x,

    nu log[(0.02+Q_U)/(0.02+Q_{U+j})]<=C'(1+L).

If the ratio is below one, the upper bound remains valid. From (1), since
the block models have size <=16,

    log m(U+j)-log m(U)
       <=-1/2 log(n+1)+C'(1+L)+O(1/n)
       <=-1/4 log n.                                (12)

For a global S containing j and all truths, with (S intersect C_b)\{j}
containing S0, removal also earns the prior ratio
w(k-1)/w(k)=(2p-k)/k>=1. Hence this removal strictly increases J.

Finally consider S!=S*. If S misses j in S*, the actual block pair for j
cannot be zero: zero requires j in the all-truth block but outside S0,
which means j in N0. Thus (11) gives a strict improvement by addition.
Otherwise S contains S* and some j in N0, and therefore all truths; (12)
gives a strict improvement by removing j. Every S!=S* has a strictly
better feasible neighbor. Finiteness gives a unique maximizer S*.
The conditional failure bound is at most 2 exp(-L)+o(1), with the last
term supplied uniformly by (4). QED.

Quantifier: this proves sup over qualifying designs and X-measurable
partition rules of the conditional failure probabilities tends to zero.
It does NOT claim one noise event on which all conceivable partitions
simultaneously succeed. It also does not allow response-selected partitions.

## 4. Population visibility and iid CS transfer, proved directly

For a correlation covariance Sigma=D+lambda lambda',
D_jj=d_j=1-lambda_j², 0<lambda_lo<=lambda_j<=lambda_hi<1,
define t_U=sum_{i in U}lambda_i²/d_i and
L_V=sum_{i in S0\U}lambda_i theta_i. Sherman–Morrison gives

    Sigma_UU^{-1}=D_U^{-1}
       -D_U^{-1}lambda_U lambda_U'D_U^{-1}/(1+t_U),
    c_Sigma(U,j)=d_j theta_j+lambda_j L_V/(1+t_U),
    v_Sigma(U,j)=d_j+lambda_j²/(1+t_U),               (13)

where theta_j=0 for a null. For completeness, first remove the contribution
of truths in U, whose conditional covariance is zero. For i,j outside U,
the residual covariance is d_j 1_{i=j}+lambda_j lambda_i/(1+t_U);
summing against theta_i proves (13). Thus d_min<=v_Sigma<=1.
An absolute covariance visibility lower bound c0 implies a normalized
one |c_Sigma|/sqrt(v_Sigma)>=c0; conversely a normalized lower bound q0
implies |c_Sigma|>=q0 sqrt(d_min). This proves the promised equivalence
up to common constants, not equality of the margins.

Bounded positive loadings alone DO NOT rule out masking. In the generalized
version assume explicitly the locked population V:
|c_Sigma(U,j)|>=c0 for |U|<=15 and either j truth or U not containing S0.
No additional no-masking theorem without V is claimed.

In CS lambda_j=sqrt(rho), d_j=1-rho. Equation (13) becomes

    c_Sigma(U,j)=(1-rho)[theta_j+
                  rho sum_{i in S0\U}theta_i/(1-rho+|U|rho)]. (14)

For a null with U not containing S0, FS-a makes the nonempty missing-truth
sum nonzero. For a truth j notin U, FS-b makes the bracket nonzero, including
U empty. Only finitely many choices (missing-truth subset, |U| in 0..15,
and truth identity) occur for the fixed coefficient vector and fixed rho.
Their nonzero absolute minimum is a constant c_FS>0. This supplies V,
including a uniform no-masking/visibility margin, from FS rather than
assuming it. Infeasible configurations may simply be omitted; including
them under the stated stronger FS is harmless.

**Elementary centered, standardized design event.** Let raw rows be iid
N(m,Sigma), with Sigma as above (CS included). Put N=n-1 and
T=(X^r)' C X^r/N. Orthogonally rotate the n rows so that C is diag(I_N,0).
The first N rotated rows are independent N(0,Sigma), by joint Gaussianity
and orthogonality. Thus E T=Sigma and
Var(T_jk)=(Sigma_jj Sigma_kk+Sigma_jk²)/N<=2/N.
Take t_n=n^{-1/4}. Chebyshev and a union bound imply

    P(max_jk |T_jk-Sigma_jk|>t_n)<=2 p²/(N t_n²).

On its complement, for t_n<1/2, all sample variances lie in [1-t_n,1+t_n]
and R_jk=T_jk/sqrt(T_jj T_kk), so

    max_jk |R_jk-Sigma_jk|<=4t_n,
    ||R-Sigma||_op<=||R-Sigma||_F<=4p t_n.           (15)

For every p<=n^a, fixed a<1/4, the failure probability tends to zero and
4p t_n->0. This deliberately conservative elementary event suffices for
the locked rate, including bounded/oscillating sequences. It never assumes
the forbidden absolute O_P(sqrt(p/n)) rate. Since Sigma>=d_min I,
(15) gives GLOBAL R>=d_min/2 eventually.

Visibility transfer uses only fixed-size matrices. For |U|<=15,
||R_UU-Sigma_UU||<=60 t_n, and both inverse norms are <=2/d_min
eventually. The inverse identity gives
||R_UU^{-1}-Sigma_UU^{-1}||<=120 t_n/d_min².
Every row R_jU, Sigma_jU has norm <=sqrt(15); each vector
R_U,S0 theta or Sigma_U,S0 theta has norm <=sqrt(15) B.
Their differences have norms <=4sqrt(15)B t_n, and the initial
j,S0 signal covariance differs by <=4B t_n. Expand the three factors
in R_jU R_UU^{-1}R_U,S0 theta, replacing one factor at a time.
These bounds yield

    sup_{|U|<=15,j notin U}|c_R(U,j)-c_Sigma(U,j)|
          <=C(d_min,B) t_n ->0,                     (16)

uniformly over all such U,j, without a further probability union or a
dependence on p. The empty U case follows from the initial term alone.
Consequently V_R holds with c0/2 (or c_FS/2 in CS) on a common design
event A_n of probability tending to one. Zero pairs remain exactly zero,
not merely approximately zero, because the response signal uses the
standardized X with fixed theta.

Apply Theorems T and S conditionally on X in A_n. All constants and
conditional failure bounds are common; integrate to get joint success
probability tending to one. This proves the requested iid-CS+FS start
result for every X-measurable partition rule of block size <=16 and
p<=n^a, a<1/4. It also proves the corresponding bounded one-factor iid
result under explicit population V. Exact standardized one-factor Grams
satisfying V are covered directly by Theorem S (and T); no random transfer
is needed in that case. No assertion of a larger iid exponent is made here.

## 5. Exact scope, remaining gaps, and falsification meaning

Proved here, unchecked: uniform order-n truth protection on the entire
truth-containing lattice under a GLOBAL floor and p=o(n); unique start S*
for iid CS+FS at the locked exponent, and one-factor+V as stated above.
The start lemma also has the explicit deterministic-design scope of section 3.
No unchecked XA geometry, ordering, or path-transfer lemma was used.

Not proved: absence of improving null additions, ordering of safe deletions
against null-null swaps, a pure-deletion adaptive path, a bound on its length,
or a terminal certificate at S0. Truth protection alone does not prove these:
LS0 could still swap nulls or add nulls while preserving S0. Neither LS0
discovery nor D_n nor reported-model/delivery consistency is assembled here.
Lemma S/Proposition F implementation inputs and allocation are lead work.
The independent review gates also remain lead work.

N9 checks use exact D0 ridge formulas and sample-standardized responses,
enumerate p=6, and use 8 distinct seed values locally. They include an X-selected
truth block with N0 nonempty, a spread-truth layout, a near-small-floor
stress, and a deliberate FS-violating masked singleton. The latter falsifies
the claim with FS removed, not the locked target. Finite-sample misses under
FS, if any, are recorded without treating them as asymptotic counterexamples.
The completed run found 8/32 data sets with a favorable truth move and
32/96 start mismatches across the three tested layouts. These are observations
at the diagnostic sample sizes, not counterexamples to a probability limit.
The omitted-FS masked singleton excluded truth 0 in 8/8 checks. The independent
subtraction and nonnegative ridge-Q formulas agreed within 1.91e-11.
Detailed parameters, every mismatch, score margins, and floors are retained
in `N9_results.json`; `N9_summary.md` records interpretation.
