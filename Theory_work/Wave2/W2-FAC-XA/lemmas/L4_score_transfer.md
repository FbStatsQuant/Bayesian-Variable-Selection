# L4 — Uniform production-score comparison on the truth-containing lattice

Status: R04 ACCEPT BOTH WITH REQUIRED FIXES, applied below; deterministic conditional lemma;
no unreviewed XA lemma is used as a theorem.

Let A and B=L A be invertible p by p matrices, A'A=Sigma a correlation matrix,
lambda_min(Sigma)>=c>0, B'B=R also a correlation matrix, ||L-I||<=e<=1/4.
Every subspace pair span(A_T),span(B_T) has projection difference <=3e:
the directed gaps are at most e and e/(1-e), respectively, by comparing u with Lu;
the projection-difference identity in L1b's proof bounds their sum by 3e.
This elementary derivation is included here, independent of L1's probabilistic result.
Let theta have fixed support S0 and bounded l1 norm, with fixed nonzero entries.
Let d=n-1>=p. Fix z in R^p and r>=0 and sigma>0. Define coupled raw-response
coordinates y_A=(sqrt(d) A theta+sigma z, sigma sqrt(r)), y_B analogously.
Design columns are (sqrt(d) a_j,0) and (sqrt(d) b_j,0). Their norm squared is d.
Theta is fixed on the STANDARDIZED scale, as in STATEMENT; raw-scale fixed beta
would give a random theta and requires a separate coupling argument.
The extra coordinate represents orthogonal residual energy; no dimension claim
is made when r=0. Normalize each response to squared norm d, exactly as production.
Use the exact production score F, prior w, g=n, nu=n/2+.01 and .02 offset.

Uniform assumptions on a deterministic event: ||z||^2<=C p L_n,
c1 n<=r<=C1 n, where L_n>=1 and p L_n=o(n). All constants below may depend
on c,c1,C1,C,sigma,||theta||1, but not T,p,n,e. These residual bounds are suitable
for p=o(n), not p comparable with n. For all large n there exist constants
C_A,C_B independent of T such that

 sup_{T containing S0}|(F_B(T)-C_B)-(F_A(T)-C_A)|
       <= C2 [e(p L_n+1)+p/n+1/n].                  (ST)

Hence every neighbor pair BOTH containing S0 has gain discrepancy at most twice
the right side. This includes null deletions, null additions and null-out swaps.
It excludes truth-out moves. It is not the full UP hypothesis in L2.
The onset n0 depends on the sequences p_n L_n/n (and any chosen e_n sequence),
not just the displayed constants. Start-mode block tables m(U)/m(empty), and
every model missing a truth, are outside ST; X1 is not proved by this lemma.

Representation bridge: for actual centered standardized rank-p design X, choose
B with B'B=R and U=XB^{-1}/sqrt(d), giving U'U=I and CU=U. Then with
z=U'Cepsilon/sigma and r=||(I-UU')Cepsilon||^2/sigma^2,
X'Y=sqrt(d)B'(sqrt(d)Btheta+sigma z) and
Y'Y=||sqrt(d)Btheta+sigma z||^2+sigma^2 r. Thus Gram, cross-products and response
norm equal the coordinate representation, and the production score is identical.
Conditional on X, z and r are independent standard Gaussian/chi-square(d-p);
their law does not depend on X. The A-world with the same z,r has the exact-Gram
reference law. A=Sigma^(1/2), L=(Sigma^(-1/2)R Sigma^(-1/2))^(1/2) is one valid
choice, with ||L-I|| bounded by the relative Gram deviation when that is small.

