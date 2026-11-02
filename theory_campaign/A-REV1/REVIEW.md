# A-REV1 — independent cross-family referee review

Reviewer: GPT-6 Astra; date: 2026-11-02; branch: `theory/A-REV1`.

**The finite Gibbs-path bound survives independent review after the F′ repair. The supplied package is not ready for an unqualified verification: Proposition U, Lemma S's attainment sentence, E3(ii), and Lemma U's printed limit contain errors; the T38 composition needs explicit rate, eligibility, and execution qualifications.** The corrected D2 constant is right. None of these conclusions promotes a candidate to a locked or adopted result, discharges a statistical premise by simulation, or changes a locked file.

## 1. Scope, versions, and verdict convention

The five requested source branches were fetched and pinned before review. Full snapshots, including their original status words and numerical outputs, are under [sources/](sources/); those copies are source evidence, not endorsements. The inspected versions are:

| Source branch | Commit |
|---|---|
| theory/W1-T24G | `9e210a3fafbc074cfbbcae18dafc5c8547e81af1` |
| theory/W2-VT24G | `dba6ff4c12e0510c5a48bf733b1623834aa21c64` |
| theory/W2-PREM | `988c5f55c0fb0fbd6050b6a4d0c75f14159716e3` |
| theory/W1-T38E | `436a7125ace4853eb9d2507513f53db9c47b3825` |
| theory/W3-VT38E | `3e4b732aff517140a124ac1f380410ee95a0d705` |
| theory/W1-EXP, only the imported Lemmas 1.1–1.4 | `722bd18e51fcc3b485c07590097e137dac71a5aa` |

The worktree's governing methodology, C++ directory, and locked-proof directory have no differences from the corresponding files on W1-T24G, W1-T38E, and W2-PREM. Campaign base: `00c7b340622faeb4466c93d92f91c830e4ccdaff`.

**VERIFIED** means the specified implication or step checks under the qualifications in its row. **GAP** means an absent premise, inference, or operational bridge; a repair is given where possible. **ERROR** means a false assertion, with a counterexample or exact calculation below. Verdicts distinguish a theorem's central inequality from ancillary sentences. Existing sketches, conjectures, and open statistical inputs retain their source status.

I checked the requested proofs against `Docs/Methodology/METHODOLOGY_v3.md`, `Docs/Theory/theorems/00_COMMON.md`, the C++ implementation, `Docs/Theory/proofs/LOCKED_PROOFS.md`, the relevant individual statements/proofs, and `COLLECTED_PROOFS_v2.tex`. This is not a new audit of every locked theorem. In particular, the register supplies T03 with its T02 dependency closed in their stated regime; it does not supply H24, terminal delivery, or arbitrary future-completion conditioning.

## 2. Verdict table and overall theorem verdicts

