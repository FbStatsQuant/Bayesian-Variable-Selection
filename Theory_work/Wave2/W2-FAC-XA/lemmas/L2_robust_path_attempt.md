# L2: independent robust-path attempt (conditional result; C1 remains open)

This file contains an independent derivation, not a review or a claim that XA
X2 has been established. No other XA lemma is an input. Sources used are locked
XA STATEMENT v1, PLAN, R01; FAC-B L1, L3, L4 and its score setting; FAC-A L1
(innovation coupling), L3 (truth moves and score expansion), L5 (design-event
uniformity). Only this file and numerics/N3* were written. No git operation,
W2-FAC-X access, contact, delegation, or new review was performed.

Cross-family review: reviews/R03_L2_path.md; conditional results verified there,
mandatory M1–M3 applied below. X2 remains open. This is not PROVED-CHECKED status.

## 1. Exact reference and the explicit perturbation hypothesis

Use FAC-B's exact-CS reference with fixed rho in (0,1), fixed s>=1, fixed nonzero
standardized truth coefficients and noise variance. Its independent coordinates
are xi_j, eta; S0 is the truth. N0 has at most 15 nulls, S*=[p]\N0,
N*=S*\S0. All coordinates and score quantities below belong to this ONE fixed
reference problem, not a new draw at each step. Write

    k=|T|, m=k-s, kappa=(1-rho)/rho+1/[rho(n^2-1)], q=k+kappa,
    B=sum_{S0} xi_j-varpi, x_T=(B+sum_{T\S0}xi_j)/q,
    tau_j=xi_j-x_T (null), gamma_k=1/q, nu=n/2+.01.

For a truth add sqrt((n-1)(1-rho))*theta_j/sigma to tau_j.
The symbol varpi denotes exactly FAC-B's offset varrho (STATEMENT section 3).
Define alpha=(n^2-1)(1-rho)+1, k1=sigma*sqrt((n-1)(1-rho))/s_Y,
psi_T=.02+Q_T, M_T=nu*n*k1^2/(alpha*psi_T). Let Delta_k be FAC-B L1.3's
exact size penalty. Put c=(1+1/(q-1))*M_T and b=(1-1/(q+1))*M_T. Exactly,

    D_j=Delta_k-nu log(1+c*tau_j^2/nu),
    A_l=-Delta_{k+1}-nu log(1-b*tau_l^2/nu),
    W_jl=-nu log(1-M_T*V_jl/nu),
    V_jl=tau_l^2-tau_j^2-(tau_l-tau_j)^2/q.

All gains are relative to the centre. Missing types are ignored.

**UP(zeta), a hypothesis, NOT an iid-CS conclusion:** on a joint coupling of
the actual problem and this reference, for every S0 subset T subset S*, and
every feasible deletion, addition or swap, the actual gain differs from the
reference gain by at most zeta. This includes truth-deleting neighbours.
It is enough to have this bound on every state reachable by the perturbed
search, but that formulation must be proved without circularity. A uniform
absolute score error r implies UP(2r); a common additive score constant is
irrelevant. Neighbour gains cannot be resampled in an actual score function.

This is a uniform GAIN assumption; it is neither an absolute nor a relative
Gram-norm assumption. No bound for centered/sample-standardized iid Grams is
claimed here. In particular no absolute O_P(sqrt(p/n)) input is used. A possible
sufficient envelope to investigate is zeta <= C p^2 (log n)^C0/sqrt(n), fixed C0;
it tends to zero polynomially for every fixed a<1/4, p<=n^a. This displayed
envelope is an UNPROVED candidate, not a transfer lemma or a derived rate.

## 2. Finite deterministic certificates and approximate argmin

At any state let d=min_{kept nulls}|tau_j|, R=max_{outside nulls}|tau_l|.
For m>0 define

    L=Delta_k-c*d^2,
    Uadd=-Delta_{k+1}+b*R^2/(1-b*R^2/nu),
    v=max(0,R^2-d^2),
    Uswap=M_T*v/(1-M_T*v/nu).

