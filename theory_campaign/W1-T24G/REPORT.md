# W1-T24G — REPORT: Gibbs-path terminal repair (restated T24)

Run of 2026-11-02, branch `theory/W1-T24G`. Nothing here has been reviewed. Every PROVED is a candidate until
cross-family review. Proofs are in `PROOF.md`, working notes in `NOTES.md`, scripts in `scripts/`, numerical
outputs in `results/`.

## Headline

1. **Restated T24 (Theorem B): PROVED (candidate).** It is deterministic given the data, and its constants are
   exact and polynomial. For a particle at x near the truth at the start of H terminal rounds at φ = 1:
   **P_x(S₀ not scored within H rounds) ≤ P(Bin(H, c_*) < v) + H·η ≤ v(1 − c_*)^{⌊H/v⌋} + H·η.**
   The per-round progress constant satisfies c₂ ≥ **1/(B+3) − ε_del** in the phase where extras are deleted.
   This confirms Fable's order, now exact, with no factorial. In the phase where missing truths are added,
   c₁ = 1 − ε_add. The factor 1/(s₀+d+B+2)! is gone. The look-alike problem is handled by a potential V that
   does not count extras while a truth is missing. Look-alike additions at incomplete states are therefore
   neutral and charged to an explicit look-alike budget |A| inside v. Leakage is evaluated only at states
   that contain S₀ (phase 2), as Fable proposed.
2. **The EXIT_d issue is resolved (Prop. U, PROVED).**
   - A Gibbs step cannot be undone by Gibbs within the same round, because each label runs once.
   - A non-Gibbs move can undo progress, but only in two ways. (i) A truth removal or a V-increasing
     independence jump is "bad" and charged to η by a uniform per-label bound; internal moves are included,
     not just exits. (ii) An extra-for-extra swap is V-neutral, so it cannot undo progress. It can only hide a
     slot, which is charged inside c₂ (term h(l)), never to η.
3. **H24 as written is false in correlated designs (CE1: COUNTEREXAMPLE, numerical and reproducible; PROOF
   SKETCH for the asymptotic version).** H24 needs a uniform one-round exit bound on 𝓡_d with (L+4)η_n → 0.
   But at a boundary state (S₀∖{j}) ∪ P with |P| = d, the Gibbs step of a look-alike of j exits with
   probability ≥ (1−o(1))/(B+d+4). Measured at p = 20, n = 200: 0.62–0.98 in S2–S6, and 0.16–0.22 even in S1.
   So **H24 cannot be discharged. T21 route (e) should be rewritten with Theorem B's inequality** (a drop-in
   replacement, §5), plus a multi-particle refinement (Cor. B-M) that holds because terminal trajectories are
   conditionally independent.
4. **The brief's target form (1−c′)^{⌊H/(s₀+d)⌋} is not a valid conclusion (CE2).** The one-step-per-round
   argument needs the factor v: the correct bound is P(Bin(H,c′) < v) ≤ v(1−c′)^{⌊H/v⌋}.
5. **Usefulness is asymptotic only, and slow, with one exception.** The exception is Corollary P1: a
   particle at Hamming distance one scores S₀ in the next round with probability ≥ a₁(x), rigorously, and
   a₁ ≥ 0.14 in all designs at n = 200. With conditional independence, N₁ such particles fail together with
   probability ≤ 0.86^{N₁}. Otherwise:
   - Under G, R, SE, BM-∞ the phase-2 premises hold automatically only at S₀ itself and for deleting a
     single extra (a = 1). Every superset family with a ≥ 1 also needs NL0(a).
   - For a ≥ 2 and for incomplete starts, six extra named conditions are needed: NL0, UDEL, TS, TL, BTP and IND.
   - With c_* ≈ 1/(B+3), the single-particle bound decays like n^{−c_*/ln 2}, about n^{−0.07}.
   - At n = 200 (p = 20) the bound is vacuous: superset leakage η₂ is about 0.4–1.0 per round, because
     π(S₀) ≈ 0.72.
   - The actual repair is far faster. From raw π₀ draws, which approximate a "masked" delivered population,
     100% of particles score S₀ within 12 terminal rounds in all 12 designs: 41–90% in round 1 (only 11–12% in
     the masked design S5), 66–99% by round 2.
   - The measured per-round progress is 0.75–1.00, against proven c₂ ≈ 0.25–0.47 and floor 1/(B+3) = 0.143.