| Claim / step | Verdict | Reason / required qualification |
|---|---|---|
| **Theorem B, restated T24, finite inequality** | **VERIFIED after F′ repair** | Correct potential argument and adapted Bernoulli domination; use the full definition of bad, feasible families, and executed or potential uninterrupted rounds. Empty-phase and nonpositive-c conventions are specified in §4. |
| Lemma F, as a standalone first-failure lemma | VERIFIED | Closure under nonfailure is sufficient; summing the first-failure events is valid. |
| W1's invocation of F in B2's slot argument | GAP, repaired | Nonfailure need not keep the state in the restricted family containing the chosen extra. F′ supplies the required union bound. |
| Lemma F′ | VERIFIED | Conditional probabilities, union bound, and the permutation bijection suffice; no closure is needed. |
| Lemma O(i)–(iii) | VERIFIED | Relative-order symmetry and independent uniform arrival times give all three formulas. |
| Lemma C and the block bound | VERIFIED | Conditional success lower bounds suffice; independence of the actual progress indicators is unnecessary. The block inequality is for integer k≥1. |
| Lemma P, exact formula and single-target polynomial bound | VERIFIED | Coupling until the first change/scoring event and integrating conditional on the target arrival time gives the formula. |
| Lemma P, informal multiple-target sentence | GAP, fixable | It does not specify the revised leakage set and denominator; an explicit valid version is given in §4. |
| **Proposition U, as written** | **ERROR** | Independence moves can remove a truth without raising V or leaving the family. Also, an extra-for-extra swap need not stay in the phase-1 family. §3.1 gives counterexamples. |
| B1, phase-1 progress | VERIFIED | On no bad/no progress, the missing set is unchanged; the selected missing coordinate therefore has the claimed uniform addition bound when its label executes. |
| B2, phase-2 progress | VERIFIED after F′ | The deletion-failure and early-slot-removal events cover no bad/no progress. The independent order bound is valid. |
| c₂≥1/(B+3)−ε_del | VERIFIED | Every proper superset has at least one extra, so H_a≤(B+2)/(B+3). |
| B1′/B2′ scoring refinements in W2-VT24G | VERIFIED with empty-supremum convention | A distance-one Gibbs evaluation scores truth irrespective of the draw. No deletability premise is needed in the one-extra case. |
| Corollary P1 | VERIFIED | Only remaining unchanged until the target Gibbs label is needed; other ways to score truth improve the bound. |
| Corollary B-M | VERIFIED under IND-T | Condition on the entire terminal-start population/past; multiply capped failure bounds for past-selected particles. This does not prove the presence of eligible particles. |
| **IND-T** | **VERIFIED for the uninterrupted process** | State-dependent consumption of a shared iid stream occurs at stopping times, yielding the product transition law. Completion conditioning or globally fresh-score sets are not covered. |
| **Lemma U, finite uniform expansion** | **VERIFIED** | Determinant/Q decomposition and a polynomial-family Gaussian projection bound work beyond blocks. §5 states the necessary family-count convention. |
| Lemma U, κ_n→0.52/c_E | ERROR | Its displayed formula tends to 0.51/c_E. The finite bound and O(1) conclusion are unaffected. |
| CE1, deterministic exit lower bound and finite obstruction | VERIFIED | W2's Lemma E is correct; an independent small BVS example has an exit lower bound above 0.14. |
| CE1, broad asymptotic wording for correlated designs | GAP as a blanket claim | Attraction and retained-truth stability must be checked for a concrete sequence. §5 gives an explicit narrow repair; source sketches are not promoted. |
| W1 §6 premises imply Hη→0 | GAP | In particular, sup of a sum is not the sum of sups used in η. W2-PREM corrects NL0's quantifiers but adds genuine assumptions. |
| **Lemma S, ESS share inequality** | **VERIFIED** | Cauchy–Schwarz proof is correct. |
| Lemma S, “bound is attained by two-level weights” on its full stated domain | ERROR | Positive equality weights require f>1−e for 0<f<1. At f=0.05,e=0.9 the proposed low weight is negative. |
| **Theorem D2 with r*=(11+2√10)/9** | **VERIFIED as a finite uninterrupted-pilot bound** | The ESS floor, weighted share, multinomial count, target-before-dangerous-labels event, and per-particle product are valid. |
| D2-∞ | VERIFIED under its additional uniform hypotheses | Fixed b>0.1, bounded dangerous set, Dep bounded below 1, and vanishing NB failure are required. |
| **Theorem E3, TD′ + eligibility ⇒ LS0 scoring, and (i)/(iii)** | **VERIFIED with centre scoring and completed scans** | Deterministic implication; a mass greater than 1/2 uniquely determines the mode. T27-H3 remains a premise. LS0 is a method extension. |
| **E3(ii), as printed without q<1** | **ERROR** | It drops an explicit hypothesis of locked T22(i-a). A realizable p=2 example gives the displayed “lower bound” ≈1.98×10²³ and actual mass ≈9.44×10⁻¹⁴. |
| E3 computation and scan budget | VERIFIED with accounting clarification | Max-plus block/size DP is exact; at most ℓ+1 scans. Add one initial centre evaluation when counting all LS0 score calls. |
| **T38(b)-R, entire supplied statement** | **GAP** | The central composition inequality and liminf manipulation are valid. Route (b1′) omits asymptotic rate margins; route (b2)'s use of B needs an eligible set and the binomial bound; operational qualification must cover pilot and terminal execution. |
| T38(b)-R, route (b1), direct ELIG+TD′+OP | VERIFIED | Work on Uᶜ and include centre scoring. Do not use the erroneous unrestricted E3(ii) shortcut. |
| T38(b)-R, route (b2), given uniform REPAIR and actual execution | VERIFIED as an implication | Select the smallest eligible index using only the past, then integrate its conditional failure bound. |
| T38(b)-R, repaired formulation in §7 | VERIFIED as a conditional implication | Does not establish DELIV, statistical repair premises, or vanishing operational failures. |

Thus the **overall finite Theorem B verdict is VERIFIED after the existing F′ repair**; its unconditional statistical application remains GAP. The **overall corrected finite D2 verdict is VERIFIED** under its operational idealisation. The **overall E3 package as printed is ERROR because of clause (ii)**, while the core deterministic implication is VERIFIED. The **overall T38(b)-R verdict is GAP**, with a complete conditional repair below. The **overall ESS Lemma S package is ERROR only in its global attainment claim**, not in the inequality D2 uses. The **overall finite Lemma U and IND-T conclusions are VERIFIED** with the qualifications above; U's printed limiting constant is ERROR.

## 3. Errors missed by the prior referees

### 3.1 Proposition U: the full bad-transition definition must be preserved

Source: [W1-T24G PROOF §3](sources/W1-T24G/PROOF.md), lines 145–157. W1 §0 correctly defines a transition as bad if it leaves the family, raises V, **or removes any present truth**. The §3 independence-move “iff” drops the third alternative.

Take S₀={1,2}, x=∅, A=∅ (explicitly allowed as a proof-device choice), c=a=0. The completion family contains every subset of S₀. At W={1}, an independence proposal W′={2} stays in the family and has V(W′)=V(W)=1, but removes truth 1. All feasible start masses and acceptance probabilities are positive, so this transition has positive probability for the actual independence kernel. It is bad under §0 and not bad under §3's claimed equivalence.

The extra-for-extra sentence also needs scope. Let S₀={1}, x=∅, A={2}, c=0, and let variable 3 be junk. At W={2}, swapping 2 for 3 preserves the extra count and V, but leaves the phase-1 family. It is bad. At supersets, where the family contains every extra configuration up to size a, such swaps are neutral; W2-PREM §5.1 itself identifies the incomplete-state obstruction.