Use Uadd or Uswap only when its denominator is positive; an empty type has
upper bound -infinity. Suppose every reference truth deletion/truth-out swap
has gain <=-t, t>zeta. If

    L>zeta, L-Uadd>2zeta, L-Uswap>2zeta,                 (C)

the actual best improving neighbour is a null deletion. Indeed the reference
best null deletion is >=L by log(1+u)<=u. Additions are <=Uadd by
-log(1-u)<=u/(1-u). For null swaps V<=R^2-d^2, giving Uswap (negative V
already gives negative gain). Perturb both sides of each comparison by zeta.
Truth moves have negative actual gain. This proves (C) without a swap-sign
assumption. A positive swap may occur in the reference; (C) only compares it
to the deletion. At m=0 check all reference neighbour gains <-zeta instead.

General certificate: the same comparison holds for ANY valid reference lower
bound L on the best null deletion and upper bounds Uadd, Uswap on the other
null move types, provided the three strict inequalities (C) and truth bounds
hold. In section 5 the end phase uses its sharper convexity upper bound for
Uswap, not necessarily the crude R-squared bound displayed above.

If an actual best deletion chooses j, then D_j>=max D-2zeta. Consequently

    tau_j^2 <= d^2 + (exp(2zeta/nu)-1)*(nu/c+d^2).       (AA)

Proof: exponentiate nu log[(1+c*tau_j^2/nu)/(1+c*d^2/nu)]<=2zeta.
For c>=1/4, d^2<=nu and 0<=zeta<=nu/2, exp(u)-1<=2u for 0<=u<=1,
so tau_j^2<=d^2+20zeta and |tau_j|<=d+sqrt(20zeta).
This allows different deletion orders. AA does not establish an interval hole.

## 3. Deterministic bulk balance with fuzzy tail exceptions

Here is a precise robust version of the sign-balance calculation. Let the M
null coordinates in N* be distinct in absolute value, bounded by H. For each
absolute top-J set assume

    |sum Top(J) xi|<=beta*J*H,
    J(1/2-beta)<=#negative Top(J), #positive Top(J),

for the J used below, with 0<beta<1/2. Let K be a retained set of m nulls and
let a<0<b, a<x<b. Put K0={xi<=a or xi>=b} within N*. Assume

    |K symmetric_difference K0|<=r,
    |a+b-2x|<=delta, x=(B+sum_K xi)/(m+s+kappa), |B|<=B0.

Then, with q=m+s+kappa,

    |x| <= max(delta/2,
       [B0+beta*H*(m+r)/(1/2-beta)+r*H]/q).            (BAL)

Proof: if x>delta/2, a+b>=2x-delta>0, so b>|a|.
Let J index all points with |xi|>=|a|. K0 is Top(J) with some POSITIVE
points removed. Its negative count equals that of Top(J), hence
J(1/2-beta)<=#negative K0<=m+r. Also sum K0<=sum Top(J)<=beta J H;
changing at most r points changes the sum by at most rH. Substitute in qx.
If x<-delta/2 reflect xi,B,a,b. In the remaining case |x|<=delta/2.
This proves BAL, including adversarial/history-dependent exceptions.

Thus delta=o(H), beta=o(1), r=o(m), B0=o(mH) give |x|=o(H).
FAC-B E5 supplies beta_J=sqrt(2[2log(J+1)+loglog n]/J) for both bounds
(the sign-count bound is even smaller). For bulk m>=K loglog n, J>=m-r,
so sup beta_J can be made a fixed small constant by large K, eventually;
take r=o(loglog n). This use of E5 is simultaneous, not conditional on a
data-selected threshold. If a fuzzy boundary band of width w contains at most
r points, it provides this exception bound only AFTER a fuzzy-tail invariant
has located every exception in those bands. That implication is not assumed
from approximate argmin. BAL explicitly requires straddling thresholds.

A second finite geometric fact makes the fuzzy-gap requirement explicit.
Suppose K agrees with K0 outside [a-w,a+w] union [b-w,b+w], and
x lies in [a+w,b-w]. Then every kept point has distance at least
min(x-a,b-x)-w, whereas every deleted point of N* has distance at most
max(x-a,b-x)+w. Consequently

    max_{deleted in N*}|xi-x| <= d+|a+b-2x|+2w.       (FG)

