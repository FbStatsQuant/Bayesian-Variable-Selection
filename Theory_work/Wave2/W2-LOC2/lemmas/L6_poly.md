# L6 — Polynomial covariance decay: a bounded-conditioning improvement

Status: **PROVED (by this seat, unchecked)**, conditional on the inherited method,
score, descent and posterior inputs listed below. Check record: R06a (Claude Opus 5.5 high, cross-family to the Codex
author, `reviews/R06a_L6_check_opus.md`): VERIFIED-WITH-AMENDMENTS (findings 1-3 applied; 4-6 optional NITs, 4 not
applied — local symbol overloads are flagged here instead: B bandwidth vs matrix, D radius constant / weight / difference,
H constant vs 2x2 matrix, lambda exponent vs coefficient vector); R06b (fresh Codex gpt-6.1-sol xhigh,
`reviews/R06b_L6_check_sol.md`): VERIFIED-WITH-AMENDMENTS (1 MINOR, applied). Dispositions: `reviews/R06_disposition.md`.
**Cutoff: alpha_0 = 17/2 = 8.5; the theorem holds for alpha > 17/2.**
**Binding step:** selection-removal reference counting followed by exclusion of
junk from a start mode of size O(n^(1/(2 alpha))). Its strict inequality is
15/(4 alpha) + 1/(2 alpha) < 1/2. This is the infimum cutoff for the specific
radius/counting argument proved here, not a necessity result for the method.

The improvement over the preliminary alpha-minus-two calculation is essential:
the sandwich only conditions on at most 15 variables. Conditional covariance
then retains exponent alpha, by a finite-dimensional argument (Section 1).
Large-set regression, needed for NA, uses a separate, weaker inverse bound.

All paths below are repository-relative. Abbreviations: LOC2 =
`Theory_work/Wave2/W2-LOC2`; APP = `Theory_work/Wave2/W2-APP`; GROW =
`Theory_work/Wave1C/C-GROW`; GEN = `Theory_work/Wave1/W1-GEN`.
In each abbreviated path:line citation, expand that prefix as just defined.
Proof seat: research parallel prover, 2026-11-09. Only this file and `numerics/poly_*`
are this seat's outputs. Local falsification: `LOC2/numerics/poly_check.py`,
`LOC2/numerics/poly_out.txt`; numerical agreement is not used as proof.

## 0. Precise result and inputs

Use the complete setting and implementation premises of
`LOC2/STATEMENT.md:15` (Section 1), with PTV as in
`APP/lemmas/L3_LOC.md:28`. Rows are iid N(0,Sigma), independent of eps;
Sigma has unit diagonal, spectrum in [c,C], and

    |Sigma_ij| <= K_dec (1+d(i,j))^(-alpha),  d(i,j)=|pi(i)-pi(j)|.

Here c,C,K_dec,alpha,A,s0,theta_lo,theta_hi,sigma are fixed, p<=n^A,
pi is a deterministic bijection, theta is fixed on its deterministic support
S0 of fixed size s0, and alpha>17/2. The partition may be any X-measurable
partition into blocks of size at most 16. The support positions can move with n.
The proof is stated for s0>=1, as in the cited GROW setting.

There is a fixed constant D such that with

    d_n = ceil(D n^(1/(2 alpha))),
    Q0 = S0 union {l: dist(l,S0)<=d_n},
    Q = Q0 if p>=2|Q0|+32s0+1, and Q=[p] otherwise,
    q=|Q|,  b=1/(2 alpha),  L={T:S0 subset T subset Q},

we have q=O(n^b), q<=K_n eventually, and the feasibility dichotomy
Q=[p] or K_n>=2q+32s0+1. In the enlarged case p=O(n^b)=o(n), so
K_n=p eventually. D is any fixed positive constant (e.g. D=1); (P5) then holds with a
constant depending on D [R06a-2].

The conclusions are

    P(Sand_n)->1, P(NA(L))->1, P(TL(L))->1,
    D_n->0,
    1-posterior(S0)=O_P(sqrt(log n/n)),
    P(O intersect {S_hat^+ != S0})->0,
    P(O intersect {S_hat^+ = S0})=1-P(U_n)-o(1).

