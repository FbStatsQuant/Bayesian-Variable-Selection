# L5 RN — covariance-general relative correlation bound with logarithmic slack
Status: PROVED (by this seat, unchecked). This is a new lemma, not a claim that
the sharper log-free RN suggested by the midpoint has been proved.

Population Sigma has unit diagonal and lambda_min>=c>0. Gaussian raw rows,
d=n-1, sample centered covariance S, correlation R=D^{-1/2} S D^{-1/2}.
For p log(p+1)=o(d), uniformly over this covariance class,

 e_R=||Sigma^{-1/2}(R-Sigma)Sigma^{-1/2}||
       =O_P(sqrt(p log(p+1)/d)).                    (RN-log)

Proof. Put E0=Sigma^{-1/2}S Sigma^{-1/2}-I. Orthogonal row centering shows
I+E0=W'W/d with W having d independent N_p(0,I) rows. For a unit v, the
moment generating function of d*v'(I+E0)v is (1-2t)^(-d/2). Chernoff gives
P(|v'E0v|>u)<=2 exp(-d u^2/8) for 0<u<1 (expanding -log(1-2t) or optimizing
t gives this conservative constant). A 1/4-net of the unit sphere with <=9^p
points exists by disjoint-radius-1/8-ball volume comparison. For symmetric E0,
||E0||<=2 max_net|v'E0v|: approximate a maximizing unit vector and bound the
quadratic-form difference by 2*(1/4)||E0||. Thus
P(||E0||>2u)<=2*9^p exp(-d u^2/8).
Taking u=C sqrt((p+t)/d), for suitable fixed C, gives failure <=2exp(-t)
whenever u<1; hence ||E0||=O_P(sqrt(p/d)), including bounded p.

Each d*Sjj is chi-square(d), irrespective of column dependence. The same
Chernoff bound plus union gives max_j|Sjj-1|=O_P(sqrt(log(p+1)/d)); with tail
parameter t one can use sqrt((log(2p)+t)/d). On max deviation<=1/2 the scalar
derivative of x^(-1/2) is bounded by 2, so for Q=D^{-1/2}-I,
||Q||<=2 max_j|Sjj-1|.
Let F=Sigma^{-1/2} Q Sigma^{1/2}. Since lambda_max(Sigma)<=tr(Sigma)=p,
||F||<=sqrt(p/c)||Q||=O_P(sqrt(p log(p+1)/d))=o_P(1).
The exact factorization is
 Sigma^{-1/2} R Sigma^{-1/2}=(I+F)(I+E0)(I+F)',
so e_R<=2||F||+||F||^2+(1+||F||)^2||E0||. This proves RN-log.
The tail bounds depend only on c,p,d, not on loadings or truth positions. QED.

For p<=n^a, a<1/4, RN-log together with the already separately checked L1b/c
would give residual-statistic error O_P(p sqrt(log(p+1)/n)), not the coarser
p^(3/2)/sqrt(n). Multiplying by ambient p in L3's shadow-width estimate gives
O_P(p^2 sqrt(log(p+1)/n)); this tends to zero polynomially at a<1/4. This is
ONLY rate arithmetic. It supplies neither a shadow-midpoint bound nor an
exception-count/end-entry argument. Do not assemble X2 from this paragraph.

Numerical falsification input: R05_scratch/R05_relnorm.py and its output (reviewer
diagnostic, not a proof), plus N1/N2 norm tables. A deterministic factorization
check and log-slack rate diagnostic are supplied in numerics/N7_transfer.py.
