Status: PROVED (by this seat, unchecked)
Seat: research parallel prover, Codex gpt-6.1-sol, high effort

# L6 — Verified examples for RM2 (claim (C5))

All claims below are asymptotic. Each PROVED label concerns the verification of
hypotheses, conditional on the theorem and input statuses recorded at the end.
The method, noise, score, prior, implementation premises and shipped configuration
are exactly RM2 `STATEMENT.md:40` (§1). They are assumed in every example; no
design family is added to any theorem. In particular this gives reported-model
consistency on the output event, not a delivery theorem.

Path abbreviations used in citations: RM2 = `Theory_work/Wave3/W3-RM2`;
RM = `Theory_work/Wave3/W3-RM`; POLY =
`Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md`; LOC2 =
`Theory_work/Wave2/W2-LOC2`; UNI = `Theory_work/Wave2/W2-UNI`;
APP = `Theory_work/Wave2/W2-APP`; GROW = `Theory_work/Wave1C/C-GROW`.
Thus, for example, POLY:118 is an exact repository path:line citation.

The v1.4 clauses of RM2 §3.2 are used, as instructed in the brief. The older
17/2 language still present in RM2 `STATEMENT.md:250` and `:301` describes the
old verification; it is not used to override the new assumptions. The Form R
implications (D-loc^b) => (D-R^b) => (W-R), and (C2), are taken as given by the
brief (RM2 `STATEMENT.md:174`, §3.2, and `:199`, (C2)).

## 0. Two uniform estimates used in E2 and E3

Let B be a unit-diagonal positive definite matrix indexed by an injective map
pi:[p] -> Z, with spectrum in [c,C] and

    |B_jk| <= K_dec (1+d(j,k))^(-alpha),  d(j,k)=|pi(j)-pi(k)|.

All constants below depend only on (c,C,K_dec,alpha), and on 15 when indicated,
not on n,p, the selected subset or the positions. A principal submatrix retains
the same spectral bounds. There are at most two indices at each positive integer
distance; gaps in the injection only improve every bound.

**Bounded conditioning.** POLY:78-109 (Lemma BC) gives a constant K_15 with

    |B_jk - B_jU B_UU^(-1) B_Uk| <= K_15 (1+d(j,k))^(-alpha)

whenever |U|<=15 and j,k are distinct and outside U. Conditional variances are
in [c,1]. One explicit permissible choice is

    K_15 = C^2 max_{2<=m<=17}
             [(m-1)! max(1,K_dec)^(m-1) (m-1)^alpha c^(-m)].

The proof uses only finite principal matrices and their distances and therefore
applies unchanged to an injection into Z, and to deterministic Gram matrices.

**Regression localisation (including the refitting error).** Assume alpha>2.
POLY:118-167 (Lemma IR) supplies H and

    f(d)=(1+d)^(1-alpha) [log(2+d)]^(alpha-1),
    |(B_SS^(-1))_ij| <= H f(d(i,j)),
    |beta_T(l)_v| <= H f(d(l,v)),
    F(r)=2H sum_{d>r} f(d) -> 0.

Here beta denotes regression using B, uniformly over all subsets T excluding l.
Set

    J = H f(0) + 2H sum_{d>=1} f(d) < infinity,
    D = 1 + 2K_dec sum_{d>=1}(1+d)^(-alpha) < infinity.

Every inverse principal matrix has induced column-sum norm at most J; every
rectangular submatrix of B has induced column-sum norm at most D. For
N_l={v in Q\{l}:d(l,v)<=r}, A=T intersect N_l and E=T\A, the normal equations give

    beta_A(l) = beta_T(l)_A + B_AA^(-1) B_AE beta_T(l)_E.

Consequently, with zero padding (and the same result when A is empty),

    ||beta_bar_T(l)-beta_bar_A(l)||_1
       <= (1+JD) ||beta_T(l)_E||_1 <= (1+JD)F(r) =: L(r).        (0.1)

This controls both the omitted coefficients and the change in the retained
coefficients. Bounding only the omitted tail would not prove (W-loc).
Orthogonal projection in the inner product defined by B also gives

    Var_B(l|A) <= Var_B(l|T) + L(r)^2
               <= [1+L(r)^2/c] Var_B(l|T).                    (0.2)

Indeed the difference of the two residuals is a linear combination of
unit-variance coordinates with coefficient norm at most L(r), orthogonal to
the full-regression residual. For an exact Gram, multiply the variances by n-1.

