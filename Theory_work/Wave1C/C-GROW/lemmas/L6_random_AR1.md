# L6 — iid-row AR(1), including p much larger than n

Status of every new result below: **PROVED (by this seat, unchecked)** (author: parallel prover, Codex gpt-6.1-sol).
Check record: R07 (fresh Codex gpt-6.1-sol xhigh, reviews/R07_L6_check_sol.md): VERIFIED, no amendments; R06 (Claude
Opus 5.5 high, cross-family to the author, reviews/R06_L6_check_opus.md): VERIFIED-WITH-AMENDMENTS (A1–A9,
presentation/records only), applied below (marked [A#]). Incorporated by the lead as STATEMENT v2.3 claim (C5)(c), an
extension of the locked target (logged); full-ticket sweep (R08) done, council pending. No input status is upgraded.
Seat: research parallel prover, 2026-11-08/09. No numerical evidence is used.

## 0. Statement, inputs, and scope

Let the rows of the raw n by p matrix W be independent N(0,Sigma),
Sigma_ij = rho^{|i-j|}, with fixed 0 < |rho| < 1, and p <= n^A for a fixed A >= 1.
Write N=n-1, C=I-11'/n, t_j=||CW_j||/sqrt(N), and X_j=CW_j/t_j.
Let Y=X theta + C eps, eps independent N(0,sigma^2 I), with fixed sigma>0,
fixed support size s0>=1 and fixed nonzero standardized coefficients theta on that support.
Support positions may vary deterministically with n. Assume the separation inequality

    sum_{k in S0, k != j} |theta_k| |rho|^{|j-k|}
      <= (|theta_j|/2) (1-rho^2)/(1+rho^2),   j in S0.             (6.0)

The bounded block size is 16; the blocks can be ANY X-measurable partition with
that bound. In particular the actual coded partition is allowed.
The response is subsequently standardized inside the shipped score, as in L0.

Put r=|rho|, c_-=(1-r)/(1+r), c_+=1/c_-,

    d_n=ceil(log n/(2 log(1/r))),
    Q=S0 union {l: dist(l,S0)<=d_n}.

If p < 2|Q|+32s0+1, replace Q by [p]. This is a deterministic enlargement;
in the enlargement case p=O(log n). Thus q=|Q|=O(log n), q<=K eventually,
and either Q=[p] or K>=2q+32s0+1. Let L={T:S0 subset T subset Q}.

**Theorem L6.1. PROVED (by this seat, unchecked), conditional on the named
inputs and method premises below.** Under these assumptions,

    P(S0 subset S_tilde subset Q for EVERY maximizer of gamma0) -> 1,
    P(NA(L)) -> 1,                    P(TL(L)) -> 1.             (6.1)

Consequently, with the implementation premises of C-GROW/STATEMENT section 1
and MR1, under the joint law of (X,eps),

    D_n -> 0,        P(O intersect {S^+ != S0}) -> 0,
    P(O intersect {S^+ = S0}) = 1-P(U_n)-o(1).                  (6.2)

Constants [A9]: A ≥ 1 enters C_A, the union-bound constants and the bound on m♯_n; n₀ depends only on
(ρ, A, s0, θ, σ). There is no delivery assertion. This does not assert the production LS0 cap
suffices. It does not assert fixed-realization NEG(eta) or exact (G4-dir).

Named inputs, with statuses retained:

* C-GROW L0 (score expansion and logarithmic-size toolkit) and L1 (deterministic
  descent): **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high): VERIFIED.
  L2.1–L2.2 (TL and maximal-Z reduction): R03 VERIFIED-WITH-AMENDMENTS (2), applied. L4 assembly:
  R04 VERIFIED-WITH-AMENDMENTS (1), applied. [A8] L0 invokes GEN L1, whose check
  record is **VERIFIED-WITH-AMENDMENTS**, applied. These remain inputs here.
* The population AR(1) facts P1–P4 in C-GROW L5(a), recorded there
  **PROVED (by this seat, unchecked)**; R04 VERIFIED-WITH-AMENDMENTS (2–7), applied [A8], are used: spectrum in [c_-,c_+],
  nearest-neighbor Gaussian regression, conditional variance bounded below,
  and |Cov(W_j,W_k | W_U)| <= r^{|j-k|}. The sign-flip reduction in that
  file permits negative rho. Only population facts, not exact sample Gram
  identities P5, are used here.
* [OP], GEN L5 operational closure, is recorded **PROVED (by this seat,
  unchecked)**, inside Theorem GEN **PROVED-CHECKED**. It uses GUARD-W,
  OP-LS0, e4, and the complete-scan premises; these are named implementation
  assumptions, not proved here.
* [S-T], T03-sharp: **PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)**.
  [M5-0], T38-(0): **PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED*
  (A-REV5))**. Their statements are as quoted in C-GROW L4.
