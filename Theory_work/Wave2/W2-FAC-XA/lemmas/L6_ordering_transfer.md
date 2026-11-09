# L6 OT — actual null deletion ordering via OLS residual statistics
Status: PROVED (by this seat, unchecked). Conditional deterministic lemma.

Use one actual centered standardized rank-p design X, Gram G=X'X with
lambda_min(G)>=c(n-1), response Y=Xtheta+Cepsilon. Fixed support S0, fixed
standardized theta of bounded l1 norm. Let T contain S0, j in T minus S0.
Assume ||Y||^2 between constants times n, full-model noise residual >=c1 n,
and projected noise energy <=C p L_n=o(n). Constants fixed, c,c1>0.
Define Z_j=(x_j'(I-P_{X_{T\j}})Cepsilon)/
[sigma sqrt(x_j'(I-P_{X_{T\j}})x_j))]. Let F be the exact production score,
and nu=n/2+.01. There are quantities A_T,b_T>0 independent of j such that

 F(T\j)-F(T)=A_T - nu log(1+b_T Z_j^2)+r_{Tj},
 sup_{T,j}|r_{Tj}|<=C2/n,                         (OT)

where nu b_T is bounded above and below by positive constants, and
nu b_T/(1+b_T u) is bounded below on 0<=u<=C p L_n.
If j maximizes the actual NULL deletion gain, then
 |Z_j|<=min_null |Z_l|+C3/sqrt(n).                (ORDER)
No assertion that a null deletion beats swaps, additions or truth moves is made.

Proof. Write V=||Y||^2 and use the exact ridge decomposition in L4, whose proof
applies here directly: Qraw_T=RSS_T+(V-RSS_T)/(n+1)+J_T, 0<=J_T<=C/n.
After response normalization, W_T=RSS_T+(V-RSS_T)/(n+1)+.02 V/(n-1)+J_T.
Set W0_T=W_T-J_T. Since T\j still contains S0,
RSS_{T\j}-RSS_T=sigma^2 Z_j^2 exactly. Consequently
W_{T\j}=W0_T+n sigma^2 Z_j^2/(n+1)+J_{T\j}.
Every W0 is >=c1 n. Dropping J at both endpoints changes the log-likelihood
gain by <=C/n, since nu=O(n) and J<=C/n. Thus the likelihood gain equals
-nu log(1+b_T Z_j^2)+O(1/n), b_T=n sigma^2/[(n+1)W0_T].
W0_T is between fixed multiples of n, proving the derivative statements, since
Z_j^2<=||P_X Cepsilon||^2/sigma^2<=CpL_n=o(n).

The determinant part for deleting j is -1/2 log[(H_T^{-1})jj/((G_T+I)^{-1})jj],
where H_T=(n+1)G_T+I. For t>=0 and lambda_min(G_T)>=c(n-1),
(1+t/[c(n-1)])^(-1)G_T^{-1} <= (G_T+tI)^(-1) <= G_T^{-1}.
Apply on diagonals with t=1/(n+1) and t=1, using
H_T^{-1}=(n+1)^(-1)(G_T+I/(n+1))^{-1}.
The logarithm of the ratio is -log(n+1)+O(1/n), uniformly in T,j.
Add the exact size-prior term log w(|T|-1)-log w(|T|), independent of j.
Thus A_T is that term plus .5 log(n+1), and OT follows.
At a maximizer, monotonicity with derivative bounded below implies
Z_j^2<=min_l Z_l^2+C/n, hence ORDER. QED.

Coupling corollary (conditional on a separately established coupling): if all
same-state actual/reference OLS deletion statistics differ by <=epsilon0,
the selected null satisfies |Z_Aj|<=min_null|Z_Al|+2epsilon0+C3/sqrt(n).
For exact CS OLS, Z_Aj=sqrt(q/(q-1))*(xi_j-x_T^OLS),
q=|T|+(1-rho)/rho; the common factor is >=1, so the same tolerance upper-bounds
coordinate-distance excess. Here x_T^OLS=(sum_T xi -sqrt((1-rho)/rho)*eta)/q.
This centre has a CONSTANT offset and the same scalar drift as L3. It is not
FAC-B's ridge centre: their discrepancy must be accounted for before substituting
the corollary into a theorem stated with the ridge-centre geometry.

No new iid consistency conclusion is claimed. This lemma does not establish
safe-move dominance, start mode, truth protection, posterior or delivery.