Choose henceforth r=floor(sqrt(log n)). Then |N_l|<=2r=o(log n), L(r)->0, and
L(r)^2 log(|Q|+1)=o(log n) whenever |Q|<=n^b. For (W-loc), any fixed h>0 with
h+b<1/2 eventually satisfies |N_l| log 2<=h log n. For (D-loc^b), |N_l|=o(log n)
is exactly the required entropy bound. Equations (0.1)-(0.2) verify the other
two local-regression clauses. There is no extension of IR to alpha<=2 here:
its summability and weighted-band proof both require alpha>2 (POLY:145, :166).

## E1. Inherited examples

Status: PROVED (by this seat, unchecked), by containment with recorded sources.

Every RM-F example is an RM2-F example. Precisely the inherited hypothesis list
is (T1-F), (FL-16), (FL-Q), (V), polylogarithmic (L-size), (L-feas), (L-gain)
with eta<eta_A, and (N-chi) or (N-D); for the block-relative variant replace
(V),(L-gain),(FL-16) by their actual-partition versions. RM2
`lemmas/L3_assemblyF.md:40-56` checks every new requirement: choose
0<b<beta(eta,A), also b<1/2-h under (N-D); polylogarithmic size implies
(L-size^b), (N) implies (W), and BM-infinity or (BM-Q) implies (BM-W).
The unchanged hypotheses and feasibility are retained. This covers any further
RM-F example, not just the following named classes.

* Exact-Gram AR(1): p<=n-1, fixed 0<|r|<1, fixed nonzero coefficients and
  sum_{k!=j}|theta_k| |r|^{|j-k|} <= |theta_j|(1-r^2)/(2(1+r^2)).
  GROW `STATEMENT.md:119-126` and RM `lemmas/L7_examples.md:50-56` verify the
  complete list, with Q the logarithmic truth neighbourhood (enlarged for
  feasibility). Exact direction counting gives (N-D)(i); q=O(log n) gives
  BM-Q. The source verifies the block conditions for every partition, hence
  the partition-free hypotheses.
* Exact-Gram orthogonal groups, uniformly bounded group sizes and spectral
  floor, at most one truth per group, BM-infinity and bounded energy.
  RM `lemmas/L7_examples.md:58-70` verifies the entire list: global floor
  gives T1 and FL; orthogonal groups give V and eta=0 outside the truth groups;
  feasibility enlargement keeps Q bounded, so (N-chi) applies.
* Fixed-p S5 population Gram and its stated diagnostic coefficients, with
  the coded partition: GROW `STATEMENT.md:127-137`, RM
  `lemmas/L7_examples.md:74-77`. This is only the block-relative example;
  the rational visibility certificate is not a partition-free certificate.
  Q=[p], leakage is vacuous, size bounded, (N-chi) and the other floors/T1 hold.
  For fixed p enumeration eventually supplies the output mechanism.

For R the complete inherited list is (T1-R),(FL-R),(V-R),(L-R),(D-R).
Containment (C4), RM2 `STATEMENT.md:220` (taken as given for R), supplies
(L-R^b) with any sufficiently small fixed positive b,rho satisfying
15rho+b<1/2, and (W-R); feasibility is unchanged.

* UNI-0: Gaussian rows, unit-diagonal Sigma in LOC(C0,d0,c,C,K,a), that is
  spectrum [c,C], exponential decay of covariance or precision along a
  pseudometric with ball size <=C0(1+r)^d0; fixed sparse bounded signals and
  PTV(a0). Definition and theorem: UNI `STATEMENT.md:50-57`, `:103-110`.
  RM `lemmas/L7_examples.md:10-30` verifies every inherited condition,
  including the exact radius/enlargement, O((log n)^d0) sizes, leak O(n^-1/2),
  localisation O(n^-2), and the population reference conditions. It includes
  banded/AR, separated Euclidean sites, polynomial-growth graphs and bounded
  blocks. The PTV/separation qualifications in that source are retained.
* LOC-BF: independent groups, each either bounded size with floor c, or
  one-factor with b_v in {0} union [b_lo,b_bar], 0<b_lo<=b_bar<1, group size
  <=(log n)^kappa; at most one truth per group. LOC2 `STATEMENT.md:76-85` and
  RM `lemmas/L7_examples.md:32-44` verify the entire inherited list. The floor
  is c_B=min(c,1-b_bar^2), PTV(c_B theta_lo) is automatic, Q is the truth
  groups with the stated enlargement, H_l includes G(l) and the truth groups;
  both leakage covariances are zero. The lattice condition is supplied by
  latent-factor frames directly, not by a claim that (D-loc) holds.

