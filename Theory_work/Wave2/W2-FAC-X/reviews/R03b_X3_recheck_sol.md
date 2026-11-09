# R03b — independent adversarial recheck of X3

**Verdict: VERIFIED-WITH-AMENDMENTS.**

All nine numbered claims (i)–(ix) are correct under the stated hypotheses. The repaired (iii) survives the check, including its strict constants and both R03 counterexamples. No FATAL or MAJOR issue was found. Three MINOR amendments remain in the proofs/explanatory text; one is a false unqualified sentence in the final remark, with a two-point counterexample below.

Scope: current `lemmas/X3_softgap.md`, lines 1–94. This review checks only this deterministic lemma, not X4 or the surrounding theorem. Step statements are read for existing steps `0 <= i < I`, state statements for `0 <= i <= I`, and the intervals with infinite endpoints in the usual extended-real sense. No source lemma or simulator was modified.

## Numbered issues

1. **MINOR — proof of (i), line 47: stale assertion of nonemptiness.**

   The statement at lines 26–27 correctly allows an empty terminal state, but its proof still ends with the unconditional assertion `K_i != empty`. This is false for an exhausted prefix, and also for an initially empty index set with I = 0. For example, N = {1}, B = 0, kappa' = 2, varpi = 0, I = 1, deleting 1 gives x_0 = 1/3, x_1 = 0 and K_1 empty, with all hypotheses satisfied.

   **Fix:** replace the last sentence by: “If K_i is nonempty, nondegeneracy places at least one kept point on one side of x_i. If K_i is empty, the endpoint conventions give a_i = -infinity, b_i = +infinity, and the asserted empty kept gap and strict centre inequalities still hold.” The claim itself needs no change.

2. **MINOR — proof of (viii), lines 84–85: the zero-tolerance endpoint argument is omitted.**

   For varpi > 0, the closed band `[a_i - 2 varpi, b_i + 2 varpi]` from (vi) lies in the required open band with coefficient 4.3. At varpi = 0, this reduces to `[a_i,b_i]`, which alone does not imply membership in `(a_i,b_i)`. Thus the last inference needs an additional sentence; this is not a counterexample to (viii).

   **Fix:** add: “When varpi = 0, every finite a_i or b_i is the coordinate of a kept index. Distinctness of all coordinates excludes a deleted point from either finite endpoint; any real deleted point automatically avoids an infinite endpoint. Consequently the closed-band bound also gives strict open containment.” Here i_0 = M = 0, so this covers all later states. For I = 0 the conclusion is immediate from D_0 empty. The endpoint/centre comparisons in lines 82–84 remain valid even at varpi = 0.