## Proof
Write V_M=||y_M||^2, RSS_M(T)=sigma^2[r+||(I-P_{M_T})z||^2] for M=A,B.
Since T contains S0, the signal residual vanishes exactly. V_M is between
positive multiples of n: its lower bound is sigma^2 r, and its upper bound
follows from ||M theta||<=||theta||1 (unit columns), ||z||^2<=CpL_n=o(n).
Also |V_B-V_A|<=C e[n+sqrt(n)||z||] <=C e n: expand the two signal terms
using B=L A, ||A theta||<=||theta||1 and ||(B-A)theta||<=e||theta||1.
Projection difference gives |RSS_B(T)-RSS_A(T)|<=3 sigma^2 e||z||^2.

For either M, let G_T=d M_T'M_T, H_T=(n+1)G_T+I, and v_T=X_T'y_M.
Define the unscaled ridge residual Q^raw_M=V_M-n v_T'H_T^{-1}v_T.
Eigenvalues of G_T are >=d c(1-e)^2. Spectral decomposition in the design
span gives, uniformly in T,

 Q^raw_M = RSS_M + (V_M-RSS_M)/(n+1) + J_M,
 0<=J_M <= C V_M/n^2 <=C/n.

Indeed on a unit eigen-direction of G_T with eigenvalue g, n v'H^-1v
has fitted coefficient n g/[(n+1)g+1]; its deficit from n/(n+1) is
n/[(n+1)((n+1)g+1)]<=C/n^2. Multiply by fitted energy <=V_M.
After response normalization, Q_M=(d/V_M) Q^raw_M, hence

 .02+Q_M=(d/V_M) W_M,
 W_M=RSS_M+(V_M-RSS_M)/(n+1)+J_M+.02 V_M/d.

Every W_M lies between positive multiples of n, since RSS_M>=sigma^2 r.
The preceding estimates give
 |W_B-W_A|<=C[e(||z||^2+1)+1/n].
The mean-value bound for log gives
 nu|log W_B-log W_A|<=C[e(pL_n+1)+1/n].

Finally
 logdet H_T-logdet(G_T+I)=|T| log(n+1)+D_M(T),
 D_M=logdet(I+G_T^{-1}/(n+1))-logdet(I+G_T^{-1}),
 |D_M|<=tr(G_T^{-1})<=C |T|/n<=Cp/n.
Therefore
 F_M(T)=log w(|T|)+log c_n-|T|log(n+1)/2-D_M(T)/2
        -nu log W_M(T)-nu log(d/V_M).
Take C_M=-nu log(d/V_M); all size/prior terms cancel on comparing the same
T. Combine the bounds to obtain ST. Differences of two scores cancel C_M,
proving the gain assertion. Empty T is harmless if S0 empty, although the
locked statistical target assumes s0>=1. QED.
Here log c_n is the production marginal likelihood's n-only constant; it cancels.

## Prospective rate, not an assembled theorem
If separately established inputs give e=O_P(p/sqrt(n)) and ||z||^2=O_P(p),
one can use slowly diverging deterministic envelopes L_n so that the ST bound
is o_P(1) whenever p<=n^a, fixed a<1/4. This rate arithmetic does not establish
truth-move negativity, start-mode behavior, adaptive geometry, or delivery.
In the iid Gaussian setting, residual r~chi-square(n-1-p) should furnish the
required residual-energy event. That invocation awaits independent lemma checks.

## General-assumption ingredients
No factor or CS identity appears here. The proof needs a GLOBAL eigenvalue
floor, a common near-identity linear coupling, bounded fixed signal l1 norm,
and positive residual degrees of freedom comparable to n. A log-size sparse
floor alone does not justify inverses of large T; iid rows alone does not
furnish the near-identity map without a concentration argument.

Numerical scope: N6_score_transfer.py is a fixed-size algebra/nonnegative-J check;
J is defined by subtraction there, so the identity is not an independent J test.
Its random Gram is generated with 2048 rows even though score n=512. Additional
real-data fidelity, scaling, and projection/error-ratio tests are supplied by
reviews/R04_scratch/R04_l4_checks.py and R04_l4_checks_out.json, incorporated as
review evidence. They do not establish a sharper relative-norm rate.
