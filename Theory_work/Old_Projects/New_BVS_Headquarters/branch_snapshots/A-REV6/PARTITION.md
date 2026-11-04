# A-REV6 partition and LH-iid repair review

This is an independent textual review of the fetched origin snapshots below. No simulations or numerical workloads were run locally or remotely for this subreview; numbers are inspected saved outputs, not reproductions. All results remain candidates, unadopted. Original A-REV3 verdicts are preserved separately from checks of later repairs. The parent task's no-commit instruction overrides the campaign's commit/push default.

## Frozen sources

| Source | Commit SHA |
|---|---|
| origin/theory/A-REV3 | `522d83df6d5848fecba401343e99553f2ea03a74` |
| origin/theory/W3-PXN | `4aebea3bf003f5f3c0c7239a24c824ec2d2aa574` |
| origin/theory/W5-VMASK | `4e41b974e0b8f954eb6adaf6be76d351821fdab0` |
| origin/theory/W7-PART | `b2aa940b6d1212c01448fcc4ff1c8851d2bce74b` |

Principal texts: W3 `PROOF.md` §§0–12; A-REV3 `REVIEW.md`; W5 `REPAIRS.md` R1–R7 and `REPORT.md`; W7 `PROOF.md` and `REPORT.md`. The reviewed `Scripts/SMC_BVS/core/cpp/v3_blocks.h` has git blob SHA `9667333ce0142133c386fd5916abd17851b9e109` both in W7 and this checkout. Read campaign `PROTOCOL.md`, `Docs/THEORY_PRIORITIES.md`, and task `W7-PART.md`. No repository-root AGENTS.md exists in this checkout; the user's supplied instructions apply.

## Disposition

| Claim | A-REV3 original verdict | Later repair check |
|---|---|---|
| W3 P1 random partition on restricted LH-iid | VERIFIED, given cited C1 | W7 B supplies a valid explicit margin route under the same size separation; candidate dependence on the cited exact correlation density remains. |
| W3 P6 uniform lattice repair | GAP | W5 R2 fixes the false numerical constant. W5 does not explicitly fix Lemma Lambda(a)'s Tr(c) dimension/cardinality mismatch. Original GAP remains. |
| W3 P7 no-tweak pilot route | GAP | W5 R1 genuinely supplies the missing cap/peeling argument and sums the tail. Its remaining bounded-dimension extension must be stated. Original GAP remains. |
| W3 P8 posterior transfer | VERIFIED | No partition repair changes the diagonal-sequence reasoning; retain T03 and joint-family hypotheses. |
| W7 Theorem B | Not present | Checked margin proof and explicit exponential bound; viable candidate on SIZE, independent of the stronger Theorem C. |
| W7 Lemma 3 as literally stated | Not present | ERROR: conditioning on the full direction vectors makes cross correlations deterministic. Corrected Gram-conditioning version is valid. |
| W7 Theorem C / Corollary C | Not present | GAP as written through Lemma 3; the corrected conditional statement repairs the proof without changing its formulas. No numerical rerun claimed. |
| Study groups of five / multiple groups per block | Outside original P1 scope | OPEN: recovering unions of groups does not identify which groups share a block or supply the required statistical law after selection. |

## What the actual partition permits

The C++ reads `Data::G` only, forms correlations, performs complete linkage on `1-abs(r)`, applies the union-lex tie rule, cuts top down at capacity B, and next-fit packs whole retained clusters. It never reads y. Thus its recovery event is X-measurable and independent of the observation noise epsilon when X and epsilon are independent. This does **not** make a selected block independent of its constituent columns or of y=X theta+epsilon.

Under a strict separation of every within-group absolute sample correlation from every cross-group one, every group completes before a cross merge. If `g_max <= B < 2 g_min`, the cut retains precisely the groups and packing cannot combine them. The study has B=14 at n=200; equal groups must therefore have 8<=g<=14. Asymptotically B=16 and the admissible fixed range is 9<=g<=16. W3's LH-iid family states this restriction explicitly. Groups of five do not belong to it.

W7 Theorem B uses a threshold t between the maximum population cross correlation psi_bar and the minimum within correlation rho. A union bound over within lower tails and cross upper tails yields its exact-law inequality. The absolute sample-correlation law is monotone in the absolute population correlation: the noncentral-t mixture proof is correct. The stated density bound factors into Lambda_r(x)^((n-4)/2), uses its monotonicity on either side of r, and bounds the remaining prefactor. At the equal-rate t*, both terms have exponent I*. The resulting bound

`P(fail) <= [2/(sqrt(pi)(1-rho))] p^2 sqrt(n) exp(-(n-4) I*)`

therefore supports the polynomial-p asymptotic statement. The fixed positive population gap is essential; a shrinking gap needs a new rate condition. This proof can bypass all of W7 A0–A2 and Lemma 3 by using the direct elementary margin argument above. The exact density remains a cited mathematical input, rather than something established by integration checks.

## W7 errors and needed precision

