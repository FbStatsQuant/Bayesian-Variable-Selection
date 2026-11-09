# L7 — O1 reformulated: direct tolerance, shadow midpoint, and tail occupancy

Research proof attempt for fresh Claude review. **No theorem-status upgrade.**
This is a conditional geometry result for C1's scalar reference recursion, not
a proof of X2 or of an iid-design coupling. Inputs read: XA STATEMENT, amended
L2 and L3, R05_midpoint (route advice), FAC-B L4_path and L3_event. L5/L6 are
not inputs. No W2-FAC-X reads/contact, subagents, or git operations. Only this
file and N8* are outputs.

## 1. Claim and scope

Write P for ambient dimension, M for the initial null count (M=P-O(1)),
c=s+kappa>1 (bounded above and bounded away from 1), q=m+c, and

    x=(B+sum_{j in K} xi_j)/q,  |B|<=C loglog n.

The xi on the initial null set are iid standard normals. The offset B can be
dependent on them; only its displayed bound is used. Consider EVERY deletion
history obeying the DIRECT coordinate hypothesis

    |xi_j-x| <= min_{l in K}|xi_l-x| + epsilon_n.             (AN)

Assume a deterministic envelope epsilon_n with

    P epsilon_n sqrt(log n) -> 0.                           (T)

In particular the question's sufficiently strong polylogarithmic budget, or
epsilon_n <= P sqrt(log(P+1)/n) times slowly diverging factors preserving (T),
suffices for P<=n^a, fixed a<1/4. No gain-to-coordinate conversion is made.
The result here concerns the large branch P>n^(1/200). Bounded/small P has
no claimed bulk/end geometry in this file; L2's separate small-branch score
argument is still conditional on its own score assumptions.

For each prescribed small constant eta>0, choose fixed K sufficiently large
and m_e=ceil(K loglog n). On an event of probability tending to one,
simultaneously for all histories (AN):

* For m>=m_e the shadow has two finite endpoints a<h<b, its midpoint error
  |a+b-2h|=o(H), and |x|<=eta H, where H is FAC-B L3_event's H.
* Every deleted initial null has distance at most d+o(H) from x, with
  d=min_K|xi-x|. The o(H) is uniform in histories and bulk m.
* At entry m=m_e-1 every survivor has magnitude in [Hbar-w,Hbar], with
  w=2 delta_e+O(P epsilon_n/m_e) and m_e w=o(Hbar).
  The entry imbalance obeys |I|/(m+c)<=eta+o(1).
* If the history continues to obey (AN), those extreme magnitudes persist;
  every deletion at nonzero imbalance is from the majority sign, and
  |I|/(m+c)<=eta+o(1) whenever |I|>=2.

These conclusions supply the geometric hypotheses of L2 section 5 (take eta
smaller than .01, and then n large). N0 is not in the deleted initial set;
its separate FAC-B bound |xi|<=loglog n gives L2's stated N0 envelope.
This does NOT prove that actual moves are deletions, the coordinate coupling,
score comparison, start, or delivery. The argument is submitted as a complete
conditional O1 proof attempt, subject to independent checking.

## 2. Deterministic shadow midpoint recurrence

Use exactly L3's online construction. Let t=M-m, h be the shadow center,
e=h-x, and E_t=max_{r<t}|delta_r| (E_0=0). L3 gives

    |e| <= t epsilon_n/(m+c),
    E_t <= epsilon_n[1+2(M-m-1)/(m+1+c)] <= 3P epsilon_n/m

after a deletion (the last, looser bound suffices). The gap endpoints are the
nearest ORIGINAL retained coordinates on either side of h. Past replacements
lie in its closure; deleted originals lie in [a-E_t,b+E_t]. Infinite endpoints
are allowed in this last statement. Gaps are nested while endpoints exist.

Suppose both sides exist before and after a step. Put L=h-a, R=b-h,
d_h=min(L,R), D=R-L. If j is on the right then its replacement is
v=h+d_h: if it was already nearest it is b, otherwise clipping ends at the
nearest distance among the others. If D>0, the clipping magnitude is at
least D. Consequently right selection implies D<=|delta_t| whenever D>0.
For D<=0 it needs no qualification. The left case is the reflection.