All signal, geometry and group restrictions in these citations are part of
the examples. No polynomial extension of LOC-BF is inferred by containment.

## E2. Gaussian rows with polynomial covariance decay on a line

Status: PROVED (by this seat, unchecked), conditional on RM2-R as given.

**Class.** Rows iid N(m_n,Sigma_n), independent of Gaussian response noise,
Sigma as in §0; s0>=1 fixed, p<=n^A, A>=1 fixed, fixed standardized signals
with 0<theta_lo<=|theta_j|<=theta_hi, and PTV(a0) as in APP
`lemmas/L3_LOC.md:28`. Assume alpha>2. Support locations may depend on n.
No truth-separation condition beyond the explicitly assumed PTV is needed.

**Leak set and its size.** Put gamma=1/(2alpha),

    R_Q = ceil(n^gamma (log n)^(-gamma/2)),
    Q0 = {k:d(k,S0)<=R_Q},
    Q = Q0 if p>=2|Q0|+32s0+1, and Q=[p] otherwise.

The enlargement is necessary for a general p sequence. If it occurs, no
outside-Q leakage/localisation condition remains. Injection into Z gives

    |Q0| <= min(p,s0(2R_Q+1)),
    |Q| <= max(s0(2R_Q+1),2s0(2R_Q+1)+32s0)
         <= 4s0 R_Q+34s0.                                    (2.1)

The actual cardinality is the number of occupied integer sites in the union
of the truth intervals; no universal exact equality follows from an envelope
or an injection. On a densely occupied line with disjoint untruncated truth
intervals, |Q0|=s0(2R_Q+1). Thus the generic order of this chosen envelope is
n^gamma/(log n)^(gamma/2), not a universally necessary model size.

For every fixed b in [gamma,1/2), (2.1) is <=n^b eventually. In particular
"any b>1/(2alpha)" is correct and not optimal at equality: the displayed
logarithmic saving permits b=gamma too. BC gives, outside Q,

    ell_n=K_15(1+R_Q)^(-alpha)
          <= K_15 n^(-1/2) (log n)^(1/4),
    ell_n sqrt(n/log n) <= K_15 (log n)^(-1/4) -> 0.           (2.2)

For a simpler pure-power construction one can take R_Q=ceil(n^t),
gamma<t<b, obtaining ell_n=O(n^(-alpha t)) and |Q|=O(n^t)<=n^b.
With a chosen radius of exponent t<gamma, the BC bound alone does not meet
the leak requirement. This is a limitation of this envelope verification,
not a necessary lower bound for every covariance satisfying the envelope
(the identity is an immediate exception). The leakage/size budget alone
admits some b<1/2 whenever alpha>1.

**All remaining RM2-R hypotheses.**

* (T1-R): the global floor implies the LSF sparse floors with phi^2=psi_n=c;
  psi_n sqrt(n)/(log n)^(3/2)->infinity. See RM `STATEMENT.md:129-133`, APP
  `lemmas/L1_POST.md:20-30`. Fixed signal bounds and independent Gaussian
  noise are in the class; energy is <=s0^2 theta_hi^2 n after standardization.
* (FL-R): every principal population matrix, including Q union {l} and sets
  of size <=16+s0, has floor c by Rayleigh/interlacing.
* (V-R): exactly the PTV(a0) assumption. It is not deduced from decay alone;
  cancellations with multiple truths would invalidate such a deduction.
* (L-size^b): (2.1), for gamma<=b<1/2. (L-feas): q=o(n); in the first branch
  p>=2q+32s0+1 and floor(n/2)>=2q+32s0+1 eventually. In the enlarged branch
  p<=2|Q0|+32s0=o(n), so K=p and Q=[p]. Both branches give q<=K.
* (L-gain-R): (2.2) is uniform over every conditioning U of size <=15,
  not merely U intersect H_l, by BC.
* (L-loc-R): choose r0=ceil(log n) and
  H_l={k:d(k,{l} union S0)<=r0}. Then H_l contains {l} union S0 and
  |H_l|<=(s0+1)(2r0+1). For v outside H_l, both d(v,l) and d(v,j) for
  j in S0 exceed r0. BC applied to U0=U intersect H_l gives both required
  covariances <=r_n:=K_15(1+r0)^(-alpha)->0. Choose, for example,
  rho=(1/2-b)/30>0: then |H_l|<=n^rho eventually and
  15rho+b=1/4+b/2<1/2. No power rate for r_n is required in v1.4.