The last four statements are precisely the PLR conclusions with polynomial Q;
the shipped LS0 cap ell_n+|S_tilde_0| suffices. No unconditional delivery claim
is added here; it requires the separate allocation hypotheses of claim (E).

Inherited inputs, not re-proved or status-upgraded: score toolkit GEN L1
(`GEN/lemmas/L1_lemmaE.md:3`: "PROVED (by this seat, unchecked)", R02
VERIFIED-WITH-AMENDMENTS); GROW L0, L2 and start-mode argument with the statuses
recorded in `GROW/lemmas/L6_random_AR1.md:51`; descent, operational closure,
posterior POST, T03-sharp and M5(0) with the verbatim statuses recorded in
`LOC2/lemmas/L5_assembly.md:7`. Assembly below uses exactly those inputs.
The new polynomial-size steps are proved here rather than invoking the
polylogarithmic hypotheses of LOC2 L1/L2/L5 outside their stated ranges.

## 1. Bounded conditioning preserves exponent alpha

**Lemma BC. PROVED (by this seat, unchecked).** For every fixed integer M there
is K_M, uniform in p, positions, indices, and U with |U|<=M, such that

    |Cov(W_j,W_k | W_U)| <= K_M (1+d(j,k))^(-alpha), j,k notin U, j!=k.

All conditional covariance matrices have spectrum in [c,C], and conditional
variances lie in [c,1], without any size restriction on U.

Proof. First take any principal m by m matrix B of Sigma, m<=M+2. Put
K0=max(1,K_dec). Entries are bounded by K0(1+d)^(-alpha), and det B>=c^m.
For i!=j each determinant monomial of the cofactor defining (B^-1)_ij
has a directed path from i to j of length h between 1 and m-1. Indeed a
bijection from rows excluding j to columns excluding i has outdegree one
except at j, indegree one except at i: the component starting at i ends at j;
it cannot join a cycle because that would give a vertex two predecessors.
All other components are cycles. A path edge has distance at least d(i,j)/h
by the triangle inequality. Bound that factor by
K0 (m-1)^alpha (1+d(i,j))^(-alpha) and all remaining factors by K0.
There are (m-1)! monomials. Thus

    |(B^-1)_ij| <= (m-1)! K0^(m-1) (m-1)^alpha c^(-m)
                   (1+d(i,j))^(-alpha).                         (P1)

This covers m>=2; there is no off-diagonal case for m=1. For
B=Sigma_{U union {j,k}}, the 2 by 2 conditional covariance S is the inverse
of the corresponding principal 2 by 2 submatrix H of B^-1. The eigenvalues
of H are in [1/C,1/c], hence det H>=1/C^2 and
|S_jk|=|H_jk|/det H<=C^2 |H_jk|. Equation (P1) proves BC.
For general U, the Schur complement is the inverse of a principal submatrix
of Sigma^-1, so its spectrum lies in [c,C]; conditional variance is at most
the marginal variance 1. This is the same block-inverse/Rayleigh argument
as `APP/lemmas/L2_CT.md:55`, independent of the decay assumption. QED.

Only M=15 is used for sandwich decay, including the conditional covariances
with each truth. The regression on truth residuals in the spherical tail
uses their spectral floor and does not need a new decay estimate conditioned
on the whole truth set.

## 2. Large-set inverse and regression tails (a different estimate)

**Lemma IR. PROVED (by this seat, unchecked).** Suppose A is a principal
submatrix of Sigma on any subset, with original positions retained. For
alpha>2 there is H, uniform in that subset and n, such that

    |(A^-1)_ij| <= H f(d(i,j)),
    f(d)=(1+d)^(1-alpha) [log(2+d)]^(alpha-1).                  (P2)

Consequently every population regression beta_T(l)=Sigma_TT^-1 Sigma_Tl has

    |beta_T(l)_v| <= H f(d(l,v)),
    ||beta_T(l)||_1 <= L0 < infinity,
    sum_{v in T:d(l,v)>r} |beta_T(l)_v| <= F(r)->0.             (P3)

Proof. At each positive integer distance there are at most two positions.
Let A_B retain entries at distances <=B, including its diagonal. Schur's
row/column-sum bound gives

    ||A-A_B|| <= 2 K_dec sum_{d>B}(1+d)^(-alpha)
              <= H1 B^(1-alpha).