If j is not the right endpoint, right endpoint increment g is zero. If it
is the right endpoint, let b' be its next survivor on that side. Every
original coordinate strictly between b and b' was previously deleted, hence
is <=b+E_t by the OLD shadow certificate. If G is the maximum consecutive
gap of the full original ordered sample, this implies

    0 <= g=b'-b <= E_t+G.

(If b'-b>E_t, take the original predecessor of b'; otherwise it is immediate.)
The shadow update gives exactly

    D' = D+g+2d_h/(q-1).

Since D<=max(0,|delta_t|), its negative part cannot grow under this positive
increment. With E_{t+1}=max(E_t,|delta_t|),

    |D'| <= max(|D|, G+2E_{t+1}+2d_h/(q-1)).                (MID)

Reflection proves the same bound for left selection. In particular there is
NO additive E per step in (MID). This is the replacement for FAC-B L4.1(iv).
The maximal ORIGINAL gap G, not a gap of a resampled virtual configuration,
is the quantity bounded by FAC-B's g_max.

Straddling distinctions matter. The shadow always straddles h by definition;
dist(x,[a,b])<=|e|, but exact straddling of x is not asserted. It can fail:
L3's c=1.5, B=-1, K={-.5,1.5}, epsilon=1, deleting 1.5 gives h'=-.2,
x'=-.6 with survivor -.5. Likewise a<0<b need not hold at every early bulk
step even in the exact path. Section 4 handles gaps on one side of zero;
section 5 proves zero-straddling at end entry.

## 3. Uniform occupancy with no additive log n

Here is the needed probability lemma, with proof. On the FAC-B maximum event
all coordinates have magnitude <=Hbar=O(sqrt(log n)). For dyadic scales
r=2^j m_e up to M, examine all states with r<=m<2r. Take deterministic
U_r=3P epsilon_n/r and enlarge constant factors below when necessary.