**Repair:** define Bad(W) by all three tests from §0, for every label. State that an extra-for-extra swap is neutral only when it stays in the family. The acceptance bound

    sum_{y in Bad(W)} pi0(y) min(1, exp(d(y)-d(W)))
      <= min(pi0(Bad(W)), [pi0(W)/pi(W)] pi(Bad(W)))

remains correct. Apply it to the corrected set. Theorem B already uses the full §0 definition, so these errors do not refute its finite inequality.

### 3.2 ESS share: positivity restricts equality

Source: [W1-T38E PROOF §3](sources/W1-T38E/PROOF.md), and W3-VT38E's unqualified “tight” verification.

Put c=1/e−1. The proposed mean-one low weight is

    w_A = 1 - sqrt(c(1-f)/f).

For 0<f<1 it is positive exactly when f>1−e. At e=0.9 and f=1/20, the asserted share bound is −0.0226483157 and w_A=−0.4529663145. A share of positive weights cannot attain a negative number. At f=1−e the proposed weight is zero and is again excluded by the strict-positive hypothesis.

**Repair:** the inequality holds everywhere, and can be strengthened to

    omega(A) >= max(0, f - sqrt(f(1-f)(1/e-1))).

For 1−e<f<1 equality is attained by the displayed positive two-level weights. For 0<f≤1−e, zero is the infimum and is not attained with strictly positive weights; take weights approaching zero on A and equal weights off A. Handle f=0 and f=1 directly. D2 uses f>0.1 and e=0.9, entirely inside the valid equality range.

The prior referee's correction of 1.925 is also necessary. An exact finite witness uses 77 weights equal to 1 and 40 weights equal to 77/40=1.925. Its ESS/H is 0.89999269486449. Solving 4r/(1+r)²=9/10 for r≥1 gives exactly

    r* = (11 + 2 sqrt(10))/9 = 1.924950591148529...

The user's corrected constant is therefore VERIFIED.

### 3.3 E3(ii): omitted q<1, with an actual BVS counterexample

Source: [W1-T38E PROOF §6.3](sources/W1-T38E/PROOF.md), line 134. Locked `T22_T16_start_aggregation/STATEMENT.md`, claim (i-a), explicitly starts **“If q < 1”**. E3 states the bound and the “whenever this exceeds 1/2” consequence without this requirement. An even exponent s+1 does not make that requirement redundant.

Take n=20,p=2, centred orthogonal columns of squared norm 19, and standardised y=x₂. The method has B=1 and singleton blocks. Let the reference x°={1}, so s=1. The exact table values are r₁≈0.2236068 and r₂≈1.935517816213×10¹². Consequently q=r₂, e=4/r₁≈17.88854, and

    (1-q)^2/(1+e) ≈ 1.983334052945×10^23,
    pi0({1}) ≈ 9.441607620478×10^-14.

The start mode is {2}, not {1}. These are method Bayes factors with the prescribed ridge, IG constants and size prior, not arbitrary positive tables. Strict inequalities persist under small perturbations. The small problem would take the exact production branch; the component start-law claim is nevertheless explicitly mathematical, just as in locked T21. It already refutes the claimed unrestricted aggregation inequality.

**Repair:** insert `0≤q<1` before invoking T22(i-a), and use the actual capped-normalizer reference quantities. E3(i) and (iii) remain valid. This missing condition also applies to any T38 shortcut that tries to establish ELIG through E3(ii).

### 3.4 Lemma U: an arithmetic error in the limiting constant

Source: [W2-PREM PROOF §2](sources/W2-PREM/PROOF.md), lines 135–137, inherited from W1-EXP.

The first summand of κ_n tends to zero; ν/n→1/2 and 1.02+1/(nφ₀²)→1.02. Therefore κ_n→**0.51/c_E**, not 0.52/c_E. For the independent AR example the values are 18.4314 and 18.7928 respectively. Replace the asserted limit; alternatively describe 0.52/c_E as a conservative eventual ceiling. No finite inequality needs to change.

## 4. Theorem B: line-by-line argument and repairs

References: [W1-T24G PROOF §§0–4](sources/W1-T24G/PROOF.md), [W2-VT24G PROOF §§1–2](sources/W2-VT24G/PROOF.md).