For B>=B0, this is <=c/2, so A_B has floor c/2. Fix column j and use
the diagonal weight D_ii=exp(t d(i,j)), t=k/B, with k>0 fixed and small.
The row and column absolute sums of E=D A_B D^-1-A_B are at most

    2 K_dec sum_{d=1}^B (1+d)^(-alpha)(exp(td)-1)
    <= 2 K_dec t exp(k) sum_{d>=1} d(1+d)^(-alpha).

The series is finite for alpha>2. Choose k so this is <=c/4 for all
B>=1 (decreasing k if necessary). The algebraic part (Schur test + Neumann bound) of
`APP/lemmas/L2_CT.md:22-28` then applies [R06a-1]: (a) the entries of E=D A_B D^-1-A_B are
(A_B)_ik(e^{t(d(i,j)-d(k,j))}-1), bounded via |e^s-1|<=e^{|s|}-1 and |d(i,j)-d(k,j)|<=d(i,k)<=B;
(b) the weight is column-specific, D_ii=e^{t d(i,j)}, so (D A_B^-1 D^-1)_ij=e^{t d(i,j)}(A_B^-1)_ij since
d(j,j)=0; with lambda_min(A_B)>=c/2 and ||E||_2<=c/4, ||(D A_B D^-1)^-1||<=4/c. This gives

    |(A_B^-1)_ij| <= (4/c) exp(-k d(i,j)/B).

Also the resolvent identity gives
||A^-1-A_B^-1|| <= (2/c^2)H1 B^(1-alpha). For large d choose
B=floor(d/(M1 log(2+d))), where fixed M1 has k M1>alpha.
Then B>=B0 eventually, the exponential term is O((2+d)^(-k M1)),
and the resolvent error is bounded by a constant times f(d). Bounded d,
including diagonal entries, is absorbed into H using ||A^-1||<=1/c.
This proves (P2), without an external inverse-decay theorem.

Apply (P2) to B=Sigma_{T union {l}} and use
beta_T(l)_v=-(B^-1)_vl/(B^-1)_ll. The denominator equals
1/Var(W_l|W_T)>=1. This proves the first part of (P3), as in the
block-inverse argument `LOC2/lemmas/L3_CTd.md:73`.
The convergent series sum_{d>=1} f(d), and its tail, give
L0=2H sum_{d>=1} f(d) and F(r)=2H sum_{d>r} f(d). QED.

There is no second inversion in the sandwich proof. In particular the
preliminary conditional exponent alpha-2 is not used for its radius or Q.

## 3. Polynomial toolkit, regularity, and true-variable retention

The entrywise augmented Gaussian event of
`GROW/lemmas/L6_random_AR1.md:85` holds unchanged, with entry error
e_n=O(sqrt(log n/n)), also for standardized Gram entries. Every submatrix
of size at most J_n has operator error <=O(J_n e_n). For the lattice and
one-move neighbors J_n<=q+1=O(n^b), so J_n e_n->0 since b<1/2.
This proves sample floor c/2 simultaneously, with no union over subsets.
The same event gives bounded-dimensional covariance comparisons involving
Y, with coefficients theta_j/t_j uniformly bounded. PTV gives sample TV
as in `APP/lemmas/L3_LOC.md:63`; m_n^sharp=O(log n), anchored SE, energy
and fixed beta-min follow as in `GROW/lemmas/L6_random_AR1.md:115`.
Here energy is deterministic: ||X theta||<=sqrt(n-1) sum |theta_j|.

For clarity re-run L0' with the lattice family in
`GROW/lemmas/L2_NA_TL.md:12` and all its contrast vectors. Its log cardinality
and the contrast log cardinality are O(q+log n), and its maximal rank is q+1.
Set

    t_n=4(log|F_n|+2 log n+J_n),
    h_n^2=2(log|VV_n|+log n).