* (W-R), through (D-loc^b): use §0, with B=Sigma and
  N_l=Q intersect {v!=l:d(l,v)<=floor(sqrt(log n))}. Equations (0.1)-(0.2)
  verify the coefficient difference, variance ratio eta_n=L(r)^2/c->0,
  |N_l|=o(log n), and L(r)^2 log(q+1)=o(log n). The references are the
  population residuals W_l-W_A beta_A(l), A subset N_l, one deterministic
  frame per (l,A); atoms are the coordinates W_v, v in Q, each of variance
  one. No extra latent coordinates are needed, so the deterministic
  Gaussian-extension contract is met by the original row law independent
  of noise. There are <=p 2^(2r)=p n^o(1) frames. This is (D-loc^b), hence
  (D-R^b) and (W-R) by the stipulated implication. As a check on its spectral
  event, uniform sample entry error O_P(sqrt(log n/n)) gives operator error
  <=(q+1)O_P(sqrt(log n/n))=o_P(1) for every Q union {l}; hence their sample
  floors are >=c/2 with probability tending to one. This entrywise event
  uses Gaussian rows and polynomial p only (APP `lemmas/L1_POST.md:43-50`).

Thus all hypotheses of RM2-R are verified for alpha>2. This is the smallest
cutoff established using the available BC/IR route: alpha>1 suffices for the
leak-size budgets, but IR's summable regression bound requires alpha>2.
No impossibility is asserted at or below 2.

**Old-cutoff ledger.** POLY:233-242 required rho>1/(4alpha) to make the old
selection-removal error vanish; POLY:264-271 exhibits its terms
n^(1/2-2alpha rho) sqrt(log n) and n^(1-4alpha rho). Counting up to 15 local
conditioning variables and excluding junk from a polynomial-size start then
required 15rho+b<1/2 with b=1/(2alpha) (POLY:10-13, :329-339). Thus
15/(4alpha)+1/(2alpha)<1/2, or alpha>17/2. The v1.4 hypotheses require the
full-U leak bound (BC supplies it) and only r_n->0. A logarithmic H_l now
works for arbitrarily small positive rho; the old lower bound on rho and its
17/2 consequence are not needed. The distinct regression-tail requirement
alpha>2 remains.

## E3. Exact-Gram polynomial decay on a line

Status: PROVED (by this seat, unchecked), conditional on RM2-F.

**Class and signals.** X is centred with X'X/(n-1)=G exactly, p<n, G as in
§0 with pi(j)=j, alpha>2, and constants c,C,K_dec. Such an X exists since
rank(G)=p<=n-1. Fix s0 and nonzero coefficients with
0<theta_lo<=|theta_j|<=theta_hi. Impose the following explicit sufficient
truth-separation condition, with the BC constant of §0:

    K_15 sum_{k in S0\{j}} |theta_k|(1+|j-k|)^(-alpha)
         <= c |theta_j|/2,  for every j in S0.                 (3.1)

This is automatic for s0=1, and can be met by sufficiently separated truths
for any fixed signal bounds. Signals of either sign are allowed.
Let B_theta=sum_{S0}|theta_j|<=s0 theta_hi.

Take Q0, Q and R_Q exactly as in E2. For b in [gamma,1/2), choose a fixed
eta>0 sufficiently small that

    eta<eta_A and b < beta(eta,A)=1/2-eta/2-sqrt(2A eta).

Existence follows from b<1/2 and continuity at zero. One may use A=1 here.

* (T1-F): GROW `STATEMENT.md:84-88` is the full H0 list. Fixed s0, p<=n^A
  and s0<=K hold. Energy is <=C s0 theta_hi^2 n, so choose
  M=C s0 theta_hi^2+1. Take phi0^2=c (unit diagonal ensures c<=1).
  The global floor gives the anchored SE_lambda(j0) for the exact
  j0=ceil((2A+1)s0)+1 and every larger set as well. It gives SE_w(m_sharp;g0)
  for any fixed g0>0 once (n-1)c>=g0, irrespective of m_sharp. Finally
  theta_lo^2 nc/(sigma^2 log n)->infinity proves BM-infinity.
* (FL-16),(FL-Q): all principal Grams have floor c.
* (V): in the G-inner product, for every |U|<=15 excluding j,
  |Cov_G(j,signal|U)| >= |theta_j| c
     - K_15 sum_{k!=j}|theta_k|(1+|j-k|)^(-alpha)
     >= c theta_lo/2.
  Terms indexed by k in U vanish. Since Var_G(j|U)<=1,
  delta_{U,j}^2>=(n-1)c^2 theta_lo^2/4. Take
  M_n=(n-1)c^2 theta_lo^2/(4 log n)->infinity.