**Lemma 3 conditioning.** The text defines U_h and U_h' to be all normalized column vectors and then asserts a Haar law conditionally on `(U_h,U_h')`. For fixed values of those vectors, the cross Gram matrix is already known. Its first conditional-law statement and the following claim for arbitrary unit w measurable in those vectors are false. Rotation invariance proves an equality in distribution before conditioning, which is not the stated conditional equality.

The needed repair is precise: condition on U_h and the within-group Gram matrix R_h', or on both within-group Gram matrices and choose a representative of U_h. Independent Gaussian groups have independent uniform relative orientation in the centered observation space. For fixed k in h', its direction is then uniform relative to U_h; the one-pair tail is H0(s). Thresholds and node sets in Theorem C depend only on the within-group matrices, so this corrected statement suffices for the conditional union bound and the subsequent peeling. It does not hold for linked LH pairs, which W7 correctly separates as dependent pairs.

**A0(c) scope.** Before the first bad merge, two already completed groups may have merged into a full union. Their roots are no longer current clusters, although A0(c)'s inequalities with parent height infinity include them. State A0(c) only for a group not already absorbed in a full union, or replace 'current' by the appropriate internal cut description. The first-bad-merge proof uses only groups containing partial current clusters and remains valid with this restriction. A2's extra no-early-full-merge hypothesis addresses the same issue for its converse. Theorem B does not need A0(c).

**CE2 scope.** The deterministic next-fit claim is justified for equal-sized groups with 2g<=B. The displayed broader condition `2 g_min<=B` alone does not force failure for unequal groups: take two groups of sizes 2 and 5 with B=5. Under separation, the cut retains them individually and next-fit cannot combine them. Do not quote the broad unequal-size header as a theorem. The equal-g=5 study example and the union-of-groups sufficient statement remain unaffected.

**Finite-n claims.** The inspected saved port output reports engine/faithful/scipy agreement in 70/70 cases. W7 `sim_partition.txt` reports 0/2000 failures for independent g=10, rho=.7, n=200,p=500; the saved analytic table gives approximately 5.658e-9 and 2.286e-8 for p=500 and 1000 after the corrected Gram-conditioning proof. Those are bounds evaluated numerically, not observed frequencies. The LH linked-pair rigorous bound is about .17, whereas 1.5e-4 is a reported Monte Carlo confidence upper limit. Neither label should be interchanged. The g=8 and g=14 simulations use p adjusted to complete groups (496/490 or 1000/994), as the report table notes. The exponent mesh bookkeeping is explicitly PROOF SKETCH and stays so.

## P6 and P7: what W5 repairs actually establish

**P6.** A-REV3 identified two separate defects: the false U1 constant and the invocation of Tr(c) on the family of every set of size at most s0+2. W5 R2 replaces the first by an O(1) constant, which is sufficient against positive linear score margins. R5 qualifies the overstated sharpness claim; R7 adds the emitted-center cost. These repairs check out.

The original Tr statement assumes j<=16, u<=16 and at most `n^(A+1) 2^17` variables. Lambda(a) instead ranges over about `p^(s0+2)` sets and allows j=|A0| as large as s0+2. W5's verification of the general-set EXP lemmas is useful but does not explicitly generalize this distinct Beta-tail lemma. Its report calls Lambda and P6 VERIFIED without recording this mismatch. Preserve A-REV3's original GAP.

A concrete repair is to state the tail lemma for any fixed dimension upper bound J and any family of at most C n^D variables, with bounded u as well, and take t_n=C1 log n with C1>4(D+2). The same chi-square argument has fixed-dimensional numerator tails of order `exp(-t_n/4+O(sqrt(t_n)))`; the denominator failure is exponentially small in n. For P6 take J and the u bound large enough for s0+2, D=A(s0+2), and retain only o(n) projection loss. This is a repair argument, not a retroactive change to W3 or W5's status. Also restrict the strict population comparison to nonprogress neighbours: another missing-hub addition may tie, which does not obstruct lattice progress.

**P7.** W5 R1 closes substantial gaps that were genuinely absent in W3. Its E1 injection handles images above K by retaining unnormalized weights through K+s. Its generating-function domination bounds the k-tail geometrically and sums it before multiplying by H0=O(p). Choosing k0+1>2A gives `p q^(k0+1)=o_P(1)`. E2 separately pays the 1/p size-prior factor for masked-block entries. A generic o_P(1) bad-draw probability would not suffice; this stronger reasoning does.

R6 correctly supplies the neutral block Beta law with extra neutral variables in the conditioning set. Its full-set Beta law has second shape `(n-2-|T|)/2`; W3 P7's `(n-3-s)/2` was off by one half. R3 correctly replaces 1.925 by r*=(11+2sqrt(10))/9. Once every pilot draw lies in the bounded neutral-extension family, telescoping d yields O(log n), below the O(log^2 n) initial threshold.

However R1 Step 2 again calls the original Tr(c), now with u=|T| as large as s+k0 and family exponent A(k0+1). Changing only A does not remove u<=16 or the fixed-dimension restrictions. State the generalized tail lemma above with u bounded by s+k0 and j=1. This is routine but explicit missing bookkeeping for the allowed arbitrary fixed v and A. The R1 argument supports a repaired candidate; it does not justify upgrading original P7's GAP. The c=1 restriction is substantive: D2 requires Gibbs distance one. For c>=2, controlling the initial d-range alone does not deliver truth in one round.

## Downstream boundary

Keep four implications separate: reference start concentration, eligibility of its exact mode, scoring truth by an authorized repair route, and reporting truth when the posterior favours it. On restricted LH-iid the P3/P5 and P8 arguments survive partition recovery; fixed-group Beta laws are established unconditionally and intersected with recovery afterwards. Do not condition those laws on recovery and claim the same distributions.

LS0 remains a method change, including actual center emission into the ledger. A lattice repair from its start mode does not certify production's original center. The repaired c=1 pilot route instead needs D2's exactness, successful calibration, and operational assumptions. Neither branch proves successful completion, removes the no-output event U, proves general masked PIP/evidence consistency, or covers the study's groups-of-five adaptive packing. W7's X-only partition fact does not close that packing-selection obligation.