1. **Geometry and feasibility.** For a phase-1 state, the number of extras is at most |A|+c=a. A missing-truth addition is feasible under s₀+a≤K and stays in the family. Its potential drops by one, or drops from at least a+1 to at most a at completion. A non-bad transition cannot remove a truth or return from phase 2 to phase 1. These facts establish the pathwise monotonicity used later. They require the full bad definition, not Proposition U's shorthand.
2. **F and F′.** F is valid under closure. F′ follows directly by summing E[1{X_{t−1}∈F} f_{σ(t)}(X_{t−1};σ)], bounding each by its supremum, and using that σ contains each label once. In B, bound the **first** bad step before scoring: prior to that step the path remains in the family. Stop at scoring. This avoids relying on a closure claim after truth has been reached.
3. **B1.** On no bad/no progress, the missing set stays equal to the initial missing set. Fix the coordinate achieving the min of the relevant uniform failure probabilities. Its Gibbs label occurs once. At that execution, the conditional probability of failure is bounded by ε_add. Conditioning on the whole future event is neither needed nor legitimate; use the pre-execution past and event inclusion.
4. **B2 slot bound.** Fix an original extra l. If l is present at G_l, retaining it has probability at most ε_del; otherwise some earlier non-Gibbs neutral step removed it. F′ bounds the latter by h(l). Revealing the complete order at time zero is allowed: step uniforms remain fresh, and P(e precedes G_l)=1/2.
5. **B2 order bound.** If an original extra Gibbs label precedes all non-Gibbs labels, all preceding Gibbs labels leave the original state unchanged on no bad/no progress. Deletion at that label has probability at least 1−ε_del. The failure bound ε_del+(B+2)/(|P|+B+2) is conservative and valid. Taking the better of the slot and order bounds gives H_a.
6. **Adapted domination.** Define J_h=1 on progress, bad, scoring, or an already stopped history. Its conditional success probability is at least c*. On no bad and no score, V stays positive and each J_h=1 lowers V by at least one. Thus at most v−1 such rounds occur. First-bad union bounds give Hη; Lemma C gives the binomial tail. There is no conditioning on the event of no bad steps to manufacture independent Bernoulli trials.
7. **Scoring sharpening.** If the state is distance one, the relevant Gibbs alternative scores S₀ regardless of inclusion/deletion. This validates B1′ and B2′, and P1's stronger one-round event.

**Boundary conventions needed in a polished statement.** For H=0 use the trivial probability bound. For nontruth x, v≥1. If a=0, omit the empty phase-2 family and take c*=c₁; probability suprema over empty sets are zero, including the restricted supremum in B1′. If c*≤0 use the trivial bound 1, or replace c* by max(0,c*) before writing a binomial distribution. An undefined negative binomial parameter is not a “trivial” distribution. For c*>0 define

    beta_H(x) = min(1, P(Bin(H,c*(x)) < v(x)) + H eta(x)).

This is the quantity to carry into composition and product formulas.

**Lemma P.** The exact formula counts the first label that changes state or performs the declared Good scoring operation. Until that moment every label acts at x, so independent frozen-state outcomes are a valid coupling. Integrating over the target arrival time gives the product integral. The polynomial lower bound remains valid when 1−tQ is negative: then its right side is nonpositive and the left side is nonnegative. For a precise multiple-target version, let C be nonempty Good labels with success probabilities at least s_min, let D be disjoint dangerous labels, and set Q=Σ_{j∉C∪D}q_j(x). Then a valid bound is

    P*(x) >= s_min |C|/(|C|+|D|) [1 - Q/(|C|+|D|+1)].

Use the earliest label of C∪D, require it to be Good, and require no outside change before it. Its arrival time has mean 1/(|C|+|D|+1). This supplies the missing denominators in W1's informal sentence.

**Corollary B-M.** Given the data and terminal-start history, the selected particles' uninterrupted extended trajectories are independent under IND-T. Therefore the all-particle no-score event is bounded by ∏ᵢ beta_H(xᵢ). Selection must be past-measurable; choosing particles by later success, diagnostics, or fresh-score counts is excluded. No independence of the initial resampled states is asserted. A bound uniformly below one and a growing eligible count can suffice, but it is an extra delivery condition. The phrase “no η→0 needed” is valid for a fixed H and sufficiently small fixed η; if H grows, beta<1 already requires Hη<1.

**Asymptotic premise gap.** W1 §6 writes NL0 using sup_W Σ_l o_l(W), while η is Σ_l sup_W o_l(W). The latter is generally larger. An array a_l(W_j)=1/p for l=j and zero otherwise has sup_W Σ_l a_l(W)=1/p but Σ_l sup_W a_l(W)=1. Tiny positive off-diagonal entries give the same discrepancy. This is a counterexample to exchanging the quantifiers, not a claim that this abstract array is a BVS instance. W2-PREM §0 correctly redefines NL0 as the sum of suprema. Use that stronger premise or establish a structural comparison. Neither uniform repair on all R_d nor Hη→0 follows from the finite theorem alone.

## 5. IND-T, Lemma U, and CE1

### IND-T and the implementation

`v3_core.cpp::cpp_final_run` seeds final islands with stream numbers 10–13. `v3_engine.h::population_round` processes particles sequentially through a shared island stream. `draw_order` consumes m−1 uniforms; move draws have bounded state-dependent lengths. A new block starts at a stopping time in the consumed-uniform filtration. Under EX-S, the unconsumed tail is iid and independent of that past. Include fixed data and independent calibration in the initial sigma-field. The conditional block kernel depends only on the particle's own current state; multiplying the chronological conditional kernels and grouping by particle proves IND-T.

The global cache/ledger does not affect moves under EX-A. The independent extended output consists of states, logical score evaluations/proposals, and RB records. The set of **globally first-ever fresh evaluations** is not a per-particle independent output: whether a model is fresh depends on earlier particles. This distinction does not affect “truth ever scored.”