* (L-size^b),(L-feas): the proof of (2.1) and E2's feasibility argument
  apply verbatim. Enlargement does not damage any other hypothesis.
* (L-gain): for l outside Q, BC and Var_G(l|U)>=c give

      delta_{U,l}^2 <= (n-1) B_theta^2 K_15^2
                             (1+R_Q)^(-2alpha)/c
                     <= (B_theta^2 K_15^2/c) sqrt(log n).

  Since tau_U^2>=sigma^2, this is <=eta tau_U^2 log n eventually. For example
  it suffices that sqrt(log n)>=B_theta^2 K_15^2/(c eta sigma^2).
  Thus a fixed, arbitrarily small positive eta works; exact eta=0 is not
  asserted for a nonzero decay tail. Alternatively, radius
  ceil(D(n/log n)^gamma) gives leak level <=B_theta^2 K_15^2/(c sigma^2 D^(2alpha));
  choose D to make this <=eta and take b>gamma to absorb its size constants.
* (BM-W): theta_lo^2 nc/[sigma^2(q+log n)]->infinity, since q<=n^b, b<1.
  This proves BM-Q, hence BM-W by RM2 `lemmas/L2_width.md:187-192`.
* (W) through (W-loc): apply (0.1)-(0.2) to G. Use the same N_l and r as
  in §0, any fixed h in (0,1/2-b), L_n=(1+JD)F(r)->0, and
  eta_n=L_n^2/c. These meet the exact two inequalities and entropy/atom
  budgets in RM2 §3.1, so (W-loc) implies (W) by RM2
  `lemmas/L2_width.md:123-180`.

Every hypothesis of (C1) is now verified. The cutoff furnished by these
lemmas is alpha>2, again because of IR, not because of a leak-size obstruction.

## E4. One truth and polynomially many weak proxies

Status: PROVED (by this seat, unchecked).

Fix 0<b<1/2, C0>0 finite, sigma^2>0 and theta=theta_1!=0 fixed. Let
p=floor(n/3), q=floor(n^b), r^2=C0 log n/n, and take centred orthonormal
e_1,...,e_p. For sufficiently large n, 0<r<1 and q<=p. Use exactly

    z_1=e_1,
    z_j=r e_1+sqrt(1-r^2)e_j  (2<=j<=q),
    z_j=e_j                  (j>q),
    x_j=sqrt(n-1) z_j,  Q={1,...,q}, S0={1}.

The proxy-proxy correlations are r^2, not zero. With m=q-1 the Gram on Q is

    G_Q = [1, r 1_m'; r 1_m, (1-r^2) I_m+r^2 1_m1_m'].

Its distance from identity in operator norm is at most

    epsilon_n=|r|sqrt(m)+r^2(m+1) ->0.

The other columns are an orthogonal identity block. Hence the full Gram has
floor >=1/2 eventually; this proves (FL-16) and (FL-Q) with phi0^2=1/2.
The same global floor verifies every anchored and weak SE in T1-F with,
for example, A=1, g0=1; M=theta^2+1 bounds energy. BM-infinity follows from
fixed |theta|>0. These are exactly all H0 clauses (GROW `STATEMENT.md:84-88`).
There is no asymptotic lower threshold on |theta| and no upper or lower
threshold on the fixed positive C0 beyond finiteness and positivity.

For any U excluding 1, the other outside-Q columns are orthogonal and at
most 15 proxies can be in U. With t such proxies, direct Schur complementation
of their equicorrelated Gram gives

    Var_G(1|U)=(1-r^2)/(1+(t-1)r^2),

with value 1 at t=0. It is >=1/2 eventually (also follows from the global
floor). Thus delta_{U,1}^2=theta^2(n-1)Var_G(1|U)
>=theta^2(n-1)/2; take M_n=theta^2(n-1)/(2 log n) for (V).

(L-size^b) holds exactly by q=floor(n^b); K=p and p>=2q+33 eventually,
proving (L-feas). For every l>q, x_l is orthogonal to the whole remaining
Gram, so its projection on every U excluding l is zero and
u_{U,l}'mu=0: (L-gain) has eta=0, and b<beta(0,1)=1/2.
BM-Q holds since theta^2 n/[2sigma^2(q+log n)]->infinity, hence BM-W.