3. **MINOR — final remark, lines 92–94: the 4 varpi mechanism needs the size restriction.**

   The remark says without qualification that a crossing requires a hole narrower than 4 varpi and that a hole at least 4 varpi wide only grows. This is false when there are two kept points and kappa' is close to 1. The numbered claims correctly restrict this threshold to steps with at least three kept points.

   **Counterexample:** let N have coordinates {-3/2, 7/2}, B = -2, kappa' = 11/10, varpi = 1, I = 1, and delete 7/2. Then

   - x_0 = 0, d_0 = 3/2, and the deletion obeys the rule with equality: 7/2 = d_0 + 2 varpi;
   - x_1 = -5/3, so the retained point -3/2 is strictly between x_1 and x_0;
   - the initial hole has width 5 >= 4 varpi;
   - neither original coordinate equals either centre.

   Thus this is a valid crossing despite a width exceeding 4 varpi. The old hole [-3/2,7/2] also fails to be contained in the new hole [-infinity,-3/2]. This does not violate (iii), whose unrestricted constant is c(11/10) = 42, or (v), whose size hypothesis fails.

   **Fix:** begin the remark “At steps with |K_i| >= 3, ...”, and qualify persistence of the 4 varpi threshold by the same restriction on every subsequent step considered. Alternatively use c(kappa') varpi as the unrestricted threshold, by (iii)–(iv).

## Claim-by-claim audit

- **Setting and drift:** verified. Substituting the removed coordinate into the two centre definitions gives the drift identity exactly. Its denominator is at least kappa' > 1, including deletion of the last point. The centre of the empty set is the finite number B/kappa'. The minimum d_i is used only at existing deletion steps, where K_i is nonempty. All denominators in (iii) and (vii) are positive: |K_i| - 2 + kappa' >= kappa' - 1 and |K_0| - Q - 1 + kappa' >= kappa' - 1.

- **(i):** the repaired statement is valid at every state, including empty and one-sided states. Nondegeneracy excludes kept coordinates at the centre. The proof needs issue 1 only.

- **(ii):** valid for either deletion side, including one-sided holes. A right deletion has finite b_i, is at least b_i, and is at most b_i + 2 varpi because d_i <= R_i. Its other bound follows from a_i < x_i < the deleted coordinate, or is vacuous when a_i = -infinity. Reflect for a left deletion.

- **(iii):** both cases of the repaired proof are valid. For a right deletion, write h = xi_j - x_i and m = |K_i| - 1 + kappa'. Crossing forces finite a_i and b_i, L_i < h/m, R_i <= h, and h <= d_i + 2 varpi. If d_i = L_i, these give d_i(m-1) < 2 varpi and omega_i <= 2d_i + 2 varpi. If d_i = R_i < L_i, then R_i < L_i < (R_i + 2 varpi)/m, yielding the same distance bound and the stronger strict width bound in that case. Reflection covers left deletions. When |K_i| >= 3, m-1 > 2, giving omega_i < 4 varpi; generally m-1 >= kappa'-1 gives omega_i < c(kappa') varpi. A crossing is impossible with a single kept point, since the next kept set is empty. At varpi = 0 the derived strict bound d_i < 0 excludes crossings altogether. No future step is used.

  The second case is genuinely possible: take {-1/5, 1/10, 1}, B = -9/10, kappa' = 2, varpi = 1, and delete 1. Then x_0 = 0, x_1 = -1/4, L_0 = 1/5, R_0 = d_0 = 1/10, and the retained point -1/5 is crossed. In particular, R03's explanation that the opposite-side distance must always be the smaller distance is unnecessary and incorrect. The current two-case proof avoids that assertion and proves the repaired statement correctly.

- **(iv):** no crossing together with nondegeneracy excludes retained points in the entire interval between the two centres, including its endpoints. For a right deletion the left endpoint stays fixed, while the right endpoint can only increase; reflection gives the other case. This also covers infinite endpoints and deletion down to the empty state. Widths are finite or +infinity, with no undefined subtraction of equal infinities.

- **(v):** induction uses only steps i_0,...,I-1. The size hypothesis and (iii) exclude each crossing; (iv) propagates nesting and the width threshold to the next state, including the terminal state. If i_0 = I, the conclusion is vacuous except for reflexive containment.

- **(vi):** apply (ii) at each specified deletion step and then endpoint nesting from (v). The proof uses only steps before i', and permits infinite endpoints.

- **(vii):** correct for every supplied prefix. A narrow hole has two finite endpoints, d_i < 2 varpi, and deletion distance < 4 varpi. If M >= Q+1, precisely the existing steps 0,...,Q are used. Bounding their pre-deletion centres needs only the first Q increments; Q+1 distinct deleted coordinates then lie in a closed interval of length 8.2 varpi, which is contained in one of length 9 varpi, a contradiction. Once M <= Q, the repeated increment estimate includes x_M and uses no step beyond M-1. If the prefix ends before any wide state, this proves I = M <= Q directly; it does not assume an extension. For varpi = 0, every hole has positive or infinite width, so i_0 = M = 0. For an empty initial set take Q = 0; all conclusions are immediate.

- **(viii):** correct, with the proof addition in issue 2. For i <= M, (vii) and a_i < x_i < b_i put the initial deletion window strictly within the claimed expanded hole. If M < i <= I, then i_0 = M is an existing state, (v) transports that window, and (vi) bounds later deletions. These arguments apply to every truncated prefix separately. The left inclusion is the empty kept gap from (i). The size hypothesis prevents an empty terminal set when I > 0, but the containment also makes sense for the empty initial set.

- **(ix):** correct without a minimum kept-size restriction. At any crossing the finite hole endpoints are distinct original coordinates, so the spacing assumption contradicts the general c(kappa') bound in (iii). Nesting and (ii) put deleted points in the final closed 2 varpi band. At a finite endpoint, spacing excludes every other original coordinate in its outer band and the endpoint itself is kept. At an infinite endpoint that side imposes no restriction on a real deleted point. This proves exact equality, also at varpi = 0 and for sets of size one or two. At exhaustion the hole is the whole line and D_I = N. When fewer than two coordinates exist, dispense with the phrase “minimal spacing” and simply note that a crossing requires two distinct kept coordinates.

## Both R03 configurations satisfy repaired (iii)

For {1/10,-21/10,-10}, B = 12, kappa' = 2, varpi = 1, deleting -21/10 gives x_0 = 0 and x_1 = 21/40. Thus d_0 = R_0 = 1/10, L_0 = 21/10, and omega_0 = 11/5. The retained 1/10 is crossed. The repaired bounds are

`1/10 < 2/3`, `11/5 <= 2(1/10) + 2 = 11/5`, `11/5 < 4`, and `11/5 < c(2) = 6`.

Reflection, with coordinates {-1/10,21/10,10}, B = -12 and deletion 21/10, gives x_1 = -21/40 and d_0 = L_0 = 1/10. Exactly the same repaired inequalities hold. Both configurations satisfy the deletion rule with equality and nondegeneracy at both states. They refute the previous strict width subclaim, but neither refutes the repaired non-strict inequality.

## Independent computational checks

All checks ran as inline Python 3.13 with exact `fractions.Fraction` arithmetic, without importing the simulator or writing scratch files. These are finite falsification checks, not substitutes for the arguments above.

1. Enumerated all subsets of {-4,-2,-1,1,2,4}, five offsets B in {-5,-1,0,1,5}, five kappa' values {11/10,3/2,2,5,1000}, and four tolerances {0,1/4,1,2}: **6,400 configurations**. Explored all reachable kept masks and admissible deletion edges, excluding states/edges violating the stated global-coordinate nondegeneracy requirement. Checked (i), (ii), all repaired (iii) bounds, (iv), and sparse-case equality/no-crossing: **42,075 states, 60,708 admissible edges, 2,632 crossings, zero violations**. Coverage included **6,232 zero-tolerance states, 5,930 empty states, and 8,153 sparse states**.

2. Built **240 exact rational trajectories** satisfying (vii)'s quantitative assumption, using both separated configurations with a small initial cluster and dense configurations with large kappa'. Used random, farthest-allowed, uppermost-allowed, and lowermost-allowed deletion policies; included varpi = 0. Checked each successive prefix, stopping at two remaining points so that every preceding deletion had at least three kept points. Checked the prefix-specific M, its Q bound, every relevant centre and initial deletion window, nesting and the later 2 varpi band, and both (viii) inclusions: **13,460 prefixes**, comprising **2,649 prefixes without a wide state yet** and **10,811 with a wide state**, with **zero violations**.

3. Recomputed both R03 examples and the two-point remark counterexample exactly. The outputs agree with the fractions recorded above.

**FATAL/MAJOR list: none.** Amend the three MINOR items above; no numbered claim requires weakening.
