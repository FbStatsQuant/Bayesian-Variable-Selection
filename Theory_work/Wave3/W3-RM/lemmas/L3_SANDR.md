# L3 - Abstract Gaussian-row sandwich SAND-R

Status: PROVED (by this seat, unchecked); cross-family check R04 (Claude Opus 5.5 high,
`../reviews/R04_SANDR_check_opus.md`): VERIFIED-WITH-AMENDMENTS (3 MINOR, 4 NIT; no FATAL/MAJOR), applied by the lead
[R04-F#]. The slower localisation rate is in `L3b_rate.md` (R04: VERIFIED).

Seat: research parallel prover, Codex gpt-6.1-sol, high effort, 2026-11-09.
All limits are as n tends to infinity. New arguments and checks of replacement inputs
are marked [NEW]. Only the sandwich interface is claimed, not NA, TL, POST or delivery.
Mathematical notation is ASCII: S0 is the true support; Sigma is population covariance.

## 1. Exact lemma statement

**Lemma SAND-R (baseline form: the v1.1 localisation rate n^{-2}; the v1.2 rate r_n is the extension L3b_rate.md
[R08-17]).** Assume Setting R of
`Theory_work/Wave3/W3-RM/STATEMENT.md:40-42`: raw rows are iid N(m_n,Sigma_n),
Sigma_n has unit diagonal, X is centered and sample-standardized,
Y=X theta*+C epsilon, epsilon is independent N(0,sigma^2 I_n), sigma>0 fixed,
s0>=1 fixed, theta_lo<=|theta*_j|<=theta_hi on S0, and p<=n^A, A>=1 fixed.
Use the shipped D0 score (response scaled internally), capped BB(1,p) prior,
block tables and start law gamma0 specified at
`Theory_work/Wave3/W3-RM/STATEMENT.md:33-36`, with K=min(p,floor(n/2)).
Let Q contain S0 and be deterministic. Assume the following fixed-constant bounds:

* (FL-R): lambda_min(Sigma_S)>=c>0 for every |S|<=16+s0 and every S=Q union {l}.
* (V-R): PTV(a0), a0>0: for every j in S0 and U not containing j, |U|<=15,
  |Cov(W_j,sum_{k in S0} theta*_k W_k | W_U)|>=a0.
* (L-size): q=|Q|<=(log n)^kappa, with kappa>=1 fixed.
* (L-feas): q<=K and either Q=[p] or K>=2q+32s0+1, eventually.
* For each l outside Q there is deterministic H_l containing {l} union S0,
  |H_l|<=(log n)^kappa. For every U not containing l with |U|<=15 put U0=U intersect H_l.
  (L-gain-R): |Cov(W_l,W_j|W_U0)|<=C_L n^{-1/2}, j in S0 minus U0.
  (L-loc-R): |Cov(W_l,W_v|W_U0)| and |Cov(W_j,W_v|W_U0)| are <=C_L n^{-2},
  for v in U minus H_l and j in S0 minus U0.

Then for any X-measurable partition into blocks of size at most 16,
under the joint law of (X,epsilon),

    P(S0 subset S_tilde subset Q for EVERY maximizer S_tilde of gamma0 on Omega) -> 1,
    Omega = {S: |S|<=K}.

[NEW] This is precisely the target as locked in STATEMENT v1.1 (localisation rate n^{-2}), with no additional condition. [R04-F3] The floor on
Q union {l} is unused for the sandwich: the lemma holds with FL-R restricted to sets of size <=16+s0 (the sets
U union S0 union {l} and their subsets); the Q union {l} floor is consumed by NA/TL only. Section 8 proves a rate weakening.

Source aliases below are exact repository path abbreviations; alias:line is a
path:line citation, with ranges specifying the complete reused argument:

* G6 = `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md`.
* G3 = `Theory_work/Wave1C/C-GROW/lemmas/L3_sandwich.md`.
* G0 = `Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md`.
* APP = `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md`.
* D4 = `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md`.
* D1 = `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md`.
* UNI = `Theory_work/Wave2/W2-UNI/lemmas/L2_k0.md`.
* RM = `Theory_work/Wave3/W3-RM/STATEMENT.md`.

Statuses copied verbatim, not upgraded: G6:3, "PROVED (by this seat, unchecked)",
checks G6:4-7 "VERIFIED" / "VERIFIED-WITH-AMENDMENTS"; G3:3,
"PROVED (by this seat, unchecked)", check "VERIFIED"; G0:3,
"PROVED (by this seat, unchecked)", check "VERIFIED"; APP:3,
"PROVED (by this seat, unchecked)", check APP:7-9 "VERIFIED-WITH-AMENDMENTS";
D4:3 and D1:3, "PROVED (by this seat, unchecked)", checks D4:5 and D1:7
"VERIFIED-WITH-AMENDMENTS"; UNI:3-4, "PROVED (by this seat, unchecked)",
"VERIFIED-WITH-AMENDMENTS". These remain named inputs with their recorded checks.

## 2. Inventory of every population and counting input

[NEW] Audit scope: G6:85-389, APP:54-96, D4:21-43, D4:78-90,
D1:44-59, UNI:79-133. The G6 labels L6.2-L6.5 correspond to its sections 1-4;
its section 5 is NA and is not used here. Unused rows below distinguish the
sandwich argument from other conclusions bundled into source regularity lemmas.

| Input, with quantifiers | Source use (aliases expand above) | Abstract supplier or verdict |
|---|---|---|
| Raw Gaussian mean removable; orthonormal basis of centered row space gives N=n-1 iid Gaussian rows | APP:15-17; G6:85-99 | Setting R |
| Unit coordinate variances, hence abs(Sigma_jk)<=1; independent noise coordinate of variance sigma^2 | G6:85-101; UNI:188-189 | Setting R; no global upper spectrum needed |
| Floor on U union S0 union {l}, |U|<=15, and on all <=16 sets | G6:134-152,205-207,254-267; APP:86-89 | FL-R: union size <=16+s0 |
| Schur-complement floors c; individual conditional design variances in [c,1] | G6:150-152,255-267 | FL-R on relevant union and unit diagonal |
| Sample floors c/2 on all <=16 design sets | G6:108-113,159-166 | FL-R plus entrywise concentration |
| Floor on Q union {l}, sample error q O(sqrt(log n/n))=o(1) | G6:108-113; D1:48-50 | FL-R and L-size; unused here, belongs to NA/TL |
| Floors on arbitrary O(log n) sets for SE_w and anchored SE; m_sharp=O(log n) | G6:115-126; D1:51 | NONE in full generality; not consumed by sandwich (POST-only bundled H0 checks) |
| Energy norm(mu)^2<=(n-1)(s0 theta_hi)^2; fixed beta-min | G6:124-126 | Setting R and standardized sample column norms |
| PTV(a0) for all j in S0, U not containing j, abs(U)<=15 | G6:128-141; APP:63-66 | V-R; replaces AR separation |
| Simultaneous sample TV: delta_{U,j}^2 >= (n-1)a0^2/4 | G6:134-141; UNI:87-88 | V-R, small-set FL-R, entrywise event; section 3 |
| For deterministic bounded b, Var(V_b given W_U)>=sigma^2; uniform bounded-dimensional response comparisons | G6:143-152; UNI:100-111 | Setting R, independent auxiliary noise; evaluate at theta*/t after uniform algebra |
| Cov(W_l,W_j given W_U0)=O(n^{-1/2}), l outside Q, j in S0 minus U0 | G6:199-201,253-260; UNI:110,118-121 | L-gain-R |
| Cov(W_l,W_v given W_U0)=O(n^{-2}), v in U minus H_l | G6:194-196; UNI:107 | L-loc-R |
| Cov(W_j,W_v given W_U0)=O(n^{-2}), j in S0 minus U0, v in U minus H_l | G6:196-198; UNI:108-109 | L-loc-R |
| Same covariances with j in S0 intersect U0 | UNI:109 | Exactly zero after conditioning; no extra hypothesis |
| Small covariances between two elements v,v' of U minus H_l | G6:203-213 | NOT needed; conditional correlation inverse controlled by FL-R |
| Truth regression on U0 has coefficient norm <=sqrt(15)/c; truth residual covariance >=cI; innovation variance in [c,1] | G6:245-267; UNI:118-121 | FL-R on union size <=16+s0, unit diagonal |
| Norm of spherical mean shift m is O(1) | G6:258-260 | L-gain-R times sqrt(n) and bounded raw norms |
| Deterministic H_l contains l,S0; reference count <=(abs(H_l)+1)^15=n^{o(1)} | G6:171-177; D4:25-27; UNI:97-99 | Neighborhood clause of L-R |
| q<=polylog; k0=q+16s0; log(2k0)=O(log log n) | G6:332,352-361,387; D4:39-42 | L-size |
| p<=n^A and p Nref exp(-t_n(k)/2) exp(C sqrt(log n)) <= k n^{-1/2+o(1)} | G6:296-305; UNI:122-123 | Setting R and neighborhood count |
| All-index score family of <=16 sets has <=17(p+1)^16 members; residual/contrast family polynomial | G6:157-167; G0:12-20 | Setting R and small-set FL-R; independent of partition selection |
| Lattice score family O(p 2^q); quasi-polynomial toolkit | G6:162-163; D1:28-42 | L-size, FL-R through D1; unused for sandwich |
| At most s0 bad blocks; size <=16; distinct blocks supply distinct l | G6:329-350; UNI:132 | Partition contract only |
| q<=K; either Q=[p] or K>=2q+32s0+1 | G6:375-378; G3:78-79 | L-feas; Q=[p] forces K=p |
| Exact BB prior ratio w(k-1)/w(k)=(2p-k)/k and table expansion | G6:336-346,371-385; G0:45-52 | Setting R's inherited method, no further population premise |

## 3. Regularity: the sandwich part of L6.2

[NEW] Write N=n-1, C=I-11'/n, t_j=norm(CW_j)/sqrt(N), X_j=CW_j/t_j.
Subtracting the deterministic raw mean changes neither X nor Y nor any table.
Reuse verbatim G6:85-106 (APP:58-59): polarization, Gaussian square mgf and a
union bound over (p+1)^2 augmented entries give an event E_cov of probability
1-o(1) on which every centered raw covariance entry of (W,epsilon) differs from
population by at most C h_n, h_n=sqrt(log n/n). Also max_j abs(t_j-1)<=C h_n,
and the standardized Gram has entrywise error O(h_n). Normalize noise by sigma
when applying the source's unit-variance argument.

[NEW] For every design set of size <=16+s0, the operator error is O(h_n).
Thus its sample floor is c/2 whenever its population floor is c. Schur formulas
and A^{-1}-B^{-1}=A^{-1}(B-A)B^{-1}, with inverse norms <=2/c, give simultaneous
O(h_n) errors in every bounded-dimensional conditional covariance needed below.
Dimensions are fixed, and all population entries have absolute value <=1.
This replaces every global spectral use in this portion of G6:108-113,134-152.

[NEW] Response comparisons follow the explicit contract UNI:100-105. For every
DETERMINISTIC coefficient vector b supported on S0, abs(b_k)<=2 theta_hi, define
V_b=sum b_k W_k+epsilon0, with independent epsilon0~N(0,sigma^2).
The augmented entrywise event gives O(h_n) conditional-covariance errors uniformly
in this coefficient box, by linear sums and bounded inverses. Population residual
variance of V_b given any design subset is at least sigma^2 and at most a fixed
constant; relevant design residual variances are >=c. Partial correlations therefore
also have uniform O(h_n) errors. Evaluate this algebraic comparison at b_k=theta*_k/t_k,
which lies in the box on E_cov. The centered empirical response is then exactly Y.
[R04-F1] In these comparison steps (sections 3-4) we never condition on the sample scales or assert a Gaussian law
given them. (Section 5 conditions on (W_D, epsilon), which contains the scales of the true columns; that is
legitimate because the innovation e is independent of (W_D, epsilon).)

[NEW] For TV work directly with the standardized Gram and the fixed coefficients
theta*: PTV plus the Schur comparison gives
abs(N^{-1} x_j'(I-P_U)mu)>=a0/2 for every truth j and every U not containing j,
abs(U)<=15. Since N^{-1} norm((I-P_U)x_j)^2<=1,
delta_{U,j}^2>=N a0^2/4. This is G6:128-141 with PTV replacing its separation
calculation; it does not require PTV for arbitrary coefficients b.

[NEW] Energy obeys norm(mu)<=sqrt(N) s0 theta_hi deterministically. Take the
score family F={A subset [p]: abs(A)<=16} and all its residual and contrast vectors.
Conditional on X having the sample small-set floors, use exactly the first-family
application G6:157-167 and G0:19-27,31-49, whose Gaussian failure bounds are uniform
in X, then integrate. Call its event E_score, with probability 1-o(1). It supplies
RSS_A<=C_R n, the RSS lower bound, the table score expansion with remainder difference
<=2 kappa_E, and the nested likelihood lower bound used at G6:371-374.
No lattice-family score event is needed. In particular neither H0, SE_w nor a
posterior assumption is required; claiming all of source L6.2 under the present
hypotheses would be unjustified but is unnecessary. If one wanted the optional
lattice event, the size extension is D1:9-26,48-56, rather than G6's polynomial count.

## 4. Selection removal: L6.3

[NEW] Fix arbitrary l outside Q and U not containing l, abs(U)<=15. Put
U0=U intersect H_l, V=U minus H_l. For deterministic b in section 3's box,
L-loc-R gives, for every v in V,

    Cov(W_l,W_v | W_U0) = O(n^{-2}),
    Cov(V_b,W_v | W_U0)
      = sum_{j in S0 minus U0} b_j Cov(W_j,W_v | W_U0) = O(n^{-2}).

Truths j already in U0 have conditional covariance zero, as does independent noise.
L-gain-R similarly bounds abs(Corr(W_l,V_b | W_U0)) by C n^{-1/2}.
Apply the uniform sample comparisons and evaluate at b=theta*/t. Let z0 be the
sample correlation of W_l,Y given U0, let a,d be their sample partial-correlation
vectors with W_V given U0, and R the sample conditional correlation matrix of W_V.
Then simultaneously on E_cov,

    abs(z0)<=C h_n,   norm(a)+norm(d)<=C h_n,   norm(R^{-1})<=C.

[NEW] The last bound needs no small covariance between v and v' in V. The raw
sample Schur complement of W_V given W_U0 has floor c/2 by the floor on U.
Its diagonal entries are <=2. Dividing by conditional standard deviations preserves
a fixed positive eigenvalue floor for R. All response comparisons use the union
U union {l} union S0, of size <=16+s0. No unlisted larger-set floor is used.

Reuse verbatim the recursive identity and algebra G6:203-215 [R04-F7]:

    z_U = (z0-a' R^{-1}d) /
          sqrt((1-a' R^{-1}a)(1-d' R^{-1}d)).

Thus abs(z_U-z0)<=C h_n^2. Define h_{U,l}=n Corr_sample(W_l,Y | W_U)^2.
It follows that, simultaneously for ALL these pairs,

    abs(h_{U,l}-h_{U0,l}) <= C n h_n^3 =: omega_n -> 0,
    h_{U,l} <= C log n.                                             (1)

[NEW] These are deterministic consequences of E_cov, so they apply to conditioning
sets selected by the partition. For each l the reference family
I_l={A subset H_l minus {l}: abs(A)<=15} is deterministic and has size
<= (abs(H_l)+1)^15 <= (1+(log n)^kappa)^15 = exp(O(log log n)) = n^{o(1)}.
One can encode each subset by its sorted list, padded with a distinguished symbol.
Put Nref=max_l abs(I_l). If there are no l outside Q all far-null statements are vacuous.

## 5. Spherical tail: L6.4

[NEW] Fix deterministic l outside Q and U0 in I_l; D=U0 union S0. Regress
W_l on W_D, writing

    W_l = W_U0 beta + sum_{j in S0 minus U0} alpha_j (W_j-W_U0 beta_j) + e.

The conditional truth covariance matrix has floor c. By L-gain-R its covariance
vector with W_l has norm O(n^{-1/2}), so norm(alpha)<=C n^{-1/2}.
Also norm(beta_j)<=sqrt(15)/c. The innovation e is independent of W_D, with iid
N(0,tau^2) entries, c<=tau^2<=1, by FL-R on D union {l}. On the W_D-measurable
event CN_D={norm(CW_j)<=2 sqrt(n) for j in D}, the projected mean shift

    m=(I-P_U0) C sum_j alpha_j (W_j-W_U0 beta_j)

has norm <=C. These replace exactly the AR-specific inputs G6:253-260, as in
APP:86-90, D4:34-35 and UNI:118-121; all relevant unions have size <=16+s0.

Reuse verbatim G6:262-294: conditional on W_D and epsilon, r_Y=(I-P_U0)Y is
fixed, since the true-column scales use only W_D. The projected e is isotropic
in dimension n-1-abs(U0), has norm >=c' sqrt(n) outside an exponentially small
event, and has uniform spherical direction. The bounded m changes sqrt(h) by
at most a constant and a factor 1+O(n^{-1/2}). Consequently uniformly for
(log n)/2<=t<=(2A+3)log n,

    P(E_cov intersect {h_{U0,l}>=t})
      <= C exp(-t/2+C sqrt(log n)) + C exp(-c' sqrt(n)).               (2)

The conditioning is NOT on E_cov: E_cov implies CN_D; integrate the conditional
tail on CN_D as in G6:291-294. [R04-F1] This conditioning contains t_{S0}; the conditional law of the innovation e
given (W_D, epsilon) is its unconditional N(0, tau^2 I) law, and no law is asserted given a sample-covariance or
scale event. [R04-F4] (2) holds for every 0<=t<=(2A+3)log n with the same proof; the case p=1 is vacuous (Q=[p]). No sphere law after conditioning on sample scales
or on the entire sample-covariance event is asserted.

[NEW] Let J(t) count l outside Q for which some U not containing l, abs(U)<=15,
has h_{U,l}>=t. Set t_n(k)=log(n+1)+2log(p/k)-C0, 1<=k<=K.
By (1), on E_cov the count is bounded by the sum of deterministic reference
indicators at t-omega_n. Equation (2), Nref=n^{o(1)}, p<=n^A, and

    p Nref exp(-t_n(k)/2) exp(C sqrt(log n)) <= C k n^{-1/2+o(1)}

give E[1_{E_cov} J(t_n(k))]<=k n^{-1/2+o(1)}, uniformly in k.
The p Nref exp(-c' sqrt(n)) remainder is negligible uniformly for k>=1.
At T_n=2log p+(log n)/2 the same union bound is n^{-1/4+o(1)}.
The t_n(k)-omega_n and T_n thresholds lie in the range of (2) eventually.
This is the counting G6:296-306 with precisely the abstract reference count.

## 6. Global size ladder: L6.5 with polylogarithmic Q

Reuse G6:316-327 and G0:45-49 verbatim: on E_cov intersect E_score,

    log m(U+l)-log m(U)
      <= -(1/2)log(n+1)+(1/2)h_{U,l}+2 kappa_E+o(1),                 (3)

[R04-F2] for all l outside Q and all U subset [p] minus {l} with abs(U)<=15 (so U and U+l belong to the score
family F). Indeed h=O(log n), so
-nu log(1-h/n)=h/2+o(1). Response scaling cancels from RSS ratios (G6:180-185).

[NEW] Here is the ladder including its altered size envelope. For ANY maximizing
S_tilde put k=abs(S_tilde), U_b=S_tilde intersect C_b, k0=q+16s0. A block is
good if it contains all of its truths in U_b; at most s0 blocks are not good.
Thus k<=k0+16 #{good b: N_b=U_b minus Q is nonempty}.
Removing N_b is feasible; per-block optimality G3:30-32 and the exact prior ratio
give log m(U_b)-log m(U_b minus N_b)>=abs(N_b)log(p/k).
Add N_b back in any order. By (3) one addition must have h_{U,l}>=t_n(k),
with C0=4 kappa_E+2. Distinct blocks supply distinct l, so

    k <= k0 + 16 J(t_n(k)).

This is exactly the algebra G6:329-350. For k>2k0 choose m_i=2^{i+1}k0 with
m_i<k<=2m_i. Then J(t_n(min(2m_i,K)))>m_i/32. Markov and section 5 give

    P(E_cov intersect E_score intersect {some maximizing k>2k0})
      <= sum_{i:m_i<K} (32/m_i) E[1_{E_cov}J(t_n(min(2m_i,K)))]
      <= O(log n) n^{-1/2+o(1)} -> 0.                               (4)

This reuses G6:352-364; K<=n/2 bounds the number of rungs, independently of q.
The replacement q<=polylog gives k0=O((log n)^kappa), precisely D4:39-42 and
UNI:127-131. Witness count events in (4) are independent of which maximizer
was chosen. Thus every maximizer, including ties and near-cap sizes, is covered.

## 7. Truth inclusion, junk exclusion, and feasibility

Reuse G6:366-374 verbatim: conditional on X, every Z_{U,j}=u_{U,j}'epsilon/sigma
is N(0,1). There are at most s0 sum_{a<=15}binom(p,a)=n^{O(1)} pairs with
j in S0, j not in U. A normal union bound gives max abs(Z)<=C sqrt(log n)
with probability 1-o(1). Section 3's TV then yields
RSS_U-RSS_{U+j}=(delta_{U,j}+sigma Z_{U,j})^2>=c1 n.
The likelihood lower bound on E_score makes the block-table gain at least
c2 n-(1/2)log(n+1)-2 kappa_E, exceeding prior cost log(2p).

[NEW] Every missing truth addition is feasible on (4)'s small-size event.
If Q differs from [p], k<=2k0=2q+32s0<=K-1 by L-feas.
If Q=[p], q<=K<=p forces K=p and any missing truth implies k<p.
Thus an omitted truth strictly improves the start score, contradicting maximality.
This is G6:375-378 and G3:78-84 with the abstract feasibility dichotomy.

[NEW] Finally use section 5's event max_{l outside Q,U} h_{U,l}<=T_n.
If l belongs to S_tilde minus Q, deleting l is feasible and, by (3) and the prior
ratio, improves the start score by at least

    log(p/k)+(1/2)log(n+1)-(1/2)T_n-2 kappa_E-o(1)
      >= (1/4)log n-log k-2 kappa_E-o(1) > 0,

since k<=2k0 and log(2k0)=O(log log n). This is G6:380-389 with exactly the
size replacement D4:42. If Q=[p], exclusion is vacuous. All score improvements
are strict; all events are common to every maximizing set. Their intersection
has probability tending to one, proving the lemma exactly as stated. QED.

## 8. Hypothesis verdict and a proved rate relaxation

[NEW] **No repair to (L-R) is required.** Truths in U0 contribute conditional
covariance zero. No smallness assumption between two remote conditioning variables
is needed. Only the small-set part of FL-R is needed for sandwich. Neither the
lattice floor nor T1-R, D-R, eta or eta_A enters this joint-law proof. It does not
claim the whole H0 conclusion of source L6.2 from the present hypotheses.

[NEW] Both C_L n^{-2} localization bounds may be replaced by
C_loc sqrt(log n/n), with any fixed C_loc. Section 4 still has
norm(a)+norm(d)=O(h_n), so (1), (2), and all subsequent estimates are unchanged.
Thus any localization envelope O(h_n) suffices, with changed constants.
This proof retains L-gain-R=O(n^{-1/2}), used to keep norm(m)=O(1) in section 5
and the tail loss exp(C sqrt(log n)). We do not claim that arbitrary
C sqrt(log n/n) can replace L-gain-R: it would permit norm(m)=O(sqrt(log n))
and the stated tail/counting bound would no longer follow with its stated slack.

## 9. Sanity checks

[NEW] **UNI-0**, `Theory_work/Wave2/W2-UNI/STATEMENT.md:103-110`.
Take Q0,Q,d_n from UNI:66-77 and H_l,R_n from UNI:97-99. The global floor c
gives FL-R and PTV is assumed. Growth gives q,abs(H_l)=O((log n)^{d0});
increase the fixed exponent to at least max(1,d0+1) to absorb constants.
The enlargement and q=o(n) give L-feas by UNI:73-75. For l outside Q,
delta(l,j)>d_n for every truth, so conditional decay CD_M gives uniformly
abs(Cov(W_l,W_j|W_U0))<=K2 exp(-t2 d_n)=O(n^{-1/2}) (UNI:76-77).
For v outside H_l its distances from l and all truths exceed R_n; CD_M gives
both O(n^{-2}) localization bounds (UNI:106-111). Truths in U0 give zero.
Hence the original hypotheses, not just their relaxed form, hold. No mismatch.
Q=[p] makes localization vacuous. No metric separation or population partition
recovery is used, including for pseudometrics with zero-distance neighbors.

[NEW] **LOC-BF**, `Theory_work/Wave2/W2-LOC2/STATEMENT.md:76-85`.
Use Q0=union_{j in S0}G(j), enlarged Q of D4:73, and
H_l=G(l) union union_{j in S0}G(j), exactly D4:87.
Independent groups remain conditionally independent after conditioning on any
coordinates (D4:79-80). For l outside Q its group has no truth, so every
L-gain-R covariance is exactly zero. For v outside H_l its group is neither
G(l) nor a truth group, so both L-loc-R covariances are exactly zero.
The global floor c_B=min(c,1-bbar^2)>0 gives FL-R even though the upper spectrum
may grow (D4:80-81). With at most one truth per group,
abs(Cov(W_j,sum theta*_k W_k|W_U))=abs(theta*_j)Var(W_j|W_U)>=c_B theta_lo,
so PTV holds (D4:81-82). Sizes and feasibility follow from D4:73,98 and
D1:57-59, enlarging the fixed exponent to absorb constants and bounded groups.
No mismatch. The lower loading bound b_lo is unused for sandwich; it enters
that class's separate NA proof, not the argument here.

## Adversarial self-check

* The sample-scale comparison is uniform algebra over deterministic b, evaluated
  at theta*/t. The sphere step conditions only on W_D,epsilon, which fix true scales.
* All required population floors concern unions of size <=16+s0. No floor on
  arbitrary growing sets is inferred, and the unused H0 checks are identified.
* The inverse conditional correlation matrix is controlled by a Schur floor,
  not by an unassumed remote/remote covariance bound.
* Residual population variance >=sigma^2 means the auxiliary V_b assertion.
  The far-null statistic is normalized by RSS_U, not a crude sigma^2 n bound.
* The score event covers every <=16 index set before any partition is realized;
  conditional-on-X Gaussian score bounds are legitimate by noise independence.
* The sphere law is used before restricting to E_cov; CN_D is W_D-measurable.
* Reference counts multiply the tail. Deterministic H_l and fixed kappa justify
  the displayed n^{o(1)} count and global size ladder.
* Q=[p] uses q<=K to obtain K=p; feasibility never follows just from small k.
* Strict contradiction margins establish EVERY maximizer, including ties.
* Source checks remain inputs and have not been independently upgraded by this seat.