Finally verify the exact definition of (W-loc). Put N_l={1} for 2<=l<=q,
and N_l=empty for l=1 or l>q. Every lattice T contains 1. For a proxy
l outside T, z_l-r z_1=sqrt(1-r^2)e_l is orthogonal to all of X_T,
including the other proxies. Therefore beta_{T,l} has coefficient r at 1
and zero elsewhere, exactly the regression on T intersect N_l={1}.
For l>q both regressions are zero. There are no lattice pairs with l=1.
Thus both (W-loc) inequalities hold with L_n=eta_n=0 and nu_n=1.
Choose any h in (0,1/2-b); nu_n log 2<=h log n eventually. This proves (W),
and hence verifies every (C1) hypothesis at genuine polynomial |Q|.

## E5. A positive equicorrelation group: direct width verification

Status: PROVED (by this seat, unchecked), for the explicit range below.
The larger candidate range is not asserted.

Fix 0<b<3/10, 0<a<1, theta!=0, sigma^2>0, all constant. Let
p=floor(n/3), q=floor(n^b), Q={1,...,q}, S0={1}. Choose centred orthonormal
e_0,e_1,...,e_p (p+1<=n-1 eventually), and set

    z_j=sqrt(a)e_0+sqrt(1-a)e_j  (j<=q),
    z_j=e_j                    (j>q),
    X=sqrt(n-1)[z_1 ... z_p], mu=theta x_1.

Thus the group has off-diagonal correlation a; the remainder is an independent
orthogonal block. Every principal Gram has floor c=1-a. The growing upper
eigenvalue 1+(q-1)a causes no problem: no bounded global upper spectrum is
assumed by (C1), and energy is exactly (n-1)theta^2.

**Hypotheses other than W.** T1-F: H0 holds with A=1, phi0^2=c,
M=theta^2+1 and g0=1, since global floor c gives both SE conditions for all
sizes and fixed theta gives BM-infinity. This also proves FL-16 and FL-Q.
For every |U|<=15 excluding the truth, Var_G(1|U)>=c and

    delta_{U,1}^2=theta^2(n-1)Var_G(1|U)>=theta^2(n-1)c;

so V holds with M_n=theta^2(n-1)c/log n. All outside-Q columns are orthogonal
to the group and one another, so L-gain holds uniformly with eta=0.
L-size^b holds by the floor definition; K=p>=2q+33 eventually, proving
L-feas. BM-Q, and hence BM-W, follows from
 theta^2 nc/[sigma^2(q+log n)]->infinity. No coefficient magnitude restriction
beyond fixed theta!=0 is needed.

**Direct width bound.** Write g_i=e_i'g, independent standard normals. For
l<=q outside a lattice T, put t=|T|>=1. The regression coefficients on T
are all A_t=a/(1-a+ta), so 0<=t A_t<=1. Its unnormalised residual is

    sqrt(a)(1-t A_t)e_0
       +sqrt(1-a)(e_l-A_t sum_{j in T}e_j).

Its squared norm is v_t=(1-a)[1+a/(1-a+ta)]>=1-a. Division by sqrt(v_t)
therefore yields, simultaneously for all these pairs,

    |u_{T,l}'g| <= 2 max_{j<=q}|g_j| + sqrt(a/(1-a)) |g_0|.  (5.1)

Let U be the maximum of the left side for within-group pairs, and V the
maximum for outside-Q pairs. Outside directions are exactly e_l, hence

    E U <= 2 sqrt(2 log(2q)) + sqrt(a/(1-a)) sqrt(2/pi),
    E V <= sqrt(2 log(2(p-q))).

For all sufficiently large n both families are nonempty. Each of U,V is
1-Lipschitz as a maximum of absolute unit Gaussian projections. The Gaussian
upper-tail bound and integration give

    E max(U,V) <= max(EU,EV) + C_G,
    C_G = integral_0^infinity min(1,2 exp(-t^2/2)) dt < infinity.

This last constant follows by the union bound on U-EU and V-EV; independence
of U and V is not required. Consequently

    E max_P |u_{T,l}'g|
       <= max(sqrt(8b log n)+O_a(1), sqrt(2 log n)+O(1)).       (5.2)

Choose a fixed delta>0 so small that

    2delta < min(1-2b, 3-10b).

Since log p=log n-log 3+o(1), (5.2) is strictly below
sqrt(2 log p+(1-2b-2delta)log n) eventually, with a positive multiple of
sqrt(log n) to spare. This is exactly (W-unif) with
0<delta<(1-2b)/2; thus W follows by RM2 `lemmas/L2_width.md:123-140`.
Equivalently the unshifted width is bounded above by

    [max(sqrt(8b),sqrt(2))-sqrt(3-2b)] sqrt(log n)+O_a(1),

