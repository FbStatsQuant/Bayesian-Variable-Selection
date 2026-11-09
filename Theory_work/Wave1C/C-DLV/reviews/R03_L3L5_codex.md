# R03 — Cross-family adversarial review of L3 and L5

Overall verdict: **ERROR as written**, localized to Corollary 5.3. The core ESS identities, variance bound, pilot stage bound, and two-model insertion argument survive. The newly added shorter-range extension has been included in this review; its extra insertion allowance is missing from the corollary, producing a genuine false overflow certificate.

Reviewed snapshots: L3 SHA256 `bc8d0fb8f841ba26441b38931b843c16d1469c127e5537a462eba92cbe9c9229`; L5 SHA256 `f6f9b21d06eb74bbec69735d931f0bde8972c7eccc2ee20bcf61682a9681eea1`. Code references below are under `Scripts/SMC_BVS/core/`. EX-A and the locked STATEMENT premises are used throughout.

| Result | Verdict |
| --- | --- |
| Lemma 3.1 | VERIFIED |
| Lemma 3.2 and Corollary 3.2′ | VERIFIED |
| Lemma 3.3 | VERIFIED under the stated valid-input/resource premises |
| Lemma 3.4 | VERIFIED-WITH-AMENDMENTS: counting conventions and false explanatory sentences |
| Proposition 3.5(a) | VERIFIED |
| Proposition 3.5(b) | VERIFIED-WITH-AMENDMENTS: count appended intervals explicitly |
| Lemma 5.0 | VERIFIED-WITH-AMENDMENTS: distinguish the raw passing endpoint from a snapped candidate |
| Lemma 5.1 | VERIFIED |
| Lemma 5.2 | VERIFIED-WITH-AMENDMENTS: counting conventions and rounded-constant justification |
| Lemma 5.2′, added during review | VERIFIED-WITH-AMENDMENTS: terminal-step bookkeeping |
| Corollary 5.3 | ERROR |

## Numbered findings

1. **FATAL — Corollary 5.3 uses the wrong insertion bound under Lemma 5.2′.** L5:59–60 allows either remainder hypothesis but explicitly uses the bound of Lemma 5.2. Under the shorter-range hypothesis this omits `ceil(log_(4/3)((1+eta)/eta))`. The omission can certify a construction that actually overflows.

   Here is a finite three-model counterexample within the deterministic affine-family setting:

   ```text
   ell_1(t) = 0
   ell_2(t) = t
   ell_3(t) = K(t - 1 - eta) + log(0.01)
   eta = 2^(-40), K = 2^80, epsilon = 0.01
   T_e = 1000
   targets = {0, 1/1000, 2/1000, ..., 977/1000, 1}
   k = 978, x_0 = 0, D = 1.
   ```

   On `[0,1+eta]`, the third model has weight at most `0.01`, whereas the first two have combined weight at least `2`. Thus `r_t < 0.005 < epsilon`; the exact maximum is approximately `0.00268220066510544`. The old displayed bound is `Nbar_b=22`, so the printed certificate says `978+22 <= 1000`.

   All first 977 targets pass: their increments are `0.001`, the required three evaluation points are within the controlled range, and `(1-epsilon)^2 rho^(2) > 0.980099 > 0.90`. At `u=0.977`, however, at least 24 additional bisection intervals are appended before reaching 1 or the snap band. Consequently the code returns `too_many_intervals` at interval **1001**.

   An analytic check avoids dependence on numerical threshold decisions. Put `B=1+eta+log(1000)/K`. If `2v-u >= B`, the third model's extrapolated weight is at least `10`. For `0 <= u <= v <= 1`,

   ```text
   rho(u,v) <= (1+exp(1)+0.01)^2 / 20 < 0.70 < 0.90.
   ```

   Hence every passing raw endpoint satisfies `v < (u+B)/2`. Starting from `0.977`, after `m <= 24` such steps,

   ```text
   u_m < B - (B-0.977) 2^(-m) < 1 - 10^(-12).
   ```

   Thus there is no snap or terminal target in these steps. The smallest midpoint passes by the local two-model condition, since its extrapolation is below 1, so there is also no `non_progress`. The 24th inserted interval forces overflow. Independent 115-digit Decimal evaluation of the literal 60-halving rule gave `u_24 ≈ 0.9999999986300026648135815` and validated ESS `≈ 0.9002693824446251`.

   **Required fix:** use the bound of the applicable lemma, including the extra term for 5.2′. Propagate that distinction into every capacity/conditional-delivery statement using the shorter-range hypothesis. This counterexample does not refute Lemma 5.2 with remainder controlled on all of `[0,2]`.

