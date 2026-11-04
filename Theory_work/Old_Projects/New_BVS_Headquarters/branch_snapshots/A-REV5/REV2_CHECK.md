# Independent REV2 / W6-FIXREV2 check

2026-11-02. Overall verdict: **GAP** for the complete package; the central repaired deterministic statements are **VERIFIED** with the qualifications below. These are review verdicts, not changes to candidate, sketch, conjecture, conditional, locked, or adoption status.

Read-only source review; no simulations or numerical workloads were run locally or remotely for this check. Numerical values below are source-reported evidence, not independently recomputed values. Algebraic counterexamples and implications were checked directly. Read A-REV2 REVIEW in full, W6 REPORT/STATEMENTS/NOTES, and the relevant downstream proof passages. Branch heads: A-REV2 `09dc2307b3b4a133765877239d5cd2149c25cd89`; W6-FIXREV2 `be2d4568bca74dec2ae6dd08e25fe709c3da44f6`; W3-PGD `fdeaec34f5a23ced83ccd85b5bf00ee643cbcba0`; W3-PXN `4aebea3bf003f5f3c0c7239a24c824ec2d2aa574`; W2-T26 `0e4f1e7f5efd1e67330affa4168b69750eaff2f1`; F-REFINE `db708ca9f98a616ea16c8ce8e950d8f65238835f`.

## Every original verdict

S03, S37, SEX, SU and V03/V37/VEX have A-REV2's source meanings. “W6 repair” means its STATEMENTS, not an edit to those source branches.

| Original claim/finding | Independent verdict and W6 disposition |
|---|---|
| S03 E1(a–d) | **VERIFIED**: exact size-marginal recurrence `(p-k)/(2p-1-k)` and tail bounds; retain the lower-bound range. |
| S03 E2(i–iii) | **VERIFIED** with the stated nonempty-truth restrictions and null-truth exception. |
| E3 proof barrier | **VERIFIED** for its numerator/denominator envelope and exact-tail cutoff; no universal posterior lower bound follows. W6 preserves this boundary. |
| den-prime / T02(i-sharp) | **VERIFIED**: ratio is the full prior size-tail mass divided by the truth's individual prior weight. The probability bound is `sup_m P`, and only deterministic cutoff sequences are discharged. |
| Lemmas I/B / T02(ii-sharp) | **VERIFIED** with fixed positive unnormalised `g0`; no claim for arbitrary vanishing `g0,n`. |
| T03-sharp C1–C10 and (i–v) | **VERIFIED** under the named SE/BM conditions. Large unions need the weak determinant bound; normalized conditioning is on the smaller truth model. Convergence of expected posterior error follows from boundedness; an expectation rate does not. |
| S03 Proposition D | **VERIFIED** as a G/R duplicate-column counterexample outside size-two SE; it does not contradict T03-sharp. |
| S03 onset near 1.2e5 | **ERROR**. The geometric-series parameter is still far above 1/2 there. W6 correctly distinguishes its roughly 2.1/2.5 million crossing from the roughly 25.6/29.8 million optional fixed-constant crossing; see residual wording defect below. |
| S37 Proposition 1 / swap identity | **VERIFIED**: at a one-extra/one-missing state the literal TD inequalities require opposite signs for the same score difference. Strict TD for d>=1 is inconsistent. Null equality requires nondegeneracy. |
| Lemma 0(a), (c) | **VERIFIED** for strict ascent and certification from the running pre-search HPM, with the ledger tie qualification. A-REV2's table phrase “initial centre already is truth is trivial success” is **ERROR** if success means final reported truth; see disagreement 1. |
| Lemma 0(b) posterior-miss inference | **ERROR**: a below-truth centre can climb to an above-truth superset. W6's delivery inclusion is **VERIFIED**. |
| V37 R2 dichotomy | **ERROR**: a below-truth inferior local optimum is neither original category. W6's pre/post-ledger three-way partition is **VERIFIED**, restricted to failed fits when naming posterior/search misses. |
| A1–A4 core theorem | **VERIFIED** with finite region, closure, all-start versus one-start quantifiers, feasible moves, and adequate cap. W6's exact certified-return condition `ell>=tau` follows from the extra scan. |
| A5 without POS | **ERROR**: in the suppressor design `mu=3x1-2.8x2`, correlation .95, both best one-variable gains may be negative while the two-variable truth improves. Literal dominance ranks neighbors but does not imply improvement. POS-repaired implication **VERIFIED**. |
| TD-P implies TD-infinity / nonconverse | **VERIFIED** for progress-closed regions. A combination proxy can make the first move nonprogress yet eventual ascent reaches truth. |
| TD-P iff strict D-events | **ERROR** deterministically: duplicate singleton scores tie, lex chooses truth, and strict separation fails. W6's tie-aware equivalence **VERIFIED**. |
| “weakest among at-most-Phi-move conditions” | **ERROR**: a neutral move can be paid for by a later extra-to-truth swap reducing Phi by two. Per-move necessity is **VERIFIED**; total-length necessity is not. |
| Theorem B inclusion / C extensions | **VERIFIED** / **GAP** respectively. A selected centre cannot justify unconditional counting by its realized lattice size. The Gaussian tail must retain the original threshold t, not excess u after subtracting `2 log p`. |
| SEX EXP-prime identity/bound | **VERIFIED** for fixed-X actual blocks, bounded block size, polynomial family and within-block SE. Conditioning on X fixes the blocks and preserves independent Gaussian observation noise. |
| SEX/SU kappa limit .52/c | **ERROR**: the exact limit is `.51/c`; `.52/c+o(1)` is a looser bound. W6 correction **VERIFIED**, including strict decrease for fixed phi. |
| VEX R1 certificate | **VERIFIED** deterministically from positive full-block RSS and realized within-block SE; no probability event is required. |
| SEX Theorem 3 | **VERIFIED** for a deterministic fixed-length chain; exact normality of each raw projection does not extend automatically to a response-selected chain. |
| SEX Theorem 4 | **VERIFIED** with normalized H3 and fixed bounded leakage. The prior and normalized-start telescope is exact; independence of remainders is unnecessary. |
| Growing leakage bound / iff gloss | Bound **VERIFIED**, iff **ERROR**. Zero actual leakage satisfies both CL(0) and an arbitrarily loose growing envelope. A chosen upper envelope cannot provide a necessary threshold. W6 sufficiency repair **VERIFIED**. |
| Lemma U expansion and events on declared family | **VERIFIED** after endpoint/auxiliary sets are budgeted. Union-with-truth projection rank is at most k+s0; no SE for that projection union is needed. |
| Lemma U “every V used below” | **GAP** without a budget: n-1 orthogonal singletons have maximal independent noise energy asymptotic to `2 log n`, exceeding `.5 log n`, despite a one-pair original family. W6 explicit H-budget repair **VERIFIED** asymptotically. |
| C3 upper ceiling | **VERIFIED** under zero increment leakage alone: a residual lower floor suffices. |
| C3 matching lower floor | **ERROR** under zero leakage alone: take orthogonal signal x1 omitted by T=empty and add null x2. RSS doubles, giving limiting improvement `Z²/4` instead of `Z²/2`. The difference exceeds any fixed remainder allowance for a fixed positive Gaussian-tail probability. W6 floor with `mu in span(X_T)` is **VERIFIED**. |
| Random-design / adaptive-packing extensions | **GAP** beyond the restricted surrogate regime; sketch status retained. The .15 universal covariance floor is false for .9 equicorrelation (minimum .1). A normalized Gaussian direction is spherical, not exactly Gaussian; second moments suffice for tightness of the masked projection. |