which tends to minus infinity for b<3/10. The size-dependent level has been
minimised at k=q (outside-group pairs allow T=Q, since q<K); its squared value is
log(n+1)+2log(p/(q+1))=(3-2b)log n+O(1).

This verifies every C1 hypothesis on a nonempty range of fixed positive
correlations. It does not verify the heuristic 8b<2A+1 range: that comparison
omits the -2b contribution from the model-size penalty. For b>=3/10 this
particular upper bound ceases to prove W; that is neither a converse nor
an assertion that another sufficient form or a sharper computation fails.

## Examples table

| class | theorem | conditions | cutoff | status |
|---|---|---|---|---|
| Every inherited RM-F example | RM2-F | Complete RM-F hypotheses, including the appropriate signal and partition qualifications; containment E1 | Original class restrictions | PROVED (by this seat, unchecked) |
| UNI-0 metric-local rows | RM2-R | Polynomial metric growth, covariance or precision exponential locality, spectral bounds, fixed signals, PTV | No polynomial-decay cutoff | PROVED (by this seat, unchecked) |
| LOC-BF independent groups | RM2-R | Bounded or polylogarithmic one-factor groups, stated loading bounds, at most one truth per group | Original polylogarithmic size | PROVED (by this seat, unchecked) |
| Polynomial-decay Gaussian covariance on a line | RM2-R | Global spectrum [c,C], unit diagonal, fixed signals, PTV; gamma<=b<1/2; rho=(1/2-b)/30 | alpha>2 using available IR | PROVED (by this seat, unchecked) |
| Exact-Gram polynomial decay on a line | RM2-F | p<n, spectrum [c,C], fixed bounded nonzero signals, separation (3.1); gamma<=b<1/2 and sufficiently small eta>0 | alpha>2 using available IR | PROVED (by this seat, unchecked) |
| One truth, weak proxies | RM2-F | p=floor(n/3), q=floor(n^b), fixed C0>0, r^2=C0 log n/n, fixed nonzero truth | 0<b<1/2 | PROVED (by this seat, unchecked) |
| One equicorrelated truth group | RM2-F | Independent orthogonal remainder, p=floor(n/3), q=floor(n^b), fixed 0<a<1 and nonzero truth | 0<b<3/10 | PROVED (by this seat, unchecked) |
| Same equicorrelated construction beyond displayed range | RM2-F candidate | Other C1 hypotheses remain verified for b<1/2 | 3/10<=b<1/2 | NOT VERIFIED: direct bound (5.2) has no strict width margin |

## Sources and statuses (copied without upgrading)

Only the assigned brief in reviews was read; no other reviews, logs or
checkpoints were consulted. References to checks below are status text in
allowed source files, not additional review inputs.

* RM2 `STATEMENT.md:4`: "v1.3 (target statement — nothing in it is proved yet)".
  Its §3.2 explicitly contains the v1.4 clauses used here; C2, C4(R) and
  D-loc^b implications are stipulated inputs of this seat's brief. Its §5,
  `:276-282`, records the downstream conditional inputs verbatim:
  "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY";
  W2-APP:POST "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied";
  W3-RM:B9 "PROVED (by this seat, unchecked)". The examples inherit those
  conditions through their respective theorem, not an upgraded posterior claim.
* RM2 `lemmas/L2_width.md:3`: "PROVED (by this seat, unchecked)";
  `:4-5`: "Lemma 0, NA-conv, NA-W, sufficient forms (i)–(v), Lemma d, TL-W VERIFIED";
  "W-conv (+ corollary) VERIFIED-WITH-AMENDMENTS". Used only for the width
  implications and BM-Q => BM-W with their exact polynomial-size budgets.
* RM2 `lemmas/L3_assemblyF.md:3`: "PROVED (by this seat, unchecked)";
  `:4-5`: "Theorem RM2-F (assembly) VERIFIED, containment of RM-F VERIFIED".
* POLY:3: "PROVED (by this seat, unchecked)"; POLY:78 and :118 each say
  "PROVED (by this seat, unchecked)" for BC and IR. POLY:5 and :8:
  "VERIFIED-WITH-AMENDMENTS". Only BC and IR and the old-cutoff ledger are
  used; the old Thm-Poly is not invoked at alpha<=17/2.