For a right endpoint b of ANY shadow certificate, every original coordinate
>b+U_r must be retained. Hence its full-sample upper-tail count is <=2r.
If 8r<M let z_r=Phi_bar^{-1}(8r/M). Binomial Chernoff gives

    Pr(#{xi>z_r}<=2r) <= exp(-c0 r).

Thus simultaneously over these dyadic scales, with failure O(exp(-c0 m_e)),
every such b satisfies b>=z_r-U_r. When 8r>=M take the deterministic domain
to be the full real line. This is a statement about all b, not conditioning
on a history or a selected threshold. There is an identical lower-tail event.

On the restricted domain [z_r-3U_r,Hbar], the normal density is at most
C Hbar r/M. Its probability mass is at most C r/M. To verify these assertions:
when 8r/M>=1/2 they follow from M<=16r; otherwise z_r>=0, z_r<=Hbar,
phi(z_r)<=C(z_r+1)Phi_bar(z_r), and Hbar U_r=o(1) by (T).
Shifting by 3U_r changes density by at most exp(3Hbar U_r+O(U_r^2))
and adds at most C U_r Hbar r/M to the tail mass. If z_r-3U_r<0 the same
bound holds by boundedness of phi and z_r=O(U_r). The case 8r>=M is direct.

Set lambda_n=C Hbar P epsilon_n=o(1). Any interval of length 2U_r
containing k observations and whose leftmost observation is in that domain
has probability, by an ordered leftmost-anchor union bound, at most

    C r lambda_n^(k-1)/(k-1)!.                             (SCAN)

Indeed sum over its M possible anchors, integrate that anchor over a domain
of mass <=Cr/M, and choose the other k-1 indices; each must fall in a right
interval of length 2U_r and probability <=C U_r Hbar r/M. Independence
applies to the ORIGINAL iid sample. Integrate only on the maximum event's
bounded range; this upper bounds its intersection without conditioning.

Apply (SCAN) to k_r=ceil(sqrt(r))+2. Sum over dyadic scales and both tails.
For lambda_n<=1 the summand is <=Cr/(ceil(sqrt(r))+1)!, so its dyadic sum
from r=m_e to infinity tends to zero (factorial decay; the same conclusion
follows by bounding it by C exp(-c sqrt(r) log(r+1))). There is no factor
log n left over from a crude uniform union bound.

The bands [b-U_r,b+U_r] and [a-U_r,a+U_r] have anchors in the enlarged
domains just used. Therefore every eligible endpoint band contains fewer
than k_r observations. Uniformly in all bulk states,

    R_m := |K symmetric_difference {xi<=a or xi>=b}|
         <= 2 k_r = O(sqrt(m)),  R_m/m ->0.               (OCC)

This bound is weaker than fixed occupancy O(1), but is sufficient even at
m=m_e. It uses tail mass O(m), not full-sample density O(P). Only one-sided
endpoint counting and L3 localization are used, so (OCC) is available BEFORE
the center or midpoint estimates. It also implies o(M) sample points in
[-U_{m_e},U_{m_e}]: alternatively a direct binomial bound gives this since
U_{m_e}->0. We include this elementary central-count event below.

## 4. Bulk induction, including one-sided configurations

Intersect FAC-B E3,E5,E6,E7 (with K chosen here), the scan event of section 3,
and the sure distinct-coordinate event. These events have probability 1-o(1).
They are simultaneous in the initial sample; no conditional Gaussian law is
assigned to h. Use G<=g_max=O(loglog n)=o(H), Hbar/H->1,
|B|=O(loglog n), and the usual E5 Top(J) sum/sign bounds. Choose K so their
beta_J=sqrt(2[2log(J+1)+loglog n]/J) is <=eta/16 uniformly for
J>=m_e/2, eventually. Constants can be increased to make this true.

Initially |x_0|=o(H), h_0=x_0, and each sign has an extreme outside h_0.
The initial gap has |D_0|<=G. Induct on deletion steps with both current and
previous counts >=m_e, proving first two-sidedness, then midpoint, then center.

Two-sidedness cannot be lost while the count remains >=m_e. Only deleting a
last endpoint on one side can cause this: the shadow drift cannot cross any
other survivor (L3). Suppose the last left endpoint a is selected. The old
certificate implies min xi>=a-E_t, so by E6

    a <= -H+delta_e+E_t.

The clipping rule implies L-R<=E_{t+1} even if the farther side is selected.
Thus, using the previous center bound and |h-x|<=P epsilon_n/m,

    b >= 2h-a-E_{t+1} >= (1-2eta-o(1))H.

Before this deletion the m-1 other survivors are >=b, while a>=-Hbar.
The ORIGINAL center identity then gives

    x >= [(m-1)(1-2eta-o(1))H-Hbar-|B|]/(m+c)
      >= (1-3eta-o(1))H,

contradicting |x|<=eta H for eta<1/10. The other side is symmetric.

MID and the preceding center bounds now imply uniformly in bulk

    Delta:=|a+b-2h|
      <= max(G, G+6P epsilon_n/m_e
                    +2(Hbar+eta H+P epsilon_n/m_e)/(m_e-1))
      =o(H).                                             (B-MID)

This controls |a+b-2x|<=Delta+2|e|=o(H).

To obtain the center bound when a<0<b, apply the proof of L2 BAL with
R_m from OCC. That proof only needs the center identity and midpoint bound,
not x strictly inside the gap: if x>delta/2, b>|a|, and comparing the negative
counts with Top(J) gives J(1/2-beta_J)<=m+R_m. Also J>=m-R_m>=m_e/2.
Its sum bound gives

    |x| <= max(delta/2,
       [|B|+beta Hbar(m+R_m)/(1/2-beta)+R_m Hbar]/(m+c))
         <= eta H

eventually, by the choice of K. This restates rather than assumes the needed
extension of BAL to centers just outside the shadow gap.

If a>=0, every original xi<-E_t is retained, hence m>=M/3-o(M), using E5
and the central-count event. Deleted negative coordinates have magnitude
<=E_t, so sum_K xi <= sum_all xi+M E_t. E5 at J=M gives
|sum_all xi|<=Hbar sqrt(2M[2log(M+1)+loglog n])=o(MH)
in the large branch. Therefore x<=o(H)+3E_t+o(E_t)=o(H), and
x>=-|e| since h>=a>=0. The b<=0 case is its reflection. This proves the
center bound also when the gap does not straddle ZERO; no false assertion
that every bulk gap does so is necessary.

Finally, for deleted initial nulls, localization and triangle inequalities give

    max_deleted |xi-x| <= max(L,R)+E_t+|e|,
    min_retained |xi-x| >= min(L,R)-|e|,

so the outside-minus-nearest envelope is <=Delta+E_t+2|e|=o(H).
This works even if x is slightly outside (a,b).

## 5. End entry, extreme magnitudes, imbalance, and majority

At entry m=m_e-1 the actual drift identity gives

    |x_entry| <= eta H+(Hbar+eta H)/(m_e-1+c)
               = (eta+o(1))H.

There need not be two shadow sides at entry. With infinite endpoints in the
extended order, however, a<0<b: if a>=0, all xi<-E_entry are retained, forcing
m>=M/3-o(M)>m_e; the same argument excludes b<=0. A missing side is allowed
as a=-infinity or b=+infinity and imposes no survivor restriction there.

Every xi>b+E_entry must be retained. E6 supplies at least m_e positive
coordinates >=H-delta_e. Since only m_e-1 total survivors remain, it follows
that b>=H-delta_e-E_entry (strict/weak endpoints do not change the result;
if necessary argue with a threshold infinitesimally below H-delta_e).
For a finite left endpoint likewise a<=-H+delta_e+E_entry.
Thus every retained coordinate has

    Hbar-w <= |xi| <= Hbar,
    w=2delta_e+E_entry,
    m_e w=O((loglog n)^2/H+P epsilon_n)=o(Hbar).           (EXT)

Subsequent retained sets are subsets, so EXT persists without any further
occupancy or midpoint argument. With I=Nplus-Nminus,

    qx=I Hbar+E',  |E'|<=|B|+m_e w=:e_n=o(Hbar).

The entry bound therefore yields |I_entry|/q_entry<=eta+o(1).
At I>=1, x>=(Hbar-e_n)/q, the nearest positive has distance <=Hbar-x,
and every negative has distance >=Hbar-w+x. Here x lies strictly between
the retained signs, since |qx|<=m Hbar+|B| and c>1 imply
Hbar-|x| >=(c Hbar-|B|)/q>w for all end counts, eventually.
The difference in distances is at least

    2(Hbar-e_n)/q-w > epsilon_n,

uniformly for m<m_e, because m_e w=o(Hbar) and m_e epsilon_n=o(Hbar).
Thus AN forces a majority deletion. Reflect for I<=-1; at I=0 either choice
gives |I'|=1. The elementary inequality
(|I|-1)/(q-1)<=|I|/q for 2<=|I|<=m<q propagates the entry bound whenever
|I|>=2. This is a coordinate-level proof, with no use of gain error.

## 6. Checks and exact remaining obligations

N8_shadow_midpoint.py exhausts deterministic small histories and checks every
permitted step's MID recurrence, L3 containment/width/center discrepancy, and
the full-sample gap bound for endpoint jumps. Larger Gaussian falsification
uses seeds 0--19 and multiple adversarial choices. The companion JSON records
the actual scope and outcomes. Finite checks do not validate the astronomical
asymptotic onset, the scan probability lemma, or uniformity over large histories.

Recorded local run: 40 deterministic configuration/parameter combinations
exhausted without subset memoization, plus 480 Gaussian paths (20 seeds,
sizes 64 and 256, three tolerances, four selection policies). Across 147,555
steps there were 95,099 MID checks and 65,747 endpoint-jump checks, with zero
failures. Maximum positive midpoint and width residuals were zero; the center
bound residual was 1.12e-16. The original center was outside its shadow gap
on 4,350 checked states, reinforcing the need for the straddling distinction
(these include one-sided gaps and large diagnostic tolerances).
N8_verify.py additionally uses exact Fraction arithmetic: all seven steps
of L3's fixed rational witness and 460 synthetic extreme end states passed,
including the direct-coordinate majority test and imbalance inequality.
These synthetic end states check the finite calculation, not random entry.

Review focus: (i) the clipping-side implication used in MID; (ii) the anchor
scan bound with moving tail domains and its dyadic sum; (iii) the induction
order and last-side contradiction; (iv) finite versus infinite entry endpoints.
Exact x-straddling and zero-straddling throughout bulk are deliberately not
conclusions, for the reasons in section 2. The center/outside conclusions do
not require them. No failure of the proposed target is claimed.

If independently verified, the remaining work for XA is still O3--O7 from
R05 (and any score-coupling premises retained from L2). This file does not
discharge them or authorize downstream theorem status. The only assumptions
about tolerance are direct AN and T; L5/L6, gain-derived tolerances, and an
absolute Gram-norm rate are nowhere used.