2. **MAJOR — Capacity alone does not imply success; `non_progress` is only conditionally excluded.** L5:60–62 says the construction “succeeds” under the capacity inequality and that `non_progress` “is impossible.” The later exceptions acknowledge the problem, but the opening assertions are false literally. Both remaining failure mechanisms occur even with a generous interval budget and zero remainder.

   Use two models `ell_1(t)=0`, `ell_2(t)=Dt`, targets `{0,1}`, `T_e=1000`, and the admissible remainder bound `epsilon=0.01`. Then `k+Nbar_b=23 <= 1000`.

   * For `D=2^62`, the smallest midpoint is `2^-60`, so its scaled increment is `4`. Its ESS is `(1+exp(4))^2/[2(1+exp(8))] ≈ 0.5183094967 < 0.90`. All 60 midpoints fail, and the construction returns `non_progress` without appending an interval.
   * For `D=log(2)/(1-2^-42)`, the exact passing boundary is `v_*=1-2^-42`. Bisection returns this dyadic boundary, which is inside the snap band. Snapping it to 1 gives `rho(0,1) ≈ 0.899999999999962175 < 0.90`, so validation fails. This example has modest `D`, not an extreme slope.

   **Required fix:** state “the construction cannot fail through `too_many_intervals`” under the correct capacity bound. Full success additionally requires exclusion of beta and gamma. State explicitly that beta is impossible **if** `(b-u)2^-60 <= s_0/D` at every attempted step; `D <= s_0 2^60` is a sufficient uniform condition. The final failure-union interpretation is otherwise correct under Lemma 5.2.

3. **MINOR — The interval identity needs appended-step counts, whereas L5 defines a bisection-limited step by its branch condition.** L3:46–47 and Proposition 3.5(b) use `#intervals=N_p′+N_b`; L5:3–4 counts every step with `rho(u,b)<0.90`. A terminal unsuccessful bisection trial satisfies that condition without appending an interval. In the `D=2^62` example, the literal attempted count is `N_b=1`, but `#intervals=0`.

   **Required fix:** distinguish `N_b^app` from `N_b^try`, or explicitly define the interval identity using successfully appended steps. For Lemmas 5.2/5.2′, counting the starting coordinates also bounds a final unsuccessful trial: all preceding counted trials made the required progress. Alternatively reserve the displayed extra `+1` for that terminal trial when using the exact constants. No double counting arises from a successfully appended snapped bisection step: such a step is impossible, because `rho(u,1) <= rho(u,b) < 0.90`.

4. **MINOR — The claimed decreasing sequence of tested midpoints is not the code's bisection trajectory.** L3:51–52 says the tested mids decrease from the initial midpoint to `u+(b-u)2^-60`. Once a midpoint passes, subsequent midpoints can increase. For the two-model family `x_0=0, D=2`, `u=0, b=1`, the first tests are `0.5` (fail), `0.25` (pass), `0.375` (fail), `0.3125` (pass).

   The stated `non_progress` equivalence is nevertheless correct. **Required fix:** argue that if no midpoint passes, every update is `hi=mid`, so the 60th test is exactly the smallest dyadic midpoint. If any midpoint passes, it is at least that smallest dyadic point, which therefore passes by monotonicity. The code's second progress check cannot newly fail under EX-A once a midpoint passed.