At the boundary **after stage T's resampling but before its move round**, H′=L+5 is correct. At the boundary **after the stage-T move round**, only H=L+4 remain. Do not combine H′ with states selected after consuming that extra round. For a pilot, condition on its forward past, not its eventual calibration record.

The proof describes the uninterrupted process. A shared runtime guard or future event can couple actual stopped trajectories. Even independent fair bits become dependent on conditioning that they are equal: P(00 | equal)=1/2, whereas the product of conditional marginal probabilities is 1/4. Thus conditioning on observed completion or diagnostics is not a repair for an abort issue.

### Lemma U

The imported W1-EXP algebra checks: Q_S=RSS_S^y+c_S with 0≤c_S≤1+1/(nφ₀²); the Schur-complement determinant increment differs from log(n+1) by at most (1+φ₀⁻²)/(φ₀²(n−1)); and the residual ratio is unchanged by response standardisation. Substitution gives the stated finite κ_n bound.

For uniformity, union-bound Gaussian projections over the complete deterministic comparison family. If its cardinality is at most Cn^A′ and the projection rank is bounded, L>4A′ suffices for a tail bounded by a constant times n^(A′−L/4). For E2, use span(X_V,X_S₀), whose rank is at most k+s₀; this changes the fixed multiplicative constant, not the exponent. If additional V's “used below” are included, count them too and enlarge A′/L accordingly. For all |V|≤k, the stated choice L=4kA+1 works. A data-dependent family selected using y is not justified by the smaller family's count; use a deterministic envelope. These details repair the compressed wording without weakening the principal expansion.

The floor can be taken directly from locked T10 and is sharper than U's eventwise version. The expansion alone does not establish NL0, TS, IND-M, or the joint statistical compatibility needed for T38. The imported EXP and premise candidates are not newly locked here.

### CE1: a precise obstruction and a narrow asymptotic repair

W2's Lemma E correctly lower-bounds a first **elementary-state exit**, not merely the end-of-round exit. Couple frozen-state label outcomes until the first change. Any earlier unselected null addition is already an exit; suppress all changes from the m missing-truth labels, d existing-extra labels, and B+2 non-Gibbs labels. The retained-truth deletion sum Q_T supplies the remaining product correction. This yields the denominator B+m+d+3 and correction denominator B+m+d+4.

The source's blanket correlated-design sketch still needs its two limits. One explicit way to complete the obstruction is the following separate, narrow construction. Let p_n=ceil(n^(1/3)), S₀={1}, fixed nonzero θ₁, and a centred exact Gram matrix with unit diagonal, corr(x₁,x₂)=r∈(0,1), and all other correlations zero. Such columns exist for large n because p_n≤n−1. The minimum eigenvalue is 1−r, so G,R,SE and BM-∞ hold. Take d=1 and boundary state Y={3}. It has no present truths, so Q_T(Y)=0 exactly. The residual signal gain from adding proxy 2 is r²θ₁²(n−1). Gaussian noise perturbs its square root by O_P(1); Lemma U/C5 gives addition odds at least a polynomial factor times exp(cn), for some c>0. Hence o₂(Y)→1. Lemma E gives

    eta_n >= (1-o_P(1))/(B_n+5) >= (1-o_P(1))/21.

Since L→∞, (L+4)eta_n cannot vanish. This is a complete repair for an explicit sequence, not a universal assertion about every correlated design. It does not promote W1/W2's broader sketches. It also does not refute Theorem B, which charges bad transitions differently; it refutes the vanishing uniform-exit premise on the original R_d.

## 6. D2 and E3 against the method

### Corrected D2

The finite proof is VERIFIED on a dataset satisfying D2-a/b/c and for its potential first pilot stage. The order of its six steps is sound:

1. The initial draws are iid π₀ and scored, giving Hoeffding for the x° fraction.
2. At the first stage the forced floor is exactly 1/T_e. On the corrected range event, weight ratio≤r*, so Kantorovich gives ESS≥0.9H at the floor. ESS decreases with the tilt. `pilot_next_phi` either accepts 1, returns a passing bisection endpoint, or takes this floor. Thus the selected first-stage ESS passes. The later-stage snapping convention is irrelevant here.
3. Lemma S supplies share at least g(b−t)>0 on the good initial-fraction event.
4. Multinomial resampling produces a Bin(H,omega) count, conditional on the weighted population.
5. The target label precedes D and B+2 non-Gibbs labels with probability 1/(|D|+B+3). Conditional on that order, a first preceding off-D Gibbs change has probability at most Dep; its state is still x° until that change. The target evaluation then scores S₀ even if the Gibbs draw rejects inclusion.
6. Fresh per-particle round randomness, also justified by the stopping-time argument, gives (1−beta omega)^H≤exp(−H beta omega).

One must not condition the pilot on its *eventual* calibration record. The finite bound may exceed one, and can be capped. NB′, the event that truth was drawn or empirical ESS at the floor passes, is a valid weaker hypothesis than the corrected discrepancy-range condition. The candidate-grid **restricted** ESS rule is a different object and supplies no substitute for this empirical pilot step.

### LS0

