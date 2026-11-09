# L3: second independent fuzzy-geometry attempt

**R04: ACCEPT BOTH WITH REQUIRED FIXES; amendments below control the original
wording. No closure of the logarithmic propagation gap.**

Read inputs: XA/lemmas/L2_robust_path_attempt.md and FAC-B/lemmas/L4_path.md
(interval, bulk, end). No reviewers, subagents, W2-FAC-X reads/contact, gain
coupling work, or git operations. Outputs are this file and numerics/N5* only.
Here XA denotes Theory_work/Wave2/W2-FAC-XA.

## 1. Result and precise scope

I prove a deterministic shadow-interval bound

    w_m <= epsilon [1 + 2(p-m-1)/(m+1+s+kappa)]       (1)

after at least one deletion, where p here is the INITIAL NUMBER OF NULLS
(replace it by the ambient p for an upper bound). No Gaussian assumption,
balance assumption, order identity, or small-B assumption is needed for (1).
It controls coordinate width, not exception count. It is polynomial, not the
requested O(epsilon log p). I do NOT establish a polynomial lower bound:
the loss in (1) might be entirely a proof artifact.

There is a small rational counterexample to the sharper deleted-hull invariant
"every surviving point is within epsilon of a deleted-hull endpoint" (§4).
This is NOT a counterexample to O(epsilon log p), or even to a larger constant
times epsilon. Neither the numerics nor this proof settles that question.

## 2. A shadow construction that does not identify deletion orders

Put c=s+kappa>1, K_t the actual retained indices, m=p-t, q_t=m+c, and

    x_t=(B+sum_{K_t} xi)/q_t,
    |xi_j-x_t| <= min_{K_t}|xi-x_t|+epsilon.

The actual identity is x_{t+1}=x_t-(xi_j-x_t)/(q_t-1).
Construct a shadow center h_0=x_0 and, at each step, a replacement
v_t=xi_j+delta_t for the point being deleted. Other retained coordinates are
never modified. Set d_other=min_{i in K_t\{j}}|xi_i-h_t|. If j is already
nearest to h_t take delta_t=0. Otherwise move xi_j straight toward h_t until
its distance is d_other. Thus v_t is an exact nearest point in the temporary
configuration consisting of v_t and the other ORIGINAL retained coordinates.
Define

    h_{t+1}=h_t-(v_t-h_t)/(q_t-1).

This is an online auxiliary construction, NOT an exact reference path on a
single preselected perturbed Gaussian sample. In particular do not apply
FAC-B's Gaussian events or its mean-balance identity to h_t.

Let e_t=h_t-x_t. Triangle inequalities give

    |delta_t| <= epsilon+2|e_t|.                    (2)

Indeed the selected distance to h_t is at most d_actual+epsilon+|e_t|,
while d_other >= d_actual-|e_t|. In the case e_t>=0 and delta_t<0, a stronger
bound holds: |delta_t|<=epsilon. Indeed xi_j>=h_t>=x_t. Then
|xi_j-h_t|=|xi_j-x_t|-e_t and d_other>=d_actual-e_t. Reflect for e_t<=0.

The exact update and bounds are

    e_{t+1}=(q_t e_t-delta_t)/(q_t-1),
    (q_t-1)|e_{t+1}| <= q_t|e_t|+epsilon,
    |e_t| <= t epsilon/q_t.                         (3)

For completeness, if e_t>=0 and delta_t>=0, (2) implies
q_t e_t-delta_t >= (q_t-2)e_t-epsilon >= -epsilon,
while its upper bound is q_t e_t. If delta_t<0 use |delta_t|<=epsilon.
Reflection proves the other sign. Induct q_t|e_t|<=t epsilon. This uses
q_t>2 at every step with another point surviving, since c>1.

**Shadow interval certificate.** At every t with a survivor, all past v_r
lie in the CLOSED gap between the nearest retained original coordinates on
either side of h_t (allow infinite endpoints); no retained original coordinate
is in the OPEN gap.