Indeed agreement rules out retained points in the central core and deleted
points beyond the two exterior band endpoints; subtract the two distance
bounds. No boundary witness is needed for this one-sided inequality. Empty
deleted sets are ignored. Thus delta+2w<=.02H implies the bulk fuzzy-gap
condition below for deleted N* nulls. N0 is handled separately. FG is a
deterministic implication from band localization, not a proof of localization.

## 4. End phase: quantitative majority stability, with no path coupling

Suppose all retained nulls have magnitudes in [H-w,H], all outside nulls have
magnitudes <=H, |B|<=B0. Let Nplus-Nminus=I, q=m+s+kappa. Then

    x=(I*H+E)/q, |E|<=e:=B0+m*w.                     (END)

Assume e<H and H-e>q*w, so |x|<H-w and each sign is on its proper side
of x. If I>=1 and both signs are present, the closest positive has squared
distance <=(H-x)^2; every negative has squared distance >=(H-w+x)^2.
Their squared-distance separation is at least

    Jgap=[2(H-e)/q-w]*(2H-w)>0.                     (MAJ)

If I<=-1 reverse signs. If only the majority sign exists the conclusion is
automatic. The gain gap favouring a majority deletion is at least

    c*Jgap/[1+4*c*H^2/nu],                         (MG)

by integrating derivative c/(1+c*u/nu) of nu log(1+c*u/nu);
all null squared distances are <=4H^2. Therefore UP(zeta) forces majority
deletion whenever MG>2zeta. This is a finite deterministic bound.
For m<=m_e, m_e*w=o(H), B0=o(H), c bounded above and below, H^2=o(n),
the uniform sufficient error budget is

    zeta=o(H^2/m_e).                               (TOL)

It follows that |I| decreases by one when nonzero, and becomes one when zero.
For |I|>=2, |I|/q never increases until |I|<=1, since
(|I|-1)/(q-1)<=|I|/q iff |I|<=q. Thus an entry bound |I|/q<=r0 propagates
whenever |I|>=2. This proves robust majority stabilization without agreement
with FAC-B's deletion order.

## 5. Conditional C1 path theorem and explicit margins

Fix 0<a<1/4, p<=n^a. In the large branch p>n^(1/200) use FAC-B's E_n and
M_T=1/2+o(1) uniformly (E2 and p=o(n) suffice for the upper bound; the matching
lower bound follows from L1.5 and RSS_T<=||e||^2). Let H=bar H from L3,
h=H^2<=2a log n+o(log n), B0=O(loglog n). Let m_e=ceil(K loglog n), fixed
large K, and suppose UP(zeta) holds with zeta=o(h/m_e). Make the following
GEOMETRIC hypotheses on every prefix of the actual search consisting so far
of safe deletions:

* While m>=m_e, |x|<=.01H and every outside null has distance <=d+.02H;
  N0 may instead use its bound |xi|<=loglog n, giving the same envelope
  max(d+.02H,loglog n+.01H).
* At the first m<m_e and thereafter every retained magnitude is in [H-w,H],
  m_e*w=o(H), and the entry imbalance satisfies |I|/q<=.04+o(1).

These hypotheses concern perturbed prefixes, NOT the exact FAC-B path.
The first centre bound can follow from BAL if its stated fuzzy-tail premises
and sufficiently small beta,r/m,delta/H are proved. The second magnitude
condition is a separate requirement, not a consequence of BAL alone.

Under these explicit hypotheses, the actual search makes exactly |S*|-s safe
deletions and stops at S0. Here is the complete margin calculation.