Exactly the mgf and normal unions in `GEN/lemmas/L1_lemmaE.md:33` give
failure probabilities at most n^-2 and 2/n: the rank factor 2^(J_n/2)
is absorbed by exp(-J_n). Thus t_n+h_n^2=O(q+log n). The event implies
RSS>=sigma^2[n-1-O(n^(2/3))-h_n^2-t_n], by completion of the square,
and hence RSS>=sigma^2 n/2 eventually. It also implies RSS<=C_R n.
The score remainder proof `GEN/lemmas/L1_lemmaE.md:74` needs only
J_n/n->0 and this RSS floor, so the same fixed kappa_E works. In the
sharp RSS bound `GROW/lemmas/L0_toolkit.md:33`,

    omega_n=4n^(-1/3)+(h_n^2+t_n+1)/n,
    omega_n log n ->0.                                      (P4)

These verify every size-sensitive step of LOC2 L1.1 with polynomial sizes.
Families may depend on the design when we condition on it: all Gaussian
noise bounds above are uniform on the common design event, so integration
is valid. For block tables use the separate family of all subsets of size
<=16, of polynomial cardinality, as in
`GROW/lemmas/L6_random_AR1.md:157`; this handles arbitrary selected partitions.

For any fixed D>0 in Section 0, Lemma BC with M=15 gives,
for l outside Q and any |U0|<=15, l notin U0,

    |Cov(W_l,W_j|W_U0)| <= H n^(-1/2), j in S0 minus U0.      (P5)

Indeed d(l,j)>d_n and (1+d_n)^(-alpha)<=D^(-alpha)n^(-1/2); the fixed H depends on D.
After summing bounded theta_j/t_j and dividing by conditional variances,
population Corr(W_l,Y|W_U0)=O(n^-1/2), uniformly. Constants may depend on
s0, theta, sigma. The population calculations with sample-dependent
theta/t are uniform algebraic bounds for all such bounded coefficient
vectors, as in `GROW/lemmas/L6_random_AR1.md:143`.

TL now follows directly from the proof
`GROW/lemmas/L2_NA_TL.md:27`: missing one truth costs signal >=c' n;
the contrast losses h_n sqrt(n) and t_n are o(n), because q=o(n).
The prior cost is O(log n). Thus P(TL(L))->1. This uses fixed beta-min,
not merely the original BM-infinity formulation for local alternatives.

## 4. Selection removal with polynomial references

Choose a fixed radius exponent rho satisfying

    1/(4 alpha) < rho < (1/2-b)/15,
    lambda=15 rho,  lambda+b<1/2.                            (P6)

Such rho exists exactly when alpha>17/2. Let R_n=ceil(n^rho),
H_l={v:dist(v,{l} union S0)<=R_n}, and I_l the subsets of
H_l minus {l} of size <=15. Then

    |H_l|<= (s0+1)(2R_n+1),   |I_l|<=H2 n^lambda.            (P7)

Retain h_{U,l}=n Corr_sample(W_l,Y|W_U)^2 from
`GROW/lemmas/L6_random_AR1.md:180`. For l outside Q and any |U|<=15
not containing l, put U0=U intersect H_l and V=U minus U0. Lemma BC
and the definition of H_l show that population partial covariances of
W_V with W_l and with Y, given U0, are O(R_n^-alpha). For the latter
sum over truths not already in U0; every such truth is farther than R_n
from every v in V. Noise contributes zero. Conditional variance floors
give the same bound for partial correlations. On the augmented entrywise
event the sample vectors a,b in the recursive correlation identity
`GROW/lemmas/L6_random_AR1.md:203` therefore obey

    ||a||+||b|| <= H3 v_n, v_n=R_n^-alpha+sqrt(log n/n),
    ||R^-1||<=H3,
    |z_0|<=H3 sqrt(log n/n),
    |z_U-z_0|<=H3 v_n^2.                                  (P8)

The last line follows by expanding the exact denominator
sqrt((1-a'R^-1 a)(1-b'R^-1 b)); all its arguments are o(1).
Consequently, uniformly in these U,l,

    |h_{U,l}-h_{U0,l}|
      <= H4 [sqrt(n log n) v_n^2+n v_n^4] =: w_n ->0,
    h_{U,l}<=H4 log n.                                    (P9)

For (P9), use |z_U^2-z_0^2|<=2|z_0||z_U-z_0|+|z_U-z_0|^2.
Since alpha rho>1/4, the largest terms are
n^(1/2-2 alpha rho) sqrt(log n), n^(1-4 alpha rho),
and powers of log n divided by sqrt(n); all tend to zero.
This proves the full replacement for GROW L6.3. An O(1) error would
suffice below, but the strict choice of rho provides o(1).