## 1. Refined statements (full; every hypothesis named)

Common setting (PROOF.md §0):
- Assumptions: EX-A, EX-S, SR; φ = 1; L + 4 terminal rounds without resampling.
- Each round has m = p+B+2 labels in a uniform random order: Gibbs labels G_j, the uniform swap U, the
  neighbour swaps N₁..N_B, and the independence move I.
- M(W) = S₀∖W, P(W) = W∖S₀. Superset family: 𝒮_a = {S₀∪P : |P| ≤ a}.
- For a start x with M(x) ≠ ∅:
  - look-alike set A(x) = ⋃_{j∈M(x)} N(j)∖S₀, built from the method's own neighbour graph;
  - junk set J = S₀ᶜ∖A, junk count c = |x∩J|;
  - completion family 𝒵(x) = {U∪P∪Q : x∩S₀ ⊆ U ⊆ S₀, P ⊆ A, Q ⊆ J, |Q| ≤ c};
  - a = |A| + c and 𝓕(x) = 𝒵(x) ∪ 𝒮_a.
- Feasibility: s₀ + a ≤ K.
- Potential: V = |M| + a while M ≠ ∅, and V = |P| on supersets.
- Step classification:
  - **bad**: leaves 𝓕(x), raises V, or removes any truth;
  - **progress**: lowers V, or is a Gibbs evaluation that scores S₀;
  - **neutral**: everything else.

**Theorem B (restated T24). PROVED.** Define:
- ε_add = max_{∅≠M′⊆M(x)} min_{j∈M′} sup_{W∈𝒵(x), M(W)=M′}(1−o_j(W)) (uniform addability, hypothesis-free
  definition);
- η₁ = Σ_labels sup_{W∈𝒵(x), M(W)≠∅} P_W(bad);
- ε_del(a) = sup_{W∈𝒮_a∖S₀, l∈P(W)} o_l(W);
- h(l) = ½Σ_{e non-Gibbs} sup_{W∈𝒮_a, l∈W} P_W(e neutrally removes l);
- H_a = sup_{W∈𝒮_a∖S₀} min{min_{l∈P(W)} h(l), (B+2)/(|P(W)|+B+2)};
- η₂(a) = Σ_labels sup_{W∈𝒮_a∖S₀} P_W(bad);
- c₁ = 1−ε_add, c₂ = 1−ε_del−H_a, c_* = min(c₁,c₂), η = η₁+η₂, v = V(x).

Then P_x(S₀ not scored within H rounds) ≤ P(Bin(H,c_*) < v) + Hη ≤ v(1−c_*)^{⌊H/v⌋} + Hη, and c₂ ≥ 1/(B+3)−ε_del.
For x ⊇ S₀ use only phase 2, with a = |P(x)|.

Choosing A = ∅ gives exactly v ≤ s₀ + d and the brief's exponent ⌊H/(s₀+d)⌋. The price is that look-alike
additions then count as bad (junk overflow) and enter η₁.

**Proposition D (drift form). PROVED.** Split η = η_ex (steps leaving 𝓕(x)) + η_in (other bad steps). With
v_max = |M(x)| + a and ρ(z) = z⁻¹ + (1−z⁻¹)(1−c_*+η) + exp{(z^{v_max}−1)η} − 1,
P_x(not scored within H) ≤ Hη_ex + inf_{z>1} ρ(z)^H z^{v−1}. Internal increases therefore need only η → 0, not
Hη → 0.

**Corollary B-unif. PROVED.** The bound holds uniformly over an eligible set 𝓧 fixed before selection, with
inf c_*, sup v, sup η.

