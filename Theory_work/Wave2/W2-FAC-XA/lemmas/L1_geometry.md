# L1 — A conservative uniform coupling of residual noise statistics

Status: PROVED (by this seat); cross-family R02b verdict PASS-WITH-FIXES (minor),
F1–F6 applied. Review: reviews/R02b_L1_geometry.md. Not a path or score theorem;
full protocol PROVED-CHECKED label is withheld until all required gates pass.
Setting: Sigma is a p by p correlation matrix, lambda_min(Sigma)>=c>0 fixed.
Raw rows iid Gaussian with covariance Sigma; d=n-1>=p, centered covariance S,
R=D^{-1/2} S D^{-1/2}, D=diag(S). All norms below are Euclidean operator norms
unless marked F (Frobenius). Centering removes one Gaussian degree of freedom.

## L1a: a sufficient (not sharp) random Gram rate
If p=o(sqrt(n)), ||R-Sigma||=O_P(p/sqrt(n)), and
e=||Sigma^{-1/2}(R-Sigma)Sigma^{-1/2}||=O_P(p/sqrt(n))=o_P(1).
This deliberately does NOT claim the sharper relative sqrt(p/n) rate.

Proof. dS is the Gram of d independent N(0,Sigma) rows, by an orthogonal change
of basis in row space whose first direction is the constant vector. Gaussian
fourth moments give E(Sij-Sigmaij)^2=(1+Sigmaij^2)/d and
E(Sii-1)^2=2/d. (Expand the product of four centered normals into its three
pairings; rows are independent.) Thus E||S-Sigma||F^2<=2p^2/d.
Let B={all Sii in [1/2,3/2]}; P(B^c)<=8p/d by Chebyshev and a union bound.
On B the map (u,v)->1/sqrt(uv) is Lipschitz with an absolute constant, and
|Rij-Sigmaij| <= 2|Sij-Sigmaij|+C|Sigmaij|(|Sii-1|+|Sjj-1|).
Square, sum, use |Sigmaij|<=1 and the displayed second moments: the expectation
of 1_B ||R-Sigma||F^2 is <=C p^2/d. Markov, together with P(B^c)->0, gives
the asserted O_P rate. Operator norm <= Frobenius norm; relative norm <=
c^{-1} times absolute norm. No spike-free covariance assumption is used. QED.

Explicit uniform constants (R02b F1): the Lipschitz constant above may be 2;
E[1_B ||R-Sigma||F^2]<=80p(p-1)/d and
P(||R-Sigma||F>M p/sqrt(d))<=80/M^2+8p/d for M>0.
Consequently P(e>1/4)<=1280p^2/(c^2 d)+8p/d. These bounds are uniform over
all correlation matrices with the same floor c. For p=1, R=Sigma=1 exactly.

## L1b: deterministic simultaneous residual-direction comparison
Suppose e<=1/4. Put A=Sigma^{1/2}, E=Sigma^{-1/2}(R-Sigma)Sigma^{-1/2},
L=(I+E)^{1/2}, B=L A. Columns of A are a_j, columns of B are b_j.
Then A'A=Sigma, B'B=R, ||L-I||<=e, and sigma_min(L)>=sqrt(1-e).
For T subset [p] and j not in T, define
q_A(T,j)=(I-P_{A_T})a_j / ||(I-P_{A_T})a_j||,
and q_B analogously. Empty T has zero projection. Simultaneously for all T,j,
||q_B(T,j)-q_A(T,j)|| <= 10 e/sqrt(c).

Proof. Let U=span(A_T), V=LU. For a unit u in U, dist(u,V)<=||(I-L)u||<=e.
For a unit v=Lu in V, ||u||<=1/sqrt(1-e), so dist(v,U)<=e/sqrt(1-e).
The identity P_U-P_V=P_U(I-P_V)-(I-P_U)P_V implies
||P_U-P_V||<=e+e/sqrt(1-e)<=3e; transpose identifies the first norm
with ||(I-P_V)P_U||. Since ||a_j||=1,
||(I-P_V)b_j-(I-P_U)a_j||<=e+3e=4e.
The residual norm for A is >=sqrt(c): for any coefficients t,
||a_j-A_T t||^2 >= c||(1,-t)||^2>=c.
For nonzero vectors r,s, ||r/||r||-s/||s||||<=2||r-s||/||s||.
B has full column rank, so its residual is nonzero. The bound 8e/sqrt(c)
therefore suffices; 10 is retained as slack. QED.

## L1c: conditional noise coupling, all subsets at once
One may realize the coupling on the original data space. Let X denote the
centered sample-sd-standardized design and epsilon~N_n(0,sigma^2 I) its independent
raw noise. With B from L1b put O=X B^{-1}/sqrt(d), so O'O=I and CO=O.
Define z=O'epsilon/sigma and r=||(C-OO')epsilon||^2/sigma^2.
Conditional on the entire raw design, z~N_p(0,I), r~chi-square(d-p), independently;
these conditional laws are constant, so (z,r) is independent of the ENTIRE design,
not merely R. When d=p, r=0. Define g_A=A'z,
g_B=B'z. They have respective conditional covariances Sigma and R. The noise
energy ||z||^2+r is chi-square(d) and has the correct joint law with each g.
Precisely, for design X define Z_X(T,j)=x_j'(I-P_{X_T})Cepsilon /
[sigma sqrt(x_j'(I-P_{X_T})x_j)]. The identity X=sqrt(d)OB gives
Z_X(T,j)=q_B(T,j)'z simultaneously for every T,j. Set Z_B=Z_X and Z_A=q_A'z.
The latter has the joint law of all such statistics for any deterministic
centered exact-Gram design with Gram d Sigma, including C2-E; isotropic Gaussian
noise makes the joint law depend only on the Gram. It is a reference coupling,
not the assertion that the reference design was the observed design.
On the event {e<=1/4}, whose complement has the uniform bound given in L1a,
Thus sup_{T,j}|Z_B-Z_A|<=10 e||z||/sqrt(c).
By L1a and ||z||=O_P(sqrt(p)), this supremum is O_P(p^{3/2}/sqrt(n)).
In particular it tends to zero for p<=n^a, any fixed a<1/3, including the
locked a<1/4 target. Bounded p is included.

The joint law assertion follows because conditional Gaussian projections onto
the p-dimensional design span have identity covariance in orthonormal
coordinates, and the orthogonal residual is independent. Signal is not included
in Z. This lemma couples residual statistics at the SAME T; it does not couple
the adaptive sequences of T. It also does not compare the production score's
ridge residuals, determinant penalties, start tables, or truth-out moves.

Scope (R02b F6): sample correlation R is invariant to raw row means and positive
column scales. In C1, c=1-rho; in C2, c>=1-lambda_hi^2. This invariance does not
relax the standardized-scale signal convention or assert an iid non-Gaussian law.
The constant 8 is proved in L1b; 10 in statements is intentional slack.

## Precisely what remains
An o_P(1) statistic perturbation does not imply identical argmin indices, nor
that approximate greedy deletions preserve FAC-B's exact interval invariant.
Both the score transfer and the robust adaptive invariant require separate lemmas.
The result covers both CS and bounded unequal-loadings covariance since the
idiosyncratic diagonal is >=1-lambda_hi^2; it alone proves neither target.