## 5. Spherical tails, ladder, and junk exclusion

For fixed l outside Q and deterministic U0 in I_l, regress W_l on
W_{U0 union S0}, exactly as in
`GROW/lemmas/L6_random_AR1.md:245`. By (P5), the vector of covariances
with the truth residuals has Euclidean norm O(n^-1/2); their conditional
Gram floor c implies ||alpha_vector||=O(n^-1/2). Regressions of truths
on U0 have bounded coefficients (dimension <=15, floor c). On the column
norm event this proves ||m||=O(1). The independent Gaussian regression
innovation has variance in [c,1]. Conditional on W_{U0 union S0} and eps,
the response residual is fixed, including its true-column sample scales.
Thus the sphere calculation and integration
`GROW/lemmas/L6_random_AR1.md:262` applies verbatim, before conditioning
on the augmented event. For log n/2<=t<=B_A log n, with any fixed B_A,

    P(A_cov intersect {h_{U0,l}>=t})
       <= H5 exp(-t/2+H5 sqrt(log n))+H5 exp(-h5 sqrt(n)).   (P10)

No extension of the source's range is needed [C1-Opus-9]: every threshold used below
(t_n(k) <= log(n+1)+2 log p, and 2 log p + tau log n with tau < 1) lies in GROW L6.4's
stated range [(1/2) log n, (2A+3) log n] (after the o(1) adjustment), so take B_A = 2A+3.
The CN_D conditioning device in that source at line 291 still applies.

Let J(t) count l outside Q for which some |U|<=15 has h_{U,l}>=t.
Using (P7), (P9), (P10), and p<=n^A, for
t_n(k)=log(n+1)+2log(p/k)-C0, 1<=k<=K_n, we get

    E[1_{A_cov} J(t_n(k))] <= k n^(-1/2+lambda+o(1)).       (P11)

Indeed p exp(-t_n(k)/2)=O(k n^-1/2); the count of references
multiplies by at most H2 n^lambda and exp(O(sqrt(log n)))=n^o(1).
The exp(-h5 sqrt(n)) term times p n^lambda is negligible uniformly in k.
All thresholds are >=(1-o(1))log n, so (P10) applies after subtracting w_n.

The score increment (6.10) of
`GROW/lemmas/L6_random_AR1.md:316` holds unchanged by (P9) and the
bounded-size score event. Per-block optimality
`GROW/lemmas/L3_sandwich.md:30` implies the same deterministic implication:
a maximizer of size k>2k0, k0=q+16s0, forces
J(t_n(min(2m_i,K_n)))>m_i/32 for some ladder point m_i=2^(i+1)k0.
This is the complete counting argument at
`GROW/lemmas/L6_random_AR1.md:329` through line 361, with C0=4 kappa_E+2.
By (P11) its probability is bounded by

    O(log n) n^(-1/2+lambda+o(1)) ->0.                      (P12)

It follows simultaneously that every maximizer has k<=2k0=O(n^b).
Truth inclusion follows from TV and the conditional Gaussian union over
all (j,U), j a truth, |U|<=15: the signal add gain is >=c' n and its
O(log n) prior/determinant cost is dominated. Addition is feasible by
the dichotomy in Section 0; when Q=[p], K_n=p and a size-p model already
contains all truths. This is the argument in
`GROW/lemmas/L6_random_AR1.md:366` with O(n^b) replacing O(log n).

For junk deletion choose a fixed tau with

    max(2lambda, 1/2) < tau < 1-2b.                      (P13)  [R06b-1]

Existence: (P6) gives 2lambda < 1-2b, and b < 1/4 gives 1/2 < 1-2b; the lower
bound 1/2 keeps the (P14) threshold, after subtracting w_n = o(1), inside the
range t >= (log n)/2 of (P10) [R06b-1]. Equations (P7), (P9), (P10) and a union
bound imply, with probability tending to one,

    max_{l outside Q, |U|<=15, l notin U} h_{U,l}
        <= 2 log p + tau log n,                            (P14)