The core of E3 is a deterministic implication: if its selected centre lies in a set from which completed production-style scans score truth, the LS0 scored set contains truth. A reference mass >1/2 identifies the unique mode. T27-H3 supplies this only when its assumed constant exceeds 1/2; H3 is not proved by T27 itself. T22 requires q<1 as explained above.

The mode DP is exact: take the best block table score for each block size, max-plus convolve across blocks up to K, add the size prior, and maximise over total size. Its O(JKB) post-table arithmetic bound is valid. Exact ties require a deterministic rule; none arise in the >1/2 reference case.

`local_search` evaluates its centre with the supplied `emit_centre` flag, scans all feasible flips and swaps, tests the move limit **after** the scan, and never changes particles. LS0 starts at a new centre, so its first evaluation must be offered to the HPM (`emit_centre=true` on that first evaluation, or an explicit equivalent ledger insertion). Ordinary production callers pass false because their centre is already scored. Reusing that default for a new mode can miss S₀ when the mode itself is truth. Avoid first caching an un-emitted centre and then assuming a cache-hit emission will update the ledger: stores are only updated on fresh events.

There are at most ℓ+1 scans, each of size at most max_{k≤K}[p+k(p−k)]. If all score calls are counted, allow **1+(ℓ+1)max_{k≤K}[p+k(p−k)]** for the initial centre as well. The supplied scan-only expression remains a scan-work bound. None of this implements LS0 in the production method; adoption remains a separate decision.

## 7. T38(b)-R: gaps and a complete conditional repair

Reference: [W1-T38E PROOF §7](sources/W1-T38E/PROOF.md), lines 144–170. The algebraic composition and liminf conclusion are VERIFIED; the named route premises need the following qualifications.

### 7.1 Missing asymptotic margins in route (b1′)

“D2's hypotheses w.p.→1, with P(NBᶜ)→0” does not by itself make its finite bound tend to zero. Finite D2 imposes no Dep<1 condition: Dep≥1 gives beta=0 and a last term equal to one. Even Dep<1 at each n is inadequate if beta_n decays too quickly. Likewise b_n>0.1 pointwise need not give a nonvanishing Hoeffding margin. This is a missing inference, not a constructed BVS counterexample to all other recovery mechanisms.

**Repair:** invoke D2-∞ explicitly: fixed b₀>0.1, bounded k_D, and Dep≤1−c₀ with fixed c₀>0 on events of probability tending to one, plus P(NB′ᶜ)→0. Choose fixed t=(b₀−0.1)/2. Then H₀≥0.2max(n,p)→∞ makes both exponentials vanish. More generally, require t_n∈(0,b_n−0.1), H_nt_n²→∞ and H_n beta_n g(b_n−t_n)→∞, with vanishing exception probabilities.

### 7.2 The new B is not uniform REPAIR on every R_d

Route (b2) names all x∈R_d and quotes the old (1−a_n)^H+Hη_n form. The new theorem instead gives a start-dependent binomial tail on a family satisfying s₀+a(x)≤K. The graph uses a symmetric union, so degrees and |A(x)| need not be bounded by B. Membership in R_d alone does not give bounded v, feasible completion budgets, small η, or a positive c*.

**Repair:** define a data-measurable eligible set X_n whose states satisfy the actual theorem's assumptions; prove delivery to X_n, not merely R_d. Use beta_H(x) from §4. Sufficient statistical inputs are bounded v, uniformly positive c*, and Hη→0 on high-probability events. Alternatively keep the entire product over eligible particles. An established abstract uniform REPAIR on R_d would also suffice, but it is an assumption, not a consequence of the reviewed B.

D3 requires the *sum* of its SHARE and EXIT-end terms to vanish, as well as its initial miss term. Listing SHARE and EXIT-end without their aggregate rates does not discharge DELIV. The set/particle and target-mass/delivery distinction in the source C1 remains essential; this review does not claim a BVS delivery theorem from that toy.

### 7.3 Completion and launch cannot be hidden in U

The source explicitly imposes OP only for LS0. Locked T21, by contrast, separately requires its designated rounds/draws/scans to execute, keeps nonlaunch terms, and prohibits conditioning on future completion. Methodology §2 permits a best-scored HPM to be returned on `schedule_limit` or `numerical_failure`; U means **no usable HPM**, not every failure to execute a planned segment. The C++ also has resource-guard partial returns and scoring exceptions. If an incomplete HPM is treated as usable, these cases are not automatically in U.

**Repair:** either state the same full-execution idealisation as locked T21 for the random discovery route, or add the relevant usable-but-unexecuted/no-score term. Do not condition on observed successful completion to recover the iid or product laws. An exact-branch usable completed enumeration scores every feasible truth and can be removed from the SMC discovery term directly. Use K=min(p,floor(n/2)), not floor(n/2) alone as written in the T38 setting.

### 7.4 Repaired composition proof

Let M be actual failure to score truth, U the explicitly defined no-usable-output event, and δ₁=1−π(S₀). On Uᶜ∩Mᶜ∩{δ₁<1/2}, truth is the strict global score maximiser, so the all-scored HPM is truth. Therefore

    P(U or wrong HPM) <= P(U) + 2 E0[delta1] + P(U^c intersect M).

This is the same set argument as locked T21(C1). Since 0≤δ₁≤1 and δ₁→0 in probability, E₀δ₁→0 (boundedness gives uniform integrability). No future event is conditioned on.