**Corollary B-M (many particles). PROVED** given (R5): no resampling during the L+4 terminal rounds, and
per-particle fresh randomness (METHODOLOGY §§6.5, 6.6, 6.8). Then
P(S₀ unscored | terminal-start population) ≤ ∏_{particles i in 𝓧} min{1, bound(x_i)}.

**Corollary P1 (distance-one scoring). PROVED.** If x △ S₀ = {j}, then
P_x(S₀ scored during the next round) ≥ a₁(x) = ∫₀¹∏_{e≠G_j}(1 − t q_e(x))dt, where q_e is the probability that
label e changes the state at x. With (R5), N₁ distance-one particles give P(no score in the round) ≤
∏(1 − a₁(x_i)). Numerically a₁ ≥ 0.14 in every design at n = 200 (Table T4c).

**Lemma P (exact first-change progress). PROVED.**
P*(x) = Σ_e s_e ∫₀¹∏_{j≠e}(1−t q_j)dt ≥ s_g[1 − Q_D/(|D|+2)]/(|D|+1) for every label g and set D. With
D = the non-Gibbs labels this gives the explicit c′ ≥ s_g[1−Q_𝔊/(B+4)]/(B+3).

**Prop. U (undo). PROVED.** See Headline 2 and PROOF.md §3.

**Prop. A (one-round sweep). PROVED, but vacuous numerically.** ε₂ ≈ 2.6 here, because extra-for-null
swaps are accepted with O(1) probability.

**Lemmas F (first-failure union over labels), O (order facts), C (binomial domination). PROVED.**

## 2. Proofs

All are in PROOF.md:
- Lemmas F, O, C: §1.
- Lemma P: §2.
- Prop. U: §3.
- Theorem B with Props. B1/B2: §4.
- Prop. A: §5.
- Asymptotics: §6 (PROOF SKETCH).
- CE1, CE2: §7.

The two delicate points were each checked line by line.
- **Prop. B2 slot argument.** It applies Lemma F to the σ-dependent event {e ≺ G_l, e removes l}. This is
  legitimate because σ is 𝓕₀-measurable.
- **Prop. B1 quantifier.** On "no bad, no progress", the missing set stays constant. This needs two things:
  every truth removal is classified bad (truth-for-truth swaps and independence jumps can keep |M| and still
  change the missing set), and ε_add takes its sup over states with the same missing set. Both were wrong in
  an earlier draft; both are fixed, and the numbers below use the corrected code.

## 3. Task 1: one terminal round at φ = 1, and the potential

PROOF.md §0 gives the exact round model:
- the kernels of T09(ii), including the Hastings ratio of the neighbour swap;
- the order is drawn independently of the state (R1), and each label runs once (R2);
- under SR every visited state is scored (R3), and a Gibbs evaluation adjacent to S₀ scores it (R4);
- terminal trajectories are conditionally independent (R5).

The potential V is the two-phase one above. While a truth is missing, V = |M| + a; once all truths are in,
V = |P|.

## 4. Task 3: premises under G, R, SE, BM-∞ (s₀, d fixed)

All entries below are PROOF SKETCH. Finite-n expressions are in PROOF.md §6.