Bulk: some kept null has |xi|<=H, hence d<=1.01H. Since q>=m_e, c=1/2+o(1).
Thus best reference deletion >=[.5-1.0201*a-o(1)]log n.
For outside distances R<=1.03H (including N0 eventually), reference addition
<=[-.5+1.0609*a+o(1)]log n. A null swap has
V<=R^2-d^2<=(.02H)(2*1.01H+.02H)=.0408h if the first R bound dominates;
if the N0 bound dominates, V<= (loglog n+.01H)^2=.0001h+o(h).
Therefore its gain <=[.0408*a+o(1)]log n. Both deletion-vs-addition and
deletion-vs-swap margins exceed .20 log n eventually for every a<1/4.

End: END gives x=IH/q+o(H)/q. Replacing retained signed magnitudes by H
costs O(H*w+H*e)=o(h) in the quadratic bounds below, uniformly. Put t=|I|.
For t>=1 the best deletion cost is at most

    (h/2)*(q-t)^2/[q(q-1)]+o(h) <= h/2+o(h).

For t=0, m>=2, its cost is at most (h/2)*q/(q-1)+o(h)<=h+o(h), since
q-1>=s+1+kappa>2. Hence every state m>0 has a deletion gain at least
[.5-2a-o(1)]log n. More specifically t>=1 gives [.5-a-o(1)]log n.
For additions the cost is at most (h/2)*(q+t)^2/[q(q+1)]+o(h).
For t=0 it is <=h/2+o(h); t=1 gives <=(h/2)*(1+1/q)+o(h)<=.75h+o(h)
because q>=s+1+kappa>2. For t>=2, majority stability gives t/q<=.04+o(1),
so it is <=(h/2)*1.0816+o(h). Additions thus have gains at most
[-.5+1.5a+o(1)]log n, negative for a<1/4.

For a null swap, convexity in the outside coordinate reduces its upper bound
to outside endpoints +/-H. Expanding at retained sign sigma gives
V<=4h*(sigma*I-1)/q+o(h) at the opposite endpoint and o(h) at the same
endpoint. Thus swaps gain <=2h*(t-1)_+/q+o(h). For t<=1 this is o(log n);
for t>=2 it is <=[.16a+o(1)]log n. Compare with the STRONGER deletion
bound [.5-a-o(1)]log n in the latter case. All deletion-vs-swap margins are
at least min(.20,.5-2a)log n eventually. This positive margin is newly derived
under the displayed hypotheses, not a positive swap-sign margin from FAC-B.

MG and TOL force the majority rule inductively after every safe prefix.
FAC-B L4.0(e)'s truth bounds apply on the entire reference lattice, so under
UP truth moves remain negative (their reference separation is order n).
The margins and zeta=o(h/m_e)=o(log n) now force the next actual move to be
a null deletion. At m=0, x=B/(s+kappa)=o(H), so every addition has gain
<=(-.5+a+o(1))log n, while truth moves remain negative. This proves stopping.
The cap ell_n+|S*| exceeds |S*|-s, so this conditional path reaches S0 within
the cap, including the final scan. No posterior/delivery theorem is inferred.

The small branch p<=n^(1/200) needs neither geometry nor majority: FAC-B
L4.2's bounds hold on every reference lattice state, with null deletions
>=.29log n, additions<=-.29log n, null swaps<=.11log n and truth moves
negative. UP with zeta=o(log n) therefore proves the same safe-path conclusion
even for bounded and oscillating p. This is conditional on UP, not iid transfer.

## 6. Exact missing steps; what this attempt does not prove

There are TWO independent gaps to an unconditional iid-CS result:

1. Prove UP at the stated budget for the centered, sample-sd-standardized iid
   design and a SINGLE CS/noise coupling, uniformly over the required states
   and all move types. FAC-A's absolute-norm innovation coupling does not by
   itself give this new score bound or the exponent 1/4. A relative covariance
   bound alone is not a gain-perturbation proof. Ridge terms, determinant terms,
   conditional noise coupling and truth neighbours must all be accounted for.