## Claude disagreements and new statements

1. **VERIFIED disagreement about starting at truth.** A-REV2's detailed text correctly says no *new delivery* is needed, but its verdict-table shorthand “trivial success” is too strong. If an addition to truth improves F, the final search updates the ledger above truth, even with move cap zero because the extra scan scores the improving neighbor. Thus starting at truth alone ensures neither certification nor final reported truth. W6's local-optimum condition is correct. No change to A-REV2's strict-ascent or certification proof follows.

2. **VERIFIED Lemma NT qualification.** On the centered response sphere, identically equal scores imply `A_T'-k A_T''=alpha C`. Rank less than n-1 forces alpha=0, then k=1. Positive definite H makes `col(A_T)=col(X_T)`; equal column spaces contradict full rank of the union for distinct sets. The analytic zero-set argument then proves null ties. In the final rank sentence choose the smaller of the two distinct sets if one contains the other; the displayed inequality using T' alone need not hold for a larger containing T'. This is a proof-writing repair, not a counterexample. Corollary NT requires its nondegeneracy at every comparison used. Gaussian noise alone does not eliminate structural ties. W6 does not rescue the original deterministic iff without these extra hypotheses.

3. **VERIFIED C3 probability qualification**, but small probability does not repair an eventwise statement or asymptotic high-probability assertion. The omitted-signal example has a fixed positive limiting failure probability. W6's weak general floor C3-low-prime is **VERIFIED**: `-nu log(1-x)>=nu x`, `nu>=n/2`, and `RSS_T<=C_R n` give exponent `sigma² Z²/(2C_R)`. The sharper fully-explained-signal floor uses `RSS_T<=||C eps||²` as required.

4. **VERIFIED Prop. F** for failed completed fits. F_post>=F_pre yields the exhaustive partition immediately, and the cap's returned/scored neighbor must be included. I=E_LS-complement because previously scored truth forces F_pre>=F(truth). The claim about study fits remains **GAP/OPEN** until actual per-fit F_pre and truth scores are inspected. A source report saying all final misses are posterior misses does not identify which were blocked before local search.