5. **MINOR — The target-visitation explanation forgets snapping.** L3:45 says a step never jumps over its current target, and L3:54–55 concludes that the next `u` is at most `b` even after expressly allowing `v=1 >= b`. For flat `F` and targets `{0,1-2^-42,1}`, the construction appends 1 immediately and never appends the current target `1-2^-42`.

   **Required fix:** say that unsnapped steps do not skip the current target; targets strictly below the first **raw candidate that is snapped** are reached, that candidate is replaced by 1, and later targets are skipped. Proposition 3.5(a) already has the appropriate exception. For Lemma 5.0, define `v_raw=lo`: its passing ESS and `hi-u <= 2(v_raw-u)` hold before snapping. A post-snap candidate need not pass; if it is actually accepted, validation supplies its passing ESS.

6. **MINOR — The rounded numerical specialization needs a separate justification.** At `epsilon=0.01`, recomputation gives

   ```text
   theta  = 0.9182736455463728191...
   s_0    = 0.5881436871152899355...
   lambda = 2.419118909249997214...
   (2 lambda + 2 s_0)/(s_0/2) = 20.45257077307228...
   ```

   In particular `s_0=0.5882` is not the four-decimal rounding. Replacing `lambda` by `2.42` and `2s_0` by `1.18` decreases the logarithm's argument; it is not automatically a conservative substitution through a ceiling.

   The displayed `22+ceil(log_(4/3) max{1,(-x_0-2.42)/1.18})` can be retained, but needs proof. Counting starting coordinates gives the stronger exact bound `21+ceil(log_(4/3) max{1,(-x_0-lambda)/(2s_0)})`, including a terminal failed trial. The exact logarithmic argument is less than `4/3` times the rounded argument for every real `x_0`, so their ceilings differ by at most one. This recovers the printed constant 22. **Required fix:** add this argument or keep exact constants; do not present the rounded expression as direct equality/substitution. Write `O(1+log(1+|x_0|))` if the asymptotic notation is intended uniformly.

7. **MINOR — The new small-midpoint range proof has an unnecessary false inequality.** L5:62 asserts `1+2^-59 <= 1+eta`, although Lemma 5.2′ allows every `eta>0`, including `eta<2^-59`.

   **Required fix:** for `m=u+(b-u)2^-60`, use

   ```text
   2m-u = u + 2^-59(b-u) <= b <= 1.
   ```

   Therefore the smallest midpoint always uses remainder values within `[0,1]`, independently of eta. The desired conditional exclusion of beta survives.

## Independent algebra and code checks

**Lemma 3.1.** For `z=2v-u`, expanding the logarithm of the proposed ratio gives

```text
log(q_u(M) q_z(M)/q_v(M)^2)
= ell_M(u)+ell_M(z)-2ell_M(v) - F(u)-F(z)+2F(v)
= 2F(v)-F(u)-F(z)
= log rho(u,v).
```

The affine contribution vanishes exactly. Both consequences follow because `0<q_v(M)<=1`. No reciprocal or sign error was found.

**Lemma 3.2 and dominance intervals.** With `Z=sum exp(ell)`, differentiation gives `F′=Z′/Z=E_q d` and `F″=Z″/Z-(Z′/Z)^2=Var_q(d)`. For `h=v-u`, integration by parts gives

```text
integral_u^v (t-u) F″(t) dt = h F′(v)-F(v)+F(u),
integral_v^(v+h) (v+h-t) F″(t) dt = -h F′(v)+F(v+h)-F(v).
```

Their sum is exactly the claimed second difference; there is no missing factor of two. The kernel area is `h^2`. Also `partial_v Delta=2[F′(2v-u)-F′(v)]>=0`, proving the required monotonicity. The dominance region is a convex sublevel set as stated; the interval assertion actually holds for every threshold in `(0,1)`.

**Lemma 3.3.** Here `T_e` is a positive integer, the particle population is nonempty, and `H` equals its size. Every nonterminal call either returns an unforced increment at least `1/T_e` or a forced increment exactly `1/T_e`; only a terminal truncation/snap can be shorter. If `T_e` nonterminal increments existed, their sum would be at least 1, a contradiction. Thus the uninterrupted pilot reaches exactly 1 in at most `T_e` stages. An unforced `lo` inside the snap band causes no extra-stage violation. The early resource return in `v3_engine.h:335–337` can return a partial schedule, but is excluded by the STATEMENT premises; do not generalize this lemma to interrupted pilots. `cpp_cal_pilot:604` prefixes 0, and `v3_calib.R:68,79,111` reuses that same pilot schedule for every build at the tier. `cpp_cal_V:674–683` supplies a nonempty deduplicated set and the stated affine coefficients.