* GEN L5.3, random-design de-randomisation, is recorded **PROVED (by this
  seat, unchecked)**, check record **VERIFIED-WITH-AMENDMENTS**, applied.
  Its diagonal-sequence argument is reproduced in section 7 where needed;
  GEN's bounded-certificate hypotheses are NOT claimed to hold here.

## 1. Common concentration and regularity

**Lemma L6.2. PROVED (by this seat, unchecked).** There are fixed constants
M,phi0>0,g0>0 and X-events A_X with probability tending to one such that
every deterministic sequence in A_X satisfies (H0), (G1), (G2), (G3a), and
(G3b) with common constants and deterministic BM/TV envelopes. Moreover a
joint event A_cov with probability tending to one has the uniform covariance
and partial-correlation properties used below.

*Proof.* Adjoin the independent noise column eps/sigma to W. An orthonormal
basis of 1-perp turns these centered columns into N independent Gaussian
rows with the same covariance, enlarged by an independent unit coordinate.
For a scalar standard Gaussian G, its squared-sum mgf is
E exp(t sum G_i^2)=(1-2t)^(-N/2). Chernoff, using
-log(1-u)-u <= u^2 for |u|<=1/2, gives

    P(|N^{-1} sum G_i^2-1|>h) <= 2 exp(-c N h^2), 0<h<1,