* RM `lemmas/L7_examples.md:3`: "PROVED (by this seat, unchecked)";
  `:4-5`: "WRONG as first written (4 MAJOR — one missing hypothesis in (E-F2) and three overstated rows of table 7.3 — and 2 MINOR), all corrected here [R06-#]".
  Its exact example verifications and qualifications are retained.
* RM `STATEMENT.md:251-255`: GROW "PROVED-CHECKED";
  W2-LOC2 "PROVED-CHECKED" with lemma statuses "PROVED (by this seat, unchecked)";
  W2-UNI UNI-0 and R1–R5 "PROVED-CHECKED"; W2-APP "PROVED-CHECKED".
  These enclosing ticket labels do not upgrade individual lemma statuses.
* GROW `STATEMENT.md:4`: "v2.5 — final; council round 1 passed (R09 9.2, R10 9.0)".
  Used for H0, exact-Gram AR(1) and the qualified S5 illustration.
* UNI `STATEMENT.md:3`: "v1.1.4 — LOCKED". Used for the precise LOC class
  and UNI-0 statement, with the theorem status quoted separately above.
* LOC2 `STATEMENT.md:3`: "v1.2"; `:97-98`:
  "L6 PROVED (by this seat, unchecked); checks R06a (Opus high) and R06b (Sol xhigh) VERIFIED-WITH-AMENDMENTS, applied".
  Used for the precise LOC-BF class and the old polynomial result's scope.
* APP `lemmas/L1_POST.md:3-5`: "PROVED (by this seat, unchecked)";
  "VERIFIED-WITH-AMENDMENTS (1 MAJOR, 2 MINOR on remarks/raw-scale wording), all applied".
  Used for LSF and the Gaussian entrywise concentration event only.
* APP `lemmas/L3_LOC.md:3`: "PROVED (by this seat, unchecked)";
  `:7-9`: "Theorem LOC VERIFIED-WITH-AMENDMENTS";
  "LOC-B VERIFIED-WITH-AMENDMENTS as stated here".
  Used for the precise PTV definition; no LOC theorem is extrapolated.

## Adversarial self-check

* E1: tried removing BM-infinity/bounded energy from the orthogonal-group
  example and promoting the S5 within-block certificate to all U. Both
  invalidate the cited verification; both restrictions are explicitly kept.
  LOC-BF's direct latent references are not replaced by an unsupported D-loc
  assertion. Containment permits polynomial bounds, not polynomial groups.
* E2: tried setting b=gamma with an untracked constant times n^gamma,
  ignoring feasibility when p is small, and using only a local-U leak bound.
  The logarithmic saving, explicit enlargement and BC for every |U|<=15
  close these issues. Injection gaps prevent an asserted exact cardinality.
  The gamma endpoint is sufficient, not a necessary size for every matrix.
  At alpha=2 IR is unavailable and its displayed tail series diverges;
  no endpoint improvement is claimed. PTV remains an assumption.
* E2/E3 localisation: tried truncating beta_T without refitting beta_A.
  Equation (0.1) explicitly bounds the refitting error using uniform inverse
  and covariance column sums. r=log n would not meet the R entropy condition
  o(log n), so the regression radius is sqrt(log n); H_l's separate log n
  radius is harmless. The variance-ratio inequality uses projection
  orthogonality rather than an unproved continuity claim.
* E3: tried cancellation of opposite-sign truths and exact eta=0 for a
  nonzero covariance tail. Separation (3.1) blocks the first, and the theorem
  uses fixed eta>0 with b<beta(eta,A). All H0 spectral sets are covered by
  the global exact-Gram floor; no sparse-floor or coefficient clause is omitted.
* E4: treating proxies as mutually orthogonal would be false. The displayed
  Gram includes r^2 off-diagonal entries; conditioning on the truth makes
  the proxy innovations orthogonal, which is the actual reason L_n=0.
  Also checked truth removal after fitting many proxies: the global floor
  tends to one since q r^2 and r sqrt(q) vanish. Fixed C0 and theta have no
  additional asymptotic threshold.
* E5: tried using a union bound over exponentially many subsets and using
  log(n)+2log p in place of the size-dependent level. The first loses the
  theorem, the second overstates the range. Formula (5.1) handles all subsets
  simultaneously; the correct minimum level is (3-2b)log n. The expectation
  of a maximum is not replaced by the maximum of expectations without a
  correction: Gaussian concentration supplies the finite C_G. No inference
  is made for b>=3/10 from failure of this sufficient upper bound.