**Lemma 3.4 and Proposition 3.5.** With a completed pilot target list, 1 is always available, so `no_target_above_u` is unreachable. An unsnapped candidate has already passed the identical ESS test; only snapping can newly cause validation failure. `too_many_intervals` is checked after appending the first excess interval (`v3_calib.h:93–94`). Under Proposition 3.5(a), every target and its possible snapped replacement pass, so there is no bisection and at most `k` intervals. The variance and endpoint-dominance sufficient conditions both cover every extrapolation `2v-u in [0,2]`. The subset-of-pilot statement belongs to part (a), not arbitrary successful constructions.

**Lemma 5.0.** After 60 exact halvings, `delta=hi-lo=(b-u)2^-60`. If any midpoint passed, `lo-u=j delta` for an integer `j>=1`; hence `hi-u=(j+1)delta<=2j delta=2(lo-u)`. The endpoint `hi` failed, including when it remains the initially tested target `b`. Thus the factor two and the `hi=b` case are correct. Snapping only increases the candidate's displacement; it can invalidate its ESS, as finding 2 shows.

**Lemma 5.1.** With `s=(v-u)D`, `a=exp(x(u))`, `c=exp(s)`, the three logistic probabilities are `a/(1+a)`, `ac/(1+ac)`, and `ac^2/(1+ac^2)`. Their ratio simplifies to

```text
rho^(2) = (1+ac)^2/[(1+a)(1+ac^2)],
(1+a)(1+ac^2)-(1+ac)^2 = a(c-1)^2.
```

For `f(a)=a/[(1+a)(1+ac^2)]`,

```text
f′(a) = (1-a^2 c^2)/[(1+a)^2(1+ac^2)^2].
```

Its maximum is at `a=1/c`, with value `1/(1+c)^2`, giving bound (i). For (ii), `a(c-1)^2/(1+ac^2)<=1`; for (iii), `a(c-1)^2/(1+a)<=ac^2`. Dividing by the remaining positive denominator gives exactly the other two bounds. Both use `c>=1`. All algebra checks.

**Lemma 5.2.** The perturbation identity and both inequalities are correct:

```text
rho/rho^(2) = (1-r_u)(1-r_(2v-u))/(1-r_v)^2
             in [(1-epsilon)^2, (1-epsilon)^(-2)].
```

The interval `[0,2]` suffices for every accepted candidate and every failing `hi<=b<=1`; no larger interval is needed. Conditions A/B/C imply, at a failing `w=u+h`,

```text
x < lambda, hD > s_0, x+2hD > -lambda,
x_next-x > max{s_0/2, (-lambda-x)/4}.
```

The Phase-1 contraction factor `3/4`, cutoff `2s_0`, and Phase-2 width `2lambda+2s_0` are correct. Non-bisection steps strictly increase `u` and therefore `x`; a successful snap increases it further and terminates. A rejected snap makes no later coordinate and is a terminal trial, not a reversal. Counting starts resolves terminal-trial bookkeeping without weakening the bound.

**Lemma 5.2′.** Type-I failing endpoints use only `[0,1+eta]` and satisfy the same coordinate inequalities. Type-II endpoints imply `v_raw-u>(1+eta-u)/4`, so `z=1+eta-u` contracts by a factor below `3/4` on each appended Type-II step. Other appended steps only decrease `z`. Count the Type-II starting values `z>eta`, rather than claiming the postterminal value is strictly above eta: if the last step reaches 1, it equals eta. The stated ceiling bound remains valid, including a final unappended trial by the same starting-value argument.

**Numerical verification.** Independent standard-library scripts were run from stdin; the lead's script was not used. Besides the counterexamples above, 2,000 random algebra checks found no two-model bound violations, and 32 grids computed at 90-digit precision found no violation of the original Lemma 5.2 bound. These searches corroborate the derivations; the counterexamples and algebra above provide the substantive evidence. No repository file other than this review was written.