since its failure probability on A_cov is n^(lambda-tau/2+o(1)).
The deletion score gain for any l in a maximizer outside Q is, by (6.10)
and the exact prior ratio, at least

    log(p/k)+(1/2)log(n+1)-(1/2)h_{U_b minus {l},l}
       -2 kappa_E-o(1)
    >= [(1-tau)/2-b]log n-O(1)>0.                         (P15)

This contradicts maximality. All bounds hold simultaneously over possible
partitions and maximizers, using deterministic reference families rather
than a conditional law for a selected partition. If Q=[p], junk exclusion
is vacuous. Equations (P12)-(P15) prove P(Sand_n)->1.

## 6. NA-R re-run on a polynomial lattice

The constant atom l1 bound in `LOC2/lemmas/L4_LOCd.md:51` is insufficient
here: log q can be of order log n. We prove a vanishing l1 bound instead.
Take r_n=ceil(log log(n+exp(exp(1)))), B_l={v!=l:d(v,l)<=r_n},
T'=T intersect B_l. Frames consist of the single functional
r_{T,l}=W_l-E[W_l|W_T']; there are at most p 2^(2r_n) frames and
log N_n<=log p+o(log n). Atoms are the coordinate functionals W_v, v in Q,
each of variance 1. Put lambda_vector=beta_T(l)-zero_padded(beta_T'(l)).
Then e_{T,l}=r_{T,l}-sum_v lambda_v W_v, an exact deterministic row identity.

Here is the stronger tail identity. For w in T minus T', write
E[W_w|W_T']=sum_v gamma_{w,v} W_v. Conditional expectation of
E[W_l|W_T] given W_T' equals E[W_l|W_T']; hence the coefficient difference
on T' is minus sum_{w in T minus T'} beta_T(l)_w gamma_w.
The coefficient difference on T minus T' is beta_T(l)_w. Uniqueness of
coefficients follows from the population floor. By (P3), uniformly,

    ||lambda_vector||_1
       <= (1+L0) sum_{w in T minus T'} |beta_T(l)_w|
       <= (1+L0) F(r_n) =: L_n ->0.                       (P16)

Also D=E[W_l|W_T]-E[W_l|W_T'] has row variance
<=||lambda_vector||_1^2: all covariance entries have absolute value <=1.
The residual e_{T,l} is orthogonal to D, so

    Var(r_{T,l})=Var(e_{T,l})+Var(D)
       <=(1+L_n^2/c)Var(e_{T,l}).                         (P17)

Thus (R1), (R2), and even the stronger atom bound with a log log n term hold:
L_n^2(log(q+1)+log log n)=o(log n) and eta_n=L_n^2/c->0.
No conditional-covariance estimate for large sets is needed here.

To re-run the probability proof, put ell=log|P_n|=O(q+log n), where
P_n={(T,l):T in L,l notin T}. Assume it is nonempty; otherwise NA is
vacuous. In Step 2 of `LOC2/lemmas/L2_NAR.md:62` use precisely its
x=ell+2log n, delta_n=2sqrt(x/(n-1))+2x/(n-1), and
v_n=4(ell+q+2log n). The E_a,E_b chi-square unions retain failure bounds
3n^-2,n^-2, even though the pair family is exponential in q.
We have delta_n=O(sqrt((q+log n)/n)+(q+log n)/n)->0 and
v_n=O(q+log n)=o(n). E_c,E_d and their probabilities are unchanged:
the frame count still has log N_n<=log p+o(log n), m0=1, and the atom
argument conditions on eps, not on fitted regressions
(`LOC2/lemmas/L2_NAR.md:72`). In particular its E_d Chernoff bound is
valid because x'_n=O(log n). For E_e one may use the explicit threshold
y_n^2=2log(2(q+1))+2log log n: the conditional Gaussian union has failure
probability <=1/log n, and L_n^2 y_n^2=o(log n) by (P16).
This is also a valid alternative to the source's revised adaptive E_e
threshold (`LOC2/lemmas/L2_NAR.md:79`). Neither choice needs an atom-norm event.

Step 3 (`LOC2/lemmas/L2_NAR.md:88`) now gives
zeta_n^2<=2 log p+o(log n), by (P16)-(P17). The sample projection error
in Step 4 (`LOC2/lemmas/L2_NAR.md:96`) is bounded by

    epsilon_n <= H6 sqrt(v_n(q+log n)/n)
              =O((q+log n)/sqrt(n)) ->0,                   (P18)

since b<1/2. Its normalization multiplier is 1+O(v_n/n)=1+o(1).
Thus uniformly Z_{T,l}^2<=2 log p+o(log n). In contrast the actual
NA threshold is

    c_n=log(n+1)+2log p-2log(q+1)-4 kappa_E-2
       >=2log p+(1-2b)log n-O(1).                         (P19)

The positive fixed slack 1-2b proves max Z^2<=c_n with probability
tending to one. Finally the reduction
`GROW/lemmas/L2_NA_TL.md:41` uses (P4), so its excess
O(log n)(omega_n+log n/n) tends to zero with the same fixed kappa_E.
It proves P(NA(L))->1. This completes the polynomial NA proof; it does
not simply assert LOC2 NA-R's original (N0).

## 7. Assembly, cutoff audit, and changed-step ledger

On Sand_n the emitted maximizer lies in L. On Sand_n intersect NA intersect
TL, deterministic descent deletes its extras one at a time and the shipped
cap ell_n+|S_tilde_0| exceeds the number of extras. The proof at
`LOC2/lemmas/L5_assembly.md:26` has no polylog-size use once these events
and feasibility hold. It gives D_n bounded by the sum of their failure
probabilities. The global population floor supplies LSF; the posterior
and M5(0) integration at `LOC2/lemmas/L5_assembly.md:30` is unchanged and
gives all the conclusions in Section 0. This is conditional on the named
inputs, with their statuses preserved, and does not claim a new proof of
POST or operational closure.

Changed steps, exhaustively relative to the cited LOC2/APP/GROW route:

1. Exponential CD for arbitrary U is replaced, in the sandwich only, by
   finite-dimensional BC (Section 1). Large-set CD is not invoked.
2. Exponential regression l1/tail is replaced by IR (Section 2).
3. Q has radius n^b and q=O(n^b); sample floors use q sqrt(log n/n)->0.
   L0' is re-run with log family size O(q+log n), retaining bounded score
   remainders; the sharp excess requires (q+log n)log n/n->0 (Section 3).
4. Selection-removal radius becomes n^rho; reference count becomes
   O(n^(15rho)); the recursive correlation error is explicitly re-bounded
   in (P8)-(P9), not claimed to retain the source's faster rate.
5. The fixed-reference spherical tail is unchanged; its count expectation
   and ladder acquire n^lambda, as (P11)-(P12). The maximum threshold's
   coefficient 1/2 in source (6.7) becomes tau, as (P13)-(P14).
6. Truth inclusion uses the same PTV argument and the rechecked polynomial
   feasibility dichotomy. Junk deletion requires (1-tau)/2>b (P15).
7. NA uses shrinking l1 atoms (P16), variance ratio (P17), polynomial pair
   chi-square unions, projection error (P18), and slack (P19). The old
   bounded-l1 argument alone does not suffice.
8. TL uses t_n+h_n^2=O(q+log n)=o(n) and fixed beta-min. Descent, cap,
   posterior transfer and output-error assembly need no further changes.

Rate audit: (the amended (P13) lower bound tau>1/2 costs nothing, since b<1/4 for alpha>2 [R06a-3].) BC is valid for any alpha>0. IR requires alpha>2. Polynomial
sample floors and (P18) require b<1/2, true for alpha>1. Toolkit, TL,
feasibility require b<1, also true. Selection removal requires
rho>1/(4alpha). The size ladder only requires 15rho<1/2. The strictly
stronger junk bound requires 15rho+b<1/2. Substituting b=1/(2alpha)
shows feasible rho and tau exist iff alpha>17/2. At equality there is
no fixed slack: this proof does not establish the boundary. For example,
one fully explicit choice for alpha>17/2 is

    rho = (1/(4alpha) + (1/2-1/(2alpha))/15)/2,
    lambda = 15rho,
    tau = (2lambda + 1-1/alpha)/2.

The preliminary alpha-minus-two conditional exponent is avoidable. Its
other warnings are real: polynomial q changes c_n by 2log q, requires a
vanishing atom l1 norm, and changes both the ladder and maximum union.
All three changes are accounted for above. No assertion of optimality
over alternative sandwich/reference constructions is made.