2. Starting from AA, prove the displayed geometric hypotheses for EVERY
   approximate-deletion prefix, including bulk-to-end entry. FAC-B L4.1's
   induction fails literally at its first line: an approximate nearest deletion
   may remove a point behind the nearest retained boundary, leaving a retained
   point in the deleted interval. For example x=0 and nulls .1,.1001,2 with
   tolerance .001 permit deleting .1001 while .1 remains. This example is also
   compatible with x=(B+sum K xi)/q by choosing B=-sum K xi. It is a failure
   of the exact interval invariant, NOT a counterexample to a fuzzy invariant
   or to X2. A uniform occupancy bound for short intervals could control
   boundary exceptions, but no argument here proves that exceptions stay in
   those bands or prevents their accumulation through centre drift. BAL does
   not repair this missing induction. Nor does it establish tail concentration
   at m_e, straddling thresholds, or the entry imbalance on its own.

Consequently the unconditional robust FAC-B path lemma and the iid-CS
a<1/4 target remain open in this attempt. The proved content is the finite
certificate, AA, BAL, END/MAJ/MG, and the explicit conditional path theorem.
No downstream use should silently discharge either gap using this file.

## 7. Unequal-loading weighted centre (secondary identity only)

For an exact one-factor Gram write psi_j=1-lambda_j^2,
A_j=(n^2-1)psi_j+1, v_j=sqrt(n^2-1)*lambda_j/sqrt(A_j),
u_j=z_j/sqrt(A_j). Then Hmat=diag(sqrt(A))*(I+vv')*diag(sqrt(A)). Hence

    z_T'Hmat_T^-1 z_T = sum_T u_j^2-(sum_T v_j*u_j)^2/(1+sum_T v_j^2).

Let C_T=sum_T v_j*u_j/(1+sum_T v_j^2). A deletion loses

    (u_j-v_j*C_T)^2/[1-v_j^2/(1+sum_T v_i^2)].

Its centre updates as

    C_{T\j}=C_T-v_j*(u_j-v_j*C_T)/(1+sum_T v_i^2-v_j^2).

These follow by Sherman-Morrison (or expanding the two displayed quadratics).
Writing r_j=u_j/v_j makes this a weighted mean with weights v_j^2 and an
anchor of weight 1 at zero. Deletion ordering includes v_j and the leverage
denominator; heterogeneous loading does not reduce to unweighted nearest r_j.
The determinant/prior contributions can also depend on j. This identity does
not prove a weighted BAL or majority rule and supplies no C2-E/C2-R conclusion.

## 8. Falsification artifact

Run numerics/N3_robust_path.py with Python -B; its JSON output records seeds,
finite certificate comparisons against direct FAC-B scores, AA, conditional
BAL and majority inequalities, weighted identities, and independently perturbed
full neighbour scans. At most 20 seeds are used. The scan perturbations are an
adversarial-oracle stress test, not an iid-CS gain coupling or necessarily an
integrable model-score perturbation. The tests cannot discharge either gap
above. See N3_robust_path_output.json for measured counts and discrepancies.

Recorded run: seeds 0--19, n=10^8, p=64, rho=.5, truth coefficients (1,1.3),
gain perturbation magnitude .001. Here p<n^.24. All 20 oracle paths made
62 safe deletions and stopped at S0; 48 selections differed from the reference
best move at the SAME current state. There were no swaps, additions or truth
losses. There were zero failures among 1,240 finite certificates, 1,240 AA
checks, 2,000 BAL checks, 2,000 FG checks and 1,730 MAJ/MG checks. Four hundred
weighted identity checks had maximum error 8.89e-15. The direct absolute-score
subtraction versus stable log1p gain discrepancy was 9.17e-6 at n=10^8
(scores have size n log n); finite certificates use the stable gains.
These tests exercise the conditional identities and oracle paths; they are
neither an iid-CS experiment nor a test of FAC-B's astronomically large
bulk/end onset constants. The imported CS scorer's SHA256 was unchanged.

Stress-test scope (R03 M2): zeta=.001 is tiny relative to the observed safety
margins. BAL numerics choose the anchor to fit the sampled centre, rather than
testing a fixed Gaussian anchor along a path. FG uses midpoint x, so does not
exercise its delta term. Every oracle path has N0 empty. These are algebra and
limited falsification checks, not strong tests of the missing stochastic invariant.