For a Gibbs route, let A be the event, measurable at an actual terminal boundary, that an eligible particle has been selected by the smallest-index rule. Define it as false when that boundary is never reached. Couple a potential uninterrupted H-round continuation from its state x to the actual run until any interruption. Let E be the event that those designated H rounds execute. Then

    P(U^c intersect M)
      <= P(U^c intersect M intersect A^c)
       + P(U^c intersect M intersect A intersect E^c)
       + E[1_A beta_H(x)].

On A∩E, actual failure implies potential-continuation failure, which has conditional probability at most beta_H(x) given the boundary past. This proves the inequality without conditioning on E or Uᶜ. Dropping M in the first two terms gives simpler sufficient bounds. A product of the capped beta_H's is available for multiple past-selected eligible particles, with an execution condition for their designated continuations. Nonlaunch, interrupted bridge, and unsuitable terminal populations are all accounted for rather than silently removed.

For the pilot route, apply corrected D2 to the potential first stage conditional on data, add the probability of usable no-score output when that stage does not execute, and add failures of the data hypotheses. The margins in §7.1 then give a vanishing discovery term. For LS0 use OP/complete scans, centre scoring, and the ELIG/TD′ exceptions; the event inclusion is required only on Uᶜ.

If the applicable discovery and execution/availability terms vanish, then

    liminf P(U^c and correct HPM) >= 1 - limsup P(U).

The reverse inequality holds automatically because success is contained in Uᶜ, so the liminf values in fact agree under the repaired assumptions. If P(U)→u, the joint success probability tends to 1−u. Recovery tending to one additionally requires P(U)→0. This is a conditional composition result; no delivery or completion probability has been established by its algebra.

## 8. Method and locked-result cross-checks

| Proof assumption | Method / implementation evidence | Consequence |
|---|---|---|
| Uniform fresh permutation of all labels | Method §6.5; `v3_engine.h` lines 191–211, `draw_order`/`one_round` | B+2 non-Gibbs labels; each Gibbs label once. No systematic-order substitution. |
| Both feasible Gibbs configurations scored | `v3_engine.h` lines 92–132: `eval`, `held`, `step_gibbs`; `v3_ledger.h` lines 93–110 | Evaluation, not acceptance or terminal occupancy, supplies scoring. Infeasible additions are excluded. |
| Rejected swap/independence proposals scored | `step_uswap`, `step_nswap`, `step_indep`, lines 145–189 | A killed no-score process must kill on scored proposals before acceptance. |
| Empirical pilot ESS and forced floor | Method §6.6; `v3_calib.h` lines 18–47 | Corrected r* or NB′ controls the first stage; restricted candidate ESS is not empirical particle ESS. |
| Resample then move | Method §§6.6/6.8; `run_island_s`, lines 300–339 | First pilot resampled x° count is binomial conditional on weights. |
| No terminal resampling | `run_island_s`, lines 344–363 | Product laws hold for uninterrupted terminal trajectories conditional on the boundary past. |
| Final streams independent of calibration under EX-S | `v3_core.cpp` lines 434–437; `CalState::stream`; `v3_util.h` generator | Ideal-stream theorem, not a mathematical independence proof for deterministic pseudorandom seeds. |
| All-scored running best survives cache eviction | Method §6.10; `Ledger::offer_hpm`, `event`; inherited HPM handling in `cpp_final_run` | Later scoring cannot displace a strict global truth maximum. Fresh-only bookkeeping must not redefine scoring. |
| Local search and final extra scan | Method §6.10; `v3_engine.h` lines 382–417 | Scores truth from a feasible neighbour even with zero remaining moves; certification is stronger and different. |
| Runtime/score failures | `run_island_s` guard near line 337; `v3_score.h` lines 231–237; `cpp_final_run` partial/error handling | Full execution is not the same event as having some HPM output. |

Locked dependencies used with their actual scope:

- T09: exact start sampling and the elementary kernels. Detailed balance alone supplies neither progress nor delivery.
- T10: deterministic feasible-addition floor; no occupancy or budget success follows from that floor alone.
- T11(iii): iid final start-draw count conditional on pre-final information. The collected document locks only the named part; T38's incidental “T11(vii)” citation should be replaced by the directly applicable locked T21(C1) or the direct set proof above.
- T12/T15: frozen-run identities and an **islandwise** evidence lower tail for occupancy. They do not justify conditioning on final diagnostics or actual completion, and do not prove the lower tail in a masked regime.
- T13: restricted ESS and its coverage conditions. It does not control resampled particle survival by itself.
- T20: completed neighbour scans and certification semantics; it does not provide an arbitrary greedy basin.
- T22(i): arbitrary feasible reference with **q<1**; T22(iv)'s singleton bridge result cannot be replaced by a set result.
- T27(i): H3 is an assumed normalized reference-mass bound. No statistical compatibility is gained by citing the conditional theorem's conclusion as if H3 had been proved.
- T23: a conditional basin-prefix result; it is not an unconditional proof of the needed B premises.
- T21: H24 remains explicitly open in the locked register. A candidate route (e′) may replace it in a new statement after adoption; this review does not delete H24 or alter the locked route.