## Residual defects in W6 wording

- **ERROR (typographical probability limit), STATEMENTS 4.1:** the displayed lower bound `1 - o(1)` is followed by `→0`; it tends to **1**. Its union-bound constants otherwise safely dominate the two projection-family bounds and Chebyshev failure probability, for nonnegative polynomial exponent a_H and sufficiently large n. State the usual `a_H>=0` and “for sufficiently large n”; small n can have negative vartheta-prime denominators and the remainder floor proof explicitly uses eventual conditions.
- **ERROR (overbroad onset sentence), STATEMENTS 1.2:** the proposed replacement says the proof's “own deterministic thresholds (as written) hold only from” roughly two million, yet the same paragraph lists the fixed c_q threshold beyond twenty-five million. Say specifically “the geometric-series condition first holds near ...; the optional displayed fixed-constant bound requires ...”. None of these named thresholds supplies a universal theorem onset.
- **ERROR (exact combinatorial equality), STATEMENTS 2.6:** the displayed count of states missing truth omits the feasibility cap. It is an upper bound in general, and an equality only when all counted sizes are feasible (eventually true for fixed s0,d as n grows). For example K=s0=2,a=1,d=2, a state with one retained truth and two extras is counted but excluded. Use `<=` or impose `s0+d<=K`. Similarly interpret Lat(S) as its feasible part when asserting `Lat(S) subset R_{a,d}`; its literal displayed definition can include infeasible truth-plus-extra supersets. The actual progress path remains feasible and the sufficient event can be imposed only on feasible lattice states.
- **Scope qualification:** Prop. F's explanatory phrase “the three conditions ... partition all fits” must read “all failed fits” when II is identified with a failure classification; the inequalities themselves partition all fits, including successful fits in I/III. The proposition's opening failed-fit restriction makes its mathematical use correct.

## Downstream use and locked methodology

Checked the locked register's T01/T02 v3, T03 v2, T22(iii) v2 and T27(i) v3 dependencies and the methodology score/start/search contract. The repaired statements use nu=n/2+.01, standardized response energy n-1, random contrast prior rate b0*s_y², capped normalized start mass, and full-response block tables. None supplies VIS, leakage-average, H3 or sampler discovery merely by proving EXP-prime.

The production `v3_engine.h::local_search` freezes each center during all feasible flips/swaps, uses plain lex neighbor ties and strict improvement, and after ell moves scans again, returning the improving neighbor with local_limit. Every scan evaluates into the ledger. `v3_core.cpp` saves hpm_before immediately before its final search from led.hpmS; this supports the proposed audit extraction, not a conclusion about unavailable per-fit values.

| Downstream source | Verdict on the reviewed dependence |
|---|---|
| W3-PGD | **VERIFIED implication only:** its strict D-event definition is stronger than tie-aware TD-P, so proving it still proves repair. P4 proves strict score reversal, and C-LD makes the current state strictly beat every progress deletion; these also refute tie-aware progress. Rename the strict event, and qualify its “ties null under G” sentence by nondegeneracy. This does not independently verify the whole Theorem W campaign. |
| W3-PXN 9.1 | **ERROR** in the asserted `nu(1.02+1/(n phi²))/(c_* n)<=1`: c_*<=1/16 makes its limit at least 8.16. Replace 1 by an adequately large fixed constant, absorbing it into kappa2. The O(1) conclusion and strict population-margin uses survive this repair. Its small-set family is explicitly polynomial and budgeted. P6 uses strict D sufficient events and its truth-addition comparison uses fully explained signal, so the C3 defect does not invalidate those uses. Whole-branch claims retain their existing review status. |
| W2-PREM 3.4 / 6.3 | **VERIFIED relevant uses:** the matching lower floor in 3.4 is at a truth superset, satisfying the repair. TL-sharp 6.3 uses the upper zero-leakage bound, valid even when signal remains omitted. |
| W2-T26 Theorem B | **VERIFIED relevant import boundary:** uses locked T03 and strict EXP-prime as an O_P(1) remainder; no dependence on false T37 or C3 floors or exact .52 limit. Its composition remains conditional on actual-partition start-concentration premises; its ORTH construction remains a sketch. |
| F-REFINE CARDS | **ERROR**: Card 4 retains the invalid R2 exhaustive dichotomy and a delivery event stated as necessary even for previously scored truth. Replace by W6 Lemma 0(b-prime)/Prop. F with ties and failed-fit scope. Card 1 already displays the sup_m probability quantifier, contrary to W6 REPORT's claim it omits it; no need to add a duplicate. Make fixed g0 and posterior/global-HPM scope explicit. Card 3 retains deterministic chain and H3. Source candidate/sketch labels must remain. |

No locked or source file was changed. Numerical reproduction claims in W6 were not treated as new independently executed evidence in this review.