for an absolute c>0 (decreasing c covers both tails). Products are controlled
by polarization, ab=((a+b)^2-(a-b)^2)/4; the variances of sums and differences
of two unit-variance Gaussian coordinates are at most 4. A union bound over
at most (p+1)^2 entries, with ħ_n=C_A sqrt(log n/n) [A2: ħ_n, ϖ_n rename L6's former h_n, omega_n to avoid the L0/GEN-L1 symbols], therefore gives an event
of probability 1-o(1) on which every augmented sample covariance entry is
within ħ_n of its population value. C_A is a sufficiently large fixed
constant. This raw event includes max_j |t_j-1|=O(ħ_n);
standardizing columns preserves the entrywise O(ħ_n) error from Sigma.
Define A_X to be the event that this standardized Gram entrywise error
is at most a sufficiently large fixed multiple of ħ_n. Thus A_X is
measurable in the standardized X itself and has probability 1-o(1).
For A_cov retain the stronger augmented raw event, including the raw
column norm bounds and the independent noise column.

For any fixed C_m, EVERY standardized Gram submatrix of size at most
C_m log n has operator error at most C_m log n O(ħ_n)=o(1), since operator
norm is bounded by size times maximal entry. Population eigenvalues are in
[c_-,c_+], so the sample lower bound is c_-/2 for n large. This simultaneously
covers (G2), all blocks, and fixed-order anchored SE; no union over subsets
is needed after the entrywise event.

Here m_n^sharp=O(log n). Indeed for p>=2 and k<=p,

    binom(p,k)/binom(2p-1,k)
      = product_{i=0}^{k-1} (p-i)/(2p-1-i) <= (2/3)^k.

Thus R_m <= (2p)^{s0} sum_{k>m}(2/3)^k. A sufficiently large fixed multiple
of log n makes this <= n^{-(s0+2)/2}. If that multiple exceeds K, use m=K,
where the tail is zero; if p=1 the claim is immediate. The minimum defining
m_n^sharp is consequently O(log n). Taking C_m large enough proves SE_w
with g0=1 eventually. Choose phi0^2=c_-/2. Energy is bounded even without a
concentration event: ||mu|| <= sqrt(N) sum_{S0}|theta_j|. BM has deterministic
envelope theta_min^2 n phi0^2/(sigma^2 log n) -> infinity.

For TV, for every j in S0 and every U not containing j with |U|<=15,
the population residual covariance with sum theta_k W_k is, by P3/P4 and
(6.0), at least in absolute value

    a0=(theta_min/2)(1-r^2)/(1+r^2)>0.

All the corresponding empirical Schur complements are within O(ħ_n) of
their population versions, uniformly in (j,U): dimensions are bounded,
inverse norms are bounded by 2/c_-, and the formula
A^{-1}-B^{-1}=A^{-1}(B-A)B^{-1} bounds the inverse perturbation. This
calculation uses the standardized sample Gram and the FIXED coefficients
theta, exactly as required by the generator. The residual column variance
is at most 1. Hence delta_{U,j}^2 >= N a0^2/4 eventually. Set
M_n=N a0^2/(4 log n). This proves TV even for arbitrary selected blocks.

For later partial correlations involving Y, use raw centered columns and
write mu=C sum theta_j W_j/t_j [A1]. On the entrywise event these coefficients
are bounded and differ from theta by O(ħ_n). All fixed-dimensional sample
conditional covariances therefore differ by O(ħ_n) from the population
algebra using the same coefficients theta_j/t_j. This is a uniform algebraic
bound for all coefficient vectors in that bounded set; the coefficients
need not be independent of the sample. Population residual variance of Y
given any design subset is at least sigma^2. Conditional design variances
are at least c_-. All denominators stay uniformly positive, so the same
O(ħ_n) comparison holds for partial correlations on sets of bounded size.
This proves the claimed properties of A_cov. The G1 checks were given in
section 0. All constants depend only on fixed parameters, not positions or
selected blocks. QED.

We also use a common score event A_score [A3: A_score := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ of L0/[GEN-L1] for both families below,
with the L0 constants (D = 16A + O(1) for the first family); [GEN-L1] L1.2 and L1.4(b) hold on it], with P(A_score)->1, on which
L0.2(c) and its bounded remainder apply to ALL subsets of [p] of size <=16,
and the L2.0 toolkit applies to the lattice and its one-move neighbors.
For clarity this is an application of the named L0 input: conditional on
X in A_X, the first family has size <=17(p+1)^16 and the second has size
<=C p 2^q, all have the required Gram floors and energy bound. Their
constants and polynomial exponents are uniform in X. L0's conditional
Gaussian union bounds thus give a uniform o(1) failure bound. Conditioning
on X and integrating proves the assertion. This avoids conditioning on a
partition chosen using X when making a fixed-pair probabilistic assertion.

## 2. Removing the selection of conditioning sets

For all l outside Q define the deterministic neighborhood

    H_l={j: dist(j,{l} union S0)<=R_n},
    R_n=ceil(2 log n/log(1/r)).

It has O(log n) elements. Let I_l be all U0 subset H_l minus {l} with
|U0|<=15. Its cardinality is at most L_n=C(1+log n)^15 (enlarge C once).
Define for any U not containing l, |U|<=15,

    h_{U,l}=n (RSS_U-RSS_{U+l})/RSS_U
           =n Corr_sample(W_l,Y | W_U)^2.                       (6.3)

These expressions use Y before its final response scaling; the correlation
is invariant to that scaling and all column scalings. On the events used
here the residual variances are positive.

**Lemma L6.3. PROVED (by this seat, unchecked).** On A_cov, uniformly over
l outside Q and ALL U not containing l with |U|<=15,

    |h_{U,l}-h_{U intersect H_l,l}| <= ϖ_n,
    ϖ_n=C (log n)^{3/2}/sqrt(n) -> 0,
    h_{U,l} <= C log n.                                        (6.4)

*Proof.* Put U0=U intersect H_l, V=U minus U0. In the population,
conditional covariance of W_l with any W_v, v in V, given W_U0 is at most
r^{|l-v|}<=r^{R_n}<=n^{-2}. Likewise conditional covariance of Y with W_v
is at most C sum_{j in S0 minus U0}r^{|j-v|}<=C n^{-2}, using P4 and the
bounded coefficients theta_j/t_j. Noise has zero population covariance.
The population residual correlation of W_l and Y given U0 is at most
C r^{d_n}<=C n^{-1/2}: P4 applies for every truth not in U0, and residual
variances have fixed positive lower bounds.

Let a,b be the sample vectors of partial correlations of W_l and Y,
respectively, with W_V given U0, and R their sample conditional correlation
matrix. Lemma L6.2 gives ||a||+||b||<=C ħ_n, ||R^{-1}||<=C, uniformly.
The inverse bound follows also directly from Schur complements of the
bounded-size joint Gram. The exact recursive correlation formula is

    z_U=(z_0-a'R^{-1}b)/sqrt((1-a'R^{-1}a)(1-b'R^{-1}b)),

where z_0=Corr_sample(W_l,Y|U0). Thus |z_U-z_0|<=C ħ_n^2, and
|z_0|<=C(n^{-1/2}+ħ_n)<=C ħ_n. It follows that
n |z_U^2-z_0^2| <= C n ħ_n^3, which is (6.4). If V is empty the
identity is exact. No independence involving U or V was assumed: this is
a simultaneous algebraic consequence of the common entrywise event. QED.

This is the selection-uniform replacement for applying a fixed-pair tail
to the random blocks. Unlike the bounded independent-group SEL input,
the deterministic reference family here grows polylogarithmically.

## 3. Joint-law spherical tail for reference statistics

**Lemma L6.4. PROVED (by this seat, unchecked).** There are constants C,c>0
such that, uniformly in l outside Q, fixed U0 in I_l, and
log n/2 <= t <= (2A+3)log n,

    P(A_cov intersect {h_{U0,l}>=t})
       <= C exp(-t/2+C sqrt(log n)) + C exp(-c sqrt(n)).          (6.5)

Consequently, if

    J(t)=#{l outside Q: there exists U, |U|<=15, l notin U,
                       h_{U,l}>=t},

then, for a fixed constant C0 and
t_n(k)=log(n+1)+2log(p/k)-C0, 1<=k<=K,

    E[1_{A_cov} J(t_n(k))] <= k n^{-1/2+o(1)},                 (6.6)

uniformly in k. Also

    P(A_cov intersect {max_{l outside Q, |U|<=15}h_{U,l}
                             >2log p+(1/2)log n}) -> 0.        (6.7)

*Proof.* All index sets in this paragraph are deterministic. Let
D=U0 union S0 and regress the raw population coordinate W_l on W_D:

    W_l=W_U0 b + m_raw + e,
    m_raw=sum_{j in S0 minus U0} alpha_j
                (W_j-W_U0 b_j).

Here b is the population regression of W_l on U0, b_j that of W_j
on U0, and alpha is the regression on the truth residuals. P4 gives
each residual covariance with l absolute value <=r^{d_n}; the conditional
truth covariance has eigenvalues >=c_-, by the Schur complement lower
bound of Sigma. Hence ||alpha||<=C r^{d_n}. The coefficients b_j are
uniformly bounded since |U0|<=15 and its covariance floor is c_-.
On A_cov every raw centered column has norm at most 2sqrt(n), so

    m=(I-P_U0) C m_raw has ||m||<=C sqrt(n) r^{d_n}<=C.          (6.8)

The innovation e is independent of W_D, has independent N(0,tau^2)
entries, and c_-<=tau^2<=1. Conditional on W_D and eps, the residual
r_Y=(I-P_U0)Y is fixed: standardizing the TRUE columns uses only W_D.
In the subspace V=1-perp intersect span(CW_U0)-perp, of dimension
d=N-|U0|, the vector g=(I-P_U0)Ce is isotropic Gaussian with variance
tau^2. Except on an event of conditional probability exp(-c n),
||g||>=c sqrt(n). On that event and the column norm event in (6.8),

    sqrt(h_{U0,l})
      <= (1+C/sqrt(n)) sqrt(n) |(g/||g||)' (r_Y/||r_Y||)| + C. (6.9)

This follows from ||g+m||>=||g||-||m|| and Cauchy–Schwarz for m.
Zero residual Y has probability zero; alternatively define its statistic
as zero, which cannot enlarge the upper tail.

For any fixed unit v in V, write g/tau as a standard d-dimensional Gaussian
G. Its direction is uniform on the sphere and
sqrt(n)|(g/||g||)'v|=sqrt(n)|G'v|/||G||. The chi-square mgf bound of
section 1 gives

    P(||G||<sqrt(d)(1-n^{-1/4})) <= C exp(-c sqrt(n)).

On the complement, a tail at z requires
|G'v| >= z sqrt(d/n)(1-n^{-1/4}); the normal Chernoff bound is
2exp(-z^2(d/n)(1-n^{-1/4})^2/2). Here d/n=1-O(1/n), uniformly.
Combining with (6.9) and integrating the conditioning gives (6.5), since
(sqrt(t)-C)^2=t-O(sqrt(log n)) on the specified range. A_cov implies
the column norm event, so restricting to A_cov is harmless even though
it also depends on e. We never claim a conditional sphere law AFTER
conditioning on A_cov. Explicitly [A4]: let CN_D be the W_D-measurable event that the raw centred columns
of W_D have norms ≤ 2√n (A_cov ⊆ CN_D). Then P(A_cov ∩ {h ≥ t}) ≤ P(CN_D ∩ {h ≥ t}) =
E[1_{CN_D} P(h ≥ t | W_D, ε)], and the inner conditional probability is bounded by the sphere tail plus the
probability of {‖g‖ < c√n}; the term C exp(−c√n) in (6.5) also absorbs that exp(−cn) term [A6].

By L6.3, on A_cov, J(t) is bounded by
sum_{l outside Q} sum_{U0 in I_l}1{h_{U0,l}>=t-ϖ_n}.
Equations (6.4)–(6.5) [A5], L_n=exp(O(log log n)), and

    p exp(-t_n(k)/2) <= C k n^{-1/2}

prove (6.6). The p L_n exp(-c sqrt(n)) term is uniformly negligible
relative to k n^{-1/2}; k>=1 and p<=n^A. A union bound at
t=2log p+(1/2)log n proves (6.7): the upper bound is
n^{-1/4+o(1)}. All thresholds used fall within the stated range after
an o(1) adjustment. QED.

The tail concerns the ENTIRE add statistic normalized by RSS_U/n. It
does not replace delta^2 by a small design-conditional upper bound.

## 4. Sandwich, including the global size ladder

**Lemma L6.5. PROVED (by this seat, unchecked).** The first event in (6.1)
has probability tending to one.

*Proof.* On A_cov intersect A_score, for any l outside Q, |U|<=15,
the table increment obeys, uniformly,

    log m(U+l)-log m(U)
       <= -(1/2)log(n+1)+(1/2)h_{U,l}+2 kappa_E+o(1).           (6.10)

Indeed RSS_{U+l}/RSS_U=1-h_{U,l}/n by definition. Since h=O(log n)
by L6.3,
nu[-log(1-h/n)]=h/2+O((h+h^2)/n)=h/2+o(1).
L0.2(c) gives the remainder 2 kappa_E, for the score actually used.
This sharp normalization is why an RSS lower bound by sigma^2 n alone
is not used for the far-null likelihood term.

Fix ANY maximizer S_tilde, k=|S_tilde|, U_b=S_tilde intersect C_b.
Call a block good if S0 intersect C_b subset U_b. There are at most s0
bad blocks, regardless of how the partition was selected. In a good
block let N_b=U_b minus Q. With k0=q+16s0,

    k <= k0+16 #{good b:N_b nonempty}.                          (6.11)

For nonempty N_b, removing it is feasible. By per-block optimality of a maximizer (L3 (3.1)) [A7], the exact
prior ratio gives

    log m(U_b)-log m(U_b minus N_b) >= |N_b| log(p/k),

because each factor w(j-1)/w(j)=(2p-j)/j>=p/k for j<=k<=p.
Add N_b back in any order. Every add is a far null with preceding
conditioning set of size <=15; the sum of (6.10) bounds the left side.
Thus at least one of these additions has

    h_{U,l} >= log(n+1)+2log(p/k)-4 kappa_E-o(1).

Choose C0=4 kappa_E+2 in L6.4. Distinct blocks supply distinct l, so
the count of such blocks is at most J(t_n(k)). This bound holds
simultaneously for all maximizers, without a union over maximizers.

For the size ladder put m_i=2^{i+1}k0. If k>2k0, choose i>=0 with
m_i<k<=2m_i; at most O(log n) such i are needed because K<=n/2.
Equation (6.11) implies J(t_n(k))>m_i/32. Since t_n is decreasing,
J(t_n(min(2m_i,K)))>=J(t_n(k)). Markov and (6.6) yield

    P(A_cov intersect A_score intersect
                  {some maximizing k>2k0})
      <= sum_{i:m_i<K} (32/m_i)
           E[1_{A_cov}J(t_n(min(2m_i,K)))]
      <= O(log n) n^{-1/2+o(1)} -> 0.                         (6.12)

If the index set is empty the event is empty. This includes near-cap
maximizers; there is no unproved small-start assumption.

Truth inclusion follows from the TV part of L6.2 and the same argument
as L3.3(a), detailed here to record uniformity. Conditional on X,
all Z_{U,j}, j in S0, |U|<=15, j notin U, are unit normals. There
are at most s0 sum_{a<=15}binom(p,a)=n^{O(1)}, so a normal union bound
gives max Z^2<=C log n with probability tending to one. Hence each
missing truth has add gain RSS_U-RSS_{U+j}=(delta+sigma Z)^2>=c n.
L0's likelihood lower bound ([GEN-L1] L1.4(b) on A_score [A7]) and remainder imply its block table gain
is at least c' n-(1/2)log(n+1)-2 kappa_E. Its prior cost is at most
log(2p). Thus it strictly improves the start score whenever addition
is feasible. On the size event k<=2k0, addition is feasible if Q!=[p]
by the construction of Q. If Q=[p], q=p=O(log n), K=p eventually;
either k<p, so addition is feasible, or S_tilde=[p] already contains
every truth. This proves inclusion for every maximizer.

Finally work also on (6.7)'s complementary high-probability event. If
l in S_tilde minus Q, deleting l gains at least

    log(p/k)+(1/2)log(n+1)-(1/2)h_{U_b minus {l},l}
                 -2 kappa_E-o(1)
      >= (1/4)log n-log k-2 kappa_E-o(1)>0,

since k<=2k0=O(log n). This contradicts maximality. If Q=[p]
exclusion is vacuous. The proof used only the block size, not a
population partition recovery assertion. QED.

## 5. NA with approximate local innovations

**Lemma L6.6. PROVED (by this seat, unchecked).** P(NA(L))->1.

*Proof.* For each deterministic T in L and l notin T, let a,b be its
nearest indices on either side of l (either can be absent). Population
Markov regression gives

    W_l=c_a W_a+c_b W_b+e_{l,a,b},

where e_{l,a,b} is independent of the entire W_T, has iid Gaussian
entries with variance tau_{l,a,b}^2 in [c_-,1]. Consequently, with
g_{l,a,b}=C e_{l,a,b},

    (I-P_T)CW_l=(I-P_T)g_{l,a,b}.                             (6.13)

This is exact. The coefficients are population coefficients, not sample
regression coefficients. Column standardization does not affect the
normalized direction in (6.13).

There are at most p(q+1)^2 innovations. Gaussian chi-square concentration
and a union bound give min ||g||>=c sqrt(n) with probability tending
to one. For each (T,l), conditional on W_T,

    ||P_T g_{l,a,b}||^2/tau_{l,a,b}^2 ~ chi^2_{|T|}.

There are at most p 2^{q-s0}=n^{O(1)} pairs and |T|<=q<=C log n.
The mgf bound
P(chi^2_d>v)<=2^{d/2}exp(-v/4) and a sufficiently large v=C'log n
therefore imply, uniformly, ||P_Tg||<=C sqrt(log n) with probability
tending to one. Also ||P_T eps||<=||P_Q eps||<=C sigma sqrt(log n)
simultaneously, by conditional chi-square concentration given X.

Define Z^0_{l,a,b}=g_{l,a,b}'eps/(sigma ||g_{l,a,b}||). Given the RAW
matrix W each is a standard normal, because g is a W-measurable linear
combination of raw columns and eps is independent of W. (The raw scales
need not be measurable in standardized X; no such claim is needed.)
A conditional union bound given W, then integration, gives

    max (Z^0)^2 <= 2log(2p(q+1)^2)+2log log n                    (6.14)

with failure probability at most 1/log n. No independence between
the different Z^0 variables is needed.

Let h=(I-P_T)g. Subtracting the two normalized noise inner products,

    |Z_{T,l}-Z^0_{l,a,b}|
      <= |Z^0| (||g||/||h||-1)
          + ||P_Teps|| ||P_Tg||/(sigma ||h||).

On the preceding events ||h||^2=||g||^2-||P_Tg||^2>=c n,
||g||/||h||-1=O(log n/n). Equations (6.14) and p<=n^A give

    max_{T,l}|Z_{T,l}-Z^0_{l,a,b}|=O(log n/sqrt(n)),
    max_{T,l} Z_{T,l}^2 <= 2log p+O(log log n)+o(1).            (6.15)

The L2.2 threshold is
c_n=log(n+1)+2log p-2log(q+1)-4 kappa_E-2. Its excess over
the right side in (6.15) tends to infinity, since q=O(log n).
L2.2 on A_score proves NA. The exact fixed-design direction family
may be exponentially larger; the proof bounds a uniform error to a
small reference family instead of asserting (G4-dir). QED.

## 6. TL

**Lemma L6.7. PROVED (by this seat, unchecked), using L2.1.**
P(TL(L))->1 under the joint law.

*Proof.* Conditional on X in A_X, the hypotheses used by L2.1 hold
with the common constants and envelopes of L6.2. The family size is
bounded by a fixed power of n, its maximum size is O(log n), and all
its Gram floors hold. The L0 Gaussian bounds defining A_score have
uniform o(1) failure probability. L2.1's deterministic comparison on
that event has uniform eventual sign because theta_min is fixed and
its missing-truth signal lower bound is c n, whereas all error and
prior terms are O(log n). Integrating gives the result. QED.

## 7. Assembly and posterior de-randomisation

*Proof of Theorem L6.1. PROVED (by this seat, unchecked), using the
listed inputs.* L6.5–L6.7 give (6.1). The pathwise argument of L4,
using L1 and [OP], applies without NEG or G4 once the THREE EVENTS
themselves are available. With MR1 the LS0 cap is at least
|S_tilde minus S0|. Thus

    D_n <= P(Sand_n^c)+P(NA(L)^c)+P(TL(L)^c) -> 0.

To apply [S-T] under the joint law, use A_X of L6.2. Every deterministic
sequence x_n in A_X satisfies H0 with the same constants and BM envelope.
If for some fixed e>0 the supremum over x in A_X of
P_eps(1-pi_x(S0)>e) failed to tend to zero, choose a violating x along
a subsequence and any x in the nonempty A_X at the remaining sufficiently
large indices. The resulting deterministic sequence satisfies H0 but
contradicts [S-T]. Thus the supremum tends to zero. Outside A_X the
unconditional failure probability is at most P(A_X^c)=o(1).
This is precisely GEN L5.3's diagonal argument, applied to the H0-only
posterior input; it does not invoke GEN's bounded-relevance conclusion.
Hence 1-pi_X(S0)->0 jointly in probability, and boundedness in [0,1]
gives E[1-pi_X(S0)]->0. Integrating [M5-0]'s conditional inequality
now gives (6.2). The last identity subtracts the error event from O,
exactly as in L4. QED.

## 8. The study's high-p S2 layouts

**Corollary L6.8. PROVED (by this seat, unchecked), with the same named
inputs and method premises as Theorem L6.1.** For rho=1/2 the p=500 and
p=1000 truth layouts in gen_dev_data.R satisfy (6.0), for every fixed
positive signal scale c. Thus Theorem L6.1 applies both to either fixed-p
sequence and to polynomially growing p sequences extending either fixed
14-truth layout.

*Proof.* In the R code the active locations have the form
5 step k+pos_{k mod 6}, k=0,...,13, with step=7 or 13 and
pos=(3,2,4,1,5,3). Any two consecutive locations are at least
5 step-4>=31 apart, and hence every distinct pair is at least 31 apart.
The absolute standardized coefficients lie between 0.8c and 1.8c.
For each truth the left side of (6.0) is at most
13(1.8c)2^{-31}. Its right side is at least
(0.8c/2)(1-1/4)/(1+1/4)=0.24c. The former is strictly smaller:
23.4<0.24 times 2^{31}, since already 0.24 times 128=30.72>23.4.
The R signal uses these exact sample-standardized coefficients; no
population rescaling assumption is involved. QED.

Caveat (council R10 F1, added by the lead): for the FIXED-p sequences (p = 500 or 1000) the production run eventually
takes the exact-enumeration branch (SoP `02_method.tex:167`), so for those sequences the conclusion eventually follows
from T03♯ and enumeration; the LS0 mechanism is the operative one for polynomially growing p sequences extending the
layouts.

## 9. Exact inventory and frontier

New results **PROVED (by this seat, unchecked)**:

1. Uniform sample regularity, H0, lattice Gram floor, within-block SE,
   and TV for sample-standardized iid Gaussian AR(1), with deterministic
   envelopes and p<=n^A, without requiring p<n (L6.2).
2. Selection-uniform reduction of every size-at-most-15 conditioning set
   to a deterministic polylogarithmic reference family, with o(1) error
   for the RSS-normalized far-null add statistic (L6.3).
3. A joint-law spherical upper tail and count bounds for that statistic,
   including the random standardized-scale signal (L6.4).
4. The full start-mode sandwich, including large and near-cap maximizers,
   for the actual X-dependent blocks (L6.5).
5. Uniform approximation of lattice noise directions by population
   innovations, and joint-law NA (L6.6); joint-law TL by L2.1 (L6.7).
6. The stated random-design discovery and reported-HPM conclusions,
   conditional on the named proof inputs and implementation premises
   and MR1 (Theorem L6.1).
7. Verification of the separation condition for both study high-p S2
   truth layouts and every fixed positive scale (L6.8).

Assumed, not newly proved: the precise score expansion L0; population
facts P1–P4 from L5; the deterministic L1/L2.1/L2.2 results; the
operational premises and [OP]; the cited posterior and M5 inputs.
Their original statuses are retained above. No partition recovery input,
fixed-design NEG input, exact direction-count input, or bounded GEN
certificate is assumed. No simulation or external numerical package is
used as proof.

**Frontier:** the author's status label remains PROVED (by this seat, unchecked); the separate check record is in
the header (R06, R07). No unclosed mathematical step was identified by the author or the two checks. The raw R generator is finite-domain (p=500 or 1000
in generate_dev_dataset); this theorem concerns asymptotic sequences
extending its S2 covariance and standardized signal construction, under
the explicit separation assumption (6.0). It does not prove arbitrary
nonseparated AR(1) truths, compound symmetry, delivery, the production
LS0 cap, LS0 integration/e4, or any upgrade to the locked C-GROW target.