Proof: initially the statement about past v's is empty. Replacing the selected
coordinate by its clipped version v_t places it in the closure of the current
gap. Every other retained coordinate has distance at least |v_t-h_t|.
The shadow drift has magnitude |v_t-h_t|/(q_t-1), strictly smaller than that
distance, so it cannot cross another retained point. Removing the original j
can only enlarge the gap. It contains the previous closed gap and v_t. The
same reasoning handles a one-sided gap. Ties are allowed at endpoints; one
must use closed containment rather than claim a strict interval identity.

At the terminal step with one point no geometry is required. This argument
uses exact-nearest only on each temporary configuration and its explicit
shadow drift, not on the actual deletion sequence.

Let a,b be these shadow-gap endpoints. Every retained original coordinate is
outside (a,b). Every deleted original coordinate is within

    E_t=max_{r<t}|delta_r|

of [a,b], because its replacement lies there. Consequently, relative to the
original finite coordinate set, K_t differs from the two tails
{xi<=a or xi>=b} only within width-E_t bands about the FINITE endpoints.
Infinite endpoints impose no band. Endpoint equalities are harmless and are
included in the bands. From (2),(3), r<=t-1 and q_r>=m+1+c yield (1).
This is a genuine geometry result for every permitted approximate path.

**Limitations:** a,b need not straddle zero. There is no BAL premise
|a+b-2x_t| small here, no occupancy estimate, and no entry concentration or
entry-majority conclusion. Shadow h_t need not equal a center computed from
the retained original coordinates. Thus (1) alone cannot be substituted for
the entire L2 geometry hypothesis.

## 3. What the center-crossing argument really proves

If deleting y makes x cross a surviving z on the opposite side, write
u=|x-z|. Since the selected distance is <=u+epsilon, crossing requires

    u <= (u+epsilon)/(q-1), hence u<=epsilon/(q-2).

The crossing step also has |x'-x|<=epsilon/(q-2). A crossing example is
c=1.5, m=2, epsilon=1, z=-.5, y=1.5, B=-1, giving x=0 and x'=-.6.
The distance excess is exactly 1 and the survivor is crossed.

Summing only these crossing-step displacements gives a harmonic quantity.
It DOES NOT bound the whole displacement between crossings or the locations
of deleted hull endpoints. A proof that charges all boundary-band growth to
these crossing displacements is still missing. In particular the nearest
boundary can change identity at a crossing; its jump is not the center's
O(epsilon/q) displacement. Equations (2),(3) show exactly where the shadow
argument instead loses a factor p/m. They do not prove that this loss occurs
in the actual retained-set geometry.

## 4. Deterministic small cases and local falsification

Take c=1.5, B=0, epsilon=.5 and the ordered coordinates

    [-1.78,-.78,-.53,-.09,-.05,.28,.43,.57,.67,1.52].

Delete zero-based indices [2,3,8,7,5,6,1]. The distance excesses over the
current exact nearest distance are, respectively,

    [.48, .04, .44, .48, .33, .48, .43] (rounded).

These can also be checked directly with rational arithmetic; each is strictly
below .5. Survivors are indices [0,4,9]. The deleted hull is [-.78,.67]; the
survivor -.05 has depths .73 and .72 from its endpoints. Thus hull depth .72
exceeds epsilon=.5. This refutes hull depth<=epsilon. For the ONE-SIDED outer
band certificate below it also forces width >=.72=1.44epsilon, refuting a
constant-1 bound. Half-depth pertains to a different symmetric-band definition.
Neither refutes C epsilon with unspecified C, or O(epsilon log p).
Scaling all coordinates and epsilon preserves the example
with arbitrarily small tolerance and still B=0. Small neighborhoods retain
the strict eligibility inequalities, so the phenomenon is compatible with
fixed Gaussian coordinates; it is not a high-probability asymptotic refutation.

numerics/N5_fuzzy.py uses only the standard library and seeds 0,...,19.
It exhausts reachable SUBSETS (keeping one witness path per subset, sufficient
because center and eligibility depend only on the subset) for 16 deterministic
instances of size <=9 and 60 Gaussian instances of size 10. It also runs 240
size-512 Gaussian paths: three epsilons and four selection policies per seed.
The hull policy greedily maximizes the next hull depth; this is not an
exhaustive large-p adversary. Results in N5_fuzzy_results.json:

* deterministic maximum hull-depth/epsilon: 1.0000000000000002;
* size-10 Gaussian maximum: 1.4373876890351853;
* size-512 sampled maximum: 0.9999609795931377.

The worst size-10 witness is seed 13, epsilon=.5, with the same index path
as above and unrounded Gaussian values; N5_fuzzy_trace.json records every
center, nearest distance and selected excess (maximum .4830264442).
These finite searches are falsification only, do not estimate a probability
of universal success, and do not test the full FAC-B E_n event, gains, or a
logarithmic asymptotic scaling. No failure of O(epsilon log p) was found.

N5_verify.py separately verifies the rational witness with Fraction arithmetic
and checks 256 shadow steps along the stored small-instance witness paths.
All checks passed (N5_verify_results.json); this checks the construction on
those histories, not every possible shadow history. The rational excesses are
exactly [12/25,1/25,417/950,202/425,33/100,12/25,477/1100].

## 5. Rate accounting and remaining gap

For squared-distance excess tau, |xi_j-x|<=d+sqrt(tau), so every deterministic
bound above applies with epsilon=sqrt(tau). This reduction can be loose when
d is large; no uniform division by d is legitimate near zero.

Under the candidate zeta ~ p^2 polylog(n)/sqrt(n), epsilon ~ sqrt(zeta)
has scale p polylog(n)/n^(1/4). At m_e=O(loglog n), (1) gives

    w_m_e = O(p^2 polylog(n)/(m_e n^(1/4))).

To make even m_e*w_m_e=o(H) via THIS upper bound would require the polynomial
condition a<1/8 (with additional logarithmic bookkeeping). This is a loss in
the present sufficient estimate, NOT an impossibility theorem for a>=1/8,
nor a proof of the full L2 hypotheses even for a<1/8. Occupancy, balanced
fronts, straddling, and extreme-tail entry are additional unproved steps.

In contrast, O(epsilon log p) would leave only logarithmic overhead and the
polynomial threshold a<1/4 intact. This attempt neither proves that bound nor
gives a counterexample to it. The specific open task is to control band growth
between center crossings (or replace the shadow estimate by one that avoids
the q_t|e_t|<=t epsilon accumulation) AND then derive balanced bulk geometry
and entry from it. L2's conditional theorem remains conditional. No claim of
XA closure, of a necessary polynomial rate loss, or of failure of entry
majority is made.

## R04 definition and scope supplement (controlling)
Standing hypotheses: deletion-only null path, retained truths, CONSTANT offset,
the approximate-nearest rule at each step, c=s0+kappa>1. Statistical application
is only via the scalar exact-CS reference recursion; no C2/general-covariance
application is claimed. In sections 1–4 p denotes initial null count (m0), B
denotes scalar offset (beta0), s=s0, and K_t denotes retained indices, not the
production size cap. These local symbols do not denote L4's matrix B. Section 5
p is ambient dimension, with m0<=p. This explicit local dictionary resolves the
clashes without changing the already-tested formulas.
Formally w_m:=E_t=max_{r<t}|delta_r|, m=m0-t. It measures the shadow certificate's
ONE-SIDED OUTER bands: retained points lie outside (a,b); deleted points lie
within distance w_m of [a,b], with bands only at finite endpoints. It is not the
minimal possible two-tail width. The exact identity q_t e_t=-sum_{r<t}delta_r
isolates accumulation in this construction.
Section 5 uses H=bar H of L2, H^2=O(log n), and m_e=ceil(K loglog n), fixed K.
Gain conversion: L2 AA gives squared-distance excess <=20zeta if c_gain>=1/4,
d_min^2<=nu and 0<=zeta<=nu/2, so epsilon=sqrt(20zeta) suffices. Invoking this
requires those bounds and gain coupling; it is not automatic under iid rows.
N5 exhaustive subset runs use c=1.5,beta0=0 and measure hull depth. Additional
certificate-width, shadow-containment and bound-(1) tests are supplied in
reviews/R04_scratch/R04_l3_adversary.py and its output, incorporated by reference.
Those finite checks neither prove logarithmic width nor close the geometry gap.