| premise | w.p. → 1? |
|---|---|
| truth deletion at supersets (τ₂) | **yes**: odds ≤ 2p√(n+1)·n^{−M_n(1−o(1))/2} |
| superset leakage at S₀ itself (zero leakage) | **yes**: O_P(s₀√(log p)/√n), heavy-tailed constant (E e^{Z²/2} = ∞) |
| superset leakage for every a ≥ 1, i.e. the sup over W = S₀∪P | needs **NL0(a)**: partial-Z inflation control. Bounded correlation degree (S2–S4, S6) or COH suffices; equicorrelated nulls (S5) fail in rate for p ≳ n^{0.58} |
| uniform deletability ε_del | **yes for a = 1**; needs **UDEL(a)** for a ≥ 2 (this is T24(iv)'s open multi-extra deletion issue, in sharper form) |
| uniform addability ε_add | **yes if one truth is missing** (SE); otherwise needs **BTP** (best-target persistence; fails under cancellation) |
| truth retention at incomplete states | **not implied by SE** (cancellation); needs **TS(𝒵)** (COH suffices) |
| junk leakage at incomplete states | **not implied**: with fixed θ, nulls just below ρ_n can be attractive; needs **TL(𝒵,A)** = TL/NL_η on 𝒵 minus A |
| independence bad acceptance | **not implied in the masked regime**; needs **IND(𝓕)**; bound ≤ min{π₀(Bad), [π₀(W)/π(W)]π(Bad)} |
| rates for (L+4)η → 0 | all of the above at o_P(1/log n) |

Conclusion (PROOF SKETCH): under these conditions, c_* ≥ 1/(B+3) − o_P(1) and (L+4)η → 0. So
P_x(unscored in L+4 rounds) → 0, at rate about n^{−0.07}.

## 5. Task 5: H24 in T21 route (e)

- **H24 cannot be discharged.** Its uniform exit input is false (CE1). Its occupancy input
  K₁(x,{S₀}) ≥ a_n ≥ c_n/2 is never needed.
- **Proposed replacement, route (e′).** T21's proof of (e) (PROOF_v3 §"Route (e)") uses H24 only to obtain
  P(M_H | selection past) ≤ (1−a_n)^H + Hη_n uniformly over eligible states. Theorem B (Cor. B-unif) gives
  P(M_H | selection past) ≤ P(Bin(H,c_*(𝓧)) < v(𝓧)) + Hη(𝓧) under the same filtration conditions: the
  selection uses the available past, future randomness is fresh, and the H rounds at φ = 1 execute with no
  resampling. Every later step of (e) uses only this inequality, its uniformity and its [0,1] cap:
  - the availability term P(A^c);
  - the final-run split into nonlaunch / no eligible particle / A_F;
  - the pilot forward filtration;
  - the capped expectation.
  So (e′) follows verbatim with (1−a_n)^H + Hη_n replaced by P(Bin(H,c_*) < v) + Hη. "H24′" consists only of
  definitions (c_*, v, η are exact functions of the data), so the hypothesis list of (e′) is EX-A, EX-S, SR,
  s₀ + a ≤ K, plus availability.
- **Asymptotic (e′).** With H = L+4, c_*(𝓧) ≥ c > 0 w.p.→1, v(𝓧) bounded and (L+4)η(𝓧) → 0 in probability
  (premises of §4), the conditional failure → 0.
- **Multi-particle (e-M).** P(M_H | population) ≤ ∏_i min{1, bound(x_i)}. This is the route that matches the
  data: many eligible particles, each with a per-particle bound bounded away from 1, are enough.
- **Status.** PROVED (candidate) as an implication; it inherits T21's own conditional status.

## 6. Task 4: evidence

The mimic designs use scripts `bvs_engine.py`, `simulate.py`, `progress_bounds.py`, `round_analysis.py`,
`run_designs.py`, `compare_cprime.py`, `counterexample_H24.py` and `scaling_reps.py`.

**Design setup.**
- p = 20 (4 groups of 5), with S1–S6 covariances copied from `gen_dev_data.R::scenario_covariance`.
- One truth per group with the R pattern: positions (3,2,4,1), β = (1.4, −1.0, 1.8, −1.2), so s₀ = 4.
- n = 200, scales c ∈ {1, 0.5}, noise sd 1. The method standardises y.
- B = min(14, 4, 16) = 4, m = 26 labels, L = 8, H = 12.
- Blocks: complete linkage on 1−|r|, top-down cut, next-fit packing; neighbour graph per §6.4; exact π₀ and d.
- R's RNG is not reproduced: these are numpy re-draws (seed 1), so they mimic the designs but are not the
  same datasets.

**Start law (π₀).**
- S3, S4, S6: supersets of S₀ with 3–7 extras; π₀(S₀) between 1e-11 and 1e-36. This is double counting of
  group-mates across split blocks.
- S2: supersets with 1–3 extras.
- S5: masked. The π₀ mode {0,2,13,14} misses truths 6 and 15 and has log π gap −119.
- π(S₀) ≈ 0.71–0.78 in all designs, and the HPM is S₀ in all.

**Simulated repair from 3000 raw π₀ draws (not S₀), actual round, exact scores.**

| design | scored in round 1 | by round 2 | by round 12 |
|---|---|---|---|
| S1 | 0.84–0.89 | 0.98–0.99 | 1.000 |
| S2 | 0.67–0.71 | 0.93 | 1.000 |
| S3 | 0.41–0.43 | 0.85 | 1.000 |
| S4 | 0.42–0.45 | 0.83–0.85 | 1.000 |
| S5 | 0.11–0.12 | 0.66–0.69 | 1.000 |
| S6 | 0.39–0.46 | 0.82–0.85 | 1.000 |

S5 needs two rounds because a proxy can be deleted only after its truth is added.

**Per-round progress, actual vs proven** (`results/compare_cprime.json`; worst superset state for P*, a = 1, 2).
- Actual (MC, 20000 reps) progress: 0.75–0.89, and progress-or-bad 0.91–0.96.
- Proven constants: P* = 0.53–0.57, c₂ = 0.25–0.47, c_poly = 0.27–0.34, floor 1/(B+3) = 0.143.
- At π₀-mode incomplete starts: c₁ = 1.000 exactly (every missing truth is addable at every family state),
  and actual progress ≈ 1.000.
- The ordering is floor < c_poly < c₂ ≤ P* < actual in every design.
- c = 1 and c = 0.5 give nearly identical constants: the signals are strong at n = 200, p = 20.


**Table T4a — phase 2 (superset families), n = 200, p = 20, B = 4.** "Actual" = Monte Carlo over the
actual round with exact scores (20000 single rounds from the state with the smallest P*); the theorem needs
actual P(progress or bad) ≥ c₂.

| design | a | worst state | actual progress | actual progress-or-bad | P* | c₂ | c_poly | 1/(B+3) |
|---|---|---|---|---|---|---|---|---|
| S1 c=1.0 | 1 | [2, 6, 13, 15, 17] | 0.891 | 0.960 | 0.573 | 0.326 | 0.271 | 0.143 |
| S1 c=1.0 | 2 | [2, 6, 13, 15, 17] | 0.893 | 0.960 | 0.573 | 0.297 | 0.271 | 0.143 |
| S1 c=0.5 | 1 | [2, 6, 13, 15, 17] | 0.828 | 0.943 | 0.547 | 0.343 | 0.270 | 0.143 |
| S1 c=0.5 | 2 | [2, 6, 13, 15, 17] | 0.829 | 0.943 | 0.547 | 0.312 | 0.270 | 0.143 |
| S2 c=1.0 | 1 | [2, 6, 13, 15, 18] | 0.760 | 0.915 | 0.531 | 0.427 | 0.316 | 0.143 |
| S2 c=1.0 | 2 | [2, 6, 13, 15, 18] | 0.754 | 0.916 | 0.531 | 0.397 | 0.316 | 0.143 |
| S2 c=0.5 | 1 | [2, 6, 13, 15, 18] | 0.752 | 0.918 | 0.529 | 0.423 | 0.311 | 0.143 |
| S2 c=0.5 | 2 | [2, 6, 13, 15, 18] | 0.749 | 0.917 | 0.529 | 0.366 | 0.311 | 0.143 |
| S3 c=1.0 | 1 | [2, 6, 13, 15, 17] | 0.772 | 0.913 | 0.541 | 0.460 | 0.340 | 0.143 |
| S3 c=1.0 | 2 | [2, 6, 13, 15, 17] | 0.767 | 0.907 | 0.541 | 0.448 | 0.340 | 0.143 |
| S3 c=0.5 | 1 | [2, 6, 13, 15, 17] | 0.771 | 0.914 | 0.539 | 0.458 | 0.336 | 0.143 |
| S3 c=0.5 | 2 | [2, 6, 13, 15, 17] | 0.771 | 0.912 | 0.539 | 0.446 | 0.336 | 0.143 |
| S4 c=1.0 | 1 | [2, 6, 13, 15, 19] | 0.776 | 0.908 | 0.546 | 0.469 | 0.350 | 0.143 |
| S4 c=1.0 | 2 | [2, 6, 7, 13, 15, 19] | 0.911 | 0.991 | 0.545 | 0.460 | 0.190 | 0.143 |
| S4 c=0.5 | 1 | [2, 5, 6, 13, 15] | 0.737 | 0.922 | 0.513 | 0.468 | 0.291 | 0.143 |
| S4 c=0.5 | 2 | [2, 5, 6, 8, 13, 15] | 0.829 | 0.994 | 0.502 | 0.458 | 0.164 | 0.143 |
| S5 c=1.0 | 1 | [2, 6, 13, 15, 19] | 0.763 | 0.911 | 0.534 | 0.459 | 0.323 | 0.143 |
| S5 c=1.0 | 2 | [2, 6, 13, 15, 19] | 0.761 | 0.912 | 0.534 | 0.446 | 0.323 | 0.143 |
| S5 c=0.5 | 1 | [2, 6, 13, 15, 19] | 0.762 | 0.914 | 0.532 | 0.457 | 0.319 | 0.143 |
| S5 c=0.5 | 2 | [2, 6, 13, 15, 19] | 0.764 | 0.916 | 0.532 | 0.444 | 0.319 | 0.143 |
| S6 c=1.0 | 1 | [2, 6, 12, 13, 15] | 0.755 | 0.915 | 0.529 | 0.435 | 0.312 | 0.143 |
| S6 c=1.0 | 2 | [2, 6, 12, 13, 15] | 0.752 | 0.916 | 0.529 | 0.412 | 0.312 | 0.143 |
| S6 c=0.5 | 1 | [2, 6, 12, 13, 15] | 0.752 | 0.914 | 0.527 | 0.431 | 0.306 | 0.143 |
| S6 c=0.5 | 2 | [2, 6, 12, 13, 15] | 0.755 | 0.917 | 0.527 | 0.406 | 0.306 | 0.143 |

**Table T4b — phase 1 (π₀-mode incomplete start).**

| design | start x | π₀(x) | c₁ | η₁ | a | P*(x) | actual progress | actual progress-or-bad | actual scored in round |
|---|---|---|---|---|---|---|---|---|---|
| S1 c=1.0 | [2, 13, 15] | 0.157 | 1.000 | 1.17 | 1 | 0.838 | 1.000 | 1.000 | 0.908 |
| S1 c=0.5 | [2, 13, 15] | 0.412 | 1.000 | 1.41 | 1 | 0.803 | 0.999 | 0.999 | 0.867 |
| S2 c=1.0 | [1, 2, 12, 13, 15] | 0.001 | 1.000 | 2.09 | 4 | 0.301 | 1.000 | 1.000 | 0.383 |
| S2 c=0.5 | [1, 2, 12, 13, 15] | 0.014 | 1.000 | 1.85 | 4 | 0.342 | 1.000 | 1.000 | 0.482 |
| S3 c=1.0 | [0, 2, 5, 8, 13, 14, 15, 19] | 0.016 | 1.000 | 3.27 | 7 | 0.273 | 1.000 | 1.000 | 0.247 |
| S3 c=0.5 | [0, 2, 5, 8, 13, 14, 15, 19] | 0.028 | 0.984 | 2.33 | 7 | 0.253 | 0.998 | 0.999 | 0.304 |
| S4 c=1.0 | [2, 4, 5, 8, 13, 14, 15, 19] | 0.050 | 1.000 | 2.42 | 7 | 0.272 | 1.000 | 1.000 | 0.289 |
| S4 c=0.5 | [2, 4, 5, 8, 13, 14, 15, 19] | 0.078 | 0.503 | 3.19 | 7 | 0.203 | 0.835 | 0.872 | 0.288 |
| S5 c=1.0 | [0, 2, 13, 14] | 0.396 | 1.000 | 2.36 | 10 | 0.152 | 1.000 | 1.000 | 0.075 |
| S5 c=0.5 | [0, 2, 13, 14] | 0.518 | 0.992 | 2.33 | 10 | 0.150 | 0.999 | 1.000 | 0.099 |
| S6 c=1.0 | [0, 2, 4, 5, 11, 13, 14, 15, 19] | 0.002 | 1.000 | 3.55 | 9 | 0.208 | 1.000 | 1.000 | 0.201 |
| S6 c=0.5 | [0, 2, 4, 5, 13, 14, 15, 19] | 0.007 | 1.000 | 2.77 | 8 | 0.240 | 0.999 | 0.999 | 0.270 |

Every cell satisfies actual ≥ proven constant (a numerical consistency check of Props. B1/B2). S4 at
c = 0.5 is the one design where uniform addability is not ≈ 1 (c₁ = 0.50, actual 0.87).


**Table T4c — Cor. P1 (rigorous one-round scoring bound at distance one, n = 200).** a₁ is the min over
the 20 distance-one states (S₀ minus a truth, or S₀ plus a null); "sim" is the actual one-round scoring
frequency at the same state (10000 reps).

| design | min a₁ (state) | its sim | mean a₁ | min sim |
|---|---|---|---|---|
| S1 c=1.0 | 0.375 (extra 17) | 0.893 | 0.476 | 0.889 |
| S1 c=0.5 | 0.439 (extra 17) | 0.823 | 0.533 | 0.811 |
| S2 c=1.0 | 0.162 (del-truth 2) | 0.394 | 0.516 | 0.394 |
| S2 c=0.5 | 0.175 (del-truth 2) | 0.418 | 0.552 | 0.418 |
| S3 c=1.0 | 0.159 (del-truth 13) | 0.284 | 0.497 | 0.273 |
| S3 c=0.5 | 0.184 (del-truth 13) | 0.299 | 0.501 | 0.288 |
| S4 c=1.0 | 0.184 (del-truth 13) | 0.277 | 0.503 | 0.275 |
| S4 c=0.5 | 0.183 (del-truth 13) | 0.304 | 0.500 | 0.304 |
| S5 c=1.0 | 0.161 (del-truth 13) | 0.246 | 0.500 | 0.246 |
| S5 c=0.5 | 0.165 (del-truth 13) | 0.276 | 0.506 | 0.276 |
| S6 c=1.0 | 0.139 (del-truth 6) | 0.267 | 0.491 | 0.267 |
| S6 c=0.5 | 0.183 (del-truth 13) | 0.287 | 0.502 | 0.287 |

With (R5), N₁ particles at distance one give P(no score in that round) ≤ ∏(1 − a₁(x_i)) ≤ 0.86^{N₁}
in every design (e.g. ≤ 0.011 for N₁ = 30). This is the one rigorous bound in this report that is
non-vacuous at n = 200. The worst distance-one state is S₀ minus a truth: look-alike additions there
compete with the scoring Gibbs label.

**Bad-event rates.** η₂(a=1) = 0.37–0.64 and η₁ = 1.2–3.3 per round at n = 200. This makes Theorem B
vacuous at this size for a single particle; see Headline 5. The cause is the sup over a family together with
O(1) superset posterior mass.

**Scaling** (`results/scaling_reps.json`, 10 design seeds, c = 0.5): see the table appended below by the
script summary.

**CE1** (`results/counterexample_H24.json`): the worst boundary state of 𝓡_d (d = 1, 2) has a one-round exit
probability (20000 reps) of:

| design | one-round exit |
|---|---|
| S1 | 0.16–0.22 |
| S2 | 0.62–0.79 |
| S3 | 0.83–0.94 |
| S4 | 0.80–0.98 |
| S5 | 0.83–0.97 |
| S6 | 0.72–0.97 |

(L+4)·exit ranges from 1.9 to 11.8.

## 7. What fails, and why

- **Uniform-over-𝓡_d formulations (H24, LK_d, EXIT_d).** 𝓡_d contains boundary states with junk extras and
  a missing truth, and at those states a look-alike is added with probability ≈ 1 (CE1). Start-adapted
  families 𝒵(x) and 𝒮_a fix the quantifier, but their sups are still crude at finite n.
- **Single-round sweep (Prop. A).** It is vacuous because extra-for-null swaps at supersets are accepted with
  O(1) probability. This is structural: replacing a poor junk extra by a better one is favoured.
- **First-change progress (P*).** It is small at incomplete states, where many neutral changes occur. Theorem B
  avoids this through target persistence (Props. B1/B2).
- **Finite n.** At n = 200, π(S₀) ≈ 0.72, so leakage-type bad events have O(1) rate per round, and H·η is
  vacuous although repair is fast. A drift (Lyapunov) argument would be needed: OPEN.
- **Cancellation.** BTP and TS fail under cancellation, and the layered version is OPEN.
- **Production B = 14–16.** The proven phase-2 floor 1/(B+3) is about 0.06. The actual non-Gibbs acceptance at
  near-truth states is small, so c₂ is much larger, but the proven worst case is weak.

## 8. Needs escalation (HQ decisions)

1. **Retire H24, and rewrite T21 route (e) as (e′) plus (e-M)** (§5). The T21 STATEMENT and the LOCKED
   register's open item "H24" would then point to Theorem B.
2. **Retire LK_d, EXIT_d and GAIN_d from the T24 hypothesis list.** Replace them with the exact constants of
   Theorem B, and with the asymptotic sufficient conditions NL0, UDEL, TS, TL(𝒵,A), BTP, IND as new inventory
   codes (PROOF.md §6).
3. **Make the multi-particle route explicit.** It is the mechanism consistent with the p ≫ n data (Gibbs
   scores ≈ 98%, local search repaired 0). It needs (R5) to be confirmed against the implementation: no
   resampling in burn-in or measured rounds, and per-particle streams.
4. **Confirm the SR reading with Felipe.** Theorem B uses only (R3), that every visited state is scored,
   which already requires the Gibbs conditional to score the configuration it lands in.

## 9. Outside scope (not attempted)

- PIP repair (T24(iii) via T23 basins).
- Pilot-phase repair.
- The drift/Lyapunov finite-n refinement.
- The layered cancellation version.
- Verification on the actual p = 500/1000 datasets.
- T38 delivery (that near-truth particles exist at terminal start).

## 10. Confidence cards

| target | statement | P(true) | P(provable at reasonable cost) | crux | method change needed? |
|---|---|---|---|---|---|
| T1 round model + potential | §0, Lemmas F/O/C/P | 0.97 | done | R1 (order independent of state) and R3 (scoring) readings | no |
| Theorem B (restated T24) | §1 | 0.90 | done (review needed) | bookkeeping of the family closure and the bad/neutral/progress classification; Prop. B2 slot step | no |
| Prop. U (EXIT_d resolution) | §1 | 0.93 | done | that every undo is either V-raising or slot-hiding | no |
| Asymptotic premises (Task 3) | §4 | 0.75 overall (conditional on the named extras); 0.85 for the automatic items (truth deletion at supersets, leakage at S₀, deletability at a = 1) | 0.5 (needs uniform log-BF expansions of EXP type over finite families; IND in the masked regime is genuinely open) | IND, TL(𝒵,A), NL0(a) including a = 1 for correlated nulls, UDEL(a≥2) | no |
| CE1 (H24 false) | §7 | 0.9 (numerical: reproducible); asymptotic sketch 0.85 | 0.8 | o_l(Y) → 1 at look-alike boundary states | no |
| CE2 (form needs factor v) | §7 | 0.99 | done | — | no |
| T21 (e′) and (e-M) | §5 | 0.9 | 0.9 | (R5) conditional independence in terminal rounds | no (confirm the implementation's streams) |
| Useful finite-n single-particle bound at n = 200 | — | 0.2 for the current proof technique | 0.3 (drift argument) | O(1) superset leakage | no |