## 9. Numerical evidence and reproducibility

All numerical jobs ran sequentially through

    /home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- <command>

No large campaign was launched. A local ignored virtual environment contains NumPy 2.0.2; the first attempt with system Python lacked NumPy and produced no result. The completed checks below used that environment. Independent numerical code is [scripts/check_review.py](scripts/check_review.py); outputs are [results/independent_checks.json](results/independent_checks.json) and [results/check_stdout.txt](results/check_stdout.txt). Seed: 20261102, with explicit fixed sub-seeds in the code.

| Check | Result | Scope |
|---|---|---|
| ESS share | 2,000 random positive-weight cases; worst slack −3.72×10⁻¹⁵ | Rounding-scale residual; valid equality example and negative-weight counterexample checked separately. |
| Corrected ESS ratio | r*=1.924950591148529; old 1.925 witness ESS/H=0.89999269486449 | Exact analytic threshold, finite multiplicity witness. |
| Shared-stream independence | All 256 length-eight binary streams; joint product residual 0 | Toy variable-consumption blocks; corroborates stopping-time reasoning, not a PRNG audit. |
| Lemma U | p=8, k=3, 232 additions at each of n=200 and 800; max absolute remainders 0.6166 and 0.6324, below κ=18.7244 and 18.5046 | Independently computed normalized BVS scores and RSS ratios. |
| Exact small round | p=4, B=2, eight labels; dynamic program integrates all 40,320 orders and all move outcomes | No Monte Carlo. Method target, composite start, graph, and rejected-proposal scoring modeled explicitly. |
| Theorem B | 45 start/horizon checks; 12 have bound below one; no violations | Original c*,η,v, with H=1,2,4. Full rows retained in JSON. |
| P1 | Four distance-one starts; a₁ between 0.2763 and 0.4970; each below its exact hit probability | The bounds are not presented as production B=14/16 constants. |
| D2 round ingredient | beta=0.1620095; exact hit probabilities exceed it at φ=0,0.3,1 | Tests the per-particle ingredient, not the start-mass premise for this small example. |
| Elementary kernel balance | Maximum target-weighted detailed-balance residual 2.35×10⁻¹⁵ | All eight labelled kernels on 16 states. |
| CE1 | Independent p=4 examples at n=200,800; exact first-change exit bounds 0.1525 and 0.1506; Lemma E lower bound ≈1/7 | First-change bounds are rigorous events in the ideal component model; these numbers are floating evaluations. |
| E3(ii) counterexample | Actual reference mass 9.44×10⁻¹⁴ versus claimed bound 1.98×10²³ | Method-consistent p=2 table law, without the omitted q<1 premise. |

Small-p cases test the **SMC components**. Production would enumerate them, so they are not claimed as end-to-end production SMC runs. The calculations enumerate exactly specified finite events using floating arithmetic; they are not formal exact-arithmetic proofs or C++/R integration tests. I did not compile the Rcpp engine.

Two additional small reproductions use the pinned prior referee's code and are explicitly **not independent implementations**:

- [CF(1) D2 reproduction](results/cf1_d2_reproduction.txt): n=400,p=89,B=9, the W1 design. Reproduced b=0.9278, Dep=0.0910, beta=0.0454. The full two-exponential bound is **2.244×10⁻⁷ plus P(NBᶜ)**, whereas 3.133×10⁻⁹ is only the last exponential with t=0. Three pilot replications all scored truth and none violated NB. Three successes do not establish a small NB-failure probability.
- [LS0 reproduction](results/ls0_reproduction.json), via [scripts/reproduce_ls0.py](scripts/reproduce_ls0.py): independent CF(2) design seed 1 at n=400,p=89,B=9. Start-mode mass 0.8521410; path {1}→{1,2}→{1,2,3}; truth scored and search stopped with no improvement. This checks a finite example, not TD′ uniformly over a sequence or over all R_d.

Commands, from the repository root after installing NumPy into the local environment:

```bash
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- theory_campaign/A-REV1/.venv/bin/python theory_campaign/A-REV1/scripts/check_review.py
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- env PYTHONDONTWRITEBYTECODE=1 W1DIR=theory_campaign/A-REV1/sources/W1-T38E/scripts theory_campaign/A-REV1/.venv/bin/python theory_campaign/A-REV1/sources/W3-VT38E/scripts/v4_d2_pilot.py 400 -1 3
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- env PYTHONDONTWRITEBYTECODE=1 theory_campaign/A-REV1/.venv/bin/python theory_campaign/A-REV1/scripts/reproduce_ls0.py
```

## 10. Disposition

Retain the repaired finite Theorem B and corrected finite D2 as conditional candidates. Correct Proposition U's two bookkeeping shortcuts, restrict Lemma S's attainment assertion, restore q<1 in E3(ii), and correct Lemma U's limiting constant. Rewrite T38's pilot rates, eligible-set interface, and execution terms as in §7 before giving the complete package a VERIFIED verdict.

The review does not establish joint asymptotic premises for the masked production method, a production-scale P1 constant, terminal delivery, or a vanishing operational failure probability. No locked status or file was upgraded or edited. All review artifacts are confined to `theory_campaign/A-REV1/`.
